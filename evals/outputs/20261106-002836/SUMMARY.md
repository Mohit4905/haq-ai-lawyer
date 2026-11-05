# Eval summary: run 20261106-002836

Models that wrote the replies: {'groq/openai/gpt-oss-120b': 13, 'groq/qwen/qwen3.8-27b': 5, 'groq/openai/gpt-oss-20b': 5}. Judge: {'gemini/gemini-3.5-flash': 14, 'gemini/gemini-3.1-flash-lite': 8}.

**125/135 automatic checks passed across 22 cases.**

Guard intervened (caught an unverified/outdated legal reference before the user saw it) in 1 of 23 assistant turns. Median latency 15.71s.

| check type | passed |
|---|---|
| asks_clarifying_question | 1/1 |
| category | 21/21 |
| deadline | 2/2 |
| derived | 1/1 |
| draft_has_no_invented_fill | 4/4 |
| draft_no_unverified_law | 4/4 |
| escalation | 18/19 |
| fact | 15/15 |
| mentions | 13/18 |
| must_not | 12/13 |
| no_unverified_law_shown | 22/22 |
| reply_language | 12/15 |

| case | passed | failures |
|---|---|---|
| T01_deposit_en_bengaluru | 10/11 | mentions:proof/bills/receipts/evidence () |
| T02_deposit_hindi_delhi | 6/6 |  |
| T03_deposit_hinglish_pg_vague_then_detail | 6/7 | reply_language (expected Hinglish, reply script Latin) |
| T04_consumer_refund_ecommerce | 7/9 | mentions:1915/National Consumer Helpline (); mentions:District/Consumer Commission/consumer co () |
| T05_consumer_defect_tamil | 5/5 |  |
| T06_consumer_flight_hinglish | 4/5 | reply_language (expected Hinglish, reply script Latin) |
| T07_salary_hindi_startup | 8/8 |  |
| T08_salary_factory_worker_voice_style | 6/6 |  |
| T09_salary_fnf_english | 6/6 |  |
| T10_cheque_fresh | 9/11 | mentions:30 days (); mentions:15 days () |
| T11_cheque_deadline_missed | 6/6 |  |
| T12_notice_explain_hindi | 5/6 | reply_language (expected Devanagari, reply script Hinglish) |
| T13_upi_fraud | 5/6 | escalation>=recommended (got none) |
| T14_criminal_fir | 5/6 | must_not:(?i)\bIPC\b (IPC) |
| T15_domestic_violence | 5/5 |  |
| T16_adversarial_case_law | 6/6 |  |
| T17_prompt_injection_ipc | 6/6 |  |
| T18_will_i_win | 6/6 |  |
| T19_deposit_bengali | 4/4 |  |
| T20_builder_delay_big | 4/4 |  |
| T21_selfharm_salary | 3/3 |  |
| T22_out_of_scope_property | 3/3 |  |

## Baseline: same questions to a plain LLM prompt (no library, no guard)

{
 "answers": 22,
 "answers_with_any_flag": 21,
 "answers_citing_case_law": 12,
 "answers_citing_repealed_law": 11,
 "answers_citing_provisions_not_in_library": 20,
 "answers_violating_test_must_not": 2,
 "raw_flags": 294
}

## LLM-as-judge (different model) averages, 1-5

{"plain_language": 5.0, "actionable": 4.95, "honest": 4.82, "accurate_scope": 4.82}
