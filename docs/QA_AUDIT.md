# End-to-end QA audit (6 Nov 2026)

How it was done: a cold-read static review of every Python/JS/HTML file (by a separate reviewer that hadn't written the code), then the app was **run** and driven by browser scripts (Edge, Playwright) on desktop and phone sizes, plus API attack tests and new legal questions to the AI. Every bug below was reproduced, fixed, and re-tested. Scripts: `scripts/qa/` (the eCourts/kanoon.dev calls go to a local fake server, `mock_court.py`, so the tests spend no credits).

## Inventory
- **Pages:** `/login` (log in, create account, forgot/reset password, Google, guest), `/` (app), `/privacy`, `/terms`.
- **App:** chat (text, voice, attach notice), welcome cards, sidebar (New case, Track case, Case file, Deadlines, Documents, Evidence, Practice, Get help, My cases with search and ⋯ rename/delete, collapse, Ctrl+B), tools open in the main area, settings (language, theme, AI model), account box, profile dialog, lawyer note, drafts in chat (fill blanks by replying), court card (Explain, Refresh, Add to calendar), downloads (.docx, .ics, case summary).
- **API (FastAPI):** chat, draft, draft/fill, docx, explain, evidence, practice, transcribe, court/{status, case, search, order, judgments}, signup, account/delete, cron/reminders, config, kb, health.
- **Integrations:** Groq + Gemini (LLMs, with fallback), Supabase (auth, database, storage), Brevo (email), eCourtsIndia (paid), kanoon.dev (pilot, currently down).
- **No placeholder, mock or TODO code** in the app. kanoon.dev is the one integration not yet verified on real data.

## Results (final run)
| Suite | Result |
|---|---|
| UI audit: every button, field, menu, tool, download, phone layout (`audit_ui.py`) | **82/82** |
| API robustness + security (`audit_api.py`) | **27/27** |
| XSS: hostile HTML in chat, replies, titles, court data, third-party links (`audit_xss.py`) | **6/6** |
| Smoke test with real AI answers (`scripts/ui_smoke.py`) | **19/19** |
| Drafts in chat / court tracking / lawyer note / New case | 11/11 · 13/13 · 12/12 · 14/14 |
| Unit tests · law-library integrity | 28/28 · OK |
| Eval suite v7 (22 cases, 5 languages) | 134/136 (both failures read and fixed; see `evals/CHANGELOG.md`) |

## Bugs found and fixed
| Sev. | Bug | Fix |
|---|---|---|
| High | Switching case while Haq was answering wrote that reply (and the whole conversation) into the other case | Switching, New case and Delete wait until the answer arrives |
| High | A network failure froze the composer for good (busy flag never reset) | `api()` never throws; returns a friendly error |
| High | Paid eCourts limit could be bypassed with a fake `X-Forwarded-For`; AI endpoints had no limits; no size caps | One request guard: per-client hourly limits (IP from Cloudflare/proxy headers, never the client-set first hop), a daily eCourts cap, 800 KB JSON / 10 MB upload caps |
| High | Deadlines and email reminders vanished after a court error or a notice explanation | Deadlines are read from the last turn that has them |
| Med | Word download crashed (500) for Hindi titles, and the client saved the error page as a .docx | RFC 5987 filename; the client checks the response |
| Med | "15 days, by 20.03.2026" in a notice became 152,032,026 days, so every later chat turn returned 500 | First 1–3 digit number only, capped at 365 |
| Med | `javascript:` links from the third-party judgments API could reach the page | http(s) only, on server and client |
| Med | "Delete all my data" said it succeeded even when it hadn't, and left data on the device | Each step is checked; the device copy is cleared only after success |
| Med | Calendar events were zero-length in India (timezone) | End date built from local date parts |
| Med | Malformed AI JSON caused 500s or a permanently broken evidence locker | Shapes are validated on server and client |
| Med | Corrupt PDF → 500; any file type accepted by "Explain notice" and the evidence locker (including .exe) | Clear 4xx messages; photos/PDF/text only |
| Med | Drafting with a malformed case → 500 | Clear message instead |
| Med | Signup: a weak password was reported as "account exists" | Errors mapped by Supabase error code |
| Low | Empty "Explain notice" still sent a request; Practice crashed before a case existed; light/dark toggle closed the settings box; login page had no privacy/terms links | Fixed |
| Low | Raw provider errors (model names, HTTP bodies) shown in chat | Logged on the server; users see a short message |
| Low | Path tricks (`..`) in an order filename; no `.dockerignore` (`.env` could enter a Docker image); a Supabase call awaited inside the auth callback (deadlock risk); dead code | Fixed |
| AI | A prompt injection made it say "as a senior advocate…"; ₹85 lakh case not referred to a lawyer; the rewritten answer said "You are right, I made a mistake"; "this case is absolutely clear" (EN/Hinglish/Hindi); a Hinglish reply to an English-interface user | Guard violations + code floor (≥ ₹10 lakh → lawyer) + prompt fixes, each re-tested |

## Known limitations (not fixed)
- **Accounts are created without proving email ownership** (server-side signup, done when Supabase's built-in email couldn't reach users). Now that Brevo email works, this could switch to email confirmation.
- **Rate limits are in memory**, so they reset when the server restarts and are per instance. Fine for one free instance; production would use Redis.
- **Prompt-only rules can be ignored by a small model.** In the probe, `gemini-3.1-flash-lite` still called a car's engine failure "deficiency in service" (a goods problem is a "defect"). Uncited legal generalisations remain the main residual risk.
- **Criminal questions are referred, not answered.** For example, the BNS punishment for cheating, because criminal law is outside the verified library.
- **The reply language follows the interface language** (the user asked for this). A Hindi typist who leaves the interface in English gets English replies.
- kanoon.dev was down (HTTP 503) all day, so that integration is unverified on real data.
