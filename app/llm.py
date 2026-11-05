"""Provider-agnostic LLM client (OpenAI-compatible chat completions) with fallback.

One function, `chat()`, is used everywhere. It tries the preferred provider and falls
back on rate limits / outages, and records which model actually answered so every
output can be traced (shown in the UI and saved in eval outputs).
"""
from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass, field

import httpx

from .config import Provider, fast_model_for, main_model_for, provider_chain, stt_provider

TIMEOUT = httpx.Timeout(90.0, connect=15.0)


class LLMError(RuntimeError):
    pass


@dataclass
class LLMResult:
    text: str
    provider: str
    model: str
    latency_s: float
    usage: dict = field(default_factory=dict)
    attempts: list = field(default_factory=list)

    def meta(self) -> dict:
        return {
            "provider": self.provider,
            "model": self.model,
            "latency_s": round(self.latency_s, 2),
            "usage": self.usage,
            "fallback_attempts": self.attempts,
        }


def _post(p: Provider, model: str, messages: list, temperature: float, json_mode: bool, max_tokens: int, reasoning: str | None = None) -> dict:
    headers = {"Content-Type": "application/json", **p.extra_headers}
    if p.api_key:
        headers["Authorization"] = f"Bearer {p.api_key}"
    if p.name == "anthropic" and p.api_key:
        headers["x-api-key"] = p.api_key
    body: dict = {"model": model, "messages": messages, "temperature": temperature, "max_tokens": max_tokens}
    if json_mode and p.supports_json_mode:
        body["response_format"] = {"type": "json_object"}
    if reasoning and p.name in ("groq", "gemini", "openai", "openrouter"):
        # reasoning models spend output tokens thinking; keep it bounded for latency/cost
        body["reasoning_effort"] = reasoning
        body["max_tokens"] = max_tokens + 1500
    r = httpx.post(f"{p.base_url.rstrip('/')}/chat/completions", headers=headers, json=body, timeout=TIMEOUT)
    if r.status_code >= 400:
        raise LLMError(f"{p.name}/{model} HTTP {r.status_code}: {r.text[:700]}")
    return r.json()


def chat(
    messages: list,
    *,
    tier: str = "main",  # "main" | "fast" | "vision"
    json_mode: bool = False,
    temperature: float = 0.2,
    max_tokens: int = 1800,
    provider: str | None = None,
    retries_per_provider: int = 3,
    reasoning: str | None = "low",
    strict_provider: bool = False,  # True: never fall back to another provider (e.g. an independent judge)
) -> LLMResult:
    from .config import PRESETS

    chain = [PRESETS[provider]] if (strict_provider and provider in PRESETS and PRESETS[provider].configured) else provider_chain(provider)
    if not chain:
        raise LLMError("No LLM provider configured. Set GROQ_API_KEY or GEMINI_API_KEY (see README).")
    attempts = []
    for p in chain:
        if tier == "vision":
            models = [p.vision_model] if p.vision_model else []
            if not models:
                attempts.append(f"{p.name}: no vision model")
                continue
        else:
            first = main_model_for(p) if tier == "main" else fast_model_for(p)
            # same-provider alternates first: free tiers rate-limit per model, not per account
            models = list(dict.fromkeys([first, *p.alt_models]))
        for model in models:
            jm, rs = json_mode, reasoning
            for attempt in range(retries_per_provider):
                t0 = time.time()
                try:
                    data = _post(p, model, messages, temperature, jm, max_tokens, rs)
                    text = (data.get("choices") or [{}])[0].get("message", {}).get("content") or ""
                    if not text.strip():
                        raise LLMError(f"{p.name}/{model} returned empty content")
                    return LLMResult(text, p.name, model, time.time() - t0, data.get("usage") or {}, attempts)
                except (LLMError, httpx.HTTPError) as e:
                    msg = str(e) or type(e).__name__
                    attempts.append(f"{p.name}/{model}: {msg[:400]}")
                    if "reasoning" in msg and "400" in msg and rs:
                        rs = None  # model doesn't support the knob; retry without it
                        continue
                    if "json_validate_failed" in msg or "response_format" in msg:
                        jm = False  # some models reject JSON mode on a given prompt
                        continue
                    if "429" in msg:
                        wait = _retry_after(msg)
                        if wait is not None and wait <= MAX_WAIT_S and attempt + 1 < retries_per_provider:
                            time.sleep(wait + 0.5)  # per-minute token limit: a short wait is cheaper than a weaker model
                            continue
                        break  # long/unknown wait -> next model
                    if any(s in msg for s in ("500", "502", "503", "504", "empty content")) and attempt + 1 < retries_per_provider:
                        time.sleep(2.0 * (attempt + 1))
                        continue
                    break  # timeouts and other errors -> next model
    raise LLMError("All providers failed: " + " | ".join(attempts[-4:]))


MAX_WAIT_S = float(__import__("os").getenv("LLM_MAX_WAIT_S", "25"))


def _retry_after(msg: str) -> float | None:
    m = re.search(r"try again in (?:(\d+)m)?([\d.]+)s", msg)
    if m:
        return float(m.group(1) or 0) * 60 + float(m.group(2))
    m = re.search(r"try again in ([\d.]+)ms", msg)
    return float(m.group(1)) / 1000 if m else None


_FENCE = re.compile(r"^```(?:json)?\s*|\s*```$", re.MULTILINE)


def parse_json(text: str) -> dict:
    """Tolerant JSON extraction (models sometimes wrap JSON in prose or fences)."""
    t = _FENCE.sub("", text.strip())
    try:
        return json.loads(t)
    except json.JSONDecodeError:
        pass
    start, end = t.find("{"), t.rfind("}")
    if start != -1 and end > start:
        try:
            return json.loads(t[start : end + 1])
        except json.JSONDecodeError:
            pass
    raise LLMError(f"Model did not return valid JSON: {text[:300]}")


def chat_json(messages: list, **kw) -> tuple[dict, LLMResult]:
    """chat() + parse; one repair retry if the JSON is malformed."""
    res = chat(messages, json_mode=True, **kw)
    try:
        return parse_json(res.text), res
    except LLMError:
        fix = messages + [
            {"role": "assistant", "content": res.text},
            {"role": "user", "content": "That was not valid JSON. Return ONLY the JSON object, nothing else."},
        ]
        res2 = chat(fix, json_mode=True, **kw)
        return parse_json(res2.text), res2


def transcribe(audio: bytes, filename: str, language: str | None = None) -> dict:
    p = stt_provider()
    if not p:
        raise LLMError("No speech-to-text provider configured (set GROQ_API_KEY).")
    files = {"file": (filename, audio)}
    data = {"model": p.stt_model, "response_format": "verbose_json"}
    if language:
        data["language"] = language
    r = httpx.post(
        f"{p.base_url.rstrip('/')}/audio/transcriptions",
        headers={"Authorization": f"Bearer {p.api_key}"},
        files=files,
        data=data,
        timeout=TIMEOUT,
    )
    if r.status_code >= 400:
        raise LLMError(f"STT HTTP {r.status_code}: {r.text[:300]}")
    j = r.json()
    return {"text": j.get("text", "").strip(), "language": j.get("language"), "provider": p.name, "model": p.stt_model}
