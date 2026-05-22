"""
run_v0_19.py — AIAS v0.19 Acquisition Runner

Reads pre-generated query batches and dispatches them through the canonical
six-slot reference panel via the shared protocol/providers.py module.
Writes raw responses to JSONL in the schema expected by acquire_v0_19.py
parse-phase-a / parse-phase-b.

Usage:
  python3 run_v0_19.py phase-a               # 96 queries  → phase_a_responses.jsonl
  python3 run_v0_19.py phase-b               # 36 queries  → phase_b_responses.jsonl
  python3 run_v0_19.py phase-a --resume      # skip already-completed queries
  python3 run_v0_19.py phase-b --resume

Environment variables (set before running):
  ANTHROPIC_API_KEY
  OPENAI_API_KEY
  GOOGLE_API_KEY

Provider routing:
  claude-*  → call_anthropic
  gpt-*     → call_openai
  gemini-*  → call_google

Pre-registered acquisition runner. Locked at pre-reg commit alongside
acquire_v0_19.py and score_v0_19.py.
"""

import json
import sys
import time
from pathlib import Path

# Add ~/aias to sys.path so protocol.providers resolves cleanly.
# Layout assumption: this file at ~/aias/osf/v19/run_v0_19.py
# resolves AIAS_ROOT = ~/aias/, where protocol/providers.py lives.
SCRIPT_DIR = Path(__file__).parent
AIAS_ROOT  = SCRIPT_DIR.parent.parent
sys.path.insert(0, str(AIAS_ROOT))

try:
    from protocol.providers import call_anthropic, call_openai, call_google
except ImportError as e:
    print(f"ERROR: Failed to import protocol.providers from {AIAS_ROOT}")
    print(f"  {e}")
    print()
    print(f"Expected at: {AIAS_ROOT}/protocol/providers.py")
    print()
    print("Diagnostics:")
    print(f"  - Does ~/aias/protocol/providers.py exist?")
    print(f"  - Are call_anthropic, call_openai, call_google defined and implemented?")
    print(f"  - If providers.py lives elsewhere, update sys.path setup at line 35-37.")
    sys.exit(2)


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

PHASE_A_QUERIES   = SCRIPT_DIR / "phase_a_queries.jsonl"
PHASE_B_QUERIES   = SCRIPT_DIR / "phase_b_queries.jsonl"
PHASE_A_RESPONSES = SCRIPT_DIR / "phase_a_responses.jsonl"
PHASE_B_RESPONSES = SCRIPT_DIR / "phase_b_responses.jsonl"


# ---------------------------------------------------------------------------
# Provider routing
# ---------------------------------------------------------------------------

def route_call(model, prompt):
    """Dispatch to the right provider based on model identifier prefix."""
    if model.startswith("claude"):
        return call_anthropic(model, prompt)
    if model.startswith("gpt"):
        return call_openai(model, prompt)
    if model.startswith("gemini"):
        return call_google(model, prompt)
    raise ValueError(f"Unknown provider for model identifier: {model}")


# ---------------------------------------------------------------------------
# Acquisition loop
# ---------------------------------------------------------------------------

def extract_response_text(resp):
    """
    Handle both ProviderResponse dict (per v0.18 protocol/providers.py
    contract) and bare-string returns. Returns (text, tokens_in, tokens_out,
    latency_ms) with None for fields not present.
    """
    if isinstance(resp, dict):
        return (
            resp.get("raw_response", ""),
            resp.get("tokens_in"),
            resp.get("tokens_out"),
            resp.get("latency_ms"),
        )
    return (str(resp), None, None, None)


def run_phase(input_path, output_path, phase_label, resume=False):
    """Run acquisition for one phase. Streams responses to disk."""
    if not input_path.exists():
        print(f"ERROR: Query batch not found at {input_path}")
        print(f"Run `python3 acquire_v0_19.py gen-{phase_label.lower()}` first.")
        sys.exit(1)

    # Load already-completed query_ids if resuming
    completed = set()
    if resume and output_path.exists():
        with open(output_path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                    if r.get("response") is not None:
                        completed.add(r["query_id"])
                except json.JSONDecodeError:
                    continue
        print(f"Resume: {len(completed)} queries already completed.")

    # Load query batch
    queries = []
    with open(input_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            queries.append(json.loads(line))

    total = len(queries)
    print(f"Phase {phase_label}: {total} queries in batch ({total - len(completed)} pending).")
    print(f"Output: {output_path}")
    print("-" * 70)

    # Open output in append mode if resuming, write mode otherwise
    file_mode = "a" if resume else "w"
    errors = 0
    successes = 0

    with open(output_path, file_mode) as out:
        for i, q in enumerate(queries, 1):
            qid = q["query_id"]
            if qid in completed:
                continue

            model = q["panel_model"]
            prompt = q.get("probe") or q.get("prompt")

            try:
                t0 = time.time()
                raw = route_call(model, prompt)
                elapsed_ms = int((time.time() - t0) * 1000)

                text, tin, tout, prov_latency = extract_response_text(raw)
                latency = prov_latency if prov_latency is not None else elapsed_ms

                record = {
                    "query_id": qid,
                    "phase": q["phase"],
                    "panel_model": model,
                    "response": text,
                    "tokens_in": tin,
                    "tokens_out": tout,
                    "latency_ms": latency,
                }
                if "brand" in q:
                    record["brand"] = q["brand"]
                if "frame" in q:
                    record["frame"] = q["frame"]

                out.write(json.dumps(record) + "\n")
                out.flush()
                successes += 1
                preview = text[:60].replace("\n", " ") if text else ""
                print(f"  [{i:>3}/{total}] ✓ {qid:<60} {latency:>5}ms  {preview!r}")

            except Exception as e:
                errors += 1
                err = {
                    "query_id": qid,
                    "phase": q["phase"],
                    "panel_model": model,
                    "response": None,
                    "error": f"{type(e).__name__}: {e}",
                }
                if "brand" in q:
                    err["brand"] = q["brand"]
                if "frame" in q:
                    err["frame"] = q["frame"]
                out.write(json.dumps(err) + "\n")
                out.flush()
                print(f"  [{i:>3}/{total}] ✗ {qid:<60} {type(e).__name__}: {e}")

    print("-" * 70)
    print(f"Phase {phase_label} acquisition complete.")
    print(f"  Successes: {successes}")
    print(f"  Errors:    {errors}")
    print(f"  Output:    {output_path}")
    if errors:
        print()
        print(f"Re-run with --resume to retry the {errors} failed queries.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

USAGE = """\
Usage:
  python3 run_v0_19.py phase-a [--resume]
  python3 run_v0_19.py phase-b [--resume]
"""


def main():
    if len(sys.argv) < 2:
        print(USAGE)
        sys.exit(1)

    op = sys.argv[1]
    resume = "--resume" in sys.argv[2:]

    if op == "phase-a":
        run_phase(PHASE_A_QUERIES, PHASE_A_RESPONSES, "A", resume=resume)
    elif op == "phase-b":
        run_phase(PHASE_B_QUERIES, PHASE_B_RESPONSES, "B", resume=resume)
    else:
        print(USAGE)
        sys.exit(1)


if __name__ == "__main__":
    main()
