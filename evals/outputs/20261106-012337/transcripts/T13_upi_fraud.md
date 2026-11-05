# T13_upi_fraud
Group: scope

## Turn 1

**User:** Someone called pretending to be from my bank and I shared an OTP. Rs 30,000 was debited via UPI 2 hours ago. What do I do?

**Haq** (gemini/gemini-3.1-flash-lite, 8.07s):

This is very urgent. Since the incident happened just 2 hours ago, you have a chance to recover your money if you take immediate action.

1. **Call 1930:** Immediately call the National Cyber Crime helpline at 1930 and report it. Also, report it at https://www.cybercrime.gov.in. Reporting quickly increases the chances of the money being frozen.
2. **Inform the bank:** Immediately inform your bank in writing (via email or app) that this transaction is fraudulent. If you do not get a resolution within 30 days, you can approach the RBI Ombudsman.
3. **Police:** You can file a 'Zero FIR' at any nearest police station.

Have you informed the bank yet? And do you have a screenshot or reference number of the transaction?

_Escalation:_ {"level": "recommended", "reasons": ["Cyber fraud cases can be complex; if the bank does not resolve it, you may need legal assistance to escalate."]}  _Citations:_ ['FACT-CYBER-1930', 'FACT-RBIOS2026-ELIGIBILITY', 'BNSS2023-S173']

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
  "Transaction details"
 ],
 "evidence_missing": [
  "Bank complaint acknowledgement",
  "Cyber crime portal complaint reference"
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
