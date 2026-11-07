# Walkthrough video: 3 minutes (your own voice; Loom or OBS)

Rehearse once, then record in one take. Speak naturally; don't read word for word. Times are targets.

**Before you record**
- Open https://haq-46bx.onrender.com in Chrome or Edge, signed in, and press Ctrl+Shift+R. Open it about 2 minutes early: the free server sleeps and the first load is slow.
- Click **New case** so the screen is clean. Keep these ready to paste:
  - Deposit message (Hinglish): `mera landlord 40000 deposit wapas nahi kar raha, 31 aug ko flat chhoda tha Pune mein, agreement hai, painting ke 15000 kaat raha hai bina bill ke`
  - Draft answers: `Mera naam Priya Sharma hai, pata Flat 3B, 12 MG Road, Pune 411001. Landlord ka pata 45 FC Road, Pune 411004.`
  - Two answers for the practice hearing:
    - `Sir, I left the flat on 31 August and returned the keys the same day. I paid 40,000 deposit and I have the rent agreement and the bank transfer.`
    - `The landlord gave no bill for the painting. After normal use some painting is wear and tear, and I have photos from the day I left.`
  - A real CNR whose case has a **final order**: on services.ecourts.gov.in → Court Orders → Final Orders, copy one CNR.
- Don't click around a lot beforehand: the free AI quota is limited (about 40 full answers a day on the main model). The practice hearing alone uses about 4 AI calls, so don't rehearse it several times before recording.

**0:00–0:20: The problem and my bet**
"I picked Problem 2. Most people give up on everyday legal problems: a deposit, a refund, unpaid salary. The danger with an AI lawyer is that it confidently invents law. So Haq answers like a lawyer, but it can only cite law I've verified, and code checks every reply."

**0:20–1:00: A lawyer-style answer + a draft**
- Paste the deposit message. Point at: **My view → Law on your side → What they will say, and your answer → What I would do**. "It takes a position and anticipates the landlord's argument, but every section it names is checked against official sources." Click a **law chip** to show its official source.
- Ask a follow-up: `agreement mein likha hai ki painting tenant karega, phir bhi 15000 kaat sakta hai?`. It answers directly ("It depends on one thing…"). Below this answer, Haq offers: **"Want to prepare for court? Just reply practice."** Leave it for now.
- Click **Draft: Deposit refund notice**. The notice appears in the chat, with questions for what's missing. Paste the answers: the blanks fill in. Click **Word**.

**1:00–1:30: Practice for court, in the same chat**
- Type `practice`. "Most people freeze in front of a judge, so Haq lets you rehearse. The AI plays the judge and puts the landlord's arguments to you, one question at a time." The bar above the message box shows the hearing is on.
- Paste the two practice answers, one after each question from the judge.
- Type `stop`. The scorecard appears: scores out of 5 for facts, proof, answering the question, what you're asking for, and composure, plus answers to try and documents to bring. "The suggested answers use only facts I gave. When a fact is missing it writes a blank like [date], and code drops any line with a number I never said."
- (If the offer box didn't appear, typing `practice` still starts the hearing.)

**1:30–2:00: Live court case**
- Paste the CNR into the chat. The case card shows status, next hearing and orders, straight from the eCourts record. Click **Add to calendar** (just show it).
- Click **Explain** on the final order. "A plain-language summary that only restates the order. The full text is below it."

**2:00–2:35: How I know it works**
- Open `evals/outputs/<latest run>/SUMMARY.md`: "22 test cases in 5 languages, <checks> automatic checks pass, and zero unverified legal references reached the user."
- Open a baseline file: "The same questions to a plain LLM: it invented Supreme Court judgments, cited the IPC (replaced in 2024), and told a user whose deadline had passed that they could still file."
- Name one honest failure: "When I told it to answer like a lawyer, it invented a painting cost. I banned unsourced figures, but that's a prompt rule, not a code check, so it's a residual risk."

**2:35–3:00: Swap and scale**
- ⚙︎ → switch the AI model from Groq to Gemini live: "Any OpenAI-compatible model plugs in."
- "Next: a lawyer reviews and grows the library, real case law via Indian Kanoon, a WhatsApp channel, and a hand-off to free legal aid with the case file attached."
