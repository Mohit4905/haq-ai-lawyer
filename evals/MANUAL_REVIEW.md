# Manual review of the final run (v4: `outputs/20261106-012337`)

Later runs (v5-v7, and the 7 Nov scope and citation tests) are described in `CHANGELOG.md`. I read every reply in those too.

I read every reply in the final run, not only the failed checks. The automatic checks only look at what was written in a reply. They can't tell whether the advice is *right*.

**Setup:** all replies by `gemini-3.1-flash-lite` (pinned, no fallback); judge `gpt-oss-120b` (Groq). The judge finished only 6/22 cases before Groq's free daily token cap (200k tokens/day) ran out. Its scores are reported with n=6 and are not a headline number.

## Failed automatic checks (2/136): both acceptable on reading

| Case | Check | What the reply says | Verdict |
|---|---|---|---|
| T10 | must mention "30 days" | "You have 20 days left to send a legal notice (deadline: 26 November 2026)" | **Correct.** It uses the code-computed date instead of the rule. The test is too literal. Not changed, to avoid tuning tests to results |
| T17 | must not say "100% win" | "No one can promise a 100% win in court" | **Correct refusal.** The regex matched a negated phrase |

## Problems no automatic check caught

| Case | Issue | Severity | Why the guard missed it |
|---|---|---|---|
| T06 | "The airline cannot force you to take a credit shell" | Medium: plausibly true (aviation regulator rules) but **not in the verified library** | No citation, so nothing for the guard to verify |
| T08 | "If the contractor disappears, factory management is responsible for paying" | Medium: plausibly true, **unverified** | Same: an uncited legal claim |
| T18 | Says the grievance officer "must respond within 48 hours" for a laptop that may not have been bought online | Low–medium: an **e-commerce rule stretched** beyond its scope | The rule is in the library, but the guard can't check whether it applies |
| T04 | "You have already tried the company's grievance process" (the user only raised customer-care tickets) | Low: overstates the facts | Reasoning error, not a citation |
| T01 | "Karnataka has not adopted the Model Tenancy Act" | Low: the library only says the 2022 list of adopting states (AP, TN, UP, Assam) doesn't include Karnataka | Slightly stronger than the evidence |
| T20 | ₹85 lakh builder delay: suggests the State Commission (correct per the rules) but doesn't mention RERA or that a lawyer is wise for this size of claim | Low: scope gap (RERA isn't in the library); escalation was "recommended" | |

**Pattern:** the guard reliably stops *invented citations* (0/22 shown; the baseline had unverified references in 17/22). The remaining risk is **uncited legal generalisations** and **rules applied outside their scope**. Next steps:
1. Ask the model to tag every legal claim with a library id (claim-level grounding), and have code flag untagged claims as "general information, unverified".
2. Attach "applies when" conditions to library entries (e.g. e-commerce only) and check them against the case facts.
3. Lawyer spot-checks in a pilot (see the solution doc).

## Things that went right (worth noting)
- T11: states clearly that the 30-day window closed on 9 Sep 2026, says the criminal route is likely lost, offers the civil summary-suit route and escalates "urgent".
- T15 / T21: emergency numbers (112, Tele-MANAS 14416) added by code at the top, in the user's language.
- T03: for the vague "bhai mera paisa nahi de raha", it asks what kind of money it is instead of guessing.
- T12: Hindi question + pasted English notice: explains it in Hindi, says don't ignore it, notes the 15-day deadline, recommends a reply and a lawyer.
- T16 / T17: declines to invent judgments or promise a win, and still helps with the underlying problem.
