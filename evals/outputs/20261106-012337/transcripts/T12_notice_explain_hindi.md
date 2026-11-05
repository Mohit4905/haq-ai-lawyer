# T12_notice_explain_hindi
Group: core

## Turn 1

**User:** मुझे वकील का नोटिस आया है अंग्रेज़ी में, समझ नहीं आ रहा। लिखा है: 'Under instructions from my client Mr. S.K. Verma, I hereby call upon you to pay Rs. 1,00,000 towards damages caused to the premises at Flat 4B, Indirapuram, within 15 days of receipt of this notice, failing which my client shall initiate appropriate civil proceedings against you at your risk as to costs.' मैंने वो फ्लैट 2 महीने पहले खाली किया था और कोई नुकसान नहीं किया।

**Haq** (gemini/gemini-3.1-flash-lite, 5.49s):

घबराइए मत, यह नोटिस सिर्फ एक कानूनी मांग (legal demand) है, कोई कोर्ट का फैसला नहीं। इसका मतलब है कि मकान मालिक आपसे पैसे मांग रहे हैं और अगर आप नहीं देंगे, तो वे कोर्ट जा सकते हैं।

चूंकि आपने फ्लैट 2 महीने पहले खाली किया था, तो आपके पास अपनी बात रखने का पूरा मौका है।

**आपको अभी क्या करना है:**
1. **नोटिस को अनदेखा न करें:** 15 दिन की समय सीमा (deadline) महत्वपूर्ण है।
2. **सबूत इकट्ठा करें:** क्या आपके पास फ्लैट खाली करते समय की फोटो या वीडियो है? क्या मकान मालिक ने उस समय कोई शिकायत की थी? क्या आपने रेंट एग्रीमेंट (rent agreement) की कॉपी रखी है?
3. **जवाब दें:** आपको इस नोटिस का लिखित जवाब (written reply) देना चाहिए, जिसमें आप स्पष्ट रूप से कहें कि आपने कोई नुकसान नहीं किया है।

**अगला कदम:**
क्या आपको याद है कि आपको यह नोटिस किस तारीख को मिला था? अगर आप चाहें, तो मैं आपको एक ड्राफ्ट (draft) तैयार करने में मदद कर सकता हूँ जिसे आप वकील को भेज सकते हैं।

_Escalation:_ {"level": "recommended", "reasons": ["The notice threatens legal proceedings: get it reviewed", "Since the claim amount is significant (1 lakh), having a lawyer review your reply is safer."]}  _Citations:_ []

## Final case file

```json
{
 "category": "notice",
 "language": "Hindi",
 "script": "Devanagari",
 "facts": {
  "notice_from": "Mr. S.K. Verma",
  "notice_demands": "100000",
  "notice_deadline_days": 15,
  "notice_text": "Under instructions from my client Mr. S.K. Verma, I hereby call upon you to pay Rs. 1,00,000 towards damages caused to the premises at Flat 4B, Indirapuram, within 15 days of receipt of this notice, failing which my client shall initiate appropriate civil proceedings against you at your risk as to costs.",
  "summary": "User received a legal notice from landlord Mr. S.K. Verma demanding 1 lakh for alleged damages to a flat vacated 2 months ago."
 },
 "timeline": [
  {
   "date": "2 months ago",
   "event": "Flat vacated"
  },
  {
   "date": "Recently",
   "event": "Received legal notice"
  }
 ],
 "evidence_have": [],
 "evidence_missing": [
  "Date of receipt of notice",
  "Photos/videos of flat condition at time of vacating",
  "Rent agreement copy",
  "Any communication with landlord regarding damages"
 ],
 "next_step": "Draft a formal reply to the notice denying the damages."
}
```

## Automatic checks

| check | pass | detail |
|---|---|---|
| category | ✅ | got notice |
| reply_language | ✅ | expected Devanagari, reply script Devanagari |
| mentions:15 | ✅ |  |
| mentions:जवाब|reply|रिप्लाई | ✅ |  |
| escalation>=recommended | ✅ | got recommended |
| no_unverified_law_shown | ✅ |  |
