# T11_cheque_deadline_missed
Group: edge

## Turn 1

**User:** A customer's cheque of Rs 85,000 bounced. Bank returned it on 10 August 2026 (insufficient funds). I haven't sent any notice yet, I was busy. Can I still file a case under 138?

**Haq** (gemini/gemini-3.1-flash-lite, 16.09s):

Namaste. I understand this is frustrating—Rs 85,000 is a significant amount. Looking at the dates, the 30-day window to send a legal notice (which is a mandatory first step for a Section 138 criminal case) expired on 9 September 2026. Because this deadline has passed, you cannot initiate the standard criminal complaint under the Negotiable Instruments Act for this specific cheque.

**Your legal position:**
Since the mandatory notice period has lapsed, the criminal route under Section 138 is effectively closed. However, you still have a valid civil claim to recover your money, as the debt itself remains legally enforceable.

**Law you can cite:**
* **Code of Civil Procedure, 1908 (Order XXXVII):** This allows for a 'summary suit' for recovery of money based on a cheque or written contract, which is often faster than a regular civil suit.
* **Limitation Act, 1963:** Generally, you have 3 years from the date of the cheque or the date of dishonour to file a civil suit for recovery of money.

**What to do now:**
1. **Consult a lawyer:** Since the criminal route is closed, you need a lawyer to file a civil summary suit for recovery. This is your best path to get your money back.
2. **Free Legal Aid:** If you need help finding a lawyer, call the national legal aid helpline at 15100 or visit your local District Legal Services Authority (DLSA).

I strongly recommend speaking to a lawyer immediately to check if any other options exist in your specific jurisdiction. I cannot draft a Section 138 notice for you as the deadline has passed.

**Calculated by code:** {"deadlines": [{"label": "Send the legal demand notice by (30 days from bank's return memo)", "date": "2026-09-09", "days_left": -58, "status": "passed", "basis": "NIA1881-S138", "note": "Count from the day you got the bank's information; send by registered post AD/speed post and keep receipts.", "user_deadline": true}], "derived": []}

_Escalation:_ {"level": "recommended", "reasons": ["The criminal deadline has passed; a civil recovery suit requires professional legal drafting and filing.", "Deadline passed: Send the legal demand notice by (30 days from bank's return memo) (2026-09-09)"]}  _Citations:_ ['NIA1881-S138', 'CPC1908-O37', 'FACT-NALSA-HELPLINE']

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
   "event": "Deadline for legal notice passed"
  }
 ],
 "evidence_have": [
  "Cheque return memo"
 ],
 "evidence_missing": [
  "Original cheque",
  "Proof of debt (invoice, contract, or loan agreement)"
 ],
 "next_step": "Consult a lawyer to file a civil summary suit for recovery."
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
