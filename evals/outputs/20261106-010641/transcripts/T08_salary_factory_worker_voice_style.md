# T08_salary_factory_worker_voice_style
Group: core

## Turn 1

**User:** sir main factory me helper hu ghaziabad me thekedar ke through kaam karta tha 14000 mahina milta tha do mahine se paisa nahi diya thekedar bhag gaya company bolti hai thekedar se lo ab kya karu ghar ka kiraya bhi nahi de pa raha

**Haq** (gemini/gemini-3.1-flash-lite, 12.02s):

Yeh sunkar bahut dukh hua ki aapko itni pareshani ho rahi hai. Ghaziabad mein factory helper ke taur par kaam karte hue agar thekedar bhag gaya hai, toh company apni zimmedari se nahi bach sakti. Code on Wages, 2019 ke tehat, agar contractor paise nahi deta, toh principal employer (factory) ki zimmedari hoti hai ki woh aapka vetan (salary) chukaye.

Sabse pehle, aapke paas kya saboot hain ki aap wahan kaam karte the? Jaise ki:
1. Koi ID card ya Gate pass?
2. Bank statement jisme salary aati thi?
3. Koi attendance record ya message?

Yeh rahe aapke options:
1. Company management ko likhit mein (email/letter) salary ki maang karein.
2. Labour Office (Inspector-cum-Facilitator) mein shikayat darj karein.
3. SAMADHAN portal par online claim file karein.

Main aapko salah dunga ki pehle company ko ek formal letter dein jisme saaf likha ho ki aapka kitna paisa baaki hai. Kya aapke paas company ke HR ya manager ka koi contact hai?

_Escalation:_ {"level": "recommended", "reasons": ["Since the contractor has absconded and the company is denying liability, you may need help navigating the labour authority process."]}  _Citations:_ ['COW2019-S2K', 'FACT-COW-NO-WAGE-CEILING', 'COW2019-S45', 'COW2019-S51']

## Final case file

```json
{
 "category": "salary",
 "language": "Hinglish",
 "script": "Latin",
 "facts": {
  "role": "helper",
  "monthly_salary": 14000,
  "unpaid_period": "2 months",
  "city_state": "Ghaziabad",
  "other_party_name": "thekedar",
  "summary": "User is a factory helper in Ghaziabad whose contractor has absconded without paying 2 months of salary."
 },
 "timeline": [
  {
   "date": "2025-01-01",
   "event": "Contractor absconded, 2 months salary unpaid"
  }
 ],
 "evidence_have": [],
 "evidence_missing": [
  "ID card",
  "Gate pass",
  "Bank statements showing salary credits",
  "Any written communication with the company"
 ],
 "next_step": "Draft a written complaint to the company management."
}
```

## Automatic checks

| check | pass | detail |
|---|---|---|
| category | ✅ | got salary |
| reply_language | ✅ | expected Hinglish, reply script Hinglish |
| fact:monthly_salary | ✅ | expected ~14, got 14000 |
| mentions:labour|Labour|श्रम|Inspector|inspector | ✅ |  |
| escalation<=urgent | ✅ | got recommended |
| no_unverified_law_shown | ✅ |  |
