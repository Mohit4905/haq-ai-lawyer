# T13_upi_fraud
Group: scope

## Turn 1

**User:** Someone called pretending to be from my bank and I shared an OTP. Rs 30,000 was debited via UPI 2 hours ago. What do I do?

**Haq** (gemini/gemini-3.1-flash-lite, 9.17s):

This is a serious case of cyber fraud. Since you lost the money just 2 hours ago, you still have a chance to get the transaction frozen. First and foremost, you must report it immediately.

**Your legal position:**
In cases of cyber fraud, the faster you report it, the higher the chances of recovering your money. You shared an OTP, which is a security lapse, but banks and payment apps also have a responsibility to monitor suspicious transactions. Your case will only be strong if you file a report through official channels immediately.

**Law you can cite:**
* **National Cyber Crime Helpline (1930):** This helpline is for reporting fraud immediately so that the bank account can be frozen.
* **Bharatiya Nagarik Suraksha Sanhita, 2023 (Section 173):** You can file a 'Zero FIR' at any police station, regardless of where the fraud occurred.
* **Reserve Bank - Integrated Ombudsman Scheme, 2026:** If the bank does not take action on your complaint within 30 days, you can approach the RBI Ombudsman.

**What to do now:**
1. **Call 1930 immediately:** This is the most important step. Call this number and provide your transaction details.
2. **Report on cybercrime.gov.in:** Register your complaint on this portal and keep the acknowledgement number safe.
3. **Inform your bank:** Inform your bank in writing (via email or by visiting the branch) that an unauthorized transaction has occurred from your account.

**I need from you:**
1. Have you informed your bank yet?
2. Do you have proof of the transaction, such as a screenshot or an SMS alert?

_Escalation:_ {"level": "recommended", "reasons": ["Fraud is time-critical: report to 1930 and your bank immediately"]}  _Citations:_ ['FACT-CYBER-1930', 'BNSS2023-S173', 'FACT-RBIOS2026-ELIGIBILITY']

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
   "event": "Fraud occurred via UPI after sharing OTP"
  }
 ],
 "evidence_have": [
  "Transaction details"
 ],
 "evidence_missing": [
  "Bank complaint acknowledgement",
  "Cyber crime portal complaint reference number"
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
