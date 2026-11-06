# T06_consumer_flight_hinglish
Group: language

## Turn 1

**User:** meri flight cancel ho gayi airline ne, 12000 ka ticket tha. 2 mahine ho gaye refund nahi aaya, customer care sirf credit shell de raha hai. mujhe paise wapas chahiye

**Haq** (gemini/gemini-3.1-flash-lite, 15.2s):

**Your legal position:**
Airline ka flight cancel karna aur sirf 'credit shell' offer karna, jabki aap refund chahte hain, ek 'deficiency in service' (sewa mein kami) maana ja sakta hai. Consumer Protection Act ke tahat, agar airline ne flight cancel ki hai, toh aap refund ke haqdaar hain; woh aapko zabardasti credit shell lene ke liye majboor nahi kar sakte.

**Law you can cite:**
* **Consumer Protection Act, 2019 (Section 2(11)):** Yeh kehta hai ki service mein koi bhi kami (deficiency) jisse aapko nuksan ho, woh consumer complaint ka aadhar hai.
* **Consumer Protection (E-Commerce) Rules, 2020 (Rule 6(3)):** Yeh rules saaf kehte hain ki agar service mein kami hai, toh seller/provider refund dene se mana nahi kar sakta.

**What to do now:**
1. **National Consumer Helpline (1915):** Sabse pehle yahan complaint register karein, yeh free hai aur aksar airlines yahan se aayi shikayat par jaldi sunwai karti hain.
2. **Formal Grievance Email:** Airline ke Nodal Officer ko ek email likhein jismein saaf likha ho ki aapko refund chahiye, credit shell nahi. Ismein apna PNR aur booking details zaroor dein.
3. **e-Jagriti Portal:** Agar 15-20 din mein koi jawab na aaye, toh aap e-Jagriti portal par District Consumer Commission mein case file kar sakte hain. Ismein koi lawyer ki zaroorat nahi hai aur ₹5 lakh tak ke claim par koi fees nahi hai.

**I need from you:**
1. Kya aapke paas airline ka woh email ya chat ka screenshot hai jismein unhone refund dene se mana kiya hai?
2. Aapka PNR number ya booking ID kya hai (sirf record ke liye)?

**Calculated by code:** {"deadlines": [{"label": "Last date to file a consumer complaint (2 years from when the problem arose)", "date": "2028-09-06", "days_left": 670, "status": "ok", "basis": "CPA2019-S69", "note": "The commission can accept a late complaint only if you show sufficient cause for the delay.", "user_deadline": true}], "derived": [{"label": "Where to file", "value": "District Consumer Disputes Redressal Commission", "basis": "CPJURIS2021-R3-5", "note": "Based on the amount you paid (₹12,000), not the amount you claim."}, {"label": "Filing fee", "value": "Nil", "basis": "CPCDRC2020-R7", "note": ""}]}

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['CPA2019-S2-11', 'CPECOM2020-R6-3', 'FACT-NCH-HELPLINE', 'FACT-EJAGRITI-PORTAL']

## Final case file

```json
{
 "category": "consumer",
 "language": "Hinglish",
 "script": "Latin",
 "facts": {
  "product_or_service": "Flight ticket",
  "amount_paid": 12000,
  "problem_date": "2026-09-06",
  "complained_to_company": true,
  "summary": "Airline cancelled flight and is offering credit shell instead of refund of 12000 rupees."
 },
 "timeline": [
  {
   "date": "2026-09-06",
   "event": "Flight cancelled by airline"
  }
 ],
 "evidence_have": [
  "Booking details",
  "Communication with customer care"
 ],
 "evidence_missing": [
  "Screenshots of credit shell offer",
  "Cancellation email from airline"
 ],
 "next_step": "Call 1915 or file a complaint on the National Consumer Helpline website.",
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
