# Deploying Haq (free)

## A. GitHub (the code + raw outputs link)

1. Go to https://github.com/new. Name: `haq-ai-lawyer`. Visibility: **Public**. Don't add a README (we have one). Click **Create repository**.
2. In VS Code's terminal, in the `haq` folder:
   ```
   git remote add origin https://github.com/<your-username>/haq-ai-lawyer.git
   git push -u origin main
   ```
   A browser window asks you to sign in to GitHub the first time. Approve it.
3. Open the repo page in a private/incognito window to confirm anyone can see it.

## B. Hugging Face Spaces (the live app link)

1. Create a free account at https://huggingface.co/join.
2. Go to https://huggingface.co/new-space:
   - Space name: `haq`
   - SDK: **Docker** → template **Blank**
   - Hardware: **CPU basic (free)**
   - Visibility: **Public**
   - Click **Create Space**
3. In the Space, open **Settings → Variables and secrets**:
   - **New secret** `GROQ_API_KEY` = your Groq key
   - **New secret** `GEMINI_API_KEY` = your Gemini key
   - **New variable** `LLM_PROVIDER` = `groq`
4. Create an access token: https://huggingface.co/settings/tokens → **Create new token** → type **Write** → copy it.
5. In the VS Code terminal (in `haq`):
   ```
   git remote add space https://huggingface.co/spaces/<your-hf-username>/haq
   git push space main
   ```
   When asked for a username, enter your HF username. For the password, paste the **token** (not your password).
6. The Space builds for 2–4 minutes (watch the **Logs** tab). When it shows **Running**, open `https://<your-hf-username>-haq.hf.space`.

## Updating later
After any change: `git add -A`, `git commit -m "..."`, `git push origin main`, `git push space main`.

## Notes
- The free Space sleeps after ~48h of inactivity and wakes on the next visit (about 30s). Open it before your interview.
- Voice input uses Groq Whisper on the server (needs `GROQ_API_KEY`). In Chrome/Edge it falls back to the browser's speech recognition.
- Never commit `.env`. It's in `.gitignore`.
