# T03_deposit_hinglish_pg_vague_then_detail
Group: multi_turn

## Turn 1

**User:** bhai mera paisa nahi de raha

**Haq** (gemini/gemini-3.1-flash-lite, 5.31s):

Bhai, main samajh sakta hoon ki paise phanse hone par kitni pareshani hoti hai. Aapki madad karne ke liye mujhe thoda aur janana hoga ki mamla kya hai. Kya ye paisa aapne kisi ko udhaar diya tha, kisi naukri ki salary baki hai, ya kisi dukandar/company ko refund ke liye diya tha? 

Jab tak aap batayenge nahi, main sahi kanooni rasta nahi bata paunga. Aap bas ye bata dein:
1. Paisa kis wajah se phansa hai (udhaar, salary, ya refund)?
2. Kitna samay ho gaya hai aur kya aapke paas koi proof hai (jaise message, email, ya receipt)?

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['FACT-NALSA-HELPLINE']

## Turn 2

**User:** PG wala hai pune me, 15000 deposit tha. 1 october ko chhoda. ab bolta hai notice period nahi diya isliye nahi dunga. koi agreement nahi tha bas whatsapp pe baat hui thi

**Haq** (gemini/gemini-3.1-flash-lite, 8.95s):

**Your legal position:**
Bhai, bina written agreement ke bhi aapka case mazboot hai kyunki WhatsApp par hui baatcheet ek 'implied contract' (maana hua samjhauta) maani jaati hai. Landlord sirf apni marzi se deposit nahi rok sakta; agar unhone notice period ka claim kiya hai, toh unhe ye saabit karna hoga ki notice period kitna tha aur aapne wo nahi diya. WhatsApp par aapke paas jo bhi proof hai, wo court mein kaam aayega.

**Law you can cite:**
* **Section 73, Indian Contract Act, 1872:** Agar koi contract todta hai, toh aap nuksan ki bharpayi (deposit refund) maang sakte hain.
* **Article 55, Limitation Act, 1963:** Aapke paas apna paisa recover karne ke liye 3 saal ka samay hota hai, isliye abhi kaafi waqt hai.

**What to do now:**
1. **Formal Demand:** WhatsApp par ek saaf message bhejiye jismein aapne kab room chhoda aur kitna paisa baki hai, uska zikr ho. Unhe 7 din ka time dein.
2. **Legal Notice:** Agar wo nahi maante, toh ek formal legal notice bhejiye (main ismein aapki madad kar sakta hoon).
3. **DLSA:** Agar phir bhi baat na bane, toh Pune ke District Legal Services Authority (DLSA) mein pre-litigation mediation ke liye apply karein (Helpline: 15100).

**I need from you:**
1. Kya aapke paas bank transfer ya UPI ka proof hai ki aapne 15,000 deposit diya tha?
2. Kya aapne room chhodne se pehle unhe koi bhi message ya verbal notice diya tha?

**Calculated by code:** {"deadlines": [{"label": "Approximate last date to sue for the deposit (3 years)", "date": "2029-10-01", "days_left": 1060, "status": "ok", "basis": "LIM1963-ART55", "note": "Limitation depends on the exact claim; confirm with legal aid before relying on it.", "user_deadline": true}], "derived": []}

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['ICA1872-S73', 'LIM1963-ART55', 'FACT-LOKADALAT-PRELITIGATION']

## Final case file

```json
{
 "category": "tenancy",
 "language": "Hinglish",
 "script": "Latin",
 "facts": {
  "summary": "PG owner refusing to return 15000 deposit, claiming no notice period was given.",
  "deposit_amount": 15000,
  "possession_handed_over_date": "2026-10-01",
  "written_agreement": false,
  "city_state": "Pune",
  "communications_so_far": "WhatsApp"
 },
 "timeline": [
  {
   "date": "2026-10-01",
   "event": "Possession handed over"
  }
 ],
 "evidence_have": [
  "WhatsApp chat history"
 ],
 "evidence_missing": [
  "nature of transaction",
  "amount involved",
  "proof of transaction",
  "Proof of deposit payment (bank statement/UPI transaction)",
  "Proof of notice given (if any)"
 ],
 "next_step": "Send a formal demand message via WhatsApp"
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
