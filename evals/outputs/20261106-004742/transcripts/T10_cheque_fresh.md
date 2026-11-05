# T10_cheque_fresh
Group: core

## Turn 1

**User:** My friend Arun Mehta borrowed Rs 2,00,000 from me last year and gave me a cheque dated 15 October 2026 to repay it. I deposited it on 20 October and my bank returned it on 27 October 2026 with the reason 'funds insufficient'. I got the return memo the same day. What should I do?

**Haq** (groq/openai/gpt-oss-20b, 10.93s):

Hi! I understand you’re dealing with a bounced cheque of ₹2,00,000 from Arun Mehta. Let’s see what you can do next.

**Quick questions**
1. Where is your bank branch (city)?
2. Have you sent a written demand notice to Arun yet? If yes, when?

**What you can do (cheapest to most expensive)**
1. Send a written demand notice (within 30 days of the return memo – by 26 Nov 2026).
2. If he pays within 15 days of that notice, you’re done.
3. If not, file a criminal complaint under the Negotiable Instruments Act (within 1 month after the 15‑day period).
4. You can also settle at any stage – it’s a compoundable offence.
5. If the 30‑day window is missed, a civil summary suit may still be possible – you’ll need a lawyer.

**Recommended next step** – Send the written demand notice today. I can draft it for you.

Let me know the city and whether you’ve already sent the notice, and I’ll help you draft it.

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
  "other_party_name": "Arun Mehta",
  "city_state": "<city>"
 },
 "timeline": [
  {
   "date": "2026-10-27",
   "event": "bank returned cheque"
  }
 ],
 "evidence_have": [],
 "evidence_missing": [
  "copy of return memo",
  "copy of cheque"
 ],
 "next_step": "send written demand notice"
}
```

## Draft document

LEGAL NOTICE
By Registered Post A.D. / Speed Post
Date: [[FILL: date of sending the notice]]

**From:**
[[FILL: your full name]]
[[FILL: your full address]]

**To:**
Mr. Arun Mehta
[[FILL: Arun Mehta's full address]]

**Subject:** Demand for payment of Rs. 2,00,000/- (Rupees Two Lakh Only) being the amount of a dishonoured cheque issued by you.

Sir/Madam,

I write to you on my own behalf. I hereby give you notice as follows:

1. You borrowed the sum of Rs. 2,00,000/- (Rupees Two Lakh Only) from me last year. This loan constitutes a legally enforceable debt owed by you to me.

2. In discharge of the above debt, you issued a cheque in my favour bearing number [[FILL: cheque number]], dated 15 October 2026, drawn on [[FILL: name of Arun Mehta's bank and branch]], for the amount of Rs. 2,00,000/- (Rupees Two Lakh Only).

3. I presented the said cheque for encashment through my bank account maintained at [[FILL: name of your bank and branch]] on 20 October 2026, which is well within the period of validity of the cheque.

4. The said cheque was dishonoured by your bank. My bank returned the cheque to me on 27 October 2026 with the return memo stating the reason for dishonour as "funds insufficient".

5. I have made no prior written demand to you for payment of the said amount. This notice constitutes my first written demand.

6. I bring to your notice that under Section 138 of the Negotiable Instruments Act, 1881, the dishonour of a cheque issued for the discharge of a legally enforceable debt, where the cheque is presented within its validity period and is returned unpaid due to insufficient funds, constitutes an offence punishable with imprisonment up to two years, or a fine up to twice the amount of the cheque, or both.

**DEMAND:**

7. I hereby demand that you pay me the sum of **Rs. 2,00,000/- (Rupees Two Lakh Only)** within **fifteen (15) days** from the date of your receipt of this notice.

8. Payment may be made by any of the following modes:
   - Bank transfer to: [[FILL: your bank name, account name, account number, IFSC code, branch]]
   - Cheque/demand draft payable to [[FILL: your name]] drawn on any nationalised bank, payable at [[FILL: your city]]

**CONSEQUENCE OF NON-COMPLIANCE:**

9. If I do not receive the full amount within the said period of fifteen (15) days from your receipt of this notice, I shall be constrained to initiate a criminal complaint against you under Section 138 read with Section 142 of the Negotiable Instruments Act, 1881, before the competent court, at your cost and risk. I shall also reserve my right to pursue any other civil or criminal remedy available to me in law.

10. This notice is issued without prejudice to any of my rights, which are expressly reserved.

Copy retained for record.

Yours faithfully,

_________________________
[[FILL: your full name]]
Phone: [[FILL: your phone number]]
Email: [[FILL: your email address]]

**Send instructions:** ["Fill in all [[FILL: ...]] placeholders with correct details before printing. Double-check the cheque number, bank names, and addresses.", "Send the notice by Registered Post A.D. AND by Speed Post (two copies) to Arun Mehta's address. Keep the postal receipts and the tracking numbers as proof of sending.", "If you also send by email, send it from your own email address and keep a screenshot of the sent message with date and time.", "Keep one original copy of the notice with the postal receipts stapled to it. This is your record.", "If you need free legal help, call the NALSA helpline 15100 (toll-free) or visit your nearest Common Service Centre (CSC) for the Tele-Law service."]

## Automatic checks

| check | pass | detail |
|---|---|---|
| category | ✅ | got cheque_bounce |
| reply_language | ✅ | expected Latin, reply script Latin |
| fact:memo_received_date | ✅ | expected ~2026-10-27, got 2026-10-27 |
| fact:cheque_amount | ✅ | expected ~2, got 200000 |
| mentions:30 days|30-day|30‑day|30 din | ✅ |  |
| mentions:15 days|15-day|15‑day|15 din | ✅ |  |
| escalation<=recommended | ✅ | got none |
| deadline:NIA1881-S138 | ✅ | [{"label": "Cheque must be presented to the bank by (3-month validity)", "date": "2027-01-14", "days_left": 69, "status": "ok", "basis": "FACT-RBI-CHEQUE-VALIDI |
| no_unverified_law_shown | ✅ |  |
| draft_no_unverified_law | ✅ | [] |
| draft_has_no_invented_fill | ✅ | 12 placeholders |
