# T03_deposit_hinglish_pg_vague_then_detail
Group: multi_turn

## Turn 1

**User:** bhai mera paisa nahi de raha

**Haq** (gemini/gemini-3.1-flash-lite, 11.27s):

Namaste. Main aapki madad karne ki koshish karunga, lekin mujhe thoda aur batana hoga taaki main sahi raasta dikha sakun. Yeh paisa kis cheez ka hai? 

Kya yeh:
1. Kisi company se refund chahiye?
2. Naukri ki salary (salary) baaki hai?
3. Ghar ka security deposit (security deposit) hai?
4. Kisi ne cheque diya tha jo bounce ho gaya?
5. Ya koi aur mamla hai?

Kitna paisa hai aur kab se nahi mil raha? Yeh bataiye, phir main aapko aage ke steps bata paunga.

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ []

## Turn 2

**User:** PG wala hai pune me, 15000 deposit tha. 1 october ko chhoda. ab bolta hai notice period nahi diya isliye nahi dunga. koi agreement nahi tha bas whatsapp pe baat hui thi

**Haq** (gemini/gemini-3.1-flash-lite, 11.11s):

Samajh gaya. Pune mein PG owner ka deposit (security deposit) ka mamla hai. Bina written agreement ke bhi, aapka claim valid ho sakta hai kyunki WhatsApp par hui baatcheet ek tarah ka saboot (evidence) hai.

**Aapki sthiti (Your standing):**
- Bina agreement ke, landlord ka 'notice period' ka claim prove karna mushkil hota hai, lekin aapka deposit wapas lena aapka haq hai.
- Indian Contract Act, 1872 (Section 73) ke tehat, aap apna paisa claim kar sakte hain.

**Options (Cheapest to formal):**
1. **Written Request:** WhatsApp ya email par ek formal message bhejiye jisme saaf likha ho ki aapne kab room chhoda aur aapka bank account details kya hai. Screenshot sambhal kar rakhein.
2. **Legal Notice:** Agar woh phir bhi na maane, toh aap khud ek legal notice bhej sakte hain (main isme madad kar sakta hoon).
3. **Lok Adalat:** District Legal Services Authority (DLSA) ke zariye free mein settlement ki koshish kar sakte hain.

**Agla kadam:**
Sabse pehle ek formal WhatsApp message bhejiye. Kya aap chahte hain ki main uske liye ek draft likh kar doon?

**Calculated by code:** {"deadlines": [{"label": "Approximate last date to sue for the deposit (3 years)", "date": "2029-10-01", "days_left": 1060, "status": "ok", "basis": "LIM1963-ART55", "note": "Limitation depends on the exact claim; confirm with legal aid before relying on it.", "user_deadline": true}], "derived": []}

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['ICA1872-S73', 'LIM1963-ART55', 'FACT-LOKADALAT-PRELITIGATION', 'FACT-NALSA-HELPLINE']

## Final case file

```json
{
 "category": "tenancy",
 "language": "Hinglish",
 "script": "Latin",
 "facts": {
  "summary": "User is claiming a security deposit of 15000 from a PG owner in Pune who is refusing to pay due to lack of notice period.",
  "deposit_amount": 15000,
  "written_agreement": false,
  "possession_handed_over_date": "2026-10-01",
  "communications_so_far": "WhatsApp",
  "city_state": "Pune",
  "deductions_claimed": "notice period"
 },
 "timeline": [
  {
   "date": "2026-10-01",
   "event": "Moved out of PG"
  }
 ],
 "evidence_have": [
  "WhatsApp chat history"
 ],
 "evidence_missing": [
  "nature of the debt",
  "amount",
  "date when payment was due",
  "Bank transfer proof of deposit payment"
 ],
 "next_step": "Draft a formal WhatsApp message demanding the refund."
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
