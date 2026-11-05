# Walkthrough video: 3 minutes (record in your own voice; Loom or OBS)

Rehearse once, then record in one take. Speak naturally and don't read word for word. Times are targets.

**0:00–0:20: The problem and my bet**
"I picked Problem 2. Most people give up on everyday legal problems: a deposit, a refund, unpaid salary. The danger with an AI lawyer is that it confidently invents law. So I built Haq around one rule: it can only cite law I've verified, and code checks every reply."

**0:20–1:20: Live demo (Hinglish deposit case)**
- Type: *"mera landlord 40000 deposit wapas nahi kar raha, 31 aug ko flat chhoda tha Pune mein, agreement hai"*
- Show: the reply in Hinglish → the **case file** filling up on the right → **Deadlines** tab (computed by code, with a source link) → click a **law chip** to show the official source.
- Click **Draft: Deposit refund notice** → show the `[[FILL]]` gaps (never invented) → **Download Word**.
- 10 seconds on **Practice**: one line to the "landlord", then the feedback scores.

**1:20–1:50: Safety and honesty**
- Type a cheque case where the 30-day window has passed. Show that Haq says it has passed and escalates to a lawyer / legal aid 15100.
- (Optional) Type "give me 3 Supreme Court judgments". Haq declines to invent them.

**1:50–2:30: How I know it works**
- Open `evals/outputs/<run>/SUMMARY.md`: "22 test cases in 5 languages, X/Y automatic checks pass, and zero unverified legal references reached the user."
- Open a baseline file: "The same questions to a plain LLM: it invented three Supreme Court judgments and cited the IPC, which was replaced in 2024."
- Name one honest failure from the summary.

**2:30–3:00: Swap and scale**
- Switch the ⚙︎ model dropdown from Groq to Gemini live, or show `.env`: "Any OpenAI-compatible model plugs in, including yours."
- "Next: grow the library with a lawyer's review, add a WhatsApp channel, and send deadline reminders."
