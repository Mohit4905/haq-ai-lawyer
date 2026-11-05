# T09_salary_fnf_english
Group: core

## Turn 1

**User:** My full and final settlement of Rs 1,35,000 hasn't been paid. I resigned and my last working day was 14 August 2026. I'm a marketing manager at a private company in Mumbai. HR stopped replying to emails after 1 October.

**Haq** (gemini/gemini-3.1-flash-lite, 9.96s):

Hello! I understand how stressful it is when your hard-earned money is stuck. Since you resigned, your final settlement (full and final) should have been paid within 2 working days of your last working day (14 August 2026). Since it is now well past that, here is how you can proceed:

1. **Written Request:** Send a formal email to HR and the company head, attaching your resignation acceptance and stating the exact amount due. Keep a copy.
2. **Demand Notice:** If they don't reply, send a formal legal notice (demand notice) giving them 15 days to pay.
3. **Labour Authority:** You can file a wage claim under the Code on Wages, 2019. As a manager, you are covered under this law. You can approach the local labour office or use the SAMADHAN portal.

To help you further, do you have your offer letter, resignation acceptance, and any email proof of the settlement amount? Also, are you still in touch with any colleagues who can confirm the company's status?

⚠️ **Deadline check (calculated by Haq, not AI):** Full & final wages were due by (2 working days after leaving): **17 Aug 2026**, which has passed. Please speak to a lawyer or free legal aid (15100) soon to check what options remain.

**Calculated by code:** {"deadlines": [{"label": "Full & final wages were due by (2 working days after leaving)", "date": "2026-08-17", "days_left": -81, "status": "passed", "basis": "COW2019-S17", "note": "Assumes a Mon–Sat working week.", "user_deadline": true}, {"label": "Approximate last date to file a wage claim with the labour authority (3 years)", "date": "2029-08-14", "days_left": 1012, "status": "ok", "basis": "COW2019-S45", "note": "", "user_deadline": true}], "derived": []}

_Escalation:_ {"level": "recommended", "reasons": ["Deadline passed: Full & final wages were due by (2 working days after leaving) (2026-08-17)"]}  _Citations:_ ['COW2019-S17', 'COW2019-S2K', 'FACT-COW-NO-WAGE-CEILING', 'COW2019-S45', 'FACT-SAMADHAN-PORTAL']

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
 "evidence_have": [],
 "evidence_missing": [
  "Offer letter",
  "Resignation acceptance",
  "Email proof of settlement amount"
 ],
 "next_step": "Draft a formal email to HR requesting the settlement"
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
