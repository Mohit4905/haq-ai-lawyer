# T12_notice_explain_hindi
Group: core

## Turn 1

**User:** मुझे वकील का नोटिस आया है अंग्रेज़ी में, समझ नहीं आ रहा। लिखा है: 'Under instructions from my client Mr. S.K. Verma, I hereby call upon you to pay Rs. 1,00,000 towards damages caused to the premises at Flat 4B, Indirapuram, within 15 days of receipt of this notice, failing which my client shall initiate appropriate civil proceedings against you at your risk as to costs.' मैंने वो फ्लैट 2 महीने पहले खाली किया था और कोई नुकसान नहीं किया।

**Haq** (groq/openai/gpt-oss-120b, 18.71s):

Aapko jo notice mila hai, usme 15 din ka deadline diya gaya hai. Pehle yeh confirm kar lein:
- Notice aapko kis date ko mila? (notice_received_date)
- Notice me likhi date kya hai? (notice_date)
Aapke paas jo proof hai, jaise ki vacancy ka handover receipt, photos ya koi communication, usko ikattha kar lein. Agar aapko lagta hai ki aapne koi nuksan nahi kiya, to aap ek **written reply** (reply_to_notice) bhej sakte hain, jisme:
- Notice receive karne ki date mention ho
- Aapka version (flat 2 mahine pehle khali kiya, koi nuksan nahi) likhen
- Saare supporting documents attach karen
Yeh reply deadline se pehle bhejna chahiye, taki aapka side record ho. Agar aapko likhne me help chahiye, to main draft bana ke de sakta hoon.

**Agle kadam:** Notice receive date aur notice date confirm karen, aur aapke paas jo proof hai uski list bana lein.

_Escalation:_ {"level": "recommended", "reasons": ["If the other side does not accept your reply, you may need legal counsel for civil suit defense."]}  _Citations:_ []

## Final case file

```json
{
 "category": "notice",
 "language": "Hinglish",
 "script": "Latin",
 "facts": {
  "notice_from": "Mr. S.K. Verma",
  "notice_demands": 100000,
  "notice_deadline_days": 15,
  "notice_text": "Under instructions from my client Mr. S.K. Verma, I hereby call upon you to pay Rs. 1,00,000 towards damages caused to the premises at Flat 4B, Indirapuram, within 15 days of receipt of this notice, failing which my client shall initiate appropriate civil proceedings against you at your risk as to costs.",
  "other_party_name": "Mr. S.K. Verma",
  "city_state": "Indirapuram"
 },
 "timeline": [],
 "evidence_have": [],
 "evidence_missing": [
  "Notice date",
  "Date you received the notice",
  "Hand over/vacancy receipt",
  "Photos of flat condition",
  "Any communication with Mr. Verma about the handover"
 ],
 "next_step": "Confirm notice_date and notice_received_date, and gather proof of vacancy handover."
}
```

## Automatic checks

| check | pass | detail |
|---|---|---|
| category | ✅ | got notice |
| reply_language | ❌ | expected Devanagari, reply script Hinglish |
| mentions:15 | ✅ |  |
| mentions:जवाब|reply|रिप्लाई | ✅ |  |
| escalation>=recommended | ✅ | got recommended |
| no_unverified_law_shown | ✅ |  |
