# T01_deposit_en_bengaluru
Group: core

## Turn 1

**User:** I moved out of my rented flat in Bengaluru on 31 August 2026 and handed over the keys the same day. I paid a deposit of Rs 60,000 by bank transfer, rent was 20,000. Landlord Mr. Ramesh Gowda says he'll cut 25,000 for painting and 'general damage' but hasn't shown any bills. It's been over 2 months. We had a registered rent agreement. What can I do?

**Haq** (gemini/gemini-3.1-flash-lite, 13.22s):

Hello. See, a landlord cannot deduct your security deposit without any proof or bills. You have a registered agreement, which is your biggest proof. Your case seems quite solid because the landlord has provided no justification. According to the contract, they must return the deposit or provide proof of valid expenses.

**Your legal position:**
The landlord deducting money without bills is a violation of the contract. Your registered agreement strengthens your claim. You are legally entitled to demand the full amount back unless they show proof of damages.

**Law you can cite:**
* **Indian Contract Act, 1872 Section 73:** If someone breaches a contract (such as not returning a deposit), you can claim compensation for the loss caused.
* **Limitation Act, 1963 Article 55:** You have 3 years to file a suit for breach of contract.

**What to do now:**
1. Send a formal email or WhatsApp message clearly stating that you require a breakdown and bills for the 25,000, otherwise, you will send a legal notice.
2. If they do not agree, send a formal 'Legal Notice' (I can help you with this).
3. For free legal advice, call the NALSA helpline at 15100 or visit your district's DLSA office.

**I need from you:**
1. Do you have proof of the bank transfer and a copy of the registered agreement?
2. Have you sent any written request to the landlord yet, or has it only been a verbal conversation?

**Calculated by code:** {"deadlines": [{"label": "Approximate last date to sue for the deposit (3 years)", "date": "2029-08-31", "days_left": 1029, "status": "ok", "basis": "LIM1963-ART55", "note": "Limitation depends on the exact claim; confirm with legal aid before relying on it.", "user_deadline": true}], "derived": [{"label": "Deposit size", "value": "3.0 × monthly rent", "basis": "MTA2021-S11", "note": "The Model Tenancy Act caps residential deposits at 2 months' rent, but it applies only in states that have adopted it, and usually only to new agreements."}]}

_Escalation:_ {"level": "recommended", "reasons": ["A lawyer can help draft a formal legal notice that carries more weight if the landlord continues to ignore your requests."]}  _Citations:_ ['ICA1872-S73', 'LIM1963-ART55']

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
  "Bank transfer proof"
 ],
 "evidence_missing": [
  "Written communication history with landlord"
 ],
 "next_step": "Send a formal written demand (email/WhatsApp) asking for the refund and bills."
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

Subject: Demand for refund of security deposit for the premises at [[FILL: address of the rented flat]].

Dear Sir,

1. I am writing to you regarding the security deposit of Rs. 60,000/- (Rupees Sixty Thousand only) paid by me to you in relation to the tenancy of the premises located at [[FILL: address of the rented flat]].

2. The tenancy was governed by a registered rent agreement. As per our arrangement, I paid a monthly rent of Rs. 20,000/-.

3. I vacated the premises and handed over the keys to you on 31 August 2026. At the time of handing over possession, the premises were in good condition.

4. It has been over two months since I vacated the property. You have informed me of your intention to deduct Rs. 25,000/- from the security deposit towards painting and general damage. However, you have failed to provide any bills, invoices, or proof of expenditure to justify these deductions.

5. Under Section 73 of the Indian Contract Act, 1872, a party who suffers a loss due to a breach of contract is entitled to receive compensation. As there is no valid basis or proof provided for the deductions you claim, the withholding of my security deposit is unjustified.

6. I hereby call upon you to refund the balance amount of the security deposit, after any legitimate and documented deductions, within 15 days of the receipt of this notice. Please remit the amount to the following bank account:
Account Name: [[FILL: your bank account name]]
Bank Name: [[FILL: your bank name]]
Account Number: [[FILL: your bank account number]]
IFSC Code: [[FILL: your bank IFSC code]]

7. If you fail to comply with this demand within the stipulated period, I shall be constrained to initiate appropriate legal proceedings against you, including filing a civil suit for recovery of the amount with interest, at your sole risk, cost, and consequences.

Copy retained for record.

Sincerely,

[[FILL: your full name]]
[[FILL: your phone number]]
[[FILL: your email address]]

**Send instructions:** ["Print two copies of this notice and sign both.", "Send one copy to the landlord via Registered Post A.D. (Acknowledgement Due) from your nearest post office.", "Keep the original postal receipt and the tracking number safely.", "When the 'Acknowledgement Due' card returns signed by the landlord, staple it to your office copy as proof of delivery.", "If the landlord does not reply or pay within 15 days of receiving the notice, you may approach the District Legal Services Authority for pre-litigation mediation or consult a lawyer to file a civil suit for recovery."]

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
| draft_has_no_invented_fill | ✅ | 11 placeholders |
