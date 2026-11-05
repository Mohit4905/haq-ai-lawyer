# T07_salary_hindi_startup
Group: core

## Turn 1

**User:** मैं नोएडा की एक स्टार्टअप में सॉफ्टवेयर डेवलपर था, सैलरी 70,000 महीना। अगस्त और सितंबर 2026 की सैलरी नहीं मिली। मैंने 30 सितंबर 2026 को रिज़ाइन कर दिया था, आख़िरी दिन वही था। HR कहता है कंपनी घाटे में है, बाद में देंगे। ऑफ़र लेटर और पुरानी सैलरी स्लिप मेरे पास हैं।

**Haq** (gemini/gemini-3.1-flash-lite, 9.03s):

नमस्ते। आपकी स्थिति स्पष्ट है: आपने काम किया, लेकिन कंपनी ने अगस्त और सितंबर 2026 की सैलरी (कुल ₹1,40,000) नहीं दी है। चूँकि आप अब वहां काम नहीं कर रहे हैं, तो Code on Wages, 2019 के अनुसार, आपकी अंतिम सैलरी आपके आखिरी कार्य दिवस (30 सितंबर 2026) के 2 कार्य दिवसों के भीतर मिल जानी चाहिए थी।

आपकी स्थिति के लिए विकल्प:
1. HR को एक औपचारिक ईमेल भेजें (रिकॉर्ड के लिए), जिसमें बकाया राशि और भुगतान की समय सीमा लिखें।
2. यदि वे नहीं मानते, तो आप 'Inspector-cum-Facilitator' (लेबर ऑफिस) के पास शिकायत दर्ज कर सकते हैं।
3. आप SAMADHAN पोर्टल (samadhan.labour.gov.in) पर भी शिकायत दर्ज कर सकते हैं।
4. कानूनी नोटिस (Legal Notice) भेजें (इसके लिए वकील की मदद लें)।

अगला कदम: सबसे पहले HR को एक औपचारिक ईमेल भेजें जिसमें बकाया सैलरी का विवरण हो। क्या आप चाहते हैं कि मैं इस ईमेल का ड्राफ्ट तैयार करने में आपकी मदद करूँ?

⚠️ **Deadline check (calculated by Haq, not AI):** Full & final wages were due by (2 working days after leaving): **02 Oct 2026**, which has passed. Please speak to a lawyer or free legal aid (15100) soon to check what options remain.

**Calculated by code:** {"deadlines": [{"label": "Full & final wages were due by (2 working days after leaving)", "date": "2026-10-02", "days_left": -35, "status": "passed", "basis": "COW2019-S17", "note": "Assumes a Mon–Sat working week.", "user_deadline": true}, {"label": "Approximate last date to file a wage claim with the labour authority (3 years)", "date": "2029-09-30", "days_left": 1059, "status": "ok", "basis": "COW2019-S45", "note": "", "user_deadline": true}], "derived": []}

_Escalation:_ {"level": "recommended", "reasons": ["Deadline passed: Full & final wages were due by (2 working days after leaving) (2026-10-02)"]}  _Citations:_ ['COW2019-S17', 'COW2019-S45', 'FACT-SAMADHAN-PORTAL']

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
  "still_employed": false,
  "employment_proof": "Offer letter, salary slips",
  "communications_so_far": "HR claims company is in loss, promised payment later",
  "city_state": "Noida",
  "summary": "Unpaid salary for August and September 2026 after resigning from a Noida startup.",
  "amount_due": 140000,
  "last_working_day": "2026-09-30"
 },
 "timeline": [
  {
   "date": "2026-09-30",
   "event": "Last working day"
  }
 ],
 "evidence_have": [
  "Offer letter",
  "Salary slips"
 ],
 "evidence_missing": [
  "Written communication/emails from HR regarding the delay"
 ],
 "next_step": "Draft a formal email to HR demanding the unpaid salary."
}
```

## Draft document

LEGAL NOTICE

By Registered Post A.D. / Speed Post

Date: [[FILL: Current Date]]

From:
[[FILL: Your Full Name]]
[[FILL: Your Full Address]]
[[FILL: Your Phone Number]]

To:
[[FILL: Employer/Company Name]]
[[FILL: Company Registered Office Address]]

Subject: Demand for payment of outstanding salary for August 2026 and September 2026.

Dear Sir/Madam,

1. I was employed with your organization as a Software Developer from [[FILL: Start Date]] until my last working day on 30 September 2026.

2. My monthly salary was fixed at Rs. 70,000/- (Rupees Seventy Thousand only).

3. Despite my service, the salary for the months of August 2026 and September 2026, amounting to a total of Rs. 1,40,000/- (Rupees One Lakh Forty Thousand only), remains unpaid.

4. I have previously communicated with your HR department regarding these dues. I was informed that the company is facing financial losses and that payment would be made at a later date. However, no payment has been received to date.

5. As per the Code on Wages, 2019, wages are required to be paid within the prescribed timelines. The non-payment of my earned wages is a violation of my rights as an employee.

6. I hereby demand that you pay the outstanding amount of Rs. 1,40,000/- (Rupees One Lakh Forty Thousand only) within 15 days of the receipt of this notice. Please remit the amount to the following bank account:
   Bank Name: [[FILL: Your Bank Name]]
   Account Holder Name: [[FILL: Your Name]]
   Account Number: [[FILL: Your Account Number]]
   IFSC Code: [[FILL: Your IFSC Code]]

7. Please be advised that if you fail to clear these dues within the stipulated period, I shall be constrained to initiate appropriate legal proceedings, including filing a wage claim before the competent labour authority and/or pursuing civil recovery, at your sole risk, cost, and consequences.

Copy retained for record.

Sincerely,

[[FILL: Your Name]]
[[FILL: Your Phone Number]]
[[FILL: Your Email Address]]

**Send instructions:** ["इस नोटिस का प्रिंट निकालें और उस पर अपने हस्ताक्षर करें।", "इसे कंपनी के रजिस्टर्ड ऑफिस के पते पर 'Registered Post A.D.' या 'Speed Post' के जरिए भेजें।", "पोस्ट ऑफिस से मिली रसीद (Receipt) को संभाल कर रखें। यह आपके पास सबूत होगा कि आपने नोटिस भेजा है।", "अगर 15 दिनों के भीतर कोई जवाब या भुगतान नहीं मिलता है, तो आप 'SAMADHAN' पोर्टल (https://samadhan.labour.gov.in) पर जाकर लेबर अथॉरिटी के पास शिकायत दर्ज करा सकते हैं।", "कानूनी सलाह के लिए आप 15100 (NALSA हेल्पलाइन) पर कॉल कर सकते हैं या अपने नजदीकी कॉमन सर्विस सेंटर (CSC) पर जाकर 'Tele-Law' सेवा का उपयोग कर सकते हैं।"]

## Automatic checks

| check | pass | detail |
|---|---|---|
| category | ✅ | got salary |
| reply_language | ✅ | expected Devanagari, reply script Devanagari |
| fact:monthly_salary | ✅ | expected ~70, got 70000 |
| fact:last_working_day | ✅ | expected ~2026-09-30, got 2026-09-30 |
| escalation<=urgent | ✅ | got recommended |
| no_unverified_law_shown | ✅ |  |
| draft_no_unverified_law | ✅ | [] |
| draft_has_no_invented_fill | ✅ | 12 placeholders |
