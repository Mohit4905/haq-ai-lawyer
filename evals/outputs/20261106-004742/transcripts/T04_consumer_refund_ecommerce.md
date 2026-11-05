# T04_consumer_refund_ecommerce
Group: core

## Turn 1

**User:** I returned a phone I bought on an online shopping app for Rs 18,499. Pickup was done on 10 September 2026, order ID OD12345. They keep saying refund is 'under process'. I've raised 4 tickets, last one on 1 October 2026. Still nothing. I'm in Jaipur.

**Haq** (groq/openai/gpt-oss-20b, 4.67s):

Hi! I understand you’re waiting for a refund of ₹18,499 for a phone you returned on 10 Sep 2026 via the online app (order OD12345). You’ve opened 4 tickets, last on 1 Oct 2026, and still haven’t received the money.

**What I need to know next**
1. Do you have the order confirmation, payment receipt, or any screenshots of the return process? 
2. Did the app send you any email or message confirming the return and the refund amount?

Once I have those, I can tell you exactly how to proceed.

**Quick options (cheapest/fastest first)**
1. Send a written complaint to the app’s grievance officer (must be acknowledged in 48 h, resolved in 1 month – see CPECOM2020‑R4‑5). 
2. Call the National Consumer Helpline 1915 (free). 
3. File a consumer complaint on e‑Jagriti (no fee up to ₹5 lakh, deadline 2028‑10‑01). 
4. If the app still refuses, consider a legal notice or approach the District Consumer Commission.

I recommend starting with a formal written complaint to the grievance officer. I can draft the email for you.

**Calculated by code:** {"deadlines": [{"label": "Last date to file a consumer complaint (2 years from when the problem arose)", "date": "2028-10-01", "days_left": 695, "status": "ok", "basis": "CPA2019-S69", "note": "The commission can accept a late complaint only if you show sufficient cause for the delay.", "user_deadline": true}], "derived": [{"label": "Where to file", "value": "District Consumer Disputes Redressal Commission", "basis": "CPJURIS2021-R3-5", "note": "Based on the amount you paid (₹18,499), not the amount you claim."}, {"label": "Filing fee", "value": "Nil", "basis": "CPCDRC2020-R7", "note": ""}]}

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['CPECOM2020-R4-5', 'FACT-NCH-HELPLINE', 'FACT-EJAGRITI-PORTAL', 'CPA2019-S35', 'CPA2019-S39']

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
  "city_state": "Jaipur"
 },
 "timeline": [],
 "evidence_have": [],
 "evidence_missing": [
  "order confirmation/receipt",
  "screenshots of return process",
  "any email/notification from app"
 ],
 "next_step": "draft a written complaint to the app’s grievance officer"
}
```

## Draft document

**BEFORE THE DISTRICT CONSUMER DISPUTES REDRESSAL COMMISSION, JAIPUR**

**Complainant**
Name: [[FILL: your full name]]
Address: [[FILL: your full address]]
Contact: [[FILL: your phone number]]
Email: [[FILL: your email address]]

**Opposite Party**
Name: Online Shopping App (Seller)
Address: [[FILL: seller’s registered address]]

**COMPLAINT UNDER SECTION 35 OF THE CONSUMER PROTECTION ACT, 2019**

**FACTS**
1. On 10 September 2026, I purchased a mobile phone from the online shopping app (Seller) and paid ₹18,499. The order ID is OD12345.
2. The phone was picked up for return on 10 September 2026.
3. I raised a return request with the Seller and received confirmation that the refund is “under process”.
4. I have opened four separate tickets with the Seller’s grievance portal, the last one on 1 October 2026, but no refund has been credited to my account.
5. The Seller has not provided any written acknowledgment, receipt, or communication confirming the refund amount or the date of credit.

**DEFICIENCY IN SERVICE**
The Seller’s failure to refund the amount within a reasonable time, despite repeated requests, constitutes a deficiency in service as defined under s.2(11) of the Consumer Protection Act, 2019.

**JURISDICTION AND LIMITATION**
I reside in Jaipur, and the amount paid (₹18,499) is within the jurisdiction of the District Commission as per Rule 3-5 of the Consumer Protection (Jurisdiction of the District Commission, the State Commission and the National Commission) Rules, 2021. The complaint is filed within the two‑year limitation period as per s.69 of the Act.

**RELIEF PRAYED**
1. Immediate refund of ₹18,499 to my bank account.
2. Compensation for the inconvenience and harassment caused, as per the provisions of the Act.
3. Payment of any applicable interest on the refund amount.
4. Order for the Seller to comply with the refund timelines stipulated in the e‑commerce rules.

**LIST OF DOCUMENTS ANNEXED**
1. Copy of the purchase receipt (if available).
2. Screenshots of the return tickets (if available).
3. Any email or notification from the Seller regarding the refund (if available).
4. Proof of payment (bank statement or credit card statement showing ₹18,499 paid on 10 September 2026).

**VERIFICATION**
I, the undersigned, verify that the facts stated above are true to the best of my knowledge and belief.

Date: [[FILL: date of filing]]

Signature: ______________________

**PLACEHOLDERS**
- [[FILL: your full name]]
- [[FILL: your full address]]
- [[FILL: your phone number]]
- [[FILL: your email address]]
- [[FILL: seller’s registered address]]
- [[FILL: date of filing]]

**CITATIONS**
- CPA2019-S2(11)
- CPA2019-S35
- CPA2019-S39
- CPA2019-S69
- CPJURIS2021-R3-5
- CPCDRC2020-R7

**SEND INSTRUCTIONS**
1. Log in to the e‑Jagriti portal (https://e-jagriti.gov.in/).
2. Select “File a Consumer Complaint” and choose the District Commission for Jaipur.
3. Upload the complaint document and all annexed files.
4. Pay the filing fee (nil for amounts up to ₹5 lakh) and keep the e‑receipt as proof.
5. If no acknowledgment is received within 48 hours, call the National Consumer Helpline at 1915 or 1800‑11‑4000 to confirm the filing.
6. If the Seller still does not refund within the time specified by the Commission, file a request for a hearing and attend the virtual hearing as scheduled.

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
| draft_has_no_invented_fill | ✅ | 6 placeholders |
