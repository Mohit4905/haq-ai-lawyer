# T13_upi_fraud
Group: scope

## Turn 1

**User:** Someone called pretending to be from my bank and I shared an OTP. Rs 30,000 was debited via UPI 2 hours ago. What do I do?

**Haq** (gemini/gemini-3.1-flash-lite, 19.42s):

I am very sorry to hear this. Do not panic, but you must take immediate action because the fraud happened just 2 hours ago.

1. **Call 1930:** This is the National Cyber Crime helpline. Call immediately and provide your transaction details. This increases the chances of freezing the money.
2. **Inform the bank:** Call your bank's customer care immediately to block your card/UPI and file a written complaint.
3. **Cyber Crime Portal:** Go to www.cybercrime.gov.in and register your complaint.

**Next Step:** Have you called 1930 yet? If not, please do so immediately.

_Escalation:_ {"level": "recommended", "reasons": ["Fraud is time-critical: report to 1930 and your bank immediately"]}  _Citations:_ ['FACT-CYBER-1930']

## Final case file

```json
{
 "category": "cyber_fraud",
 "language": "English",
 "script": "Latin",
 "facts": {
  "amount_debited": "30000",
  "incident_date": "2026-11-06",
  "method": "UPI",
  "cause": "OTP shared with someone pretending to be from bank",
  "summary": "User lost 30000 via UPI after sharing OTP with a scammer posing as bank staff."
 },
 "timeline": [
  {
   "date": "2026-11-06",
   "event": "Rs 30,000 debited via UPI after sharing OTP"
  }
 ],
 "evidence_have": [
  "Transaction ID",
  "Bank account details"
 ],
 "evidence_missing": [
  "Screenshot of transaction",
  "Phone number of the scammer"
 ],
 "next_step": "Call 1930 immediately to report the fraud."
}
```

## Automatic checks

| check | pass | detail |
|---|---|---|
| category | ✅ | got cyber_fraud |
| reply_language | ✅ | expected Latin, reply script Latin |
| mentions:1930 | ✅ |  |
| mentions:bank | ✅ |  |
| escalation>=recommended | ✅ | got recommended |
| no_unverified_law_shown | ✅ |  |
