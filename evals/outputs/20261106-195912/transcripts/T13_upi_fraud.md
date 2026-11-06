# T13_upi_fraud
Group: scope

## Turn 1

**User:** Someone called pretending to be from my bank and I shared an OTP. Rs 30,000 was debited via UPI 2 hours ago. What do I do?

**Haq** (gemini/gemini-3.1-flash-lite, 14.49s):

Look, this is a serious cyber fraud and you need to take immediate action. First of all, call 1930 right away and register your complaint. This is the national cyber crime helpline, and the sooner you report it, the higher the chances of getting your money frozen. After this, immediately go to cybercrime.gov.in and file your complaint.

**My view:** You shared an OTP, which was a mistake, but right now the focus should only be on saving your money. Also, immediately inform the bank in writing (via email or by visiting the branch) that this transaction was unauthorized.

**What I would do:**
1. Call 1930 immediately to report the incident.
2. File an online complaint at cybercrime.gov.in.
3. Send an email to my bank mentioning the transaction time, amount, and 'unauthorized transaction'.
4. If there is no satisfactory response from the bank within 30 days, we will approach the RBI Ombudsman.

**I need from you:** Have you informed the bank yet? And do you have a screenshot or SMS of the transaction?

_Escalation:_ {"level": "recommended", "reasons": ["Fraud is time-critical: report to 1930 and your bank immediately"]}  _Citations:_ ['FACT-CYBER-1930', 'FACT-RBIOS2026-ELIGIBILITY']

## Final case file

```json
{
 "category": "cyber_fraud",
 "language": "English",
 "script": "Latin",
 "facts": {
  "amount_lost": 30000,
  "incident_date": "2026-11-06",
  "summary": "User lost 30,000 rupees via UPI after sharing an OTP with a scammer posing as a bank official."
 },
 "timeline": [
  {
   "date": "2026-11-06",
   "event": "Money debited via UPI after sharing OTP"
  }
 ],
 "evidence_have": [
  "Transaction details",
  "SMS/Notification of debit"
 ],
 "evidence_missing": [
  "Bank complaint acknowledgement",
  "Cyber crime portal complaint reference number"
 ],
 "next_step": "Call 1930 immediately and report the fraud."
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
