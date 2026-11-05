# T01_deposit_en_bengaluru
Group: core

## Turn 1

**User:** I moved out of my rented flat in Bengaluru on 31 August 2026 and handed over the keys the same day. I paid a deposit of Rs 60,000 by bank transfer, rent was 20,000. Landlord Mr. Ramesh Gowda says he'll cut 25,000 for painting and 'general damage' but hasn't shown any bills. It's been over 2 months. We had a registered rent agreement. What can I do?

**Haq** (gemini/gemini-3.1-flash-lite, 6.11s):

It is frustrating when a landlord holds back your deposit without proof of damages. Since you have a registered agreement, you are in a better position.

Here is where you stand:
- You have a strong basis to demand the return of the deposit under the Indian Contract Act, 1872, as the landlord must justify deductions with actual expenses.
- Since you are in Bengaluru, Karnataka, note that the Model Tenancy Act does not apply here as the state has not adopted it. Your rights are governed by your agreement and general contract law.

**Your Options:**
1. **Written Request:** Send a formal email or WhatsApp message to Mr. Gowda demanding the itemized bills for the Rs 25,000 deduction within 7 days, or the full refund.
2. **Legal Notice:** If he ignores you, send a formal legal notice demanding the refund within 15 days.
3. **Legal Aid:** Contact the Karnataka State Legal Services Authority (KSLA) or call 15100 for free guidance.
4. **Civil Suit:** You can file a recovery suit in a civil court, but this is a longer process.

**Next Step:** Start by sending a formal written request asking for the bills. Would you like me to help you draft that message?

**Calculated by code:** {"deadlines": [{"label": "Approximate last date to sue for the deposit (3 years)", "date": "2029-08-31", "days_left": 1029, "status": "ok", "basis": "LIM1963-ART55", "note": "Limitation depends on the exact claim; confirm with legal aid before relying on it.", "user_deadline": true}], "derived": [{"label": "Deposit size", "value": "3.0 × monthly rent", "basis": "MTA2021-S11", "note": "The Model Tenancy Act caps residential deposits at 2 months' rent, but it applies only in states that have adopted it, and usually only to new agreements."}]}

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['ICA1872-S73', 'FACT-NALSA-HELPLINE', 'LIM1963-ART55']

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
  "deductions_claimed": "25000 for painting and general damage",
  "city_state": "Bengaluru",
  "other_party_name": "Ramesh Gowda",
  "summary": "Landlord is withholding 25,000 from 60,000 security deposit without providing bills for painting and damages.",
  "communications_so_far": "None mentioned",
  "proof_of_payment": "Bank transfer"
 },
 "timeline": [
  {
   "date": "2026-08-31",
   "event": "Moved out and handed over keys"
  }
 ],
 "evidence_have": [
  "Registered rent agreement",
  "Bank transfer record of deposit"
 ],
 "evidence_missing": [
  "Written communication with landlord regarding the deduction",
  "Photos of the flat condition at move-out"
 ],
 "next_step": "Draft a formal written request for the landlord"
}
```

## Draft document

LEGAL NOTICE
By Registered Post A.D.
Date: [[FILL: date]]

From:
[[FILL: Your Full Name]]
[[FILL: Your Current Address]]

To:
Mr. Ramesh Gowda
[[FILL: Landlord's Full Address]]

Subject: Demand for refund of security deposit regarding premises at [[FILL: Rented Property Address]].

Dear Mr. Ramesh Gowda,

1. I am writing to you regarding the registered rent agreement dated [[FILL: Date of Rent Agreement]] for the premises located at [[FILL: Rented Property Address]].

2. As per our agreement, I deposited a sum of Rs. 60,000/- as a security deposit, which was paid via bank transfer.

3. I vacated the premises and handed over the keys to you on 31 August 2026.

4. You have informed me of your intention to deduct Rs. 25,000/- from the security deposit for painting and general damages. However, you have failed to provide any bills, invoices, or evidence to justify these deductions.

5. Under Section 73 of the Indian Contract Act, 1872, you are liable to compensate for the loss caused by the breach of contract, which includes the failure to refund the security deposit as agreed upon the termination of the tenancy.

6. I hereby demand that you refund the balance of the security deposit, or provide valid, itemized bills for the claimed deductions, within 15 days of receiving this notice.

7. Please remit the amount to the following bank account:
   Account Name: [[FILL: Your Name]]
   Bank Name: [[FILL: Your Bank Name]]
   Account Number: [[FILL: Your Account Number]]
   IFSC: [[FILL: Your IFSC Code]]

8. If you fail to comply with this demand within the specified period, I shall be constrained to initiate appropriate legal proceedings for the recovery of the amount, including interest and legal costs, at your risk and expense.

Copy retained for record.

Sincerely,

[[FILL: Your Full Name]]
[[FILL: Your Phone Number]]
[[FILL: Your Email Address]]

**Send instructions:** ["Print two copies of this notice. Sign both copies in blue or black ink.", "Send one copy to the landlord via 'Registered Post A.D.' (Acknowledgement Due) from your nearest post office.", "Keep the original postal receipt and the 'Acknowledgement Due' card (which will be returned to you by post once the landlord receives the letter) as proof of delivery.", "Keep the second copy for your own records.", "If the landlord does not respond or pay within 15 days of receiving the notice, you may consider filing a civil suit for recovery or approaching the local District Legal Services Authority for mediation/Lok Adalat."]

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
| escalation<=recommended | ✅ | got none |
| no_unverified_law_shown | ✅ |  |
| draft_no_unverified_law | ✅ | [] |
| draft_has_no_invented_fill | ✅ | 12 placeholders |
