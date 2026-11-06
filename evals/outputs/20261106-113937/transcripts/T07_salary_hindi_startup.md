# T07_salary_hindi_startup
Group: core

## Turn 1

**User:** मैं नोएडा की एक स्टार्टअप में सॉफ्टवेयर डेवलपर था, सैलरी 70,000 महीना। अगस्त और सितंबर 2026 की सैलरी नहीं मिली। मैंने 30 सितंबर 2026 को रिज़ाइन कर दिया था, आख़िरी दिन वही था। HR कहता है कंपनी घाटे में है, बाद में देंगे। ऑफ़र लेटर और पुरानी सैलरी स्लिप मेरे पास हैं।

**Haq** (gemini/gemini-3.1-flash-lite, 8.91s):

नमस्ते। आपकी स्थिति काफी स्पष्ट है और कानून आपके साथ है। कंपनी का 'घाटे में होना' आपकी मेहनत की कमाई रोकने का कोई कानूनी आधार नहीं है। आपके पास ऑफ़र लेटर और सैलरी स्लिप्स जैसे ठोस सबूत हैं, जो यह साबित करने के लिए काफी हैं कि आपका वेतन बकाया है। कानून के अनुसार, इस्तीफे के बाद अंतिम वेतन 2 कार्य दिवसों के भीतर मिल जाना चाहिए।

**आपकी कानूनी स्थिति:**
आपकी स्थिति मजबूत है क्योंकि आपके पास रोजगार का लिखित प्रमाण है। कंपनी का यह कहना कि 'बाद में देंगे' केवल टालमटोल है, और आप इसके खिलाफ कानूनी कार्रवाई कर सकते हैं।

**कानून जो आप उद्धृत कर सकते हैं:**
* **Code on Wages, 2019, Section 17:** यह कहता है कि इस्तीफा देने पर आपका अंतिम वेतन 2 कार्य दिवसों के भीतर मिलना चाहिए।
* **Code on Wages, 2019, Section 45:** यह आपको श्रम अधिकारी (Labour Authority) के पास बकाया वेतन के लिए दावा करने का अधिकार देता है।

**अब क्या करें:**
1. **ईमेल/नोटिस:** कंपनी को एक औपचारिक 'डिमांड नोटिस' भेजें जिसमें बकाया राशि और भुगतान की समय सीमा (15 दिन) का उल्लेख हो।
2. **SAMADHAN पोर्टल:** यदि कंपनी जवाब न दे, तो श्रम मंत्रालय के SAMADHAN पोर्टल (samadhan.labour.gov.in) पर शिकायत दर्ज करें।
3. **श्रम कार्यालय:** अपने क्षेत्र के 'Inspector-cum-Facilitator' के पास शिकायत दर्ज करें।

मेरी सलाह है कि आप सबसे पहले कंपनी को एक औपचारिक ईमेल (डिमांड नोटिस) भेजें। क्या आप चाहते हैं कि मैं इसका ड्राफ्ट तैयार करने में आपकी मदद करूँ?

**मुझे आपसे यह जानना है:**
1. कंपनी का पूरा नाम क्या है?
2. क्या आपने HR को ईमेल पर वेतन के बारे में कोई लिखित सवाल पूछा है?

**Calculated by code:** {"deadlines": [{"label": "Employer had to pay your full & final wages by (2 working days after you left)", "date": "2026-10-02", "days_left": -35, "status": "passed", "basis": "COW2019-S17", "note": "This is the employer's legal deadline; if it has passed, the employer is in default. Assumes a Mon–Sat working week.", "user_deadline": false}, {"label": "Approximate last date to file a wage claim with the labour authority (3 years)", "date": "2029-09-30", "days_left": 1059, "status": "ok", "basis": "COW2019-S45", "note": "", "user_deadline": true}], "derived": []}

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['COW2019-S17', 'COW2019-S45', 'FACT-SAMADHAN-PORTAL']

## Final case file

```json
{
 "category": "salary",
 "language": "Hindi",
 "script": "Devanagari",
 "facts": {
  "role": "Software Developer",
  "monthly_salary": 70000,
  "unpaid_period": "August 2026, September 2026",
  "amount_due": 140000,
  "still_employed": "false",
  "employment_proof": "Offer letter, salary slips",
  "city_state": "Noida",
  "summary": "User is claiming unpaid salary for August and September 2026 after resigning on 2026-09-30.",
  "last_working_day": "2026-09-30"
 },
 "timeline": [
  {
   "date": "2026-09-30",
   "event": "Resignation"
  }
 ],
 "evidence_have": [
  "Offer letter",
  "Salary slips"
 ],
 "evidence_missing": [
  "Written communication from HR regarding the delay"
 ],
 "next_step": "Draft a formal demand notice to the HR/Employer."
}
```

## Draft document

LEGAL NOTICE
By Registered Post A.D.
Date: [[FILL: Date]]

From:
[[FILL: Your Name]]
[[FILL: Your Address]]

To:
[[FILL: HR Manager/Director Name]]
[[FILL: Company Name]]
[[FILL: Company Address]]

Subject: Demand for payment of outstanding salary amounting to Rs. 1,40,000/-.

1. I was employed as a Software Developer with your company, [[FILL: Company Name]], at a monthly salary of Rs. 70,000/-.

2. I resigned from my position on 30 September 2026, which was my last working day.

3. Despite my service, my salary for the months of August 2026 and September 2026, totaling Rs. 1,40,000/-, remains unpaid.

4. I have previously requested the release of these dues, but I was informed by your HR department that the company is currently in financial loss and that payment would be made at a later date.

5. Under Section 17 of the Code on Wages, 2019, wages must be paid in full upon the termination of employment. The delay in settling my dues is a violation of this provision.

6. I hereby demand that you pay the outstanding amount of Rs. 1,40,000/- within 15 days of receiving this notice. Please remit the payment to the following bank account: [[FILL: Bank Name]], Account Number: [[FILL: Account Number]], IFSC: [[FILL: IFSC Code]].

7. If you fail to comply with this demand within the stipulated period, I shall be constrained to initiate legal proceedings, including filing a claim before the appropriate labour authority, at your sole risk, cost, and consequence.

8. Copy retained for record.

[[FILL: Your Name]]
[[FILL: Your Phone Number]]
[[FILL: Your Email Address]]

**Send instructions:** ["इस नोटिस का प्रिंट निकालें और उस पर अपने हस्ताक्षर करें।", "इसे 'Registered Post A.D.' के माध्यम से कंपनी के पते पर भेजें। पोस्ट ऑफिस से मिलने वाली रसीद को संभाल कर रखें।", "अगर कंपनी का ईमेल पता है, तो इस नोटिस की एक स्कैन कॉपी ईमेल पर भी भेजें।", "अगर 15 दिनों के भीतर कोई जवाब या भुगतान नहीं मिलता है, तो आप 'SAMADHAN' पोर्टल (https://samadhan.labour.gov.in) पर अपनी शिकायत दर्ज कर सकते हैं।", "कानूनी सलाह के लिए आप 15100 (NALSA हेल्पलाइन) पर कॉल कर सकते हैं या अपने नजदीकी कॉमन सर्विस सेंटर (CSC) पर जाकर 'Tele-Law' सेवा का उपयोग कर सकते हैं।"]

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
| draft_has_no_invented_fill | ✅ | 11 placeholders |
