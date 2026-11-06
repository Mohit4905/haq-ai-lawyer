# T10_cheque_fresh
Group: core

## Turn 1

**User:** My friend Arun Mehta borrowed Rs 2,00,000 from me last year and gave me a cheque dated 15 October 2026 to repay it. I deposited it on 20 October and my bank returned it on 27 October 2026 with the reason 'funds insufficient'. I got the return memo the same day. What should I do?

**Haq** (gemini/gemini-3.1-flash-lite, 31.79s):

Arun Mehta's cheque bouncing is a serious matter, and now is the right time for you to take action. Your case is strong because the cheque was deposited within the valid timeframe and the reason is 'funds insufficient', which falls under the Negotiable Instruments Act.

**My view:**
This is a clear-cut case. According to the law, a cheque bounce is a criminal offence if it was issued for a legally enforceable debt (money that is owed back). You have 30 days from 27 October 2026 to send a legal notice. Do not delay this, as sending a notice is mandatory before filing a court case.

**Law on your side:**
*   **Section 138, Negotiable Instruments Act, 1881:** A cheque bounce is an offence. You must send a notice giving them 15 days to make the payment.
*   **Section 142, Negotiable Instruments Act, 1881:** If they do not make the payment within 15 days, you can file a complaint in court.

**What they will say, and your answer:**
*   Arun might say, "Give me some more time, I will pay." Your answer should be: "I am sending a legal notice; if you make the payment, the matter will be resolved, but the legal process will not stop until the money is in the account."

**What I would do:**
1.  **Today:** Draft a formal legal notice clearly stating that they must make the payment within 15 days, or you will take legal action.
2.  **Next step:** Send the notice via 'Registered Post AD' or 'Speed Post' and keep the receipt safe. If there is no response or payment within 15 days, we will prepare for a court case.

**I need from you:**
1. Do you have any written agreement or message that can prove this was a loan?
2. In which city is your bank branch located?

**Calculated by code:** {"deadlines": [{"label": "Cheque must be presented to the bank by (3-month validity)", "date": "2027-01-14", "days_left": 69, "status": "ok", "basis": "FACT-RBI-CHEQUE-VALIDITY", "note": "", "user_deadline": true}, {"label": "Send the legal demand notice by (30 days from bank's return memo)", "date": "2026-11-26", "days_left": 20, "status": "ok", "basis": "NIA1881-S138", "note": "Count from the day you got the bank's information; send by registered post AD/speed post and keep receipts.", "user_deadline": true}], "derived": []}

_Escalation:_ {"level": "recommended", "reasons": ["A lawyer should review the notice draft to ensure it meets all technical requirements before sending."]}  _Citations:_ ['NIA1881-S138', 'NIA1881-S142-1']

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
   "event": "Bank return memo received"
  }
 ],
 "evidence_have": [
  "Original cheque",
  "Bank return memo"
 ],
 "evidence_missing": [
  "Proof of loan (messages/agreement)",
  "Postal receipts of notice (to be generated)"
 ],
 "next_step": "Send a formal legal demand notice via registered post."
}
```

## Draft document

LEGAL NOTICE

By Registered Post A.D. / Speed Post

Date: [[FILL: date of sending notice]]

From:
[[FILL: your full name]]
[[FILL: your full address]]
[[FILL: your phone and email]]

To:
Arun Mehta
[[FILL: Arun Mehta's full address]]

Subject: Demand for payment of Rs 2,00,000 against dishonoured cheque.

Dear Sir,

1. I am writing to you regarding the loan of Rs 2,00,000 that you borrowed from me. To discharge this legally enforceable debt, you issued a cheque bearing number [[FILL: cheque number]] dated 15 October 2026, drawn on [[FILL: your bank name and branch]] in my favour.

2. I presented the said cheque for payment through my bank on 20 October 2026. However, the cheque was returned unpaid by your bank with the remark "funds insufficient" as per the bank return memo dated 27 October 2026, which I received on the same day.

3. This notice is being served upon you under Section 138 of the Negotiable Instruments Act, 1881. The dishonour of the cheque due to insufficient funds constitutes a criminal offence under the said Act.

4. I hereby demand that you pay the full cheque amount of Rs 2,00,000 to me within 15 days of the receipt of this notice. Please make the payment via [[FILL: your bank details (account name, number, bank, IFSC)]].

5. If you fail to make the payment within the stipulated 15-day period, I shall be constrained to initiate appropriate legal proceedings against you, including filing a criminal complaint under Section 138 read with Section 142 of the Negotiable Instruments Act, 1881, in a court of competent jurisdiction. In such an event, you will be liable for all costs, expenses, and consequences arising from such litigation.

Copy retained for record.

Sincerely,

[[FILL: your full name]]
[[FILL: your phone and email]]

**Send instructions:** ["Print two copies of this notice. Sign both copies in blue or black ink.", "Send one copy to Arun Mehta via Registered Post A.D. or Speed Post. Keep the original postal receipt safely.", "Keep the second copy for your own records, along with the original cheque and the bank return memo.", "Wait for 15 days from the date Arun Mehta receives the notice (track the delivery status online using the postal tracking number).", "If he does not pay within those 15 days, you have one month from the end of that period to file a criminal complaint in the court where your bank branch is located."]

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
| draft_has_no_invented_fill | ✅ | 8 placeholders |
