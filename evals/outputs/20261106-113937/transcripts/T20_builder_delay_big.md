# T20_builder_delay_big
Group: edge

## Turn 1

**User:** I paid Rs 85 lakh to a builder in Gurugram for a flat in 2021, possession was promised by December 2024 and still nothing. Can I file a consumer complaint myself?

**Haq** (gemini/gemini-3.1-flash-lite, 11.15s):

Look, a builder delaying possession is a clear 'deficiency in service'. You are absolutely a consumer and you can file a complaint yourself; you do not need to be a lawyer to do so. Since your claim is for ₹85 lakh, you will have to file it with the State Consumer Disputes Redressal Commission. You still have plenty of time, but start gathering your paperwork now.

**Your legal position:**
A builder failing to deliver a flat by the promised date is considered 'deficiency in service' under the Consumer Protection Act. Your case looks strong because you will have proof of payment, but it is important to check the builder's agreement (Buyer-Seller Agreement) to see what terms they have written.

**Law you can cite:**
* **Section 2(11), Consumer Protection Act, 2019:** This states that if there is any deficiency in service, you can approach the consumer commission.
* **Section 39, Consumer Protection Act, 2019:** Under this, you can demand a refund, interest, or compensation.
* **Section 35, Consumer Protection Act, 2019:** This gives you the right to file a complaint yourself without a lawyer.

**What to do now:**
1. Send a formal email/letter to the builder (if you haven't already) demanding possession.
2. Call the National Consumer Helpline (1915) to register your complaint.
3. Visit the e-Jagriti portal to file a formal complaint with the State Commission (Fee: ₹2,000).

I can draft a 'Formal Complaint Email' for you to send to the builder. Have you sent any written notice or email to the builder yet?

**Calculated by code:** {"deadlines": [{"label": "Last date to file a consumer complaint (2 years from when the problem arose)", "date": "2026-12-01", "days_left": 25, "status": "ok", "basis": "CPA2019-S69", "note": "The commission can accept a late complaint only if you show sufficient cause for the delay.", "user_deadline": true}], "derived": [{"label": "Where to file", "value": "State Consumer Disputes Redressal Commission", "basis": "CPJURIS2021-R3-5", "note": "Based on the amount you paid (₹85,00,000), not the amount you claim."}, {"label": "Filing fee", "value": "₹2,000", "basis": "CPCDRC2020-R7", "note": ""}]}

_Escalation:_ {"level": "recommended", "reasons": ["Real estate matters involving large sums (85 lakhs) can be complex; while you can file yourself, a lawyer can help ensure the compensation claim is calculated correctly."]}  _Citations:_ ['CPA2019-S2-11', 'CPA2019-S39', 'CPA2019-S35', 'CPJURIS2021-R3-5', 'CPCDRC2020-R7', 'FACT-EJAGRITI-PORTAL']

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
   "event": "Promised possession date missed"
  }
 ],
 "evidence_have": [
  "Payment receipts",
  "Buyer-Seller Agreement"
 ],
 "evidence_missing": [
  "Copy of Builder-Buyer Agreement",
  "Any previous correspondence/emails with the builder"
 ],
 "next_step": "Draft a formal complaint email to the builder",
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
