"""
AIAS Day 1 — Hello World
Verifies that all three model APIs work from this machine.
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_KEY = os.getenv("GOOGLE_API_KEY")

PROMPT = "Say hello in exactly one short sentence."


def call_openai():
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_KEY)
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[{"role": "user", "content": PROMPT}],
    )
    return response.choices[0].message.content


def call_anthropic():
    import anthropic
    client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=100,
        messages=[{"role": "user", "content": PROMPT}],
    )
    return message.content[0].text


def call_google():
    from google import genai
    client = genai.Client(api_key=GOOGLE_KEY)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=PROMPT,
    )
    return response.text


def main():
    print("=" * 60)
    print("AIAS Day 1 — Hello World")
    print("=" * 60)

    missing = []
    if not OPENAI_KEY: missing.append("OPENAI_API_KEY")
    if not ANTHROPIC_KEY: missing.append("ANTHROPIC_API_KEY")
    if not GOOGLE_KEY: missing.append("GOOGLE_API_KEY")
    if missing:
        print(f"\nERROR: Missing keys in .env: {', '.join(missing)}")
        sys.exit(1)

    providers = [
        ("OpenAI    (gpt-5.4-mini)",      call_openai),
        ("Anthropic (claude-sonnet-4-6)", call_anthropic),
        ("Google    (gemini-2.5-flash)",  call_google),
    ]

    results = {}
    for name, fn in providers:
        print(f"\n-> {name}")
        try:
            answer = fn()
            print(f"   OK: {answer.strip()}")
            results[name] = "OK"
        except Exception as e:
            print(f"   FAILED: {type(e).__name__}: {e}")
            results[name] = f"FAILED: {type(e).__name__}"

    print("\n" + "=" * 60)
    print("Summary:")
    for name, status in results.items():
        print(f"  {name}: {status}")
    print("=" * 60)


if __name__ == "__main__":
    main()
