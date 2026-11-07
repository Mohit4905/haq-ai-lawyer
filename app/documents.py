"""Document drafting: fixed structure (code) + facts filled in by the model + guard check.

The model never chooses the structure of a legal notice. The code does, and the model
only fills in facts. Missing facts become visible [[FILL: ...]] placeholders, never
made-up values.
"""
from __future__ import annotations

import io
import re
from datetime import date

from . import guard, kb, prompts, rules
from .engine import _calculated_text, _case_file_text
from .llm import LLMError, chat_json

COMMON_NOTICE = """1. Heading: "LEGAL NOTICE" / "NOTICE FOR DEMAND", the mode of sending (By Registered Post A.D. / Speed Post / Email), and the date [[FILL: date]].
2. From: sender name and address. To: recipient name and address.
3. Subject line, one sentence.
4. Numbered paragraphs of facts in date order (what was agreed, what was paid, what went wrong, earlier requests made).
5. Paragraph stating the legal basis briefly (only from the library, or no section if unsure).
6. Clear demand: exact amount or action, and a deadline of {days} days from receipt, plus how to pay (bank details placeholder).
7. Consequence: that the sender will pursue lawful remedies ({remedy}) at the recipient's cost if not complied with.
8. "Copy retained for record." Signature block with name, phone, email."""

DOCS: dict[str, dict] = {
    "deposit_demand_notice": {
        "label": "legal notice to a landlord demanding refund of the security deposit",
        "structure": COMMON_NOTICE.format(days=15, remedy="a civil suit for recovery with interest, or approaching Lok Adalat/mediation"),
    },
    "company_complaint_email": {
        "label": "firm written complaint email to the company's customer care / grievance officer (first step before a consumer case)",
        "structure": """1. Subject with order/booking ID. 2. Facts: what was bought, when, amount, what went wrong, earlier complaints/ticket numbers. 3. Specific demand (refund/replacement/repair + compensation if appropriate) and a deadline of 15 days. 4. Note that if unresolved they will approach the National Consumer Helpline and the Consumer Commission. 5. List of attachments. 6. Name, phone, email.""",
    },
    "consumer_legal_notice": {
        "label": "legal notice to a company/seller before filing a consumer complaint",
        "structure": COMMON_NOTICE.format(days=15, remedy="a complaint before the Consumer Commission under the Consumer Protection Act, 2019"),
    },
    "consumer_commission_complaint": {
        "label": "draft consumer complaint for the District Consumer Commission (for e-filing)",
        "structure": """1. "BEFORE THE DISTRICT CONSUMER DISPUTES REDRESSAL COMMISSION, [[FILL: district]]". 2. Complainant and Opposite Party details. 3. "COMPLAINT UNDER SECTION 35 OF THE CONSUMER PROTECTION ACT, 2019" (only if in library). 4. Facts in numbered paragraphs with dates and amounts. 5. Deficiency in service / defect / unfair trade practice: explain in plain terms. 6. Jurisdiction (where complainant resides / where cause arose; amount paid within the District limit) and limitation (filed within time). 7. Reliefs prayed: refund, compensation for harassment, litigation cost. 8. List of documents annexed. 9. Verification paragraph and signature.""",
    },
    "salary_demand_notice": {
        "label": "legal notice to an employer demanding unpaid salary / full and final settlement",
        "structure": COMMON_NOTICE.format(days=15, remedy="a claim before the labour authority and/or a civil suit for recovery"),
    },
    "labour_authority_complaint": {
        "label": "complaint letter/application to the labour authority (Inspector-cum-Facilitator / Labour Commissioner office) about unpaid wages",
        "structure": """1. To: The Inspector-cum-Facilitator / Labour Commissioner, [[FILL: district, state]]. 2. Subject. 3. Applicant details and employer details (name, address, nature of business). 4. Employment details: role, joining date, salary, mode of payment. 5. Unpaid period and amount, month-wise table. 6. Requests already made to the employer. 7. Request: direct the employer to pay the wages due (plus any compensation the authority can order) . 8. Documents enclosed. 9. Declaration, name, signature, date.""",
    },
    "cheque_demand_notice_s138": {
        "label": "statutory demand notice for a dishonoured cheque under Section 138 of the Negotiable Instruments Act, 1881",
        "structure": COMMON_NOTICE.format(days=15, remedy="a criminal complaint under Section 138 read with Section 142 of the Negotiable Instruments Act, 1881")
        + "\nMANDATORY: state cheque number, date, amount, bank and branch; date of presentation; date and reason of dishonour from the return memo; that the cheque was issued for a legally enforceable debt (describe it); and DEMAND PAYMENT OF THE CHEQUE AMOUNT within 15 days of receipt of the notice.",
    },
    "reply_to_notice": {
        "label": "reply to a legal notice the user received",
        "structure": """1. Heading "REPLY TO LEGAL NOTICE DATED [[FILL]]", mode of sending, date. 2. To the sender (or their advocate). 3. Paragraph-wise response: admit only what is true, deny what is false, give the user's version with dates. 4. Without prejudice: what the user is willing to do (if anything). 5. Reservation of rights. 6. Signature. Add a top line: "Review with a lawyer before sending if the amount is large or a court case is threatened.\"""",
    },
}


def draft(state: dict, doc_type: str, doc_language: str = "English", provider: str | None = None, today: date | None = None) -> dict:
    if doc_type not in DOCS:
        return {"error": f"Unknown document type {doc_type}"}
    case = state.get("case") if isinstance(state, dict) else None
    if not isinstance(case, dict) or not case.get("category"):  # audit: a state without 'case' used to 500
        return {"error": "Tell Haq about your problem in the chat first, then ask for the draft."}
    if not isinstance(case.get("facts"), dict):
        case["facts"] = {}
    entries = kb.retrieve(case.get("category"))
    allowed = {e["id"] for e in entries}
    calc = rules.compute(case.get("category"), case.get("facts", {}), today)
    spec = DOCS[doc_type]
    lib = kb.render_for_prompt(entries)
    sys = prompts.DRAFT.format(
        doc_label=spec["label"],
        doc_language=doc_language,
        structure=spec["structure"],
        library=lib,
        calculated=_calculated_text(calc),
        case_file=_case_file_text(case),
        user_language=case.get("language") or "English",
    )
    convo = "\n".join(f"{m['role']}: {m['content']}" for m in [x for x in state.get("messages", []) if isinstance(x, dict) and not x.get("practice") and not x.get("aside")][-12:] if m.get("role") == "user")
    msgs = [{"role": "system", "content": sys}, {"role": "user", "content": "What the user told us, in their words:\n" + convo[:4000]}]
    try:
        out, res = chat_json(msgs, tier="main", temperature=0.2, max_tokens=2600, provider=provider)
    except LLMError as e:
        return {"error": str(e)}
    body = str(out.get("body_markdown") or "")
    support = lib + _calculated_text(calc) + convo
    rep = guard.check(body, allowed, support)
    stripped = False
    if not rep.ok:
        body = guard.strip_violations(body, rep)
        stripped = True
    # the "how to send it" steps are guarded too: drop any step that cites unverified law
    raw_steps = out.get("send_instructions", []) or []
    if isinstance(raw_steps, str):
        raw_steps = [raw_steps]
    flat = []
    for s in raw_steps:  # models sometimes return all steps in one numbered string
        parts = re.split(r"(?:^|\s)\d{1,2}[.)]\s+", str(s))
        flat += [x.strip() for x in parts if x.strip()]
    steps = []
    for s in flat:
        if guard.check(s, allowed, support).ok:
            steps.append(s)
    out["send_instructions"] = steps
    placeholders = re.findall(r"\[\[FILL:?[^\]]*\]\]", body)
    return {
        "doc_type": doc_type,
        "title": out.get("title") or spec["label"].capitalize(),
        "body_markdown": body,
        "placeholders": list(dict.fromkeys(placeholders)),
        "citations": [kb.public_entry(kb.by_id()[i]) for i in out.get("citations", []) if i in kb.by_id()],
        "send_instructions": out.get("send_instructions", []),
        "guard": {"initial": rep.to_dict(), "stripped": stripped},
        "model": res.meta(),
        "disclaimer": "Draft prepared with AI from what you told Haq. Read every line, fill the [[FILL]] gaps, and remove anything untrue before sending. For large amounts or if the other side has a lawyer, get it checked by a lawyer (free legal aid: NALSA 15100).",
    }


FILL_RE = re.compile(r"\[\[FILL:?\s*([^\]]*)\]\]")


def blanks(body: str) -> list[str]:
    """Distinct [[FILL: label]] labels in order of appearance (same label = one question)."""
    out: list[str] = []
    for m in FILL_RE.finditer(body):
        lab = m.group(1).strip() or "missing detail"
        if lab.lower() not in (x.lower() for x in out):
            out.append(lab)
    return out


def _grounded(value: str, answer: str, label: str) -> bool:
    """A filled value must come from the user's message (dates may be reformatted)."""
    norm = lambda s: re.sub(r"[^\w]+", " ", s.lower()).split()  # noqa: E731
    v, a = norm(value), set(norm(answer))
    if re.search(r"(?i)\bdate|\bday\b|\bwhen\b", label) and re.search(r"(?i)\btoday\b|\baaj\b|आज", answer):
        return True  # "today" is turned into today's date by the model
    return bool(v) and sum(t in a for t in v) / len(v) >= 0.6


def fill(body: str, answer: str, provider: str | None = None, today: date | None = None) -> dict:
    """Fill a draft's [[FILL]] blanks from the user's chat reply. Code does the substitution;
    the model only says which part of the reply answers which blank, and values not found in
    the reply are rejected."""
    labels = blanks(body)
    if not labels or not answer.strip():
        return {"body_markdown": body, "filled": {}, "remaining": labels}
    sys = prompts.DRAFT_FILL.format(today=(today or date.today()).strftime("%d %B %Y"),
                                    blanks="\n".join(f"{i + 1}. {lab}" for i, lab in enumerate(labels)))
    try:
        out, res = chat_json([{"role": "system", "content": sys}, {"role": "user", "content": answer}],
                             tier="fast", temperature=0, max_tokens=900, provider=provider)
    except LLMError as e:
        return {"error": str(e)}
    filled: dict[str, str] = {}
    vals = out.get("values") if isinstance(out, dict) else None
    if isinstance(vals, list):  # some models answer [{"blank": 1, "value": ...}] or a plain list (audit: .items() crashed)
        vals = {str(x.get("blank", i + 1)) if isinstance(x, dict) else str(i + 1): (x.get("value") if isinstance(x, dict) else x) for i, x in enumerate(vals)}
    for k, v in (vals if isinstance(vals, dict) else {}).items():
        v = re.sub(r"\s+", " ", str(v or "")).strip()
        if not v or "[[" in v or len(v) > 400:
            continue
        k = str(k).strip()
        lab = labels[int(k) - 1] if k.isdigit() and 0 < int(k) <= len(labels) else next((x for x in labels if x.lower() == k.lower()), None)
        if lab and _grounded(v, answer, lab):
            filled[lab] = v

    def sub(m: re.Match) -> str:
        lab = (m.group(1).strip() or "missing detail").lower()
        return next((v for x, v in filled.items() if x.lower() == lab), m.group(0))

    new = FILL_RE.sub(sub, body)
    return {"body_markdown": new, "filled": filled, "remaining": blanks(new), "model": res.meta()}


def to_docx(title: str, body_markdown: str) -> bytes:
    from docx import Document
    from docx.shared import Pt

    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(11)
    for line in body_markdown.splitlines():
        s = line.rstrip()
        if not s:
            doc.add_paragraph("")
            continue
        if s.startswith("#"):
            level = min(len(s) - len(s.lstrip("#")), 3)
            doc.add_heading(s.lstrip("#").strip(), level=level)
            continue
        p = doc.add_paragraph()
        bullet = re.match(r"^\s*[-*]\s+", s)
        if bullet:
            s = s[bullet.end():]
            p.style = doc.styles["List Bullet"]
        # **bold** segments
        for i, part in enumerate(re.split(r"\*\*", s)):
            run = p.add_run(part)
            run.bold = i % 2 == 1
            if "[[FILL" in part:
                run.font.highlight_color = 7  # yellow
    buf = io.BytesIO()
    doc.save(buf)
    return buf.getvalue()
