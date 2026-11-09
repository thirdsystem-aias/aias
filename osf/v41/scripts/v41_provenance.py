#!/usr/bin/env python3
"""
v41_provenance.py — provenance SIDECAR for the v0.41 t3 re-acquisition.

Forked from v34_provenance.py (v0.34, t2). Logging only. Tees, per provider call,
the provider-returned model id plus the finish reason and output-token counts
(including thinking tokens where the SDK reports them) to
osf/v41/data/v41_provenance.csv. It does NOT touch any runner's output schema;
run_acquisition_v41.py wraps the SDK call boundary (not runner internals), so the
five t1 runners stay byte-identical (probe text / frame ordering / output schema
unchanged; checksums preserved).

Change from v34: finish_reason, output_tokens and thinking_tokens columns
(descriptive truncation check, MC_Truncation; t2 did not record them), and the
AIAS root is read from $AIAS_ROOT when set (runs from a git worktree).

Sidecar columns: substrate, phase, call_index, alias, returned_model_id,
finish_reason, output_tokens, thinking_tokens, timestamp.
"""
import csv
import os
import threading
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(os.environ.get("AIAS_ROOT", str(Path.home() / "aias")))
SIDECAR = ROOT / "osf" / "v41" / "data" / "v41_provenance.csv"
FIELDS = ["substrate", "phase", "call_index", "alias", "returned_model_id",
          "finish_reason", "output_tokens", "thinking_tokens", "timestamp"]

_LOCK = threading.Lock()
_COUNTER = {}

# set by the orchestrator before invoking each runner phase
CURRENT = {"substrate": "?", "phase": "?"}


def set_context(substrate: str, phase: str) -> None:
    CURRENT["substrate"] = substrate
    CURRENT["phase"] = phase


def record(alias: str, returned_model_id, finish_reason=None,
           output_tokens=None, thinking_tokens=None) -> None:
    """Append one provenance row. Thread-safe (runners use thread pools)."""
    sub, ph = CURRENT["substrate"], CURRENT["phase"]
    with _LOCK:
        SIDECAR.parent.mkdir(parents=True, exist_ok=True)
        is_new = not SIDECAR.exists()
        key = (sub, ph)
        idx = _COUNTER.get(key, 0) + 1
        _COUNTER[key] = idx
        with open(SIDECAR, "a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS)
            if is_new:
                w.writeheader()
            w.writerow({
                "substrate": sub, "phase": ph, "call_index": idx,
                "alias": alias or "", "returned_model_id": (returned_model_id or ""),
                "finish_reason": "" if finish_reason is None else str(finish_reason),
                "output_tokens": "" if output_tokens is None else output_tokens,
                "thinking_tokens": "" if thinking_tokens is None else thinking_tokens,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
