# T19_deposit_bengali
Group: language

## Turn 1

**User:** আমি কলকাতায় ভাড়া বাড়ি ছেড়েছি ১ অক্টোবর ২০২৬। ৩০,০০০ টাকা অগ্রিম দিয়েছিলাম। বাড়িওয়ালা টাকা ফেরত দিচ্ছে না। কী করব?

**Haq** (groq/openai/gpt-oss-20b, 4.76s):

আপনি ১ অক্টোবর ২০২৬-এ বাড়ি ছেড়েছেন এবং ৩০,০০০ টাকা অগ্রিম দিয়েছেন।

১. **কী কী তথ্য দরকার?**
- ভাড়ার চুক্তি কি লিখিত ছিল? (হ্যাঁ/না)
- বাড়িওয়ালা কি কোনো কাটতি দাবি করেছে? (যেমন রং করা, ক্ষতি, বিল)
- আপনি কি ইতিমধ্যে কোনো লিখিত অনুরোধ (WhatsApp/ইমেইল) পাঠিয়েছেন? কবে?
- অগ্রিমের পেমেন্টের প্রমাণ আছে কি? (ব্যাংক ট্রান্সফার, রিসিপ্ট)

২. **আপনার অবস্থান**
- আপনার দেওয়া তথ্য থেকে দেখা যাচ্ছে যে, আপনি অগ্রিম দিয়েছেন এবং বাড়ি ছেড়েছেন। যদি কোনো লিখিত চুক্তি না থাকে বা বাড়িওয়ালা কোনো বৈধ কাটতি দাবি না করে, তাহলে আপনার দাবির শর্ত পূরণ হচ্ছে।

৩. **বিকল্পগুলো (সস্তা ও দ্রুত থেকে শুরু করে)**
- **লিখিত অনুরোধ**: WhatsApp/ইমেইলে ১৫ দিনের মধ্যে ফেরত চেয়ে লিখে দিন, রসিদ/স্ক্রিনশট সংরক্ষণ করুন।
- **আইনি নোটিশ**: নিজে ১৫ দিনের মধ্যে নোটিশ পাঠিয়ে ফেরত দাবি করুন।
- **লোক আদালত/ডিএলএসএ**: বিনামূল্যে মধ্যস্থতা বা লোক আদালতে আবেদন করতে পারেন।
- **সিভিল মামলা**: ৩ বছরের সীমা (২০২৯‑১০‑০১ পর্যন্ত) মধ্যে মামলা দায়ের করতে পারেন।

৪. **পরবর্তী পদক্ষেপ**
- প্রথমে একটি লিখিত অনুরোধ পাঠিয়ে ১৫ দিনের মধ্যে ফেরত দাবি করুন।

5. **সহায়তা**
- আমি আপনাকে একটি "deposit_demand_notice" খসড়া করতে সাহায্য করতে পারি।

**প্রশ্ন**
- আপনার কি লিখিত ভাড়ার চুক্তি আছে?

**Calculated by code:** {"deadlines": [{"label": "Approximate last date to sue for the deposit (3 years)", "date": "2029-10-01", "days_left": 1060, "status": "ok", "basis": "LIM1963-ART55", "note": "Limitation depends on the exact claim; confirm with legal aid before relying on it.", "user_deadline": true}], "derived": []}

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['ICA1872-S73']

## Final case file

```json
{
 "category": "tenancy",
 "language": "Bengali",
 "script": "Bengali",
 "facts": {
  "deposit_amount": "30000",
  "possession_handed_over_date": "2026-10-01",
  "city_state": "Kolkata, West Bengal",
  "other_party_name": "landlord"
 },
 "timeline": [],
 "evidence_have": [],
 "evidence_missing": [
  "written_agreement",
  "proof_of_payment",
  "communications_so_far"
 ],
 "next_step": "Send a written request demanding refund within 15 days"
}
```

## Automatic checks

| check | pass | detail |
|---|---|---|
| category | ✅ | got tenancy |
| reply_language | ✅ | expected Bengali, reply script Bengali |
| escalation<=recommended | ✅ | got none |
| no_unverified_law_shown | ✅ |  |
