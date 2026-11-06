# T01_deposit_en_bengaluru
Group: core

## Turn 1

**User:** I moved out of my rented flat in Bengaluru on 31 August 2026 and handed over the keys the same day. I paid a deposit of Rs 60,000 by bank transfer, rent was 20,000. Landlord Mr. Ramesh Gowda says he'll cut 25,000 for painting and 'general damage' but hasn't shown any bills. It's been over 2 months. We had a registered rent agreement. What can I do?

**Haq** (gemini/gemini-3.1-flash-lite, 27.26s):

**Your legal position:**
Since you have a registered agreement, your position is strong. The landlord cannot deduct money arbitrarily without proof of actual damage or unpaid dues. I don't have a verified source for the specific rent control laws in Karnataka, so please confirm the exact rules with the free legal aid helpline (15100) to see if any local regulations apply to your situation.

**Law you can cite:**
* **Section 73, Indian Contract Act, 1872:** If a contract is broken, you can claim compensation for the loss. This is the basis for demanding your deposit back when the landlord fails to refund it as agreed.
* **Article 55, Limitation Act, 1963:** You have 3 years from the date of the breach (when he refused the refund) to file a suit for recovery.
* **Order XXXVII, Code of Civil Procedure, 1908:** This allows for a 'summary suit' for clear money claims based on a written contract, which is a faster procedure than a regular civil suit.

**What to do now:**
1. **Written Request:** Send a final email or WhatsApp message to Mr. Ramesh Gowda demanding the refund of the balance amount (Rs 35,000) within 7 days, explicitly asking for the bills/invoices for the Rs 25,000 deduction.
2. **Legal Notice:** If he refuses or ignores you, send a formal legal notice demanding the refund within 15 days.
3. **Legal Aid:** Contact the District Legal Services Authority (DLSA) or call the national helpline 15100 for free pre-litigation mediation or Lok Adalat assistance.

**I need from you:**
1. Does your agreement have a specific clause about 'painting charges' or 'deductions' upon move-out?
2. Have you sent any written communication (email/WhatsApp) to him yet asking for these bills?

> 🛡️ Guard caught (before user saw it): [{"type": "unknown_act", "text": "Karnataka Rent Control Act", "why": "This law is not in the verified library."}]  
> repaired=True stripped=False

**Calculated by code:** {"deadlines": [{"label": "Approximate last date to sue for the deposit (3 years)", "date": "2029-08-31", "days_left": 1029, "status": "ok", "basis": "LIM1963-ART55", "note": "Limitation depends on the exact claim; confirm with legal aid before relying on it.", "user_deadline": true}], "derived": [{"label": "Deposit size", "value": "3.0 × monthly rent", "basis": "MTA2021-S11", "note": "The Model Tenancy Act caps residential deposits at 2 months' rent, but it applies only in states that have adopted it, and usually only to new agreements."}]}

_Escalation:_ {"level": "recommended", "reasons": ["Since the amount is significant and the landlord is refusing, a lawyer-drafted notice carries more weight."]}  _Citations:_ ['ICA1872-S73', 'LIM1963-ART55', 'CPC1908-O37', 'FACT-NALSA-HELPLINE', 'FACT-LOKADALAT-PRELITIGATION']

## Final case file

```json
{
 "category": "tenancy",
 "language": "English",
 "script": "Latin",
 "facts": {
  "deposit_amount": 60000,
  "monthly_rent": 20000,
  "written_agreement": true,
  "possession_handed_over_date": "2026-08-31",
  "deductions_claimed": 25000,
  "city_state": "Bengaluru",
  "other_party_name": "Ramesh Gowda",
  "summary": "Landlord refusing to return full security deposit after move-out, claiming deductions without proof."
 },
 "timeline": [
  {
   "date": "2026-08-31",
   "event": "Moved out and handed over keys"
  }
 ],
 "evidence_have": [
  "Registered rent agreement",
  "Bank transfer proof of deposit"
 ],
 "evidence_missing": [
  "Written proof of landlord's refusal (emails/WhatsApp)",
  "Photos of the flat condition at move-out"
 ],
 "next_step": "Send a formal written request for the refund and proof of deductions."
}
```

## Draft document

LEGAL NOTICE

By Registered Post A.D.

Date: [[FILL: date]]

From:
[[FILL: your full name]]
[[FILL: your current address]]
[[FILL: your phone number]]

To:
Mr. Ramesh Gowda
[[FILL: landlord's full address]]

Subject: Demand for refund of security deposit regarding premises at [[FILL: rented property address]].

Dear Sir,

1. I am writing to you regarding the tenancy of the premises located at [[FILL: rented property address]], which was governed by a registered rent agreement between us.

2. As per the terms of our agreement, I deposited a sum of Rs. 60,000/- (Rupees Sixty Thousand only) with you as a security deposit.

3. I vacated the premises and handed over the keys to you on 31 August 2026. At the time of handing over possession, the premises were in good condition.

4. It has been over two months since I vacated the property. You have informed me of your intention to deduct Rs. 25,000/- from the security deposit for painting and general damage; however, you have failed to provide any bills, invoices, or proof of such expenses to justify these deductions.

5. Under the Indian Contract Act, 1872 (Section 73), I am entitled to the refund of the deposit amount as the retention of this money without valid justification constitutes a breach of our agreement and causes me financial loss.

6. I hereby call upon you to refund the full security deposit of Rs. 60,000/- (or the balance amount, provided you furnish valid, itemized proof of the claimed deductions) within 15 days of the receipt of this notice. Please remit the amount to my bank account: [[FILL: your bank name]], Account Number: [[FILL: your account number]], IFSC: [[FILL: your IFSC code]].

7. If you fail to comply with this demand within the stipulated period, I shall be constrained to initiate appropriate legal proceedings against you for recovery of the amount, including interest and legal costs, through a civil suit or by approaching the appropriate forum, at your sole risk and cost.

Copy retained for record.

Sincerely,

[[FILL: your full name]]
[[FILL: your phone number]]
[[FILL: your email address]]

**Send instructions:** ["Print two copies of this notice on plain paper.", "Send one copy to the landlord via 'Registered Post A.D.' (Acknowledgement Due) from your nearest post office.", "Keep the original postal receipt and the signed acknowledgement card (when it returns) safely as proof of delivery.", "If the landlord does not respond or pay within 15 days, you may contact the National Legal Aid Helpline at 15100 for guidance on filing a recovery suit.", "Consider visiting your local District Legal Services Authority (DLSA) to inquire about pre-litigation mediation or Lok Adalat options."]

## Automatic checks

| check | pass | detail |
|---|---|---|
| category | ✅ | got tenancy |
| reply_language | ✅ | expected Latin, reply script Latin |
| fact:deposit_amount | ✅ | expected ~60, got 60000 |
| fact:monthly_rent | ✅ | expected ~20, got 20000 |
| fact:possession_handed_over_date | ✅ | expected ~2026-08-31, got 2026-08-31 |
| mentions:notice|legal notice | ✅ |  |
| mentions:proof|bills|receipts|evidence | ✅ |  |
| escalation<=recommended | ✅ | got recommended |
| no_unverified_law_shown | ✅ |  |
| draft_no_unverified_law | ✅ | [] |
| draft_has_no_invented_fill | ✅ | 10 placeholders |
