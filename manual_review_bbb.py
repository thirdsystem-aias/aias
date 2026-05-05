"""
AIAS Phase 2 — Manual Review Script (with checkpointing + retry)
Risks #6 and #7 from the locked design doc.

Reads the enriched CSV, finds every BBB mention, classifies via gpt-5.4-mini:
  1. Valence (live_recommendation / live_with_caveat / status_correction /
     historical_reference / ambiguous)
  2. Entity reference (legacy_brand / corporate_parent / both / unclear)

Writes results to a manual_review CSV with full source quotes for spot-checking.

Robustness:
  - Saves partial results every 10 rows
  - Per-call 60s timeout
  - One retry on transient errors
  - Resumes from existing checkpoint if found
"""
import os
import csv
import glob
import json
import time
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), timeout=60.0)

MODEL = "gpt-5.4-mini"
TEMPERATURE = 0
CHECKPOINT_PATH = "manual_review_bbb_checkpoint.csv"
CHECKPOINT_EVERY = 10

csv_files = sorted(glob.glob("results_enriched_household_v1.0_*.csv"))
INPUT_CSV = csv_files[-1]
print(f"Reading: {INPUT_CSV}")

BBB_ALIASES = [
    "Bed Bath & Beyond", "Bed Bath and Beyond", "BBB", "Bed, Bath & Beyond",
    "Bed Bath Beyond", "bedbathandbeyond.com", "Beyond, Inc.", "Beyond Inc",
]

CLASSIFICATION_TOOL = {
    "type": "function",
    "function": {
        "name": "classify_bbb_mention",
        "description": "Classify how Bed Bath & Beyond (or its rebrand Beyond, Inc.) is mentioned in an AI response.",
        "parameters": {
            "type": "object",
            "properties": {
                "valence": {
                    "type": "string",
                    "enum": [
                        "live_recommendation",
                        "live_with_caveat",
                        "status_correction",
                        "historical_reference",
                        "ambiguous",
                    ],
                    "description": (
                        "How the AI presents BBB:\n"
                        "- live_recommendation: presents BBB as a currently-operating retailer to use, no caveats about closure or rebrand.\n"
                        "- live_with_caveat: recommends BBB but acknowledges its physical stores closed or it now operates as Beyond, Inc.\n"
                        "- status_correction: explicitly notes BBB is closed/bankrupt/defunct and does NOT recommend it.\n"
                        "- historical_reference: mentions BBB only in past tense as a former retailer, not as a current option.\n"
                        "- ambiguous: cannot determine from context."
                    ),
                },
                "entity_reference": {
                    "type": "string",
                    "enum": ["legacy_brand", "corporate_parent", "both", "unclear"],
                    "description": (
                        "Which entity the mention specifically references:\n"
                        "- legacy_brand: 'Bed Bath & Beyond', 'BBB', 'bedbathandbeyond.com' — the legacy retail brand.\n"
                        "- corporate_parent: 'Beyond, Inc.' or 'Beyond Inc' — the post-2023 corporate entity.\n"
                        "- both: explicitly mentions both names with awareness they are related.\n"
                        "- unclear: cannot tell from the quote which is being referenced."
                    ),
                },
                "source_quote": {
                    "type": "string",
                    "description": "The exact sentence(s) from the response that mention BBB. Up to ~50 words. Used for human spot-checking.",
                },
            },
            "required": ["valence", "entity_reference", "source_quote"],
        },
    },
}


def classify_mention(response_text, max_retries=1):
    system_prompt = (
        "You are reviewing AI-generated responses about household goods retailers to classify how Bed Bath & Beyond (BBB) is mentioned. "
        "BBB filed for bankruptcy April 2023, liquidated all physical stores, and was acquired by Overstock which rebranded as 'Beyond, Inc.' "
        "and relaunched bedbathandbeyond.com as an online-only entity. "
        "Your job: read the response, find where BBB or 'Beyond, Inc.' is mentioned, and classify (a) what the AI says about it (valence) and "
        "(b) which entity name is referenced. Quote the exact source sentence."
    )
    last_exc = None
    for attempt in range(max_retries + 1):
        try:
            completion = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": response_text},
                ],
                tools=[CLASSIFICATION_TOOL],
                tool_choice={"type": "function", "function": {"name": "classify_bbb_mention"}},
                temperature=TEMPERATURE,
            )
            tool_call = completion.choices[0].message.tool_calls[0]
            args = json.loads(tool_call.function.arguments)
            return args
        except Exception as e:
            last_exc = e
            if attempt < max_retries:
                time.sleep(3)
    raise last_exc


def save_checkpoint(rows, path):
    if not rows:
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def load_checkpoint(path):
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    print("=" * 78)
    print("Manual review: BBB valence + entity-reference classification")
    print(f"Model: {MODEL} (temperature {TEMPERATURE})")
    print(f"Checkpoint: {CHECKPOINT_PATH} (saves every {CHECKPOINT_EVERY} rows)")
    print("=" * 78)

    with open(INPUT_CSV, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    bbb_rows = []
    for row in rows:
        if not row.get("raw_response", "").strip():
            continue
        canonicals = row.get("brands_canonical", "")
        bbb_in_canonical = "Bed Bath & Beyond" in canonicals
        response_lower = row["raw_response"].lower()
        alias_in_response = any(a.lower() in response_lower for a in BBB_ALIASES)
        if bbb_in_canonical or alias_in_response:
            bbb_rows.append(row)

    print(f"Found {len(bbb_rows)} responses mentioning BBB or aliases")

    # Resume from checkpoint if present
    completed = load_checkpoint(CHECKPOINT_PATH)
    completed_keys = set()
    for r in completed:
        key = (r.get("prompt_id", ""), r.get("model_slot", ""), str(r.get("run_idx", "")))
        completed_keys.add(key)

    if completed:
        print(f"Resuming: {len(completed)} rows already classified in checkpoint")
    print()

    review_rows = list(completed)
    valence_counts = {}
    entity_counts = {}
    failures = 0
    for r in completed:
        v = r.get("valence", "")
        e = r.get("entity_reference", "")
        if v:
            valence_counts[v] = valence_counts.get(v, 0) + 1
        if e:
            entity_counts[e] = entity_counts.get(e, 0) + 1

    new_in_session = 0
    for i, row in enumerate(bbb_rows, 1):
        slot = row.get("model_slot", "?")
        prompt_id = row.get("prompt_id", "?")
        run_idx = row.get("run_idx", "?")
        key = (prompt_id, slot, str(run_idx))
        if key in completed_keys:
            continue

        print(f"  [{i:3d}/{len(bbb_rows)}] {prompt_id:18s} | {slot:18s} | run {run_idx}", end=" ", flush=True)
        try:
            result = classify_mention(row["raw_response"])
            valence = result["valence"]
            entity = result["entity_reference"]
            quote = result["source_quote"]
            valence_counts[valence] = valence_counts.get(valence, 0) + 1
            entity_counts[entity] = entity_counts.get(entity, 0) + 1
            print(f"-> {valence:22s} | {entity}")
        except Exception as e:
            print(f"-> FAILED: {type(e).__name__}: {str(e)[:80]}")
            failures += 1
            valence = "ERROR"
            entity = "ERROR"
            quote = ""

        review_rows.append({
            "prompt_id": prompt_id,
            "cep": row.get("cep", ""),
            "model_slot": slot,
            "provider": row.get("provider", ""),
            "model_version": row.get("model_version", ""),
            "run_idx": run_idx,
            "extractor_canonical": "Bed Bath & Beyond" if "Bed Bath & Beyond" in row.get("brands_canonical", "") else "",
            "valence": valence,
            "entity_reference": entity,
            "source_quote": quote,
        })

        new_in_session += 1
        if new_in_session % CHECKPOINT_EVERY == 0:
            save_checkpoint(review_rows, CHECKPOINT_PATH)

    save_checkpoint(review_rows, CHECKPOINT_PATH)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    final_path = f"manual_review_bbb_{timestamp}.csv"
    if review_rows:
        with open(final_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(review_rows[0].keys()))
            writer.writeheader()
            writer.writerows(review_rows)

    print()
    print("=" * 78)
    print(f"Manual review complete. Saved {len(review_rows)} rows to {final_path}")
    print(f"(Checkpoint also at {CHECKPOINT_PATH})")
    print()
    print("VALENCE DISTRIBUTION:")
    for v, n in sorted(valence_counts.items(), key=lambda x: x[1], reverse=True):
        pct = 100 * n / len(review_rows) if review_rows else 0
        print(f"  {v:25s} {n:4d}  ({pct:5.1f}%)")
    print()
    print("ENTITY REFERENCE DISTRIBUTION:")
    for e, n in sorted(entity_counts.items(), key=lambda x: x[1], reverse=True):
        pct = 100 * n / len(review_rows) if review_rows else 0
        print(f"  {e:25s} {n:4d}  ({pct:5.1f}%)")
    if failures:
        print()
        print(f"  WARNING: {failures} classifications failed in this session")
    print("=" * 78)


if __name__ == "__main__":
    main()
