# T08_salary_factory_worker_voice_style
Group: core

## Turn 1

**User:** sir main factory me helper hu ghaziabad me thekedar ke through kaam karta tha 14000 mahina milta tha do mahine se paisa nahi diya thekedar bhag gaya company bolti hai thekedar se lo ab kya karu ghar ka kiraya bhi nahi de pa raha

**Haq** (gemini/gemini-3.1-flash-lite, 7.09s):

Dekhiye, aap pareshan na hon, kanoon aapke saath hai. Factory owner ye keh kar nahi bach sakta ki 'thekedar se lo', kyunki Code on Wages ke tahat agar thekedar paisa nahi deta, toh principal employer (factory) ki zimmedari banti hai ki woh aapka baki salary chukaye. Aapki sthiti gambhir hai kyunki aapka ghar ka kiraya bhi atka hai, isliye humein turant action lena hoga.

**My view:** Aapka case mazboot hai. Factory owner ki legal liability hai ki woh contract workers ka payment ensure kare. Company ka ye kehna ki 'thekedar se lo' sirf ek bahana hai taaki woh apni zimmedari se bhage. Aapko abhi ek formal notice company ke manager ko dena hoga aur saath hi Labour Commissioner ke yahan shikayat karni hogi.

**Law on your side:**
*   Code on Wages, 2019 ke tahat, principal employer (factory) ki zimmedari hai ki agar contractor payment nahi karta, toh woh aapka salary pay kare.
*   Aapke paas 3 saal ka samay hai claim file karne ka, lekin humein ise turant karna chahiye.

**What they will say, and your answer:**
*   **Company:** "Humara thekedar se contract khatam ho gaya hai, hum zimmedar nahi hain."
*   **Aapka jawab:** "Kanoon ke mutabik, principal employer hone ke naate aap mere salary ke liye primary liable hain, chahe thekedar bhag gaya ho."

**What I would do:**
1.  **Aaj:** Apne paas jitne bhi proof hain (ID card, gate pass, attendance card, ya koi message/call record thekedar ke saath), unhe ek jagah jama karein.
2.  **Kal:** Main aapke liye ek 'Salary Demand Notice' draft kar deta hoon jo aapko factory ke manager ko dena hai aur uski ek copy register post se bhejni hai.
3.  **Agla kadam:** Agar 7 din mein jawab nahi aata, toh hum Ghaziabad ke Labour Commissioner ke office mein 'Inspector-cum-Facilitator' ke paas formal complaint file karenge.

**I need from you:**
1. Kya aapke paas koi aisa document hai (jaise ID card, payslip, ya gate pass) jisse ye sabit ho ki aap us factory mein kaam karte the?
2. Kya aapke paas thekedar ka koi phone number ya address hai?

**Aap yeh kanoon cite kar sakte hain (official source se verified):**
- **Section 17, Code on Wages, 2019**: Wages are due by these deadlines: daily workers at the end of the shift; weekly workers on the last working day of the week; fortnightly workers before the end of the second day after the fortnight; monthly workers before the end of the 7th day of the next month.
- **Section 45, Code on Wages, 2019**: Wage claims under the Code are heard by an authority the Government appoints, who must be at least a Gazetted Officer.
- **Section 2(k), Code on Wages, 2019**: Under the Code on Wages, 'employee' covers anyone an establishment employs on wages for skilled, unskilled, manual, clerical, technical, supervisory, managerial or administrative work.

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['COW2019-S45', 'COW2019-S51', 'FACT-COW-NO-WAGE-CEILING', 'COW2019-S17', 'COW2019-S2K']

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
  "amount_due": 28000,
  "city_state": "Ghaziabad",
  "other_party_name": "thekedar",
  "summary": "User is a factory helper in Ghaziabad whose contractor (thekedar) has absconded without paying 2 months of salary."
 },
 "timeline": [
  {
   "date": "2025-05-22",
   "event": "User reported 2 months unpaid salary and absconding contractor"
  }
 ],
 "evidence_have": [],
 "evidence_missing": [
  "Employment proof (ID card, gate pass, attendance record)",
  "Contractor contact details"
 ],
 "next_step": "Draft a formal salary demand notice to the factory management"
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
