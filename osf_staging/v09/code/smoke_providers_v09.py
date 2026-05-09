"""Provider smoke test for v0.9 — calls each model slot once with a trivial prompt.

Confirms all 4 providers (anthropic, openai, google, xai) have working auth and
correct model strings before committing the full v0.9 token budget. Run from
~/aias root after the schema fix has been committed.

Usage:
    cd ~/aias
    python3 smoke_providers_v09.py
"""
import sys
sys.path.insert(0, '.')

from run_aias_v2 import call_openai, call_anthropic, call_google, call_xai, MODELS

CALLERS = {
    'openai': call_openai,
    'anthropic': call_anthropic,
    'google': call_google,
    'xai': call_xai,
}
TEST_PROMPT = "Say OK and nothing else."

print('Provider smoke test: one call per model slot')
print('-' * 60)

for slot, info in MODELS.items():
    provider = info['provider']
    model = info['model']
    use_temp = info.get('supports_temperature', True)
    try:
        result = CALLERS[provider](TEST_PROMPT, model, use_temp)
        snippet = (result[:40] + '...') if len(result) > 40 else result
        print(f'  {slot:20s} ({provider:10s}): OK   | {snippet!r}')
    except Exception as e:
        msg = str(e)[:80]
        print(f'  {slot:20s} ({provider:10s}): FAIL | {type(e).__name__}: {msg}')

print('-' * 60)
print('Done. If all 6 lines say OK, proceed to full v0.9 measurement run.')
