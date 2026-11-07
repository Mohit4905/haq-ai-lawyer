# Testing and QA

Last updated 7 Nov 2026.

How I tested: first a cold read of every Python, JS and HTML file by a separate AI reviewer that hadn't written the code, to find likely bugs. Then I ran the app and drove it with browser scripts (Playwright with Edge) at desktop and phone sizes, sent hostile requests straight to the API, and asked the AI new legal questions. I reproduced, fixed and re-tested every bug below. The scripts are in `scripts/qa/`. Court lookups go to a small fake server (`mock_court.py`) so the tests don't spend paid eCourts credits.

## What's in the app
- **Pages:** `/login` (log in, sign up, forgot / reset password, Google, guest), `/` (the app), `/privacy`, `/terms`.
- **In the app:** chat (text, voice, attach a notice), welcome cards, the sidebar (New case, Track case, Case file, Deadlines, Documents, Evidence, Get help, My cases with search, rename and delete), settings (language, theme, AI model), account and profile, the lawyer note, drafts in the chat, the practice hearing, court cards (Explain, Refresh, Add to calendar), downloads (.docx, .ics, case summary), and buttons under every message (edit, copy, share, rate, read aloud, try again, report).
- **API:** chat, draft, draft/fill, docx, explain, evidence, practice, transcribe, feedback, court (status, case, search, order), signup, account/delete, cron/reminders, config, kb, health.
- **Services:** Groq and Gemini (AI, with fallback), Supabase (accounts, database, storage), Brevo (email), eCourtsIndia (court records, paid).

## Latest results

| Suite | Result |
|---|---|
| Unit tests (`tests/test_offline.py`) · library integrity | 43/43 · OK |
| UI: every button, field, menu, tool, download, phone layout (`audit_ui.py`) | 79/79 |
| Message buttons (`actions_test.py`, chat faked in the browser) | 42/42, also on the live site |
| Practice hearing in the chat (`prep_test.py`) | 25/25 |
| Drafts in chat · court tracking · lawyer note · New case | 11/11 · 12/12 · 12/12 · 14/14 |
| API robustness and security (`audit_api.py`) · XSS (`audit_xss.py`) | 25/25 · 6/6 |
| Smoke test with real AI answers (`scripts/ui_smoke.py`, last run 6 Nov) | 19/19 |
| 22 written legal cases, 5 languages (eval v7) | 134/136; 0/22 showed unverified law |
| Scope test with the real model: legal, off-topic, unsafe, prompt injection (`scope_test.py`) | 31/31 (third run) |
| "Which law applies?" test with the real model (`citations_test.py`) | 10/10 (third run) |

Two notes on the last two rows. The first two scope runs scored 27/31 and the first two citation runs 9/10; the failures and fixes are in `AI_ERRORS_LOG.md` (entries 10 and 11). In the final runs one check each was my test's fault: it matched "ram" inside "framework", and it didn't count "s.173" as naming a section. I fixed the checks and re-scored the saved replies; the replies themselves weren't touched, and the summary files say so.

## Bugs found and fixed

| How bad | Bug | Fix |
|---|---|---|
| High | Switching case while Haq was answering wrote the reply into the other case | Switching, New case and Delete wait for the answer |
| High | A network failure froze the message box for good | `api()` never throws; you get a short error instead |
| High | The paid eCourts limit could be bypassed with a fake `X-Forwarded-For`; AI endpoints had no limits or size caps | Per-client hourly limits (real client IP only), a daily eCourts cap, 800 KB / 10 MB size caps |
| High | Deadlines and email reminders vanished after a court error, a notice explanation or (later) a greeting | The case panel reads the last answer that carries case data |
| Med | Word download failed (500) for Hindi titles, and the browser saved the error page as a .docx | Proper UTF-8 filename; the browser checks the response |
| Med | "15 days, by 20.03.2026" in a notice became 152,032,026 days and broke every later message | Only a 1–3 digit number, capped at 365 |
| Med | "Delete all my data" said it worked even when it hadn't | Each step is checked; the device copy is cleared only after success |
| Med | Calendar events were zero-length in India (time zone) | End date built from local date parts |
| Med | Malformed AI JSON caused errors or a broken evidence locker | Shapes are checked on server and browser |
| Med | Corrupt PDF gave a 500; any file type (even .exe) was accepted | Clear messages; photos, PDF and text only |
| Med | Sign-up reported a weak password as "account exists" | Errors mapped by Supabase error code |
| Med | The edit box stayed open until the new answer arrived | It closes on Send / Enter; the original text comes back if the request fails |
| Low | Empty "Explain notice" still sent a request; the theme toggle closed settings; raw provider errors shown in chat; `..` tricks in an order filename; no `.dockerignore` | Fixed |
| AI | Prompt injection made it say "as a senior advocate"; an ₹85 lakh case wasn't sent to a lawyer; "this case is absolutely clear"; invented section shielded by an old-law name; "a right guaranteed by Article 14" flagged as a promise | Guard rules and code floors, each with a test (see `AI_ERRORS_LOG.md`) |

## Changes on 7 Nov and how each was tested

**Practice hearing moved into the chat.** Haq offers a mock hearing once per case; reply "practice" and it plays the judge, "stop" gives a scorecard. Hearing messages are kept out of the legal answers and drafts. The coach once invented a date, so code now drops any suggested line with a number the user never gave. Still possible: a suggestion can name a document the user never mentioned.

**Past judgments search removed.** It used the kanoon.dev pilot API, which returned an error (HTTP 503) every time. Rather than ship something that never worked, I took out the panel, the endpoint and its tests. Haq still cites no case law.

**Legal assistant only.** Every message is labelled legal, general knowledge, greeting, off-topic or unsafe by the step that already reads it, so there's no extra AI call. Only legal messages get the full answer; greetings are answered by code; the rest get a short reply that goes through the same guard and never touches the case file. The user's own criminal, family or property matter now gets general guidance plus a lawyer recommendation instead of only a referral. Risk left: the router is a small model and can mislabel odd phrasing. The code backstops push mistakes towards the legal path, which is the safer direction.

**Buttons under every message.** Every message has its own permanent ID (from the server for chat, from the browser for drafts, court cards, practice and notices), so a button only ever acts on its own message. Edit and try again change only that exchange and keep the old answer as a version (‹ 1/2 ›). The case file only updates if it's the latest exchange. Ratings are saved with the case and logged on the server; a report also sends that answer's text. Limit: editing an earlier message doesn't re-answer the later ones.

**Answers name the laws that apply.** 21 more provisions in the library, each read from an official PDF. The law offered to the model now depends on the question asked, and every provision named in an answer gets a link to its official text. Not in the library because I couldn't open an official copy: the IT Act's 2008 sections, the Special Marriage Act and property statutes. Answers on those explain the rule in words without a section number.

## Known limitations
- **Sign-up doesn't confirm the email address.** I set it up this way when Supabase's own email couldn't reach users. Now that Brevo email works, this could switch to email confirmation.
- **Rate limits live in memory**, so they reset on restart and are per server. Fine for one free server; a real deployment would use Redis.
- **Prompt-only rules can be ignored.** In one probe the model still called a car's engine failure a "deficiency in service" (for goods it should be "defect"). Advice that's wrong without citing anything is the main risk left.
- **Criminal law is covered only partly.** The library has the BNS / BNSS commencement, cheating, theft, FIR and arrest provisions; other offences are explained without section numbers.
- **The reply language follows the app's language setting.** Someone who types in Hindi but leaves the app in English gets English replies.
