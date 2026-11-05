# T20_builder_delay_big
Group: edge

## Turn 1

**User:** I paid Rs 85 lakh to a builder in Gurugram for a flat in 2021, possession was promised by December 2024 and still nothing. Can I file a consumer complaint myself?

**Haq** (gemini/gemini-3.1-flash-lite, 16.25s):

Yes, you can absolutely file a consumer complaint yourself. You do not need a lawyer for this. Your case falls under the 'Consumer Protection Act, 2019' because the builder has committed a deficiency in service.

Since you have paid ₹85 lakh, you will have to file a complaint with the State Consumer Disputes Redressal Commission.

**Your options:**
1. **Written Complaint:** Send a formal email/letter to the builder (if you haven't already).
2. **National Consumer Helpline (1915):** For free advice and mediation.
3. **e-Jagriti Portal:** You can file an online complaint here. The fee for this is ₹2,000.

**Next step:** Have you sent any written complaint or notice to the builder yet? And do you have the 'Allotment Letter' or 'Builder-Buyer Agreement'? These documents will be necessary.

**Calculated by code:** {"deadlines": [{"label": "Last date to file a consumer complaint (2 years from when the problem arose)", "date": "2026-12-01", "days_left": 25, "status": "ok", "basis": "CPA2019-S69", "note": "The commission can accept a late complaint only if you show sufficient cause for the delay.", "user_deadline": true}], "derived": [{"label": "Where to file", "value": "State Consumer Disputes Redressal Commission", "basis": "CPJURIS2021-R3-5", "note": "Based on the amount you paid (₹85,00,000), not the amount you claim."}, {"label": "Filing fee", "value": "₹2,000", "basis": "CPCDRC2020-R7", "note": ""}]}

_Escalation:_ {"level": "recommended", "reasons": ["Real estate disputes involving large amounts (85 lakh) can be complex; while you can file yourself, professional guidance is advisable for drafting the complaint."]}  _Citations:_ ['CPA2019-S2-11', 'CPA2019-S35', 'CPJURIS2021-R3-5', 'CPCDRC2020-R7', 'FACT-EJAGRITI-PORTAL']

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
   "event": "Flat purchase payment made"
  },
  {
   "date": "2024-12-01",
   "event": "Promised possession date missed"
  }
 ],
 "evidence_have": [],
 "evidence_missing": [
  "Builder-Buyer Agreement",
  "Allotment Letter",
  "Payment receipts",
  "Any previous communication with the builder"
 ],
 "next_step": "Ask user about existing documentation and previous communication with the builder.",
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
