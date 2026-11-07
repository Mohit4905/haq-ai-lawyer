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

# Haq (हक़): an AI lawyer for everyday problems in India

**Live app:** https://haq-46bx.onrender.com (it's on a free server, so the first load after a quiet spell can take about 50 seconds)

Kuku AI Generalist assignment, Problem 2. Mohit Piplani, 23113101, Civil Engineering.

Most people in India never get help with small legal problems: a deposit the landlord keeps, a refund that never comes, salary that stops, a notice they can't make sense of. Haq is my attempt at a lawyer you can just talk to, in your own language, by text or voice.

## What it does

1. **Builds your case.** It turns a messy story into a case file: what happened, when, what proof you have and what you still need. It only asks for what's missing.
2. **Tells you where you stand.** Like a first meeting with a lawyer: how strong your case looks and what it depends on, the law on your side, what the other side will say, and what I'd do next.
3. **Works out your deadlines in code.** The 30-day window for a cheque-bounce notice, the 2-year limit for a consumer complaint and so on. The AI never calculates a date, and each one links to its source.
4. **Drafts the paperwork in the chat.** Legal notice, complaint email, Consumer Commission or labour-office complaint, or a reply to a notice. It asks for the missing details right there and fills them in (Word or PDF). Anything it doesn't know stays as a `[[FILL]]` blank.
5. **Lets you practise.** After a case reply, type "practice". The AI plays the judge, puts the other side's arguments to you, and scores your answers when you type "stop".
6. **Explains a notice or court order.** Paste it or upload a photo/PDF. Paste a court case number (CNR) and it pulls the live eCourts record.
7. **Explains other legal questions** (fundamental rights, arrest, theft, divorce, termination) and names the exact articles and sections that apply, as long as I could verify them.
8. **Tells you when you need a real lawyer**, and points to free legal aid (NALSA 15100) or emergency help (112, Tele-MANAS 14416).
9. **Message buttons, like in ChatGPT.** Edit, copy or share your messages; copy, rate, listen to, share or regenerate Haq's answers (old answers stay as ‹ 1/2 › versions), or report one.

**What it covers well:** security deposits, consumer refunds and defects (including online shopping), unpaid salary and final settlement, bounced cheques, legal notices.
**What it explains in general terms:** other legal topics. For your own criminal, family, property or tax matter it gives the general position and sends you to a lawyer or legal aid.
**What it won't do:** anything that isn't legal (code, poems, recipes, shopping advice). It says so politely, and points out a legal angle if there really is one. Greetings and short general-knowledge questions get a one-line answer.

## Making sure it doesn't invent law

This was the main problem. A plain AI model, given my test questions, made up Supreme Court judgments and cited the IPC, which was replaced in 2024. So:

| Layer | What it does | AI or code? |
|---|---|---|
| Verified library ([kb/laws.json](kb/laws.json)) | 107 entries: sections, Constitution articles, rules, helplines and limits. I read each one in an official source (India Code, e-Gazette, the Legislative Department's Constitution, ministries, RBI, NALSA) and it keeps that link. Entries I couldn't confirm are kept but never shown to the model. | Checked by me |
| Picking the law | The entries for your kind of problem, plus the provisions for the topic you asked about (equality gives Articles 14-18; arrest gives BNSS sections 35, 47, 48, 58 and Article 22; theft gives BNS section 303). See `TOPICS` in [app/kb.py](app/kb.py). | Code |
| Prompt rules | The model may only mention a law or number that's in the library or in the code's calculations. No case law. | AI |
| **Guard** ([app/guard.py](app/guard.py)) | Checks every reply before you see it. Flags sections, articles and Acts that aren't in the library (English and Hindi), any case-law citation, repealed laws (IPC, CrPC, CPA 1986…) with their replacement, promised outcomes, and in answers any money amount or percentage nothing supports. | Code |
| Rewrite, then remove | If the guard finds a problem, the model rewrites once. Whatever is still wrong gets removed, and you're told. | AI, then code |
| Deadlines, forum, fees | Plain functions in [app/rules.py](app/rules.py), each tied to a library entry. | Code |
| Red flags | Arrest, violence, self-harm, family or land matters trigger escalation, in English, Hindi and Hinglish. Safety text is added by code. | Code |

Every answer shows what happened, e.g. "🛡️ 2 legal references verified". Click a law chip to open the official source.

### Staying a legal assistant
Every message gets a label from the step that already reads it: legal, general knowledge, greeting, off-topic or unsafe ([app/intent.py](app/intent.py)). Only legal messages get the full answer; the rest get a short reply and don't touch your case file. This happens on the server, so calling the API directly doesn't get around it. A few things are done in code so they don't depend on the model: greetings are answered without any AI call, a safety red flag always gets the full answer, a "general knowledge" label on a question with legal words is overruled, and a reply that quotes the hidden instructions is replaced.

## How a message flows

```
browser (plain JavaScript, keeps the conversation)
   │  POST /api/chat {state, message}
   ▼
FastAPI (keeps no state) ── red flags (regex) ─────────────┐
   │── a greeting? reply from code, no AI call               │
   │── router (small model): label, problem type, language,  │
   │   facts                                                 │
   │     not legal: short reply (small model), guard, done   │
   │── pick verified law (problem type + topic of question)  │
   │── deadlines / forum / fee (code)                        │
   │── answer (main model): reply, facts, citations…         │
   │── guard, rewrite once, remove what's left               │
   └── update case file; lawyer warning = highest of rules,  │
       model and deadlines                                   │
```

**Swapping the model** only needs environment variables. Anything that speaks the OpenAI-compatible API works: Groq, Gemini, OpenRouter, OpenAI, Anthropic, Ollama, or `custom` (point it at any `/v1` URL). If one model hits a rate limit it falls back to the next, and you can switch providers live from the ⚙︎ menu. Every answer records which model wrote it.

## Running it yourself

```bash
python -m venv .venv && .venv/Scripts/activate   # Windows; on Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # add GROQ_API_KEY and/or GEMINI_API_KEY (both have free tiers)
python kb/build_kb.py       # builds and checks the law library
uvicorn app.main:app --port 8000
# open http://localhost:8000
```

Tests:

```bash
python -m tests.test_offline                       # 43 unit tests, no API key needed
python -m tests.test_kb_integrity                  # every library entry and the guard agree
python -m evals.run_evals --baseline --judge gemini   # the 22 written cases + a plain-LLM baseline
python scripts/qa/scope_test.py http://127.0.0.1:8000     # legal vs off-topic vs prompt injection (31 cases)
python scripts/qa/citations_test.py http://127.0.0.1:8000 # "which law applies?" (10 questions)
```

Browser tests of the real UI are in [scripts/qa/](scripts/qa/) (Playwright with Edge). The court tests use a local fake server, so they cost no credits.

## Results

- **22 written test cases, 5 languages:** 134/136 automatic checks pass, and **0/22 answers showed an unverified legal reference**.
- **The same 22 questions to the same model with a plain "helpful Indian lawyer" prompt:** 19/22 answers had a flagged reference, 7 cited case law, 12 cited repealed laws, and in every run it told someone who had missed the cheque-notice deadline that they could still file.
- **Scope test** (legal, off-topic, unsafe, prompt injection, follow-ups): 31/31 on the third run.
- **Citation test** (equality, free speech, arrest, theft, consumer, fraud, divorce, termination, Article 21): 10/10 on the third run.

Every raw output is in [evals/outputs/](evals/outputs/). What changed between runs, and every failure I read by hand: [evals/CHANGELOG.md](evals/CHANGELOG.md), [evals/MANUAL_REVIEW.md](evals/MANUAL_REVIEW.md), [evals/QA_AUDIT.md](evals/QA_AUDIT.md).

More: [where AI got it wrong](evals/AI_ERRORS_LOG.md) · [the law library](kb/README.md)

## Limits

The library is small and hand-checked; it has no case law and no state rules (rent Acts, Shops and Establishments). The guard checks citations, not reasoning, so advice that's wrong without citing anything can still get through. Deadlines assume the dates you give are right. On free tiers you get about 40 full answers a day, and each takes 7 to 16 seconds. Haq gives legal information, not legal advice.
