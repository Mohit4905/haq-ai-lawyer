# T11_cheque_deadline_missed
Group: edge

## Turn 1

**User:** A customer's cheque of Rs 85,000 bounced. Bank returned it on 10 August 2026 (insufficient funds). I haven't sent any notice yet, I was busy. Can I still file a case under 138?

**Haq** (gemini/gemini-3.1-flash-lite, 52.04s):

Namaste. Let me be direct: your 30-day deadline to send a legal notice expired on 9 September 2026. This means you can no longer file a criminal case under Section 138 of the Negotiable Instruments Act, as sending the notice is the first and mandatory requirement for it.

**Your legal position:**
Since the notice deadline has passed, the path for Section 138 is closed to you. Now, you only have the civil route remaining, where you can file a suit for the recovery of money, but for this, you will need to consult a lawyer to assess the strength of your case.

**Law you can cite:**
*   **Order XXXVII, Code of Civil Procedure, 1908:** This is the route for a 'Summary Suit', which is intended for clear money claims like cheques. It is different from Section 138, and through this, you can file a civil claim to recover your money.
*   **Section 147, Negotiable Instruments Act, 1881:** This states that cheque bounce cases can be settled (compounded) at any time. If you can still talk to the party and recover the money, that would be the best option.

**What to do now:**
1.  **Direct Settlement:** Talk to the party and ask for the money. This is the cheapest and fastest method.
2.  **Legal Aid:** Call 15100 (NALSA) to get free legal advice and ask if there is any chance for 'delay condonation' in your case or how to file a civil suit.
3.  **Civil Lawyer:** Meet with a civil lawyer and discuss filing a 'Summary Suit'.

**I need from you:**
1. Did you provide any written agreement or invoice to the party for the payment?
2. Have you asked them for the money via phone or message yet?

**Calculated by code:** {"deadlines": [{"label": "Send the legal demand notice by (30 days from bank's return memo)", "date": "2026-09-09", "days_left": -58, "status": "passed", "basis": "NIA1881-S138", "note": "Count from the day you got the bank's information; send by registered post AD/speed post and keep receipts.", "user_deadline": true}], "derived": []}

_Escalation:_ {"level": "recommended", "reasons": ["The statutory deadline for the criminal complaint has passed; a civil summary suit requires professional legal drafting and strategy.", "Deadline passed: Send the legal demand notice by (30 days from bank's return memo) (2026-09-09)"]}  _Citations:_ ['NIA1881-S138', 'CPC1908-O37', 'NIA1881-S147']

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
   "event": "Cheque bounced"
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
  "Written agreement or invoice for the transaction",
  "Proof of communication with the drawer"
 ],
 "next_step": "Call NALSA helpline 15100 for guidance on civil recovery options."
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
