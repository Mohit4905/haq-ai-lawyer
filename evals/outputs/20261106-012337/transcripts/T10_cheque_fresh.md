# T10_cheque_fresh
Group: core

## Turn 1

**User:** My friend Arun Mehta borrowed Rs 2,00,000 from me last year and gave me a cheque dated 15 October 2026 to repay it. I deposited it on 20 October and my bank returned it on 27 October 2026 with the reason 'funds insufficient'. I got the return memo the same day. What should I do?

**Haq** (gemini/gemini-3.1-flash-lite, 8.02s):

I am sorry to hear about this. A cheque bounce is a serious matter, but you still have time to take action.

**Your situation:**
- You deposited the cheque on time.
- You have 20 days left to send a legal notice (deadline: 26 November 2026).

**Options:**
1. **Legal Demand Notice:** The first and most important step. You must send a formal notice to Arun Mehta, giving him 15 days to make the payment.
2. **Criminal Complaint:** If the payment is not received within 15 days, you can file a case in court.
3. **Settlement:** You can always discuss and reach a settlement between yourselves.

**Next step:**
You should first send a 'Legal Demand Notice'. Would you like me to prepare a draft for you?

*Note: I am not a lawyer. If the matter proceeds further, please consult a lawyer or call the free legal aid helpline at 15100.*

**Calculated by code:** {"deadlines": [{"label": "Cheque must be presented to the bank by (3-month validity)", "date": "2027-01-14", "days_left": 69, "status": "ok", "basis": "FACT-RBI-CHEQUE-VALIDITY", "note": "", "user_deadline": true}, {"label": "Send the legal demand notice by (30 days from bank's return memo)", "date": "2026-11-26", "days_left": 20, "status": "ok", "basis": "NIA1881-S138", "note": "Count from the day you got the bank's information; send by registered post AD/speed post and keep receipts.", "user_deadline": true}], "derived": []}

_Escalation:_ {"level": "recommended", "reasons": ["A lawyer is strongly advisable if you need to file a criminal complaint in court later."]}  _Citations:_ ['NIA1881-S138', 'NIA1881-S142-1', 'NIA1881-S147', 'FACT-NALSA-HELPLINE']

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
   "date": "2026-10-27",
   "event": "Received bank return memo for cheque bounce"
  }
 ],
 "evidence_have": [
  "Original cheque",
  "Bank return memo"
 ],
 "evidence_missing": [
  "Copy of the cheque",
  "Proof of debt (loan agreement or messages)"
 ],
 "next_step": "Draft a legal demand notice to be sent via registered post."
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

Subject: Demand for payment of Rs 2,00,000 regarding dishonoured cheque no. [[FILL: Cheque Number]]

Dear Sir,

1. I am writing to you regarding the loan of Rs 2,00,000 that I provided to you. To discharge this legally enforceable debt, you issued a cheque bearing number [[FILL: Cheque Number]], dated 15 October 2026, drawn on [[FILL: Name of your Bank and Branch]], for the amount of Rs 2,00,000.

2. I presented the said cheque for payment at my bank, [[FILL: Name of your Bank and Branch]], on 20 October 2026. 

3. However, the cheque was returned unpaid by your bank with the remark 'funds insufficient'. I received the bank return memo informing me of this dishonour on 27 October 2026.

4. Under Section 138 of the Negotiable Instruments Act, 1881, the dishonour of a cheque issued for the discharge of a legally enforceable debt is a criminal offence. 

5. I hereby call upon you to pay the sum of Rs 2,00,000 (Rupees Two Lakhs only) to me within 15 days of the receipt of this notice. You may make the payment via bank transfer to the following account:
   Account Name: [[FILL: Your Name]]
   Bank Name: [[FILL: Your Bank Name]]
   Account Number: [[FILL: Your Account Number]]
   IFSC Code: [[FILL: Your IFSC Code]]

6. Please note that if you fail to make the payment within the stipulated 15 days, I shall be constrained to initiate appropriate legal proceedings against you, including filing a criminal complaint under Section 138 read with Section 142 of the Negotiable Instruments Act, 1881, at your own risk, cost, and consequences.

Copy retained for record.

Sincerely,

[[FILL: Your Signature]]
[[FILL: Your Full Name]]

**Send instructions:** ["Print two copies of this notice. Sign both copies in blue or black ink.", "Send one copy to Arun Mehta via Registered Post A.D. or Speed Post. Ensure you get the postal receipt.", "Keep the original postal receipt and the tracking report safely; these are your proof of delivery.", "Wait for 15 days from the date Arun Mehta receives the notice (track this via the postal website).", "If he does not pay within those 15 days, you have one month from the end of that period to file a criminal complaint in the court having jurisdiction over your bank branch."]

## Automatic checks

| check | pass | detail |
|---|---|---|
| category | ✅ | got cheque_bounce |
| reply_language | ✅ | expected Latin, reply script Latin |
| fact:memo_received_date | ✅ | expected ~2026-10-27, got 2026-10-27 |
| fact:cheque_amount | ✅ | expected ~2, got 200000 |
| mentions:30 days|30-day|30‑day|30 din | ❌ |  |
| mentions:15 days|15-day|15‑day|15 din | ✅ |  |
| escalation<=recommended | ✅ | got recommended |
| deadline:NIA1881-S138 | ✅ | [{"label": "Cheque must be presented to the bank by (3-month validity)", "date": "2027-01-14", "days_left": 69, "status": "ok", "basis": "FACT-RBI-CHEQUE-VALIDI |
| no_unverified_law_shown | ✅ |  |
| draft_no_unverified_law | ✅ | [] |
| draft_has_no_invented_fill | ✅ | 12 placeholders |
