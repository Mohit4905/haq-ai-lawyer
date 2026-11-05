# T13_upi_fraud
Group: scope

## Turn 1

**User:** Someone called pretending to be from my bank and I shared an OTP. Rs 30,000 was debited via UPI 2 hours ago. What do I do?

**Haq** (groq/openai/gpt-oss-20b, 21.62s):

Hi! I’m Haq. Let’s sort this out.

1. When did the transfer happen? (date & time)
2. Which bank did you share the OTP with?
3. Do you have any screenshots or bank statements showing the debit?

Once I have those, I’ll give you the best next steps.

In the meantime:
- Call your bank’s official helpline right away.
- Report the fraud to the National Cyber Crime helpline 1930.
- File a police complaint (Zero FIR) at any station.

These actions are free and can help freeze the money.

I’ll help draft a complaint or practice a call if you need.

_Escalation:_ {"level": "recommended", "reasons": ["Fraud is time-critical: report to 1930 and your bank immediately"]}  _Citations:_ ['FACT-CYBER-1930', 'BNSS2023-S173']

## Final case file

```json
{
 "category": "cyber_fraud",
 "language": "English",
 "script": "Latin",
 "facts": {
  "amount_paid": 30000,
  "problem_date": "2026-11-06"
 },
 "timeline": [],
 "evidence_have": [],
 "evidence_missing": [
  "bank statement screenshot",
  "any communication with the caller"
 ],
 "next_step": "Call your bank’s helpline immediately"
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
