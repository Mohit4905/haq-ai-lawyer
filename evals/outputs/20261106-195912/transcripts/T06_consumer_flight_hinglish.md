# T06_consumer_flight_hinglish
Group: language

## Turn 1

**User:** meri flight cancel ho gayi airline ne, 12000 ka ticket tha. 2 mahine ho gaye refund nahi aaya, customer care sirf credit shell de raha hai. mujhe paise wapas chahiye

**Haq** (gemini/gemini-3.1-flash-lite, 6.4s):

**My view:** Airline ka flight cancel karna aur refund ke badle sirf 'credit shell' dena ek unfair trade practice hai. Aapka case strong hai kyunki service provider ne service nahi di, toh woh aapko paisa wapas dene se mana nahi kar sakte. Credit shell lena aapki marzi honi chahiye, airline ki zabardasti nahi. Aapko seedha refund ke liye pressure banana hoga.

**Law on your side:**
*   Consumer Protection (E-Commerce) Rules, 2020 ke mutabik, agar service defective ya deficient hai (jaise flight cancel hona), toh seller refund dene se mana nahi kar sakta.
*   Consumer Protection Act, 2019 ke tehat, aap refund ke saath-saath pareshani ke liye compensation bhi maang sakte hain.

**What they will say, and your answer:**
*   *Woh kahenge:* "Hamari policy sirf credit shell dene ki hai."
*   *Aapka jawab:* "Policy law se upar nahi hai. Consumer Protection Act ke under mujhe refund ka poora haq hai, aur main credit shell lene ke liye bound nahi hoon."

**What I would do:**
1.  **Aaj:** Airline ke Grievance Officer ko ek formal email likhiye (unki website par 'Grievance Officer' ka email mil jayega). Usme saaf likhiye ki aapko credit shell nahi, 12,000 ka refund chahiye aur agar 7 din mein nahi mila toh aap National Consumer Helpline (1915) aur e-Jagriti portal par complaint karenge.
2.  **Agar 7 din mein jawab na aaye:** 1915 par call karke ya consumerhelpline.gov.in par apni complaint register kariye.

**I need from you:**
1. Kya aapke paas airline ka cancellation email ya message hai?
2. Kya aapne abhi tak kisi grievance officer ko email kiya hai?

**Aap yeh kanoon cite kar sakte hain (official source se verified):**
- **Section 2(11), Consumer Protection Act, 2019**: A deficiency is any fault, shortcoming or inadequacy in the quality, nature or manner of a service that the law or a contract requires.
- **Section 35, Consumer Protection Act, 2019**: A complaint can be filed with the District Commission by the consumer, by a registered consumer association, by one or more consumers on behalf of many with the same interest (with the Commission's permission), or by the Central/State Government or the Central Authority.
- **Section 69, Consumer Protection Act, 2019**: You must file a consumer complaint within two years from the date the problem (cause of action) arose.

**Calculated by code:** {"deadlines": [{"label": "Last date to file a consumer complaint (2 years from when the problem arose)", "date": "2028-09-06", "days_left": 670, "status": "ok", "basis": "CPA2019-S69", "note": "The commission can accept a late complaint only if you show sufficient cause for the delay.", "user_deadline": true}], "derived": [{"label": "Where to file", "value": "District Consumer Disputes Redressal Commission", "basis": "CPJURIS2021-R3-5", "note": "Based on the amount you paid (₹12,000), not the amount you claim."}, {"label": "Filing fee", "value": "Nil", "basis": "CPCDRC2020-R7", "note": ""}]}

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['CPECOM2020-R6-3', 'CPA2019-S39', 'FACT-NCH-HELPLINE', 'CPA2019-S2-11', 'CPA2019-S35', 'CPA2019-S69']

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
  "Cancellation notification"
 ],
 "evidence_missing": [
  "Email correspondence with customer care",
  "Proof of payment (bank statement/transaction ID)"
 ],
 "next_step": "Draft a formal email to the airline's Grievance Officer demanding a refund.",
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
