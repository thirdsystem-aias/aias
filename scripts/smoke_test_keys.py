"""AIAS smoke test — verifies 3 provider keys post-rotation.

Hits each API with minimal cost:
  - Anthropic: 1 message, claude-sonnet-4-6, 10 max_tokens
  - OpenAI:    1 message, gpt-5.4-mini, no token cap (matches run_aias_v2.py)
  - SerpAPI:   /account endpoint (no search burn)

Run from anywhere after `source ~/aias/.env`:
    python3 ~/aias/scripts/smoke_test_keys.py
"""
import os
import sys

print("=== AIAS smoke test: 3 providers ===")
print()

passed = 0
failed = 0

# 1. Anthropic — claude-sonnet-4-6 (MATCHED_MODEL)
try:
    import anthropic
    c = anthropic.Anthropic()
    m = c.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=10,
        messages=[{"role": "user", "content": "Reply with the single word ok"}],
    )
    print(f"✓ Anthropic: reply={m.content[0].text!r}  "
          f"model={m.model}  "
          f"tokens={m.usage.input_tokens}in/{m.usage.output_tokens}out")
    passed += 1
except Exception as e:
    print(f"✗ Anthropic FAILED: {type(e).__name__}: {e}")
    failed += 1

# 2. OpenAI — gpt-5.4-mini (MATCHED_MODEL)
# Note: no max_tokens param — newer OpenAI models deprecated it in favor of
# max_completion_tokens. run_aias_v2.py doesn't pass either, so we match that
# behavior to validate the real pipeline shape.
try:
    from openai import OpenAI
    c = OpenAI()
    r = c.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[{"role": "user", "content": "Reply with the single word ok"}],
    )
    print(f"✓ OpenAI:    reply={r.choices[0].message.content!r}  "
          f"model={r.model}")
    passed += 1
except Exception as e:
    print(f"✗ OpenAI FAILED: {type(e).__name__}: {e}")
    failed += 1

# 3. SerpAPI — /account endpoint (no search burn)
# Note: SerpAPI auth uses query params, so HTTPError messages would normally
# include the api_key in the URL. We catch HTTPError separately to strip the URL
# from the printed error and avoid re-leaking on auth failures.
try:
    import requests
    serpapi_key = os.environ.get("SERPAPI_KEY")
    if not serpapi_key:
        raise RuntimeError("SERPAPI_KEY not set in environment")
    r = requests.get(
        "https://serpapi.com/account",
        params={"api_key": serpapi_key},
        timeout=10,
    )
    r.raise_for_status()
    j = r.json()
    print(f"✓ SerpAPI:   email={j.get('account_email')}  "
          f"plan={j.get('plan_name', '?')}  "
          f"searches_left={j.get('total_searches_left', j.get('searches_left', '?'))}")
    passed += 1
except requests.HTTPError as e:
    status = e.response.status_code if e.response is not None else "?"
    diagnosis = {
        401: "key rejected — either not yet rotated, or .env has old/wrong value, or didn't reload .env",
        403: "key valid but lacks permission — check account status",
        429: "rate limited",
    }.get(status, f"HTTP {status}")
    print(f"✗ SerpAPI FAILED: HTTP {status} — {diagnosis}")
    failed += 1
except Exception as e:
    print(f"✗ SerpAPI FAILED: {type(e).__name__}: {e}")
    failed += 1

print()
print(f"Summary: {passed} passed, {failed} failed")
sys.exit(0 if failed == 0 else 1)
