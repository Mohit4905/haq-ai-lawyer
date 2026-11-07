"""Deterministic rules: scope, intake checklists, red flags, replaced laws, deadline maths.

Anything that has a single correct answer (a date, a threshold, a fee slab, an emergency
number) lives here as plain code with a KB id as its source, never in the model's head.
"""
from __future__ import annotations

import re
from datetime import date, datetime, timedelta

# ------------------------------------------------------------------ scope
CATEGORIES = {
    "tenancy": "Security deposit / rent dispute with landlord",
    "consumer": "Refund, defective product, bad service, e-commerce",
    "salary": "Unpaid salary / wages / full-and-final settlement",
    "cheque_bounce": "Cheque bounced (someone owes you money)",
    "notice": "I received a legal notice and don't understand it",
    "cyber_fraud": "Online / UPI fraud (pointer only: police + bank)",
    "general_legal": "A question about the law (rights, laws, procedures)",
    "out_of_scope": "Other legal matter: criminal, family, property title, etc. (general guidance + lawyer / legal aid)",
    "other": "Not yet clear",
}
# What a message is, before any legal routing (decided by the router; greetings also by code).
INTENTS = {"legal", "general_knowledge", "greeting", "off_topic", "unsafe"}

IN_DEPTH = {"tenancy", "consumer", "salary", "cheque_bounce", "notice"}

# Facts Haq tries to collect for each category (drives follow-up questions + completeness meter)
CHECKLISTS: dict[str, list[tuple[str, str]]] = {
    "tenancy": [
        ("deposit_amount", "How much deposit did you pay (₹)?"),
        ("monthly_rent", "What was the monthly rent (₹)?"),
        ("written_agreement", "Is there a written rent agreement? (yes/no)"),
        ("possession_handed_over_date", "On what date did you vacate and hand over the keys?"),
        ("deductions_claimed", "Has the landlord claimed any deductions (painting, damage, dues)?"),
        ("communications_so_far", "How have you asked for it so far (calls, WhatsApp, email)?"),
        ("proof_of_payment", "Do you have proof you paid the deposit (bank transfer, receipt)?"),
        ("city_state", "Which city and state is the flat in?"),
        ("other_party_name", "Landlord's name (and address, if you have it)?"),
    ],
    "consumer": [
        ("product_or_service", "What did you buy or which service was it?"),
        ("other_party_name", "Which company / seller / platform?"),
        ("amount_paid", "How much did you pay (₹)?"),
        ("purchase_date", "When did you buy it?"),
        ("problem_date", "When did the problem start (or refund become due)?"),
        ("complained_to_company", "Have you complained to the company? When, and what did they say?"),
        ("proof", "What proof do you have (invoice, order ID, chats, emails, photos)?"),
        ("city_state", "Which city and state do you live in?"),
    ],
    "salary": [
        ("other_party_name", "Employer / company name?"),
        ("role", "What is your job role? (helps decide which law applies)"),
        ("monthly_salary", "Monthly salary (₹)?"),
        ("unpaid_period", "Which months are unpaid?"),
        ("amount_due", "Total amount due (₹)?"),
        ("still_employed", "Are you still working there? If not, what was your last working day?"),
        ("employment_proof", "Proof of employment (offer letter, payslips, bank credits, ID card)?"),
        ("communications_so_far", "Have you asked HR/employer in writing?"),
        ("city_state", "Which city and state is the workplace in?"),
    ],
    "cheque_bounce": [
        ("cheque_amount", "Cheque amount (₹)?"),
        ("cheque_date", "Date written on the cheque?"),
        ("reason_for_cheque", "Why was the cheque given (loan repayment, payment for goods...)?"),
        ("presentation_date", "When did you deposit it?"),
        ("dishonour_reason", "Bank's reason for return (e.g. 'funds insufficient')?"),
        ("memo_received_date", "When did your bank tell you it bounced (return memo date)?"),
        ("notice_sent_date", "Have you sent a legal notice yet? Date?"),
        ("other_party_name", "Name of the person/company who gave the cheque?"),
        ("city_state", "Where is your bank branch (city)?"),
    ],
    "notice": [
        ("notice_from", "Who sent the notice (person, company, lawyer, court, government)?"),
        ("notice_date", "Date on the notice?"),
        ("received_date", "When did you receive it?"),
        ("notice_demands", "What does it ask you to do or pay?"),
        ("notice_deadline_days", "Does it give a deadline (e.g. 15 days)?"),
        ("notice_text", "Can you paste the text or upload a photo of it?"),
    ],
}

# Vetted "options ladders": the routes the model may suggest, cheapest first. The model explains
# them in the user's language; it does not invent new routes. Each step cites library ids.
PLAYBOOKS: dict[str, list[str]] = {
    "tenancy": [
        "Written request (WhatsApp/email) with amount, move-out date and bank details; keep screenshots.",
        "Legal notice demanding refund within ~15 days (user can send it themselves) [ICA1872-S73].",
        "Free pre-litigation Lok Adalat / legal aid through the District Legal Services Authority (DLSA); NALSA 15100 [FACT-LOKADALAT-PRELITIGATION, FACT-NALSA-HELPLINE].",
        "Civil suit for recovery of the deposit within 3 years [LIM1963-ART55]; a summary suit may be possible if there is a written agreement [CPC1908-O37]. A lawyer helps here.",
        "Model Tenancy Act deposit rules apply ONLY in states that adopted it (AP, TN, UP, Assam as of July 2022) [MTA2021-S11, FACT-MTA-STATE-ADOPTION].",
        "Do NOT suggest the Consumer Commission for landlord-tenant deposit disputes, and do not call any court a 'small claims court'.",
        "Eviction questions: the answer depends on the rent agreement and the state's rent law. Give the general position first (the landlord must give the notice the agreement or law requires; if the tenant does not leave, the landlord has to go through the rent authority or court, not use force), then ask the state and what the agreement says; a lawyer or legal aid should check the state rules.",
    ],
    "consumer": [
        "Written complaint to the company / platform grievance officer (must acknowledge in 48h, resolve in 1 month for e-commerce) [CPECOM2020-R4-5].",
        "National Consumer Helpline 1915 / WhatsApp 8800001915: free, pre-litigation [FACT-NCH-HELPLINE].",
        "Legal notice to the company (optional).",
        "Consumer complaint on e-Jagriti within 2 years; forum and fee as in CALCULATED FACTS (nil fee up to ₹5 lakh); no lawyer needed [CPA2019-S35, CPA2019-S69, FACT-EJAGRITI-PORTAL, CPJURIS2021-R3-5, CPCDRC2020-R7].",
        "Reliefs: refund, replacement, compensation [CPA2019-S39].",
    ],
    "salary": [
        "Written request to HR/employer (email) listing months and amount due; keep proof of employment.",
        "Demand notice to employer (~15 days).",
        "Wage claim before the authority under the Code on Wages within 3 years; it can award up to 10x compensation; covers all employees incl. managers [COW2019-S45, COW2019-S2K, FACT-COW-NO-WAGE-CEILING]. Ask the local labour office / Inspector-cum-Facilitator [COW2019-S51]; SAMADHAN portal [FACT-SAMADHAN-PORTAL].",
        "Final wages after resignation/termination are due within 2 working days [COW2019-S17].",
        "Civil suit for unpaid wages (3 years) is an alternative, e.g. for amounts outside 'wages' like incentives [LIM1963-ART7, COW2019-S57]. A lawyer helps here.",
        "Government offices/local authorities: different rules may apply [COW2019-S25].",
    ],
    "cheque_bounce": [
        "Send a written demand notice within 30 days of getting the bank's return memo [NIA1881-S138].",
        "The drawer has 15 days from receiving the notice to pay [NIA1881-S138].",
        "If unpaid, file a criminal complaint within 1 month after those 15 days, in the court where the payee's bank branch is [NIA1881-S142-1, NIA1881-S142-2]. A lawyer is strongly advisable for the court case.",
        "Settlement is possible at any stage (compoundable) [NIA1881-S147]; court may order interim compensation up to 20% [NIA1881-S143A].",
        "If the 30-day notice window was missed, the criminal route is likely lost for this presentation; a civil summary suit may still be possible [CPC1908-O37]; get a lawyer to check.",
    ],
    "notice": [
        "Don't ignore it; note the deadline in it. Don't admit anything or pay in panic.",
        "Collect your proof; reply in writing within the deadline (a reply is usually wise even if you disagree).",
        "If it is from a court, police, tax authority or demands a large amount, see a lawyer / free legal aid (15100) urgently.",
    ],
    "cyber_fraud": [
        "Call 1930 immediately and report on cybercrime.gov.in; quick reporting improves chances of freezing the money [FACT-CYBER-1930].",
        "Inform your bank in writing at once; if unresolved after 30 days, RBI Ombudsman (within 90 days) at cms.rbi.org.in [FACT-RBIOS2026-ELIGIBILITY, FACT-RBI-CMS-PORTAL].",
        "File a police complaint (an FIR can be filed at any police station: zero FIR) [BNSS2023-S173].",
    ],
    "general_legal": [
        "Explain the law, right or procedure asked about, directly and in plain words; cite the VERIFIED LIBRARY where it covers the point (e.g. Constitution articles, FIR, BNS/BNSS commencement).",
        "If the user then describes a dispute of their own, move on to their facts and a plan.",
    ],
    "out_of_scope": [
        "Give any urgent protective step first where it applies (danger: 112; a crime: police complaint / FIR at any police station [BNSS2023-S173]; keep evidence).",
        "Explain the general legal position and the usual procedure in plain words; name a provision only if it is in the VERIFIED LIBRARY.",
        "Do not name specific offences, authorities, government offices or court remedies unless the VERIFIED LIBRARY supports them; when unsure, keep to safe universal steps: preserve evidence, use the platform's or institution's own complaint route, police / cybercrime complaint (1930, cybercrime.gov.in) [FACT-CYBER-1930], and a lawyer or legal aid.",
        "Recommend a lawyer or free legal aid to handle it (NALSA 15100) [FACT-NALSA-HELPLINE]; do not draft court papers.",
    ],
}

# ------------------------------------------------------------------ case tracker
CASE_STATUSES = ["new", "notice_sent", "waiting", "complaint_filed", "resolved", "closed"]

# Action checklist per problem type: (id, English, Hindi). Ordered; derived from PLAYBOOKS.
CASE_STEPS: dict[str, list[tuple[str, str, str]]] = {
    "tenancy": [
        ("proof", "Collect proof: agreement, deposit payment, move-out/handover date, chats", "सबूत जुटाएँ: एग्रीमेंट, डिपॉज़िट भुगतान, घर खाली करने की तारीख़, चैट"),
        ("ask", "Ask for the deposit in writing (WhatsApp/email) with bank details", "लिखित में डिपॉज़िट माँगें (WhatsApp/ईमेल), बैंक विवरण के साथ"),
        ("notice", "Send a legal notice (15 days to pay); keep the postal receipt", "लीगल नोटिस भेजें (15 दिन में भुगतान); डाक रसीद रखें"),
        ("aid", "Approach DLSA / Lok Adalat or call NALSA 15100 (free)", "DLSA / लोक अदालत जाएँ या NALSA 15100 पर कॉल करें (मुफ़्त)"),
        ("suit", "If still unpaid: civil suit for recovery within 3 years (lawyer advised)", "फिर भी न मिले तो: 3 साल के भीतर वसूली का दीवानी मुकदमा (वकील की सलाह)"),
    ],
    "consumer": [
        ("proof", "Keep invoice, order ID, ticket numbers, chats, photos", "बिल, ऑर्डर ID, टिकट नंबर, चैट, फ़ोटो सँभालें"),
        ("complain", "Complain in writing to the company / grievance officer", "कंपनी / ग्रीवेंस ऑफ़िसर को लिखित शिकायत करें"),
        ("nch", "Register on National Consumer Helpline 1915 (free)", "नेशनल कंज़्यूमर हेल्पलाइन 1915 पर शिकायत दर्ज करें (मुफ़्त)"),
        ("notice", "Optional: legal notice to the company", "वैकल्पिक: कंपनी को लीगल नोटिस"),
        ("file", "File a consumer complaint on e-Jagriti within 2 years", "2 साल के भीतर e-Jagriti पर उपभोक्ता शिकायत दर्ज करें"),
    ],
    "salary": [
        ("proof", "Collect proof: offer letter, payslips, bank credits, attendance, ID card", "सबूत जुटाएँ: ऑफ़र लेटर, सैलरी स्लिप, बैंक क्रेडिट, हाज़िरी, ID कार्ड"),
        ("ask", "Email HR listing unpaid months and the amount", "HR को ईमेल करें: बकाया महीने और रकम"),
        ("notice", "Send a demand notice (15 days)", "डिमांड नोटिस भेजें (15 दिन)"),
        ("claim", "File a wage claim: labour office / SAMADHAN portal (within 3 years)", "वेतन दावा करें: लेबर ऑफ़िस / SAMADHAN पोर्टल (3 साल के भीतर)"),
        ("aid", "Need help? NALSA 15100 (free legal aid)", "मदद चाहिए? NALSA 15100 (मुफ़्त कानूनी सहायता)"),
    ],
    "cheque_bounce": [
        ("memo", "Keep the cheque copy and the bank's return memo", "चेक की कॉपी और बैंक का रिटर्न मेमो सँभालें"),
        ("notice", "Send the demand notice within 30 days of the memo (registered post)", "मेमो के 30 दिन के भीतर डिमांड नोटिस भेजें (रजिस्टर्ड डाक)"),
        ("track", "Track delivery; the 15 days to pay start when they receive it", "डिलीवरी ट्रैक करें; भुगतान के 15 दिन मिलने की तारीख़ से शुरू"),
        ("complaint", "If unpaid: file the complaint within 1 month after those 15 days (lawyer advised)", "भुगतान न हो तो: उन 15 दिनों के बाद 1 महीने के भीतर शिकायत (वकील की सलाह)"),
    ],
    "notice": [
        ("read", "Note the deadline in the notice and who sent it", "नोटिस की समय-सीमा और भेजने वाले को नोट करें"),
        ("proof", "Collect your proof (photos, handover report, payments, chats)", "अपने सबूत जुटाएँ (फ़ोटो, हैंडओवर रिपोर्ट, भुगतान, चैट)"),
        ("reply", "Send a written reply before the deadline", "समय-सीमा से पहले लिखित जवाब भेजें"),
        ("lawyer", "Large amount or court/police involved? See a lawyer / NALSA 15100", "बड़ी रकम या कोर्ट/पुलिस? वकील / NALSA 15100 से मिलें"),
    ],
    "cyber_fraud": [
        ("1930", "Call 1930 and report on cybercrime.gov.in immediately", "तुरंत 1930 पर कॉल करें और cybercrime.gov.in पर रिपोर्ट करें"),
        ("bank", "Inform your bank in writing; keep the complaint number", "बैंक को लिखित सूचना दें; शिकायत नंबर रखें"),
        ("fir", "File a police complaint / FIR (zero FIR possible)", "पुलिस शिकायत / FIR करें (ज़ीरो FIR संभव)"),
        ("ombudsman", "No resolution in 30 days? RBI Ombudsman (cms.rbi.org.in) within 90 days", "30 दिन में हल नहीं? 90 दिन के भीतर RBI लोकपाल (cms.rbi.org.in)"),
    ],
}

# Core provisions a user can cite, per problem type (all verified ids). If the model's reply
# cites none, code appends these, so a covered case always shows citable law.
CORE_CITATIONS: dict[str, list[str]] = {
    "cyber_fraud": ["BNSS2023-S173", "BNS2023-S318"],  # QA 7 Nov: fraud answers gave steps but named no law
    "tenancy": ["ICA1872-S73", "LIM1963-ART55"],
    "consumer": ["CPA2019-S2-11", "CPA2019-S35", "CPA2019-S69"],
    "salary": ["COW2019-S17", "COW2019-S45", "COW2019-S2K"],
    "cheque_bounce": ["NIA1881-S138", "NIA1881-S142-1", "NIA1881-S142-2"],
}
CITE_HEADING = {
    "Hindi": "आप ये क़ानून उद्धृत कर सकते हैं (सरकारी स्रोत से जाँचे हुए)",
    "Hinglish": "Aap yeh kanoon cite kar sakte hain (official source se verified)",
    "Punjabi": "ਤੁਸੀਂ ਇਹ ਕਾਨੂੰਨ ਹਵਾਲੇ ਵਜੋਂ ਦੇ ਸਕਦੇ ਹੋ (ਸਰਕਾਰੀ ਸਰੋਤ ਨਾਲ ਜਾਂਚੇ)",
    "Marathi": "तुम्ही हे कायदे उद्धृत करू शकता (अधिकृत स्रोतातून तपासलेले)",
}


def provision_label(e: dict) -> str:
    s = str(e.get("section") or "").strip()
    act = e["act"]
    if not s:
        return act
    m = re.search(r"(?i)article\s*(\S+)", s)
    if m:
        return f"Article {m.group(1)}, {act}"
    if re.match(r"(?i)^(order|rule)", s):
        return f"{s}, {act}"
    return f"Section {s}, {act}"

# ------------------------------------------------------------------ red flags
# (regex, level, reason). level: "emergency" > "urgent" > "recommended"
RED_FLAGS: list[tuple[str, str, str]] = [
    (r"suicid|kill myself|end my life|marna chahta|mar jaunga|mar jaungi|jaan de d|आत्महत्या|खुदकुशी|ख़ुदकुशी|मर जाऊं|जान दे", "emergency", "Mentions self-harm"),
    (r"(?:beats? me|beating me|hits? me|attacked me|threat(?:en)?(?:ed|ing)? to kill|maar[- ]?pit|marpeet|maarte hain|marta hai|मारपीट|जान से मार|पीटा|पीटते|मारते हैं|मारता है)", "emergency", "Violence or threat to safety"),
    (r"\barrest|giraftar|गिरफ्तार|गिरफ़्तार|\bbail\b|ज़मानत|जमानत", "urgent", "Arrest / bail: needs a criminal lawyer now"),
    (r"\bFIR\b|एफआईआर|police (?:case|complaint) against|thane|थाने|थाना", "urgent", "Police / FIR involvement"),
    (r"warrant|वारंट|summons|समन|court (?:date|notice|case) against|case filed against me|मुकदमा दर्ज|केस कर दिया", "urgent", "Court process against the user"),
    (r"divorce|talaq|तलाक|child custody|custody of (?:my|our|the) (?:child|son|daughter|kids)|(?:wife|husband|spouse|spousal|child|interim) maintenance|maintenance (?:from|to|for) (?:my )?(?:wife|husband|spouse|child|children)|गुजारा भत्ता|alimony|dowry|dahej|दहेज|domestic violence|घरेलू हिंसा", "urgent", "Family law matter: a family lawyer or free legal aid should handle it"),
    (r"sexual harass|POSH|यौन उत्पीड़न|molest", "urgent", "Sexual harassment: needs specialised help"),
    (r"(?:land|plot|property) (?:title|dispute|registry)|mutation|ancestral (?:land|property)|zameen|ज़मीन|जमीन|कब्जा|कब्ज़ा|kabza|encroach|दाखिल खारिज|पैतृक", "urgent", "Property title / possession: needs a lawyer"),
    (r"lock(?:ed)? (?:me )?out|threw (?:out )?my (?:things|belongings)|forcibly evict|सामान बाहर|ताला लगा", "urgent", "Forcible eviction"),
    (r"proceedings against you|initiate (?:appropriate )?(?:civil |criminal |legal )?proceedings|legal action against you|at your (?:own )?risk as to costs|आपके (?:खिलाफ|विरुद्ध) (?:कानूनी )?कार्रवाई", "recommended", "The notice threatens legal proceedings: get it reviewed"),
]

EMERGENCY_PREFIX = {
    "en": "🚨 **If you are in danger right now, call 112.** If you are thinking of harming yourself, please call **Tele-MANAS 14416** (free, 24×7). You are not alone.\n\n",
    "hi": "🚨 **अगर आप अभी ख़तरे में हैं तो 112 पर कॉल करें।** अगर ख़ुद को नुकसान पहुँचाने के विचार आ रहे हैं तो **टेली-मानस 14416** पर कॉल करें (मुफ़्त, 24×7)। आप अकेले नहीं हैं।\n\n",
    "hinglish": "🚨 **Agar aap abhi khatre mein hain to 112 call karein.** Agar khud ko nuksaan pahunchane ke khayal aa rahe hain to **Tele-MANAS 14416** par call karein (free, 24×7). Aap akele nahi hain.\n\n",
}

DEADLINE_ALERT = {
    "en": "⚠️ **Deadline check (calculated by Haq, not AI):** {label}: **{date}**, which has passed. Please speak to a lawyer or free legal aid (15100) soon to check what options remain.",
    "hi": "⚠️ **समय-सीमा जाँच (हक़ के कोड से गणना, AI से नहीं):** {label}: **{date}**, यह तारीख़ निकल चुकी है। जल्द किसी वकील या मुफ़्त कानूनी सहायता (15100) से बात करें कि अब क्या विकल्प बचे हैं।",
    "hinglish": "⚠️ **Deadline check (Haq ke code se calculate, AI se nahi):** {label}: **{date}**, yeh tareekh nikal chuki hai. Jaldi kisi vakeel ya free legal aid (15100) se baat kijiye ki ab kya options bache hain.",
}

EMERGENCY_CONTACTS = [
    {"label": "Emergency (police / ambulance)", "value": "112", "kb": "FACT-ERSS-112"},
    {"label": "Tele-MANAS mental health helpline (24x7, free)", "value": "14416", "kb": "FACT-TELEMANAS"},
]


def red_flags(text: str) -> list[dict]:
    out = []
    for rx, level, reason in RED_FLAGS:
        if re.search(rx, text, re.IGNORECASE):
            out.append({"level": level, "reason": reason})
    return out


LEVEL_ORDER = {"none": 0, "recommended": 1, "urgent": 2, "emergency": 3}

# ------------------------------------------------------------------ replaced laws
# Models trained on older data keep citing these. The guard blocks them and suggests the replacement.
OUTDATED_LAWS: dict[str, dict] = {
    "Indian Penal Code, 1860": {
        "aliases": ["Indian Penal Code", "IPC", "I.P.C.", "भारतीय दंड संहिता", "आईपीसी"],
        "status": "was replaced by the Bharatiya Nyaya Sanhita, 2023 with effect from 1 July 2024",
        "replacement": "Bharatiya Nyaya Sanhita, 2023 (BNS)",
    },
    "Code of Criminal Procedure, 1973": {
        "aliases": ["Code of Criminal Procedure", "CrPC", "Cr.P.C.", "Cr.P.C", "दंड प्रक्रिया संहिता"],
        "status": "was replaced by the Bharatiya Nagarik Suraksha Sanhita, 2023 with effect from 1 July 2024",
        "replacement": "Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS)",
    },
    "Indian Evidence Act, 1872": {
        "aliases": ["Indian Evidence Act", "Evidence Act, 1872"],
        "status": "was replaced by the Bharatiya Sakshya Adhiniyam, 2023 with effect from 1 July 2024",
        "replacement": "Bharatiya Sakshya Adhiniyam, 2023",
    },
    "Consumer Protection Act, 1986": {
        "aliases": ["Consumer Protection Act, 1986", "Consumer Protection Act 1986", "CPA 1986", "CPA, 1986"],
        "status": "was repealed by the Consumer Protection Act, 2019 (in force from 20 July 2020)",
        "replacement": "Consumer Protection Act, 2019",
    },
}

# Verified in KB: COW2019-S69 (repeal) + FACT-LABOUR-CODES-COMMENCEMENT (in force 21 Nov 2025).
_COW = {"status": "was repealed by the Code on Wages, 2019 (in force from 21 November 2025)", "replacement": "Code on Wages, 2019"}
OUTDATED_LAWS.update({
    "Payment of Wages Act, 1936": {"aliases": ["Payment of Wages Act", "वेतन भुगतान अधिनियम"], **_COW},
    "Minimum Wages Act, 1948": {"aliases": ["Minimum Wages Act", "न्यूनतम मजदूरी अधिनियम"], **_COW},
    "Payment of Bonus Act, 1965": {"aliases": ["Payment of Bonus Act", "बोनस संदाय अधिनियम"], **_COW},
    "Equal Remuneration Act, 1976": {"aliases": ["Equal Remuneration Act", "समान पारिश्रमिक अधिनियम"], **_COW},
})

# ------------------------------------------------------------------ date helpers
_DATE_FORMATS = ["%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%d.%m.%Y", "%d %B %Y", "%d %b %Y", "%B %d, %Y", "%b %d, %Y", "%Y/%m/%d"]


def parse_date(v) -> date | None:
    if not v or not isinstance(v, str):
        return None
    s = v.strip()
    for f in _DATE_FORMATS:
        try:
            return datetime.strptime(s, f).date()
        except ValueError:
            continue
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", s)
    if m:
        try:
            return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            return None
    return None


def parse_inr(v) -> float | None:
    """'₹45,000' / '45000' / '1.5 lakh' / '2 crore' -> float rupees."""
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).lower().replace(",", "").replace("₹", "").replace("rs.", "").replace("rs", "").replace("inr", "").strip()
    m = re.search(r"(\d+(?:\.\d+)?)\s*(lakh|lac|lakhs|crore|cr|k|thousand|हजार|लाख|करोड़)?", s)
    if not m:
        return None
    n = float(m.group(1))
    mult = {"lakh": 1e5, "lac": 1e5, "lakhs": 1e5, "लाख": 1e5, "crore": 1e7, "cr": 1e7, "करोड़": 1e7, "k": 1e3, "thousand": 1e3, "हजार": 1e3}
    return n * mult.get(m.group(2) or "", 1)


def add_months(d: date, n: int) -> date:
    y, m = divmod(d.month - 1 + n, 12)
    y += d.year
    m += 1
    import calendar

    day = min(d.day, calendar.monthrange(y, m)[1])
    return date(y, m, day)


def inr(n: float) -> str:
    n = int(round(n))
    s = str(n)
    if len(s) <= 3:
        return "₹" + s
    head, tail = s[:-3], s[-3:]
    parts = []
    while len(head) > 2:
        parts.insert(0, head[-2:])
        head = head[:-2]
    if head:
        parts.insert(0, head)
    return "₹" + ",".join(parts) + "," + tail


# ------------------------------------------------------------------ calculators
def _deadline(label: str, d: date, basis: str, note: str = "", today: date | None = None, mine: bool = True) -> dict:
    today = today or date.today()
    left = (d - today).days
    status = "passed" if left < 0 else ("soon" if left <= 7 else "ok")
    return {"label": label, "date": d.isoformat(), "days_left": left, "status": status, "basis": basis, "note": note, "user_deadline": mine}


# Thresholds below are set from the verified KB (see kb/laws.json ids in `basis`).
CONSUMER_FORUM = [  # (max consideration paid in ₹, forum)
    (50_00_000, "District Consumer Disputes Redressal Commission"),
    (2_00_00_000, "State Consumer Disputes Redressal Commission"),
    (float("inf"), "National Consumer Disputes Redressal Commission"),
]
CONSUMER_FEE = [  # (max consideration ₹, fee ₹)
    (5_00_000, 0),
    (10_00_000, 200),
    (20_00_000, 400),
    (50_00_000, 1000),
    (1_00_00_000, 2000),
    (2_00_00_000, 2500),
    (4_00_00_000, 3000),
    (6_00_00_000, 4000),
    (8_00_00_000, 5000),
    (10_00_00_000, 6000),
    (float("inf"), 7500),
]
FEE_BASIS = "CPCDRC2020-R7"
FORUM_BASIS = "CPJURIS2021-R3-5"


def compute(category: str | None, facts: dict, today: date | None = None) -> dict:
    """Return deadlines + derived facts with their KB basis. Pure function; unit-tested."""
    f = facts or {}
    out: dict = {"deadlines": [], "derived": []}
    today = today or date.today()

    if category == "consumer":
        cause = parse_date(f.get("problem_date")) or parse_date(f.get("purchase_date"))
        if cause:
            out["deadlines"].append(_deadline("Last date to file a consumer complaint (2 years from when the problem arose)", add_months(cause, 24), "CPA2019-S69", "The commission can accept a late complaint only if you show sufficient cause for the delay.", today))
        amt = parse_inr(f.get("amount_paid"))
        if amt:
            forum = next(name for lim, name in CONSUMER_FORUM if amt <= lim)
            fee = next(fee for lim, fee in CONSUMER_FEE if amt <= lim)
            out["derived"].append({"label": "Where to file", "value": forum, "basis": FORUM_BASIS, "note": f"Based on the amount you paid ({inr(amt)}), not the amount you claim."})
            out["derived"].append({"label": "Filing fee", "value": "Nil" if fee == 0 else inr(fee), "basis": FEE_BASIS, "note": ""})
        comp = parse_date(f.get("complained_to_company_date"))
        if comp and str(f.get("is_ecommerce", "")).lower() in ("yes", "true", "1"):
            out["deadlines"].append(_deadline("If your complaint reached the platform's grievance officer, they had to resolve it by", add_months(comp, 1), "CPECOM2020-R4-5", "Acknowledgement is due within 48 hours. This is the company's deadline, not yours.", today, mine=False))

    elif category == "cheque_bounce":
        cd = parse_date(f.get("cheque_date"))
        if cd:
            out["deadlines"].append(_deadline("Cheque must be presented to the bank by (3-month validity)", add_months(cd, 3) - timedelta(days=1), "FACT-RBI-CHEQUE-VALIDITY", "", today))
        memo = parse_date(f.get("memo_received_date"))
        if memo:
            out["deadlines"].append(_deadline("Send the legal demand notice by (30 days from bank's return memo)", memo + timedelta(days=30), "NIA1881-S138", "Count from the day you got the bank's information; send by registered post AD/speed post and keep receipts.", today))
        nrec = parse_date(f.get("notice_received_date"))
        if not nrec and parse_date(f.get("notice_sent_date")):
            nrec = parse_date(f.get("notice_sent_date")) + timedelta(days=5)
            assumed = True
        else:
            assumed = False
        if nrec:
            pay_by = nrec + timedelta(days=15)
            out["deadlines"].append(_deadline("Other side's 15 days to pay end on", pay_by, "NIA1881-S138", "Assumed delivery 5 days after posting; use the actual delivery date from tracking." if assumed else "", today, mine=False))
            out["deadlines"].append(_deadline("Last date to file the criminal complaint in court (1 month after the 15 days end)", add_months(pay_by, 1), "NIA1881-S142-1", "Courts can condone delay for sufficient cause, but don't rely on it.", today))

    elif category == "tenancy":
        ho = parse_date(f.get("possession_handed_over_date"))
        if ho:
            out["deadlines"].append(_deadline("Approximate last date to sue for the deposit (3 years)", add_months(ho, 36), "LIM1963-ART55", "Limitation depends on the exact claim; confirm with legal aid before relying on it.", today))
        dep, rent = parse_inr(f.get("deposit_amount")), parse_inr(f.get("monthly_rent"))
        if dep and rent and rent > 0:
            months = dep / rent
            out["derived"].append({"label": "Deposit size", "value": f"{months:.1f} × monthly rent", "basis": "MTA2021-S11", "note": "The Model Tenancy Act caps residential deposits at 2 months' rent, but it applies only in states that have adopted it, and usually only to new agreements."})

    elif category == "salary":
        lwd = parse_date(f.get("last_working_day"))
        if lwd:
            d, added = lwd, 0
            while added < 2:
                d += timedelta(days=1)
                if d.weekday() < 6:  # Mon-Sat counted as working days (assumption)
                    added += 1
            out["deadlines"].append(_deadline("Employer had to pay your full & final wages by (2 working days after you left)", d, "COW2019-S17", "This is the employer's legal deadline; if it has passed, the employer is in default. Assumes a Mon–Sat working week.", today, mine=False))
        due = parse_date(f.get("salary_due_date")) or lwd
        if due:
            out["deadlines"].append(_deadline("Approximate last date to file a wage claim with the labour authority (3 years)", add_months(due, 36), "COW2019-S45", "", today))

    elif category == "notice":
        rec = parse_date(f.get("received_date"))
        # first 1-3 digit number only: "15 days, by 20.03.2026" used to become 152032026 days (audit: OverflowError -> 500)
        m = re.search(r"\b(\d{1,3})\b", str(f.get("notice_deadline_days") or ""))
        days = int(m.group(1)) if m else 0
        if rec and 0 < days <= 365:
            out["deadlines"].append(_deadline(f"Deadline given in the notice ({days} days from receipt)", rec + timedelta(days=days), "", "This is the sender's deadline, not a court order. Missing it doesn't automatically mean you lose, but don't ignore it.", today, mine=True))

    return out


def completeness(category: str | None, facts: dict) -> dict:
    items = CHECKLISTS.get(category or "", [])
    if not items:
        return {"pct": 0, "missing": []}
    have = [k for k, _ in items if str((facts or {}).get(k, "")).strip() not in ("", "unknown", "null", "None")]
    missing = [{"key": k, "question": q} for k, q in items if k not in have]
    return {"pct": round(100 * len(have) / len(items)), "missing": missing}
