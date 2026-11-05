# T08_salary_factory_worker_voice_style
Group: core

## Turn 1

**User:** sir main factory me helper hu ghaziabad me thekedar ke through kaam karta tha 14000 mahina milta tha do mahine se paisa nahi diya thekedar bhag gaya company bolti hai thekedar se lo ab kya karu ghar ka kiraya bhi nahi de pa raha

**Haq** (gemini/gemini-3.1-flash-lite, 7.03s):

Yeh sunkar bahut bura laga ki aapko itni pareshani ho rahi hai. Ghaziabad mein labour laws ke mutabik, agar thekedar gayab hai, toh factory management ki zimmedari banti hai ki woh aapka baki paisa dilwaye. Aap akele nahi hain, kanoon mein iska rasta hai.

Kya aapke paas factory ka koi ID card, gate pass, ya attendance ka proof hai? Kya aapne factory ke manager ko abhi tak koi written complaint di hai?

Yeh rahe aapke options:
1. Factory management ko formal letter/email likhein (unhe yaad dilayein ki thekedar unke premises par tha).
2. Ghaziabad ke Labour Office mein 'Inspector-cum-Facilitator' se milein.
3. SAMADHAN portal (samadhan.labour.gov.in) par online complaint darj karein.

Sabse pehle, aapko factory management ko ek written notice dena chahiye jisme saaf likha ho ki kitne mahine ka paisa baki hai. Kya main aapke liye yeh letter draft karun?

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['COW2019-S2K', 'COW2019-S45', 'FACT-SAMADHAN-PORTAL']

## Final case file

```json
{
 "category": "salary",
 "language": "Hinglish",
 "script": "Latin",
 "facts": {
  "role": "helper",
  "monthly_salary": "14000",
  "unpaid_period": "2 months",
  "city_state": "Ghaziabad",
  "other_party_name": "thekedar",
  "summary": "User is a factory helper in Ghaziabad whose contractor has absconded without paying 2 months of salary."
 },
 "timeline": [
  {
   "date": "2025-05-01",
   "event": "Approximate start of unpaid period"
  }
 ],
 "evidence_have": [],
 "evidence_missing": [
  "ID card",
  "Gate pass",
  "Attendance proof",
  "Written communication with employer"
 ],
 "next_step": "Draft a formal letter to the factory management demanding the unpaid wages."
}
```

## Automatic checks

| check | pass | detail |
|---|---|---|
| category | ✅ | got salary |
| reply_language | ✅ | expected Hinglish, reply script Hinglish |
| fact:monthly_salary | ✅ | expected ~14, got 14000 |
| mentions:labour|Labour|श्रम|Inspector|inspector | ✅ |  |
| escalation<=urgent | ✅ | got none |
| no_unverified_law_shown | ✅ |  |
