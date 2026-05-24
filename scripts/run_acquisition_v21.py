#!/usr/bin/env python3
"""
run_acquisition_v21.py — AIAS v0.21 acquisition runner (v2 — fail-fast auth).

Executes Phase A (Recognition) and Phase B (six-frame Recall) against the
locked six-slot reference panel per pre-registration v0.21-prereg-r1.

Phase A: Recognition probes (brands × 6 models) with the locked C_P probe template.
Phase B: 36 queries (6 frames × 6 models), raw responses preserved.

v2 changes:
  - Detects auth/credential errors across providers and fails immediately
    (no retry loop, no 30s of wasted backoff on bad keys).
  - Retains exponential backoff for transient/rate-limit errors.
  - Clear error message points to check_llm_keys.py when auth fails.
  - Cancels pending futures in the threadpool on first auth failure so the
    run aborts cleanly instead of churning through 143 doomed retries.

Required env vars:
    ANTHROPIC_API_KEY  for Claude models
    OPENAI_API_KEY     for GPT models
    GOOGLE_API_KEY     (or GEMINI_API_KEY) for Gemini models

Required pip packages:
    anthropic, openai, google-generativeai

Usage:
    python run_acquisition_v21.py                          # both phases
    python run_acquisition_v21.py --phase a                # Phase A only
    python run_acquisition_v21.py --phase b                # Phase B only
    python run_acquisition_v21.py --dry-run                # no API calls
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

# --- Configuration -----------------------------------------------------------

DEFAULT_REGISTRY = Path.home() / "aias" / "prereg" / "v0_21_registry.json"
DEFAULT_OUTPUT_DIR = Path.home() / "aias" / "osf" / "v21"

PROVIDER_BY_MODEL = {
    "claude-opus-4-5":      "anthropic",
    "claude-sonnet-4-5":    "anthropic",
    "gpt-4o":               "openai",
    "gpt-4o-mini":          "openai",
    "gemini-2.5-flash":     "google",
    "gemini-2.5-flash-lite": "google",
}


# --- Auth/credential error detection (NEW IN v2) ----------------------------

class AuthErrorFatal(Exception):
    """Auth/credential failure — must not be retried, must abort the run."""
    pass


def _is_auth_error(e: Exception) -> bool:
    msg = str(e).lower()
    type_name = type(e).__name__.lower()
    if "authentication" in type_name or "permission" in type_name:
        return True
    markers = [
        "invalid x-api-key", "invalid api key", "api key not valid",
        "api_key_invalid", "incorrect api key", "authentication_error",
        "unauthorized", "401", "403 forbidden",
    ]
    return any(m in msg for m in markers)


def _is_rate_limit(e: Exception) -> bool:
    msg = str(e).lower()
    type_name = type(e).__name__.lower()
    if "ratelimit" in type_name or "rate_limit" in type_name:
        return True
    return any(m in msg for m in [
        "rate limit", "rate-limit", "429", "quota exceeded", "too many requests",
    ])


# --- LLM client adapters (lazy-imported) -------------------------------------

_anthropic_client = None
_openai_client = None
_google_models = {}


def _get_anthropic():
    global _anthropic_client
    if _anthropic_client is None:
        try:
            from anthropic import Anthropic
        except ImportError:
            sys.exit("ERROR: anthropic package not installed. Run: python -m pip install anthropic")
        _anthropic_client = Anthropic()
    return _anthropic_client


def _get_openai():
    global _openai_client
    if _openai_client is None:
        try:
            from openai import OpenAI
        except ImportError:
            sys.exit("ERROR: openai package not installed. Run: python -m pip install openai")
        _openai_client = OpenAI()
    return _openai_client


def _get_google(model_name: str):
    if model_name not in _google_models:
        try:
            import google.generativeai as genai
        except ImportError:
            sys.exit("ERROR: google-generativeai not installed. Run: python -m pip install google-generativeai")
        key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
        if not key:
            sys.exit("ERROR: GOOGLE_API_KEY (or GEMINI_API_KEY) env var not set")
        genai.configure(api_key=key)
        _google_models[model_name] = genai.GenerativeModel(model_name)
    return _google_models[model_name]


def call_llm(model_name: str, prompt: str,
             max_tokens: int = 1024,
             max_retries: int = 4) -> tuple[str, float]:
    """Call an LLM. Fails fast on auth errors; retries transient errors."""
    provider = PROVIDER_BY_MODEL.get(model_name)
    if not provider:
        raise ValueError(f"Unknown model: {model_name}")

    last_err: Exception | None = None
    for attempt in range(1, max_retries + 1):
        try:
            start = time.time()
            if provider == "anthropic":
                client = _get_anthropic()
                resp = client.messages.create(
                    model=model_name, max_tokens=max_tokens,
                    messages=[{"role": "user", "content": prompt}],
                )
                text = resp.content[0].text if resp.content else ""
            elif provider == "openai":
                client = _get_openai()
                resp = client.chat.completions.create(
                    model=model_name, max_tokens=max_tokens,
                    messages=[{"role": "user", "content": prompt}],
                )
                text = resp.choices[0].message.content or ""
            elif provider == "google":
                model = _get_google(model_name)
                resp = model.generate_content(prompt)
                try:
                    text = resp.text
                except Exception:
                    text = ""
                    if hasattr(resp, "candidates") and resp.candidates:
                        parts = getattr(resp.candidates[0].content, "parts", [])
                        text = "".join(getattr(p, "text", "") for p in parts)
            else:
                raise ValueError(f"Unhandled provider: {provider}")
            return text, time.time() - start
        except Exception as e:
            # FAIL FAST on auth errors — bad keys are not transient
            if _is_auth_error(e):
                raise AuthErrorFatal(
                    f"{model_name} rejected the API key — {type(e).__name__}: {e}"
                ) from e
            last_err = e
            if attempt == max_retries:
                break
            if _is_rate_limit(e):
                sleep = min(5.0 * attempt + 5.0, 60.0)
                kind = "rate-limit"
            else:
                sleep = min(2.0 ** attempt + 0.5, 30.0)
                kind = "transient"
            print(f"    ! {model_name} attempt {attempt} {kind} "
                  f"({type(e).__name__}); sleep {sleep:.1f}s", flush=True)
            time.sleep(sleep)
    raise RuntimeError(f"LLM call failed after {max_retries} attempts: {last_err}") from last_err


# --- Response parsing --------------------------------------------------------

def parse_yes_no(response_text: str) -> str:
    if not response_text:
        return "ambiguous"
    t = response_text.strip().lower()
    while t and t[0] in "*_`#- \"'.,":
        t = t[1:]
    if not t:
        return "ambiguous"
    first_word = t.split()[0].strip(".,!?'\"`*_")
    if first_word == "yes":
        return "yes"
    if first_word == "no":
        return "no"
    first_sentence = t.split(".")[0]
    has_yes = " yes" in (" " + first_sentence) or first_sentence.startswith("yes")
    has_no = " no " in (" " + first_sentence + " ") or first_sentence.startswith("no ")
    if has_yes and not has_no:
        return "yes"
    if has_no and not has_yes:
        return "no"
    return "ambiguous"


# --- Phase A: Recognition ----------------------------------------------------

def run_phase_a(registry: dict, output_path: Path, max_workers: int,
                dry_run: bool) -> None:
    models = registry["reference_panel"]
    probe_template = registry["phase_a_probe_template"]

    tasks = []
    for cell_id, cell in registry["cells"].items():
        for brand in cell["brands"]:
            for model in models:
                tasks.append({
                    "brand": brand["name"], "cell": cell_id,
                    "cascade_order": brand["cascade_order"], "model": model,
                })

    total_brands = sum(len(c["brands"]) for c in registry["cells"].values())
    print(f"\n--- Phase A: Recognition ---")
    print(f"  {len(tasks)} probes ({len(models)} models × {total_brands} brands)")
    print(f"  Probe template: {probe_template!r}")

    if dry_run:
        print(f"  [dry-run] would call {len(tasks)} LLM probes; skipping.")
        return

    rows: list[dict] = []
    auth_failure = False

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        future_to_task = {}
        for task in tasks:
            prompt = probe_template.replace("{BRAND}", task["brand"]).replace("{brand}", task["brand"])
            future = pool.submit(call_llm, task["model"], prompt, 64)
            future_to_task[future] = (task, prompt)

        for i, future in enumerate(as_completed(future_to_task), start=1):
            task, prompt = future_to_task[future]
            try:
                response_text, latency = future.result()
                recognized = parse_yes_no(response_text)
                rows.append({
                    **task, "probe_text": prompt, "response_text": response_text,
                    "recognized": recognized,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "latency_s": f"{latency:.3f}",
                })
                print(f"  [{i:3d}/{len(tasks)}] {task['model']:25s} "
                      f"{task['cell']}.{task['cascade_order']} "
                      f"{task['brand']:32s} → {recognized}", flush=True)
            except AuthErrorFatal as e:
                if not auth_failure:
                    auth_failure = True
                    print(f"\n  ✗ AUTH FAILURE: {e}", flush=True)
                    print(f"\n  Aborting Phase A. Diagnose with:", flush=True)
                    print(f"      python ~/aias/scripts/check_llm_keys.py", flush=True)
                    print(f"      python ~/aias/scripts/setup_llm_keys.py  # if any need refreshing\n", flush=True)
                for f in future_to_task:
                    f.cancel()
            except Exception as e:
                rows.append({**task, "probe_text": prompt,
                             "response_text": f"<ERROR: {type(e).__name__}: {e}>",
                             "recognized": "error",
                             "timestamp": datetime.now(timezone.utc).isoformat(),
                             "latency_s": "0"})
                print(f"  [{i:3d}/{len(tasks)}] ! {task['brand']} on "
                      f"{task['model']}: FAILED ({e})", flush=True)

    if auth_failure:
        sys.exit(1)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["brand", "cell", "cascade_order", "model", "probe_text",
              "response_text", "recognized", "timestamp", "latency_s"]
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        sorted_rows = sorted(rows, key=lambda r: (r["cell"], r["cascade_order"], r["model"]))
        for row in sorted_rows:
            writer.writerow(row)
    print(f"\n  → Phase A results written: {output_path} ({len(rows)} rows)")

    print("\n  Per-brand C_P (Recognition score, 0..6):")
    for cell_id, cell in registry["cells"].items():
        print(f"    Cell {cell_id} ({cell['label']}):")
        for brand in cell["brands"]:
            brand_rows = [r for r in rows if r["brand"] == brand["name"]]
            yes_count = sum(1 for r in brand_rows if r["recognized"] == "yes")
            n = len(brand_rows)
            print(f"      {brand['cascade_order']}. {brand['name']:32s}  C_P = {yes_count}/{n}")


# --- Phase B: Six-frame Recall ----------------------------------------------

def run_phase_b(registry: dict, output_path: Path, max_workers: int,
                dry_run: bool) -> None:
    models = registry["reference_panel"]
    frames = registry["phase_b_frames"]

    tasks = []
    for channel, channel_frames in frames.items():
        for frame_id, frame_text in channel_frames.items():
            for model in models:
                tasks.append({"model": model, "frame_id": frame_id,
                              "channel": channel, "frame_text": frame_text})

    print(f"\n--- Phase B: Six-frame Recall ---")
    print(f"  {len(tasks)} queries ({len(models)} models × 6 frames)")
    print(f"  Channels: R_cat (q1-q3) + R_cult (q4-q6)")

    if dry_run:
        print(f"  [dry-run] would call {len(tasks)} LLM queries; skipping.")
        return

    rows: list[dict] = []
    auth_failure = False

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        future_to_task = {
            pool.submit(call_llm, t["model"], t["frame_text"], 2048): t
            for t in tasks
        }
        for i, future in enumerate(as_completed(future_to_task), start=1):
            task = future_to_task[future]
            try:
                response_text, latency = future.result()
                rows.append({**task, "response_text": response_text,
                             "timestamp": datetime.now(timezone.utc).isoformat(),
                             "latency_s": f"{latency:.3f}"})
                preview = response_text[:80].replace("\n", " ")
                print(f"  [{i:2d}/{len(tasks)}] {task['model']:25s} "
                      f"{task['frame_id']} ({task['channel']:6s}): {preview}...",
                      flush=True)
            except AuthErrorFatal as e:
                if not auth_failure:
                    auth_failure = True
                    print(f"\n  ✗ AUTH FAILURE: {e}", flush=True)
                    print(f"\n  Aborting Phase B. Run check_llm_keys.py to diagnose.\n", flush=True)
                for f in future_to_task:
                    f.cancel()
            except Exception as e:
                rows.append({**task,
                             "response_text": f"<ERROR: {type(e).__name__}: {e}>",
                             "timestamp": datetime.now(timezone.utc).isoformat(),
                             "latency_s": "0"})
                print(f"  [{i:2d}/{len(tasks)}] ! {task['frame_id']} on "
                      f"{task['model']}: FAILED ({e})", flush=True)

    if auth_failure:
        sys.exit(1)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["model", "frame_id", "channel", "frame_text", "response_text",
              "timestamp", "latency_s"]
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        sorted_rows = sorted(rows, key=lambda r: (r["channel"], r["frame_id"], r["model"]))
        for row in sorted_rows:
            writer.writerow(row)
    print(f"\n  → Phase B results written: {output_path} ({len(rows)} responses)")


# --- Main --------------------------------------------------------------------

def check_api_keys(registry: dict) -> list[str]:
    providers_needed = {PROVIDER_BY_MODEL[m] for m in registry["reference_panel"]
                        if m in PROVIDER_BY_MODEL}
    missing = []
    if "anthropic" in providers_needed and "ANTHROPIC_API_KEY" not in os.environ:
        missing.append("ANTHROPIC_API_KEY")
    if "openai" in providers_needed and "OPENAI_API_KEY" not in os.environ:
        missing.append("OPENAI_API_KEY")
    if "google" in providers_needed and \
       "GOOGLE_API_KEY" not in os.environ and "GEMINI_API_KEY" not in os.environ:
        missing.append("GOOGLE_API_KEY (or GEMINI_API_KEY)")
    return missing


def main() -> int:
    parser = argparse.ArgumentParser(
        description="AIAS v0.21 acquisition runner (Phase A + Phase B)"
    )
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--phase", choices=["a", "b", "all"], default="all")
    parser.add_argument("--max-workers", type=int, default=6)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    registry_path = Path(args.registry).expanduser()
    output_dir = Path(args.output_dir).expanduser()

    if not registry_path.exists():
        print(f"ERROR: registry not found at {registry_path}", file=sys.stderr)
        return 2

    with open(registry_path) as f:
        registry = json.load(f)

    print("AIAS v0.21 acquisition runner (v2 — fail-fast auth)")
    print(f"  Registry:    {registry_path}")
    print(f"  Phase:       {registry.get('phase')}")
    print(f"  Substrate:   {registry.get('substrate')}")
    print(f"  Lock state:  {registry.get('lock_state')}")
    print(f"  Panel:       {len(registry.get('reference_panel', []))}-slot")
    total_brands = sum(len(c["brands"]) for c in registry["cells"].values())
    print(f"  Brands:      {total_brands} ({len(registry['cells'])} cells)")
    print(f"  Output:      {output_dir}")

    if registry.get("phase") != "v0.21":
        print(f"WARNING: registry phase is '{registry.get('phase')}', expected 'v0.21'",
              file=sys.stderr)

    missing_keys = check_api_keys(registry)
    if missing_keys and not args.dry_run:
        print(f"\nERROR: missing API keys: {', '.join(missing_keys)}", file=sys.stderr)
        return 2

    if args.dry_run:
        print("\n[DRY-RUN] No API calls will be made.")

    if args.phase in ("a", "all"):
        run_phase_a(registry, output_dir / "phase_a_results.csv",
                    args.max_workers, args.dry_run)

    if args.phase in ("b", "all"):
        run_phase_b(registry, output_dir / "phase_b_results.csv",
                    args.max_workers, args.dry_run)

    if not args.dry_run:
        print("\n✓ Acquisition complete.")
        print(f"\n  Next steps:")
        print(f"    cd ~/aias")
        print(f"    git add osf/v21/phase_a_results.csv osf/v21/phase_b_results.csv")
        print(f"    git commit -m 'acquisition: v0.21 — Phase A + Phase B raw results'")
        print(f"    git tag v0.21-acquisition-locked")
        print(f"    python ~/aias/scripts/score_v21.py")

    return 0


if __name__ == "__main__":
    sys.exit(main())
