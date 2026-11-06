# T07_salary_hindi_startup
Group: core

## Turn 1

**User:** मैं नोएडा की एक स्टार्टअप में सॉफ्टवेयर डेवलपर था, सैलरी 70,000 महीना। अगस्त और सितंबर 2026 की सैलरी नहीं मिली। मैंने 30 सितंबर 2026 को रिज़ाइन कर दिया था, आख़िरी दिन वही था। HR कहता है कंपनी घाटे में है, बाद में देंगे। ऑफ़र लेटर और पुरानी सैलरी स्लिप मेरे पास हैं।

**Haq** (gemini/gemini-3.1-flash-lite, 7.44s):

नमस्ते। मैं हक़ हूँ। आपकी स्थिति को देखते हुए, कानून स्पष्ट है: कंपनी का घाटे में होना आपकी मेहनत की कमाई को रोकने का कोई कानूनी आधार नहीं है। Code on Wages, 2019 के तहत, नौकरी छोड़ने या निकाले जाने पर आपका अंतिम वेतन (full and final settlement) 2 कार्य दिवसों के भीतर मिलना चाहिए। आपके पास ऑफर लेटर और सैलरी स्लिप्स हैं, जो आपके दावे को मजबूत बनाती हैं।

**आपकी कानूनी स्थिति:**
आपकी स्थिति काफी स्पष्ट है क्योंकि आपके पास रोजगार का प्रमाण है। कानून के अनुसार, वेतन आपका अधिकार है, न कि कंपनी की मर्जी।

**कानून जो आप बता सकते हैं:**
*   **Code on Wages, 2019, Section 17:** कहता है कि नौकरी छोड़ने पर अंतिम वेतन 2 कार्य दिवसों के भीतर मिलना चाहिए। यह आपके मामले में सबसे महत्वपूर्ण है।
*   **Code on Wages, 2019, Section 45:** आपको लेबर अथॉरिटी (Labour Authority) के पास शिकायत दर्ज करने का अधिकार देता है, जो 3 साल तक मान्य है।

**अब क्या करें:**
1. कंपनी को एक औपचारिक ईमेल भेजें (अगर नहीं भेजा है), जिसमें बकाया राशि और भुगतान की समय सीमा (जैसे 7 दिन) लिखें।
2. यदि वे जवाब न दें, तो नोएडा के लेबर ऑफिस में 'Inspector-cum-Facilitator' के पास शिकायत दर्ज करें।
3. आप SAMADHAN पोर्टल (samadhan.labour.gov.in) पर भी ऑनलाइन शिकायत कर सकते हैं।
4. किसी भी कानूनी सहायता के लिए 15100 (NALSA) पर कॉल करें।

मेरा सुझाव है कि आप सबसे पहले कंपनी को एक औपचारिक ईमेल भेजें। क्या आप चाहते हैं कि मैं उस ईमेल का ड्राफ्ट तैयार करने में आपकी मदद करूँ?

**Calculated by code:** {"deadlines": [{"label": "Employer had to pay your full & final wages by (2 working days after you left)", "date": "2026-10-02", "days_left": -35, "status": "passed", "basis": "COW2019-S17", "note": "This is the employer's legal deadline; if it has passed, the employer is in default. Assumes a Mon–Sat working week.", "user_deadline": false}, {"label": "Approximate last date to file a wage claim with the labour authority (3 years)", "date": "2029-09-30", "days_left": 1059, "status": "ok", "basis": "COW2019-S45", "note": "", "user_deadline": true}], "derived": []}

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['COW2019-S17', 'COW2019-S45', 'FACT-SAMADHAN-PORTAL', 'FACT-NALSA-HELPLINE']

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
   "event": "Resigned from the company"
  }
 ],
 "evidence_have": [
  "Offer letter",
  "Salary slips"
 ],
 "evidence_missing": [
  "Written communication with HR regarding unpaid salary"
 ],
 "next_step": "Send a formal email to the employer demanding the unpaid salary within a specific deadline."
}
```

## Draft document

LEGAL NOTICE
(Sent by Registered Post A.D. / Speed Post)
Date: [[FILL: Current Date]]

From:
[[FILL: Your Name]]
[[FILL: Your Address]]

To:
[[FILL: Employer Name/HR Manager]]
[[FILL: Company Name]]
[[FILL: Company Address]]

Subject: Demand for payment of outstanding salary for August and September 2026.

Dear Sir/Madam,

1. I was employed as a Software Developer at [[FILL: Company Name]] from [[FILL: Start Date]] to 2026-09-30.

2. My last working day with the company was 2026-09-30.

3. My monthly salary was Rs. 70,000.

4. My salary for the months of August 2026 and September 2026, totaling Rs. 1,40,000, remains unpaid. Despite my resignation, the full and final settlement has not been processed.

5. I have been informed by the HR department that the payment is delayed due to financial losses, but no concrete timeline for payment has been provided.

6. Under Section 17 of the Code on Wages, 2019, wages must be paid within the prescribed time limits, including upon resignation. The failure to pay my earned wages is a violation of these provisions.

7. I hereby demand that you pay the outstanding amount of Rs. 1,40,000 within 15 days of the receipt of this notice. Please transfer the amount to the following bank account:
Bank Name: [[FILL: Bank Name]]
Account Number: [[FILL: Account Number]]
IFSC Code: [[FILL: IFSC Code]]

8. If you fail to comply with this demand within the stipulated period, I shall be constrained to initiate legal proceedings, including filing a formal claim before the appropriate labour authority under Section 45 of the Code on Wages, 2019, at your cost and risk.

Copy retained for record.

Sincerely,

[[FILL: Your Name]]
[[FILL: Your Phone Number]]
[[FILL: Your Email Address]]

**Send instructions:** ["इस नोटिस का प्रिंट निकालें और उस पर अपने हस्ताक्षर करें।", "इसे 'Registered Post A.D.' या 'Speed Post' के माध्यम से कंपनी के पते पर भेजें।", "पोस्ट ऑफिस से मिली रसीद (Receipt) को संभाल कर रखें, यह भविष्य में सबूत के तौर पर काम आएगी।", "यदि 15 दिनों के भीतर जवाब या भुगतान नहीं मिलता है, तो आप 'SAMADHAN' पोर्टल (samadhan.labour.gov.in) पर शिकायत दर्ज कर सकते हैं।"]

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
| draft_has_no_invented_fill | ✅ | 12 placeholders |
