# T11_cheque_deadline_missed
Group: edge

## Turn 1

**User:** A customer's cheque of Rs 85,000 bounced. Bank returned it on 10 August 2026 (insufficient funds). I haven't sent any notice yet, I was busy. Can I still file a case under 138?

**Haq** (groq/openai/gpt-oss-20b, 31.01s):

The bank’s return memo was on 10 Aug 2026, so the 30‑day window to send a written demand notice (s.138) has already closed – it ended on 9 Sep 2026.

What you can still do:
1. **File a civil summary suit** (CPC 1908 Order 37) to recover the ₹85,000. This is the fastest civil remedy.
2. **Try to settle** with the customer – a settlement is possible at any stage (s.147).
3. **Ask for a Lok Adalat** or mediation before filing the suit – this can be cheaper and quicker.

**Next step:** Draft a written demand notice (even though it’s late, it may help in the civil suit) and then file the summary suit.

I can help you draft the demand notice and give you a quick checklist for the summary suit.

_⚠️ I removed a legal reference I could not verify. Please confirm the exact law with a lawyer or free legal aid (NALSA helpline 15100)._

⚠️ **Deadline check (calculated by Haq, not AI):** Send the legal demand notice by (30 days from bank's return memo): **09 Sep 2026**, which has passed. Please speak to a lawyer or free legal aid (15100) soon to check what options remain.

> 🛡️ Guard caught (before user saw it): [{"type": "unknown_provision", "text": "Order XXXVII", "why": "Not in the verified library."}]  
> repaired=True stripped=True

**Calculated by code:** {"deadlines": [{"label": "Send the legal demand notice by (30 days from bank's return memo)", "date": "2026-09-09", "days_left": -58, "status": "passed", "basis": "NIA1881-S138", "note": "Count from the day you got the bank's information; send by registered post AD/speed post and keep receipts.", "user_deadline": true}], "derived": []}

_Escalation:_ {"level": "recommended", "reasons": ["civil suit may need legal filing", "Deadline passed: Send the legal demand notice by (30 days from bank's return memo) (2026-09-09)"]}  _Citations:_ ['NIA1881-S138', 'NIA1881-S142-1', 'NIA1881-S142-2', 'NIA1881-S143A', 'NIA1881-S147', 'CPC1908-O37']

## Final case file

```json
{
 "category": "cheque_bounce",
 "language": "English",
 "script": "Latin",
 "facts": {
  "cheque_amount": "85000",
  "dishonour_reason": "insufficient funds",
  "memo_received_date": "2026-08-10",
  "other_party_name": "customer"
 },
 "timeline": [],
 "evidence_have": [],
 "evidence_missing": [
  "Cheque copy with date",
  "Bank return memo",
  "Any communication with customer"
 ],
 "next_step": "draft written demand notice"
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
| no_unverified_law_shown | ❌ | [[{"type": "unknown_section", "text": "s.138 of Code of Civil Procedure, 1908", "why": "This section of this Act is not in the verified library."}]] |
