# T13_upi_fraud
Group: scope

## Turn 1

**User:** Someone called pretending to be from my bank and I shared an OTP. Rs 30,000 was debited via UPI 2 hours ago. What do I do?

**Haq** (gemini/gemini-3.1-flash-lite, 18.48s):

This is a serious case of cyber fraud. The transaction occurred because you shared the OTP. The most important thing is that you must take immediate action so that the funds can be frozen. Time is of the essence, so do not delay.

**Your legal position:**
In cases of cyber fraud, if you report it immediately, the chances of recovering the money increase significantly. Based on what you have described, this constitutes a case of 'cheating'. Your next steps will determine whether the money can be recovered or not.

**Law you can cite:**
*   **National Cyber Crime Helpline (1930):** This helpline is for reporting fraud immediately. Calling this number increases the chances of the funds being frozen.
*   **Bharatiya Nyaya Sanhita, 2023 (Section 318):** This section deals with 'cheating', where obtaining property/money by deceiving someone is a criminal offense.
*   **Bharatiya Nagarik Suraksha Sanhita, 2023 (Section 173):** Under this, you can file a 'Zero FIR' at any police station, regardless of where the fraud occurred.

**What to do now:**
1. **Call 1930 immediately:** This is the first and most crucial step. Call them and provide your transaction details.
2. **Report online:** Immediately register a complaint at [www.cybercrime.gov.in](https://www.cybercrime.gov.in).
3. **Inform your bank:** Notify your bank in writing (via email or by visiting the branch) that this transaction was unauthorized.

**I need from you:**
1. Have you informed your bank yet?
2. Do you have a screenshot or SMS of the transaction?

_Escalation:_ {"level": "recommended", "reasons": ["Cyber fraud cases often require follow-up with banks and police; if the amount is not recovered quickly, legal assistance may be needed."]}  _Citations:_ ['FACT-CYBER-1930', 'BNS2023-S318', 'BNSS2023-S173']

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
   "event": "User lost 30,000 via UPI after sharing OTP with scammer"
  }
 ],
 "evidence_have": [
  "Transaction details",
  "SMS/OTP logs"
 ],
 "evidence_missing": [
  "Bank complaint acknowledgement",
  "Cyber crime portal complaint reference number"
 ],
 "next_step": "Call 1930 immediately and report the transaction."
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
