# T10_cheque_fresh
Group: core

## Turn 1

**User:** My friend Arun Mehta borrowed Rs 2,00,000 from me last year and gave me a cheque dated 15 October 2026 to repay it. I deposited it on 20 October and my bank returned it on 27 October 2026 with the reason 'funds insufficient'. I got the return memo the same day. What should I do?

**Haq** (groq/openai/gpt-oss-120b, 32.64s):

Arun ne aapko Rs 2,00,000 ka cheque diya tha, aapne 20 Oct ko deposit kiya aur 27 Oct ko bank ne ‘funds insufficient’ ke reason se return memo diya. Ab aapke paas 30 din ka window hai (till 26 Nov 2026) demand notice bhejne ka.

**What to do next**
- **Write a demand notice** under Sec 138 of the Negotiable Instruments Act, 1881. Mention cheque details, amount, date, return memo date, and ask Arun to pay the full amount within 15 days of receiving your notice.
- Send it by **registered post or speed‑post** and keep the receipt.
- If he pays within 15 days, case ends. If not, you can file a criminal complaint under Sec 142(1) of the same Act (within 1 month after the 15‑day period ends).

**Key points**
- Cheque was presented within its 3‑month validity (valid till 14 Jan 2027).
- You still have time to send the notice (20 days left).
- No lawyer needed for the notice; you can handle it yourself.

Would you like me to draft the demand notice?

> 🛡️ Guard caught (before user saw it): [{"type": "unknown_act", "text": "NI Act", "why": "This law is not in the verified library."}]  
> repaired=True stripped=False

**Calculated by code:** {"deadlines": [{"label": "Cheque must be presented to the bank by (3-month validity)", "date": "2027-01-14", "days_left": 69, "status": "ok", "basis": "FACT-RBI-CHEQUE-VALIDITY", "note": "", "user_deadline": true}, {"label": "Send the legal demand notice by (30 days from bank's return memo)", "date": "2026-11-26", "days_left": 20, "status": "ok", "basis": "NIA1881-S138", "note": "Count from the day you got the bank's information; send by registered post AD/speed post and keep receipts.", "user_deadline": true}], "derived": []}

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['NIA1881-S138', 'NIA1881-S142-1', 'NIA1881-S142-2']

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
  "other_party_name": "Arun Mehta"
 },
 "timeline": [
  {
   "date": "2026-10-27",
   "event": "Bank returned cheque with insufficient funds memo"
  }
 ],
 "evidence_have": [
  "bank return memo (dated 27 Oct 2026)"
 ],
 "evidence_missing": [
  "copy of the cheque, any communication with Arun about repayment"
 ],
 "next_step": "Send a written demand notice to Arun by 26 Nov 2026 (registered post) and keep receipt."
}
```

## Draft document

**LEGAL NOTICE**

**Mode of Sending:** By Registered Post A.D.

**Date:** [[FILL: date of sending (dd/mm/yyyy)]]

**From:**
[[FILL: Your Full Name]]
[[FILL: Your Full Address]]

**To:**
Arun Mehta
[[FILL: Arun Mehta's full address]]

**Subject:** Demand for payment of Rs. 2,00,000 due to dishonour of Cheque No. [[FILL: cheque number]] dated 15‑Oct‑2026.

1. On **15‑Oct‑2026**, Arun Mehta issued me a cheque (Cheque No. [[FILL: cheque number]]) for **Rs. 2,00,000** as repayment of a loan of Rs. 2,00,000 that he had borrowed from me on [[FILL: loan date or "last year"]].
2. I deposited the said cheque on **20‑Oct‑2026** in my account at [[FILL: your bank name and branch]].
3. On **27‑Oct‑2026**, my bank returned the cheque with a memo stating **"funds insufficient"**. I received the return memo on the same day.
4. I have made no prior written demand for payment to Arun Mehta.
5. The cheque was presented within the statutory validity period of three months as per RBI guidelines.
6. The amount represented a legally enforceable debt arising from the loan given by me to Arun Mehta.

**Legal Basis:**
The dishonour of the cheque amounts to an offence under **Section 138 of the Negotiable Instruments Act, 1881** ([NIA1881‑S138]).

**Demand:**
I hereby demand that Arun Mehta pay the full cheque amount of **Rs. 2,00,000** within **fifteen (15) days** from the date of receipt of this notice. Payment may be made by direct transfer to my bank account:

- **Bank Name:** [[FILL: your bank name]]
- **Branch:** [[FILL: your bank branch]]
- **Account Number:** [[FILL: your account number]]
- **IFSC Code:** [[FILL: IFSC code]]

**Consequences of Non‑Compliance:**
If the amount is not received within the stipulated period, I will be compelled to file a criminal complaint against Arun Mehta under **Section 138 read with Section 142 of the Negotiable Instruments Act, 1881**. The complaint will be filed in the appropriate court, and all costs incurred will be borne by the defaulting party.

**Copy retained for record.**

______________________________
[[FILL: Your Full Name]]
Phone: [[FILL: Your phone number]]
Email: [[FILL: Your email address]]

## Automatic checks

| check | pass | detail |
|---|---|---|
| category | ✅ | got cheque_bounce |
| reply_language | ✅ | expected Latin, reply script Latin |
| fact:memo_received_date | ✅ | expected ~2026-10-27, got 2026-10-27 |
| fact:cheque_amount | ✅ | expected ~2, got 200000 |
| mentions:30 days | ❌ |  |
| mentions:15 days | ❌ |  |
| escalation<=recommended | ✅ | got none |
| deadline:NIA1881-S138 | ✅ | [{"label": "Cheque must be presented to the bank by (3-month validity)", "date": "2027-01-14", "days_left": 69, "status": "ok", "basis": "FACT-RBI-CHEQUE-VALIDI |
| no_unverified_law_shown | ✅ |  |
| draft_no_unverified_law | ✅ | [] |
| draft_has_no_invented_fill | ✅ | 13 placeholders |
