# Interview prep: understand every decision in Haq

Kuku says: *"submit only work you understand… We'll talk through [decisions] in your interview."* Read this, run the app yourself, and open each file mentioned. You should be able to explain any line.

---

## 1. The 60-second pitch

> "Most people drop everyday legal problems (deposits, refunds, unpaid salary, bounced cheques) because a lawyer feels expensive and the process is confusing. I built Haq: you talk to it in your language, by text or voice. It builds your case file, explains where you stand, calculates your deadlines, drafts the notice or complaint, and lets you practise the conversation. The hard part of an AI lawyer isn't writing nice text. It's *not inventing law*. A plain LLM, given my test questions, made up three Supreme Court judgments and cited the IPC, which was repealed in 2024. So Haq can only cite from a law library I verified against official sources, a code-based guard checks every reply before the user sees it, and all deadlines are computed in code, not by the model."

## 2. Architecture: what happens on one message

File: `app/engine.py` → `turn()`

1. **Red flags (code, `rules.py: red_flags`).** A regex over the message in English, Hindi and Hinglish: arrest, FIR, violence, self-harm, divorce, land. *Why code?* Safety should never depend on a model's mood.
2. **Intake (fast model, `prompts.ROUTER`).** Category + language + **facts extracted as JSON** (dates as YYYY-MM-DD, amounts as numbers).
3. **Calculate (code, `rules.py: compute`).** Deadlines, which Consumer Commission, filing fee. Each result carries a library id as its source.
4. **Retrieve (code, `kb.py: CATEGORY_IDS`).** A hand-picked list of verified provisions per problem type.
5. **Counsel (main model, `prompts.COUNSEL`).** Writes the reply using only the library and the calculations, and returns JSON: reply, citations, actions, needs_lawyer…
6. **Guard (code, `guard.py`).** Scans the reply for sections, Acts, case law and repealed laws. On a violation it asks for one rewrite, then strips the offending sentence.
7. **Safety nets (code).** Strips leaked library ids, appends any passed deadline the model failed to mention, and adds emergency numbers on red flags.
8. **Escalation = max(rules, model judgement, deadline urgency).**

The **backend is stateless**: the browser sends the whole conversation each time. *Why?* Any server can answer any request, so scaling means adding servers. The same function runs in the UI and in the evals, so what I test is what users get.

## 3. Decisions you'll be asked about

| Question | Answer |
|---|---|
| Why Problem 2? | It's the problem where AI is most dangerous (invented law) and most useful (people give up). It needs no domain data from Kuku, so I could test it end to end. |
| Why these 4 problem types? | Very common; the money is usually recoverable *without* a lawyer; cheap forums exist (Consumer Commission with no fee up to ₹5 lakh, labour authority, legal notice); and some have strict deadlines (cheque: 30 days), where wrong AI advice does real harm. |
| What did you give to AI vs keep as code? | AI: understanding messy language, extracting facts, explaining in the user's language, drafting prose, role-play. Code: anything with one right answer (dates, thresholds, fees, which law exists, safety triggers). Human: curating and verifying the library; the user reviews every draft (`[[FILL]]` gaps, disclaimer). |
| Why not RAG with embeddings over all Indian law? | At this size (~75 entries), a hand-picked list per category is predictable, auditable, testable and free. Embeddings help when the corpus is large. The next step is to grow the library, not to switch retrieval method. |
| How do you stop invented laws? | Four layers: (1) only verified entries reach the prompt; (2) the prompt allows only those; (3) the code guard checks every reply and blocks unknown sections/Acts, any case law and repealed laws; (4) rewrite, then strip. The guard is **regex-based**: it can miss oddly phrased references (false negatives) and can flag real-but-unverified sections (false positives). That's deliberate: being over-strict is safer. |
| Why no case law at all? | I couldn't verify judgments at scale for free. An invented judgment in a legal notice is worse than none. Next step: add a few landmark judgments with verified citations from official reporters. |
| Why does the model choose the language but code the script? | The script the user typed in is observable (Unicode ranges). Models sometimes replied in Devanagari to Hinglish users. Code fixed that. |
| How is the model swappable? | Every provider speaks the OpenAI-compatible API. Changing `LLM_PROVIDER` / `CUSTOM_BASE_URL` / `CUSTOM_MODEL` in `.env` swaps the model, with no code changes. Providers and models fall back automatically on rate limits (the free tier is 8k tokens/minute per model on Groq). |
| How do you know it's good? | 22 hand-written test cases with automatic checks: category, reply language, extracted facts, must/must-not phrases, escalation level, deadline maths, zero unverified law shown, draft quality. Plus a baseline (same questions to a plain LLM) and an LLM judge from a *different* model family, to avoid self-preference. Plus 19 offline unit tests. |
| What fails? | See the "Failures" section of the solution doc and `evals/outputs/<run>/SUMMARY.md`. Know 2–3 specific failures by heart. |
| How would you know it works with real users? | North star: **% of conversations where the user takes the recommended action** (sends the notice or files the complaint), followed up after 30 days: "did you get your money?". Guardrails: escalation acceptance, lawyer-review spot checks on a sample of drafts, guard intervention rate, and drop-off at each step. |
| Cost at scale? | Measured: about N tokens per turn (see doc). At ~$0.15/M input and ~$0.60/M output (third-party-reported Groq price for gpt-oss-120b), that's a fraction of a rupee per conversation. The real costs are legal review of the library and the escalation path. |
| What would you do with more time? | Grow the library with a lawyer's review; state-specific rent and Shops & Establishments rules; verified landmark judgments; WhatsApp channel (where users already are); follow-up reminders before deadlines; human lawyer hand-off (NALSA / Tele-Law) with the case file attached. |
| Biggest risk? | Someone relies on a wrong deadline. Mitigations: dates computed in code with their source shown, "estimate: confirm with legal aid" notes, and escalation when a deadline is near or past. |

## 4. Live demo on a new input (they will ask)

1. `cd haq`, activate the venv, run `uvicorn app.main:app --port 8000` (or open the deployed link).
2. Type their scenario. Point out: the case file filling up (right panel), deadlines with their source links, the 🛡️ chip (click a law chip to see the official source), escalation banners.
3. Click **Draft** and show the `[[FILL]]` gaps, Word download, and "how to send".
4. **Practice** tab: role-play, then feedback scores.
5. Swap the model live: the ⚙︎ dropdown (Groq ↔ Gemini), or set their key in `.env`:
   ```
   LLM_PROVIDER=custom
   CUSTOM_BASE_URL=<their endpoint>/v1
   CUSTOM_API_KEY=<key>
   CUSTOM_MODEL=<model name>
   ```
   then restart the server.
6. If something goes wrong, say what happened and why. They value honesty over polish.

## 5. Files to know

- `app/engine.py`: the turn pipeline (start here)
- `app/guard.py`: the anti-hallucination checker
- `app/rules.py`: deadlines, red flags, repealed-law list
- `app/kb.py` + `kb/laws.json`: the verified library and the per-category lists
- `app/prompts.py`: every prompt in one place
- `app/llm.py` + `app/config.py`: provider/model swapping and fallback
- `evals/cases.json` + `evals/run_evals.py`: tests and how they're scored
- `docs/AI_ERRORS_LOG.md`: "where AI got it wrong" (you must mention one in the doc)
