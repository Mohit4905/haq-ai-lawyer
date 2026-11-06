# T12_notice_explain_hindi
Group: core

## Turn 1

**User:** मुझे वकील का नोटिस आया है अंग्रेज़ी में, समझ नहीं आ रहा। लिखा है: 'Under instructions from my client Mr. S.K. Verma, I hereby call upon you to pay Rs. 1,00,000 towards damages caused to the premises at Flat 4B, Indirapuram, within 15 days of receipt of this notice, failing which my client shall initiate appropriate civil proceedings against you at your risk as to costs.' मैंने वो फ्लैट 2 महीने पहले खाली किया था और कोई नुकसान नहीं किया।

**Haq** (gemini/gemini-3.1-flash-lite, 9.68s):

घबराइए मत, यह एक कानूनी नोटिस है, लेकिन इसका मतलब यह नहीं कि आप गलत हैं। दो महीने बाद 1 लाख रुपये का दावा करना बहुत संदिग्ध है। जब आपने फ्लैट खाली किया था, तब उन्होंने कोई आपत्ति क्यों नहीं जताई? कानून के अनुसार, उन्हें यह साबित करना होगा कि नुकसान आपकी वजह से हुआ है और वह 'सामान्य टूट-फूट' (normal wear and tear) से ज्यादा है।

**मेरी राय:** आपका केस मजबूत है क्योंकि आपने फ्लैट दो महीने पहले खाली कर दिया था। अगर कोई नुकसान होता, तो उन्हें पजेशन (possession) लेते समय ही बताना चाहिए था। अब वे जो दावा कर रहे हैं, उसे साबित करने की जिम्मेदारी पूरी तरह से उन पर है।

**कानून आपकी तरफ है:**
*   भारतीय अनुबंध अधिनियम (Indian Contract Act, 1872) की धारा 73 के तहत, उन्हें यह साबित करना होगा कि नुकसान वास्तव में हुआ है और वह आपकी लापरवाही का नतीजा है। वे मनमाना जुर्माना नहीं लगा सकते।

**वे क्या कहेंगे और आपका जवाब:**
*   वे कह सकते हैं कि उन्हें नुकसान बाद में पता चला। आप जवाब देंगे कि पजेशन लेते समय उन्होंने फ्लैट का निरीक्षण (inspection) किया था और तब कोई शिकायत नहीं थी।

**मैं क्या करूँगा:**
1. आज ही एक लिखित जवाब (Reply) तैयार करें। इसमें स्पष्ट रूप से लिखें कि आपने फ्लैट सही स्थिति में सौंपा था और यह दावा निराधार है।
2. उनसे उन बिलों या सबूतों की मांग करें जिनके आधार पर वे 1 लाख रुपये मांग रहे हैं।
3. अगर आपके पास फ्लैट खाली करते समय की कोई फोटो या वीडियो है, तो उसे संभाल कर रखें।

**मुझे आपसे यह जानना है:**
1. यह नोटिस आपको किस तारीख को मिला था? (ताकि हम 15 दिन की समय सीमा का हिसाब रख सकें)
2. क्या फ्लैट खाली करते समय आपने कोई 'हैंडओवर डॉक्यूमेंट' (handover document) साइन किया था या कोई ईमेल/मैसेज भेजा था?

_Escalation:_ {"level": "recommended", "reasons": ["The notice threatens legal proceedings: get it reviewed", "The amount is significant (1 lakh) and it is a formal legal notice."]}  _Citations:_ ['ICA1872-S73']

## Final case file

```json
{
 "category": "notice",
 "language": "Hindi",
 "script": "Devanagari",
 "facts": {
  "notice_from": "Mr. S.K. Verma",
  "notice_demands": "100000",
  "notice_deadline_days": "15",
  "notice_text": "Under instructions from my client Mr. S.K. Verma, I hereby call upon you to pay Rs. 1,00,000 towards damages caused to the premises at Flat 4B, Indirapuram, within 15 days of receipt of this notice, failing which my client shall initiate appropriate civil proceedings against you at your risk as to costs.",
  "possession_handed_over_date": "2026-09-01",
  "summary": "User received a legal notice from landlord Mr. S.K. Verma demanding 1 lakh for alleged damages to a flat vacated 2 months ago."
 },
 "timeline": [
  {
   "date": "2026-09-01",
   "event": "Flat vacated"
  },
  {
   "date": "Today",
   "event": "Received legal notice"
  }
 ],
 "evidence_have": [],
 "evidence_missing": [
  "Photos/videos of flat at handover",
  "Handover document/email",
  "Date of receipt of notice"
 ],
 "next_step": "Draft a formal reply to the notice denying the claims.",
 "approximate": [
  "possession_handed_over_date"
 ]
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
