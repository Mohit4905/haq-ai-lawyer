# T04_consumer_refund_ecommerce
Group: core

## Turn 1

**User:** I returned a phone I bought on an online shopping app for Rs 18,499. Pickup was done on 10 September 2026, order ID OD12345. They keep saying refund is 'under process'. I've raised 4 tickets, last one on 1 October 2026. Still nothing. I'm in Jaipur.

**Haq** (groq/openai/gpt-oss-120b, 35.82s):

Hi! From what you’ve told me, you bought a phone for ₹18,499, returned it on 10‑Sep‑2026 and have raised 4 tickets (last on 1‑Oct‑2026) but no refund yet. You have the order ID (OD12345) and ticket numbers as proof. 

**Next step:** Send a written complaint to the e‑commerce platform’s grievance officer (they must acknowledge within 48 hrs and resolve within a month). I can draft that email for you.

**What to include:**
- Order ID and purchase/return dates
- Copies of all ticket numbers and screenshots of the “under process” replies
- Clear demand: full refund of ₹18,499 + interest (if any) within 7 days
- Mention that under Consumer Protection (E‑Commerce) Rules 2020 you’re entitled to a timely refund.

Let me know if you’d like me to draft the email or need help gathering the screenshots.

**Calculated by code:** {"deadlines": [{"label": "Last date to file a consumer complaint (2 years from when the problem arose)", "date": "2028-10-01", "days_left": 695, "status": "ok", "basis": "CPA2019-S69", "note": "The commission can accept a late complaint only if you show sufficient cause for the delay.", "user_deadline": true}], "derived": [{"label": "Where to file", "value": "District Consumer Disputes Redressal Commission", "basis": "CPJURIS2021-R3-5", "note": "Based on the amount you paid (₹18,499), not the amount you claim."}, {"label": "Filing fee", "value": "Nil", "basis": "CPCDRC2020-R7", "note": ""}]}

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['CPECOM2020-R4-5', 'CPA2019-S69', 'CPA2019-S39']

## Final case file

```json
{
 "category": "consumer",
 "language": "English",
 "script": "Latin",
 "facts": {
  "product_or_service": "phone",
  "other_party_name": "online shopping app",
  "amount_paid": 18499,
  "purchase_date": "2026-09-10",
  "problem_date": "2026-10-01",
  "complained_to_company": "online shopping app",
  "city_state": "Jaipur",
  "proof": "order ID OD12345, ticket numbers, chat screenshots"
 },
 "timeline": [
  {
   "date": "2026-09-10",
   "event": "Phone returned, pickup done"
  },
  {
   "date": "2026-10-01",
   "event": "Last ticket raised, still no refund"
  }
 ],
 "evidence_have": [
  "order ID OD12345",
  "ticket numbers and dates",
  "chat screenshots showing “refund under process”"
 ],
 "evidence_missing": [
  "official receipt of return, email/letter acknowledging return"
 ],
 "next_step": "Send written complaint to the platform’s grievance officer"
}
```

## Draft document

BEFORE THE DISTRICT CONSUMER DISPUTES REDRESSAL COMMISSION, [[FILL: district]]

**Complainant:**
Name: [[FILL: Your Full Name]]
Address: [[FILL: Your Full Residential Address]]
Phone: [[FILL: Your Mobile Number]]
Email: [[FILL: Your Email Address]]

**Opposite Party:**
Name: [[FILL: Online Shopping App Name]]
Address: [[FILL: Registered Office/Corporate Address of the App]]
Phone: [[FILL: Customer Care Number of the App]]
Email: [[FILL: Official Customer Care Email]]

**COMPLAINT UNDER SECTION 35 OF THE CONSUMER PROTECTION ACT, 2019**

1. I am a consumer within the meaning of **CPA2019‑S2‑7** as I purchased a mobile phone through the online shopping app and paid Rs 18,499.
2. On **10 September 2026** I returned the phone (order ID **OD12345**) and the pickup was completed as per the app’s return policy.
3. The amount paid for the phone was **Rs 18,499**.
4. I raised a refund request immediately after the return. The app’s grievance officer repeatedly assured me that the refund was “under process”.
5. I lodged four separate tickets with the app’s support team; the last ticket (Ticket No. [[FILL: Ticket Number]]) was raised on **1 October 2026** and still no refund has been credited to my bank account.
6. I possess the following evidence: order ID **OD12345**, ticket numbers and dates, and chat screenshots showing the “refund under process” messages.
7. I have not received any official receipt of the return or any written acknowledgment from the app confirming the return or the pending refund.

**Deficiency in Service / Unfair Trade Practice**
The app has failed to refund the amount paid for the returned phone despite completing the pickup and acknowledging the return. This constitutes a *deficiency* in service under **CPA2019‑S2‑11** and amounts to an *unfair trade practice* under **CPA2019‑S2‑47** as the app misleads the consumer by repeatedly assuring a refund that is never effected.

**Jurisdiction**
- The cause of action arose in **Jaipur, Rajasthan**, where I reside and where the return was effected. 
- The amount in dispute (Rs 18,499) falls within the jurisdiction of the District Commission as per **CPJURIS2021‑R3‑5** (limit up to Rs 50 lakh).
- The complaint is filed within the statutory period of two years from the date the problem arose (**1 October 2026**) in accordance with **CPA2019‑S69**.

**Reliefs Prayed For**
1. Refund of the full amount of **Rs 18,499** with interest at the prevailing bank rate from the date of the last ticket (1 Oct 2026) until actual payment.
2. Compensation of **Rs 5,000** for mental harassment and inconvenience caused by the undue delay.
3. Reimbursement of any costs incurred in filing this complaint, including the nominal filing fee (nil as per **CPCDRC2020‑R7**).
4. Any other relief that the Hon’ble Commission may deem just and proper.

**List of Documents Annexed**
1. Copy of the order confirmation and payment receipt (if available).
2. Copy of the return pickup acknowledgment (if any).
3. Screenshots of chat conversations showing “refund under process”.
4. Copies of all four ticket numbers and dates.
5. Copy of this complaint.

**Verification**
I, [[FILL: Your Full Name]], the complainant above, do hereby verify that the contents of this complaint are true to the best of my knowledge and belief, and that no material fact has been concealed.

Date: [[FILL: Date of filing]]
Place: Jaipur

Signature of Complainant

---


**Send instructions:** ["1. Register on the e‑Jagriti portal (https://e-jagriti.gov.in/) and select ‘File a Complaint’.", "2. Fill in the details as per the draft, upload the annexed documents and the chat screenshots as evidence.", "3. Pay the filing fee (nil for amounts up to Rs 5 lakh) and submit the complaint electronically.", "4. After submission, download the acknowledgement receipt (PDF) and keep it safe as proof of filing.", "5. If the opposite party does not respond within 30 days, file a follow‑up application on e‑Jagriti requesting the Commission to issue a notice."]

## Automatic checks

| check | pass | detail |
|---|---|---|
| category | ✅ | got consumer |
| reply_language | ✅ | expected Latin, reply script Latin |
| fact:amount_paid | ✅ | expected ~18, got 18499 |
| mentions:1915|National Consumer Helpline | ❌ |  |
| mentions:District|Consumer Commission|consumer co | ❌ |  |
| escalation<=recommended | ✅ | got none |
| no_unverified_law_shown | ✅ |  |
| draft_no_unverified_law | ✅ | [] |
| draft_has_no_invented_fill | ✅ | 11 placeholders |
