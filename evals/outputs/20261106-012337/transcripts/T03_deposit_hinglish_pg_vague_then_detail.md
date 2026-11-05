# T03_deposit_hinglish_pg_vague_then_detail
Group: multi_turn

## Turn 1

**User:** bhai mera paisa nahi de raha

**Haq** (gemini/gemini-3.1-flash-lite, 4.98s):

Namaste. Main aapki madad karne ki koshish karunga, par mujhe thoda aur batana hoga ki mamla kya hai. 

Kya aap bata sakte hain ki ye paise kis baat ke hain? 
- Kya ye naukri ki salary (salary) hai?
- Kya ye kisi saman ka refund (consumer refund) hai?
- Kya ye ghar ka security deposit (rent deposit) hai?
- Ya phir kisi ne cheque bounce kiya hai?

Ye bhi batayein ki kitne paise hain aur kab se nahi mil rahe hain? Isse main aapko sahi rasta dikha paunga.

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ []

## Turn 2

**User:** PG wala hai pune me, 15000 deposit tha. 1 october ko chhoda. ab bolta hai notice period nahi diya isliye nahi dunga. koi agreement nahi tha bas whatsapp pe baat hui thi

**Haq** (gemini/gemini-3.1-flash-lite, 5.95s):

Samajh gaya. Pune mein PG owner ka deposit na dena kaafi pareshan karne wala ho sakta hai. Bina written agreement ke thoda mushkil hota hai, par aapke WhatsApp messages hi aapka sabse bada saboot (evidence) hain. 

Kanooni taur par, aap ye raste apna sakte hain:

1. **Written Request:** Owner ko WhatsApp ya email par ek formal message bhejein. Usme saaf likhein ki aapne kab room chhoda, kitna deposit tha, aur aapka bank account details kya hai. Screenshot lekar rakhein.
2. **Legal Notice:** Agar wo phir bhi na mane, toh aap khud ek 'Legal Notice' bhej sakte hain jisme 15 din ka time dein.
3. **Legal Aid:** Agar baat nahi banti, toh aap Pune ke District Legal Services Authority (DLSA) se sampark kar sakte hain ya 15100 par call karke free salah le sakte hain.

Agla kadam: Kya aapke paas wo WhatsApp chat hai jisme deposit aur room chhodne ki baat hui thi? Main aapko ek formal message ka draft bana kar de sakta hoon jo aap owner ko bhej sakein.

**Calculated by code:** {"deadlines": [{"label": "Approximate last date to sue for the deposit (3 years)", "date": "2029-10-01", "days_left": 1060, "status": "ok", "basis": "LIM1963-ART55", "note": "Limitation depends on the exact claim; confirm with legal aid before relying on it.", "user_deadline": true}], "derived": []}

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['ICA1872-S73', 'FACT-NALSA-HELPLINE']

## Final case file

```json
{
 "category": "tenancy",
 "language": "Hinglish",
 "script": "Latin",
 "facts": {
  "summary": "PG owner refusing to return 15000 deposit claiming no notice period was given.",
  "deposit_amount": 15000,
  "written_agreement": false,
  "possession_handed_over_date": "2026-10-01",
  "communications_so_far": "WhatsApp",
  "city_state": "Pune",
  "deductions_claimed": "notice period not given"
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
  "nature of the debt",
  "amount",
  "date when payment was due",
  "Proof of payment (bank transfer receipt/screenshot)"
 ],
 "next_step": "Draft a formal request message to the landlord."
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
