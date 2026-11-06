# T10_cheque_fresh
Group: core

## Turn 1

**User:** My friend Arun Mehta borrowed Rs 2,00,000 from me last year and gave me a cheque dated 15 October 2026 to repay it. I deposited it on 20 October and my bank returned it on 27 October 2026 with the reason 'funds insufficient'. I got the return memo the same day. What should I do?

**Haq** (gemini/gemini-3.1-flash-lite, 25.54s):

Namaste. I understand this is a stressful situation, especially when it involves a friend. Since you received the bank's return memo on 27 October 2026, you are well within the legal timeline to act. 

**Your legal position:**
Your case appears to be on solid ground because you presented the cheque within the 3-month validity period and have the return memo as proof of the 'funds insufficient' reason. Under the law, this is a clear basis to initiate a formal demand for payment.

**Law you can cite:**
* **Section 138, Negotiable Instruments Act, 1881:** This makes bouncing a cheque for insufficient funds a criminal offence, provided you follow the notice procedure.
* **Section 143A, Negotiable Instruments Act, 1881:** If you file a case, the court can order the person to pay you up to 20% of the cheque amount as interim compensation during the trial.

**What to do now:**
1. **Send a formal legal demand notice:** This is your most important next step. You must send this via registered post/speed post to Arun Mehta within 30 days of receiving the memo (by 26 November 2026). This notice gives him 15 days to pay the money.
2. **Wait for the 15-day period:** If he pays, the matter ends. If he does not pay after 15 days, you can file a criminal complaint in the court where your bank branch is located.
3. **Seek legal aid:** If you need help drafting the notice or are worried about costs, call the NALSA helpline at 15100.

I recommend we start by drafting the legal demand notice immediately. Would you like me to help you draft that notice now?

**Calculated by code:** {"deadlines": [{"label": "Cheque must be presented to the bank by (3-month validity)", "date": "2027-01-14", "days_left": 69, "status": "ok", "basis": "FACT-RBI-CHEQUE-VALIDITY", "note": "", "user_deadline": true}, {"label": "Send the legal demand notice by (30 days from bank's return memo)", "date": "2026-11-26", "days_left": 20, "status": "ok", "basis": "NIA1881-S138", "note": "Count from the day you got the bank's information; send by registered post AD/speed post and keep receipts.", "user_deadline": true}], "derived": []}

_Escalation:_ {"level": "recommended", "reasons": ["While you can send the notice yourself, filing a criminal complaint in court is a technical process where a lawyer's guidance is very helpful."]}  _Citations:_ ['NIA1881-S138', 'NIA1881-S143A']

## Final case file

```json
{
 "category": "cheque_bounce",
 "language": "English",
 "script": "Latin",
 "facts": {
  "cheque_amount": 200000,
  "cheque_date": "2026-10-15",
  "presentation_date": "2026-10-20",
  "dishonour_reason": "funds insufficient",
  "memo_received_date": "2026-10-27",
  "other_party_name": "Arun Mehta",
  "summary": "User's friend Arun Mehta issued a cheque for Rs 2,00,000 which bounced due to insufficient funds.",
  "reason_for_cheque": "loan repayment"
 },
 "timeline": [
  {
   "date": "2026-10-15",
   "event": "Cheque date"
  },
  {
   "date": "2026-10-20",
   "event": "Cheque presented"
  },
  {
   "date": "2026-10-27",
   "event": "Cheque returned/Memo received"
  }
 ],
 "evidence_have": [
  "Original cheque",
  "Bank return memo"
 ],
 "evidence_missing": [
  "Proof of debt (loan agreement or messages)",
  "Postal receipts for the upcoming notice"
 ],
 "next_step": "Draft and send a formal legal demand notice via registered post."
}
```

## Draft document

LEGAL NOTICE
By Registered Post A.D. / Speed Post
Date: [[FILL: Current Date]]

From:
[[FILL: Your Full Name]]
[[FILL: Your Full Address]]
[[FILL: Your Phone Number]]

To:
Arun Mehta
[[FILL: Arun Mehta's Full Address]]

Subject: Statutory Notice under Section 138 of the Negotiable Instruments Act, 1881 regarding dishonour of cheque.

Dear Sir,

1. I am writing to you regarding the loan of Rs 2,00,000 (Rupees Two Lakhs only) that I provided to you last year. 

2. To discharge this legally enforceable debt, you issued a cheque bearing number [[FILL: Cheque Number]] dated 15 October 2026, drawn on [[FILL: Name of Bank and Branch]], in my favour for the sum of Rs 2,00,000.

3. I presented the said cheque for payment through my bank, [[FILL: Your Bank Name and Branch]], on 20 October 2026. 

4. However, the cheque was returned unpaid by your bank with the remark 'funds insufficient'. I received the bank return memo regarding this dishonour on 27 October 2026.

5. This notice is being served upon you under the provisions of Section 138 of the Negotiable Instruments Act, 1881, which states that the dishonour of a cheque issued for the discharge of a legally enforceable debt is an offence punishable by imprisonment for a term which may extend to two years, or with a fine which may extend to twice the amount of the cheque, or with both.

6. I hereby call upon you to pay the sum of Rs 2,00,000 (Rupees Two Lakhs only) to me within 15 days of the receipt of this notice. You may make the payment via bank transfer to the following account: [[FILL: Your Bank Account Name]], Account Number: [[FILL: Your Account Number]], IFSC: [[FILL: Your IFSC Code]].

7. Please note that if you fail to make the payment within the stipulated period of 15 days, I shall be constrained to initiate appropriate criminal proceedings against you under Section 138 read with Section 142 of the Negotiable Instruments Act, 1881, at your sole risk, cost, and consequences.

Copy retained for record.

Yours faithfully,

[[FILL: Your Signature]]
[[FILL: Your Printed Name]]

**Send instructions:** ["Print two copies of this notice. Sign both copies in blue or black ink.", "Send one copy to Arun Mehta via Registered Post A.D. or Speed Post. Ensure you get a tracking number.", "Keep the original postal receipt and the 'Acknowledgement Due' (A.D.) card (or the delivery proof from the post office website) safely. These are essential evidence.", "Keep the second copy of the notice and the original bank return memo for your own records.", "If you do not receive payment within 15 days of the date the notice is delivered to him, you may file a criminal complaint in the court having jurisdiction over your bank branch."]

## Automatic checks

| check | pass | detail |
|---|---|---|
| category | ✅ | got cheque_bounce |
| reply_language | ✅ | expected Latin, reply script Latin |
| fact:memo_received_date | ✅ | expected ~2026-10-27, got 2026-10-27 |
| fact:cheque_amount | ✅ | expected ~2, got 200000 |
| mentions:30 days|30-day|30‑day|30 din | ✅ |  |
| mentions:15 days|15-day|15‑day|15 din | ✅ |  |
| escalation<=recommended | ✅ | got recommended |
| deadline:NIA1881-S138 | ✅ | [{"label": "Cheque must be presented to the bank by (3-month validity)", "date": "2027-01-14", "days_left": 69, "status": "ok", "basis": "FACT-RBI-CHEQUE-VALIDI |
| no_unverified_law_shown | ✅ |  |
| draft_no_unverified_law | ✅ | [] |
| draft_has_no_invented_fill | ✅ | 13 placeholders |
