# T01_deposit_en_bengaluru
Group: core

## Turn 1

**User:** I moved out of my rented flat in Bengaluru on 31 August 2026 and handed over the keys the same day. I paid a deposit of Rs 60,000 by bank transfer, rent was 20,000. Landlord Mr. Ramesh Gowda says he'll cut 25,000 for painting and 'general damage' but hasn't shown any bills. It's been over 2 months. We had a registered rent agreement. What can I do?

**Haq** (groq/qwen/qwen3.8-27b, 8.98s):

You handed over keys on 31 Aug 2026 and the landlord is holding ₹25,000 without showing any bills. From what you've told me, the main conditions for getting your money back seem to be met — you have a registered agreement and bank-transfer proof. The landlord's claim of 'general damage' without bills is a weak spot on his side.

**Your options (cheapest → formal):**

1. **Written demand** (WhatsApp/email) — state the amount, ask for bills, give a deadline. Free, same day.
2. **Legal notice** demanding refund within ~15 days. You can send it yourself; a lawyer's letter carries more weight. Cost: a few hundred to a couple of thousand for drafting.
3. **Free Lok Adalat / legal aid** via District Legal Services Authority (DLSA) or call **NALSA 15100** (toll-free). No court fee, settlement-focused.
4. **Civil suit** for recovery (within 3 years, so by ~31 Aug 2029). A summary suit may be possible since you have a written agreement — faster than a regular suit. A lawyer helps here.

**My recommendation:** Send a clear written demand today (WhatsApp is fine). State: deposit ₹60,000, keys handed 31 Aug 2026, no bills provided for the ₹25,000 deduction, refund ₹35,000 to [your bank] within 7 days. Keep screenshots.

Two quick questions:
- How have you asked him so far — calls, WhatsApp, in person?
- Do you have photos of the flat's condition when you moved out?

**Calculated by code:** {"deadlines": [{"label": "Approximate last date to sue for the deposit (3 years)", "date": "2029-08-31", "days_left": 1029, "status": "ok", "basis": "LIM1963-ART55", "note": "Limitation depends on the exact claim; confirm with legal aid before relying on it.", "user_deadline": true}], "derived": [{"label": "Deposit size", "value": "3.0 × monthly rent", "basis": "MTA2021-S11", "note": "The Model Tenancy Act caps residential deposits at 2 months' rent, but it applies only in states that have adopted it, and usually only to new agreements."}]}

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['LIM1963-ART55', 'CPC1908-O37', 'FACT-LOKADALAT-PRELITIGATION', 'FACT-NALSA-HELPLINE', 'ICA1872-S73', 'FACT-MTA-STATE-ADOPTION']

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
  "city_state": "Bengaluru, Karnataka",
  "other_party_name": "Ramesh Gowda",
  "summary": "Landlord withholding ₹25,000 from ₹60,000 deposit, no bills provided, over 2 months since move-out.",
  "proof_of_payment": "bank transfer"
 },
 "timeline": [
  {
   "date": "2026-08-31",
   "event": "Keys handed over, possession returned to landlord"
  }
 ],
 "evidence_have": [
  "Registered rent agreement",
  "Bank transfer record for ₹60,000 deposit"
 ],
 "evidence_missing": [
  "Photos of flat condition at move-out",
  "Record of all communications with landlord (calls, WhatsApp, emails)",
  "Any written demand already sent"
 ],
 "next_step": "Send a written demand (WhatsApp/email) to landlord stating amount owed, no bills provided, and a 7-day deadline for refund of ₹35,000."
}
```

## Draft document

LEGAL NOTICE

By Registered Post A.D. / Speed Post

Date: [[FILL: date]]

From:
[[FILL: Your Full Name]]
[[FILL: Your Current Address]]
[[FILL: Your Phone Number]]

To:
Mr. Ramesh Gowda
[[FILL: Landlord's Full Address]]

Subject: Notice for refund of security deposit regarding the premises at [[FILL: Address of the rented flat]].

Dear Sir,

1. I am writing to you regarding the tenancy of the premises located at [[FILL: Address of the rented flat]], which I vacated on 31 August 2026.

2. As per our registered rent agreement, I had paid a security deposit of ₹60,000 (Rupees Sixty Thousand only) to you via bank transfer.

3. On 31 August 2026, I handed over the peaceful possession of the premises and the keys to you. At that time, the property was in good condition, consistent with normal wear and tear.

4. It has been over two months since I vacated the premises. You have informed me of your intention to deduct ₹25,000 from the deposit for painting and general damage. However, you have failed to provide any invoices, bills, or proof of expenditure to justify these deductions.

5. Under Section 73 of the Indian Contract Act, 1872, you are obligated to return the security deposit upon the termination of the tenancy, subject only to legitimate deductions for actual damages, which must be substantiated.

6. I hereby demand that you refund the balance amount of ₹35,000 (Rupees Thirty-Five Thousand only) to me within 15 days of the receipt of this notice. Please transfer the amount to the following bank account:
   Bank Name: [[FILL: Your Bank Name]]
   Account Holder Name: [[FILL: Your Name]]
   Account Number: [[FILL: Your Account Number]]
   IFSC Code: [[FILL: Your IFSC Code]]

7. If you fail to comply with this demand within the stipulated period, I shall be constrained to initiate appropriate legal proceedings against you for recovery of the amount, including interest and legal costs, by approaching the competent court or the relevant legal forum.

Copy retained for record.

Sincerely,

[[FILL: Your Name]]
[[FILL: Your Phone Number]]
[[FILL: Your Email Address]]

**Send instructions:** ["Print two copies of this notice. Sign both copies.", "Send one copy to Mr. Ramesh Gowda via 'Registered Post A.D.' (Acknowledgement Due) or 'Speed Post' from your nearest post office. This provides you with a tracking number and proof of delivery.", "Keep the second copy and the original postal receipt safely with your records.", "If you receive the 'Acknowledgement Due' card back in the mail, staple it to your copy of the notice as proof that he received it.", "If he does not pay within 15 days of receiving the notice, you may consider filing a civil suit for recovery or approaching the local District Legal Services Authority for mediation/Lok Adalat.", "You can contact the NALSA helpline at 15100 for further guidance on how to proceed if the landlord continues to withhold your money."]

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
| draft_has_no_invented_fill | ✅ | 11 placeholders |
