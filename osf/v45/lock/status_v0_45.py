#!/usr/bin/env python3
"""Read-only status of the v0.45 (t5) collection (osf/v45/LOCK_STEPS.md steps 10-11). Adapted from
osf/v42/lock/status_v0_42.py (v0.42 @ 58d1891): module names and paths only. No model call, no write.

Prints: whether an acquire_v*.py --collect process runs; the window deadline; spend from the recorded usage (the same
ledger the guard uses, judge reserve included) and the approvals; per block x model: lines, answered calls, errors and
empties; the Message Batches journal (open batches); for the FIRST Fable batch: statuses, served model IDs, finish
reasons, tokens and cost per answer; calls answered by a served model other than the requested one (MC_Served); and
the last lines of the run log.
--batch-status additionally asks Anthropic for the status of open batches (messages.batches.retrieve: metadata only,
not billed). AIAS_ROOT overrides the repository root.
"""
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(os.environ.get("AIAS_ROOT", str(Path(__file__).resolve().parents[3])))
sys.path.insert(0, str(ROOT / "osf/v45/scripts"))
import acquire_v0_45 as AQ  # noqa: E402
import budget_v0_45 as BG  # noqa: E402

SNAP = re.compile(r"-(\d{4}-\d{2}-\d{2}|\d{8})$")


def served_ok(req, served):
    if not served:
        return True
    s = served[len("models/"):] if served.startswith("models/") else served
    return s == req or (s.startswith(req) and bool(SNAP.fullmatch(s[len(req):])))


def main():
    procs = [(p, c) for p, (pp, c) in AQ.process_table().items() if AQ.PAID_COLLECTION.search(c) and p != os.getpid()]
    print("collection processes:", procs or "none")
    lines = [json.loads(l) for l in AQ.RAW_PATH.read_text().splitlines() if l.strip()] if AQ.RAW_PATH.exists() else []
    print(f"raw lines: {len(lines)}; calls answered: {len(AQ.done_ids())} of {AQ.EXPECTED_TOTAL}")
    if lines:
        print("window: no new request after", AQ.collection_deadline(AQ.RAW_PATH).isoformat())
    L = BG.Ledger(AQ.RAW_PATH, AQ.STATE_PATH)
    print("budget:", L.summary())
    print("approvals:", json.dumps(L.state().get("approvals") or {}))
    by = defaultdict(Counter)
    for r in lines:
        by[(AQ.BLOCKS.index((r["phase"], r["condition"], r["run"])) + 1, r["model_requested"])][r["status"]] += 1
    done = AQ.done_ids()
    for (b, m), c in sorted(by.items()):
        ans = sum(1 for r in {x["call_id"] for x in lines if x["model_requested"] == m
                              and AQ.BLOCKS.index((x["phase"], x["condition"], x["run"])) + 1 == b} if r in done)
        print(f"  block {b} {AQ.BLOCKS[b - 1]} {m:17s} lines {sum(c.values()):4d} answered {ans:4d} {dict(c)}")
    jr = [json.loads(l) for l in AQ.BATCH_LOG.read_text().splitlines()] if AQ.BATCH_LOG.exists() else []
    created = [e for e in jr if e["event"] == "created"]
    print(f"batches created: {len(created)}; open (in flight or left by a stopped run): "
          f"{[e['batch_id'] for e in AQ.open_batches(AQ.BATCH_LOG)]}")
    if created:
        first = created[0]["batch_id"]
        fl = [r for r in lines if r.get("batch_id") == first]
        print(f"FIRST batch {first} (created {created[0]['utc']}, {len(created[0]['requests'])} requests): "
              f"{len(fl)} lines; status {dict(Counter(r['status'] for r in fl))}; "
              f"served {dict(Counter(r['served_model'] for r in fl))}; finish {dict(Counter(r['finish_reason'] for r in fl))}")
        if fl:
            n = len(fl)
            print(f"  mean tokens in/out {sum(r['input_tokens'] or 0 for r in fl) / n:.0f}/"
                  f"{sum(r['output_tokens'] or 0 for r in fl) / n:.0f}; cost ${sum(r['cost_usd'] for r in fl):.4f} "
                  f"(${sum(r['cost_usd'] for r in fl) / n:.4f}/answer); errors {[r['error'] for r in fl if r['error']][:3]}")
    bad = [(r["call_id"], r["served_model"]) for r in lines
           if r["status"] == "ok" and not served_ok(r["model_requested"], r.get("served_model"))]
    print(f"MC_Served: {len(bad)} answered lines served by another model ID {bad[:5]}")
    log = AQ.RAW_PATH.parent / "collect_v0_45.log"
    if log.exists():
        print("log tail:")
        for l in log.read_text(errors="replace").splitlines()[-5:]:
            print("  " + l[:200])
    if "--batch-status" in sys.argv:
        import anthropic
        c = anthropic.Anthropic()
        for e in AQ.open_batches(AQ.BATCH_LOG):
            b = c.messages.batches.retrieve(e["batch_id"])
            print(f"  {b.id}: {b.processing_status} counts {getattr(b, 'request_counts', None)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
