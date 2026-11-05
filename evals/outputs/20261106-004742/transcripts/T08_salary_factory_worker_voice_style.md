# T08_salary_factory_worker_voice_style
Group: core

## Turn 1

**User:** sir main factory me helper hu ghaziabad me thekedar ke through kaam karta tha 14000 mahina milta tha do mahine se paisa nahi diya thekedar bhag gaya company bolti hai thekedar se lo ab kya karu ghar ka kiraya bhi nahi de pa raha

**Haq** (groq/openai/gpt-oss-20b, 40.71s):

Hey! Chalo isko clear karte hain.
1. Kya aap abhi bhi factory mein kaam kar rahe hain ya chhod diya? Agar chhod diya hai toh aapka last working day kab tha?
2. Kya aapke paas employment ka koi proof hai – offer letter, payslips, salary credit dikhane wale bank statements, ya ID card?
3. Kya aapne factory/HR ko unpaid wages ke baare mein likha ya bola hai? Haan toh unhone kya kaha?

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['COW2019-S45', 'COW2019-S17']

## Final case file

```json
{
 "category": "salary",
 "language": "Hinglish",
 "script": "Latin",
 "facts": {
  "other_party_name": "thekedar",
  "role": "helper",
  "monthly_salary": 14000,
  "unpaid_period": "2 months",
  "amount_due": 28000,
  "city_state": "Ghaziabad"
 },
 "timeline": [],
 "evidence_have": [],
 "evidence_missing": [
  "employment proof",
  "communication with factory/HR"
 ],
 "next_step": "Ask for the missing facts"
}
```

## Automatic checks

| check | pass | detail |
|---|---|---|
| category | ✅ | got salary |
| reply_language | ✅ | expected Hinglish, reply script Hinglish |
| fact:monthly_salary | ✅ | expected ~14, got 14000 |
| mentions:labour|Labour|श्रम|Inspector|inspector | ❌ |  |
| escalation<=urgent | ✅ | got none |
| no_unverified_law_shown | ✅ |  |
