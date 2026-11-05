# T03_deposit_hinglish_pg_vague_then_detail
Group: multi_turn

## Turn 1

**User:** bhai mera paisa nahi de raha

**Haq** (groq/openai/gpt-oss-20b, 4.87s):

Kya hua? Kiska paisa hai, kitna, kab aur kis tarah ka proof hai?

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['FACT-NALSA-HELPLINE']

## Turn 2

**User:** PG wala hai pune me, 15000 deposit tha. 1 october ko chhoda. ab bolta hai notice period nahi diya isliye nahi dunga. koi agreement nahi tha bas whatsapp pe baat hui thi

**Haq** (groq/openai/gpt-oss-20b, 5.4s):

Bhai, samajh gaye. Thoda aur detail chahiye:
1. Kya aapke paas 15,000 ka receipt ya bank statement hai? 
2. PG owner ne koi deduction claim kiya? (painting, damage, dues?) 
3. WhatsApp conversation ka screenshot ya message log? 
4. Notice period ka kya agreement tha? (Kya 30 din ka notice diya tha?)

Inke bina exact steps batana mushkil hai. 

Options (cheapest to expensive):
1. Written request (WhatsApp/email) with amount, move‑out date, bank details – keep screenshots.
2. Legal notice demanding refund within ~15 days (you can send it yourself).
3. Free pre‑litigation Lok Adalat / DLSA helpline (15100).
4. Civil suit for recovery (3‑year limit already passed – lawyer needed).

**Recommended next step:** Draft a simple written request (WhatsApp/email) asking for the 15,000 refund, mention move‑out date and give bank details. Keep screenshots. 

I can help draft that message. Let me know if you want me to do it.

⚠️ **Deadline check (calculated by Haq, not AI):** Approximate last date to sue for the deposit (3 years): **01 Oct 2026**, which has passed. Please speak to a lawyer or free legal aid (15100) soon to check what options remain.

**Calculated by code:** {"deadlines": [{"label": "Approximate last date to sue for the deposit (3 years)", "date": "2026-10-01", "days_left": -36, "status": "passed", "basis": "LIM1963-ART55", "note": "Limitation depends on the exact claim; confirm with legal aid before relying on it.", "user_deadline": true}], "derived": []}

_Escalation:_ {"level": "recommended", "reasons": ["Deadline passed: Approximate last date to sue for the deposit (3 years) (2026-10-01)"]}  _Citations:_ ['ICA1872-S73', 'FACT-LOKADALAT-PRELITIGATION', 'FACT-NALSA-HELPLINE']

## Final case file

```json
{
 "category": "tenancy",
 "language": "Hinglish",
 "script": "Latin",
 "facts": {
  "user_name": "bhai",
  "summary": "User says someone is not giving them money",
  "deposit_amount": "15000",
  "possession_handed_over_date": "2023-10-01",
  "written_agreement": "no",
  "city_state": "Pune, Maharashtra",
  "other_party_name": "PG owner",
  "communications_so_far": "WhatsApp",
  "proof_of_payment": "none"
 },
 "timeline": [
  {
   "date": "2023-10-01",
   "event": "Left PG"
  }
 ],
 "evidence_have": [],
 "evidence_missing": [
  "proof of amount, date, communication",
  "proof of payment (bank statement/receipt)",
  "WhatsApp screenshots",
  "any deduction claim"
 ],
 "next_step": "draft written request",
 "approximate": [
  "possession_handed_over_date"
 ]
}
```

## Automatic checks

| check | pass | detail |
|---|---|---|
| category | ✅ | got tenancy |
| reply_language | ❌ | expected Hinglish, reply script Latin |
| fact:deposit_amount | ✅ | expected ~15, got 15000 |
| mentions:whatsapp|WhatsApp|screenshot|chat | ✅ |  |
| escalation<=recommended | ✅ | got recommended |
| asks_clarifying_question | ✅ |  |
| no_unverified_law_shown | ✅ |  |
