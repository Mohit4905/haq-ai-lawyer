---
title: Haq - AI legal help
emoji: ⚖️
colorFrom: green
colorTo: yellow
sdk: gradio
sdk_version: 6.31.0
app_file: space_app.py
python_version: "3.12"
pinned: false
---

# Haq (हक़): AI legal help for everyday problems in India

**Live app:** https://haq-46bx.onrender.com (free instance: the first load after idling takes ~50s)

Haq helps an ordinary person in India act on an everyday legal problem. You can type or speak in Hindi, English, Hinglish, Tamil, Bengali and other languages. Haq:

1. **Builds the case.** It turns a messy story into a structured case file (facts, timeline, proof you have, proof you still need) and asks only for what's missing.
2. **Explains where you stand.** In plain language: your options from cheapest to most expensive, and one recommended next step.
3. **Calculates deadlines in code, not with the AI.** Examples: the 30-day window to send a cheque-bounce notice, or the 2-year limit for consumer complaints. Each date links to the official source.
4. **Drafts the document.** Legal notice, complaint email, consumer-commission complaint, labour-office complaint, or a reply to a notice. Downloadable as Word. Missing details are marked `[[FILL]]`, never invented.
5. **Prepares you for the hearing.** After a case reply, type "practice" in the chat: the AI plays the judge, asks what a judge would ask, puts the other side's arguments to you, and scores your answers when you type "stop".
6. **Explains a notice you received.** Paste it or upload a photo or PDF.
7. **Says when you need a real lawyer**, and points to free legal aid (NALSA 15100) and emergency help (112, Tele-MANAS 14416).
8. **Message actions.** Under your messages: edit (re-asks and replaces that answer), share, copy. Under Haq's answers: copy, 👍/👎, read aloud, share, try again (earlier answers kept as ‹ 1/2 › versions), and ⋯ (copy with sources, report). Every message has a stable id, so an action only ever touches the message it belongs to ([static/actions.js](static/actions.js)).

**Covered in depth:** security deposits, consumer refunds and defects (including e-commerce), unpaid salary and final settlement, bounced cheques, understanding legal notices.
**Explained in general terms:** any other legal question: fundamental rights (Constitution articles are in the verified library), BNS vs IPC, how to file an FIR, starting a business, online fraud. For your own criminal, family, property-title or tax matter, Haq explains the general position and the usual steps, then recommends a lawyer or free legal aid.
**Not answered:** non-legal requests (code, poems, recipes, shopping advice, workout plans…). Haq redirects to the legal angle if there is a genuine one (a laptop → consumer rights). Short general-knowledge questions ("capital of India?") and greetings get a one-line answer.

### Staying a legal assistant (not a general chatbot)
Each message is labelled by the router call that already runs on every turn: **legal**, **general_knowledge**, **greeting**, **off_topic** or **unsafe** ([app/intent.py](app/intent.py)). Only *legal* messages reach the full grounded answer. The rest get a short reply and never touch the case file or the legal context. This runs on the server, so calling the API directly gets the same behaviour. Code backstops:
- plain greetings ("hi", "how are you", "नमस्ते") are answered by code, with no model call;
- a red flag (self-harm, violence, arrest…) always gets the full answer;
- a "general knowledge" label on a message with legal words is overridden to *legal*;
- any reply containing text from the hidden instructions is replaced (prompt-leak check);
- off-topic and unsafe replies go through the same guard as legal ones, so no invented law.
Tested with the real model by [scripts/qa/scope_test.py](scripts/qa/scope_test.py) (outputs in `evals/outputs/*_scope/`).

## How Haq avoids invented laws

| Layer | What it does | AI or code? |
|---|---|---|
| Verified library ([kb/laws.json](kb/laws.json)) | 86 provisions (incl. 12 Constitution articles), rules, helplines and thresholds, each checked against an official source URL (India Code, Gazette, ministries, RBI, NALSA). Unverified entries are kept for transparency but never shown to the model. | Human-curated |
| Scoped retrieval | Only the library entries for the user's problem type go into the prompt. | Code |
| Prompt rules | The model may mention a law or number only if it appears in the library or in the code's calculations. No case law, ever. | AI |
| **Guard** ([app/guard.py](app/guard.py)) | Scans every reply before the user sees it. It flags sections, Articles, Orders and Acts that aren't in the library (English and Hindi patterns), any case-law citation (`X v. Y`, AIR/SCC, "the Supreme Court held"), repealed laws (IPC, CrPC, CPA 1986…) with their replacement, money amounts and percentages that nothing supports, and time periods that nothing supports (warning only). | Code |
| Repair, then strip | On a violation, the model rewrites once. If the problem remains, the offending sentence is removed and the user is told. | AI, then code |
| Deadlines, forum, fees | Pure functions in [app/rules.py](app/rules.py), each tagged with its library id. | Code |
| Red flags | Arrest, FIR, violence, self-harm, family or property matters trigger escalation by regex in English, Hindi and Hinglish. Safety text is added by code, not the model. | Code |

The UI shows the result on every message. For example "🛡️ 2 legal references verified" (click a law chip to see its source), or "🛡️ 1 unverified reference caught & fixed".

## Architecture

```
browser (vanilla JS; holds session state)
   │  POST /api/chat {state, message}
   ▼
FastAPI (stateless) ── red-flag rules (regex) ─────────────┐
   │── greeting? → reply by code (no model call)            │
   │── router: fast model → intent + category + language    │
   │     not legal → short reply (fast model) → guard → done│
   │── retrieve verified law for that category              │
   │── calculators: deadlines / forum / fee (code)          │
   │── counsel: main model → JSON {reply, facts, citations…}│
   │── guard → repair → strip                               │
   └── merge case file, escalation = max(rules, model, deadlines)
```

**Swapping the model** takes environment variables only. Any OpenAI-compatible endpoint works: Groq, Gemini, OpenRouter, OpenAI, Anthropic, Ollama, or `custom` (point it at any `/v1` URL). Providers are tried in order and fall back on rate limits. You can also switch providers live from the ⚙︎ menu in the UI. Every output records which model produced it.

## Run it

```bash
python -m venv .venv && .venv/Scripts/activate   # Windows; on Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # add GROQ_API_KEY and/or GEMINI_API_KEY (free)
python kb/build_kb.py       # merge + validate the law library
uvicorn app.main:app --port 8000
# open http://localhost:8000
```

Tests and evals:

```bash
python -m tests.test_offline                      # deterministic parts, no API key needed
python -m evals.run_evals --baseline --judge gemini
```

Raw outputs land in `evals/outputs/<run>/`: full JSON per case, readable transcripts, drafted documents, the baseline comparison, and `SUMMARY.md`.

## Results (final controlled run, 22 test cases)

- **134/136 automatic checks passed**; **0/22 replies showed an unverified legal reference**; escalation level correct 19/19; reply language correct 15/15 (English, Hindi, Hinglish, Tamil, Bengali).
- **Baseline:** the same model with a plain helpful Indian lawyer prompt put unverified legal references in 17/22 answers (7 cited case law, 7 cited repealed laws such as the IPC and the Payment of Wages Act), and in every run it told a user who had missed the cheque-bounce notice window Yes, you can still file a case.
- All runs and every failure, read by hand: [evals/CHANGELOG.md](evals/CHANGELOG.md), [evals/MANUAL_REVIEW.md](evals/MANUAL_REVIEW.md). Raw outputs: [evals/outputs/](evals/outputs/).

More docs: [where AI got it wrong](docs/AI_ERRORS_LOG.md) · [verified library](kb/README.md) · [deploy](docs/DEPLOY.md)

## Limitations

See the solution document. In short: the library is small and hand-checked, state-specific rules (rent laws, Shops and Establishments Acts) are only flagged, not modelled, and deadline maths assumes the dates the user gives are right. Haq gives legal information, not legal advice.
