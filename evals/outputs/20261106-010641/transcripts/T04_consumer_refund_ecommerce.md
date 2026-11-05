# T04_consumer_refund_ecommerce
Group: core

## Turn 1

**User:** I returned a phone I bought on an online shopping app for Rs 18,499. Pickup was done on 10 September 2026, order ID OD12345. They keep saying refund is 'under process'. I've raised 4 tickets, last one on 1 October 2026. Still nothing. I'm in Jaipur.

**Haq** (groq/qwen/qwen3.8-27b, 9.75s):

Frustrating situation — 4 tickets and still nothing. Here's where you stand:

**Good news:** The platform's 1-month resolution deadline has already passed. That works in your favour.

**Your options (cheapest first):**

1. **National Consumer Helpline** – call 1915 or WhatsApp 8800001915. Free, pre-litigation. They'll nudge the company.
2. **Legal notice** to the company (optional, adds pressure).
3. **Consumer complaint on e-Jagriti** (e-jagriti.gov.in) – District Commission, Jaipur. Filing fee: **nil** (your amount is under ₹5 lakh). No lawyer needed. You can file from home.

**My recommendation:** Since the company has already missed its deadline and you have 4 tickets as proof, go straight to **e-Jagriti**. It's free and you can file the complaint yourself.

Two quick questions:
- Which app/platform was it (Flipkart, Amazon, etc.)?
- Do you have the pickup confirmation or ticket numbers saved (screenshot or email)?

**Calculated by code:** {"deadlines": [{"label": "Last date to file a consumer complaint (2 years from when the problem arose)", "date": "2028-09-10", "days_left": 674, "status": "ok", "basis": "CPA2019-S69", "note": "The commission can accept a late complaint only if you show sufficient cause for the delay.", "user_deadline": true}, {"label": "If your complaint reached the platform's grievance officer, they had to resolve it by", "date": "2026-11-01", "days_left": -5, "status": "passed", "basis": "CPECOM2020-R4-5", "note": "Acknowledgement is due within 48 hours. This is the company's deadline, not yours.", "user_deadline": false}], "derived": [{"label": "Where to file", "value": "District Consumer Disputes Redressal Commission", "basis": "CPJURIS2021-R3-5", "note": "Based on the amount you paid (₹18,499), not the amount you claim."}, {"label": "Filing fee", "value": "Nil", "basis": "CPCDRC2020-R7", "note": ""}]}

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['CPECOM2020-R4-5', 'CPECOM2020-R6-3', 'CPA2019-S69', 'CPJURIS2021-R3-5', 'CPCDRC2020-R7', 'FACT-EJAGRITI-PORTAL', 'FACT-NCH-HELPLINE', 'CPA2019-S39']

## Final case file

```json
{
 "category": "consumer",
 "language": "English",
 "script": "Latin",
 "facts": {
  "product_or_service": "Phone",
  "amount_paid": 18499,
  "complained_to_company": "Yes, 4 tickets raised",
  "complained_to_company_date": "2026-10-01",
  "city_state": "Jaipur",
  "is_ecommerce": true,
  "summary": "Refund pending for returned phone (Order OD12345) despite 4 complaints. Pickup done 10 Sep 2026. Company's 1-month resolution deadline passed.",
  "purchase_date": "2026-09-10",
  "problem_date": "2026-09-10"
 },
 "timeline": [
  {
   "date": "2026-09-10",
   "event": "Phone pickup done for return"
  },
  {
   "date": "2026-10-01",
   "event": "4th ticket raised with company"
  }
 ],
 "evidence_have": [
  "Order ID OD12345",
  "4 complaint tickets (dates unknown except last: 1 Oct 2026)"
 ],
 "evidence_missing": [
  "Pickup confirmation (screenshot/email)",
  "Original order confirmation/invoice",
  "Ticket numbers or chat screenshots",
  "Platform name"
 ],
 "next_step": "File consumer complaint on e-Jagriti (e-jagriti.gov.in) against the platform for non-refund"
}
```

## Draft document

BEFORE THE DISTRICT CONSUMER DISPUTES REDRESSAL COMMISSION, [[FILL: Jaipur]]

COMPLAINT NO. ________ OF 2026

IN THE MATTER OF:

[[FILL: Your Full Name]]
[[FILL: Your Full Address]]
[[FILL: Your Phone Number]]
...COMPLAINANT

VERSUS

[[FILL: Name of E-commerce Platform]]
[[FILL: Address of E-commerce Platform]]
...OPPOSITE PARTY

COMPLAINT UNDER SECTION 35 OF THE CONSUMER PROTECTION ACT, 2019

MOST RESPECTFULLY SHOWETH:

1. The Complainant is a consumer as defined under Section 2(7) of the Consumer Protection Act, 2019, having purchased a phone from the Opposite Party for a total consideration of Rs. 18,499 (Order ID: OD12345).

2. The Complainant returned the said phone, and the pickup was successfully completed by the Opposite Party on 10 September 2026.

3. Despite the return of the product, the Opposite Party has failed to process the refund, repeatedly stating that the refund is 'under process'.

4. The Complainant has raised 4 separate complaints with the Opposite Party regarding the non-receipt of the refund, with the last complaint raised on 01 October 2026. Despite these efforts, the Opposite Party has failed to resolve the grievance.

5. The Opposite Party’s failure to refund the amount for the returned product constitutes a 'deficiency in service' under Section 2(11) of the Consumer Protection Act, 2019, and a violation of the Consumer Protection (E-Commerce) Rules, 2020, specifically Rule 6(3) and Rule 4(10), which mandate that a refund must be processed for returned goods.

6. This complaint is filed within the limitation period of two years as prescribed under Section 69 of the Consumer Protection Act, 2019.

7. This Commission has the pecuniary and territorial jurisdiction to entertain this complaint as the amount paid is below Rs. 50 Lakhs and the cause of action arose within the jurisdiction of this Commission.

RELIEFS PRAYED:

In view of the facts stated above, it is most respectfully prayed that this Hon'ble Commission may be pleased to direct the Opposite Party to:

a) Refund the amount of Rs. 18,499 to the Complainant;
b) Pay compensation for the mental agony and harassment caused by the deficiency in service;
c) Pay the costs of litigation.

LIST OF DOCUMENTS ANNEXED:
[[FILL: List of documents attached, e.g., Order confirmation, Pickup receipt, Screenshots of complaint tickets]]

VERIFICATION

I, [[FILL: Your Full Name]], the Complainant, do hereby verify that the contents of paragraphs 1 to 7 are true to my knowledge and belief. No part of it is false and nothing material has been concealed therefrom.

Verified at [[FILL: Jaipur]] on this ____ day of ________ 2026.

(Signature)
[[FILL: Your Full Name]]

**Send instructions:** ["1. Visit the e-Jagriti portal at https://e-jagriti.gov.in/.", "2. Register or log in to your account and select 'File a Complaint'.", "3. Fill in the details using the draft above. Ensure you attach all evidence (Order ID, pickup confirmation, and screenshots of your 4 complaint tickets) as PDFs.", "4. Since the amount is below Rs. 5 Lakh, there is no filing fee required.", "5. Submit the complaint electronically and save the acknowledgement receipt provided by the portal for your records."]

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
| draft_has_no_invented_fill | ✅ | 7 placeholders |
