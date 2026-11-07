"""Verified legal knowledge base (KB).

`kb/laws.json` is hand-curated: every entry was checked against an official source
(India Code, Gazette, ministry or regulator sites) and carries its URL. Only entries
with "verified": true are ever shown to the model or allowed as citations.
"""
from __future__ import annotations

import json
import re
from functools import lru_cache

from .config import ROOT

KB_PATH = ROOT / "kb" / "laws.json"


@lru_cache(maxsize=1)
def load_kb() -> list[dict]:
    with open(KB_PATH, encoding="utf-8") as f:
        data = json.load(f)
    return [e for e in data if e.get("verified")]


def by_id() -> dict[str, dict]:
    return {e["id"]: e for e in load_kb()}


# Hand-picked library per problem type. Deterministic retrieval beats embeddings at this
# size: predictable, auditable, testable, free, and it keeps prompts inside free-tier limits.
_AID = ["FACT-NALSA-HELPLINE", "LSA1987-S12", "FACT-LOKADALAT-PRELITIGATION", "FACT-TELE-LAW", "FACT-ERSS-112", "FACT-TELEMANAS"]
_COI = ["COI-ART12", "COI-ART14", "COI-ART15", "COI-ART17", "COI-ART19", "COI-ART21", "COI-ART21A", "COI-ART22", "COI-ART23", "COI-ART25", "COI-ART32", "COI-ART51A"]
_CRIMINAL = ["FACT-BNS-BNSS-COMMENCEMENT", "BNS2023-S358", "BNSS2023-S531", "BNSS2023-S173", "BNS2023-S318", "BNS2023-S316", "FACT-CYBER-1930"]
CATEGORY_IDS: dict[str, list[str]] = {
    "tenancy": ["ICA1872-S73", "MTA2021-S11", "FACT-MTA-STATUS", "FACT-MTA-STATE-ADOPTION", "LIM1963-ART55", "CPC1908-O37", "MED2023-S1", *_AID],
    "consumer": ["CPA2019-S2-7", "CPA2019-S2-11", "CPA2019-S2-47", "CPA2019-S35", "CPA2019-S39", "CPA2019-S69", "CPA2019-S37",
                 "CPJURIS2021-R3-5", "CPCDRC2020-R7", "CPECOM2020-R4-5", "CPECOM2020-R4-10", "CPECOM2020-R6-3",
                 "FACT-NCH-HELPLINE", "FACT-EJAGRITI-PORTAL", "LSA1987-S22A", "LSA1987-S22C", *_AID],
    "salary": ["FACT-LABOUR-CODES-COMMENCEMENT", "COW2019-S2K", "FACT-COW-NO-WAGE-CEILING", "COW2019-S17", "COW2019-S18", "COW2019-S45",
               "COW2019-S51", "COW2019-S57", "COW2019-S25", "COW2019-S69", "FACT-SAMADHAN-PORTAL", "LIM1963-ART7", "BNS2023-S316", *_AID],
    "cheque_bounce": ["NIA1881-S138", "NIA1881-S142-1", "NIA1881-S142-2", "NIA1881-S143A", "NIA1881-S147", "FACT-RBI-CHEQUE-VALIDITY", "CPC1908-O37", *_AID],
    "notice": ["CPC1908-S80", "NIA1881-S138", "CPA2019-S69", "LIM1963-ART55", "COW2019-S45", "MTA2021-S11", "ICA1872-S73", *_AID],
    "cyber_fraud": ["FACT-CYBER-1930", "FACT-RBIOS2026-ELIGIBILITY", "FACT-RBIOS2026-COMPENSATION", "FACT-RBI-CMS-PORTAL", "BNSS2023-S173", "BNS2023-S318", *_AID],
    # topic retrieval (retrieve_for) adds the provisions for what was asked; this is the fallback set
    "general_legal": ["COI-ART14", "COI-ART19", "COI-ART21", "COI-ART32", "COI-ART226", *_CRIMINAL, "ICA1872-S73", "CPA2019-S2-9", "FACT-NCH-HELPLINE", *_AID],
    "out_of_scope": [*_CRIMINAL, "COI-ART14", "COI-ART21", "COI-ART22", "COI-ART32", *_AID],
    "other": [*_AID],
}
# library for the short replies to off-topic / unsafe messages (only what a redirect might name)
ASIDE_IDS = ["FACT-CYBER-1930", "FACT-NCH-HELPLINE", "FACT-NALSA-HELPLINE", "FACT-ERSS-112"]


def retrieve(category: str | None, limit: int = 30) -> list[dict]:
    ids = CATEGORY_IDS.get(category or "other", CATEGORY_IDS["other"])
    idx = by_id()
    return [idx[i] for i in ids if i in idx][:limit]


# Topic -> verified provisions. Matched against the user's question, so the law offered to the model
# (and allowed past the guard) depends on what was asked, not only on the case's category.
_FR = ["COI-ART12", "COI-ART14", "COI-ART15", "COI-ART16", "COI-ART17", "COI-ART18", "COI-ART19", "COI-ART19-2", "COI-ART20", "COI-ART21",
       "COI-ART21A", "COI-ART22", "COI-ART23", "COI-ART24", "COI-ART25", "COI-ART26", "COI-ART29", "COI-ART30", "COI-ART32", "COI-ART226"]
TOPICS: list[tuple[str, list[str]]] = [
    (r"fundamental rights?|मौलिक अधिकार|maulik adhikar|part iii|constitution(?:al)? rights?", [*_FR, "COI-ART51A"]),
    (r"fundamental dut|मौलिक कर्तव्य|51a", ["COI-ART51A"]),
    (r"equal|discriminat|untouchab|caste|reservation|samanta|समानता|भेदभाव|abolition of titles|titles? from (?:a )?foreign",["COI-ART12", "COI-ART14", "COI-ART15", "COI-ART16", "COI-ART17", "COI-ART18"]),
    (r"speech|expression|free(?:dom)? to|freedom of|protest|assembl|association|union|criticis|social media post|बोलने|अभिव्यक्ति", ["COI-ART19", "COI-ART19-2"]),
    (r"life|liberty|privacy|jeevan|जीवन|स्वतंत्रता|article\s*21\b", ["COI-ART21"]),
    (r"educat|school|shiksha|शिक्षा", ["COI-ART21A", "COI-ART29", "COI-ART30"]),
    (r"arrest|warrant|custody|detain|detention|police station|giraftar|गिरफ्त|हिरासत|24 hours", ["BNSS2023-S35", "BNSS2023-S47", "BNSS2023-S48", "BNSS2023-S58", "COI-ART22", "COI-ART21", "BNSS2023-S173"]),
    (r"self.?incriminat|double jeopardy|punished twice|retrospective|retroactive|witness against", ["COI-ART20"]),
    (r"traffick|forced labour|bonded|begar|child labour|बाल श्रम", ["COI-ART23", "COI-ART24"]),
    (r"religio|dharm|धर्म|worship|convert", ["COI-ART25", "COI-ART26"]),
    (r"minorit|alpsankhyak|अल्पसंख्यक|language|culture", ["COI-ART29", "COI-ART30"]),
    (r"writ|habeas|mandamus|certiorari|quo warranto|high court|supreme court|remed(?:y|ies) for (?:my )?rights", ["COI-ART32", "COI-ART226"]),
    (r"theft|thief|stole|stolen|chori|chor\b|चोरी|चोर", ["BNS2023-S303", "BNSS2023-S173", "FACT-BNS-BNSS-COMMENCEMENT"]),
    (r"\bfir\b|police complaint|एफआईआर|zero fir", ["BNSS2023-S173"]),
    (r"cheat|fraud|scam|dhokha|धोखा|ठगी", ["BNS2023-S318", "FACT-CYBER-1930", "BNSS2023-S173"]),
    (r"\bipc\b|\bcrpc\b|bns|bnss|new criminal law|evidence act|sakshya", ["FACT-BNS-BNSS-COMMENCEMENT", "BNS2023-S358", "BNSS2023-S531"]),
    (r"consumer|refund|defect|warranty|deficien|e-?commerce|upbhokta|उपभोक्ता", ["CPA2019-S2-9", "CPA2019-S2-7", "CPA2019-S2-11", "CPA2019-S35", "CPA2019-S39", "CPA2019-S69", "FACT-NCH-HELPLINE", "FACT-EJAGRITI-PORTAL"]),
    (r"divorce|talaq|talak|तलाक|judicial separation|living separately from (?:my )?(?:wife|husband|spouse)|mutual consent divorce|end (?:my|our|the) marriage",["HMA1955-S13", "HMA1955-S13B", "HMA1955-S14", "FACT-NALSA-HELPLINE"]),
    (r"terminat|fired|sack|dismiss|retrench|lay ?off|notice period|naukri se nikal|नौकरी से निकाल", ["IRC2020-S70", "IRC2020-S2ZH", "IRC2020-S2ZR", "FACT-LABOUR-CODES-COMMENCEMENT", "ICA1872-S73"]),
]


def retrieve_for(category: str | None, text: str, limit: int = 34) -> list[dict]:
    """The category's library plus the provisions for the topics named in the question.
    Topic matches come first (they are what was asked about)."""
    import re as _re

    ids: list[str] = []
    m = _re.findall(r"(?i)\barticle\s*(\d{1,3}[A-Z]?)", text or "")
    ids += [f"COI-ART{n.upper()}" for n in m]  # "What does Article 21 say?"
    for rx, lst in TOPICS:
        if _re.search(rx, text or "", _re.I):
            ids += lst
    ids += CATEGORY_IDS.get(category or "other", CATEGORY_IDS["other"])
    idx = by_id()
    return [idx[i] for i in dict.fromkeys(ids) if i in idx][:limit]


def render_for_prompt(entries: list[dict], max_plain: int = 330) -> str:
    lines = []
    for e in entries:
        s = str(e.get("section") or "")
        sec = "" if not s else (f" {s}" if s.lower().startswith(("art", "order", "rule", "schedule")) else f" s.{s}")
        plain = e["plain"] if len(e["plain"]) <= max_plain else e["plain"][:max_plain].rsplit(" ", 1)[0] + "…"
        lines.append(f"[{e['id']}] {e['act']}{sec}: {plain}")
    return "\n".join(lines)


def public_entry(e: dict) -> dict:
    return {k: e.get(k) for k in ("id", "act", "section", "title", "plain", "source_url", "source_type")}


# ---------------------------------------------------------------- act name index
def _norm(s: str) -> str:
    # keep letters of any script (Hindi act names must still match); drop spaces/punctuation
    return re.sub(r"[\W_]", "", s.lower())


ACT_ALIASES: dict[str, list[str]] = {
    # canonical act name in KB  -> aliases people/models use
    "Consumer Protection Act, 2019": ["Consumer Protection Act", "CPA 2019", "CP Act", "उपभोक्ता संरक्षण अधिनियम"],
    "Negotiable Instruments Act, 1881": ["Negotiable Instruments Act", "NI Act", "N.I. Act", "परक्राम्य लिखत अधिनियम"],
    "Code on Wages, 2019": ["Code on Wages", "Wage Code", "वेतन संहिता", "मजदूरी संहिता"],
    "Indian Contract Act, 1872": ["Indian Contract Act", "Contract Act", "भारतीय संविदा अधिनियम"],
    "Model Tenancy Act, 2021": ["Model Tenancy Act", "आदर्श किरायेदारी अधिनियम"],
    "Limitation Act, 1963": ["Limitation Act", "परिसीमा अधिनियम"],
    "Code of Civil Procedure, 1908": ["Code of Civil Procedure", "CPC", "C.P.C.", "सिविल प्रक्रिया संहिता"],
    "Legal Services Authorities Act, 1987": ["Legal Services Authorities Act", "विधिक सेवा प्राधिकरण अधिनियम"],
    "Bharatiya Nyaya Sanhita, 2023": ["Bharatiya Nyaya Sanhita", "BNS", "भारतीय न्याय संहिता"],
    "Bharatiya Nagarik Suraksha Sanhita, 2023": ["Bharatiya Nagarik Suraksha Sanhita", "BNSS", "भारतीय नागरिक सुरक्षा संहिता"],
    "Mediation Act, 2023": ["Mediation Act"],
    "Constitution of India": ["Constitution of India", "Indian Constitution", "Constitution", "भारत का संविधान", "संविधान"],
    "Commercial Courts Act, 2015": ["Commercial Courts Act"],
    "Industrial Relations Code, 2020": ["Industrial Relations Code", "IR Code"],
    # "Industrial Relations Code" belongs to its own entries now (s.70 etc.), not to the commencement fact
    "Four Labour Codes (Code on Wages, 2019; Industrial Relations Code, 2020; Code on Social Security, 2020; Occupational Safety, Health and Working Conditions Code, 2020)": [
        "Labour Codes", "Code on Social Security", "Occupational Safety, Health and Working Conditions Code", "श्रम संहिता"],
    "Hindu Marriage Act, 1955": ["Hindu Marriage Act", "HMA", "हिंदू विवाह अधिनियम", "हिन्दू विवाह अधिनियम"],
    "Four Labour Codes": ["Labour Codes"],
    "Bharatiya Nyaya Sanhita, 2023 / Bharatiya Nagarik Suraksha Sanhita, 2023": ["Bharatiya Nyaya Sanhita", "BNS", "Bharatiya Nagarik Suraksha Sanhita", "BNSS"],
    "Code on Wages (Central) Rules, 2026": ["Code on Wages (Central) Rules", "Central Rules"],
    "Ministry of Labour & Employment (SAMADHAN portal)": ["SAMADHAN", "Samadhan portal"],
    "Reserve Bank - Integrated Ombudsman Scheme, 2026": ["RBI Integrated Ombudsman Scheme", "Integrated Ombudsman Scheme", "RB-IOS", "RBI Ombudsman Scheme", "Ombudsman Scheme"],
    "Consumer Protection (E-Commerce) Rules, 2020": ["E-Commerce Rules", "Consumer Protection (E-Commerce) Rules", "ई-कॉमर्स नियम"],
    "Consumer Protection (Consumer Disputes Redressal Commissions) Rules, 2020": ["Consumer Disputes Redressal Commissions Rules"],
    "Consumer Protection (Jurisdiction of the District Commission, the State Commission and the National Commission) Rules, 2021": ["Jurisdiction Rules", "Consumer Protection Jurisdiction Rules"],
}


def known_acts() -> dict[str, str]:
    """normalised alias -> canonical act, restricted to acts actually present in the KB."""
    present = {e["act"] for e in load_kb()}
    out: dict[str, str] = {}
    for act in present:
        out[_norm(act)] = act
        out[_norm(re.sub(r",?\s*\d{4}$", "", act))] = act
        for a in ACT_ALIASES.get(act, []):
            out[_norm(a)] = act
    # rules / schemes that are recorded in the KB as "acts"
    return out


def sections_for_act(act: str) -> set[str]:
    out = set()
    for e in load_kb():
        if e["act"] == act and e.get("section"):
            out.add(base_section(str(e["section"])))
    return out


_ROMAN = {"i": 1, "v": 5, "x": 10, "l": 50}


def _roman(s: str) -> int:
    total, prev = 0, 0
    for ch in reversed(s):
        v = _ROMAN[ch]
        total += -v if v < prev else v
        prev = max(prev, v)
    return total


def base_section(s: str) -> str:
    """'Schedule, Article 55' -> 'art55'; 'Order XXXVII' -> 'order37'; '2(7)' -> '2'; 'Rule 4(5)' -> 'rule4'."""
    s = s.strip().lower()
    m = re.search(r"\b(order|article|art\.?|rules?)\s*([0-9]+[a-z]?|[ivxl]+)\b", s)
    if m:
        kind = {"article": "art", "art.": "art", "art": "art", "rules": "rule"}.get(m.group(1), m.group(1))
        num = m.group(2)
        if re.fullmatch(r"[ivxl]+", num):
            num = str(_roman(num))
        return f"{kind}{num}"
    m = re.search(r"([0-9]+[a-z]?)", s)
    return m.group(1) if m else s
