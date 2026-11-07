# Walkthrough video: 3 minutes (my own voice; Loom or OBS)

Rehearse once, then record in one take. Talk normally; don't read it word for word. The times are targets.

**Before recording**
- Record on a day I haven't been testing, so the free AI quota is fresh (Groq allows a limited number of answers a day, and when it runs out answers come from the slower backup model).
- Open https://haq-46bx.onrender.com in Chrome or Edge about 2 minutes early (the free server sleeps), sign in, and press Ctrl+Shift+R.
- Click **New case** so the screen is clean. Keep these ready to paste:
  - Deposit message (Hinglish): `mera landlord 40000 deposit wapas nahi kar raha, 31 aug ko flat chhoda tha Pune mein, agreement hai, painting ke 15000 kaat raha hai bina bill ke`
  - Draft answers: `Mera naam Priya Sharma hai, pata Flat 3B, 12 MG Road, Pune 411001. Landlord ka pata 45 FC Road, Pune 411004.`
  - One practice answer: `Sir, I left the flat on 31 August and returned the keys the same day. I paid 40,000 deposit and I have the rent agreement and the bank transfer.`
  - A real CNR whose case has a final order (services.ecourts.gov.in → Court Orders → Final Orders).
- Don't rehearse the practice hearing several times; it uses about 4 AI calls each time.

**0:00–0:20 The problem and my bet**
"I picked Problem 2. Most people give up on small legal problems like a deposit, a refund or unpaid salary. The danger with an AI lawyer is that it makes up law with total confidence. So Haq answers like a lawyer, but it can only cite law I've checked against official sources, and code checks every reply before you see it."

**0:20–0:55 A lawyer-style answer and a draft**
- Paste the deposit message. Point at *My view, Law on your side, What they will say, What I would do*. Click a law chip: "every section links to its official source."
- Click **Draft: Deposit refund notice**. The notice appears in the chat with questions for the missing details. Paste the answers and the blanks fill in. Click **Word**.

**0:55–1:20 Practice for court**
- Type `practice`. "The AI plays the judge and puts the landlord's side to me." Paste the practice answer, then type `stop`. The scorecard appears. "Suggested answers only use facts I gave; if a fact is missing it leaves a blank."

**1:20–1:45 A live court case**
- Paste the CNR. The card shows status, next hearing and orders from the eCourts record. Click **Explain** on the final order: "a plain summary that only restates the order."

**1:45–2:10 It stays a legal assistant, and names the law**
- Click **New case** (so the question isn't read as part of the deposit case), then ask `What is the right to equality?`. Point at the chips for Articles 14 to 18: "it names the exact articles, and only ones I've verified."
- Type `write me a poem about rain`. "It politely says no and offers legal help instead. That check happens on the server, not just in the app."

**2:10–2:40 How I know it works**
- Open `evals/outputs/20261106-195912/SUMMARY.md`: "22 test cases in 5 languages, 134 of 136 checks pass, and no unverified law reached the user."
- Open `evals/outputs/20261106-004742/baseline/T16_adversarial_case_law.json` (search "R. K. M."): "the same questions to a plain AI made up Supreme Court cases, cited the IPC, and told someone past their deadline they could still file."
- One honest failure: "When I told it to answer like a lawyer, it invented a painting cost. I banned that in the prompt, but it's a prompt rule, not a code check, so it's still a risk."

**2:40–3:00 Swapping the model, and what's next**
- ⚙︎ → switch from Groq to Gemini live: "any OpenAI-compatible model plugs in."
- "Next I'd have a lawyer review and grow the library, add verified case law, put it on WhatsApp, and hand cases to free legal aid with the file attached."
