# T04_consumer_refund_ecommerce
Group: core

## Turn 1

**User:** I returned a phone I bought on an online shopping app for Rs 18,499. Pickup was done on 10 September 2026, order ID OD12345. They keep saying refund is 'under process'. I've raised 4 tickets, last one on 1 October 2026. Still nothing. I'm in Jaipur.

**Haq** (gemini/gemini-3.1-flash-lite, 6.66s):

Hello! It is frustrating when a refund gets stuck like this. Since you have already raised 4 tickets and the company has not resolved it, you have a clear path forward. 

From what you have told me, the company is failing to meet its obligation to process your refund after a return, which is a deficiency in service. Since you have already tried the company's grievance process, here are your next options:

1. **National Consumer Helpline (1915):** A free, quick way to escalate this. They act as a mediator.
2. **e-Jagriti Portal:** You can file a formal complaint online. Since the amount is under ₹5 lakh, there is no filing fee.

**Recommended Next Step:** I suggest you first call the National Consumer Helpline (1915) or file a complaint on their website. If that does not work within a few weeks, we can draft a formal complaint for the District Consumer Commission.

Do you have the return pickup receipt or any email confirmation of the return?

**Calculated by code:** {"deadlines": [{"label": "If your complaint reached the platform's grievance officer, they had to resolve it by", "date": "2026-11-01", "days_left": -5, "status": "passed", "basis": "CPECOM2020-R4-5", "note": "Acknowledgement is due within 48 hours. This is the company's deadline, not yours.", "user_deadline": false}], "derived": [{"label": "Where to file", "value": "District Consumer Disputes Redressal Commission", "basis": "CPJURIS2021-R3-5", "note": "Based on the amount you paid (₹18,499), not the amount you claim."}, {"label": "Filing fee", "value": "Nil", "basis": "CPCDRC2020-R7", "note": ""}]}

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['CPECOM2020-R4-5', 'CPECOM2020-R6-3', 'FACT-NCH-HELPLINE', 'FACT-EJAGRITI-PORTAL', 'CPCDRC2020-R7']

## Final case file

```json
{
 "category": "consumer",
 "language": "English",
 "script": "Latin",
 "facts": {
  "product_or_service": "Phone",
  "amount_paid": 18499,
  "complained_to_company": "Yes",
  "complained_to_company_date": "2026-10-01",
  "city_state": "Jaipur",
  "is_ecommerce": true,
  "summary": "Refund pending for returned phone (Order OD12345) despite multiple complaints."
 },
 "timeline": [
  {
   "date": "2026-09-10",
   "event": "Phone pickup completed"
  },
  {
   "date": "2026-10-01",
   "event": "Last complaint ticket raised"
  }
 ],
 "evidence_have": [
  "Order ID OD12345"
 ],
 "evidence_missing": [
  "Return pickup receipt",
  "Email/chat confirmation of return",
  "Copies of the 4 tickets raised"
 ],
 "next_step": "File a complaint with the National Consumer Helpline (1915) or on consumerhelpline.gov.in."
}
```

## Draft document

BEFORE THE DISTRICT CONSUMER DISPUTES REDRESSAL COMMISSION, [[FILL: District, e.g., Jaipur]]

COMPLAINANT:
[[FILL: Your Full Name]]
[[FILL: Your Full Address]]
[[FILL: Your Phone Number]]
[[FILL: Your Email Address]]

VERSUS

OPPOSITE PARTY:
[[FILL: Name of E-commerce Company]]
[[FILL: Registered Office Address of Company]]

COMPLAINT UNDER SECTION 35 OF THE CONSUMER PROTECTION ACT, 2019

MOST RESPECTFULLY SHOWETH:

1. I am a consumer as defined under Section 2(7) of the Consumer Protection Act, 2019, having purchased a phone from the Opposite Party for a total consideration of Rs 18,499 (Order ID: OD12345).

2. The phone was returned to the Opposite Party, and the pickup was successfully completed on 10 September 2026.

3. Despite the return of the product, the Opposite Party has failed to process the refund of Rs 18,499. I have contacted the Opposite Party multiple times regarding this delay.

4. I have raised 4 separate complaint tickets with the Opposite Party, with the last ticket raised on 1 October 2026. The Opposite Party continues to state that the refund is 'under process' but has failed to credit the amount.

5. The failure to refund the amount for a returned product constitutes a deficiency in service under Section 2(11) of the Consumer Protection Act, 2019, and an unfair trade practice under Section 2(47) of the Act.

6. This Commission has the pecuniary jurisdiction to entertain this complaint as the value of the goods is Rs 18,499, which is within the limit of the District Commission. The cause of action arose in [[FILL: City, e.g., Jaipur]], where I reside and where the service was availed. The complaint is filed within the limitation period of two years as per Section 69 of the Consumer Protection Act, 2019.

RELIEFS PRAYED:
In view of the facts mentioned above, I pray that this Hon'ble Commission may be pleased to direct the Opposite Party to:
(a) Refund the amount of Rs 18,499 immediately;
(b) Pay compensation for the mental agony and harassment caused by the deficiency in service;
(c) Pay the costs of this litigation.

LIST OF DOCUMENTS ANNEXED:
1. Copy of Order ID OD12345 details.
2. [[FILL: Any available proof of return pickup, if any]].
3. [[FILL: Copies of the 4 tickets raised, if available]].

VERIFICATION:
I, [[FILL: Your Full Name]], do hereby verify that the contents of paragraphs 1 to 6 are true to my knowledge and belief. Verified at [[FILL: City]] on this [[FILL: Date]] day of [[FILL: Month]], 2026.

____________________
(Signature of Complainant)

**Send instructions:** ["1. Visit the e-Jagriti portal (https://e-jagriti.gov.in/) to register and file your complaint electronically.", "2. Upload the drafted complaint along with any screenshots of your order, return status, and the ticket numbers you have.", "3. Since the amount paid is below Rs 5 lakh, there is no court fee required for filing.", "4. Keep a digital copy of the filed complaint and the acknowledgement receipt generated by the portal for your records.", "5. If you need assistance with the filing process, you can contact the National Consumer Helpline at 1915 or visit your nearest Common Service Centre (CSC) for Tele-Law support."]

## Automatic checks

| check | pass | detail |
|---|---|---|
| category | ✅ | got consumer |
| reply_language | ✅ | expected Latin, reply script Latin |
| fact:amount_paid | ✅ | expected ~18, got 18499 |
| mentions:1915|National Consumer Helpline | ✅ |  |
| mentions:District|Consumer Commission|consumer co | ✅ |  |
| escalation<=recommended | ✅ | got none |
| no_unverified_law_shown | ✅ |  |
| draft_no_unverified_law | ✅ | [] |
| draft_has_no_invented_fill | ✅ | 13 placeholders |
