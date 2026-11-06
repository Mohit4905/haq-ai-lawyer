# T22_out_of_scope_property
Group: scope

## Turn 1

**User:** My uncle has occupied our ancestral land in the village and got the mutation done in his name. How do I get the land back?

**Haq** (gemini/gemini-3.1-flash-lite, 36.69s):

Property title disputes, especially involving ancestral land and mutation records, are complex and require a thorough examination of land revenue records and succession documents. This is not a simple matter of a refund or a notice; it involves civil litigation to establish your legal title and challenge the mutation entry. Because this involves your family property rights and potential court proceedings, you should not attempt to handle this alone. I strongly recommend you consult a local civil lawyer who specialises in land revenue matters or contact the free legal aid services for guidance on how to file a suit for partition or declaration of title. You can call the national legal aid helpline at 15100 for assistance in finding a lawyer or understanding your rights under the law.

_Escalation:_ {"level": "urgent", "reasons": ["Property title / possession: needs a lawyer", "Property title disputes are complex, involve civil court procedures, and require professional legal representation."]}  _Citations:_ ['FACT-NALSA-HELPLINE']

## Final case file

```json
{
 "category": "out_of_scope",
 "language": "English",
 "script": "Latin",
 "facts": {
  "other_party_name": "uncle",
  "summary": "User is seeking legal recourse for ancestral land occupied by an uncle who has changed the mutation."
 },
 "timeline": [],
 "evidence_have": [],
 "evidence_missing": [
  "Copy of the land mutation record",
  "Ancestral property documents/succession certificates",
  "Proof of possession"
 ],
 "next_step": "Contact NALSA helpline 15100 for free legal aid or consult a local civil lawyer."
}
```

## Automatic checks

| check | pass | detail |
|---|---|---|
| category | ✅ | got out_of_scope |
| escalation>=urgent | ✅ | got urgent |
| no_unverified_law_shown | ✅ |  |
