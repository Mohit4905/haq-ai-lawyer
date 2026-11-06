# T03_deposit_hinglish_pg_vague_then_detail
Group: multi_turn

## Turn 1

**User:** bhai mera paisa nahi de raha

**Haq** (gemini/gemini-3.1-flash-lite, 8.23s):

Namaste. Main samajh sakta hoon ki paisa phansa hona kitna pareshan karne wala hota hai. Aapka mamla samajhne ke liye mujhe thodi aur jaankari chahiye taaki main sahi raasta dikha sakoon.

**Your legal position:**
Jab tak mujhe ye nahi pata ki paisa kis baat ka hai (salary, loan, security deposit, ya koi aur deal), tab tak main exact kanoon nahi bata sakta. Lekin, har mamle mein aapke paas proof hona zaroori hai ki paisa kab aur kaise diya gaya tha.

**What to do now:**
1. Sabse pehle, apne paas saare proofs ikattha karein (bank statement, chat, ya koi agreement).
2. Agar mamla samajh nahi aa raha, toh aap NALSA ki helpline 15100 par call karke free legal advice le sakte hain.

**I need from you:**
1. Ye paisa kis cheez ka hai? (Salary, kisi ko udhaar diya tha, security deposit, ya koi saman khareeda tha?)
2. Kya aapke paas koi proof hai (jaise bank transfer, message, ya koi likhit agreement)?

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['FACT-NALSA-HELPLINE']

## Turn 2

**User:** PG wala hai pune me, 15000 deposit tha. 1 october ko chhoda. ab bolta hai notice period nahi diya isliye nahi dunga. koi agreement nahi tha bas whatsapp pe baat hui thi

**Haq** (gemini/gemini-3.1-flash-lite, 15.15s):

Namaste. PG owner ka deposit rokna ek aam samasya hai, lekin aapke paas WhatsApp chats hain, jo ek strong saboot (evidence) ka kaam karti hain. Bina written agreement ke bhi, owner ko deposit wapas karna hota hai agar aapne koi nuksan nahi kiya hai. Owner sirf tabhi paise kaat sakta hai agar koi valid nuksan (damage) hua ho, sirf 'notice period' ka bahana bana kar pura paisa rokna galat hai.

**Your legal position:**
WhatsApp chats aapke contract ka proof hain. Aapka claim strong hai kyunki aapne possession de diya hai. Owner ko legally deposit wapas karna chahiye, aur agar wo nahi karta, toh aap contract ke breach ke liye claim kar sakte hain.

**Law you can cite:**
* **Section 73, Indian Contract Act, 1872:** Agar koi contract toda jata hai, toh aap usse hue nuksan ki bharpayi maang sakte hain. Ye aapke deposit recovery ka main basis hai.
* **Limitation Act, 1963 (Article 55):** Aapke paas deposit recovery ke liye 3 saal ka samay hai, jo ki 1 October 2026 se shuru hota hai.

**What to do now:**
1. **Formal Request:** Ek formal WhatsApp message ya email bhejein jisme saaf likha ho ki aapne kab room chhoda aur aapka bank account details kya hai. Screenshot lekar rakhein.
2. **Legal Notice:** Agar wo phir bhi na mane, toh ek formal legal notice bhejein (aap khud bhi draft kar sakte hain).
3. **DLSA:** Agar baat nahi banti, toh Pune District Legal Services Authority (DLSA) se sampark karein ya 15100 par call karein.

**I need from you:**
1. Kya aapke paas bank statement ya koi proof hai ki aapne 15000 deposit transfer kiya tha?
2. Kya WhatsApp chat mein kahin bhi 'notice period' ki shart (condition) ka zikr tha?

**Calculated by code:** {"deadlines": [{"label": "Approximate last date to sue for the deposit (3 years)", "date": "2029-10-01", "days_left": 1060, "status": "ok", "basis": "LIM1963-ART55", "note": "Limitation depends on the exact claim; confirm with legal aid before relying on it.", "user_deadline": true}], "derived": []}

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['ICA1872-S73', 'LIM1963-ART55']

## Final case file

```json
{
 "category": "tenancy",
 "language": "Hinglish",
 "script": "Latin",
 "facts": {
  "summary": "PG owner refusing to return 15000 deposit, citing lack of notice period. No written agreement, only WhatsApp chats.",
  "deposit_amount": 15000,
  "written_agreement": false,
  "possession_handed_over_date": "2026-10-01",
  "city_state": "Pune"
 },
 "timeline": [
  {
   "date": "2026-10-01",
   "event": "Possession handed over"
  }
 ],
 "evidence_have": [
  "WhatsApp chats"
 ],
 "evidence_missing": [
  "proof of transaction (bank statement/chat/agreement)",
  "nature of the transaction",
  "Proof of payment (bank statement/transaction ID)",
  "Copy of chat discussing notice period"
 ],
 "next_step": "Send a formal written request via WhatsApp/Email demanding the refund."
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
