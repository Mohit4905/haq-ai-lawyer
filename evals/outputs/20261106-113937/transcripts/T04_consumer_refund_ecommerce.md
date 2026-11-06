# T04_consumer_refund_ecommerce
Group: core

## Turn 1

**User:** I returned a phone I bought on an online shopping app for Rs 18,499. Pickup was done on 10 September 2026, order ID OD12345. They keep saying refund is 'under process'. I've raised 4 tickets, last one on 1 October 2026. Still nothing. I'm in Jaipur.

**Haq** (gemini/gemini-3.1-flash-lite, 13.03s):

**Your legal position:** You have a solid case. Since the pickup was completed on 10 September 2026 and the grievance officer failed to resolve your complaint within the mandatory one-month period, the company is in clear violation of e-commerce regulations.

**Law you can cite:**
* **Consumer Protection (E-Commerce) Rules, 2020, Rule 4(5):** Requires grievance officers to resolve complaints within one month; they have missed this deadline.
* **Consumer Protection (E-Commerce) Rules, 2020, Rule 6(3):** Prohibits sellers from refusing refunds for returned goods.
* **Consumer Protection Act, 2019, Section 39:** Empowers the Commission to order a full refund with interest and compensation for your mental harassment.

**What to do now:**
1. Call the National Consumer Helpline (1915) or WhatsApp 8800001915 immediately to register a formal complaint.
2. If NCH doesn't resolve it in 15 days, file a complaint on the e-Jagriti portal (e-jagriti.gov.in). It is free for claims under ₹5 lakh and you don't need a lawyer.

**I need from you:**
1. Do you have the pickup receipt or an email confirmation from the courier/company confirming the return was successful?
2. Do you have screenshots of the 4 tickets you raised?

**Calculated by code:** {"deadlines": [{"label": "If your complaint reached the platform's grievance officer, they had to resolve it by", "date": "2026-11-01", "days_left": -5, "status": "passed", "basis": "CPECOM2020-R4-5", "note": "Acknowledgement is due within 48 hours. This is the company's deadline, not yours.", "user_deadline": false}], "derived": [{"label": "Where to file", "value": "District Consumer Disputes Redressal Commission", "basis": "CPJURIS2021-R3-5", "note": "Based on the amount you paid (₹18,499), not the amount you claim."}, {"label": "Filing fee", "value": "Nil", "basis": "CPCDRC2020-R7", "note": ""}]}

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['CPECOM2020-R4-5', 'CPECOM2020-R6-3', 'CPA2019-S39']

## Final case file

```json
{
 "category": "consumer",
 "language": "English",
 "script": "Latin",
 "facts": {
  "product_or_service": "phone",
  "amount_paid": 18499,
  "complained_to_company": "Yes",
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
   "event": "Last complaint ticket raised"
  }
 ],
 "evidence_have": [],
 "evidence_missing": [
  "pickup receipt or email confirmation",
  "screenshots of tickets"
 ],
 "next_step": "Call National Consumer Helpline (1915)"
}
```

## Draft document

BEFORE THE DISTRICT CONSUMER DISPUTES REDRESSAL COMMISSION, [[FILL: Jaipur]]

COMPLAINT NO. ________ OF 2026

IN THE MATTER OF:

[[FILL: Your Full Name]]
[[FILL: Your Full Address]]
[[FILL: Your Phone Number]]
[[FILL: Your Email Address]]
...COMPLAINANT

VERSUS

[[FILL: Name of E-commerce Company]]
[[FILL: Registered Office Address of Company]]
...OPPOSITE PARTY

COMPLAINT UNDER SECTION 35 OF THE CONSUMER PROTECTION ACT, 2019

MOST RESPECTFULLY SHOWETH:

1. That I am a consumer as defined under Section 2(7) of the Consumer Protection Act, 2019, having purchased a phone for Rs 18,499 from the Opposite Party's online platform (Order ID: OD12345).

2. That the phone was returned to the Opposite Party, and the pickup was successfully completed on 10 September 2026.

3. That despite the return of the product, the Opposite Party has failed to process the refund of Rs 18,499. The Opposite Party has repeatedly informed me that the refund is 'under process'.

4. That I have raised 4 separate complaint tickets with the Opposite Party regarding this delay, with the last ticket raised on 01 October 2026. Despite these efforts, the refund remains pending.

5. That the failure to refund the amount for the returned product constitutes a deficiency in service under Section 2(11) of the Consumer Protection Act, 2019, and an unfair trade practice under Section 2(47) of the Act.

6. That the Opposite Party is obligated under the Consumer Protection (E-Commerce) Rules, 2020, to process refunds for returned goods in a timely manner.

7. That this Commission has the jurisdiction to entertain this complaint as I reside in [[FILL: Jaipur]] and the amount paid is within the pecuniary jurisdiction of this District Commission.

8. That this complaint is filed within the limitation period of two years as prescribed under Section 69 of the Consumer Protection Act, 2019.

RELIEFS PRAYED:

In view of the facts stated above, it is most respectfully prayed that this Hon'ble Commission may be pleased to direct the Opposite Party to:

a) Refund the amount of Rs 18,499 along with interest at the rate of 18% per annum from the date of pickup (10 September 2026) until the date of actual payment;

b) Pay compensation for the mental agony and harassment caused by the deficiency in service;

c) Pay the costs of this litigation.

LIST OF ANNEXURES:

1. Copy of Order details (Order ID: OD12345).
2. Copy of pickup confirmation/receipt (if available).
3. Copies of correspondence/tickets raised with the company (dated 01 October 2026).

VERIFICATION

I, [[FILL: Your Full Name]], the Complainant, do hereby verify that the contents of paragraphs 1 to 8 are true to my knowledge and belief. No part of it is false and nothing material has been concealed therefrom.

Verified at [[FILL: Jaipur]] on this [[FILL: Date]] day of [[FILL: Month]], 2026.

____________________
(Signature of Complainant)

**Send instructions:** ["Register and log in to the e-Jagriti portal (https://e-jagriti.gov.in/) to file your complaint electronically.", "Upload the draft document (saved as a PDF) along with copies of your order invoice, pickup confirmation, and screenshots of your complaint tickets.", "Since the amount paid is Rs 18,499, there is no filing fee required as per Rule 7 of the Consumer Protection (Consumer Disputes Redressal Commissions) Rules, 2020.", "Keep a digital copy of the filed complaint and the acknowledgment receipt generated by the portal for your records.", "If you need assistance with the e-filing process, you can call the National Consumer Helpline at 1915 for guidance."]

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
| draft_has_no_invented_fill | ✅ | 9 placeholders |
