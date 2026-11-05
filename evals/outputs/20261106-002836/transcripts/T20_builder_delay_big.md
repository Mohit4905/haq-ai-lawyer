# T20_builder_delay_big
Group: edge

## Turn 1

**User:** I paid Rs 85 lakh to a builder in Gurugram for a flat in 2021, possession was promised by December 2024 and still nothing. Can I file a consumer complaint myself?

**Haq** (groq/qwen/qwen3.8-27b, 7.53s):

Yes — you can file a consumer complaint yourself, no lawyer needed. You file directly on **e-Jagriti** (e-jagriti.gov.in).

**⚠️ Deadline is close:** your last date to file is **1 December 2026** — about **25 days from now**. If you miss it, the Commission can still accept a late complaint only if you show a good reason for the delay. So don't sit on this.

**Where & how much:**
- Haryana **State** Consumer Commission (your payment is above ₹50 lakh)
- Filing fee: **₹2,000**

**Before you file, two quick questions:**
1. Have you sent any written complaint or email to the builder about the delay? If yes, when, and what did they reply?
2. What proof do you have — sale agreement, payment receipts, any letters or WhatsApp messages from the builder about the promised date?

**Suggested order (cheapest first):**
- Written complaint to builder → NCH 1915 (free) → e-Jagriti filing

Given the amount (₹85 lakh) and the tight deadline, I'd recommend at least a quick call to **NALSA 15100** (free) to confirm your strategy before filing. Want me to draft the written complaint to the builder, or the e-Jagriti complaint?

**Calculated by code:** {"deadlines": [{"label": "Last date to file a consumer complaint (2 years from when the problem arose)", "date": "2026-12-01", "days_left": 25, "status": "ok", "basis": "CPA2019-S69", "note": "The commission can accept a late complaint only if you show sufficient cause for the delay.", "user_deadline": true}], "derived": [{"label": "Where to file", "value": "State Consumer Disputes Redressal Commission", "basis": "CPJURIS2021-R3-5", "note": "Based on the amount you paid (₹85,00,000), not the amount you claim."}, {"label": "Filing fee", "value": "₹2,000", "basis": "CPCDRC2020-R7", "note": ""}]}

_Escalation:_ {"level": "recommended", "reasons": ["Large amount (₹85 lakh), deadline within 25 days, and construction-delay cases can involve complex facts (RERA, specific performance vs refund). A quick free consult via NALSA 15100 is wise before filing."]}  _Citations:_ ['CPA2019-S35', 'CPA2019-S69', 'CPJURIS2021-R3-5', 'CPCDRC2020-R7', 'FACT-EJAGRITI-PORTAL', 'FACT-NCH-HELPLINE', 'FACT-NALSA-HELPLINE']

## Final case file

```json
{
 "category": "consumer",
 "language": "English",
 "script": "Latin",
 "facts": {
  "product_or_service": "flat construction",
  "other_party_name": "builder",
  "amount_paid": 8500000,
  "purchase_date": "2021-01-01",
  "problem_date": "2024-12-01",
  "city_state": "Gurugram, Haryana",
  "summary": "Paid Rs 85 lakh to builder in 2021 for a flat, possession promised by Dec 2024 but not delivered."
 },
 "timeline": [
  {
   "date": "2021-01-01",
   "event": "Paid ₹85 lakh to builder for flat (approximate)"
  },
  {
   "date": "2024-12-01",
   "event": "Promised possession date passed without delivery (approximate)"
  }
 ],
 "evidence_have": [],
 "evidence_missing": [
  "Sale/booking agreement with builder",
  "Payment receipts or bank transfer records",
  "Any written communication (letters, emails, WhatsApp) from builder about the promised date or delay",
  "Any prior complaint sent to builder and their reply"
 ],
 "next_step": "Send a written complaint to the builder (email + registered post) demanding possession or refund, with a 15-day deadline; keep proof of sending.",
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
