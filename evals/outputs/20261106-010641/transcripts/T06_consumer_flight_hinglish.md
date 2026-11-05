# T06_consumer_flight_hinglish
Group: language

## Turn 1

**User:** meri flight cancel ho gayi airline ne, 12000 ka ticket tha. 2 mahine ho gaye refund nahi aaya, customer care sirf credit shell de raha hai. mujhe paise wapas chahiye

**Haq** (gemini/gemini-3.1-flash-lite, 10.94s):

Flight cancel hone par refund na milna pareshani ki baat hai. Aapka case 'Consumer Protection Act' ke under aata hai. Airline aapko refund dene se mana nahi kar sakti agar flight unhone cancel ki hai.

Ye rahe aapke options:
1. Airline ke Grievance Officer ko formal email likhein (agar pehle sirf customer care se baat ki hai).
2. National Consumer Helpline (1915) par call ya WhatsApp (+91 8800001915) karke complaint register karein.
3. e-Jagriti portal par online complaint file karein (₹5 lakh tak ke claims ke liye koi fee nahi hai).

Agla kadam: Kya aapke paas airline ka cancellation email aur unka 'credit shell' dene wala response hai? Agar haan, toh main aapko Grievance Officer ko bhejne ke liye ek email draft karne mein madad kar sakta hoon.

**Calculated by code:** {"deadlines": [{"label": "Last date to file a consumer complaint (2 years from when the problem arose)", "date": "2028-09-01", "days_left": 665, "status": "ok", "basis": "CPA2019-S69", "note": "The commission can accept a late complaint only if you show sufficient cause for the delay.", "user_deadline": true}], "derived": [{"label": "Where to file", "value": "District Consumer Disputes Redressal Commission", "basis": "CPJURIS2021-R3-5", "note": "Based on the amount you paid (₹12,000), not the amount you claim."}, {"label": "Filing fee", "value": "Nil", "basis": "CPCDRC2020-R7", "note": ""}]}

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['CPECOM2020-R6-3', 'FACT-NCH-HELPLINE', 'FACT-EJAGRITI-PORTAL', 'CPCDRC2020-R7']

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
   "event": "Flight cancelled (approximate)"
  }
 ],
 "evidence_have": [
  "booking details",
  "cancellation notice"
 ],
 "evidence_missing": [
  "email/chat proof of refund request",
  "airline's refusal/credit shell offer"
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
