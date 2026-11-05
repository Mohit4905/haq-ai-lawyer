# T11_cheque_deadline_missed
Group: edge

## Turn 1

**User:** A customer's cheque of Rs 85,000 bounced. Bank returned it on 10 August 2026 (insufficient funds). I haven't sent any notice yet, I was busy. Can I still file a case under 138?

**Haq** (groq/openai/gpt-oss-120b, 25.78s):

The 30‑day window to send a demand notice under s.138 has already passed (deadline was 9 Sept 2026). Because the notice period is missed, filing a criminal complaint under s.138 is now risky – courts may reject it as out of time. You could still try a civil summary suit to recover the ₹85,000, but you’ll need a lawyer to check if it’s viable.

**What you can do next**
- Gather all proof: the bounced‑cheque copy, bank’s return memo (dated 10 Aug 2026), any email/WhatsApp where the customer promised payment, and your bank statements showing the cheque was presented.
- Talk to a lawyer (free legal aid via NALSA 15100 or Tele‑Law) to see if a civil suit or any other remedy is possible.
- If you later manage to send a notice, it may help in settlement, but it won’t revive the criminal route.

I can help draft a simple demand notice you can still send, or prepare a list of documents for a lawyer.

⚠️ **Deadline check (calculated by Haq, not AI):** Send the legal demand notice by (30 days from bank's return memo): **09 Sep 2026**, which has passed. Please speak to a lawyer or free legal aid (15100) soon to check what options remain.

**Calculated by code:** {"deadlines": [{"label": "Send the legal demand notice by (30 days from bank's return memo)", "date": "2026-09-09", "days_left": -58, "status": "passed", "basis": "NIA1881-S138", "note": "Count from the day you got the bank's information; send by registered post AD/speed post and keep receipts.", "user_deadline": true}], "derived": []}

_Escalation:_ {"level": "recommended", "reasons": ["criminal route likely time‑barred; civil suit needs legal advice", "Deadline passed: Send the legal demand notice by (30 days from bank's return memo) (2026-09-09)"]}  _Citations:_ ['NIA1881-S138', 'NIA1881-S142-1', 'CPC1908-O37']

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
  "other_party_name": "customer"
 },
 "timeline": [
  {
   "date": "2026-08-10",
   "event": "Bank returned cheque (insufficient funds)"
  }
 ],
 "evidence_have": [
  "bounced cheque copy",
  "bank return memo (10 Aug 2026)"
 ],
 "evidence_missing": [
  "proof of cheque date, any communication promising payment, bank statement showing presentation"
 ],
 "next_step": "Consult a lawyer (free legal aid) to explore a civil summary suit and gather all documents"
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
