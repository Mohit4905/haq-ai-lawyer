"""Practice mode (the AI plays the other side) and notice explainer."""
from __future__ import annotations

import base64
import json

from . import guard, kb, prompts, rules
from .llm import LLMError, chat, chat_json

PERSONAS = {
    "tenancy": ("the landlord", "unpaid electricity bill, 'damage' to walls, painting charges, 'you left without one month notice'"),
    "consumer": ("a customer-care supervisor of the company", "'refund is under process', 'policy does not allow', 'it was customer misuse', 'contact the seller not us'"),
    "salary": ("the employer / HR manager", "'company is in loss', 'you didn't serve notice period', 'performance issues', 'we will pay next month'"),
    "cheque_bounce": ("the person who gave the bounced cheque", "'it was a security cheque', 'I already paid you in cash', 'give me more time', 'the debt was smaller'"),
    "notice": ("the person/company who sent the notice", "insisting on their demand"),
}


def _summary(case: dict) -> str:
    f = case.get("facts", {})
    s = f.get("summary") or ""
    return (s + " Facts: " + json.dumps(f, ensure_ascii=False))[:1500]


def practice_turn(case: dict, history: list, provider: str | None = None) -> dict:
    persona, counter = PERSONAS.get(case.get("category") or "", ("the other party", "their own version"))
    sys = prompts.PRACTICE_PERSONA.format(persona=persona, case_summary=_summary(case), counter_claims=counter, language=case.get("language") or "English")
    msgs = [{"role": "system", "content": sys}]
    if not history:
        msgs.append({"role": "user", "content": "(The user walks up to you / calls you to raise the issue. Open with a short, slightly dismissive line.)"})
    for m in history[-12:]:
        msgs.append({"role": "user" if m["role"] == "user" else "assistant", "content": m["content"]})
    try:
        res = chat(msgs, tier="main", temperature=0.8, max_tokens=200, provider=provider)
    except LLMError as e:
        return {"error": str(e)}
    return {"reply": res.text.strip().strip('"'), "persona": persona, "model": res.meta()}


def practice_feedback(case: dict, history: list, provider: str | None = None) -> dict:
    persona, _ = PERSONAS.get(case.get("category") or "", ("the other party", ""))
    transcript = "\n".join(f"{'USER' if m['role']=='user' else persona.upper()}: {m['content']}" for m in history)
    sys = prompts.PRACTICE_COACH.format(persona=persona, case_summary=_summary(case), transcript=transcript[:6000], language=case.get("language") or "English")
    try:
        out, res = chat_json([{"role": "user", "content": sys}], tier="main", temperature=0.2, max_tokens=900, provider=provider)
    except LLMError as e:
        return {"error": str(e)}
    out["model"] = res.meta()
    return out


def explain_notice(text: str | None, image_bytes: bytes | None, mime: str | None, language: str, script: str, provider: str | None = None) -> dict:
    entries = kb.retrieve("notice")
    lib = kb.render_for_prompt(entries)
    vision_used = False
    if image_bytes and not text:
        # Step 1: transcribe the photo with a vision model (OCR); step 2: explain the text.
        b64 = base64.b64encode(image_bytes).decode()
        try:
            res = chat(
                [{"role": "user", "content": [
                    {"type": "text", "text": "Transcribe ALL text in this document exactly as written (any language). Output only the text."},
                    {"type": "image_url", "image_url": {"url": f"data:{mime or 'image/jpeg'};base64,{b64}"}},
                ]}],
                tier="vision", max_tokens=2500, provider=provider,
            )
            text = res.text
            vision_used = True
        except LLMError as e:
            return {"error": "Could not read the photo. Please paste the text instead. (" + str(e)[:150] + ")"}
    if not text or len(text.strip()) < 40:
        return {"error": "Please paste the full text of the notice (or upload a clear photo)."}
    sys = prompts.EXPLAIN_NOTICE.format(language=language, script=script, notice=text[:8000], library=lib)
    try:
        out, res = chat_json([{"role": "user", "content": sys}], tier="main", temperature=0.1, max_tokens=1200, provider=provider)
    except LLMError as e:
        return {"error": str(e)}
    # model JSON is untrusted in shape: lists may come back as null or a string (audit: TypeError -> 500)
    for k in ("do_now", "do_not", "laws_mentioned_in_notice"):
        v = out.get(k)
        out[k] = [str(x) for x in v] if isinstance(v, list) else ([str(v)] if isinstance(v, str) and v.strip() else [])
    if not isinstance(out.get("needs_lawyer"), dict):
        out["needs_lawyer"] = {"level": "none", "reason": ""}
    # guard the explanation fields we generated (not the notice itself, which may cite anything)
    gen = " ".join(str(out.get(k, "")) for k in ("plain_summary", "what_they_want", "risk_reason")) + " " + " ".join(out["do_now"] + out["do_not"])
    rep = guard.check(gen, {e["id"] for e in entries}, lib + text)
    flags = rules.red_flags(text)
    if any(f["level"] in ("urgent", "emergency") for f in flags):
        out["needs_lawyer"] = {"level": "urgent", "reason": "; ".join(f["reason"] for f in flags)}
    out["guard"] = rep.to_dict()
    out["extracted_text"] = text if vision_used else None
    out["model"] = res.meta()
    return out
