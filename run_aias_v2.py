"""
AIAS — Measurement Engine v2
Adds: retry logic, rate-limit handling, methodology version metadata, robust error reporting.

Phase 2 refactor (May 2026):
  - --category <name> CLI arg required
  - Reads registries/brands_<cat>.json and prompts/prompts_<cat>.json
  - Output lands in data/<cat>/results_v2_<cat>_<timestamp>.csv
  - Stamps category into every CSV row for cross-run analysis
  - Auto-derives PROMPT_SET_VERSION and BRAND_REGISTRY_VERSION from JSON metadata when present

6-model lineup, slot-keyed MODELS dict.
4 providers: anthropic, openai, google, xai.
"""
import os, sys, json, csv, time, argparse
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from retry_helper import retry_call

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_KEY = os.getenv("GOOGLE_API_KEY")
XAI_KEY = os.getenv("XAI_API_KEY")

# ----- METHODOLOGY METADATA -----
METHODOLOGY_VERSION = "0.4"
RUNS_PER_PROMPT = 8
TEMPERATURE = 0.7
# PROMPT_SET_VERSION and BRAND_REGISTRY_VERSION are derived per-category at runtime
# from the registry/prompts JSON metadata; see load_category_files().

# Slot-keyed: each slot is a distinct (provider, model) pair.
# supports_temperature=False for reasoning models (Opus 4.7, gpt-5.5) where
# temperature is deprecated/unsupported by the provider.
MODELS = {
    "anthropic_sonnet": {"provider": "anthropic", "label": "Anthropic claude-sonnet-4-6", "model": "claude-sonnet-4-6", "supports_temperature": True},
    "anthropic_opus":   {"provider": "anthropic", "label": "Anthropic claude-opus-4-7",   "model": "claude-opus-4-7",   "supports_temperature": False},
    "openai_mini":      {"provider": "openai",    "label": "OpenAI gpt-5.4-mini",         "model": "gpt-5.4-mini",      "supports_temperature": True},
    "openai_flagship":  {"provider": "openai",    "label": "OpenAI gpt-5.5",              "model": "gpt-5.5",           "supports_temperature": False},
    "google_flash":     {"provider": "google",    "label": "Google gemini-2.5-flash",     "model": "gemini-2.5-flash",  "supports_temperature": True},
    "xai_grok":         {"provider": "xai",       "label": "xAI grok-4-1-fast",           "model": "grok-4-1-fast",     "supports_temperature": True},
}


def load_category_files(category):
    """Load brands and prompts for a category. Tolerates v0.6 bare-list and v1.1 wrapper schemas.

    Returns: (brands_list, prompts_list, registry_version, prompt_set_version)
    Errors and exits if either file is missing.
    """
    registry_path = Path("registries") / f"brands_{category}.json"
    prompts_path = Path("prompts") / f"prompts_{category}.json"

    if not registry_path.exists():
        sys.exit(f"ERROR: registry file not found: {registry_path}\n"
                 f"       expected per-category file at this path. "
                 f"Available registries: {sorted(p.name for p in Path('registries').glob('brands_*.json'))}")
    if not prompts_path.exists():
        sys.exit(f"ERROR: prompts file not found: {prompts_path}")

    with open(registry_path) as f:
        registry_raw = json.load(f)
    with open(prompts_path) as f:
        prompts_raw = json.load(f)

    # Schema tolerance: bare list (v0.6) or wrapper dict (v1.1+)
    brands = registry_raw if isinstance(registry_raw, list) else registry_raw["brands"]
    prompts = prompts_raw if isinstance(prompts_raw, list) else prompts_raw["prompts"]

    # Version metadata: from wrapper if present, else fallback to <category>_v1.0
    registry_version = (
        registry_raw.get("registry_version") if isinstance(registry_raw, dict) else None
    ) or f"{category}_v1.0"
    prompt_set_version = (
        prompts_raw.get("prompt_set_version") if isinstance(prompts_raw, dict) else None
    ) or f"{category}_v1.0"

    return brands, prompts, registry_version, prompt_set_version


def call_openai(prompt_text, model_string, use_temperature=True):
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_KEY)
    kwargs = {
        "model": model_string,
        "messages": [{"role": "user", "content": prompt_text}],
    }
    if use_temperature:
        kwargs["temperature"] = TEMPERATURE
    r = client.chat.completions.create(**kwargs)
    return r.choices[0].message.content


def call_anthropic(prompt_text, model_string, use_temperature=True):
    import anthropic
    client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
    kwargs = {
        "model": model_string,
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": prompt_text}],
    }
    if use_temperature:
        kwargs["temperature"] = TEMPERATURE
    m = client.messages.create(**kwargs)
    return m.content[0].text


def call_google(prompt_text, model_string, use_temperature=True):
    from google import genai
    from google.genai import types
    client = genai.Client(api_key=GOOGLE_KEY)
    config = types.GenerateContentConfig(temperature=TEMPERATURE) if use_temperature else None
    r = client.models.generate_content(
        model=model_string,
        contents=prompt_text,
        config=config,
    )
    return r.text


def call_xai(prompt_text, model_string, use_temperature=True):
    from openai import OpenAI
    client = OpenAI(api_key=XAI_KEY, base_url="https://api.x.ai/v1")
    kwargs = {
        "model": model_string,
        "messages": [{"role": "user", "content": prompt_text}],
    }
    if use_temperature:
        kwargs["temperature"] = TEMPERATURE
    r = client.chat.completions.create(**kwargs)
    return r.choices[0].message.content


CALLERS = {
    "openai": call_openai,
    "anthropic": call_anthropic,
    "google": call_google,
    "xai": call_xai,
}


def main():
    parser = argparse.ArgumentParser(
        description="AIAS measurement runner — per-category brands/prompts loading.",
        epilog="Example: python run_aias_v2.py --category knives"
    )
    parser.add_argument("--category", required=True,
                        help="Category short name. Reads registries/brands_<cat>.json and prompts/prompts_<cat>.json. "
                             "Output goes to data/<cat>/.")
    parser.add_argument("--missing-cells-file", default=None,
                        help="Optional CSV with columns prompt_id,model_slot,run_idx — "
                             "if provided, only fire these specific cells (surgical resume).")
    parser.add_argument("--output-dir", default=None,
                        help="Override output directory (default: data/<category>/)")
    args = parser.parse_args()

    category = args.category
    BRANDS, PROMPTS, BRAND_REGISTRY_VERSION, PROMPT_SET_VERSION = load_category_files(category)

    output_dir = Path(args.output_dir) if args.output_dir else Path("data") / category
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 78)
    print(f"AIAS Measurement Run v{METHODOLOGY_VERSION}")
    print(f"Category: {category}")
    print(f"Started:  {datetime.now().isoformat(timespec='seconds')}")
    print(f"Plan:     {len(PROMPTS)} prompts x {len(MODELS)} models x {RUNS_PER_PROMPT} runs = {len(PROMPTS)*len(MODELS)*RUNS_PER_PROMPT} calls")
    print(f"Methodology: prompts={PROMPT_SET_VERSION}, registry={BRAND_REGISTRY_VERSION}, temp={TEMPERATURE}")
    print(f"Registry: {len(BRANDS)} brands")
    print(f"Output:   {output_dir}/")
    print(f"Models:")
    for slot, info in MODELS.items():
        temp_note = "" if info["supports_temperature"] else " (no temp)"
        print(f"  - {slot:18s} -> {info['label']}{temp_note}")
    print("=" * 78)

    for name, key in [("OPENAI_API_KEY", OPENAI_KEY), ("ANTHROPIC_API_KEY", ANTHROPIC_KEY), ("GOOGLE_API_KEY", GOOGLE_KEY), ("XAI_API_KEY", XAI_KEY)]:
        if not key:
            print(f"ERROR: missing {name}"); sys.exit(1)

    # MISSING_CELLS_FILTER_ENABLED — optional surgical resumption filter
    cells_filter = None
    if args.missing_cells_file:
        import csv as _csv_filter
        cells_filter = set()
        with open(args.missing_cells_file) as _f:
            for _r in _csv_filter.DictReader(_f):
                cells_filter.add((_r["prompt_id"], _r["model_slot"], int(_r["run_idx"])))
        print(f"Missing-cells filter loaded: {len(cells_filter)} cells to fire "
              f"(from {args.missing_cells_file})")

    # INCREMENTAL_WRITE_ENABLED — CSV is opened here and written row-by-row
    # inside the inner loop, so a mid-run crash preserves all rows up to the
    # crash point. The end-of-run "save rows" block is replaced with a close.
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = output_dir / f"results_v2_{category}_{timestamp}.csv"
    CSV_FIELDS = [
        "timestamp", "category", "methodology_version", "prompt_set_version",
        "brand_registry_version", "prompt_id", "cep", "model_slot", "provider",
        "model_version", "temperature", "run_idx", "call_status", "attempts",
        "elapsed_sec", "raw_response",
    ]
    csv_file = open(out_path, "w", newline="", encoding="utf-8")
    csv_writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDS)
    csv_writer.writeheader()
    csv_file.flush()
    print(f"CSV (incremental): {out_path}")
    rows_written = 0
    call_idx = 0
    total = (len(cells_filter) if cells_filter is not None
             else len(PROMPTS) * len(MODELS) * RUNS_PER_PROMPT)
    status_counts = {"ok": 0, "rate_limit_final": 0, "transient_final": 0, "hard_error": 0}

    for prompt in PROMPTS:
        for slot, info in MODELS.items():
            provider = info["provider"]
            model_string = info["model"]
            use_temp = info.get("supports_temperature", True)
            for run_idx in range(RUNS_PER_PROMPT):
                # MISSING_CELLS_FILTER_ENABLED — skip cells not in filter
                if cells_filter is not None:
                    cell_key = (prompt["id"], slot, run_idx + 1)
                    if cell_key not in cells_filter:
                        continue
                call_idx += 1
                t0 = time.time()
                print(f"  [{call_idx:3d}/{total}] {prompt['id']:18s} | {slot:18s} | run {run_idx+1}", end=" ", flush=True)

                result, status, attempts = retry_call(CALLERS[provider], prompt["prompt"], model_string, use_temp)
                elapsed = time.time() - t0
                status_counts[status] = status_counts.get(status, 0) + 1

                if status == "ok":
                    raw = result
                    note = f"OK ({attempts} attempt{'s' if attempts > 1 else ''}, {elapsed:.1f}s)"
                else:
                    raw = ""
                    note = f"FAILED [{status}] after {attempts} attempts ({elapsed:.1f}s)"
                print(f"-> {note}")

                row = {
                    "timestamp": datetime.now().isoformat(timespec='seconds'),
                    "category": category,
                    "methodology_version": METHODOLOGY_VERSION,
                    "prompt_set_version": PROMPT_SET_VERSION,
                    "brand_registry_version": BRAND_REGISTRY_VERSION,
                    "prompt_id": prompt["id"],
                    "cep": prompt["cep"],
                    "model_slot": slot,
                    "provider": provider,
                    "model_version": model_string,
                    "temperature": TEMPERATURE if use_temp else "default",
                    "run_idx": run_idx + 1,
                    "call_status": status,
                    "attempts": attempts,
                    "elapsed_sec": round(elapsed, 2),
                    "raw_response": raw.replace("\n", " ").replace("\t", " ") if raw else "",
                }
                csv_writer.writerow(row)
                csv_file.flush()
                rows_written += 1

    csv_file.close()

    print()
    print("=" * 78)
    print(f"Run complete. Saved {rows_written} rows to {out_path}")
    print(f"  ok:                 {status_counts.get('ok', 0)}")
    print(f"  rate_limit_final:   {status_counts.get('rate_limit_final', 0)}")
    print(f"  transient_final:    {status_counts.get('transient_final', 0)}")
    print(f"  hard_error:         {status_counts.get('hard_error', 0)}")
    print("=" * 78)


if __name__ == "__main__":
    main()
