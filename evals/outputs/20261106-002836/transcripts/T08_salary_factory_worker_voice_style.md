# T08_salary_factory_worker_voice_style
Group: core

## Turn 1

**User:** sir main factory me helper hu ghaziabad me thekedar ke through kaam karta tha 14000 mahina milta tha do mahine se paisa nahi diya thekedar bhag gaya company bolti hai thekedar se lo ab kya karu ghar ka kiraya bhi nahi de pa raha

**Haq** (groq/qwen/qwen3.8-27b, 7.42s):

Bhai, tension mat lo — aapka case clear hai. Company bol rahi hai 'thekedar se lo', lekin law ke hisaab se **company (principal employer) hi aapki salary dene ke liye zimmedar hai**. Thekedar aapka agent hai, company uske through aapko employ kar rahi hai. Code on Wages, 2019 ke under aap 'employee' ho, chahe thekedar ke through hi kyun na kaam karo.

**Abhi kya karein:**

1. **Aaj hi company ko likh kar demand karo** — email ya WhatsApp pe, jo bhi ho. Likho: 'Main [naam], [date] se helper hu, 2 mahine ki salary Rs 28,000 due hai. Thekedar available nahi hai. Company principal employer hai, salary do.'
2. Screenshot/photo save karo har message ka.
3. Agar 7-10 din me nahi diya, to **labour office (Inspector-cum-Facilitator)** me complaint file karo — free hai, 3 saal ka time hai.

**Mujhe batao:**
- Koi ID card, attendance register, ya bank me salary aane ki entry hai?
- Company ka naam kya hai aur aapne unhe likh kar kaha hai abhi tak?

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['COW2019-S2K', 'FACT-COW-NO-WAGE-CEILING', 'COW2019-S45', 'COW2019-S51']

## Final case file

```json
{
 "category": "salary",
 "language": "Hinglish",
 "script": "Latin",
 "facts": {
  "other_party_name": "thekedar (contractor) + company (principal employer)",
  "role": "helper",
  "monthly_salary": 14000,
  "unpaid_period": "2 months",
  "amount_due": 28000,
  "still_employed": true,
  "city_state": "Ghaziabad, Uttar Pradesh",
  "summary": "Helper in factory via thekedar; thekedar ran away; company refuses to pay saying 'go to thekedar'; 2 months unpaid (Rs 28,000)"
 },
 "timeline": [],
 "evidence_have": [],
 "evidence_missing": [
  "ID card / worker ID from company",
  "Attendance register or biometric records",
  "Bank statements showing earlier salary credits",
  "Any written communication with company or thekedar",
  "Name of the company / factory"
 ],
 "next_step": "Write a demand message to the company (principal employer) today, stating 2 months unpaid salary of Rs 28,000, and save the screenshot"
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
