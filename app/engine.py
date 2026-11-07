"""Conversation orchestration: rules -> router -> grounded counsel -> guard -> (repair) -> merge.

The backend is stateless: the client sends the whole session state each turn and gets the
updated state back. That makes it trivially horizontally scalable and easy to replay in evals.
"""
from __future__ import annotations

import copy
import json
import uuid
import re
import time
from datetime import date

from . import guard, intent, kb, prompts, rules
from .llm import LLMError, chat, chat_json

LARGE_CLAIM = 1_000_000  # ₹10 lakh and above: always recommend a lawyer's review
MAX_HISTORY = 10  # last N messages sent to the model (case file carries the long-term memory)

DOC_TYPES = {
    "tenancy": ["deposit_demand_notice"],
    "consumer": ["company_complaint_email", "consumer_legal_notice", "consumer_commission_complaint"],
    "salary": ["salary_demand_notice", "labour_authority_complaint"],
    "cheque_bounce": ["cheque_demand_notice_s138"],
    "notice": ["reply_to_notice"],
    "cyber_fraud": [],
    "general_legal": [],
    "out_of_scope": [],
    "other": [],
}


def new_id() -> str:
    """Stable unique id for a chat message (the client keeps it; actions like copy/regenerate use it)."""
    return uuid.uuid4().hex


def new_state() -> dict:
    return {
        "version": 1,
        "messages": [],
        "case": {"category": None, "language": None, "script": None, "facts": {}, "timeline": [], "evidence_have": [], "evidence_missing": [], "next_step": None},
        "flags": {"level": "none", "reasons": []},
        "log": [],
    }


def _case_file_text(case: dict) -> str:
    c = {k: v for k, v in case.items() if k not in ("language", "script")}
    return json.dumps(c, ensure_ascii=False, indent=1)[:3500]


def _calculated_text(calc: dict) -> str:
    lines = []
    for d in calc.get("deadlines", []):
        when = f"{d['date']} ({'PASSED ' + str(-d['days_left']) + ' days ago' if d['days_left'] < 0 else str(d['days_left']) + ' days left'})"
        if d["days_left"] < 0 and d.get("user_deadline", True):
            when = "⚠️ ALREADY PASSED on " + when
        lines.append(f"- {d['label']}: {when} [basis {d['basis'] or 'notice'}] {d['note']}")
    for d in calc.get("derived", []):
        lines.append(f"- {d['label']}: {d['value']} [basis {d['basis']}] {d['note']}")
    return "\n".join(lines) or "(none yet: dates/amounts not known)"


def _convo(state: dict) -> list:
    """The legal conversation, without mock-hearing messages (those belong to the rehearsal, not the case)
    and without asides (greetings, general-knowledge and off-topic exchanges)."""
    return [m for m in state.get("messages", []) if isinstance(m, dict) and not m.get("practice") and not m.get("aside")]


def route(state: dict, message: str, provider: str | None = None, today: date | None = None) -> tuple[dict, dict]:
    """Intake step (fast model): category, language AND fact extraction, so code can
    compute deadlines before the main model writes anything."""
    prev = state["case"].get("category")
    hist = "\n".join(f"{m['role']}: {m['content'][:300]}" for m in _convo(state)[-4:])
    keys = {f"k_{c}": ", ".join(k for k, _ in rules.CHECKLISTS[c]) for c in rules.CHECKLISTS}
    sys = prompts.ROUTER.format(today=(today or date.today()).isoformat(), **keys)
    msgs = [
        {"role": "system", "content": sys},
        {"role": "user", "content": f"Current category: {prev}\nKnown facts: {json.dumps(state['case'].get('facts', {}), ensure_ascii=False)[:800]}\nRecent conversation:\n{hist}\n\nNEW MESSAGE:\n{message}"},
    ]
    try:
        data, res = chat_json(msgs, tier="fast", temperature=0, max_tokens=700, provider=provider)
        return data, res.meta()
    except LLMError as e:
        # router failure is non-fatal: fall back to heuristics
        return {"category": prev or "other", "language": None, "script": guard.detect_script(message)}, {"error": str(e)[:200]}


LANG_SCRIPT = {"English": "Latin", "Hinglish": "Latin", "Hindi": "Devanagari", "Marathi": "Devanagari", "Bengali": "Bengali", "Tamil": "Tamil",
               "Telugu": "Telugu", "Kannada": "Kannada", "Malayalam": "Malayalam", "Gujarati": "Gujarati", "Punjabi": "Gurmukhi", "Odia": "Odia", "Urdu": "Arabic"}


def _pick_language(case: dict, r: dict, message: str, lang_pref: str | None) -> tuple[str, str, str]:
    """(language, script, script_seen). The script the user typed in is observable, so code decides it;
    the model only names the language. An explicit choice in the UI beats auto-detection."""
    script_seen = guard.detect_script(message)
    lang = r.get("language") or case.get("language") or "English"
    if script_seen == "Hinglish" or (script_seen == "Latin" and lang in ("Hindi", "Hinglish") and guard.hinglish_score(message) > 0.06):
        lang, script = "Hinglish", "Latin"
    elif script_seen == "Latin" and lang in ("Hindi", "Hinglish"):
        lang, script = "English", "Latin"  # English with Indian names is still English
    elif script_seen == "Latin":
        script = "Latin"
        if lang not in ("English", "Hinglish"):
            lang = "English" if len(message.split()) > 3 else (case.get("language") or "English")
    else:
        script = script_seen
        if lang in ("English", "Hinglish"):
            lang = {"Devanagari": "Hindi", "Tamil": "Tamil", "Bengali": "Bengali", "Telugu": "Telugu", "Kannada": "Kannada",
                    "Gujarati": "Gujarati", "Gurmukhi": "Punjabi", "Malayalam": "Malayalam", "Odia": "Odia", "Arabic": "Urdu"}.get(script_seen, lang)
    if lang_pref in LANG_SCRIPT:
        lang, script = lang_pref, LANG_SCRIPT[lang_pref]
    return lang, script, script_seen


def _aside(state: dict, message: str, kind: str, reply: str, meta: dict | None, guard_log: dict, trace: dict, t0: float) -> dict:
    """A non-legal exchange: answered briefly, kept out of the case file and the legal context."""
    uid, rid = new_id(), new_id()
    state["messages"].append({"role": "user", "content": message, "aside": True, "id": uid})
    state["messages"].append({"role": "assistant", "content": reply, "aside": True, "id": rid, "reply_to": uid})
    state["log"].append({"t": round(time.time() - t0, 2), "intent": kind, "model": (meta or {}).get("model"), "provider": (meta or {}).get("provider")})
    return {
        "state": state, "reply": reply, "intent": kind, "message_id": rid, "user_message_id": uid, "citations": [], "calculated": None, "completeness": None,
        "actions": [], "next_step": None, "needs_lawyer": state["flags"], "emergency_contacts": [], "confidence": None,
        "unknowns": [], "guard": guard_log, "model": meta, "trace": trace, "latency_s": round(time.time() - t0, 2),
    }


def turn(state: dict | None, message: str, provider: str | None = None, today: date | None = None, lang_pref: str | None = None) -> dict:
    t0 = time.time()
    state = copy.deepcopy(state) if state else new_state()
    case = state["case"]
    trace: dict = {"steps": []}

    # 1. deterministic red flags (never depend on the model for safety)
    flags = rules.red_flags(message)
    trace["steps"].append({"step": "red_flags", "result": flags})

    # 1b. plain greetings / small talk: answered by code, no model call
    parts = None if flags else intent.greeting_parts(message)
    if parts:
        g_lang, g_script, _ = _pick_language(case, {}, message, lang_pref)
        key = intent.lang_key(g_lang, g_script)
        trace["steps"].append({"step": "intent", "result": "greeting", "by": "code", "parts": parts})
        if key:
            return _aside(state, message, "greeting", intent.canned_greeting(parts, key), None, {"final": {"ok": True}}, trace, t0)
        try:
            reply, meta, glog = intent.aside_reply("greeting", message, g_lang, g_script, provider)
            return _aside(state, message, "greeting", reply, meta, glog, trace, t0)
        except LLMError:
            pass  # fall through to the normal path

    # 2. route: intent + category + language
    r, rmeta = route(state, message, provider, today)
    trace["steps"].append({"step": "router", "result": r, "llm": rmeta})
    kind = r.get("intent") if r.get("intent") in rules.INTENTS else "legal"  # router failure -> treat as legal
    if flags:
        kind = "legal"  # a safety red flag always gets the full answer + safety text
    if kind == "general_knowledge" and intent.LEGAL_WORDS.search(message):
        kind = "legal"  # QA 7 Nov: "what are my fundamental rights?" was labelled general knowledge and answered wrongly
    if kind != "legal":
        a_lang, a_script, _ = _pick_language(case, r, message, lang_pref)
        trace["steps"].append({"step": "intent", "result": kind, "by": "router"})
        try:
            reply, meta, glog = intent.aside_reply(kind, message, a_lang, a_script, provider)
        except LLMError as e:
            return {"state": state, "error": str(e), "trace": trace}
        if intent.leaks_prompt(reply):
            reply = intent.LEAK_REPLY.get(intent.lang_key(a_lang, a_script) or "en")
            glog["leak_blocked"] = True
        return _aside(state, message, kind, reply, meta, glog, trace, t0)

    cat = r.get("category") if r.get("category") in rules.CATEGORIES else (case.get("category") or "other")
    if case.get("category") in rules.IN_DEPTH and cat in ("other", "general_legal"):
        cat = case["category"]  # a follow-up question inside a case stays in that case
    case["category"] = cat
    lang, script, script_seen = _pick_language(case, r, message, lang_pref)
    case["language"], case["script"] = lang, script

    # merge facts extracted at intake, so this turn's deadlines are computed by code BEFORE generation
    _merge_case(case, {"facts_update": r.get("facts") or {}})
    approx = [k for k in (r.get("approximate_dates") or []) if isinstance(k, str)]
    if approx:
        case.setdefault("approximate", [])
        case["approximate"] = sorted(set(case["approximate"]) | set(approx))

    # 3. retrieve verified law (the category's set + the provisions for the topics in the question) + deadlines
    prev_user = next((m["content"] for m in reversed(_convo(state)) if m.get("role") == "user"), "")
    entries = kb.retrieve_for(cat, message + "\n" + prev_user[:500])
    allowed = {e["id"] for e in entries}
    calc = rules.compute(cat, case["facts"], today)
    comp = rules.completeness(cat, case["facts"])

    uid = new_id()
    state["messages"].append({"role": "user", "content": message, "id": uid})
    library_text = kb.render_for_prompt(entries)
    sys = prompts.COUNSEL.format(
        role_rules=prompts.ROLE_RULES,
        language=case["language"],
        script=case["script"],
        missing=", ".join(m["question"] for m in comp["missing"][:6]) or "none",
        playbook="\n".join(f"- {s}" for s in rules.PLAYBOOKS.get(cat, ["Understand the problem first and give the general legal position; if it turns out to be outside deposits, consumer, salary, cheque or notices, explain the general position and say a lawyer / free legal aid (NALSA 15100) should handle it."])),
        library=library_text,
        calculated=_calculated_text(calc),
        case_file=_case_file_text(case),
        category=cat,
        fact_keys=", ".join(k for k, _ in rules.CHECKLISTS.get(cat, [])),
        doc_types=", ".join(DOC_TYPES.get(cat, [])) or "none",
    )
    msgs = [{"role": "system", "content": sys}] + [
        {"role": m["role"], "content": m["content"]} for m in _convo(state)[-MAX_HISTORY:]
    ]

    # 4. grounded generation
    try:
        out, res = chat_json(msgs, tier="main", temperature=0.2, max_tokens=1600, provider=provider)
    except LLMError as e:
        state["messages"].pop()
        return {"state": state, "error": str(e), "trace": trace}
    trace["steps"].append({"step": "counsel", "llm": res.meta()})

    # 5. apply fact updates first so the guard can use freshly computed deadlines as support
    _merge_case(case, out)
    calc = rules.compute(case["category"], case["facts"], today)
    support = (library_text + "\n" + "\n".join(rules.PLAYBOOKS.get(case["category"], [])) + "\n" + _calculated_text(calc) + "\n"
               + json.dumps(case.get("facts") or {}, ensure_ascii=False) + "\n" + " ".join(m["content"] for m in _convo(state) if m["role"] == "user"))
    # the user asked about an old law (IPC, CrPC...): it may be discussed as history if the reply says it was replaced
    hist_ok = any(re.search(rf"(?<![A-Za-z]){re.escape(a)}(?![A-Za-z])", message, re.I) for info in rules.OUTDATED_LAWS.values() for a in info["aliases"] if len(a) > 2)

    def gchk(text: str) -> guard.GuardReport:
        return guard.check(text, allowed, support, history_ok=hist_ok, figures=True)

    # 6. guard (+ one repair round)
    reply = strip_ids(str(out.get("reply") or "").strip())
    rep = gchk(reply)
    bad_ids = guard.check_declared_ids(out.get("citations", []), allowed)
    guard_log = {"initial": rep.to_dict(), "bad_ids": bad_ids, "repaired": False, "stripped": False}
    if not rep.ok:
        problems = "\n".join(f"- {v['text']}: {v['why']}" + (f" Use instead: {v['suggestion']}" if v.get("suggestion") else "") for v in rep.violations)
        try:
            fix_msgs = msgs + [{"role": "assistant", "content": json.dumps(out, ensure_ascii=False)}, {"role": "user", "content": prompts.REPAIR.format(problems=problems)}]
            out2, res2 = chat_json(fix_msgs, tier="main", temperature=0.1, max_tokens=1600, provider=provider)
            trace["steps"].append({"step": "repair", "llm": res2.meta()})
            reply2 = strip_ids(str(out2.get("reply") or "").strip())
            rep2 = gchk(reply2)
            guard_log["repaired"] = True
            guard_log["after_repair"] = rep2.to_dict()
            if reply2:
                reply, rep = reply2, rep2
                out["citations"] = out2.get("citations", out.get("citations"))
        except LLMError as e:
            trace["steps"].append({"step": "repair", "error": str(e)[:200]})
        if not rep.ok:
            reply = guard.strip_violations(reply, rep)
            guard_log["stripped"] = True
            rep = gchk(reply)
    guard_log["final"] = rep.to_dict()

    # 6b. language check (code): reply must be in the user's script; one rewrite if not
    want = case["script"] if case["script"] != "Latin" else ("Hinglish" if case["language"] == "Hinglish" else "Latin")
    got = guard.detect_script(reply)
    mismatch = (
        (want not in ("Latin", "Hinglish") and got != want)
        or (want == "Hinglish" and got != "Hinglish" and guard.hinglish_score(reply) < 0.06)
        or (want == "Latin" and got != "Latin" and (got != "Hinglish" or guard.hinglish_score(reply) > 0.15 or lang_pref == "English"))
    )  # an explicit English choice in the UI means English, even for lightly Hinglish replies (QA probe)
    guard_log["language"] = {"wanted": want, "got": got, "rewritten": False}
    if mismatch:
        try:
            target = "Hinglish (Hindi written in Latin letters)" if want == "Hinglish" else (f"{case['language']} in {want} script" if want != "Latin" else "English")
            res_l = chat(
                [{"role": "system", "content": f"Rewrite the text below in {target}. Keep the meaning, markdown, numbers, dates, law names and section numbers exactly. Output only the rewritten text."},
                 {"role": "user", "content": reply}],
                tier="main", temperature=0.1, max_tokens=1400, provider=provider,
            )
            cand = strip_ids(res_l.text.strip())
            if cand and gchk(cand).ok:
                reply = cand
                guard_log["language"]["rewritten"] = True
                guard_log["language"]["got_after"] = guard.detect_script(reply)
            trace["steps"].append({"step": "language_rewrite", "llm": res_l.meta()})
        except LLMError as e:
            trace["steps"].append({"step": "language_rewrite", "error": str(e)[:200]})

    # 7. escalation = max(code red flags, model judgement, computed deadline urgency)
    level = "none"
    reasons = []
    general = case["category"] == "general_legal"  # a question about the law, not the user's own matter
    for f in flags:
        if general and f["level"] != "emergency":
            continue  # "how do I file an FIR?" is not an FIR against the user (QA 7 Nov)
        if rules.LEVEL_ORDER[f["level"]] > rules.LEVEL_ORDER[level]:
            level = f["level"]
        reasons.append(f["reason"])
    nl = {} if general else (out.get("needs_lawyer") or {})
    if isinstance(nl, dict) and nl.get("level") in rules.LEVEL_ORDER and rules.LEVEL_ORDER[nl["level"]] > rules.LEVEL_ORDER[level]:
        level = nl["level"]
    if isinstance(nl, dict) and nl.get("reason") and nl.get("level") not in (None, "none"):
        reasons.append(nl["reason"])
    for d in calc.get("deadlines", []):
        if d["status"] in ("passed", "soon") and d.get("user_deadline", True):
            if rules.LEVEL_ORDER[level] < rules.LEVEL_ORDER["recommended"]:
                level = "recommended"
            reasons.append(f"Deadline {d['status']}: {d['label']} ({d['date']})")
    # large claims: a code floor (eval v7: the model told an ₹85 lakh buyer to "absolutely" file alone)
    money = [v for k, v in (case.get("facts") or {}).items()
             if isinstance(v, (int, float)) and not isinstance(v, bool) and re.search(r"amount|paid|price|deposit|claim|dues|cheque", k)]
    if money and max(money) >= LARGE_CLAIM and rules.LEVEL_ORDER[level] < rules.LEVEL_ORDER["recommended"]:
        level = "recommended"
        reasons.append(f"Large amount (₹{max(money):,.0f}): have a lawyer review the case before filing")
    if case["category"] == "cyber_fraud" and rules.LEVEL_ORDER[level] < rules.LEVEL_ORDER["recommended"]:
        level, reasons = "recommended", reasons + ["Fraud is time-critical: report to 1930 and your bank immediately"]
    if case["category"] == "out_of_scope" and rules.LEVEL_ORDER[level] < rules.LEVEL_ORDER["recommended"]:
        # general guidance only; police/arrest/court red flags above still make it urgent
        level, reasons = "recommended", reasons + ["Outside Haq's in-depth areas: have a lawyer or free legal aid handle it"]
    prev_level = state["flags"].get("level", "none")
    if rules.LEVEL_ORDER[prev_level] > rules.LEVEL_ORDER[level]:
        level = prev_level
    state["flags"] = {"level": level, "reasons": list(dict.fromkeys(state["flags"].get("reasons", []) + reasons))[-6:]}

    # 7b. citable-law guarantee: a covered problem always shows verified provisions the user can cite
    core = rules.CORE_CITATIONS.get(case["category"] or "", [])
    user_text = " ".join(m["content"] for m in _convo(state) if m["role"] == "user")
    if case["category"] == "tenancy" and not (case["facts"].get("deposit_amount") or re.search(r"(?i)deposit|advance|security|jama|डिपॉज़िट|डिपॉजिट|जमा", user_text)):
        core = []  # the tenancy core law is about deposits; an eviction question shouldn't get it (QA 7 Nov)
    if core and not rep.verified and not any(f["level"] in ("urgent", "emergency") for f in flags):
        idx = kb.by_id()
        lines = []
        for cid in core:
            e = idx.get(cid)
            if e:
                first = re.split(r"(?<=[.!?])\s", e["plain"].strip())[0]
                lines.append(f"- **{rules.provision_label(e)}**: {first}")
        if lines:
            head = rules.CITE_HEADING.get(case.get("language") or "", "Law you can cite (checked against official sources)")
            reply += f"\n\n**{head}:**\n" + "\n".join(lines)
            out["citations"] = list(dict.fromkeys((out.get("citations") or []) + core))
            guard_log["core_citations_added"] = core

    # 8a. deadline safety net: a passed deadline must be visible even if the model glossed over it
    passed = [d for d in calc.get("deadlines", []) if d["status"] == "passed" and d.get("user_deadline", True)]
    for d in passed:
        dt = date.fromisoformat(d["date"])
        variants = {d["date"], dt.strftime("%d %b %Y").lstrip("0"), dt.strftime("%d %B").lstrip("0"), dt.strftime("%d-%m-%Y"), dt.strftime("%d/%m/%Y")}
        lowered = reply.lower()
        if not any(v.lower() in lowered for v in variants):
            key = "hi" if case.get("script") == "Devanagari" else ("hinglish" if case.get("language") == "Hinglish" else "en")
            reply += "\n\n" + rules.DEADLINE_ALERT[key].format(label=d["label"], date=dt.strftime("%d %b %Y"))
    guard_log["deadline_alerts_added"] = len([1 for d in passed if d["label"] in reply])

    # 8b. safety text is added by code, never left to the model
    if any(f["level"] == "emergency" for f in flags):
        key = "hi" if case.get("script") == "Devanagari" else ("hinglish" if script_seen == "Hinglish" else "en")
        reply = rules.EMERGENCY_PREFIX[key] + reply

    # 8c. hidden instructions never reach the user (code check, whatever the model was told)
    if intent.leaks_prompt(reply):
        reply = intent.LEAK_REPLY.get(intent.lang_key(case.get("language"), case.get("script")) or "en")
        out["citations"], out["actions"] = [], []
        guard_log["leak_blocked"] = True

    # 8d. every provision the guard verified in the text gets a clickable source chip, even if the model forgot to list it
    named = []
    for mention, act in ([] if guard_log.get("leak_blocked") else rep.verified):
        key = kb.base_section(str(mention))
        named += [e["id"] for e in entries if e["act"] == act and e.get("section") and kb.base_section(str(e["section"])) == key]
    out["citations"] = list(dict.fromkeys([c for c in (out.get("citations") or []) if isinstance(c, str)] + named))

    # 9. assemble
    cited =[kb.public_entry(kb.by_id()[i]) for i in out.get("citations", []) if i in kb.by_id()]
    rid = new_id()
    state["messages"].append({"role": "assistant", "content": reply, "id": rid, "reply_to": uid})
    state["log"].append({"t": round(time.time() - t0, 2), "model": res.model, "provider": res.provider, "guard_ok": rep.ok, "repaired": guard_log["repaired"]})
    return {
        "state": state,
        "reply": reply,
        "intent": "legal",
        "message_id": rid,
        "user_message_id": uid,
        "citations": cited,
        "calculated": calc,
        "completeness": rules.completeness(case["category"], case["facts"]),
        "actions": out.get("actions", []),
        "next_step": out.get("next_step"),
        "needs_lawyer": state["flags"],
        "emergency_contacts": rules.EMERGENCY_CONTACTS if level == "emergency" else [],
        "confidence": out.get("confidence"),
        "unknowns": out.get("unknowns", []),
        "guard": guard_log,
        "model": res.meta(),
        "trace": trace,
        "latency_s": round(time.time() - t0, 2),
    }


_ID_BRACKETS = re.compile(r"\s*[【\[]\s*((?:[A-Z][A-Z0-9]+-[A-Za-z0-9\-()]+)(?:\s*[,;]\s*[A-Z][A-Z0-9]+-[A-Za-z0-9\-()]+)*)\s*[】\]]")


def strip_ids(text: str) -> str:
    """Remove internal library ids the model leaked into user-facing text (e.g. 【COW2019-S17】)."""
    ids = set(kb.by_id())

    def repl(m: re.Match) -> str:
        parts = [p.strip() for p in re.split(r"[,;]", m.group(1))]
        return "" if all(p in ids or re.match(r"^[A-Z]{2,}\d{0,4}-", p) for p in parts) else m.group(0)

    text = _ID_BRACKETS.sub(repl, text)
    # JSON fields the model sometimes echoes into the reply ("**Actions:** [{...}]", "citations: [...]")
    text = re.sub(r"(?im)^\s*\**\s*(?:actions|citations|next_step|needs_lawyer)\s*\**\s*:\s*\**\s*[\[{].*$", "", text).rstrip()
    # "**Action:** get_help (...)" (QA 7 Nov): an action code echoed as a line
    text = re.sub(r"(?im)^\s*\**\s*actions?\s*:?\s*\**\s*:?\s*(?:draft|practice|get_help)\b.*$", "", text).rstrip()
    # internal field names like "(notice_received_date)" or "(reply_to_notice)"
    return re.sub(r"\s*\((?:[a-z0-9]+_)+[a-z0-9]+\)", "", text)


def _merge_case(case: dict, out: dict) -> None:
    if out.get("category") in rules.CATEGORIES and out.get("category") not in ("other",):
        if not (out["category"] == "general_legal" and case.get("category") in rules.IN_DEPTH):  # a question inside a case keeps the case
            case["category"] = out["category"]
    fu = out.get("facts_update") or {}
    if isinstance(fu, dict):
        for k, v in fu.items():
            if v not in (None, "", "unknown", [], {}):
                case["facts"][str(k)] = v if isinstance(v, (str, int, float, bool)) else json.dumps(v, ensure_ascii=False)
    for t in out.get("timeline_add") or []:
        if isinstance(t, dict) and t.get("event") and t not in case["timeline"]:
            case["timeline"].append({"date": str(t.get("date", "")), "event": str(t["event"])})
    case["timeline"].sort(key=lambda x: x.get("date") or "9999")
    for key in ("evidence_have", "evidence_missing"):
        for e in out.get(key) or []:
            if isinstance(e, str) and e not in case[key]:
                case[key].append(e)
    # evidence that is now "have" should not stay in "missing"
    case["evidence_missing"] = [e for e in case["evidence_missing"] if e not in case["evidence_have"]]
    if out.get("next_step"):
        case["next_step"] = out["next_step"]
