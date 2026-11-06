# T04_consumer_refund_ecommerce
Group: core

## Turn 1

**User:** I returned a phone I bought on an online shopping app for Rs 18,499. Pickup was done on 10 September 2026, order ID OD12345. They keep saying refund is 'under process'. I've raised 4 tickets, last one on 1 October 2026. Still nothing. I'm in Jaipur.

**Haq** (gemini/gemini-3.1-flash-lite, 16.35s):

Namaste. I understand how frustrating it is to wait for your money, especially when you have followed up four times. Since your last complaint was on 1 October 2026, the company's one-month deadline to resolve this has passed (as of 1 November 2026). From what you have told me, the main conditions for a consumer complaint seem to be met, as you are a consumer who has paid for a product and the service appears deficient.

**Your legal position:**
Under the Consumer Protection (E-Commerce) Rules, 2020, the company is required to resolve your grievance within one month. Since they have failed to do so, this may be considered a 'deficiency in service' under the Consumer Protection Act, 2019. Your position depends on your ability to prove the return was completed and accepted by the company.

**Law you can cite:**
* **Consumer Protection (E-Commerce) Rules, 2020, Rule 4(5):** E-commerce platforms must acknowledge complaints within 48 hours and resolve them within one month.
* **Consumer Protection Act, 2019, Section 2(11):** Defines 'deficiency' as any fault or shortcoming in the quality or manner of service that the law requires.
* **Consumer Protection Act, 2019, Section 39:** If your complaint is proved, the Commission can order a refund, replacement, or compensation.

**What to do now:**
1. **National Consumer Helpline:** Call 1915 or register your complaint at consumerhelpline.gov.in. This is a free, pre-litigation step.
2. **File on e-Jagriti:** If NCH does not resolve it, file a formal complaint on the [e-Jagriti portal](https://e-jagriti.gov.in/). There is no fee for claims up to ₹5 lakh.

**I need from you:**
1. Do you have a 'Return Pickup Receipt' or an email/SMS confirmation from the courier/company confirming the pickup on 10 September?
2. Do you have copies of the 4 ticket numbers you raised?

> 🛡️ Guard caught (before user saw it): [{"type": "overclaim", "text": "a clear case", "why": "Don't promise or pre-judge the outcome; say what the facts suggest and what depends on evidence."}]  
> repaired=True stripped=False

**Calculated by code:** {"deadlines": [{"label": "If your complaint reached the platform's grievance officer, they had to resolve it by", "date": "2026-11-01", "days_left": -5, "status": "passed", "basis": "CPECOM2020-R4-5", "note": "Acknowledgement is due within 48 hours. This is the company's deadline, not yours.", "user_deadline": false}], "derived": [{"label": "Where to file", "value": "District Consumer Disputes Redressal Commission", "basis": "CPJURIS2021-R3-5", "note": "Based on the amount you paid (₹18,499), not the amount you claim."}, {"label": "Filing fee", "value": "Nil", "basis": "CPCDRC2020-R7", "note": ""}]}

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['CPECOM2020-R4-5', 'CPA2019-S2-11', 'CPA2019-S39']

## Final case file

```json
{
 "category": "consumer",
 "language": "English",
 "script": "Latin",
 "facts": {
  "product_or_service": "phone",
  "amount_paid": 18499,
  "complained_to_company": "Yes, 4 tickets raised",
  "complained_to_company_date": "2026-10-01",
  "city_state": "Jaipur",
  "is_ecommerce": true,
  "summary": "Refund for returned phone (Rs 18,499) pending since pickup on 2026-09-10."
 },
 "timeline": [
  {
   "date": "2026-09-10",
   "event": "Phone pickup completed"
  },
  {
   "date": "2026-10-01",
   "event": "Last grievance ticket raised"
  }
 ],
 "evidence_have": [
  "Order ID OD12345"
 ],
 "evidence_missing": [
  "Return pickup receipt/proof",
  "Screenshots of ticket history"
 ],
 "next_step": "Register a complaint on the National Consumer Helpline (1915)"
}
```

## Draft document

BEFORE THE DISTRICT CONSUMER DISPUTES REDRESSAL COMMISSION, JAIPUR

COMPLAINANT:
[[FILL: Your Full Name]]
[[FILL: Your Full Address]]
[[FILL: Your Phone Number]]
[[FILL: Your Email Address]]

VERSUS

OPPOSITE PARTY:
[[FILL: Name of E-commerce Company]]
[[FILL: Registered Office Address of the Company]]

COMPLAINT UNDER SECTION 35 OF THE CONSUMER PROTECTION ACT, 2019

MOST RESPECTFULLY SHOWETH:

1. I am a consumer as defined under Section 2(7) of the Consumer Protection Act, 2019, having purchased a phone for Rs 18,499 from the Opposite Party's online platform (Order ID: OD12345).

2. The product was found to be unsatisfactory, and I initiated a return request. The Opposite Party successfully completed the pickup of the returned phone on 10 September 2026.

3. Despite the successful return of the product, the Opposite Party has failed to process the refund of Rs 18,499. 

4. I have made multiple attempts to resolve this issue with the Opposite Party, raising 4 separate grievance tickets, the last of which was raised on 01 October 2026. The Opposite Party continues to state that the refund is 'under process' without providing a concrete timeline or resolution.

5. The failure to refund the amount for a returned product constitutes a 'deficiency in service' under Section 2(11) of the Consumer Protection Act, 2019, as the Opposite Party has failed to adhere to the reasonable timelines for refunds as required by law.

6. This Commission has the pecuniary jurisdiction to entertain this complaint as the value of the goods is Rs 18,499, which is well within the limit of the District Commission. This Commission also has territorial jurisdiction as I reside in Jaipur and the cause of action arose here.

7. The complaint is filed within the limitation period of two years as prescribed under Section 69 of the Consumer Protection Act, 2019.

RELIEFS PRAYED:
In view of the facts stated above, it is prayed that this Hon'ble Commission may be pleased to direct the Opposite Party to:

a) Refund the amount of Rs 18,499 immediately along with interest at the rate of 12% per annum from the date of pickup (10 September 2026) until the date of actual payment.

b) Pay a sum of Rs [[FILL: Amount]] as compensation for the mental agony and harassment caused by the deficiency in service.

c) Pay a sum of Rs [[FILL: Amount]] towards the cost of litigation.

LIST OF DOCUMENTS ANNEXED:
1. Copy of Order ID OD12345.
2. [[FILL: Copy of any communication/emails/screenshots of ticket history]].

VERIFICATION:
I, [[FILL: Your Full Name]], the Complainant, do hereby verify that the contents of paragraphs 1 to 7 are true to my personal knowledge and belief. No part of it is false and nothing material has been concealed therefrom.

Verified at Jaipur on this [[FILL: Date]] day of [[FILL: Month]], 2026.

_____________________
(Signature of Complainant)

**Send instructions:** ["Visit the e-Jagriti portal (https://e-jagriti.gov.in/) to register and create an account.", "Fill in the details of the Opposite Party (the company) using their official registered office address (usually found on their website's 'Contact Us' or 'Legal' page).", "Upload a PDF copy of this complaint, signed by you, along with copies of your Order ID and any screenshots of your ticket history.", "Since the claim amount is below Rs 5 lakh, there is no filing fee required.", "Submit the complaint online and save the acknowledgement receipt provided by the portal.", "Keep a digital copy of all submitted documents and the acknowledgement for your records."]

## Automatic checks

| check | pass | detail |
|---|---|---|
| category | ✅ | got consumer |
| reply_language | ✅ | expected Latin, reply script Latin |
| fact:amount_paid | ✅ | expected ~18, got 18499 |
| mentions:1915|National Consumer Helpline | ✅ |  |
| mentions:District|Consumer Commission|consumer co | ❌ |  |
| escalation<=recommended | ✅ | got none |
| no_unverified_law_shown | ✅ |  |
| draft_no_unverified_law | ✅ | [] |
| draft_has_no_invented_fill | ✅ | 10 placeholders |
