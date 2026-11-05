# T20_builder_delay_big
Group: edge

## Turn 1

**User:** I paid Rs 85 lakh to a builder in Gurugram for a flat in 2021, possession was promised by December 2024 and still nothing. Can I file a consumer complaint myself?

**Haq** (gemini/gemini-3.1-flash-lite, 37.91s):

Yes, you can file a consumer complaint yourself without a lawyer. Since you paid ₹85 lakh, your case falls under the jurisdiction of the State Consumer Disputes Redressal Commission. 

From what you have shared, the builder's failure to deliver possession by the promised date is a 'deficiency in service'. 

Here are your options:
1. **Written complaint to the builder:** Send a formal letter/email demanding possession or a refund with interest.
2. **National Consumer Helpline:** Call 1915 or visit consumerhelpline.gov.in for free guidance.
3. **State Consumer Commission:** File a formal complaint on the e-Jagriti portal (e-jagriti.gov.in). The filing fee for your claim amount is ₹2,000.

To help me guide you better:
- Have you already sent any written complaints or legal notices to the builder?
- Do you have the Builder-Buyer Agreement and payment receipts ready?

Because this involves a large amount and real estate laws can be complex, I recommend consulting a lawyer or using free legal aid (15100) to review your agreement before filing.

**Calculated by code:** {"deadlines": [{"label": "Last date to file a consumer complaint (2 years from when the problem arose)", "date": "2026-12-01", "days_left": 25, "status": "ok", "basis": "CPA2019-S69", "note": "The commission can accept a late complaint only if you show sufficient cause for the delay.", "user_deadline": true}], "derived": [{"label": "Where to file", "value": "State Consumer Disputes Redressal Commission", "basis": "CPJURIS2021-R3-5", "note": "Based on the amount you paid (₹85,00,000), not the amount you claim."}, {"label": "Filing fee", "value": "₹2,000", "basis": "CPCDRC2020-R7", "note": ""}]}

_Escalation:_ {"level": "recommended", "reasons": ["Real estate disputes involving high amounts are complex; a lawyer can ensure your agreement is interpreted correctly."]}  _Citations:_ ['CPA2019-S2-11', 'CPA2019-S35', 'CPA2019-S39', 'CPJURIS2021-R3-5', 'CPCDRC2020-R7', 'FACT-NCH-HELPLINE', 'FACT-EJAGRITI-PORTAL', 'FACT-NALSA-HELPLINE']

## Final case file

```json
{
 "category": "consumer",
 "language": "English",
 "script": "Latin",
 "facts": {
  "product_or_service": "flat",
  "amount_paid": 8500000,
  "purchase_date": "2021-01-01",
  "problem_date": "2024-12-01",
  "city_state": "Gurugram",
  "summary": "Builder failed to provide possession of flat by promised date of December 2024."
 },
 "timeline": [
  {
   "date": "2021-01-01",
   "event": "Paid for flat"
  },
  {
   "date": "2024-12-01",
   "event": "Promised possession date missed"
  }
 ],
 "evidence_have": [],
 "evidence_missing": [
  "Builder-Buyer Agreement",
  "Payment receipts",
  "Any previous correspondence with the builder"
 ],
 "next_step": "Gather your Builder-Buyer Agreement and payment receipts, then consider sending a formal written complaint to the builder.",
 "approximate": [
  "problem_date",
  "purchase_date"
 ]
}
```

## Automatic checks

| check | pass | detail |
|---|---|---|
| category | ✅ | got consumer |
| escalation>=recommended | ✅ | got recommended |
| derived:Where to file | ✅ | [{"label": "Where to file", "value": "State Consumer Disputes Redressal Commission", "basis": "CPJURIS2021-R3-5", "note": "Based on the amount you paid (\u20b98 |
| no_unverified_law_shown | ✅ |  |
