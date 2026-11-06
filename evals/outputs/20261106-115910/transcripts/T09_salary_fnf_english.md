# T09_salary_fnf_english
Group: core

## Turn 1

**User:** My full and final settlement of Rs 1,35,000 hasn't been paid. I resigned and my last working day was 14 August 2026. I'm a marketing manager at a private company in Mumbai. HR stopped replying to emails after 1 October.

**Haq** (gemini/gemini-3.1-flash-lite, 15.65s):

Namaste. I understand how frustrating it is when your hard-earned money is stuck, especially after you have moved on from the company. Since your last working day was 14 August 2026, your full and final settlement was legally due by 17 August 2026. Because that date has passed, the company is currently in default.

**Your legal position:**
Under the Code on Wages, 2019, you are considered an 'employee' regardless of your designation as a manager. The law is clear that final wages must be paid within two working days of your last day. Since HR has stopped responding, you have a solid basis to escalate this formally.

**Law you can cite:**
* **Section 17, Code on Wages, 2019:** Mandates that final wages must be paid within two working days of resignation or termination.
* **Section 45, Code on Wages, 2019:** Allows you to file a wage claim with the government-appointed authority within 3 years to recover unpaid dues.

**What to do now:**
1. Send a formal 'Demand Notice' via email and registered post to the company's registered office, giving them 15 days to pay.
2. If they still don't respond, file a claim through the SAMADHAN portal (samadhan.labour.gov.in).
3. For free guidance, call the NALSA helpline at 15100.

I recommend we start by drafting a formal demand notice to the company. Do you have your offer letter and resignation acceptance email handy? Also, what is the exact name of the company?

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
   "event": "Legal deadline for full and final settlement"
  },
  {
   "date": "2026-10-01",
   "event": "HR stopped responding to emails"
  }
 ],
 "evidence_have": [
  "Resignation email",
  "Emails to HR"
 ],
 "evidence_missing": [
  "Offer letter",
  "Resignation acceptance",
  "Payslips",
  "Company registered address"
 ],
 "next_step": "Draft a formal demand notice to the employer"
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
