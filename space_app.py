"""Entry point for a Hugging Face *Gradio* Space (free tier).

Haq is a FastAPI app with its own HTML/JS front-end; it doesn't use Gradio components.
A Gradio Space simply runs this file, so we start the same FastAPI app with uvicorn on
the port Spaces expose (7860). Locally, use `uvicorn app.main:app` instead.
"""
import os

import uvicorn

from app.main import app

if __name__ == "__main__":
    port = int(os.getenv("GRADIO_SERVER_PORT") or os.getenv("PORT") or 7860)
    uvicorn.run(app, host="0.0.0.0", port=port)
