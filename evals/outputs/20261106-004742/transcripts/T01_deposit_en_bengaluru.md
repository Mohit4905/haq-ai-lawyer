# T01_deposit_en_bengaluru
Group: core

## Turn 1

**User:** I moved out of my rented flat in Bengaluru on 31 August 2026 and handed over the keys the same day. I paid a deposit of Rs 60,000 by bank transfer, rent was 20,000. Landlord Mr. Ramesh Gowda says he'll cut 25,000 for painting and 'general damage' but hasn't shown any bills. It's been over 2 months. We had a registered rent agreement. What can I do?

**Haq** (groq/qwen/qwen3.8-27b, 7.9s):

You're in a reasonable position. You have a registered agreement and a bank-transfer receipt — that's solid proof. The landlord's main weakness: he claims ₹25,000 for painting and 'general damage' but hasn't shown any bills or a move-out inspection report. He needs to prove both the damage and the cost.

**Quick questions before I help further:**
1. How have you asked so far — calls, WhatsApp, email? Any written reply from him?
2. Does your agreement say anything about who pays for painting or deductions?

**Your options (cheapest → costliest):**
1. **Written demand** (WhatsApp/email) — state the amount, move-out date, bank details; ask for bills for any deduction. Free, do today.
2. **Legal notice** — formal letter giving ~15 days to refund or show bills. You can send it yourself; a lawyer can also send it for a fee.
3. **Lok Adalat / free legal aid** — apply through Karnataka DLSA or call NALSA 15100 (toll-free). Free.
4. **Civil suit** — file within 3 years (your deadline: 31 Aug 2029). A summary suit is possible since you have a written agreement. A lawyer helps here.

**My recommendation:** Send a clear written demand today (WhatsApp + email). If he doesn't respond in 7–10 days, we can draft a legal notice for you.

**Calculated by code:** {"deadlines": [{"label": "Approximate last date to sue for the deposit (3 years)", "date": "2029-08-31", "days_left": 1029, "status": "ok", "basis": "LIM1963-ART55", "note": "Limitation depends on the exact claim; confirm with legal aid before relying on it.", "user_deadline": true}], "derived": [{"label": "Deposit size", "value": "3.0 × monthly rent", "basis": "MTA2021-S11", "note": "The Model Tenancy Act caps residential deposits at 2 months' rent, but it applies only in states that have adopted it, and usually only to new agreements."}]}

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['ICA1872-S73', 'LIM1963-ART55', 'CPC1908-O37', 'FACT-LOKADALAT-PRELITIGATION', 'FACT-NALSA-HELPLINE']

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
  "proof_of_payment": true,
  "city_state": "Bengaluru, Karnataka",
  "other_party_name": "Mr. Ramesh Gowda"
 },
 "timeline": [
  {
   "date": "2026-08-31",
   "event": "Moved out, handed over keys"
  }
 ],
 "evidence_have": [
  "Registered rent agreement",
  "Bank transfer receipt for deposit"
 ],
 "evidence_missing": [
  "Move-out inspection report or photos",
  "Any written communication from landlord about deductions",
  "Copy of agreement clause on deductions/painting"
 ],
 "next_step": "Send a written demand (WhatsApp + email) to Mr. Ramesh Gowda stating the deposit amount, move-out date, bank details, and asking him to share bills for any claimed deduction within 7 days."
}
```

## Draft document

**LEGAL NOTICE**

**Mode of Sending:** By Registered Post A.D. / Speed Post

**Date:** [[FILL: date]]

**From:**

[Your Full Name]
[Your Current Address]
[City, State, PIN]

**To:**

Mr. Ramesh Gowda
[Landlord's Full Address]

**Subject:** Demand for Refund of Security Deposit – Rs 60,000

1. I entered into a registered rent agreement with Mr. Ramesh Gowda for the premises located at [[FILL: address of the flat]] in Bengaluru, Karnataka. The agreement was signed on [[FILL: date of agreement signing]] and I paid a security deposit of Rs 60,000 by bank transfer on [[FILL: date of deposit payment]].
2. I vacated the premises and handed over the keys to the landlord on 31 August 2026.
3. Mr. Gowda has claimed that Rs 25,000 will be deducted from my deposit for alleged painting and general damage. No bills, invoices or any written communication detailing these deductions have been provided to me.
4. I have not received any notice or statement from the landlord regarding the deductions, and it has been over two months since I vacated the premises.
5. I have retained copies of the registered rent agreement and the bank transfer receipt as evidence of the deposit payment.

**Legal Basis:**

Under the Model Tenancy Act, 2021 s.11, the security deposit must be refunded when the landlord takes back vacant possession, after deducting any amounts the tenant owes. The landlord has not provided any evidence of legitimate deductions, and therefore the full deposit is due. (MTA2021-S11)

Under the Indian Contract Act, 1872 s.73, a breach of contract entitles the aggrieved party to claim the loss caused by the breach. (ICA1872-S73)

**Demand:**

I demand the refund of the full security deposit amounting to Rs 60,000 within 15 days from the date of receipt of this notice. The refund should be made to the following bank account:

- Account Name: [[FILL: your account name]]
- Account Number: [[FILL: your account number]]
- IFSC Code: [[FILL: IFSC code]]

**Consequence of Non‑Compliance:**

If the full deposit is not refunded within the stipulated period, I will pursue lawful remedies, including filing a civil suit for recovery of the deposit with interest, or approaching the District Legal Services Authority for a Lok Adalat settlement, at your cost. (FACT-LOKADALAT-PRELITIGATION)

**Copy retained for record.**

Signature: ______________________

Name: [[FILL: your full name]]
Phone: [[FILL: your phone number]]
Email: [[FILL: your email address]]

**Send instructions:** ["1. Print the notice on a clean sheet of paper.\n2. Sign the notice and keep a photocopy for your records.\n3. Send the notice via Registered Post (A.D.) or Speed Post to the landlord’s address, and request a return receipt.\n4. Keep the tracking number and the proof of dispatch (receipt, e‑mail confirmation).\n5. If you do not receive a response within 15 days, consider filing a civil suit for recovery of the deposit with interest, or approach the District Legal Services Authority for a Lok Adalat settlement."]

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
| draft_has_no_invented_fill | ✅ | 10 placeholders |
