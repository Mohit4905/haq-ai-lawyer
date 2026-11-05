"""Anti-hallucination guard. Deterministic code, no LLM.

Every model reply is scanned BEFORE the user sees it:
  1. Statute references (Section / धारा / Article / Order / Rule + act name) must exist in the
     verified KB. Unknown acts or sections are violations.
  2. Case-law citations ("X v. Y", AIR / SCC citations, "the Supreme Court held") are always
     violations: the KB has no verified case law, so the product policy is to cite none.
  3. Repealed / replaced laws (IPC, CrPC, Payment of Wages Act ...) are violations, with the
     replacement suggested.
  4. Numbers with time units ("within 45 days") that are not supported by the KB, the code's
     own calculations, or the user's words are soft warnings (shown, not removed).
If there are violations, the engine asks the model to rewrite once; if violations remain,
the offending sentences are removed and the user is told.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from .kb import _norm, base_section, known_acts, load_kb, sections_for_act
from .rules import OUTDATED_LAWS

SECTION_RE = re.compile(
    r"(?i)(?:\bsections?|\bsecs?\.?|\bu/s\.?|\bs\.(?=\s*\d)|धारा|धाराओं|कलम|பிரிவு|ధారా|ಸೆಕ್ಷನ್|ধারা)\s*"
    r"(\d{1,4}[A-Z]?)((?:\s*\(\s*[0-9a-z]{1,4}\s*\))*)"
)
ARTICLE_RE = re.compile(r"(?i)\b(?:article|art\.)\s*(\d{1,3}[A-Z]?)")
ORDER_RE = re.compile(r"(?i)\border\s+([IVXL]{1,7}|\d{1,2})\b(?:\s*,?\s*rule\s*\d+)?")
ACT_RE = re.compile(
    r"\b((?:[A-Z][A-Za-z\.\-()]*\s+){0,7}?(?:Act|Code|Sanhita|Adhiniyam|Rules|Regulations|Scheme))\b,?\s*(?:of\s+)?(\d{4})?"
)
HINDI_ACT_RE = re.compile(r"([ऀ-ॿ]+(?:\s[ऀ-ॿ]+){0,4}\s(?:अधिनियम|संहिता))")
CASE_RES = [
    re.compile(r"\b[A-Z][A-Za-z.&']+(?:\s+[A-Z][A-Za-z.&']+){0,5}\s+(?:v\.|vs\.?|versus)\s+[A-Z][A-Za-z]"),
    re.compile(r"\bAIR\s+\d{4}\b"),
    re.compile(r"\(\d{4}\)\s*\d+\s*SCC\b"),
    re.compile(r"\b\d{4}\s+(?:SCC|SCR|INSC)\b"),
    re.compile(r"(?i)\bSCC\s+Online\b"),
    re.compile(r"(?i)\b(?:supreme court|high court)\s+(?:has\s+)?(?:held|ruled|observed|said)\b"),
    re.compile(r"(?i)\b(?:landmark|in the case of)\b"),
    re.compile(r"(?:सुप्रीम कोर्ट|उच्च न्यायालय|उच्चतम न्यायालय|हाई कोर्ट)\s*(?:ने)\s*(?:कहा|फैसला|निर्णय)"),
]
NUM_UNIT_RE = re.compile(
    r"(?i)(\d{1,3})\s*(?:-|to)?\s*(working days?|days?|months?|years?|weeks?|hours?|दिन|दिनों|महीने|महीनों|माह|साल|वर्ष|घंटे)"
)

# "<word> Code" phrases that are not laws
NON_LAW_PREFIX = {"pin", "postal", "qr", "ifsc", "promo", "coupon", "dress", "discount", "otp", "error", "source", "hsn", "sac", "area", "std", "bar", "zip", "swift", "micr", "referral", "verification"}

# phrases that are generic, not legal claims, and should not trigger the number check
_NUM_WHITELIST = {"24 hours", "7 days"}


@dataclass
class GuardReport:
    verified: list = field(default_factory=list)  # list of (mention, kb_id or act)
    violations: list = field(default_factory=list)  # list of dicts {type, text, why, suggestion?}
    warnings: list = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.violations

    def to_dict(self) -> dict:
        return {"verified": self.verified, "violations": self.violations, "warnings": self.warnings, "ok": self.ok}


_ALIAS_RX_CACHE: dict = {}


def _alias_regex(acts: dict[str, str]):
    """One regex per known act alias, tolerant of spaces/punctuation between words."""
    key = id(acts), len(acts)
    if key not in _ALIAS_RX_CACHE:
        from .kb import ACT_ALIASES, load_kb

        names: dict[str, str] = {}
        for e in load_kb():
            act = e["act"]
            for a in [act, re.sub(r",?\s*\d{4}$", "", act), *ACT_ALIASES.get(act, [])]:
                if len(_norm(a)) >= 3:
                    names[a] = act
        pats = []
        for a, act in sorted(names.items(), key=lambda x: -len(x[0])):
            words = [re.escape(w) for w in re.split(r"[\s,.\-]+", a) if w]
            pats.append((re.compile(r"(?i)(?<![\w])" + r"[\s,.\-]*".join(words) + r"(?![\w])"), act))
        _ALIAS_RX_CACHE.clear()
        _ALIAS_RX_CACHE[key] = pats
    return _ALIAS_RX_CACHE[key]


def _nearby_act(text: str, start: int, end: int, acts: dict[str, str]) -> tuple[str | None, str | None]:
    """Return (canonical act, raw act seen) ATTACHED to a mention: 'Section 69 of the X Act'
    (act starts within ~45 chars after) or 'X Act, Section 69' / 'X Act की धारा 69' (act ends within ~35 chars before).
    An act merely mentioned somewhere nearby is NOT attached (avoids misattribution)."""
    after = text[end : min(len(text), end + 60)]
    before = text[max(0, start - 60) : start]
    for old, info in OUTDATED_LAWS.items():
        for alias in info["aliases"]:
            rx = rf"(?<![A-Za-z]){re.escape(alias)}(?![A-Za-z])"
            m1 = re.search(rx, after)
            m2 = None
            for m2 in re.finditer(rx, before):
                pass
            if (m1 and m1.start() <= 45) or (m2 and len(before) - m2.end() <= 35):
                return None, alias
    best, best_d = None, 10**9
    for rx, act in _alias_regex(acts):
        m = rx.search(after)
        if m and m.start() <= 45 and m.start() < best_d:
            best, best_d = act, m.start()
        last = None
        for last in rx.finditer(before):
            pass
        if last is not None:
            d = len(before) - last.end()
            if d <= 35 and d < best_d:
                best, best_d = act, d
    raw = None
    m = ACT_RE.search(after[:50]) or HINDI_ACT_RE.search(before[-40:] + after[:50])
    if m:
        raw = m.group(0).strip()
    return best, raw


def check(text: str, allowed_ids: set[str] | None = None, support_text: str = "") -> GuardReport:
    rep = GuardReport()
    acts = known_acts()

    # 3. outdated laws (checked first; replacement suggestions are useful to the user)
    for old, info in OUTDATED_LAWS.items():
        for alias in info["aliases"]:
            for m in re.finditer(rf"(?<![A-Za-z]){re.escape(alias)}(?![A-Za-z])", text):
                # allow mentions that explicitly say it was replaced
                ctx = text[max(0, m.start() - 80) : m.end() + 80].lower()
                if any(w in ctx for w in ("replaced", "repealed", "earlier", "old ", "no longer", "जगह", "पुराना", "पहले")):
                    continue
                rep.violations.append(
                    {"type": "outdated_law", "text": m.group(0), "why": f"{old} {info['status']}", "suggestion": info["replacement"]}
                )

    # 2. case law
    for rx in CASE_RES:
        for m in rx.finditer(text):
            rep.violations.append({"type": "case_law", "text": m.group(0), "why": "Case-law citations are not allowed: none are in the verified library."})

    # 1a. sections
    for m in SECTION_RE.finditer(text):
        sec = m.group(1)
        act, raw = _nearby_act(text, m.start(), m.end(), acts)
        if act:
            if base_section(sec) in sections_for_act(act):
                rep.verified.append([m.group(0).strip(), act])
            else:
                rep.violations.append({"type": "unknown_section", "text": f"{m.group(0).strip()} of {act}", "why": "This section of this Act is not in the verified library."})
        elif raw and any(raw == a for info in OUTDATED_LAWS.values() for a in info["aliases"]):
            continue  # already reported as outdated
        else:
            # no act named nearby: accept only if exactly-matching section exists among allowed ids
            pool = [e for e in load_kb() if (allowed_ids is None or e["id"] in allowed_ids) and e.get("section")]
            if any(base_section(str(e["section"])) == base_section(sec) for e in pool):
                rep.warnings.append({"type": "ambiguous_section", "text": m.group(0).strip(), "why": "Section mentioned without naming the Act."})
            else:
                rep.violations.append({"type": "unknown_section", "text": m.group(0).strip(), "why": f"Not in the verified library{f' (near: {raw})' if raw else ''}."})

    # 1b. articles / orders (Limitation Act articles, CPC orders)
    for rx, kind in ((ARTICLE_RE, "art"), (ORDER_RE, "order")):
        for m in rx.finditer(text):
            act, _ = _nearby_act(text, m.start(), m.end(), acts)
            key = base_section(f"{'article' if kind == 'art' else 'order'} {m.group(1)}")
            ok = act is not None and key in sections_for_act(act)
            if ok:
                rep.verified.append([m.group(0).strip(), act])
            else:
                rep.violations.append({"type": "unknown_provision", "text": m.group(0).strip(), "why": "Not in the verified library."})

    # 1c. act names that are not in the KB at all
    seen = set()
    for m in ACT_RE.finditer(text):
        raw = m.group(1).strip()
        n = _norm(raw)
        if n in seen or len(raw.split()) < 2 or raw.split()[-2].lower() in NON_LAW_PREFIX:
            continue
        seen.add(n)
        if any(n.endswith(a) or a.endswith(n) for a in acts if len(a) > 6):
            continue
        if any(_norm(alias) and _norm(alias) in n for info in OUTDATED_LAWS.values() for alias in info["aliases"]):
            continue
        if re.match(r"(?i)^(the\s+)?(this|that|an?|any|such)\s", raw) or raw.split()[0].lower() in {"the", "this", "that", "an", "a"} and len(raw.split()) <= 2:
            continue
        rep.violations.append({"type": "unknown_act", "text": raw + (f", {m.group(2)}" if m.group(2) else ""), "why": "This law is not in the verified library."})

    # 4. numbers with units (soft)
    sup = _norm_space(support_text.lower())
    for m in NUM_UNIT_RE.finditer(text):
        phrase = _norm_space(m.group(0).lower())
        n, unit = m.group(1), m.group(2).lower()
        if phrase in _NUM_WHITELIST:
            continue
        unit_root = unit.rstrip("s")[:3]
        if re.search(rf"\b{n}\s*(?:-|to)?\s*{re.escape(unit_root)}", sup) or (n + " " + unit) in sup:
            continue
        rep.warnings.append({"type": "unsupported_number", "text": m.group(0), "why": "Time period not found in the verified library or calculations."})

    # declared citation ids
    return rep


def check_declared_ids(ids: list[str], allowed_ids: set[str]) -> list[dict]:
    kb_ids = {e["id"] for e in load_kb()}
    out = []
    for i in ids or []:
        if i not in kb_ids:
            out.append({"type": "bad_citation_id", "text": i, "why": "Cited id does not exist in the verified library."})
    return out


def _norm_space(s: str) -> str:
    return re.sub(r"\s+", " ", s)


_ABBREV = re.compile(r"(?i)(?:\bv|\bvs|\bs|\bsec|\bno|\brs|\bmr|\bmrs|\bms|\bdr|\bltd|\bco|\bart|\bu/s|\bi\.e|\be\.g)\.$")


def _split_sentences(line: str) -> list[str]:
    parts = re.split(r"(?<=[.!?।])\s+", line)
    out: list[str] = []
    for p in parts:
        if out and _ABBREV.search(out[-1]):
            out[-1] += " " + p  # "Ram v." + "Shyam ..." belong together
        else:
            out.append(p)
    return out


def strip_violations(text: str, rep: GuardReport) -> str:
    """Last-resort: remove sentences that still contain violations."""
    # match on the raw mention (e.g. "s.55"), not the "X of <Act>" label we build for messages
    bad = [v["text"].split(" of ")[0] if v["type"] == "unknown_section" else v["text"] for v in rep.violations]
    if not bad:
        return text
    removed = 0
    out_lines = []
    for line in text.split("\n"):  # keep line structure (lists, headings) intact
        if not any(b and b in line for b in bad):
            out_lines.append(line)
            continue
        sents = _split_sentences(line)
        keep = [s for s in sents if not any(b and b in s for b in bad)]
        if len(keep) == len(sents):  # violation spans a sentence boundary we couldn't resolve: drop the line
            keep = []
        removed += len(sents) - len(keep)
        prefix = re.match(r"^\s*(?:[-*•]|\d+[.)])\s+", line)
        if keep:
            joined = " ".join(keep)
            if prefix and not joined.startswith(prefix.group(0)):
                joined = prefix.group(0) + joined.lstrip()
            out_lines.append(joined)
    out = "\n".join(out_lines)
    if removed:
        out += (
            "\n\n_⚠️ I removed a legal reference I could not verify. "
            "Please confirm the exact law with a lawyer or free legal aid (NALSA helpline 15100)._"
        )
    return out


# ---------------------------------------------------------------- language
SCRIPTS = {
    "Devanagari": (0x0900, 0x097F),
    "Bengali": (0x0980, 0x09FF),
    "Gurmukhi": (0x0A00, 0x0A7F),
    "Gujarati": (0x0A80, 0x0AFF),
    "Odia": (0x0B00, 0x0B7F),
    "Tamil": (0x0B80, 0x0BFF),
    "Telugu": (0x0C00, 0x0C7F),
    "Kannada": (0x0C80, 0x0CFF),
    "Malayalam": (0x0D00, 0x0D7F),
    "Arabic": (0x0600, 0x06FF),  # Urdu
}
HINGLISH_WORDS = {
    "hai", "hain", "nahi", "nahin", "mera", "meri", "mere", "kya", "kaise", "raha", "rahi", "diya", "kiya", "paisa", "paise",
    "mujhe", "maine", "bhi", "aur", "lekin", "kar", "karna", "ko", "se", "ka", "ki", "ke", "tha", "thi", "wala", "abhi",
    "bol", "bola", "de", "dena", "chahiye", "kab", "kyun", "sab", "hua", "hoga", "mein", "malik", "naukri", "tankhwah",
}


def hinglish_score(text: str) -> float:
    words = re.findall(r"[a-zA-Z]+", text.lower())
    return sum(w in HINGLISH_WORDS for w in words) / len(words) if words else 0.0


def detect_script(text: str) -> str:
    counts = {k: 0 for k in SCRIPTS}
    latin = 0
    for ch in text:
        o = ord(ch)
        if ch.isascii() and ch.isalpha():
            latin += 1
            continue
        for k, (a, b) in SCRIPTS.items():
            if a <= o <= b:
                counts[k] += 1
                break
    best = max(counts, key=counts.get)
    # mixed messages (Hindi question + pasted English notice): substantial native text wins
    if counts[best] > 0 and (counts[best] > latin * 0.5 or (counts[best] >= 25 and counts[best] > latin * 0.2)):
        return best
    words = re.findall(r"[a-zA-Z]+", text.lower())
    if words and sum(w in HINGLISH_WORDS for w in words) / len(words) > 0.12:
        return "Hinglish"
    return "Latin"
