"""
protocol/providers.py — frontier-model provider abstraction (v1.4 canonical)

Single dispatch point for the 6-slot reference panel. Three providers
behind one route_call() interface.

Authentication via environment variables:
  - ANTHROPIC_API_KEY
  - OPENAI_API_KEY
  - GOOGLE_API_KEY        (or GEMINI_API_KEY — google SDK accepts both)

Retry policy: 3 attempts with exponential backoff (1s, 2s, 4s) on transient
errors (rate limits, 5xx, network timeouts). Permanent errors (auth, model
not found) fail immediately.

Dependencies: anthropic, openai, google-generativeai (install via pip).
"""

import os
import time
from typing import TypedDict


class ProviderResponse(TypedDict):
    raw_response: str
    tokens_in: int
    tokens_out: int
    latency_ms: int
    model: str
    finish_reason: str


# ============================================================
# Common retry wrapper
# ============================================================

class TransientProviderError(Exception):
    """Rate-limit, 5xx, or network error — retry-eligible."""


def _retry(fn, *args, max_attempts: int = 3, base_delay: float = 1.0, **kwargs):
    last_exc = None
    for attempt in range(max_attempts):
        try:
            return fn(*args, **kwargs)
        except TransientProviderError as e:
            last_exc = e
            if attempt < max_attempts - 1:
                time.sleep(base_delay * (2 ** attempt))
    raise last_exc  # exhausted


# ============================================================
# Anthropic
# ============================================================

_anthropic_client = None

def _get_anthropic_client():
    global _anthropic_client
    if _anthropic_client is None:
        import anthropic
        _anthropic_client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    return _anthropic_client


def _call_anthropic_once(model: str, prompt: str) -> ProviderResponse:
    import anthropic
    client = _get_anthropic_client()
    start = time.time()
    try:
        resp = client.messages.create(
            model=model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
    except anthropic.RateLimitError as e:
        raise TransientProviderError(f"Anthropic rate limit: {e}") from e
    except anthropic.APIStatusError as e:
        if 500 <= e.status_code < 600:
            raise TransientProviderError(f"Anthropic 5xx: {e}") from e
        raise
    latency_ms = int((time.time() - start) * 1000)
    text = "".join(b.text for b in resp.content if hasattr(b, "text"))
    return ProviderResponse(
        raw_response=text,
        tokens_in=resp.usage.input_tokens,
        tokens_out=resp.usage.output_tokens,
        latency_ms=latency_ms,
        model=model,
        finish_reason=resp.stop_reason or "stop",
    )


def call_anthropic(model: str, prompt: str) -> ProviderResponse:
    return _retry(_call_anthropic_once, model, prompt)


# ============================================================
# OpenAI
# ============================================================

_openai_client = None

def _get_openai_client():
    global _openai_client
    if _openai_client is None:
        import openai
        _openai_client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    return _openai_client


def _call_openai_once(model: str, prompt: str) -> ProviderResponse:
    import openai
    client = _get_openai_client()
    start = time.time()
    try:
        resp = client.chat.completions.create(
            model=model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
    except openai.RateLimitError as e:
        raise TransientProviderError(f"OpenAI rate limit: {e}") from e
    except openai.APIStatusError as e:
        if 500 <= e.status_code < 600:
            raise TransientProviderError(f"OpenAI 5xx: {e}") from e
        raise
    latency_ms = int((time.time() - start) * 1000)
    choice = resp.choices[0]
    return ProviderResponse(
        raw_response=choice.message.content or "",
        tokens_in=resp.usage.prompt_tokens,
        tokens_out=resp.usage.completion_tokens,
        latency_ms=latency_ms,
        model=model,
        finish_reason=choice.finish_reason or "stop",
    )


def call_openai(model: str, prompt: str) -> ProviderResponse:
    return _retry(_call_openai_once, model, prompt)


# ============================================================
# Google (Gemini)
# ============================================================

_google_configured = False

def _configure_google():
    global _google_configured
    if not _google_configured:
        import google.generativeai as genai
        key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
        if not key:
            raise KeyError("GOOGLE_API_KEY (or GEMINI_API_KEY) not set")
        genai.configure(api_key=key)
        _google_configured = True


def _call_google_once(model: str, prompt: str) -> ProviderResponse:
    import google.generativeai as genai
    from google.api_core import exceptions as g_exc
    _configure_google()
    client = genai.GenerativeModel(model)
    start = time.time()
    try:
        resp = client.generate_content(
            prompt,
            generation_config={"max_output_tokens": 1024},
        )
    except g_exc.ResourceExhausted as e:
        raise TransientProviderError(f"Google rate limit: {e}") from e
    except g_exc.ServiceUnavailable as e:
        raise TransientProviderError(f"Google 5xx: {e}") from e
    except g_exc.DeadlineExceeded as e:
        raise TransientProviderError(f"Google timeout: {e}") from e
    latency_ms = int((time.time() - start) * 1000)
    text = resp.text if hasattr(resp, "text") else ""
    usage = getattr(resp, "usage_metadata", None)
    tokens_in = usage.prompt_token_count if usage else 0
    tokens_out = usage.candidates_token_count if usage else 0
    finish = "stop"
    if resp.candidates:
        finish = str(resp.candidates[0].finish_reason).lower()
    return ProviderResponse(
        raw_response=text,
        tokens_in=tokens_in,
        tokens_out=tokens_out,
        latency_ms=latency_ms,
        model=model,
        finish_reason=finish,
    )


def call_google(model: str, prompt: str) -> ProviderResponse:
    return _retry(_call_google_once, model, prompt)


# ============================================================
# Dispatch
# ============================================================

def route_call(model: str, prompt: str) -> ProviderResponse:
    """Single entry point — phase scripts only call this."""
    if model.startswith("claude-"):
        return call_anthropic(model, prompt)
    if model.startswith("gpt-"):
        return call_openai(model, prompt)
    if model.startswith("gemini-"):
        return call_google(model, prompt)
    raise ValueError(f"Unrouted model identifier: {model}")
