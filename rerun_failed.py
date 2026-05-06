"""
AIAS — Failed-call recovery script.

Re-runs every cell with call_status != 'ok' from a source CSV. Provider-agnostic
(retries Google, Anthropic, OpenAI, xAI failures uniformly). Category-aware
via the new --category-loading path (uses load_category_files from
run_aias_v2 to resolve the prompt set).

Usage:
  python rerun_failed.py --input data/knives/results_v2_knives_<ts>.csv --category knives
  python rerun_failed.py --input <path> --category <cat> --provider google     # filter to one provider (legacy mode)
  python rerun_failed.py --input <path> --category <cat> --sleep 0             # disable inter-call pacing

Output filename mirrors the v0.7 convention:
  results_v2_<cat>_<orig_ts>_rerun_<new_ts>.csv

Methodologically parallel to v0.7 BBB recovery (protocol §11 v0.7 entry,
§4.3 retry handling). Re-runs are flagged in the output filename and have
their own timestamp; merging into the canonical dataset is a separate step.
"""
import os, sys, csv, time, argparse
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from retry_helper import retry_call
from run_aias_v2 import MODELS, CALLERS, load_category_files

load_dotenv()


def main():
    parser = argparse.ArgumentParser(
        description="Failed-call recovery — re-runs non-ok cells from a source CSV.",
        epilog="Example: python rerun_failed.py --input data/knives/results_v2_knives_<ts>.csv --category knives"
    )
    parser.add_argument("--input", required=True,
                        help="Source CSV with cells to retry (typically a results_v2_*.csv from a prior run)")
    parser.add_argument("--category", required=True,
                        help="Category short name (must match registries/brands_<cat>.json)")
    parser.add_argument("--provider", default=None,
                        help="Optional: filter retries to one provider (anthropic|openai|google|xai). "
                             "Default: retry all failed cells regardless of provider.")
    parser.add_argument("--sleep", type=float, default=1.5,
                        help="Seconds to sleep between calls (default 1.5; set to 0 to disable)")
    parser.add_argument("--output-dir", default=None,
                        help="Override output dir (default: same dir as --input)")
    args = parser.parse_args()

    source_path = Path(args.input)
    if not source_path.exists():
        sys.exit(f"ERROR: source CSV not found: {source_path}")

    output_dir = Path(args.output_dir) if args.output_dir else source_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load the category's prompt set (we need prompt text + cep for the failed cells)
    _, prompts_list, _, _ = load_category_files(args.category)
    prompts_by_id = {p["id"]: p for p in prompts_list}

    # Read source
    with open(source_path) as f:
        original_rows = list(csv.DictReader(f))

    # Filter to non-ok cells, optionally narrow to one provider
    failed = [r for r in original_rows if r["call_status"] != "ok"]
    if args.provider:
        failed = [r for r in failed if r["provider"] == args.provider]

    print("=" * 78)
    print("AIAS Failed-Call Recovery")
    print(f"Source:   {source_path}")
    print(f"Category: {args.category}")
    print(f"Filter:   {'provider=' + args.provider if args.provider else 'all providers'}")
    print(f"Total rows in source: {len(original_rows)}")
    print(f"Cells to retry:       {len(failed)}")
    print(f"Started:  {datetime.now().isoformat(timespec='seconds')}")
    print("=" * 78)

    if not failed:
        print("No failed cells to retry. Exiting.")
        return

    # ----- API key checks -----
    needed_providers = {r["provider"] for r in failed}
    key_map = {
        "anthropic": "ANTHROPIC_API_KEY",
        "openai":    "OPENAI_API_KEY",
        "google":    "GOOGLE_API_KEY",
        "xai":       "XAI_API_KEY",
    }
    for prov in needed_providers:
        env_name = key_map.get(prov)
        if env_name and not os.getenv(env_name):
            sys.exit(f"ERROR: missing {env_name} (needed for provider={prov})")

    rows = []
    status_counts = {"ok": 0, "rate_limit_final": 0, "transient_final": 0, "hard_error": 0}

    for idx, failed_row in enumerate(failed, 1):
        slot = failed_row["model_slot"]
        prompt_id = failed_row["prompt_id"]
        run_idx = int(failed_row["run_idx"])

        info = MODELS.get(slot)
        if not info:
            print(f"  [{idx:3d}/{len(failed)}] SKIP unknown slot: {slot}")
            continue

        prompt = prompts_by_id.get(prompt_id)
        if not prompt:
            print(f"  [{idx:3d}/{len(failed)}] SKIP unknown prompt: {prompt_id}")
            continue

        provider = info["provider"]
        model_string = info["model"]
        use_temp = info.get("supports_temperature", True)

        t0 = time.time()
        print(f"  [{idx:3d}/{len(failed)}] {prompt_id:18s} | {slot:20s} | run {run_idx}", end=" ", flush=True)

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

        rows.append({
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "category": args.category,
            "methodology_version": failed_row["methodology_version"],
            "prompt_set_version": failed_row["prompt_set_version"],
            "brand_registry_version": failed_row["brand_registry_version"],
            "prompt_id": prompt_id,
            "cep": prompt["cep"],
            "model_slot": slot,
            "provider": provider,
            "model_version": model_string,
            "temperature": failed_row["temperature"],
            "run_idx": run_idx,
            "call_status": status,
            "attempts": attempts,
            "elapsed_sec": round(elapsed, 2),
            "raw_response": raw.replace("\n", " ").replace("\t", " ") if raw else "",
        })

        if args.sleep > 0:
            time.sleep(args.sleep)

    # ----- Write recovery CSV -----
    new_ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    suffix = f"_rerun_{args.provider}" if args.provider else "_rerun"
    out_path = output_dir / source_path.name.replace(".csv", f"{suffix}_{new_ts}.csv")
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
    print()
    print("Next: merge the recovery rows into the source dataset before extraction.")
    print(f"  Original: {source_path}")
    print(f"  Recovery: {out_path}")
    print("  See merge step in your post-collection pipeline.")
    print("=" * 78)


if __name__ == "__main__":
    main()
