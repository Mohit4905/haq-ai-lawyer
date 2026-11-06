# T12_notice_explain_hindi
Group: core

## Turn 1

**User:** मुझे वकील का नोटिस आया है अंग्रेज़ी में, समझ नहीं आ रहा। लिखा है: 'Under instructions from my client Mr. S.K. Verma, I hereby call upon you to pay Rs. 1,00,000 towards damages caused to the premises at Flat 4B, Indirapuram, within 15 days of receipt of this notice, failing which my client shall initiate appropriate civil proceedings against you at your risk as to costs.' मैंने वो फ्लैट 2 महीने पहले खाली किया था और कोई नुकसान नहीं किया।

**Haq** (gemini/gemini-3.1-flash-lite, 10.38s):

घबराइए मत, यह एक कानूनी नोटिस (legal notice) है। इसका मतलब यह नहीं है कि आप दोषी हैं, बल्कि यह एक औपचारिक तरीका है अपनी बात रखने का। चूंकि आपने फ्लैट 2 महीने पहले खाली कर दिया था, इसलिए 'नुकसान' (damages) का आरोप साबित करने की जिम्मेदारी मकान मालिक की है। अगर आपके पास फ्लैट की अच्छी स्थिति के सबूत हैं, तो आप इस नोटिस का मजबूती से जवाब दे सकते हैं।

**आपकी कानूनी स्थिति:**
कानून के अनुसार, मकान मालिक को यह साबित करना होगा कि नुकसान आपकी वजह से हुआ है। अगर आपने फ्लैट सही स्थिति में छोड़ा था, तो आप इन आरोपों को पूरी तरह नकार सकते हैं।

**कानून जो आप इस्तेमाल कर सकते हैं:**
* **Indian Contract Act, 1872 (Section 73):** यह कहता है कि नुकसान के लिए केवल वही राशि मांगी जा सकती है जो वास्तव में हुई हो और जिसे साबित किया जा सके।
* **Model Tenancy Act, 2021 (Section 11):** यह स्पष्ट करता है कि सुरक्षा जमा (security deposit) और नुकसान के दावों के लिए मकान मालिक को उचित प्रक्रिया का पालन करना होता है।

**अब क्या करें:**
1. नोटिस को नजरअंदाज न करें; 15 दिन की समय सीमा महत्वपूर्ण है।
2. एक औपचारिक जवाब (reply) तैयार करें जिसमें आप इन आरोपों को स्पष्ट रूप से नकारें।
3. फ्लैट खाली करते समय की कोई भी फोटो, वीडियो या हैंडओवर रसीद ढूंढें।

**मुझे आपसे ये जानना है:**
1. यह नोटिस आपको किस तारीख को मिला था?
2. क्या फ्लैट खाली करते समय आपने कोई फोटो या वीडियो ली थी, या कोई 'हैंडओवर' डॉक्यूमेंट साइन किया था?

_Escalation:_ {"level": "recommended", "reasons": ["The notice threatens legal proceedings: get it reviewed", "Since this is a formal legal notice demanding a significant amount, a lawyer should review your reply to ensure it is legally sound."]}  _Citations:_ ['ICA1872-S73', 'MTA2021-S11']

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
  }
 ],
 "evidence_have": [],
 "evidence_missing": [
  "Photos or videos of the flat at the time of vacating",
  "Handover document or email communication",
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
