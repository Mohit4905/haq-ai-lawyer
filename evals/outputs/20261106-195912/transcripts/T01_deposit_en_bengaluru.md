# T01_deposit_en_bengaluru
Group: core

## Turn 1

**User:** I moved out of my rented flat in Bengaluru on 31 August 2026 and handed over the keys the same day. I paid a deposit of Rs 60,000 by bank transfer, rent was 20,000. Landlord Mr. Ramesh Gowda says he'll cut 25,000 for painting and 'general damage' but hasn't shown any bills. It's been over 2 months. We had a registered rent agreement. What can I do?

**Haq** (gemini/gemini-3.1-flash-lite, 33.52s):

Your case is strong. A landlord cannot deduct a security deposit without any proof or bills. Under the agreement, a tenant is not responsible for 'normal wear and tear' (natural wear resulting from living in the property), and painting costs can only be deducted if the agreement explicitly states that you are required to paint the flat before moving out. Deducting 25,000 without bills is wrong.

**My view:** Your case is solid because you have a registered agreement and you made payments via bank transfer. The landlord deducting money by citing 'general damage' is not legally valid; they must provide proof (bills) for every deduction. It has been 2 months, so you now need to apply pressure formally.

**Law on your side:**
*   **Contract Law:** Your agreement is a contract. If the landlord is deducting money without any valid reason or proof, it is a breach of contract. You can demand proof of 'actual loss' from them.
*   **Burden of Proof:** If the matter goes to court, the landlord will have to prove that you caused the damage and that the cost is indeed 25,000.

**What they will say, and your answer:**
*   *They will say:* "Painting and repair costs are standard."
*   *Your answer:* "The agreement allows for 'normal wear and tear.' If you have carried out repairs, please show me the genuine bills and the photos taken at the time of move-out."

**What I would do:**
1.  **Today:** Send them a formal email or WhatsApp message (if you haven't already) clearly stating that you handed over possession on 31 August and have not yet received the full refund. Ask them for the bills.
2.  **If there is no response within 7 days:** Send a 'Legal Notice' giving them 15 days to process the refund, warning them of legal action otherwise. I can help you draft this.

**I need from you:**
1. Have you sent any written request (email/WhatsApp) for the refund so far?
2. Do you have photos or videos of the flat from the time of move-out?

**Law you can cite (checked against official sources):**
- **Section 73, Indian Contract Act, 1872**: If someone breaks a contract with you, you can claim money for the loss it caused.
- **Article 55, Limitation Act, 1963**: A suit for compensation for breach of a contract (written or implied), where no other article covers it specifically, must be filed within 3 years.

**Calculated by code:** {"deadlines": [{"label": "Approximate last date to sue for the deposit (3 years)", "date": "2029-08-31", "days_left": 1029, "status": "ok", "basis": "LIM1963-ART55", "note": "Limitation depends on the exact claim; confirm with legal aid before relying on it.", "user_deadline": true}], "derived": [{"label": "Deposit size", "value": "3.0 × monthly rent", "basis": "MTA2021-S11", "note": "The Model Tenancy Act caps residential deposits at 2 months' rent, but it applies only in states that have adopted it, and usually only to new agreements."}]}

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['ICA1872-S73', 'LIM1963-ART55']

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
  "Bank transfer proof for deposit"
 ],
 "evidence_missing": [
  "Photos/videos of flat at move-out",
  "Written communication asking for refund"
 ],
 "next_step": "Send a formal written demand for the deposit refund via email/WhatsApp."
}
```

## Draft document

LEGAL NOTICE

By Registered Post A.D.

Date: [[FILL: date of sending]]

From:
[[FILL: your full name]]
[[FILL: your current address]]

To:
Mr. Ramesh Gowda
[[FILL: landlord's full address]]

Subject: Demand for refund of security deposit for the premises at [[FILL: address of the rented property]].

Dear Sir,

1. I am writing to you regarding the tenancy of the premises located at [[FILL: address of the rented property]], which I vacated on 31 August 2026.

2. As per our registered rent agreement, I had paid a security deposit of Rs. 60,000/- to you via bank transfer at the commencement of the tenancy.

3. On 31 August 2026, I handed over vacant possession of the premises and returned the keys to you. At that time, the property was in good condition, consistent with normal wear and tear.

4. It has been over two months since I vacated the premises, and the security deposit has not been refunded. You have verbally claimed a deduction of Rs. 25,000/- for painting and general damage; however, you have failed to provide any invoices, bills, or evidence justifying these deductions.

5. Under Section 73 of the Indian Contract Act, 1872, you are obligated to compensate for the loss caused by the breach of contract, which includes the failure to refund the deposit as agreed.

6. I hereby demand that you refund the balance of the security deposit, amounting to Rs. 60,000/- (or the undisputed portion thereof), within 15 days of receiving this notice. Please remit the amount to the following bank account:

[[FILL: your bank details (account name, number, bank, IFSC)]]

7. If you fail to comply with this demand within the stipulated period, I shall be constrained to initiate appropriate legal proceedings, including filing a civil suit for recovery of the amount with interest, at your sole risk, cost, and consequence.

Copy retained for record.

Sincerely,

[[FILL: your full name]]
[[FILL: your phone and email]]

**Send instructions:** ["Print two copies of the notice on plain paper and sign both.", "Send one copy to the landlord via 'Registered Post A.D.' (Acknowledgement Due) from your nearest post office. This provides you with a tracking number and a signed receipt when they receive it.", "Keep the second copy and the original postal receipt safely with your rent agreement and bank transfer proofs.", "If you do not receive a response or payment within 15 days of the landlord receiving the notice, you may consult a local lawyer or contact the nearest District Legal Services Authority (DLSA) to inquire about filing a civil suit or seeking pre-litigation mediation."]

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
| draft_has_no_invented_fill | ✅ | 7 placeholders |
