# T20_builder_delay_big
Group: edge

## Turn 1

**User:** I paid Rs 85 lakh to a builder in Gurugram for a flat in 2021, possession was promised by December 2024 and still nothing. Can I file a consumer complaint myself?

**Haq** (gemini/gemini-3.1-flash-lite, 8.12s):

Yes, you can absolutely file a consumer complaint yourself without a lawyer. In fact, the Consumer Protection Act is designed specifically so that you can represent your own case before the Commission. Since you paid Rs 85 lakh, your case falls under the jurisdiction of the State Consumer Disputes Redressal Commission. 

**My view:** Your case is strong because the builder has failed to deliver possession by the promised date, which is a clear 'deficiency in service'. The law is on your side here; you are entitled to either possession with delay interest or a full refund with interest and compensation. The most important thing is to gather all your documents—the Builder-Buyer Agreement, payment receipts, and any emails or letters where they promised the December 2024 date.

**Law on your side:**
*   **Deficiency in Service:** Under the Consumer Protection Act, 2019, failure to deliver possession on time is a 'deficiency in service'. You can claim a refund of your money with interest or possession along with compensation for the delay.
*   **Right to File:** You do not need a lawyer to file this. You can file the complaint yourself on the e-Jagriti portal.

**What they will say, and your answer:**
*   **They will say:** 'There were unavoidable delays like force majeure (e.g., COVID, labor issues) or regulatory approvals.'
*   **Your answer:** 'The agreement had a fixed date. Unless there was a specific clause for extension due to force majeure that they communicated to you in writing at the time, they are liable for the delay.'

**What I would do:**
1.  **Today:** Gather your Builder-Buyer Agreement, all payment receipts (bank statements), and any communication (emails/letters) regarding the possession date.
2.  **Next Step:** Draft a formal legal notice to the builder demanding possession or a refund with interest. This creates pressure and serves as evidence that you tried to resolve it before approaching the Commission.
3.  **Filing:** If they don't respond satisfactorily within 15 days, file your complaint on the e-Jagriti portal. The filing fee for your claim amount is Rs 2,000.

I can help you draft the legal notice to the builder. Would you like me to do that?

**Law you can cite (checked against official sources):**
- **Section 2(11), Consumer Protection Act, 2019**: A deficiency is any fault, shortcoming or inadequacy in the quality, nature or manner of a service that the law or a contract requires.
- **Section 35, Consumer Protection Act, 2019**: A complaint can be filed with the District Commission by the consumer, by a registered consumer association, by one or more consumers on behalf of many with the same interest (with the Commission's permission), or by the Central/State Government or the Central Authority.
- **Section 69, Consumer Protection Act, 2019**: You must file a consumer complaint within two years from the date the problem (cause of action) arose.

**Calculated by code:** {"deadlines": [{"label": "Last date to file a consumer complaint (2 years from when the problem arose)", "date": "2026-12-01", "days_left": 25, "status": "ok", "basis": "CPA2019-S69", "note": "The commission can accept a late complaint only if you show sufficient cause for the delay.", "user_deadline": true}], "derived": [{"label": "Where to file", "value": "State Consumer Disputes Redressal Commission", "basis": "CPJURIS2021-R3-5", "note": "Based on the amount you paid (₹85,00,000), not the amount you claim."}, {"label": "Filing fee", "value": "₹2,000", "basis": "CPCDRC2020-R7", "note": ""}]}

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['CPA2019-S2-11', 'CPA2019-S35', 'CPA2019-S39', 'CPJURIS2021-R3-5', 'CPCDRC2020-R7', 'FACT-EJAGRITI-PORTAL', 'CPA2019-S69']

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
  "Builder-Buyer Agreement"
 ],
 "evidence_missing": [
  "Emails/letters regarding possession date",
  "Any communication from the builder about delays"
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
| escalation>=recommended | ❌ | got none |
| derived:Where to file | ✅ | [{"label": "Where to file", "value": "State Consumer Disputes Redressal Commission", "basis": "CPJURIS2021-R3-5", "note": "Based on the amount you paid (\u20b98 |
| no_unverified_law_shown | ✅ |  |
