# Deploying Haq

The live app runs on Render's free plan: https://haq-46bx.onrender.com. The code is on GitHub: https://github.com/Mohit4905/haq-ai-lawyer. Every push to `main` redeploys the app automatically.

## Render (how the live app is set up)
1. On https://render.com, sign in with GitHub, choose **New → Blueprint** and pick `haq-ai-lawyer`. It reads `render.yaml`.
2. Under **Environment**, add the keys. Only the first two are needed for the chat; the rest switch on extra features.

| Variable | What it's for |
|---|---|
| `GROQ_API_KEY` | Main AI models and voice input (free tier) |
| `GEMINI_API_KEY` | Backup AI model (free tier) |
| `LLM_PROVIDER` | Which provider to try first (`groq`) |
| `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY` | Accounts and saving cases (optional; without them everyone uses guest mode) |
| `SUPABASE_GOOGLE_LOGIN` | Shows "Continue with Google" (optional) |
| `BREVO_API_KEY`, `REMINDER_FROM_EMAIL`, `PUBLIC_APP_URL`, `CRON_SECRET` | Deadline reminder emails (optional) |
| `ECOURTS_API_KEY` | Live court records by CNR (optional, paid credits) |

3. Click **Apply**. The free plan sleeps when nobody uses it, so the first request after a while takes about 50 seconds. Open the app a few minutes before a demo.

Never put keys in the code or in chat. They live only in Render's Environment page and in your local `.env`, which is in `.gitignore`.

## Running it locally
See "Running it yourself" in the README. Copy `.env.example` to `.env` and add at least `GROQ_API_KEY` or `GEMINI_API_KEY`.

## Using a different model
Set these in `.env` or on Render, then restart. No code changes needed:
```
LLM_PROVIDER=custom
CUSTOM_BASE_URL=<endpoint>/v1
CUSTOM_API_KEY=<key>
CUSTOM_MODEL=<model name>
```

## Hugging Face Spaces (alternative)
`space_app.py` starts the same app inside a Gradio Space, if you'd rather host it there: create a Gradio Space on the free CPU, add `GROQ_API_KEY` and `GEMINI_API_KEY` as secrets, and push the repo to the Space's git remote.
