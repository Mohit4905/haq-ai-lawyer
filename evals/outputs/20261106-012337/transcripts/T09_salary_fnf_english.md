# T09_salary_fnf_english
Group: core

## Turn 1

**User:** My full and final settlement of Rs 1,35,000 hasn't been paid. I resigned and my last working day was 14 August 2026. I'm a marketing manager at a private company in Mumbai. HR stopped replying to emails after 1 October.

**Haq** (gemini/gemini-3.1-flash-lite, 8.13s):

I am sorry to hear that your settlement is stuck. According to the Code on Wages, 2019, your final wages should have been paid within 2 working days after your resignation. Since HR has stopped responding, you now need to proceed formally.

Options:
1. Send a final 'Demand Notice' to the HR/Company (via email and registered post).
2. File a complaint on the SAMADHAN portal (samadhan.labour.gov.in).
3. Contact the 'Inspector-cum-Facilitator' at the Labour office.

Next step: I can prepare a draft of a 'Demand Notice' for you, which you can send to the company. Do you have your 'Resignation Acceptance' letter or the 'Full and Final' settlement calculation email?

⚠️ **Deadline check (calculated by Haq, not AI):** Full & final wages were due by (2 working days after leaving): **17 Aug 2026**, which has passed. Please speak to a lawyer or free legal aid (15100) soon to check what options remain.

**Calculated by code:** {"deadlines": [{"label": "Full & final wages were due by (2 working days after leaving)", "date": "2026-08-17", "days_left": -81, "status": "passed", "basis": "COW2019-S17", "note": "Assumes a Mon–Sat working week.", "user_deadline": true}, {"label": "Approximate last date to file a wage claim with the labour authority (3 years)", "date": "2029-08-14", "days_left": 1012, "status": "ok", "basis": "COW2019-S45", "note": "", "user_deadline": true}], "derived": []}

_Escalation:_ {"level": "recommended", "reasons": ["Deadline passed: Full & final wages were due by (2 working days after leaving) (2026-08-17)"]}  _Citations:_ ['COW2019-S17', 'COW2019-S45', 'FACT-SAMADHAN-PORTAL']

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
  "last_working_day": "2026-08-14"
 },
 "timeline": [
  {
   "date": "2026-08-14",
   "event": "Last working day"
  },
  {
   "date": "2026-10-01",
   "event": "HR stopped responding"
  }
 ],
 "evidence_have": [
  "Resignation details"
 ],
 "evidence_missing": [
  "Resignation acceptance letter",
  "Full and final settlement calculation email",
  "Offer letter",
  "Payslips"
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
| escalation>=none | ✅ | got recommended |
| no_unverified_law_shown | ✅ |  |
