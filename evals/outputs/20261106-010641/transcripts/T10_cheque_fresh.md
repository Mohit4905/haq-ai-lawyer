# T10_cheque_fresh
Group: core

## Turn 1

**User:** My friend Arun Mehta borrowed Rs 2,00,000 from me last year and gave me a cheque dated 15 October 2026 to repay it. I deposited it on 20 October and my bank returned it on 27 October 2026 with the reason 'funds insufficient'. I got the return memo the same day. What should I do?

**Haq** (gemini/gemini-3.1-flash-lite, 16.84s):

Arun Mehta's cheque bouncing is a serious matter. Under section 138 of the Negotiable Instruments Act, 1881, a cheque bounce is an offence if it was issued for a legally enforceable debt (such as a loan).

You currently have 20 days (until 26 November 2026) to send a legal notice. Follow this process:

1. **Legal Demand Notice:** You must send a formal notice to Arun. In this, you must give him 15 days to make the payment.
2. **Wait & File:** If the payment is not received within 15 days, you can file a criminal complaint in court.
3. **Settlement:** You can opt for a settlement (compounding) at any time.

**Next Step:** You should immediately draft a 'Legal Demand Notice' and send it via registered post. Would you like me to draft this notice for you?

**Calculated by code:** {"deadlines": [{"label": "Cheque must be presented to the bank by (3-month validity)", "date": "2027-01-14", "days_left": 69, "status": "ok", "basis": "FACT-RBI-CHEQUE-VALIDITY", "note": "", "user_deadline": true}, {"label": "Send the legal demand notice by (30 days from bank's return memo)", "date": "2026-11-26", "days_left": 20, "status": "ok", "basis": "NIA1881-S138", "note": "Count from the day you got the bank's information; send by registered post AD/speed post and keep receipts.", "user_deadline": true}], "derived": []}

_Escalation:_ {"level": "recommended", "reasons": ["While you can send the notice yourself, filing a criminal complaint in court requires legal expertise."]}  _Citations:_ ['NIA1881-S138', 'NIA1881-S142-1', 'NIA1881-S147']

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
   "event": "Cheque dishonoured and memo received"
  }
 ],
 "evidence_have": [
  "Original cheque",
  "Bank return memo"
 ],
 "evidence_missing": [
  "Proof of loan (loan agreement or messages)",
  "Postal receipts for notice"
 ],
 "next_step": "Draft a legal demand notice to be sent via registered post."
}
```

## Draft document

LEGAL NOTICE
By Registered Post A.D. / Speed Post
Date: [[FILL: Date of sending]]

From:
[[FILL: Your Full Name]]
[[FILL: Your Full Address]]
[[FILL: Your Phone Number]]

To:
Arun Mehta
[[FILL: Arun Mehta's Full Address]]

Subject: Notice for demand of payment regarding dishonoured cheque of Rs 2,00,000.

Dear Sir,

1. I am writing to you regarding the loan of Rs 2,00,000 (Rupees Two Lakhs only) that I provided to you. To discharge this legally enforceable debt, you issued a cheque bearing number [[FILL: Cheque Number]] dated 15 October 2026, drawn on [[FILL: Name of Bank and Branch]], in my favour.

2. I presented the said cheque for payment through my bank on 20 October 2026. However, the cheque was returned unpaid by your bank with the remark 'funds insufficient'.

3. I received the bank return memo informing me of this dishonour on 27 October 2026.

4. Under Section 138 of the Negotiable Instruments Act, 1881, the dishonour of a cheque issued for the discharge of a legally enforceable debt is a criminal offence. 

5. I hereby call upon you to pay the sum of Rs 2,00,000 (Rupees Two Lakhs only) to me within 15 days from the date of receipt of this notice. Payment may be made via bank transfer to the following account: [[FILL: Your Bank Name]], Account Number: [[FILL: Your Account Number]], IFSC: [[FILL: Your IFSC Code]].

6. Please note that if you fail to make the payment within the stipulated 15 days, I shall be constrained to initiate appropriate legal proceedings against you, including filing a criminal complaint under Section 138 read with Section 142 of the Negotiable Instruments Act, 1881, at your risk and cost.

Copy retained for record.

Sincerely,

[[FILL: Your Signature]]
[[FILL: Your Full Name]]
[[FILL: Your Phone Number]]
[[FILL: Your Email Address]]

**Send instructions:** ["Print two copies of this notice. Sign both copies in blue or black ink.", "Send one copy to Arun Mehta via Registered Post A.D. or Speed Post. Keep the original postal receipt safely.", "Keep the second copy for your own records, attached to the original postal receipt and the bank return memo.", "Wait for 15 days from the date Arun Mehta receives the notice (track the delivery status online using the postal tracking number).", "If you do not receive payment after 15 days, you have one month to file a criminal complaint in the court having jurisdiction over your bank branch."]

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
