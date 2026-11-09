#!/usr/bin/env python3
"""
make_synthetic_t3.py — synthetic t3 waves for testing score_v41.py before the lock.

Builds a folder in the osf/v41/data/ layout (each runner's real output schema) from
frozen t1/t2 files. No API call; nothing is written inside the repo unless you point
OUT there (don't).

Scenarios
  copy_t2        t3 = t2 byte copy                 (known answers: rho(t2,t3) = 1)
  copy_t1        t3 = t1 byte copy                 (rho(t2,t3) = rho(t1,t2); D < 0)
  shuffle_models t3 = t2 with model labels permuted within each frame
                 (pi_hat preserved exactly; per-model counts, so phi, scrambled)
  drop_model     copy_t2 without one model anywhere (unavailable alias)
  partial_fail   copy_t2 with one Phase B response of one model blanked
  snapshot_drift copy_t2 with a different served id for gpt-4o in the sidecar

Usage: AIAS_ROOT=<tree> python3 make_synthetic_t3.py <scenario> <OUT> [--seed N]
"""
import argparse
import csv
import json
import os
import random
import shutil
import sys
from pathlib import Path

ROOT = Path(os.environ.get("AIAS_ROOT", str(Path.home() / "aias")))
OSF = ROOT / "osf"
T2 = OSF / "v34/data"
SUBS = ["v19", "v20", "v21", "v22", "v23"]
PANEL = ["claude-opus-4-5", "claude-sonnet-4-5", "gpt-4o", "gpt-4o-mini",
         "gemini-2.5-flash", "gemini-2.5-flash-lite"]
V19_FILES = ["phase_a_responses.jsonl", "phase_b_responses.jsonl", "phase_a_results.csv", "phase_b_results.csv"]
RAW_FILES = ["phase_a_results.csv", "phase_b_results.csv"]
V23_FILES = ["v23_phase_a_raw.json", "v23_phase_b_raw.json", "v23_phase_a_scored.json", "v23_phase_b_scored.json"]


def src_dir(wave, sub):
    if wave == "t2":
        return T2 / sub
    return OSF / ("v23/data" if sub == "v23" else sub)


def copy_wave(wave, out):
    for sub in SUBS:
        d = out / sub
        d.mkdir(parents=True, exist_ok=True)
        files = V19_FILES if sub == "v19" else V23_FILES if sub == "v23" else RAW_FILES
        for f in files:
            shutil.copyfile(src_dir(wave, sub) / f, d / f)


def sidecar(out, override=None):
    """t3 sidecar synthesized from the t2 record (adds the v41 columns)."""
    rows = list(csv.DictReader(open(T2 / "v34_provenance.csv", newline="")))
    fields = ["substrate", "phase", "call_index", "alias", "returned_model_id",
              "finish_reason", "output_tokens", "thinking_tokens", "timestamp"]
    with open(out / "v41_provenance.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            rid = r["returned_model_id"]
            if override and r["alias"].removeprefix("models/") == override[0]:
                rid = override[1]
            ts = r["timestamp"].replace("2026-06-10", "2026-11-18")
            w.writerow({**{k: r.get(k, "") for k in fields}, "returned_model_id": rid,
                        "finish_reason": "end_turn", "output_tokens": "", "thinking_tokens": "", "timestamp": ts})


def _rw_csv(path, fn):
    rows = list(csv.DictReader(open(path, newline="", encoding="utf-8")))
    fields = list(rows[0].keys())
    rows = fn(rows)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def shuffle_models(out, seed):
    rng = random.Random(seed)
    # v19 parsed results: permute panel_model per frame (same map for every brand row)
    def v19(rows):
        frames = sorted({r["frame"] for r in rows})
        maps = {}
        for fr in frames:
            p = PANEL[:]
            rng.shuffle(p)
            maps[fr] = dict(zip(PANEL, p))
        for r in rows:
            r["panel_model"] = maps[r["frame"]].get(r["panel_model"], r["panel_model"])
        return rows
    _rw_csv(out / "v19/phase_b_results.csv", v19)

    def raw(rows):
        by = {}
        for r in rows:
            by.setdefault(r["frame_id"], []).append(r)
        for fr, rs in by.items():
            models = [r["model"] for r in rs]
            rng.shuffle(models)
            for r, m in zip(rs, models):
                r["model"] = m
        return rows
    for sub in ("v20", "v21", "v22"):
        _rw_csv(out / sub / "phase_b_results.csv", raw)

    for fn in ("v23_phase_b_scored.json", "v23_phase_b_raw.json"):
        p = out / "v23" / fn
        d = json.load(open(p))
        by = {}
        for r in d:
            by.setdefault(r["probe_id"], []).append(r)
        st = random.Random(seed + 1)          # same permutation for raw and scored
        for pid in sorted(by):
            rs = by[pid]
            models = [r["model_id"] for r in rs]
            st.shuffle(models)
            for r, m in zip(rs, models):
                r["model_id"] = m
        json.dump(d, open(p, "w"), ensure_ascii=False, indent=1)


def drop_model(out, model):
    for name in V19_FILES:
        p = out / "v19" / name
        if name.endswith(".jsonl"):
            lines = [l for l in open(p) if l.strip() and json.loads(l).get("panel_model") != model]
            open(p, "w").writelines(lines)
        else:
            _rw_csv(p, lambda rows: [r for r in rows if r["panel_model"] != model])
    for sub in ("v20", "v21", "v22"):
        for name in RAW_FILES:
            _rw_csv(out / sub / name, lambda rows: [r for r in rows if r["model"] != model])
    for name in V23_FILES:
        p = out / "v23" / name
        d = [r for r in json.load(open(p)) if r.get("model_id") != model]
        json.dump(d, open(p, "w"), ensure_ascii=False, indent=1)


def partial_fail(out, model):
    done = {"n": 0}

    def blank(rows):
        for r in rows:
            if r["model"] == model and done["n"] == 0:
                r["response_text"] = ""
                done["n"] = 1
        return rows
    _rw_csv(out / "v21/phase_b_results.csv", blank)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scenario")
    ap.add_argument("out")
    ap.add_argument("--seed", type=int, default=41)
    a = ap.parse_args()
    out = Path(a.out)
    if out.resolve().is_relative_to(ROOT.resolve()):
        sys.exit("refusing to write synthetic data inside the repo")
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    wave = "t1" if a.scenario == "copy_t1" else "t2"
    copy_wave(wave, out)
    if a.scenario == "copy_t1":
        sidecar(out)
    elif a.scenario == "copy_t2":
        sidecar(out)
    elif a.scenario == "shuffle_models":
        shuffle_models(out, a.seed)
        sidecar(out)
    elif a.scenario == "drop_model":
        drop_model(out, "gemini-2.5-flash-lite")
        sidecar(out)
    elif a.scenario == "partial_fail":
        partial_fail(out, "gpt-4o-mini")
        sidecar(out)
    elif a.scenario == "snapshot_drift":
        sidecar(out, override=("gpt-4o", "gpt-4o-2024-11-20"))
    else:
        sys.exit(f"unknown scenario {a.scenario}")
    print(f"{a.scenario} -> {out}")


if __name__ == "__main__":
    main()
