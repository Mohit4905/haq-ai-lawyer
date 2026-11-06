# T08_salary_factory_worker_voice_style
Group: core

## Turn 1

**User:** sir main factory me helper hu ghaziabad me thekedar ke through kaam karta tha 14000 mahina milta tha do mahine se paisa nahi diya thekedar bhag gaya company bolti hai thekedar se lo ab kya karu ghar ka kiraya bhi nahi de pa raha

**Haq** (gemini/gemini-3.1-flash-lite, 10.05s):

**Your legal position:**
Aapki situation mushkil hai, par kanoon aapke saath hai. Code on Wages, 2019 ke mutabik, agar contractor (thekedar) paisa nahi de raha, toh factory (principal employer) ki zimmedari banti hai ki woh aapka baki salary clear kare. Company sirf yeh keh kar nahi bach sakti ki "thekedar se lo."

**Law you can cite:**
* **Code on Wages, 2019 (Section 17):** Salary time par milna aapka haq hai. Agar contractor gayab hai, toh factory ko payment karni hogi.
* **Code on Wages, 2019 (Section 45):** Aap Labour Authority ke paas claim file kar sakte hain. Yeh authority aapka paisa dilwane mein madad karti hai.
* **Code on Wages, 2019 (Section 51):** Aap Ghaziabad ke 'Inspector-cum-Facilitator' se milkar apni shikayat darj karwa sakte hain, woh aapki madad karenge.

**What to do now:**
1. Apne paas jo bhi proof hai (ID card, gate pass, bank statement, ya thekedar ki chat) sambhal kar rakhein.
2. Factory Manager ko ek written letter ya email dein, jisme saaf likha ho ki thekedar gayab hai aur aapka 2 mahine ka salary (Rs 28,000) baki hai.
3. Agar 3-4 din mein jawab na aaye, toh Ghaziabad ke Labour Office mein 'Inspector-cum-Facilitator' se milein. Free madad ke liye 15100 par call karein.

**I need from you:**
1. Kya aapke paas koi ID card, gate pass, ya bank statement hai jisse sabit ho sake ki aap wahan kaam karte the?
2. Kya aapne Factory Manager ko abhi tak koi written complaint di hai?

_Escalation:_ {"level": "recommended", "reasons": ["Since the contractor has absconded, you need to establish the factory's liability, which may require formal intervention by the Labour Inspector."]}  _Citations:_ ['COW2019-S17', 'COW2019-S45', 'COW2019-S51']

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
 "timeline": [],
 "evidence_have": [],
 "evidence_missing": [
  "ID card",
  "Gate pass",
  "Bank statement",
  "Any communication with thekedar"
 ],
 "next_step": "Write a formal letter to the factory management demanding the unpaid wages."
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
