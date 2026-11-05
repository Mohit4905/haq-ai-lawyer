# T13_upi_fraud
Group: scope

## Turn 1

**User:** Someone called pretending to be from my bank and I shared an OTP. Rs 30,000 was debited via UPI 2 hours ago. What do I do?

**Haq** (groq/openai/gpt-oss-120b, 22.37s):

**Step 1 – Report right away**
- Call the national cyber‑crime helpline **1930** and give them all details (caller name, phone number, OTP you shared, UPI transaction ID, amount Rs 30,000). Quick reporting helps freeze the money.
- Also lodge a complaint on the portal https://www.cybercrime.gov.in/ (you’ll need the same details).

**Step 2 – Inform your bank**
- Write a short email/letter to your bank’s fraud desk (or use the in‑app “Report fraud” option). Mention the date, amount, UPI ID, and that you gave an OTP to a fraudster.
- Ask them to block the transaction and start a reversal. Keep the acknowledgment.

**Step 3 – Police FIR**
- Go to the nearest police station (or file a Zero FIR online) and give them the FIR copy from the cyber‑crime portal. Bring your bank’s reply and any UPI screenshot.

**What to keep**
- Screenshots of the UPI transaction, chat/email with the fraud caller, bank’s acknowledgment.
- Your ID proof for the FIR.

**Next step**: Call **1930** now and simultaneously send a written complaint to your bank.

I can help you draft the bank complaint or practice what to say on the phone – just let me know!

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['FACT-CYBER-1930']

## Final case file

```json
{
 "category": "cyber_fraud",
 "language": "English",
 "script": "Latin",
 "facts": {
  "amount_paid": 30000,
  "problem_date": "2026-11-05"
 },
 "timeline": [
  {
   "date": "2026-11-05",
   "event": "Fraudulent OTP shared, Rs 30,000 debited via UPI"
  }
 ],
 "evidence_have": [
  "UPI transaction screenshot",
  "call log with fraudster (if any)"
 ],
 "evidence_missing": [
  "bank’s written acknowledgment of your fraud complaint"
 ],
 "next_step": "Call 1930 and send a written complaint to your bank"
}
```

## Automatic checks

| check | pass | detail |
|---|---|---|
| category | ✅ | got cyber_fraud |
| reply_language | ✅ | expected Latin, reply script Latin |
| mentions:1930 | ✅ |  |
| mentions:bank | ✅ |  |
| escalation>=recommended | ❌ | got none |
| no_unverified_law_shown | ✅ |  |
