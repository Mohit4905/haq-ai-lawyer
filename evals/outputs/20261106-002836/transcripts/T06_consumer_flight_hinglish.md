# T06_consumer_flight_hinglish
Group: language

## Turn 1

**User:** meri flight cancel ho gayi airline ne, 12000 ka ticket tha. 2 mahine ho gaye refund nahi aaya, customer care sirf credit shell de raha hai. mujhe paise wapas chahiye

**Haq** (groq/openai/gpt-oss-20b, 6.7s):

Hey! Let’s get the details straight so we can help you get your ₹12,000 back.

1. **Ticket purchase date** (or at least month/year)?
2. Do you have the booking confirmation, e‑mail, or screenshot of the ticket?
3. Which city/state do you live in?

Once we have that, we can see if you’re still within the 2‑year window and what the quickest route is.

In the meantime:
- Send a written complaint to the airline’s grievance officer (they must reply in 48 hrs and resolve in 1 month per e‑commerce rules).
- If no reply, file a consumer complaint on e‑Jagriti (no fee for ₹12,000).

**Calculated by code:** {"deadlines": [{"label": "Last date to file a consumer complaint (2 years from when the problem arose)", "date": "2028-09-06", "days_left": 670, "status": "ok", "basis": "CPA2019-S69", "note": "The commission can accept a late complaint only if you show sufficient cause for the delay.", "user_deadline": true}], "derived": [{"label": "Where to file", "value": "District Consumer Disputes Redressal Commission", "basis": "CPJURIS2021-R3-5", "note": "Based on the amount you paid (₹12,000), not the amount you claim."}, {"label": "Filing fee", "value": "Nil", "basis": "CPCDRC2020-R7", "note": ""}]}

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['CPECOM2020-R4-5', 'CPECOM2020-R6-3', 'CPA2019-S69', 'CPJURIS2021-R3-5', 'CPCDRC2020-R7']

## Final case file

```json
{
 "category": "consumer",
 "language": "Hinglish",
 "script": "Latin",
 "facts": {
  "product_or_service": "flight ticket",
  "other_party_name": "airline",
  "amount_paid": "12000",
  "problem_date": "2026-09-06",
  "complained_to_company": "yes"
 },
 "timeline": [],
 "evidence_have": [],
 "evidence_missing": [
  "booking confirmation / e‑mail / screenshot"
 ],
 "next_step": "Send a written complaint to the airline’s grievance officer",
 "approximate": [
  "problem_date"
 ]
}
```

## Automatic checks

| check | pass | detail |
|---|---|---|
| category | ✅ | got consumer |
| reply_language | ❌ | expected Hinglish, reply script Latin |
| fact:amount_paid | ✅ | expected ~12, got 12000 |
| escalation<=recommended | ✅ | got none |
| no_unverified_law_shown | ✅ |  |
