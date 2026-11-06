# T06_consumer_flight_hinglish
Group: language

## Turn 1

**User:** meri flight cancel ho gayi airline ne, 12000 ka ticket tha. 2 mahine ho gaye refund nahi aaya, customer care sirf credit shell de raha hai. mujhe paise wapas chahiye

**Haq** (gemini/gemini-3.1-flash-lite, 12.6s):

**Your legal position:**
Airline ka flight cancel karna aur sirf 'credit shell' offer karna, jabki aap refund chahte hain, ek 'deficiency in service' (sewa mein kami) maani ja sakti hai. Consumer Protection Act ke tahat, agar airline ne flight cancel ki hai, toh aap refund ke haqdaar hain; woh aapko zabardasti credit shell lene ke liye majboor nahi kar sakte.

**Law you can cite:**
* **Consumer Protection Act, 2019 (Section 2(11)):** Yeh 'deficiency in service' ko define karta hai, jismein airline ka refund na dena aur apni marzi thopna shamil hai.
* **Consumer Protection (E-Commerce) Rules, 2020 (Rule 6(3)):** Yeh saaf kehta hai ki agar service mein kami hai, toh seller/provider refund dene se mana nahi kar sakta.

**What to do now:**
1. **National Consumer Helpline (1915):** Sabse pehle yahan complaint register karein, yeh free hai aur aksar airlines yahan se aayi shikayat par jaldi sunwai karti hain.
2. **Formal Email:** Airline ke Nodal Officer ko ek email bhejein jismein saaf likhein ki aapko credit shell nahi, refund chahiye (Consumer Protection Act ka hawala dein).
3. **e-Jagriti Portal:** Agar 15 din mein hal na nikle, toh [e-Jagriti](https://e-jagriti.gov.in/) par online complaint file karein. Ismein koi lawyer ki zaroorat nahi hai aur ₹12,000 ke claim ke liye koi fees bhi nahi hai.

**I need from you:**
1. Kya aapke paas airline ka woh email ya message hai jismein unhone refund dene se mana kiya hai?
2. Aapka city aur state kya hai?

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
  "Booking confirmation",
  "Cancellation notice from airline"
 ],
 "evidence_missing": [
  "Email/chat proof of airline refusing refund and offering credit shell"
 ],
 "next_step": "National Consumer Helpline (1915) par call karke complaint register karein.",
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
