"""Central configuration. Everything model-related is swappable via environment variables.

Any OpenAI-compatible endpoint works (Groq, Gemini, OpenRouter, OpenAI, Anthropic, Ollama,
or a custom endpoint such as an internal gateway). To swap the model, change env vars only:

    LLM_PROVIDER=gemini            # which preset to use as primary
    LLM_MODEL=gemini-2.5-flash     # optional override of the preset's main model
    LLM_FAST_MODEL=...             # optional override of the cheap/fast model (routing, judging)
    LLM_FALLBACKS=groq,openrouter  # tried in order on rate-limit / outage

    # Fully custom endpoint (e.g. an API key the interviewers provide):
    LLM_PROVIDER=custom
    CUSTOM_BASE_URL=https://.../v1
    CUSTOM_API_KEY=...
    CUSTOM_MODEL=...
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

try:  # optional: load .env when running locally
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
except Exception:  # pragma: no cover
    pass

ROOT = Path(__file__).resolve().parent.parent


@dataclass
class Provider:
    name: str
    base_url: str
    key_env: str
    main_model: str
    fast_model: str
    vision_model: str | None = None
    stt_model: str | None = None  # OpenAI-compatible /audio/transcriptions
    supports_json_mode: bool = True
    extra_headers: dict = field(default_factory=dict)
    alt_models: list = field(default_factory=list)  # tried (same provider) when the first model is rate-limited

    @property
    def api_key(self) -> str | None:
        return os.getenv(self.key_env) or None

    @property
    def configured(self) -> bool:
        # a local Ollama server counts as configured only if the user points to it explicitly
        return bool(self.api_key) or (self.name == "ollama" and bool(os.getenv("OLLAMA_BASE_URL")))


def _env(name: str, default: str | None = None) -> str | None:
    v = os.getenv(name)
    return v if v not in (None, "") else default


def _alts(name: str, default: str) -> list:
    """Comma-separated alternates; "none" disables them (used to pin a model for controlled evals)."""
    return [m.strip() for m in (_env(name, default) or "").split(",") if m.strip() and m.strip().lower() != "none"]


# Default model names are only defaults; every one can be overridden by env vars
# (e.g. GROQ_MODEL, GEMINI_FAST_MODEL). Free-tier model line-ups change often.
PRESETS: dict[str, Provider] = {
    "groq": Provider(
        name="groq",
        base_url="https://api.groq.com/openai/v1",
        key_env="GROQ_API_KEY",
        main_model=_env("GROQ_MODEL", "openai/gpt-oss-120b"),
        fast_model=_env("GROQ_FAST_MODEL", "openai/gpt-oss-20b"),
        vision_model=_env("GROQ_VISION_MODEL"),  # none on Groq's current free line-up
        stt_model=_env("GROQ_STT_MODEL", "whisper-large-v3"),
        alt_models=_alts("GROQ_ALT_MODELS", "qwen/qwen3.8-27b,openai/gpt-oss-20b"),
    ),
    "gemini": Provider(
        name="gemini",
        base_url="https://generativelanguage.googleapis.com/v1beta/openai",
        key_env="GEMINI_API_KEY",
        main_model=_env("GEMINI_MODEL", "gemini-3.5-flash"),
        fast_model=_env("GEMINI_FAST_MODEL", "gemini-3.1-flash-lite"),
        vision_model=_env("GEMINI_VISION_MODEL", "gemini-3.5-flash"),
        alt_models=_alts("GEMINI_ALT_MODELS", "gemini-3.1-flash-lite"),
    ),
    "openrouter": Provider(
        name="openrouter",
        base_url="https://openrouter.ai/api/v1",
        key_env="OPENROUTER_API_KEY",
        main_model=_env("OPENROUTER_MODEL", "meta-llama/llama-3.3-70b-instruct:free"),
        fast_model=_env("OPENROUTER_FAST_MODEL", "meta-llama/llama-3.3-70b-instruct:free"),
        extra_headers={"X-Title": "Haq AI legal helper"},
    ),
    "openai": Provider(
        name="openai",
        base_url="https://api.openai.com/v1",
        key_env="OPENAI_API_KEY",
        main_model=_env("OPENAI_MODEL", "gpt-4.1-mini"),
        fast_model=_env("OPENAI_FAST_MODEL", "gpt-4.1-nano"),
        vision_model=_env("OPENAI_VISION_MODEL", "gpt-4.1-mini"),
        stt_model=_env("OPENAI_STT_MODEL", "whisper-1"),
    ),
    "anthropic": Provider(  # Anthropic's OpenAI-SDK-compatible endpoint
        name="anthropic",
        base_url="https://api.anthropic.com/v1",
        key_env="ANTHROPIC_API_KEY",
        main_model=_env("ANTHROPIC_MODEL", "claude-sonnet-5-5"),
        fast_model=_env("ANTHROPIC_FAST_MODEL", "claude-haiku-5-5"),
        vision_model=_env("ANTHROPIC_MODEL", "claude-sonnet-5-5"),
        supports_json_mode=False,
    ),
    "ollama": Provider(
        name="ollama",
        base_url=_env("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
        key_env="OLLAMA_API_KEY",
        main_model=_env("OLLAMA_MODEL", "qwen2.5:7b"),
        fast_model=_env("OLLAMA_FAST_MODEL", "qwen2.5:7b"),
    ),
    "custom": Provider(
        name="custom",
        base_url=_env("CUSTOM_BASE_URL", "http://localhost:8000/v1"),
        key_env="CUSTOM_API_KEY",
        main_model=_env("CUSTOM_MODEL", "model"),
        fast_model=_env("CUSTOM_FAST_MODEL", _env("CUSTOM_MODEL", "model")),
        vision_model=_env("CUSTOM_VISION_MODEL"),
        stt_model=_env("CUSTOM_STT_MODEL"),
        supports_json_mode=_env("CUSTOM_JSON_MODE", "1") == "1",
    ),
}


def primary_provider_name() -> str:
    return _env("LLM_PROVIDER", "groq")


def provider_chain(preferred: str | None = None) -> list[Provider]:
    """Preferred provider first, then fallbacks; only configured ones."""
    names: list[str] = []
    for n in [preferred, primary_provider_name(), *(_env("LLM_FALLBACKS", "gemini,groq,openrouter").split(","))]:
        n = (n or "").strip()
        if n and n in PRESETS and n not in names:
            names.append(n)
    chain = [PRESETS[n] for n in names if PRESETS[n].configured]
    # allow a main-model override for the primary provider only
    return chain


def main_model_for(p: Provider) -> str:
    if p.name == primary_provider_name() and _env("LLM_MODEL"):
        return _env("LLM_MODEL")  # type: ignore[return-value]
    return p.main_model


def fast_model_for(p: Provider) -> str:
    if p.name == primary_provider_name() and _env("LLM_FAST_MODEL"):
        return _env("LLM_FAST_MODEL")  # type: ignore[return-value]
    return p.fast_model


def stt_provider() -> Provider | None:
    for name in [_env("STT_PROVIDER", ""), "groq", "openai", "custom"]:
        p = PRESETS.get(name or "")
        if p and p.configured and p.stt_model:
            return p
    return None


def supabase_url() -> str | None:
    """Supabase project URLs always end in .supabase.co; fix common typos (".com", spaces, trailing slash)."""
    u = (os.getenv("SUPABASE_URL") or "").strip().rstrip("/")
    if not u:
        return None
    if u.endswith(".supabase.com"):
        u = u[: -len(".supabase.com")] + ".supabase.co"
    if not u.startswith("http"):
        u = "https://" + u
    return u


def public_config() -> dict:
    return {
        "primary": primary_provider_name(),
        "providers": [
            {"name": p.name, "configured": p.configured, "main_model": main_model_for(p), "fast_model": fast_model_for(p)}
            for p in PRESETS.values()
            if p.configured
        ],
        "stt": bool(stt_provider()),
    }
