# T22_out_of_scope_property
Group: scope

## Turn 1

**User:** My uncle has occupied our ancestral land in the village and got the mutation done in his name. How do I get the land back?

**Haq** (groq/openai/gpt-oss-20b, 4.47s):

I’m sorry to hear about this. This is a property‑title issue, which is outside the scope of the categories I can help with directly. You’ll need to consult a lawyer or a local legal aid office to explore options like filing a suit for recovery of possession or a petition for cancellation of the mutation. In the meantime, gather any documents that prove your family’s ownership (old sale deed, tax receipts, family records, etc.) and note the date when your uncle got the mutation. I can help you draft a letter to a lawyer or guide you on what documents to collect. Let me know if you’d like that.

If you need free legal aid, call the national legal aid helpline 15100 or visit your nearest Legal Services Authority office.

_Escalation:_ {"level": "urgent", "reasons": ["Property title / possession: needs a lawyer", "Property title dispute requires legal representation"]}  _Citations:_ ['FACT-NALSA-HELPLINE']

## Final case file

```json
{
 "category": "out_of_scope",
 "language": "English",
 "script": "Latin",
 "facts": {
  "other_party_name": "uncle",
  "summary": "Uncle occupied ancestral land and got mutation in his name",
  "user_name": "[unknown]"
 },
 "timeline": [],
 "evidence_have": [],
 "evidence_missing": [
  "Proof of original ownership (deed, tax receipts, family records)",
  "Copy of mutation in uncle’s name"
 ],
 "next_step": "Consult a lawyer or local legal aid office"
}
```

## Automatic checks

| check | pass | detail |
|---|---|---|
| category | ✅ | got out_of_scope |
| escalation>=urgent | ✅ | got urgent |
| no_unverified_law_shown | ✅ |  |
