# T09_salary_fnf_english
Group: core

## Turn 1

**User:** My full and final settlement of Rs 1,35,000 hasn't been paid. I resigned and my last working day was 14 August 2026. I'm a marketing manager at a private company in Mumbai. HR stopped replying to emails after 1 October.

**Haq** (groq/qwen/qwen3.8-27b, 7.93s):

I'm sorry you're dealing with this. Here's where you stand:

**The deadline has passed.** Under the Code on Wages, 2019, final wages after resignation are due within **2 working days** of your last working day. Yours was 14 Aug 2026, so the money was due by around 16–17 Aug. It's well past that now.

**Your options (cheapest → most formal):**

1. **Written request to HR** – you've already done this; they went silent after 1 Oct.
2. **Demand notice to the company** (~15 days to respond) – a formal letter stating the amount, the legal deadline, and a clear last date. This is your best next move.
3. **Wage claim before the labour authority** under the Code on Wages (file within 3 years; the authority can award up to 10× the amount as compensation).
4. **Civil suit** (3-year limit) – a lawyer would help here; usually for items that don't count as 'wages'.

**My recommendation:** Send a demand notice now. I can draft it for you.

Two quick questions:
- What is your **monthly salary** (so I can check the F&F figure looks right)?
- Do you have **proof of employment** – offer letter, payslips, or bank credit screenshots?

⚠️ **Deadline check (calculated by Haq, not AI):** Full & final wages were due by (2 working days after leaving): **17 Aug 2026**, which has passed. Please speak to a lawyer or free legal aid (15100) soon to check what options remain.

**Calculated by code:** {"deadlines": [{"label": "Full & final wages were due by (2 working days after leaving)", "date": "2026-08-17", "days_left": -81, "status": "passed", "basis": "COW2019-S17", "note": "Assumes a Mon–Sat working week.", "user_deadline": true}, {"label": "Approximate last date to file a wage claim with the labour authority (3 years)", "date": "2029-08-14", "days_left": 1012, "status": "ok", "basis": "COW2019-S45", "note": "", "user_deadline": true}], "derived": []}

_Escalation:_ {"level": "recommended", "reasons": ["Deadline passed: Full & final wages were due by (2 working days after leaving) (2026-08-17)"]}  _Citations:_ ['COW2019-S17', 'COW2019-S45', 'COW2019-S2K', 'FACT-COW-NO-WAGE-CEILING', 'LIM1963-ART7']

## Final case file

```json
{
 "category": "salary",
 "language": "English",
 "script": "Latin",
 "facts": {
  "other_party_name": "private company",
  "role": "Marketing Manager",
  "amount_due": 135000,
  "unpaid_period": "2026-08-14 to present",
  "communications_so_far": "HR stopped replying after 2026-10-01",
  "city_state": "Mumbai",
  "last_working_day": "2026-08-14",
  "still_employed": false
 },
 "timeline": [
  {
   "date": "2026-08-14",
   "event": "Last working day; resigned"
  },
  {
   "date": "2026-10-01",
   "event": "HR last replied; went silent after this"
  }
 ],
 "evidence_have": [],
 "evidence_missing": [
  "Offer letter or appointment letter",
  "Payslips (last 3-6 months)",
  "Bank credit statements showing salary deposits",
  "Written resignation email/letter and any acknowledgement",
  "Any email or document stating the F&F amount of ₹1,35,000"
 ],
 "next_step": "Draft and send a demand notice to the company for ₹1,35,000 with a 15-day deadline"
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
