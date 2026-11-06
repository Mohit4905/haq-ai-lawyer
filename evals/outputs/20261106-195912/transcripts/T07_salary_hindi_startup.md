# T07_salary_hindi_startup
Group: core

## Turn 1

**User:** मैं नोएडा की एक स्टार्टअप में सॉफ्टवेयर डेवलपर था, सैलरी 70,000 महीना। अगस्त और सितंबर 2026 की सैलरी नहीं मिली। मैंने 30 सितंबर 2026 को रिज़ाइन कर दिया था, आख़िरी दिन वही था। HR कहता है कंपनी घाटे में है, बाद में देंगे। ऑफ़र लेटर और पुरानी सैलरी स्लिप मेरे पास हैं।

**Haq** (gemini/gemini-3.1-flash-lite, 6.88s):

नमस्ते। देखिए, कंपनी का 'घाटे में होना' आपकी सैलरी न देने का कोई कानूनी आधार नहीं है। कानून के मुताबिक, इस्तीफा देने के बाद आपका पूरा हिसाब (Full and Final Settlement) 2 कार्य दिवसों (working days) के भीतर हो जाना चाहिए था। आपके पास ऑफर लेटर और सैलरी स्लिप्स हैं, जो कि बहुत मजबूत सबूत हैं। HR का 'बाद में देंगे' कहना सिर्फ टालमटोल है, इसे लिखित में न लें।

**मेरी राय:** आपका केस काफी मजबूत है। कंपनी को यह साबित करना होगा कि उन्होंने भुगतान क्यों नहीं किया, और 'घाटा' कोई वैध कारण नहीं है। हमें अब दबाव बनाने की जरूरत है।

**कानून आपकी तरफ:**
*   **Code on Wages, 2019 (Section 17):** इस्तीफा देने या नौकरी छोड़ने पर, आपकी बकाया सैलरी 2 कार्य दिवसों के भीतर मिल जानी चाहिए।
*   **Code on Wages, 2019 (Section 45):** आप लेबर अथॉरिटी (Labour Authority) के पास शिकायत दर्ज कर सकते हैं, जो आपकी बकाया राशि वसूलने में मदद कर सकती है।

**वे क्या कहेंगे और आपका जवाब:**
*   वे कहेंगे: "कंपनी घाटे में है, थोड़ा इंतज़ार करें।" जवाब: "कानून के तहत सैलरी मेरा अधिकार है, यह कंपनी के मुनाफे पर निर्भर नहीं है। कृपया भुगतान की तारीख लिखित में दें।"

**मैं क्या करूँगा:**
1. आज ही HR को एक औपचारिक ईमेल भेजें (मैं इसका ड्राफ्ट दे सकता हूँ), जिसमें बकाया राशि और भुगतान की समय सीमा (जैसे 7 दिन) का स्पष्ट उल्लेख हो।
2. अगर 7 दिन में जवाब या पैसा न आए, तो हम नोएडा के लेबर कमिश्नर (Labour Commissioner) के पास शिकायत दर्ज करेंगे।

**मुझे आपसे चाहिए:**
1. क्या आपने HR को अब तक कोई ईमेल भेजा है जिसमें आपने सैलरी की मांग की हो?
2. कंपनी का नाम क्या है?

**Calculated by code:** {"deadlines": [{"label": "Employer had to pay your full & final wages by (2 working days after you left)", "date": "2026-10-02", "days_left": -35, "status": "passed", "basis": "COW2019-S17", "note": "This is the employer's legal deadline; if it has passed, the employer is in default. Assumes a Mon–Sat working week.", "user_deadline": false}, {"label": "Approximate last date to file a wage claim with the labour authority (3 years)", "date": "2029-09-30", "days_left": 1059, "status": "ok", "basis": "COW2019-S45", "note": "", "user_deadline": true}], "derived": []}

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['COW2019-S17', 'COW2019-S45']

## Final case file

```json
{
 "category": "salary",
 "language": "Hindi",
 "script": "Devanagari",
 "facts": {
  "role": "Software Developer",
  "monthly_salary": "70000",
  "unpaid_period": "August 2026 and September 2026",
  "amount_due": "140000",
  "still_employed": "false",
  "employment_proof": "Offer letter and salary slips",
  "city_state": "Noida",
  "summary": "User is claiming unpaid salary for August and September 2026 after resigning on 2026-09-30.",
  "last_working_day": "2026-09-30"
 },
 "timeline": [
  {
   "date": "2026-09-30",
   "event": "Resignation date"
  }
 ],
 "evidence_have": [
  "Offer letter",
  "Salary slips"
 ],
 "evidence_missing": [
  "Written communication with HR regarding unpaid salary"
 ],
 "next_step": "Draft a formal demand email to HR"
}
```

## Draft document

LEGAL NOTICE

By Registered Post A.D. / Speed Post / Email

Date: [[FILL: date]]

From:
[[FILL: your full name]]
[[FILL: your address]]
[[FILL: your phone and email]]

To:
[[FILL: employer's name/HR manager name]]
[[FILL: company name]]
[[FILL: company address]]

Subject: Demand for payment of outstanding salary dues.

Dear Sir/Madam,

1. I was employed as a Software Developer at [[FILL: company name]] from [[FILL: date of joining]] until my resignation on 30 September 2026.

2. My monthly salary was Rs. 70,000. Despite my service, my salary for the months of August 2026 and September 2026, amounting to a total of Rs. 1,40,000, remains unpaid.

3. As per the Code on Wages, 2019, wages must be paid in a timely manner. Upon the termination of employment, all dues must be settled promptly. My last working day was 30 September 2026, and the statutory deadline for the settlement of my full and final dues has long since passed.

4. I have previously requested the release of these funds, but the payments remain outstanding.

5. This notice serves as a formal demand for the payment of Rs. 1,40,000. Please remit this amount to my bank account within 15 days of receiving this notice. My bank details are as follows: [[FILL: your bank details (account name, number, bank, IFSC)]].

6. If you fail to clear these dues within the specified period, I shall be constrained to initiate appropriate legal proceedings, including filing a claim before the relevant labour authority and/or pursuing civil recovery, at your sole risk, cost, and consequence.

Copy retained for record.

Sincerely,

[[FILL: your full name]]
[[FILL: your phone and email]]

**Send instructions:** ["इस नोटिस को ईमेल और रजिस्टर्ड पोस्ट (Registered Post A.D.) दोनों के माध्यम से भेजें।", "रजिस्टर्ड पोस्ट की रसीद (receipt) और ट्रैकिंग रिपोर्ट को संभाल कर रखें, यह कोर्ट में सबूत के तौर पर काम आएगी।", "ईमेल भेजते समय 'Read Receipt' का विकल्प चुनें ताकि आपको पता चल सके कि उन्होंने ईमेल खोल लिया है।", "यदि 15 दिनों के भीतर कोई जवाब या भुगतान नहीं मिलता है, तो आप नोएडा के लेबर कमिश्नर कार्यालय (Labour Commissioner Office) में शिकायत दर्ज कर सकते हैं।", "आप अपनी शिकायत 'SAMADHAN' पोर्टल (https://samadhan.labour.gov.in) पर भी ऑनलाइन दर्ज कर सकते हैं।"]

## Automatic checks

| check | pass | detail |
|---|---|---|
| category | ✅ | got salary |
| reply_language | ✅ | expected Devanagari, reply script Devanagari |
| fact:monthly_salary | ✅ | expected ~70, got 70000 |
| fact:last_working_day | ✅ | expected ~2026-09-30, got 2026-09-30 |
| escalation<=urgent | ✅ | got none |
| no_unverified_law_shown | ✅ |  |
| draft_no_unverified_law | ✅ | [] |
| draft_has_no_invented_fill | ✅ | 9 placeholders |
