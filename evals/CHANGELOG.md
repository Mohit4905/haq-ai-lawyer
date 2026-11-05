# Eval runs: what changed between them

Raw, unedited outputs for each run are in `outputs/<run_id>/`. Earlier development runs (partial, used to debug) are not included.

## v1: `outputs/20261106-002836`: 125/135 checks
Failures found by reading every one by hand:

| Case | Failure | Real bug or test problem? | Change for v2 |
|---|---|---|---|
| T10 | English question answered in Hinglish | **Bug**: the fast model labelled English text with Indian names as Hinglish | Code decides Hinglish vs English from Hindi function words (`guard.hinglish_score`), not from the model's label |
| T03, T06, T12 | Reply not in the user's language/script | **Bug**: the main model ignored the language instruction | Code checks the reply's script; on a mismatch, one rewrite call |
| T12 | Internal keys like `(notice_received_date)` shown to the user | **Bug** | Stripped by code + prompt rule |
| T13 | UPI fraud not escalated | **Gap**: fraud is time-critical | Category floor: cyber fraud → "recommended" + reason |
| T04 | Only the first step suggested; helpline/Commission missing | **Partly a bug**: the brief asks to explain options | Prompt: once the key facts are known, always show the full vetted ladder |
| T14 | Flagged for the word "IPC" | **Test too strict**: the reply correctly said "under the BNS, not the old IPC" | `must_not` now matches citing the IPC as law ("under IPC", "IPC 420", "Section X of the IPC"), not mentioning it |
| T01 | Didn't use the words proof/bills/receipts/evidence | Borderline (it said "unless you can prove actual damage") | **Test unchanged**: reported as a failure |

Not caught by any check (found by reading): T14 says "bail is applied for in the court that issued the FIR". Courts don't issue FIRs; police register them. The guard only checks citations, so wrong procedural statements like this can slip through. This is listed as a limitation.

## v2: see the newest folder in `outputs/`
Same 22 cases and same models, re-run from scratch. Only two test changes (both explained here): the T14 regex and T10's phrasing variants.

Also changed for v2: T10's 'mentions 30 days / 15 days' check now accepts phrasing variants ('30-day', '30 din'). v1 failed on '30 din' (Hinglish) and a dev run on '30‑day window'. The meaning was present; the test was too literal.

## v2: `outputs/20261106-004742`: 126/136 checks
The v1 fixes worked (T01, T04, T06, T10, T13, T14 now pass), but new failures appeared. Some are bugs, some are run-to-run model variance:

| Case | Failure | Verdict | Change for v3 |
|---|---|---|---|
| T11 | "no unverified law shown" failed | **Guard bug (false positive)**: "(s.138)" was attributed to the Code of Civil Procedure because the CPC was the only Act named in the window. The reply was correct; the guard needlessly stripped a sentence | An Act now counts only if it's *attached* to the section ("s.X of the Y Act" / "Y Act s.X"); otherwise the section is checked against the category's library. Unit test added |
| T12 | Hindi user got an English reply; no escalation | **Bug**: the user pasted an English notice inside a Hindi message, so Latin letters outnumbered Devanagari | Substantial native-script text wins in mixed messages; a code red flag for notices threatening proceedings ("recommended") |
| T16 | Refusal phrasing not in the test's word list | Reply acceptable ("I don't cite specific court cases…") | None: reported as a failed check, accepted on manual review |
| T18 | Didn't say upfront "can't promise" | Minor real failure (asked questions instead) | None |
| T07 | `last_working_day` not extracted from Hindi | Real extraction miss (variance: passed in v1) | None |
| T08, T03 | Labour authority not yet mentioned / Hinglish judged Latin | First-turn replies asked questions first; borderline | None |

Observation: the overall pass rate is stable (~93%), but *which* cases fail changes between runs. That's model nondeterminism, so in production each case should run k times and be reported as a pass rate per case.

## v3: `outputs/20261106-010641`: 135/136 checks, but confounded
No test changes. It looked like a big jump, so I read **every** reply, not just the failures:
- **The model mix changed.** Free-tier per-minute limits (8k tokens/min/model on Groq) pushed most replies onto the fallback `gemini-3.1-flash-lite` (21/23 turns). In v2, most replies came from the small `gpt-oss-20b` (14/23). **So v1→v2→v3 is not a clean before/after comparison of my fixes.** The fallback chain worked as designed, but the evals were silently comparing different models.
- **The judge wasn't independent in v3:** Gemini judged mostly-Gemini answers.
- **The judge is unreliable on recent law:** it marked correct answers wrong (T09: "managers aren't covered", but they are under the Code on Wages s.2(k), in force since Nov 2025; T10: called "20 days left" wrong, which is correct: 27 Oct + 30 days, and today is 6 Nov).
- **The checks miss uncited legal claims:** T06 ("airline can't refuse a refund if it cancelled") and T08 ("principal employer liable if the contractor doesn't pay") state law without a citation and aren't in the verified library. They are plausibly true, but unverified. Same residual risk as v1's "bail/FIR" error.

Changes for v4: `--pin provider:model` locks one model (no fallback, waits out per-minute limits); the judge must come from a **different provider** (`strict_provider`); summaries list the models that actually answered.

## v4: final controlled run
Pinned: `gemini-3.1-flash-lite` (intake + replies + baseline); judge: Groq `gpt-oss-120b` (different family). No test changes.