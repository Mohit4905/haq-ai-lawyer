# T20_builder_delay_big
Group: edge

## Turn 1

**User:** I paid Rs 85 lakh to a builder in Gurugram for a flat in 2021, possession was promised by December 2024 and still nothing. Can I file a consumer complaint myself?

**Haq** (gemini/gemini-3.1-flash-lite, 36.85s):

Yes, absolutely, you can file a consumer complaint yourself. You do not need a lawyer, but since your case involves 85 lakh, it will go to the State Consumer Commission, which can be a bit technical.

**My view:** The builder's failure to provide possession is a clear 'deficiency of service'. Your case is strong because you will have proof of payment and the builder had promised possession. You should start gathering all documents (allotment letter, payment receipts, builder-buyer agreement) right away.

**Law on your side:**
* Under the Consumer Protection Act, 2019, if there is a deficiency in service, you can claim a refund or possession along with interest and compensation.
* You can file a complaint on the e-Jagriti portal even without a lawyer.

**What they will say, and your answer:**
* The builder will say that the 'delay is due to force majeure (unavoidable circumstances)'. Your answer will be that the builder must provide justification for the delay beyond the date written in the agreement, and mere claims will not suffice.

**What I would do:**
1. First of all, send a formal email/letter to the builder (if you haven't already) asking for the possession status.
2. Keep all documents scanned and ready.
3. When you are ready, file a complaint on the e-Jagriti portal.

**I need from you:**
1. Do you have the 'Builder-Buyer Agreement' which mentions the possession date?
2. Have you sent any written complaint or email to the builder yet?

**Law you can cite (checked against official sources):**
- **Section 2(11), Consumer Protection Act, 2019**: A deficiency is any fault, shortcoming or inadequacy in the quality, nature or manner of a service that the law or a contract requires.
- **Section 35, Consumer Protection Act, 2019**: A complaint can be filed with the District Commission by the consumer, by a registered consumer association, by one or more consumers on behalf of many with the same interest (with the Commission's permission), or by the Central/State Government or the Central Authority.
- **Section 69, Consumer Protection Act, 2019**: You must file a consumer complaint within two years from the date the problem (cause of action) arose.

**Calculated by code:** {"deadlines": [{"label": "Last date to file a consumer complaint (2 years from when the problem arose)", "date": "2026-12-01", "days_left": 25, "status": "ok", "basis": "CPA2019-S69", "note": "The commission can accept a late complaint only if you show sufficient cause for the delay.", "user_deadline": true}], "derived": [{"label": "Where to file", "value": "State Consumer Disputes Redressal Commission", "basis": "CPJURIS2021-R3-5", "note": "Based on the amount you paid (₹85,00,000), not the amount you claim."}, {"label": "Filing fee", "value": "₹2,000", "basis": "CPCDRC2020-R7", "note": ""}]}

_Escalation:_ {"level": "recommended", "reasons": ["Since the claim is in the State Commission (above 50 lakhs), the procedure is more formal than the District Commission. While you can file yourself, having a lawyer review your complaint draft is advisable."]}  _Citations:_ ['CPA2019-S2-7', 'CPA2019-S2-11', 'CPA2019-S39', 'CPJURIS2021-R3-5', 'FACT-EJAGRITI-PORTAL', 'CPA2019-S35', 'CPA2019-S69']

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
   "event": "Payment made for flat"
  },
  {
   "date": "2024-12-01",
   "event": "Promised possession date passed"
  }
 ],
 "evidence_have": [
  "Payment receipts"
 ],
 "evidence_missing": [
  "Builder-Buyer Agreement",
  "Allotment letter",
  "Copies of any previous communication with the builder"
 ],
 "next_step": "Gather all documents including the Builder-Buyer Agreement and payment receipts.",
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
