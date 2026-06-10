#!/usr/bin/env python3
"""
v34_provenance.py — provenance SIDECAR for v0.34 t2 re-acquisition.

Logging only. Tees the provider-returned model id per call to
osf/v34/data/v34_provenance.csv. Does NOT touch any runner's output schema. Used by
run_acquisition_v34.py, which wraps the SDK call boundary (not runner internals) so
the five t1 runners stay byte-identical (probe text / frame ordering / output schema
unchanged; checksums preserved).

Sidecar columns: substrate, phase, call_index, alias, returned_model_id, timestamp.
"""
import csv
import threading
from pathlib import Path
from datetime import datetime, timezone

SIDECAR = Path.home() / "aias" / "osf" / "v34" / "data" / "v34_provenance.csv"
FIELDS = ["substrate", "phase", "call_index", "alias", "returned_model_id", "timestamp"]

_LOCK = threading.Lock()
_COUNTER = {}

# set by the orchestrator before invoking each runner phase
CURRENT = {"substrate": "?", "phase": "?"}


def set_context(substrate: str, phase: str) -> None:
    CURRENT["substrate"] = substrate
    CURRENT["phase"] = phase


def record(alias: str, returned_model_id) -> None:
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
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
