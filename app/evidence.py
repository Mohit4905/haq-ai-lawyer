"""Evidence locker: read a receipt / chat screenshot / agreement / PDF and extract facts.

The AI only *proposes* facts; the user ticks which ones to add to the case file
(human in the loop). Files are never stored on the server: device storage or the
user's own private cloud bucket.
"""
from __future__ import annotations

import base64
import io
import re

from . import rules
from .llm import LLMError, chat, chat_json

PROMPT = """You are reading a piece of evidence a person in India uploaded for their legal case ({category}).
Today is {today}. Extract ONLY what is visibly written. Never guess or fill gaps.
Return ONLY JSON:
{{"doc_type": "ONE of: rent agreement, rent/deposit receipt, bank transfer receipt, WhatsApp chat, invoice, payslip, offer letter, cheque, bank return memo, legal notice, email, photo of damage, other",
 "summary": "one plain sentence in {language}: what this document shows",
 "dates": [{{"date": "YYYY-MM-DD", "what": "what happened on this date (short, {language})"}}],
 "amounts": [{{"amount": number_in_rupees, "what": "short"}}],
 "parties": ["names / companies shown"],
 "facts_update": {{ only keys from this list that the document clearly shows, with the ACTUAL VALUE (amounts as rupee numbers, dates as YYYY-MM-DD, names as text; never true/false except for yes/no keys like written_agreement): {keys} }},
 "proves": ["what this helps prove, e.g. 'deposit of ₹40,000 was paid on 1 Jan 2025' ({language})"],
 "readable": true/false, "notes": "anything unclear"}}
Document content:
"""


def extract(category: str | None, language: str, filename: str, mime: str | None, raw: bytes, today: str, provider: str | None = None) -> dict:
    keys = ", ".join(k for k, _ in rules.CHECKLISTS.get(category or "", [])) or "other_party_name, summary"
    sys_prompt = PROMPT.format(category=category or "unknown", today=today, language=language or "English", keys=keys)
    name = (filename or "").lower()
    text = None
    if name.endswith(".pdf") or (mime or "").endswith("pdf"):
        from pypdf import PdfReader

        try:
            reader = PdfReader(io.BytesIO(raw))
            text = "\n".join((p.extract_text() or "") for p in reader.pages[:8]).strip()
        except Exception as e:  # noqa: BLE001
            return {"error": f"Could not read the PDF ({e})."}
        if len(text) < 30:
            return {"error": "This PDF looks like a scan with no text layer. Upload a photo of the page instead."}
    elif name.endswith((".txt", ".csv")) or (mime or "").startswith("text/"):
        text = raw.decode("utf-8", errors="ignore")
    try:
        if text is not None:
            data, res = chat_json([{"role": "user", "content": sys_prompt + text[:12000]}], tier="main", temperature=0, max_tokens=1200, provider=provider)
        else:
            if len(raw) > 6_000_000:
                return {"error": "Image too large (max 6 MB). Take a smaller photo."}
            b64 = base64.b64encode(raw).decode()
            res = chat(
                [{"role": "user", "content": [
                    {"type": "text", "text": sys_prompt + "(see the attached image)"},
                    {"type": "image_url", "image_url": {"url": f"data:{mime or 'image/jpeg'};base64,{b64}"}},
                ]}],
                tier="vision", json_mode=True, temperature=0, max_tokens=1200, provider=provider,
            )
            from .llm import parse_json

            data = parse_json(res.text)
    except LLMError as e:
        return {"error": "Could not read this file right now (" + str(e)[:160] + "). You can still keep it in the locker."}
    data["facts_update"] = _clean_facts(data.get("facts_update"))
    data["model"] = res.meta()
    return data


_BOOL_OK = {"written_agreement", "is_ecommerce", "still_employed", "complained_to_company"}


def _clean_facts(fu) -> dict:
    """Code check on AI output: drop placeholder values (true/false/yes) for keys that need real values."""
    out = {}
    if not isinstance(fu, dict):
        return out
    for k, v in fu.items():
        if v in (None, "", "null", "unknown"):
            continue
        is_bool = isinstance(v, bool) or str(v).strip().lower() in ("true", "false", "yes", "no")
        if is_bool and k not in _BOOL_OK:
            continue
        if re.search(r"amount|deposit|rent|salary|due|paid", k) and not re.search(r"\d", str(v)):
            continue
        if re.search(r"date|day$", k) and not re.match(r"^\d{4}-\d{2}-\d{2}$", str(v)):
            continue
        out[k] = v
    return out
