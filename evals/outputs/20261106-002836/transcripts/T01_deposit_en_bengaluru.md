# T01_deposit_en_bengaluru
Group: core

## Turn 1

**User:** I moved out of my rented flat in Bengaluru on 31 August 2026 and handed over the keys the same day. I paid a deposit of Rs 60,000 by bank transfer, rent was 20,000. Landlord Mr. Ramesh Gowda says he'll cut 25,000 for painting and 'general damage' but hasn't shown any bills. It's been over 2 months. We had a registered rent agreement. What can I do?

**Haq** (groq/openai/gpt-oss-120b, 4.19s):

From what you’ve told me, you have a registered agreement, paid the ₹60,000 deposit by bank transfer and handed over the flat on 31‑Aug‑2026. Your landlord is keeping ₹25,000 without any bill or itemised list. 

**Where you stand**
- The deposit amount is higher than the Model Tenancy Act cap (2 months’ rent) but that law only applies in a few states, not Karnataka, so the usual contract rules apply. 
- You can claim the full deposit back unless you can prove actual damage costing ₹25,000. 

**Options (cheapest first)**
1. **Written demand** – send a WhatsApp/email asking for the ₹60,000 back, list the amount, your bank details and say you’ll take further steps if not paid in 15 days. Keep screenshots. 
2. **Legal notice** – if no reply, a formal notice (you can send yourself) demanding refund within 15 days. 
3. **Pre‑litigation Lok Adalat** – apply through the District Legal Services Authority for an amicable settlement (free). 
4. **Civil suit** – file a recovery suit (within 3 years). This needs a lawyer and court fees.

**Next step**: Send a written demand now. I can draft a simple demand notice for you.

Would you like me to draft that document?

**Calculated by code:** {"deadlines": [{"label": "Approximate last date to sue for the deposit (3 years)", "date": "2029-08-31", "days_left": 1029, "status": "ok", "basis": "LIM1963-ART55", "note": "Limitation depends on the exact claim; confirm with legal aid before relying on it.", "user_deadline": true}], "derived": [{"label": "Deposit size", "value": "3.0 × monthly rent", "basis": "MTA2021-S11", "note": "The Model Tenancy Act caps residential deposits at 2 months' rent, but it applies only in states that have adopted it, and usually only to new agreements."}]}

_Escalation:_ {"level": "recommended", "reasons": ["to send a proper legal notice if demand is ignored"]}  _Citations:_ ['ICA1872-S73', 'LIM1963-ART55']

## Final case file

```json
{
 "category": "tenancy",
 "language": "English",
 "script": "Latin",
 "facts": {
  "deposit_amount": 60000,
  "monthly_rent": 20000,
  "written_agreement": "registered",
  "possession_handed_over_date": "2026-08-31",
  "deductions_claimed": 25000,
  "other_party_name": "Mr. Ramesh Gowda",
  "city_state": "Bengaluru, India"
 },
 "timeline": [
  {
   "date": "2026-08-31",
   "event": "Handed over keys and possession"
  }
 ],
 "evidence_have": [],
 "evidence_missing": [
  "Bank transfer receipt of deposit",
  "Any communication (WhatsApp, email, call log) with landlord about deductions",
  "Itemised bill or estimate for painting/damage"
 ],
 "next_step": "Send a written demand for full deposit refund"
}
```

## Draft document

## LEGAL NOTICE (By Registered Post A.D.)
**Date:** [[FILL: date]]

**From:**
[[FILL: Your Full Name]]
[[FILL: Your Current Address]]

**To:**
Mr. Ramesh Gowda
[[FILL: Landlord's Full Address]]

**Subject:** Demand for Refund of Security Deposit of Rs. 60,000

1. I entered into a **registered rent agreement** with Mr. Ramesh Gowda for a residential flat in Bengaluru, India, at a monthly rent of Rs. 20,000.
2. As per the agreement, I paid a security deposit of Rs. 60,000 by bank transfer on [[FILL: deposit payment date]].
3. I vacated the premises and handed over the keys and possession on **31 August 2026**.
4. The landlord has informed me that he will retain Rs. 25,000 for alleged painting and "general damage" but has not produced any itemised bill, estimate, or any communication evidencing such deductions.
5. It has now been more than two months since I vacated the premises, and despite my verbal/ informal requests, the landlord has not refunded the balance of the deposit.

**Legal Basis**
- Under **Indian Contract Act, 1872 s.73** (citation: [ICA1872‑S73]), a party who breaches a contract is liable to compensate the loss caused, which includes the return of a security deposit when no valid deduction is proven.
- Although the Model Tenancy Act, 2021 caps deposits and mandates refund on vacant possession (citation: [MTA2021‑S11]), its applicability depends on state adoption. Regardless, the principle that a landlord may retain a deposit only after showing actual, documented loss is well‑established under contract law.

**Demand**
I hereby demand the immediate refund of the **balance amount of Rs. 35,000** (Rs. 60,000 deposit – Rs. 25,000 alleged deduction) within **15 days** of receipt of this notice. The amount should be transferred to the following bank account:
- Account Holder: [[FILL: Your Name]]
- Bank Name: [[FILL: Bank Name]]
- Account Number: [[FILL: Account Number]]
- IFSC Code: [[FILL: IFSC]]

**Consequences of Non‑Compliance**
If the demanded amount is not received within the stipulated period, I will be compelled to initiate lawful remedies, including filing a civil suit for recovery of the deposit with interest and costs, or approaching the appropriate Lok Adalat for pre‑litigation settlement, as provided under the Legal Services Authorities Act, 1987. All expenses incurred will be borne by you.

**Copy retained for record.**

---
**Signature**
[[FILL: Your Full Name]]
Phone: [[FILL: Your Phone Number]]
Email: [[FILL: Your Email Address]]

**Send instructions:** ["Print the notice on plain A4 paper and sign it.", "Attach a self‑addressed, stamped envelope for the landlord's reply.", "Send the notice by Registered Post (A.D.) to the landlord's address; retain the postal receipt as proof of dispatch.", "Make a scanned copy of the signed notice and the postal receipt for your records.", "If no response is received within 15 days, consult a lawyer or approach the District Legal Services Authority to initiate a Lok Adalat or file a civil suit."]

## Automatic checks

| check | pass | detail |
|---|---|---|
| category | ✅ | got tenancy |
| reply_language | ✅ | expected Latin, reply script Latin |
| fact:deposit_amount | ✅ | expected ~60, got 60000 |
| fact:monthly_rent | ✅ | expected ~20, got 20000 |
| fact:possession_handed_over_date | ✅ | expected ~2026-08-31, got 2026-08-31 |
| mentions:notice|legal notice | ✅ |  |
| mentions:proof|bills|receipts|evidence | ❌ |  |
| escalation<=recommended | ✅ | got recommended |
| no_unverified_law_shown | ✅ |  |
| draft_no_unverified_law | ✅ | [] |
| draft_has_no_invented_fill | ✅ | 11 placeholders |
