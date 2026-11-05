# T06_consumer_flight_hinglish
Group: language

## Turn 1

**User:** meri flight cancel ho gayi airline ne, 12000 ka ticket tha. 2 mahine ho gaye refund nahi aaya, customer care sirf credit shell de raha hai. mujhe paise wapas chahiye

**Haq** (gemini/gemini-3.1-flash-lite, 7.08s):

Flight cancel hone par refund na milna ek 'deficiency in service' hai. Airline aapko zabardasti credit shell lene ke liye majboor nahi kar sakti agar aap refund chahte hain.

Aapke paas ye options hain:
1. Airline ke Grievance Officer ko email likhein (agar pehle nahi kiya hai).
2. National Consumer Helpline (1915) par call karein ya WhatsApp (+91 8800001915) karein.
3. e-Jagriti portal par consumer complaint file karein (₹12,000 ke liye koi fee nahi hai).

Agla kadam: Kya aapne airline ke 'Grievance Officer' ko formal email bheja hai? Agar nahi, toh main aapko uska draft likhne mein madad kar sakta hoon.

**Calculated by code:** {"deadlines": [{"label": "Last date to file a consumer complaint (2 years from when the problem arose)", "date": "2028-09-01", "days_left": 665, "status": "ok", "basis": "CPA2019-S69", "note": "The commission can accept a late complaint only if you show sufficient cause for the delay.", "user_deadline": true}], "derived": [{"label": "Where to file", "value": "District Consumer Disputes Redressal Commission", "basis": "CPJURIS2021-R3-5", "note": "Based on the amount you paid (₹12,000), not the amount you claim."}, {"label": "Filing fee", "value": "Nil", "basis": "CPCDRC2020-R7", "note": ""}]}

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['CPA2019-S2-11', 'CPECOM2020-R6-3', 'FACT-NCH-HELPLINE', 'FACT-EJAGRITI-PORTAL', 'CPCDRC2020-R7']

## Final case file

```json
{
 "category": "consumer",
 "language": "Hinglish",
 "script": "Latin",
 "facts": {
  "product_or_service": "flight ticket",
  "amount_paid": 12000,
  "problem_date": "2026-09-01",
  "complained_to_company": true,
  "summary": "Flight cancelled 2 months ago, airline offering credit shell instead of refund."
 },
 "timeline": [
  {
   "date": "2026-09-01",
   "event": "Flight cancelled, refund pending"
  }
 ],
 "evidence_have": [
  "Booking ID",
  "Cancellation email/message"
 ],
 "evidence_missing": [
  "Email correspondence with customer care",
  "Proof of payment"
 ],
 "next_step": "Draft a formal grievance email to the airline",
 "approximate": [
  "problem_date"
 ]
}
```

## Automatic checks

| check | pass | detail |
|---|---|---|
| category | ✅ | got consumer |
| reply_language | ✅ | expected Hinglish, reply script Hinglish |
| fact:amount_paid | ✅ | expected ~12, got 12000 |
| escalation<=recommended | ✅ | got none |
| no_unverified_law_shown | ✅ |  |
