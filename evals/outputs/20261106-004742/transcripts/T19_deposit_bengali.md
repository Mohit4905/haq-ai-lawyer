# T19_deposit_bengali
Group: language

## Turn 1

**User:** আমি কলকাতায় ভাড়া বাড়ি ছেড়েছি ১ অক্টোবর ২০২৬। ৩০,০০০ টাকা অগ্রিম দিয়েছিলাম। বাড়িওয়ালা টাকা ফেরত দিচ্ছে না। কী করব?

**Haq** (groq/openai/gpt-oss-20b, 9.44s):

আপনি কি জানেন:
1️⃣ ভাড়ার মাসিক পরিমাণ কত ছিল?
2️⃣ ভাড়ার চুক্তি লিখিত ছিল কি? (হ্যাঁ/না)
3️⃣ বাড়িওয়ালা কি কোনো কাটতি (দাগ, মেরামত, বিল) দাবি করেছে?

**Calculated by code:** {"deadlines": [{"label": "Approximate last date to sue for the deposit (3 years)", "date": "2029-10-01", "days_left": 1060, "status": "ok", "basis": "LIM1963-ART55", "note": "Limitation depends on the exact claim; confirm with legal aid before relying on it.", "user_deadline": true}], "derived": []}

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['ICA1872-S73', 'MTA2021-S11', 'FACT-MTA-STATE-ADOPTION', 'LIM1963-ART55', 'CPC1908-O37', 'FACT-LOKADALAT-PRELITIGATION', 'FACT-NALSA-HELPLINE']

## Final case file

```json
{
 "category": "tenancy",
 "language": "Bengali",
 "script": "Bengali",
 "facts": {
  "deposit_amount": 30000,
  "possession_handed_over_date": "2026-10-01",
  "city_state": "Kolkata, West Bengal",
  "other_party_name": "landlord"
 },
 "timeline": [],
 "evidence_have": [],
 "evidence_missing": [
  "ভাড়ার চুক্তি (যদি থাকে), ব্যাংক রেকর্ড/রসিদ, বাড়িওয়ালার সাথে যোগাযোগের স্ক্রিনশট"
 ],
 "next_step": "প্রথমে লিখিত অনুরোধ (WhatsApp/ইমেইল) পাঠিয়ে ১৫ দিনের মধ্যে ফেরত চেয়ে নিন"
}
```

## Automatic checks

| check | pass | detail |
|---|---|---|
| category | ✅ | got tenancy |
| reply_language | ✅ | expected Bengali, reply script Bengali |
| escalation<=recommended | ✅ | got none |
| no_unverified_law_shown | ✅ |  |
