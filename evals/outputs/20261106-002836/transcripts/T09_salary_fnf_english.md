# T09_salary_fnf_english
Group: core

## Turn 1

**User:** My full and final settlement of Rs 1,35,000 hasn't been paid. I resigned and my last working day was 14 August 2026. I'm a marketing manager at a private company in Mumbai. HR stopped replying to emails after 1 October.

**Haq** (groq/openai/gpt-oss-120b, 28.57s):

From what you’ve told me, you can first send a formal demand notice to your former employer. It should list your role, last working day (14‑Aug‑2026), amount owed (₹1,35,000) and give them 15 days to pay. Keep a copy and send it by registered post or email with read‑receipt so you have proof. If they still ignore you, you can file a wage claim with the labour authority (within 3 years) via the SAMADHAN portal. I can draft the demand notice for you.

Would you like me to draft the notice?

⚠️ **Deadline check (calculated by Haq, not AI):** Full & final wages were due by (2 working days after leaving): **17 Aug 2026**, which has passed. Please speak to a lawyer or free legal aid (15100) soon to check what options remain.

**Calculated by code:** {"deadlines": [{"label": "Full & final wages were due by (2 working days after leaving)", "date": "2026-08-17", "days_left": -81, "status": "passed", "basis": "COW2019-S17", "note": "Assumes a Mon–Sat working week.", "user_deadline": true}, {"label": "Approximate last date to file a wage claim with the labour authority (3 years)", "date": "2029-08-14", "days_left": 1012, "status": "ok", "basis": "COW2019-S45", "note": "", "user_deadline": true}], "derived": []}

_Escalation:_ {"level": "recommended", "reasons": ["Deadline passed: Full & final wages were due by (2 working days after leaving) (2026-08-17)"]}  _Citations:_ ['COW2019-S45', 'COW2019-S51', 'FACT-SAMADHAN-PORTAL']

## Final case file

```json
{
 "category": "salary",
 "language": "English",
 "script": "Latin",
 "facts": {
  "other_party_name": "private company",
  "role": "Marketing Manager",
  "unpaid_period": "2026-08-14",
  "amount_due": 135000,
  "still_employed": false,
  "communications_so_far": "HR stopped replying after 2026-10-01",
  "city_state": "Mumbai",
  "last_working_day": "2026-08-14"
 },
 "timeline": [
  {
   "date": "2026-08-14",
   "event": "Resigned, last working day"
  },
  {
   "date": "2026-10-01",
   "event": "HR stopped replying"
  }
 ],
 "evidence_have": [],
 "evidence_missing": [
  "Employment proof (offer letter, payslips, bank salary credits)",
  "Resignation email/letter",
  "Copy of any previous salary statements"
 ],
 "next_step": "Send a written demand notice (registered post/email) giving 15 days to pay"
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
