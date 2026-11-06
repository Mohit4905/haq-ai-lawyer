# T03_deposit_hinglish_pg_vague_then_detail
Group: multi_turn

## Turn 1

**User:** bhai mera paisa nahi de raha

**Haq** (gemini/gemini-3.1-flash-lite, 6.73s):

Bhai, main samajh sakta hoon ki paisa phansa hona kitna pareshan karne wala hota hai. Lekin sahi advice dene ke liye mujhe thoda aur context chahiye. 

Ye paisa kis cheez ka hai? Jaise ki:
1. Kya ye kisi ne udhaar (loan) liya tha?
2. Kya ye aapki salary hai?
3. Kya ye kisi saman ya service ke liye advance payment thi?
4. Ya phir ghar ka security deposit hai?

Aur kitna amount hai aur kya aapke paas koi proof hai (jaise bank transfer, agreement, ya WhatsApp chat)? Ye details bataiye, phir main aapko bataunga ki aapko legal notice bhejna chahiye ya seedha complaint karni chahiye.

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ []

## Turn 2

**User:** PG wala hai pune me, 15000 deposit tha. 1 october ko chhoda. ab bolta hai notice period nahi diya isliye nahi dunga. koi agreement nahi tha bas whatsapp pe baat hui thi

**Haq** (gemini/gemini-3.1-flash-lite, 12.67s):

Bhai, bina written agreement ke landlord ke liye ye sabit karna mushkil hai ki koi notice period ka rule tha. Agar usne pehle se ye baat clear nahi ki thi, toh wo aapka paisa aise nahi rok sakta. 

**My view:** Aapka case strong hai kyunki burden of proof landlord par hai ki wo dikhaye ki aapne notice period ke liye haan kaha tha. Bina kisi written contract ya clear communication ke, wo apni marzi se paise nahi kaat sakta.

**Law on your side:**
- Indian Contract Act, 1872 (Section 73): Agar koi contract breach hua hai, toh landlord ko ye sabit karna hoga ki kya terms decide hue the. Bina proof ke wo penalty nahi laga sakta.

**What they will say, and your answer:**
- Wo kahenge: "Notice period nahi diya."
- Aapka jawab: "Humare beech koi written agreement nahi tha jisme notice period ka zikr ho. Aap mujhe wo proof dikhayein jahan maine notice period ke liye agree kiya tha."

**What I would do:**
- Aaj hi ek formal message (WhatsApp/Email) bhejiye. Usme likhiye: 'Maine 1 October ko room vacate kiya tha. Mere 15,000 deposit ka refund abhi tak nahi mila hai. Humare beech koi written agreement nahi tha jisme notice period ka zikr ho, isliye aap mera paisa nahi rok sakte. Kripya 3 din ke andar refund process karein, varna mujhe aage legal action lena padega.'
- Agar 3 din mein jawab na aaye, toh main aapko ek legal notice ka draft bana kar dunga.

**Calculated by code:** {"deadlines": [{"label": "Approximate last date to sue for the deposit (3 years)", "date": "2029-10-01", "days_left": 1060, "status": "ok", "basis": "LIM1963-ART55", "note": "Limitation depends on the exact claim; confirm with legal aid before relying on it.", "user_deadline": true}], "derived": []}

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['ICA1872-S73']

## Final case file

```json
{
 "category": "tenancy",
 "language": "Hinglish",
 "script": "Latin",
 "facts": {
  "summary": "PG owner in Pune refusing to return 15000 deposit, citing lack of notice period.",
  "deposit_amount": 15000,
  "written_agreement": false,
  "possession_handed_over_date": "2026-10-01",
  "city_state": "Pune",
  "communications_so_far": "WhatsApp"
 },
 "timeline": [
  {
   "date": "2026-10-01",
   "event": "Vacated PG"
  }
 ],
 "evidence_have": [
  "WhatsApp chat"
 ],
 "evidence_missing": [
  "nature of transaction",
  "amount",
  "proof of payment",
  "Proof of payment (bank transfer/receipt)"
 ],
 "next_step": "Send a formal demand message"
}
```

## Automatic checks

| check | pass | detail |
|---|---|---|
| category | ✅ | got tenancy |
| reply_language | ✅ | expected Hinglish, reply script Hinglish |
| fact:deposit_amount | ✅ | expected ~15, got 15000 |
| mentions:whatsapp|WhatsApp|screenshot|chat | ✅ |  |
| escalation<=recommended | ✅ | got none |
| asks_clarifying_question | ✅ |  |
| no_unverified_law_shown | ✅ |  |
