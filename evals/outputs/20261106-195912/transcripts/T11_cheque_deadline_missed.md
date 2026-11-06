# T11_cheque_deadline_missed
Group: edge

## Turn 1

**User:** A customer's cheque of Rs 85,000 bounced. Bank returned it on 10 August 2026 (insufficient funds). I haven't sent any notice yet, I was busy. Can I still file a case under 138?

**Haq** (gemini/gemini-3.1-flash-lite, 10.45s):

Look, the bottom line is that the time to send your 30-day legal notice has passed. For a criminal case under Section 138, it is mandatory to send the notice within 30 days of receiving the memo from the bank, and your deadline expired on 9 September 2026. Therefore, you can no longer file a Section 138 case on technical grounds.

**My view:**
The criminal route is now closed to you, but civil avenues for recovering your money are still open. You can file a 'Summary Suit', which is a fast and effective way to recover money in cheque bounce cases. In this, you will have to prove in court that this money is legally owed to you. You should meet with a lawyer to prepare for a civil suit.

**Law on your side:**
*   **Order XXXVII of the Code of Civil Procedure, 1908:** This is the provision for a 'Summary Suit'. In this, you can file a suit for recovery of money using the cheque as evidence. It proceeds faster than a normal civil suit.

**What they will say, and your answer:**
*   They might say that the notice was not received or that the time has passed. Your answer will be that the expiry of the notice period does not extinguish your debt; your claim is still valid.

**What I would do:**
1. Show all your documents (cheque, bank memo, and any agreement or bill, if available) to a civil lawyer today.
2. Ask them to file a 'Summary Suit'. The limitation period (the time to file a case) in civil court is up to 3 years, so you still have plenty of time.

**I need from you:**
1. Do you have any written agreement or invoice with that customer for which this cheque was given?
2. Have you sent them any message or email asking for the money back?

**Calculated by code:** {"deadlines": [{"label": "Send the legal demand notice by (30 days from bank's return memo)", "date": "2026-09-09", "days_left": -58, "status": "passed", "basis": "NIA1881-S138", "note": "Count from the day you got the bank's information; send by registered post AD/speed post and keep receipts.", "user_deadline": true}], "derived": []}

_Escalation:_ {"level": "recommended", "reasons": ["Since the S.138 criminal route is time-barred, you need a lawyer to initiate a civil Summary Suit for recovery.", "Deadline passed: Send the legal demand notice by (30 days from bank's return memo) (2026-09-09)"]}  _Citations:_ ['NIA1881-S138', 'CPC1908-O37']

## Final case file

```json
{
 "category": "cheque_bounce",
 "language": "English",
 "script": "Latin",
 "facts": {
  "cheque_amount": 85000,
  "presentation_date": "2026-08-10",
  "dishonour_reason": "insufficient funds",
  "memo_received_date": "2026-08-10",
  "summary": "User wants to know if they can file a Section 138 case for an Rs 85,000 cheque that bounced on 2026-08-10, as no notice has been sent yet."
 },
 "timeline": [
  {
   "date": "2026-08-10",
   "event": "Cheque dishonoured"
  },
  {
   "date": "2026-09-09",
   "event": "Deadline for S.138 notice passed"
  }
 ],
 "evidence_have": [
  "Cheque",
  "Bank return memo"
 ],
 "evidence_missing": [
  "Written agreement or invoice",
  "Proof of communication (messages/emails)"
 ],
 "next_step": "Consult a civil lawyer to file a Summary Suit under Order 37 CPC."
}
```

## Automatic checks

| check | pass | detail |
|---|---|---|
| category | ✅ | got cheque_bounce |
| reply_language | ✅ | expected Latin, reply script Latin |
| fact:memo_received_date | ✅ | expected ~2026-08-10, got 2026-08-10 |
| escalation>=recommended | ✅ | got recommended |
| deadline:NIA1881-S138 | ✅ | [{"label": "Send the legal demand notice by (30 days from bank's return memo)", "date": "2026-09-09", "days_left": -58, "status": "passed", "basis": "NIA1881-S1 |
| no_unverified_law_shown | ✅ |  |
