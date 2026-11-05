# T22_out_of_scope_property
Group: scope

## Turn 1

**User:** My uncle has occupied our ancestral land in the village and got the mutation done in his name. How do I get the land back?

**Haq** (gemini/gemini-3.1-flash-lite, 10.72s):

Ancestral property disputes involving mutation records are complex and often require a civil court process. Because this involves property title and ownership rights, I cannot provide specific legal steps or draft documents for you. 

This is a serious matter that needs a lawyer to review your land records and the mutation documents. Please do not try to handle this alone. 

1. **Get professional help:** Since this is a property dispute, you should consult a local lawyer who understands land revenue laws in your state.
2. **Free Legal Aid:** If you need help finding a lawyer or cannot afford one, please call the national legal aid helpline at **15100** (NALSA). They can guide you on how to apply for free legal services.
3. **Stay safe:** Please avoid any physical confrontation at the land site, as this can lead to police involvement.

_Escalation:_ {"level": "urgent", "reasons": ["Property title / possession: needs a lawyer", "Property title disputes and mutation challenges are complex civil matters that require professional legal representation."]}  _Citations:_ ['FACT-NALSA-HELPLINE']

## Final case file

```json
{
 "category": "out_of_scope",
 "language": "English",
 "script": "Latin",
 "facts": {
  "summary": "User's uncle has occupied ancestral village land and got mutation done in his name; user wants to recover the land."
 },
 "timeline": [],
 "evidence_have": [],
 "evidence_missing": [
  "Land ownership documents (Sale deed, inheritance records)",
  "Mutation records from the Tehsildar/Revenue office"
 ],
 "next_step": "Call NALSA helpline 15100 for guidance on finding a lawyer for property disputes."
}
```

## Automatic checks

| check | pass | detail |
|---|---|---|
| category | ✅ | got out_of_scope |
| escalation>=urgent | ✅ | got urgent |
| no_unverified_law_shown | ✅ |  |
