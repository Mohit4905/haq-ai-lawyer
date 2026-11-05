# The verified law library

`laws.json` is the only source of legal content Haq is allowed to mention. It is built by `python kb/build_kb.py` from:

| File | What it covers |
|---|---|
| `research_consumer_cheque_aid.json` | Consumer Protection Act 2019 and its Rules (jurisdiction, fees, e-commerce), e-Jagriti, National Consumer Helpline, NI Act (cheque bounce), RBI cheque validity, RBI Integrated Ombudsman Scheme 2026, Legal Services Authorities Act, NALSA, Tele-Law, cyber-fraud helpline 1930 |
| `research_labour_tenancy_general.json` | Labour Codes commencement (21 Nov 2025), Code on Wages 2019 (s.2(k), 17, 18, 25, 45, 51, 57, 69), SAMADHAN, Indian Contract Act s.73, Model Tenancy Act s.11 and adoption status, Limitation Act Articles 7/55/113, CPC Order XXXVII and s.80, BNS/BNSS commencement and key sections, Mediation Act status, Commercial Courts Act s.12A |
| `manual_facts.json` | Emergency number 112 (MHA ERSS) and Tele-MANAS 14416 (MoHFW) |

**How entries were made.** For each entry, a research agent opened the source (India Code, the e-Gazette, ministry, RBI or NALSA pages) and wrote a plain-language summary, a short verbatim quote, the URL, and notes on caveats and amendments. I reviewed every entry before using it. Entries that could not be confirmed against a primary source are kept with `"verified": false` and are **never** shown to the model. One entry exists (`FACT-RBIOS2021-SUPERSEDED`).

**Manual edit.** `MED2023-S5` (pre-litigation mediation under the Mediation Act 2023) was prefixed with "NOT YET IN FORCE". The research found that s.5 had not been brought into force as of the latest official text (Oct 2025), and the model must not suggest it as an available option.

**Known gaps and caveats** (also in each entry's `notes`):
- State-specific rules (rent control Acts, Shops and Establishments Acts, state wage rules, legal-aid income limits) are flagged, not modelled.
- The RBI Ombudsman Scheme 2026 entries rely on RBI's official FAQ. The scheme PDF was behind a bot check, so clause numbers are not cited.
- The E-Commerce (Amendment) Rules 2026 commencement date (1 Jan 2027) is confirmed only by secondary sources. That entry is not used in prompts.
- India Code moved to indiacode.gov.in during the research; some sources are bare-act copies hosted on High Court websites.
- No case law is included. Haq's policy is to cite none.

**Integrity check:** `python -m tests.test_kb_integrity` verifies that every id used in the code exists and is verified, that every entry has a source URL, and that the guard accepts each section when it is cited correctly.
