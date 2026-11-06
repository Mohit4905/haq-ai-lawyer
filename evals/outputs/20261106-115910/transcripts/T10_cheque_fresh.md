# T10_cheque_fresh
Group: core

## Turn 1

**User:** My friend Arun Mehta borrowed Rs 2,00,000 from me last year and gave me a cheque dated 15 October 2026 to repay it. I deposited it on 20 October and my bank returned it on 27 October 2026 with the reason 'funds insufficient'. I got the return memo the same day. What should I do?

**Haq** (gemini/gemini-3.1-flash-lite, 34.85s):

Namaste. I understand this is a stressful situation, especially when it involves a friend. Since you received the bank's return memo on 27 October 2026, you are well within the legal timeline to act. Under the Negotiable Instruments Act, a cheque bounce for insufficient funds is a serious matter, and the law provides a specific process to recover your money.

**Your legal position:**
Your case appears to be procedurally sound because you presented the cheque within the 3-month validity period and the reason for dishonour ('funds insufficient') is covered under the law. You have a strong basis to initiate the formal recovery process, provided you send the legal demand notice within 30 days of receiving the bank's memo.

**Law you can cite:**
*   **Section 138, Negotiable Instruments Act, 1881:** This makes cheque bouncing a criminal offence if the cheque was for a legally enforceable debt and was presented within its validity.
*   **Section 143A, Negotiable Instruments Act, 1881:** This allows the court to order the person who issued the cheque to pay you interim compensation of up to 20% of the cheque amount during the trial.
*   **Section 147, Negotiable Instruments Act, 1881:** This confirms that you can settle the matter amicably with your friend at any stage, which is often the fastest way to get your money back.

**What to do now:**
1.  **Send a formal legal demand notice:** This must be sent via registered post/speed post by 26 November 2026. This is your most important next step.
2.  **Wait 15 days:** After your friend receives the notice, they have 15 days to pay the amount.
3.  **File a complaint:** If they still do not pay, you can file a criminal complaint in the court where your bank branch is located.
4.  **Free Legal Aid:** If you need help drafting the notice or have questions about the process, call the NALSA helpline at 15100.

I can help you draft the legal demand notice now. Would you like me to prepare that for you? 

**I need from you:**
1. What is your city and state (so I can help you identify the correct jurisdiction)?
2. Do you have a copy of the original loan agreement or any written proof (like WhatsApp messages) confirming the loan?

**Calculated by code:** {"deadlines": [{"label": "Cheque must be presented to the bank by (3-month validity)", "date": "2027-01-14", "days_left": 69, "status": "ok", "basis": "FACT-RBI-CHEQUE-VALIDITY", "note": "", "user_deadline": true}, {"label": "Send the legal demand notice by (30 days from bank's return memo)", "date": "2026-11-26", "days_left": 20, "status": "ok", "basis": "NIA1881-S138", "note": "Count from the day you got the bank's information; send by registered post AD/speed post and keep receipts.", "user_deadline": true}], "derived": []}

_Escalation:_ {"level": "recommended", "reasons": ["While you can send the notice yourself, filing a court case requires a lawyer to ensure all procedures are followed correctly."]}  _Citations:_ ['NIA1881-S138', 'NIA1881-S143A', 'NIA1881-S147']

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
  "Cheque return memo",
  "Original cheque"
 ],
 "evidence_missing": [
  "Proof of loan (agreement/messages)",
  "Copy of the bank's return memo"
 ],
 "next_step": "Draft and send the legal demand notice via registered post."
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

Subject: Legal notice for dishonour of cheque no. [[FILL: Cheque Number]] dated 15 October 2026 for Rs 2,00,000.

Dear Sir,

1. I am writing to you regarding the loan of Rs 2,00,000 given by me to you. To discharge this legally enforceable debt, you issued a cheque bearing number [[FILL: Cheque Number]], dated 15 October 2026, drawn on [[FILL: Name of Arun Mehta's Bank and Branch]], in my favour.

2. I presented the said cheque for payment through my bank, [[FILL: Name of Your Bank and Branch]], on 20 October 2026. However, the cheque was returned unpaid by your bank with the remark 'funds insufficient'.

3. I received the bank's return memo regarding the dishonour of the cheque on 27 October 2026.

4. Under Section 138 of the Negotiable Instruments Act, 1881, the dishonour of a cheque issued for the discharge of a legally enforceable debt is a criminal offence. 

5. I hereby call upon you to pay the sum of Rs 2,00,000 (Rupees Two Lakhs only) to me within 15 days from the date of receipt of this notice. Payment may be made via bank transfer to the following account: 
Account Name: [[FILL: Your Account Name]]
Bank Name: [[FILL: Your Bank Name]]
Account Number: [[FILL: Your Account Number]]
IFSC Code: [[FILL: Your IFSC Code]]

6. Please note that if you fail to make the payment within the stipulated period of 15 days, I shall be constrained to initiate appropriate legal proceedings against you, including filing a criminal complaint under Section 138 read with Section 142 of the Negotiable Instruments Act, 1881, at your risk and cost.

Copy retained for record.

Sincerely,

[[FILL: Your Signature]]
[[FILL: Your Printed Name]]

**Send instructions:** ["Print two copies of this notice on plain paper and sign both.", "Send one copy to Arun Mehta via Registered Post A.D. or Speed Post. Keep the original postal receipt safely.", "Keep the second copy for your own records, attached to the original postal receipt and the cheque return memo.", "Wait for 15 days from the date Arun Mehta receives the notice (track the delivery status online using the postal tracking number).", "If he does not pay within those 15 days, you have one month from the end of that 15-day period to file a criminal complaint in the court having jurisdiction over your bank branch."]

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
| draft_has_no_invented_fill | ✅ | 14 placeholders |
