# Interview prep: my notes on every decision in Haq

Kuku's brief says "submit only work you understand… we'll talk through [decisions] in your interview." Before the interview: run the app, open each file listed at the end, and make sure I can explain any line.

## 1. The 60-second pitch

> "Most people drop everyday legal problems like deposits, refunds, unpaid salary or bounced cheques, because a lawyer feels expensive and the process is confusing. Haq lets you talk about it in your own language, by text or voice. It builds your case file, tells you where you stand, works out your deadlines, drafts the notice or complaint, and lets you practise a court hearing. The hard part isn't writing nice text, it's not inventing law. A plain AI model given my test questions made up Supreme Court judgments and cited the IPC, which was replaced in 2024. So Haq can only cite from a law library I checked against official sources, a guard in code checks every reply before the user sees it, and every deadline is calculated in code, not by the model."

## 2. What happens to one message

File: `app/engine.py`, function `turn()`.

1. **Red flags (code, `rules.red_flags`).** A regex over the message in English, Hindi and Hinglish: arrest, FIR, violence, self-harm, divorce, land. Safety shouldn't depend on a model.
2. **Greeting? (code, `intent.greeting_parts`).** "hi", "how are you", "नमस्ते" get a fixed reply with no AI call.
3. **Router (small model, `prompts.ROUTER`).** Labels the message legal / general knowledge / greeting / off-topic / unsafe, and pulls out the problem type, language and facts as JSON (dates as YYYY-MM-DD, amounts as numbers).
4. **Not legal?** One short reply (small model; unsafe ones from the main model), checked by the guard, then done. It never touches the case file.
5. **Calculate (code, `rules.compute`).** Deadlines, which Consumer Commission, the fee. Each result points to a library entry.
6. **Pick the law (code, `kb.retrieve_for`).** The list for the problem type plus provisions matching the question's topic (`kb.TOPICS`).
7. **Answer (main model, `prompts.COUNSEL`).** Uses only that law and the calculations, and returns JSON: reply, citations, actions, lawyer level…
8. **Guard (code, `guard.py`).** Checks sections, Acts, case law, repealed laws, promised outcomes, and unsupported amounts. One rewrite, then the bad sentence is removed.
9. **Safety nets (code).** Strips leaked ids, adds any passed deadline the reply missed, adds emergency numbers on red flags, adds law chips for every verified provision, blocks prompt leaks.
10. **Lawyer warning** = the highest of the rules, the model's view and deadline urgency.

The server keeps no state: the browser sends the whole conversation each time. So any server can answer any request, and the tests run exactly what users get.

## 3. Questions I expect

| Question | My answer |
|---|---|
| Why Problem 2? | It's where AI is most useful (people give up) and most dangerous (invented law). It also needs no data from Kuku, so I could test it end to end. |
| Why these five problem types? | Very common, usually winnable without a lawyer, cheap forums exist (Consumer Commission is free up to ₹5 lakh), and some have strict deadlines (cheque: 30 days) where a wrong answer does real harm. |
| What's AI and what's code? | AI: understanding messy language, pulling out facts, explaining in the user's language, drafting, role-play. Code: anything with one right answer (dates, limits, fees, which law exists, safety triggers). People: checking the library; the user reviews every draft. |
| Why not embeddings over all of Indian law? | With about 100 entries, a hand-picked list per problem type plus topic matching is predictable, testable and free. Embeddings make sense once the library is much bigger. The real next step is growing the library, not changing how it's searched. |
| How do you stop invented laws? | Only verified entries reach the prompt; the prompt allows only those; the guard checks every reply and blocks anything else; one rewrite, then removal. The guard is regex, so it can miss odd phrasing and can block real sections I haven't verified. I chose over-strict on purpose. |
| How does it decide which law to cite? | `kb.TOPICS` maps words in the question to provisions (equality → Articles 14-18, arrest → BNSS 35/47/48/58 and Article 22, theft → BNS 303…). That's added to the problem type's list. The model then has to cite every provision that applies and none that doesn't. |
| Why can't it cite the IT Act or Special Marriage Act? | I couldn't open an official text: India Code timed out, and the only official IT Act copy was the 2000 version without the 2008 sections. I didn't want to quote law from secondary websites, so Haq explains those in words and says the section isn't verified. |
| Why no case law? | I couldn't verify judgments at scale for free, and an invented judgment in a legal notice is worse than none. The guard blocks every case citation. Next step: a few landmark judgments checked against official reporters. |
| Why refuse non-legal questions? | It's built as a legal assistant, and every off-topic answer spends the same free quota real users need. The labelling happens on the server so the API can't be used around it. Greetings and short facts still get a one-line answer. |
| What if the router mislabels? | Code pushes mistakes the safe way: anything with legal words goes to the legal path, a red flag always gets the full answer, and if the router fails the message is treated as legal. |
| How do the message buttons know which message? | Every message has a permanent ID (from the server for chat, from the browser for drafts, court, practice and notices). A reply stores its prompt's ID, so "try again" on the 5th answer re-asks the 5th question and changes nothing else. |
| Why the model chooses the language but code the script? | The script the user typed in is visible (Unicode ranges). Models sometimes replied in Devanagari to Hinglish users, so code decides. |
| How is the model swappable? | Every provider uses the OpenAI-compatible API. Changing `LLM_PROVIDER` / `CUSTOM_BASE_URL` / `CUSTOM_MODEL` swaps it with no code change, and it falls back automatically on rate limits. |
| How do you know it's good? | 22 written cases with automatic checks, a plain-LLM baseline, a 31-case scope test, a 10-question citation test, 43 unit tests and about 214 browser checks. I read every reply, not just the failures. |
| What fails? | The guard checks citations, not reasoning (the bail/FIR example). Uncited rules can be stretched (airline credit shell). The small router can mislabel. Know these by heart. |
| How would you know it works with real users? | The share of users who take the recommended step, plus a 30-day "did you get your money back?" follow-up. Also lawyer spot-checks, guard rate, 👎/report rate, escalations followed, drop-off. |
| Cost at scale? | About 4.2k input + 0.9k output tokens per legal turn, roughly ₹0.10 at Groq's reported gpt-oss-120b price. The real costs are legal review of the library and the human escalation path. |
| What next with more time? | A lawyer reviewing and growing the library; state rent and Shops & Establishments rules; verified judgments; WhatsApp; reminders; hand-off to NALSA / Tele-Law with the case file. |
| Biggest risk? | Someone relying on a wrong deadline. Dates come from code with the source shown, they're labelled estimates, and a near or passed deadline triggers a lawyer warning. |

## 4. Running it on a new input in the interview

1. Open https://haq-46bx.onrender.com a few minutes early (the free server sleeps; the first load takes about 50 s). Local backup: in `haq`, run `.\.venv\Scripts\python.exe -m uvicorn app.main:app --port 8000`.
2. Type their scenario. Point at the case file filling up, the deadlines with source links, the 🛡️ chip and law chips, and any lawyer warning.
3. Click **Draft**, show the blanks being asked for in the chat, the Word download and "how to send".
4. Type "practice" after a case reply for the mock hearing; "stop" for the scorecard.
5. Try a general question ("Can the police arrest me without a warrant?") to show the cited provisions, and something off-topic to show the redirect.
6. Swap the model live with ⚙︎, or put their key in `.env`:
   ```
   LLM_PROVIDER=custom
   CUSTOM_BASE_URL=<their endpoint>/v1
   CUSTOM_API_KEY=<key>
   CUSTOM_MODEL=<model name>
   ```
   and restart.
7. If something goes wrong, say what happened and why. They've said they value that over polish.

## 5. Files to know
- `app/engine.py`: the message pipeline (start here)
- `app/intent.py`: labelling messages, greetings, short replies, the leak check
- `app/guard.py`: the checker for invented law
- `app/rules.py`: deadlines, red flags, the repealed-law list
- `app/kb.py` + `kb/laws.json`: the verified library, per-problem lists and `TOPICS`
- `app/prompts.py`: every prompt in one place
- `app/llm.py` + `app/config.py`: model swapping and fallback
- `static/actions.js`: the buttons under each message and message IDs
- `evals/cases.json` + `evals/run_evals.py`, `scripts/qa/`: the tests
- `docs/AI_ERRORS_LOG.md`: where AI got it wrong
