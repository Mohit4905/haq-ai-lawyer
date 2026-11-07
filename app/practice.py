"""Practice mode (the AI plays the other side) and notice explainer."""
from __future__ import annotations

import base64
import json
import re

from . import guard, kb, prompts, rules
from .llm import LLMError, chat, chat_json

# Mock hearing in the chat: the AI plays the judge and puts the other side's arguments to the user.
# category -> (judge, other side, short name, example argument, likely arguments)
# Forums are kept generic where they differ by state (tenancy, salary).
HEARINGS = {
    "tenancy": ("the judge hearing a security-deposit dispute", "the landlord", "landlord", "the walls were damaged",
                "unpaid electricity bill, damage to walls, painting charges, 'you left without one month's notice'"),
    "consumer": ("the President of the District Consumer Commission", "the company (opposite party)", "company", "the product was misused",
                 "'refund is under process', 'company policy does not allow it', 'it was customer misuse', 'contact the seller, not us', 'the warranty does not cover this'"),
    "salary": ("the presiding officer hearing an unpaid-salary claim", "the employer", "employer", "you did not serve the notice period",
               "'the company is in loss', 'you didn't serve the notice period', 'performance issues', 'you took company property', 'we will pay next month'"),
    "cheque_bounce": ("the Magistrate hearing a cheque-dishonour complaint", "the accused (who gave the cheque)", "accused", "it was only a security cheque",
                      "'it was a security cheque', 'I already paid in cash', 'the debt was smaller', 'I never received the notice'"),
    "notice": ("the judge hearing the dispute behind the notice", "the party who sent the notice", "other side", "you agreed to pay",
               "insisting their demand is valid, saying the user agreed to it, questioning the user's proof"),
}
DEFAULT_HEARING = ("the judge hearing this dispute", "the other party", "other side", "your version is not correct",
                   "denying the user's version and questioning their proof")


def _summary(case: dict) -> str:
    f = case.get("facts") if isinstance(case.get("facts"), dict) else {}
    s = str(f.get("summary") or "")
    return (s + " Facts: " + json.dumps(f, ensure_ascii=False))[:1500]


def _clean(history: list) -> list:
    """Model-safe history: dicts with string content only (the client is untrusted)."""
    out = []
    for m in history:
        if isinstance(m, dict) and isinstance(m.get("content"), str) and m["content"].strip():
            out.append({"role": "user" if m.get("role") == "user" else "assistant", "content": m["content"][:1500]})
    return out


def practice_turn(case: dict, history: list, provider: str | None = None, language: str | None = None) -> dict:
    judge, other, short, example, counter = HEARINGS.get(case.get("category") or "", DEFAULT_HEARING)
    hist = _clean(history)
    sys = prompts.PRACTICE_PERSONA.format(
        judge=judge, other_side=other, other_side_short=short, counter_example=example, counter_claims=counter,
        case_summary=_summary(case), language=language or case.get("language") or "English",
        opening="" if hist else prompts.PRACTICE_OPENING)
    msgs = [{"role": "system", "content": sys}] + (hist[-14:] or [{"role": "user", "content": "(The hearing begins.)"}])
    if msgs[-1]["role"] == "assistant":  # providers want the last turn from the user
        msgs.append({"role": "user", "content": "(continue)"})
    try:
        res = chat(msgs, tier="main", temperature=0.6, max_tokens=260, provider=provider)
        text = res.text.strip().strip('"')
        rep = guard.check(text, set(), "")
        if not rep.ok:  # the judge must not cite law or pre-judge; drop offending sentences
            text = guard.strip_violations(text, rep).split("\n\n_⚠️")[0].strip() or text
    except LLMError as e:
        return {"error": str(e)}
    return {"reply": text, "judge": judge, "model": res.meta()}


def practice_feedback(case: dict, history: list, provider: str | None = None, language: str | None = None) -> dict:
    judge, *_ = HEARINGS.get(case.get("category") or "", DEFAULT_HEARING)
    hist = _clean(history)
    if not any(m["role"] == "user" for m in hist):
        return {"error": "no_answers"}
    transcript = "\n".join(f"{'USER' if m['role'] == 'user' else 'JUDGE'}: {m['content']}" for m in hist)
    sys = prompts.PRACTICE_COACH.format(judge=judge, case_summary=_summary(case), transcript=transcript[-6000:], language=language or case.get("language") or "English")
    try:
        out, res = chat_json([{"role": "user", "content": sys}], tier="main", temperature=0.2, max_tokens=1000, provider=provider)
    except LLMError as e:
        return {"error": str(e)}
    # untrusted shapes (audit lesson): scores 1-5 ints, lists of strings
    sc = out.get("scores") if isinstance(out.get("scores"), dict) else {}
    clean = {}
    for k in ("facts", "proof", "answers", "relief", "composure"):
        try:
            clean[k] = max(1, min(5, int(round(float(sc.get(k))))))
        except (TypeError, ValueError):
            pass
    out["scores"] = clean
    for k in ("went_well", "improve", "better_lines", "bring"):
        v = out.get(k)
        out[k] = [str(x) for x in v if str(x).strip()][:5] if isinstance(v, list) else ([v] if isinstance(v, str) and v.strip() else [])
    # code check (the prompt alone was ignored once: it invented "notice on 15 August 2026"):
    # a suggested line may not contain a number the user never gave
    source = transcript + " " + _summary(case)
    known = {n.replace(",", "") for n in re.findall(r"\d[\d,]*", source)}
    out["better_lines"] = [s for s in out["better_lines"] if all(n.replace(",", "") in known for n in re.findall(r"\d[\d,]*", s))]
    out["summary"] = str(out.get("summary") or "")
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
