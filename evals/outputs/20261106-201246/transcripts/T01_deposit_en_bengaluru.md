# T01_deposit_en_bengaluru
Group: core

## Turn 1

**User:** I moved out of my rented flat in Bengaluru on 31 August 2026 and handed over the keys the same day. I paid a deposit of Rs 60,000 by bank transfer, rent was 20,000. Landlord Mr. Ramesh Gowda says he'll cut 25,000 for painting and 'general damage' but hasn't shown any bills. It's been over 2 months. We had a registered rent agreement. What can I do?

**Haq** (gemini/gemini-3.1-flash-lite, 48.14s):

Your case is strong because the landlord is deducting the deposit without any proof. According to the law, a landlord can only deduct money for 'actual damage' (which exceeds normal wear and tear), and the burden of proof lies with them—meaning they must provide bills. They cannot deduct money simply by claiming there was 'painting' or 'damage'.

**My view:**
The landlord deducting 25,000 without bills is illegal. Your agreement is registered, which is a huge plus point for you. You should immediately send a formal notice asking for the bills and demanding a refund. If they cannot produce the bills, they must return the full amount.

**Law on your side:**
*   **Contractual Obligation:** Your agreement is a contract. If there is no specific clause for 'painting charges' in the agreement, the landlord cannot deduct them.
*   **Burden of Proof:** In civil law, if a deduction is being made, the proof (bills/invoices) must be provided by the landlord. A deduction without proof is arbitrary.

**What they will say, and your answer:**
*   *Landlord:* "Painting and repair costs are inevitable." -> *Your answer:* "Please show me the bills and photos of the repairs that were taken after I moved out. Without valid bills, I cannot accept this deduction."

**What I would do:**
1.  **Today:** Send a formal email or WhatsApp message (if you haven't already) clearly stating when you handed over the keys and that you have not yet received your refund. Demand the bills.
2.  **In 15 days:** If they do not respond or provide the bills, send a 'Legal Notice' (I can help you draft one). This will put pressure on them.

**I need from you:**
1. Do you have photos or videos of the flat from the time of move-out that show it was in good condition?
2. Have you made any written communication (email/WhatsApp) regarding the refund yet?

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
  "Bank transfer proof of deposit"
 ],
 "evidence_missing": [
  "Photos/videos of flat condition at move-out",
  "Copy of the registered rent agreement"
 ],
 "next_step": "Send a formal written demand for the refund and bills via email/WhatsApp."
}
```

## Draft document

LEGAL NOTICE

By Registered Post A.D. / Speed Post / Email

Date: [[FILL: date of notice]]

From:
[[FILL: your full name]]
[[FILL: your current address]]

To:
Mr. Ramesh Gowda
[[FILL: landlord's full address]]

Subject: Demand for refund of security deposit for premises at [[FILL: address of the rented property]].

Dear Sir,

1. I am writing to you regarding the tenancy of the premises located at [[FILL: address of the rented property]], which I vacated on 31 August 2026.

2. Upon the commencement of our tenancy, I paid a security deposit of Rs. 60,000/- via bank transfer. This was governed by our registered rent agreement.

3. On 31 August 2026, I handed over vacant possession and the keys of the premises to you. At that time, the property was in good condition, consistent with normal wear and tear.

4. It has been over two months since I vacated the premises, yet the security deposit has not been refunded. You have informed me of your intention to deduct Rs. 25,000/- for painting and general damages; however, you have failed to provide any bills, invoices, or proof of such expenses to justify this deduction.

5. Under the Indian Contract Act, 1872, specifically section 73, I am entitled to claim compensation for the loss caused by the breach of our agreement regarding the refund of the deposit.

6. I hereby demand that you refund the balance of the security deposit, amounting to Rs. 60,000/- (or the undisputed amount if you provide valid, itemized proof of legitimate deductions), within 15 days of receiving this notice. Please transfer the amount to the following account: [[FILL: your bank details (account name, number, bank, IFSC)]].

7. If you fail to comply with this request within the specified period, I shall be constrained to initiate appropriate legal proceedings, including a civil suit for recovery of the amount with interest, at your cost and risk. I may also approach the local authorities for mediation or legal assistance.

Copy retained for record.

Sincerely,

[[FILL: your full name]]
[[FILL: your phone and email]]

**Send instructions:** ["Print two copies of the notice and sign both.", "Send one copy to the landlord via Registered Post A.D. (Acknowledgement Due) so you have proof of delivery.", "Keep the second copy and the postal receipt safely with your records.", "If you have the landlord's email address, send a scanned copy of the signed notice via email as well.", "If the landlord does not respond within 15 days, consider contacting the NALSA helpline (15100) or visiting your local District Legal Services Authority to inquire about pre-litigation mediation."]

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
