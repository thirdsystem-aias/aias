"""Fingerprint SerpAPI key in shell env vs .env file.

No full-value exposure — only length, first 4 chars, last 4 chars.
Compare against the SerpAPI dashboard's active key fingerprint to diagnose
which of the failure modes applies (stale shell, unchanged .env, typo, etc.).

Run after `source ~/aias/.env`:
    python3 ~/aias/scripts/diagnose_serpapi_key.py
"""
import os
import re
import pathlib


def fp(s: str) -> str:
    """Return a value-hiding fingerprint string."""
    return f"len={len(s)}, prefix={s[:4]}, suffix={s[-4:]}"


# 1. Shell environment
shell_val = os.environ.get("SERPAPI_KEY", "")
if shell_val:
    print(f"shell env:  {fp(shell_val)}")
else:
    print("shell env:  SERPAPI_KEY not set")

# 2. .env file
env_path = pathlib.Path.home() / "aias" / ".env"
try:
    text = env_path.read_text()
    # Match `export SERPAPI_KEY=<value>` or `SERPAPI_KEY=<value>`
    # with optional quotes around the value
    m = re.search(r'SERPAPI_KEY\s*=\s*"?([^"\n]+)"?', text)
    if m:
        env_val = m.group(1).strip().rstrip('"')
        print(f".env file:  {fp(env_val)}")
    else:
        print(".env file:  SERPAPI_KEY line not found in ~/aias/.env")
except FileNotFoundError:
    print(".env file:  ~/aias/.env not found")

# 3. Compare
if shell_val:
    try:
        if env_val == shell_val:
            print()
            print("→ Shell env and .env file MATCH. If smoke test still 401s,")
            print("  the key is either invalid at SerpAPI or rotation didn't take.")
            print("  Check https://serpapi.com/manage-api-key — is the displayed")
            print("  active key's prefix/suffix the same as above?")
        else:
            print()
            print("→ Shell env and .env file DIFFER. Run: source ~/aias/.env")
    except NameError:
        # env_val undefined if file parsing failed
        pass
