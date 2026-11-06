# T09_salary_fnf_english
Group: core

## Turn 1

**User:** My full and final settlement of Rs 1,35,000 hasn't been paid. I resigned and my last working day was 14 August 2026. I'm a marketing manager at a private company in Mumbai. HR stopped replying to emails after 1 October.

**Haq** (gemini/gemini-3.1-flash-lite, 37.51s):

Namaste. I understand how frustrating it is when your hard-earned money is stuck, especially after you have moved on from a job. Since your last working day was 14 August 2026, your full and final settlement was legally due by 17 August 2026. Because that date has passed, your employer is currently in default of their payment obligations under the Code on Wages, 2019.

**Your legal position:**
Your claim for Rs 1,35,000 is legally valid. Under the Code on Wages, 2019, you are considered an 'employee' regardless of your designation as a marketing manager, and you are entitled to receive your final dues within two working days of leaving. Since HR has stopped responding, you need to escalate this formally to create a legal record.

**Law you can cite:**
* **Section 17, Code on Wages, 2019:** Mandates that wages must be paid within two working days of resignation or termination; this is the primary rule your employer has violated.
* **Section 45, Code on Wages, 2019:** Allows you to file a wage claim before the government-appointed authority within 3 years; this is your strongest formal route if informal requests fail.

**What to do now:**
1. Send a formal 'Demand Notice' via email and registered post to the company's registered office, clearly stating the amount due and the date of your last working day.
2. If they do not respond within 15 days, file a complaint on the [SAMADHAN portal](https://samadhan.labour.gov.in).
3. For free guidance, call the NALSA helpline at 15100.

I recommend we start by drafting a formal demand notice to the company. Would you like me to help you draft that email/letter?

**Calculated by code:** {"deadlines": [{"label": "Employer had to pay your full & final wages by (2 working days after you left)", "date": "2026-08-17", "days_left": -81, "status": "passed", "basis": "COW2019-S17", "note": "This is the employer's legal deadline; if it has passed, the employer is in default. Assumes a Mon–Sat working week.", "user_deadline": false}, {"label": "Approximate last date to file a wage claim with the labour authority (3 years)", "date": "2029-08-14", "days_left": 1012, "status": "ok", "basis": "COW2019-S45", "note": "", "user_deadline": true}], "derived": []}

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['COW2019-S17', 'COW2019-S45', 'FACT-COW-NO-WAGE-CEILING']

## Final case file

```json
{
 "category": "salary",
 "language": "English",
 "script": "Latin",
 "facts": {
  "amount_due": 135000,
  "role": "marketing manager",
  "city_state": "Mumbai",
  "communications_so_far": "HR stopped replying to emails after 2026-10-01",
  "last_working_day": "2026-08-14",
  "summary": "User is seeking unpaid full and final settlement of Rs 1,35,000 after resigning from a marketing manager role in Mumbai."
 },
 "timeline": [
  {
   "date": "2026-08-14",
   "event": "Last working day"
  },
  {
   "date": "2026-08-17",
   "event": "Legal deadline for full and final settlement passed"
  },
  {
   "date": "2026-10-01",
   "event": "HR stopped responding to emails"
  }
 ],
 "evidence_have": [
  "Resignation acceptance/email",
  "Last working day proof",
  "Email trail with HR"
 ],
 "evidence_missing": [
  "Offer letter",
  "Payslips",
  "Bank statement showing last salary credit"
 ],
 "next_step": "Draft a formal demand notice to the employer."
}
```

## Automatic checks

| check | pass | detail |
|---|---|---|
| category | ✅ | got salary |
| reply_language | ✅ | expected Latin, reply script Latin |
| fact:last_working_day | ✅ | expected ~2026-08-14, got 2026-08-14 |
| mentions:manager|managerial|civil|lawyer|depends | ✅ |  |
| escalation>=none | ✅ | got none |
| no_unverified_law_shown | ✅ |  |
