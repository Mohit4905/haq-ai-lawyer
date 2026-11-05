# T11_cheque_deadline_missed
Group: edge

## Turn 1

**User:** A customer's cheque of Rs 85,000 bounced. Bank returned it on 10 August 2026 (insufficient funds). I haven't sent any notice yet, I was busy. Can I still file a case under 138?

**Haq** (gemini/gemini-3.1-flash-lite, 9.85s):

I have some difficult news. Under the Negotiable Instruments Act, you are required to send a legal demand notice within 30 days of receiving the bank's return memo. Since your memo was dated 10 August 2026, that deadline passed on 9 September 2026.

Because this 30-day window has expired, you likely cannot file a criminal case under Section 138 of the Negotiable Instruments Act. 

However, you may still have options to recover your money through a civil route, such as a summary suit for recovery of money. Because the legal timelines are strict and the situation is now complex, I strongly recommend you speak with a lawyer or contact free legal aid to see if any other legal path remains for your specific case.

- **Next Step:** Please contact the National Legal Aid helpline at 15100 for free guidance on whether a civil recovery suit is still viable for you.

**Calculated by code:** {"deadlines": [{"label": "Send the legal demand notice by (30 days from bank's return memo)", "date": "2026-09-09", "days_left": -58, "status": "passed", "basis": "NIA1881-S138", "note": "Count from the day you got the bank's information; send by registered post AD/speed post and keep receipts.", "user_deadline": true}], "derived": []}

_Escalation:_ {"level": "urgent", "reasons": ["The statutory deadline for the criminal cheque bounce case has passed; a lawyer is needed to explore civil recovery options.", "Deadline passed: Send the legal demand notice by (30 days from bank's return memo) (2026-09-09)"]}  _Citations:_ ['NIA1881-S138', 'CPC1908-O37', 'FACT-NALSA-HELPLINE']

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
  "Proof of debt (invoice/contract)"
 ],
 "next_step": "Contact NALSA helpline 15100 for legal aid"
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
