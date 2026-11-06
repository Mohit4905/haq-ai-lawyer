# T20_builder_delay_big
Group: edge

## Turn 1

**User:** I paid Rs 85 lakh to a builder in Gurugram for a flat in 2021, possession was promised by December 2024 and still nothing. Can I file a consumer complaint myself?

**Haq** (gemini/gemini-3.1-flash-lite, 11.1s):

Look, a builder failing to provide possession is a clear 'deficiency of service'. You can absolutely file a consumer complaint; you do not need a lawyer for this. Since you have paid 85 lakh, your case will go to the 'State Consumer Disputes Redressal Commission'. Your case seems strong because the builder made a promise and there is now a delay, but you must have the agreement made with the builder (Buyer-Seller Agreement) and payment receipts.

**Your legal position:**
Under the Consumer Protection Act, a builder failing to provide possession on time is a major fault. You can demand a refund or possession along with interest and compensation.

**Laws you can quote:**
*   **Section 2(11), Consumer Protection Act, 2019:** This states that you can file a complaint for any deficiency in service.
*   **Section 39, Consumer Protection Act, 2019:** This empowers the commission to order the builder to provide a refund, interest, or compensation.
*   **Rule 3-5, Consumer Protection (Jurisdiction) Rules, 2021:** This specifies that cases between 50 lakh and 2 crore are filed in the State Commission.

**What to do now:**
1. First, send a formal 'Legal Notice' to the builder (I can draft this for you).
2. If they do not comply, file a complaint on the 'e-Jagriti' portal (the fee is ₹2,000).
3. If needed, talk to the National Consumer Helpline at 1915.

**I need the following from you:**
1. Have you sent any written complaint or email to the builder yet?
2. Do you have a copy of the 'Buyer-Seller Agreement'?

**Calculated by code:** {"deadlines": [{"label": "Last date to file a consumer complaint (2 years from when the problem arose)", "date": "2026-12-01", "days_left": 25, "status": "ok", "basis": "CPA2019-S69", "note": "The commission can accept a late complaint only if you show sufficient cause for the delay.", "user_deadline": true}], "derived": [{"label": "Where to file", "value": "State Consumer Disputes Redressal Commission", "basis": "CPJURIS2021-R3-5", "note": "Based on the amount you paid (₹85,00,000), not the amount you claim."}, {"label": "Filing fee", "value": "₹2,000", "basis": "CPCDRC2020-R7", "note": ""}]}

_Escalation:_ {"level": "recommended", "reasons": ["Since the claim amount is high (85 lakhs) and involves a real estate developer, having a lawyer review the complaint before filing in the State Commission is safer."]}  _Citations:_ ['CPA2019-S2-11', 'CPA2019-S39', 'CPJURIS2021-R3-5', 'CPCDRC2020-R7']

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
   "event": "Flat payment made"
  },
  {
   "date": "2024-12-01",
   "event": "Promised possession date missed"
  }
 ],
 "evidence_have": [
  "Payment receipts"
 ],
 "evidence_missing": [
  "Buyer-Seller Agreement",
  "Proof of communication with builder"
 ],
 "next_step": "Draft a legal notice to the builder",
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
