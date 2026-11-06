# T19_deposit_bengali
Group: language

## Turn 1

**User:** আমি কলকাতায় ভাড়া বাড়ি ছেড়েছি ১ অক্টোবর ২০২৬। ৩০,০০০ টাকা অগ্রিম দিয়েছিলাম। বাড়িওয়ালা টাকা ফেরত দিচ্ছে না। কী করব?

**Haq** (gemini/gemini-3.1-flash-lite, 13.63s):

আপনার টাকা আটকে রাখাটা অন্যায়, যদি না আপনার কোনো বকেয়া থাকে বা বাড়ির কোনো বড় ক্ষতি করে থাকেন। আমার পরামর্শ হলো, বাড়িওয়ালা যদি কোনো কারণ না দেখিয়ে টাকা আটকে রাখেন, তবে আইনত তিনি তা করতে পারেন না। আপনার কাছে যদি বাড়ি ছাড়ার সময়কার ছবি বা ভিডিও থাকে, তবে আপনার অবস্থান খুব মজবুত।

**আমার মতামত:** বাড়িওয়ালা আপনার টাকা আটকে রাখতে পারেন না, যদি না তিনি কোনো নির্দিষ্ট খরচের (যেমন: বাড়ির ক্ষতি বা বকেয়া ভাড়া) প্রমাণ দিতে পারেন। সাধারণ ক্ষয়ক্ষতি (normal wear and tear) বা রং করার খরচের নামে পুরো টাকা আটকে রাখা বেআইনি।

**আপনার পক্ষে আইন:**
* যদি তিনি তা না করেন, তবে আপনি সেই টাকার ওপর ক্ষতিপূরণ দাবি করতে পারেন।

**তারা যা বলবে এবং আপনার উত্তর:**
* তারা বলবে: 'রং করার খরচ' বা 'মেরামতির খরচ'।
* আপনার উত্তর: 'আমাকে খরচের রসিদ বা বিল দেখান। সাধারণ ক্ষয়ক্ষতির জন্য আমি দায়ী নই, আর আপনি যদি কোনো খরচ করে থাকেন, তবে তার প্রমাণ দিন।' 

**আমি যা করতাম:**
* আজই একটি আনুষ্ঠানিক মেসেজ বা ইমেল পাঠান যেখানে পরিষ্কারভাবে আপনার ব্যাংক ডিটেইলস এবং বাড়ি ছাড়ার তারিখ উল্লেখ থাকবে।
* যদি ১৫ দিনের মধ্যে উত্তর না পান, তবে একজন আইনজীবীর মাধ্যমে একটি 'লিগ্যাল নোটিশ' (Legal Notice) পাঠান।

**আপনার কাছে আমার প্রশ্ন:**
১. আপনাদের কি কোনো লিখিত ভাড়ার চুক্তি (Rent Agreement) আছে?
২. বাড়িওয়ালা কি কোনো নির্দিষ্ট খরচের কথা বলেছেন, নাকি শুধু টাকা দিতে অস্বীকার করছেন?

_⚠️ I removed a legal reference I could not verify. Check the exact provision before quoting it in a notice._

**Law you can cite (checked against official sources):**
- **Section 73, Indian Contract Act, 1872**: If someone breaks a contract with you, you can claim money for the loss it caused.
- **Article 55, Limitation Act, 1963**: A suit for compensation for breach of a contract (written or implied), where no other article covers it specifically, must be filed within 3 years.

> 🛡️ Guard caught (before user saw it): [{"type": "unknown_section", "text": "ধারা ৭৩", "why": "Not in the verified library."}]  
> repaired=True stripped=True

**Calculated by code:** {"deadlines": [{"label": "Approximate last date to sue for the deposit (3 years)", "date": "2029-10-01", "days_left": 1060, "status": "ok", "basis": "LIM1963-ART55", "note": "Limitation depends on the exact claim; confirm with legal aid before relying on it.", "user_deadline": true}], "derived": []}

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['ICA1872-S73', 'LIM1963-ART55']

## Final case file

```json
{
 "category": "tenancy",
 "language": "Bengali",
 "script": "Bengali",
 "facts": {
  "deposit_amount": 30000,
  "possession_handed_over_date": "2026-10-01",
  "city_state": "Kolkata",
  "summary": "Landlord refusing to return security deposit of 30,000 after vacating the property."
 },
 "timeline": [
  {
   "date": "2026-10-01",
   "event": "Vacated property"
  }
 ],
 "evidence_have": [],
 "evidence_missing": [
  "written_agreement",
  "deductions_claimed",
  "communications_so_far"
 ],
 "next_step": "Send a formal written demand (WhatsApp/Email)"
}
```

## Automatic checks

| check | pass | detail |
|---|---|---|
| category | ✅ | got tenancy |
| reply_language | ✅ | expected Bengali, reply script Bengali |
| escalation<=recommended | ✅ | got none |
| no_unverified_law_shown | ✅ |  |
