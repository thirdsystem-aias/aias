"""
AIAS — Recovery script (Google-only).
Re-runs the 38 Google failures from the original CSV.
Now on paid tier with proper rate limits.
"""
import os, sys, csv, time, json
from datetime import datetime
from dotenv import load_dotenv
from retry_helper import retry_call
from run_aias_v2 import MODELS, CALLERS, PROMPTS

load_dotenv()

# Source CSV — the original run with failures
SOURCE_CSV = "results_v2_20260504_132404.csv"

# Paid tier — slight pacing for safety, much faster than free tier
SLEEP_BETWEEN_CALLS = 1.5


def main():
    print("=" * 78)
    print(f"AIAS Recovery Run (Google-only, paid tier)")
    print(f"Source: {SOURCE_CSV}")
    print(f"Started: {datetime.now().isoformat(timespec='seconds')}")
    print("=" * 78)

    # Read original
    with open(SOURCE_CSV) as f:
        original_rows = list(csv.DictReader(f))

    # Failures from Google ONLY
    failed = [r for r in original_rows
              if r['call_status'] != 'ok' and r['provider'] == 'google']

    print(f"Total rows in source: {len(original_rows)}")
    print(f"Google failures to retry: {len(failed)}")
    print("=" * 78)

    # Index prompts by id
    prompts_by_id = {p['id']: p for p in PROMPTS}

    rows = []
    status_counts = {"ok": 0, "rate_limit_final": 0, "transient_final": 0, "hard_error": 0}

    for idx, failed_row in enumerate(failed, 1):
        slot = failed_row['model_slot']
        prompt_id = failed_row['prompt_id']
        run_idx = int(failed_row['run_idx'])

        info = MODELS.get(slot)
        if not info:
            print(f"  [{idx:3d}/{len(failed)}] SKIP unknown slot: {slot}")
            continue

        prompt = prompts_by_id.get(prompt_id)
        if not prompt:
            print(f"  [{idx:3d}/{len(failed)}] SKIP unknown prompt: {prompt_id}")
            continue

        provider = info['provider']
        model_string = info['model']
        use_temp = info.get('supports_temperature', True)

        t0 = time.time()
        print(f"  [{idx:3d}/{len(failed)}] {prompt_id:18s} | {slot:20s} | run {run_idx}", end=" ", flush=True)

        result, status, attempts = retry_call(CALLERS[provider], prompt['prompt'], model_string, use_temp)
        elapsed = time.time() - t0
        status_counts[status] = status_counts.get(status, 0) + 1

        if status == "ok":
            raw = result
            note = f"OK ({attempts} attempt{'s' if attempts > 1 else ''}, {elapsed:.1f}s)"
        else:
            raw = ""
            note = f"FAILED [{status}] after {attempts} attempts ({elapsed:.1f}s)"
        print(f"-> {note}")

        rows.append({
            "timestamp": datetime.now().isoformat(timespec='seconds'),
            "methodology_version": failed_row['methodology_version'],
            "prompt_set_version": failed_row['prompt_set_version'],
            "brand_registry_version": failed_row['brand_registry_version'],
            "prompt_id": prompt_id,
            "cep": prompt['cep'],
            "model_slot": slot,
            "provider": provider,
            "model_version": model_string,
            "temperature": failed_row['temperature'],
            "run_idx": run_idx,
            "call_status": status,
            "attempts": attempts,
            "elapsed_sec": round(elapsed, 2),
            "raw_response": raw.replace("\n", " ").replace("\t", " ") if raw else "",
        })

        time.sleep(SLEEP_BETWEEN_CALLS)

    # Write recovery CSV
    out_path = SOURCE_CSV.replace(".csv", "_rerun_google.csv")
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print()
    print("=" * 78)
    print(f"Recovery complete. Saved {len(rows)} rows to {out_path}")
    print(f"  ok:                 {status_counts.get('ok', 0)}")
    print(f"  rate_limit_final:   {status_counts.get('rate_limit_final', 0)}")
    print(f"  transient_final:    {status_counts.get('transient_final', 0)}")
    print(f"  hard_error:         {status_counts.get('hard_error', 0)}")
    print("=" * 78)


if __name__ == "__main__":
    main()