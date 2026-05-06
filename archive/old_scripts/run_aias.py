"""
AIAS Day 2 — First Real Measurement
Queries 5 prompts × 3 models × 5 runs = 75 API calls.
Saves raw responses + structured brand mentions to CSV.
"""

import os
import sys
import json
import csv
import time
import re
from datetime import datetime
from itertools import product
from dotenv import load_dotenv

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_KEY = os.getenv("GOOGLE_API_KEY")

# ----- CONFIG -----
RUNS_PER_PROMPT = 5
TEMPERATURE = 0.7  # day 2 keeps it simple, all runs at same temp

MODELS = {
    "openai":    {"label": "OpenAI gpt-5.4-mini",        "model": "gpt-5.4-mini"},
    "anthropic": {"label": "Anthropic claude-sonnet-4-6", "model": "claude-sonnet-4-6"},
    "google":    {"label": "Google gemini-2.5-flash",     "model": "gemini-2.5-flash"},
}

# ----- LOAD INPUTS -----
with open("brands.json") as f:
    BRANDS = json.load(f)

with open("prompts.json") as f:
    PROMPTS = json.load(f)


# ----- MODEL CALLERS -----
def call_openai(prompt_text):
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_KEY)
    response = client.chat.completions.create(
        model=MODELS["openai"]["model"],
        messages=[{"role": "user", "content": prompt_text}],
        temperature=TEMPERATURE,
    )
    return response.choices[0].message.content


def call_anthropic(prompt_text):
    import anthropic
    client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
    message = client.messages.create(
        model=MODELS["anthropic"]["model"],
        max_tokens=1024,
        temperature=TEMPERATURE,
        messages=[{"role": "user", "content": prompt_text}],
    )
    return message.content[0].text


def call_google(prompt_text):
    from google import genai
    from google.genai import types
    client = genai.Client(api_key=GOOGLE_KEY)
    response = client.models.generate_content(
        model=MODELS["google"]["model"],
        contents=prompt_text,
        config=types.GenerateContentConfig(temperature=TEMPERATURE),
    )
    return response.text


CALLERS = {
    "openai":    call_openai,
    "anthropic": call_anthropic,
    "google":    call_google,
}


# ----- BRAND DETECTION (simple word-boundary matching) -----
def detect_brands(text):
    """
    Returns a list of canonical brand names mentioned in the text.
    Uses case-insensitive whole-word matching against each alias.
    Each brand counted at most once per response.
    """
    text_lower = text.lower()
    found = []
    for brand in BRANDS:
        for alias in brand["aliases"]:
            # whole word match: alias must be bordered by non-word chars
            pattern = r"\b" + re.escape(alias.lower()) + r"\b"
            if re.search(pattern, text_lower):
                found.append(brand["canonical"])
                break  # don't double-count if multiple aliases match
    return found


# ----- MAIN LOOP -----
def main():
    print("=" * 70)
    print(f"AIAS Day 2 — Measurement Run")
    print(f"Started:  {datetime.now().isoformat(timespec='seconds')}")
    print(f"Plan:     {len(PROMPTS)} prompts × {len(MODELS)} models × {RUNS_PER_PROMPT} runs")
    print(f"          = {len(PROMPTS) * len(MODELS) * RUNS_PER_PROMPT} total API calls")
    print("=" * 70)

    # check keys
    for name, key in [("OPENAI_API_KEY", OPENAI_KEY),
                      ("ANTHROPIC_API_KEY", ANTHROPIC_KEY),
                      ("GOOGLE_API_KEY", GOOGLE_KEY)]:
        if not key:
            print(f"ERROR: missing {name} in .env"); sys.exit(1)

    rows = []
    call_idx = 0
    total_calls = len(PROMPTS) * len(MODELS) * RUNS_PER_PROMPT

    for prompt in PROMPTS:
        for model_key, model_info in MODELS.items():
            for run_idx in range(RUNS_PER_PROMPT):
                call_idx += 1
                print(f"  [{call_idx:3d}/{total_calls}] {prompt['id']:18s} | {model_key:10s} | run {run_idx+1}", end=" ", flush=True)
                try:
                    raw = CALLERS[model_key](prompt["text"])
                    brands_found = detect_brands(raw)
                    print(f"-> {len(brands_found)} brands")
                except Exception as e:
                    print(f"-> FAILED: {type(e).__name__}: {e}")
                    raw = ""
                    brands_found = []

                rows.append({
                    "timestamp": datetime.now().isoformat(timespec='seconds'),
                    "prompt_id": prompt["id"],
                    "cep": prompt["cep"],
                    "model": model_key,
                    "model_version": model_info["model"],
                    "temperature": TEMPERATURE,
                    "run_idx": run_idx + 1,
                    "brands_found": "|".join(brands_found),
                    "n_brands": len(brands_found),
                    "raw_response": raw.replace("\n", " ").replace("\t", " "),
                })

    # save CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = f"results_{timestamp}.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print()
    print("=" * 70)
    print(f"Done. Saved {len(rows)} rows to {out_path}")
    print("=" * 70)


if __name__ == "__main__":
    main()
