#!/usr/bin/env python3
"""Targeted faithful retry of errored v23 t2 raw records (transient network/503).
Re-calls each non-ok record with its STORED prompt (byte-identical) + same model_id +
temperature=0 via the verbatim acquire_v0_23 call functions; merges in place. Provenance
teed (phase=*_retry)."""
import sys, json, time, importlib.util
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, "scripts")
ROOT = Path.home() / "aias"
D = ROOT / "osf/v34/data/v23"
import run_acquisition_v34 as ORCH
import v34_provenance as PROV
ORCH.install_sdk_provenance()
spec = importlib.util.spec_from_file_location("acq23", str(ROOT / "scripts/acquire_v0_23.py"))
m = importlib.util.module_from_spec(spec); sys.modules["acq23"] = m; spec.loader.exec_module(m)


def retry(path, phase_label):
    recs = json.load(open(path))
    PROV.set_context("v23", phase_label + "_retry")
    n = 0
    for r in recs:
        if r.get("status") == "ok" and r.get("response"):
            continue
        call_fn, _ = m.PROVIDER_DISPATCH[r["provider"]]
        r["ts_start"] = datetime.now(timezone.utc).isoformat()
        try:
            r["response"] = call_fn(r["model_id"], r["prompt"])
            r["status"] = "ok"; r["error"] = None
        except Exception as e:
            r["status"] = "error"; r["error"] = str(e)
        r["ts_end"] = datetime.now(timezone.utc).isoformat()
        n += 1
        time.sleep(0.5)
    json.dump(recs, open(path, "w"), ensure_ascii=False, indent=2)
    remaining = sum(1 for r in recs if r.get("status") != "ok" or not r.get("response"))
    print(f"{path.name}: retried {n}, remaining errors {remaining}")
    return remaining


if __name__ == "__main__":
    ra = retry(D / "v23_phase_a_raw.json", "A")
    rb = retry(D / "v23_phase_b_raw.json", "B")
    print(f"DONE v23 retry; remaining A={ra} B={rb}")
