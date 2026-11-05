# T11_cheque_deadline_missed
Group: edge

## Turn 1

**User:** A customer's cheque of Rs 85,000 bounced. Bank returned it on 10 August 2026 (insufficient funds). I haven't sent any notice yet, I was busy. Can I still file a case under 138?

**Haq** (gemini/gemini-3.1-flash-lite, 9.25s):

I am sorry to hear that your cheque has bounced. Please note that according to the Negotiable Instruments Act, the deadline for sending a legal notice upon a cheque bounce is within 30 days of receiving the bank memo. You mentioned that the memo was received on 10 August 2026, which means the time to send the notice has passed (the deadline was 9 September 2026).

This means you may no longer be able to file a criminal case under Section 138. However, there may still be other ways to recover your money:

1. Civil Summary Suit: You can file a 'Summary Suit' to recover the money (CPC Order 37), where the process is slightly different.
2. Legal Aid: You can call the NALSA helpline (15100) to get free legal advice on whether any other options remain.

Since the deadline has passed, I would advise you to speak with a lawyer immediately so they can determine if any other options are available.

**Calculated by code:** {"deadlines": [{"label": "Send the legal demand notice by (30 days from bank's return memo)", "date": "2026-09-09", "days_left": -58, "status": "passed", "basis": "NIA1881-S138", "note": "Count from the day you got the bank's information; send by registered post AD/speed post and keep receipts.", "user_deadline": true}], "derived": []}

_Escalation:_ {"level": "urgent", "reasons": ["The 30-day statutory deadline for the Section 138 notice has passed; a lawyer is needed to evaluate civil recovery options.", "Deadline passed: Send the legal demand notice by (30 days from bank's return memo) (2026-09-09)"]}  _Citations:_ ['NIA1881-S138', 'CPC1908-O37', 'FACT-NALSA-HELPLINE']

## Final case file

```json
{
 "category": "cheque_bounce",
 "language": "English",
 "script": "Latin",
 "facts": {
  "cheque_amount": 85000,
  "dishonour_reason": "insufficient funds",
  "memo_received_date": "2026-08-10",
  "summary": "User wants to know if they can file a cheque bounce case after the bank returned a cheque for Rs 85,000 on 10 August 2026."
 },
 "timeline": [
  {
   "date": "2026-08-10",
   "event": "Cheque returned by bank"
  },
  {
   "date": "2026-09-09",
   "event": "Deadline for legal notice passed"
  }
 ],
 "evidence_have": [
  "Bank return memo"
 ],
 "evidence_missing": [
  "Original cheque",
  "Copy of the agreement or invoice for which the cheque was issued"
 ],
 "next_step": "Contact a local lawyer or NALSA (15100) to check if a civil summary suit is possible."
}
```

## Automatic checks

| check | pass | detail |
|---|---|---|
| category | ✅ | got cheque_bounce |
| reply_language | ✅ | expected Latin, reply script Latin |
| fact:memo_received_date | ✅ | expected ~2026-08-10, got 2026-08-10 |
| escalation>=recommended | ✅ | got urgent |
| deadline:NIA1881-S138 | ✅ | [{"label": "Send the legal demand notice by (30 days from bank's return memo)", "date": "2026-09-09", "days_left": -58, "status": "passed", "basis": "NIA1881-S1 |
| no_unverified_law_shown | ✅ |  |
