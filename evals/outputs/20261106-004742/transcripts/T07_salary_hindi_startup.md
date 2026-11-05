# T07_salary_hindi_startup
Group: core

## Turn 1

**User:** मैं नोएडा की एक स्टार्टअप में सॉफ्टवेयर डेवलपर था, सैलरी 70,000 महीना। अगस्त और सितंबर 2026 की सैलरी नहीं मिली। मैंने 30 सितंबर 2026 को रिज़ाइन कर दिया था, आख़िरी दिन वही था। HR कहता है कंपनी घाटे में है, बाद में देंगे। ऑफ़र लेटर और पुरानी सैलरी स्लिप मेरे पास हैं।

**Haq** (groq/openai/gpt-oss-20b, 21.17s):

आपकी जानकारी के अनुसार, अगस्त और सितंबर 2026 की ₹140,000 की सैलरी अभी तक नहीं मिली है और आप 30 सितंबर 2026 को ही इस्तीफा दे चुके हैं।

**आपकी स्थिति**
- आप एक कर्मचारी (सॉफ्टवेयर डेवलपर) हैं, इसलिए Code on Wages, 2019 के तहत आपकी सैलरी का दावा किया जा सकता है।
- सैलरी का भुगतान न होने की तारीख से 3 वर्ष के भीतर दावा दायर किया जा सकता है (साल 2026 से 2029 तक)।
- कंपनी के घाटे का दावा आपके दावे को नहीं रोकता; आपको लिखित माँग करनी होगी।

**विकल्प (सबसे सस्ता/सबसे तेज़ से लेकर औपचारिक फ़ोरम तक)**
1. HR/कंपनी को लिखित सैलरी डिमांड नोटिस भेजें।
2. यदि कोई जवाब नहीं मिलता, तो Code on Wages, 2019 के तहत Wage Claim Authority (Inspector‑cum‑Facilitator) में शिकायत दर्ज करें।
3. यदि अभी भी निपटारा नहीं होता, तो 3 वर्ष के भीतर Civil Court में सैलरी के लिए मुकदमा दायर करें।

**अगला कदम**
- सबसे पहले HR को एक औपचारिक सैलरी डिमांड नोटिस (ई‑मेल/पत्र) भेजें। मैं आपको यह नोटिस ड्राफ़्ट करने में मदद कर सकता हूँ।

कृपया बताएं कि क्या आप नोटिस ड्राफ़्ट चाहते हैं, या कोई अन्य दस्तावेज़ या साक्ष्य जुटाने में सहायता चाहिए।

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['COW2019-S45', 'COW2019-S17', 'COW2019-S18', 'COW2019-S69']

## Final case file

```json
{
 "category": "salary",
 "language": "Hindi",
 "script": "Devanagari",
 "facts": {
  "other_party_name": "Startup company in Noida",
  "user_name": "Unknown",
  "role": "Software Developer",
  "monthly_salary": 70000,
  "unpaid_period": "2026-08-01 to 2026-09-30",
  "amount_due": 140000,
  "still_employed": false,
  "employment_proof": "Offer letter and old salary slips",
  "communications_so_far": "HR said company is in loss and will pay later",
  "city_state": "Noida, India",
  "summary": "Software developer in Noida startup resigned on 30 Sep 2026, unpaid salaries for Aug and Sep 2026 amounting to ₹140,000."
 },
 "timeline": [
  {
   "date": "2026-09-30",
   "event": "Resignation and last working day"
  }
 ],
 "evidence_have": [
  "Offer letter",
  "Old salary slips"
 ],
 "evidence_missing": [
  "Proof of resignation (e.g., resignation letter or HR acknowledgment)",
  "Any written communication from HR about payment delay"
 ],
 "next_step": "Draft salary demand notice"
}
```

## Draft document

**LEGAL NOTICE**

**Mode of Sending:** By Registered Post A.D. / Speed Post / Email

**Date:** [[FILL: date]]

**From:**

[Your Full Name]
[Your Address]
[City, State, PIN]

**To:**

[Name of the Employer – Startup Company]
[Company Address]
Noida, Uttar Pradesh, India

**Subject:** Demand for payment of unpaid salary for the period August 2026 to September 2026.

1. I was employed as a Software Developer by the above‑named company, receiving a monthly salary of ₹70,000 as per the offer letter and the salary slips issued by the company.
2. My last working day was 30 September 2026, on which I submitted my resignation.
3. The company has failed to pay my salary for the months of August 2026 and September 2026, amounting to a total of ₹140,000.
4. I have communicated with the HR department, who informed me that the company is experiencing losses and will pay the dues at a later date.
5. I possess the offer letter and the salary slips for the relevant months as evidence of the agreed remuneration.

**Legal Basis:**

Under the Code on Wages, 2019, wages are due to employees within the deadlines specified in Section 17. The unpaid salary of ₹140,000 is a clear breach of the employer’s obligation to pay wages on time.

**Demand:**

I hereby demand that the company pay the full amount of ₹140,000 within 15 days from the receipt of this notice. Payment should be made to the following bank account:

Bank Name: [[FILL: bank name]]
Account Number: [[FILL: account number]]
IFSC Code: [[FILL: IFSC code]]

**Consequence:**

If the company fails to comply with this demand within the stipulated period, I will pursue all lawful remedies, including filing a claim before the appropriate labour authority and/or initiating a civil suit for recovery of the unpaid wages, at the company’s cost.

**Copy retained for record.**


**Signature**

[Your Name]
Phone: [[FILL: phone number]]
Email: [[FILL: email address]]

**Send instructions:** ["1. Print the notice and sign it.\n2. Send it via Registered Post (A.D.) to the employer’s address; keep the receipt as proof of dispatch.\n3. If sending by email, use a read‑receipt request and keep the email copy.\n4. If no reply is received within 15 days, file a wage claim on the SAMADHAN portal or approach the labour authority.\n5. If the matter remains unresolved, consider filing a civil suit for recovery of wages."]

## Automatic checks

| check | pass | detail |
|---|---|---|
| category | ✅ | got salary |
| reply_language | ✅ | expected Devanagari, reply script Devanagari |
| fact:monthly_salary | ✅ | expected ~70, got 70000 |
| fact:last_working_day | ❌ | expected ~2026-09-30, got None |
| escalation<=urgent | ✅ | got none |
| no_unverified_law_shown | ✅ |  |
| draft_no_unverified_law | ✅ | [] |
| draft_has_no_invented_fill | ✅ | 6 placeholders |
