#!/usr/bin/env python3
"""code_predictors_v0_46.py -- AIAS(TM) v0.46 (#76): v0.42's locked coder run on v46_raw's predictor blocks.

Stage 1 code r3, task 3. Section 3.4 ("Coding"): the predictor blocks P1-P4 are coded by v0.42's locked coder
(osf/v42/scripts/code_t4_v0_42.py, blob 2d36735d), unchanged. This is a thin wrapper, not a re-write:
  1. verify the coder file is byte-identical to the locked blob (git blob hash) -- else halt;
  2. select the predictor lines of v46_raw (part == "predictor"; acquire_v0_46 writes them in t4's schema:
     call_id, substrate v20..v23, phase A|B, condition S0, run, model_requested, probe_id, brand_id, frame_id,
     status, text, error). Choice lines (part == "choice", phase "v0.46") are left out: v0.42's coder would read
     a phase that is not "B" as Phase A;
  3. run the coder as its own process (it re-executes the interpreter under a ~/aias shim when the worktree is
     not ~/aias, so it cannot be imported here) with `--raw <predictor lines> --out <dir>` and NEVER `--judge`;
     the child's environment has every API-key variable removed, so it could not call a model even if asked.
Output: v0.42's tables {sub}_phase_a.csv / {sub}_phase_b.csv, which predictors_v0_46.py reads. v0.23 (spirits)
Phase A recognition is NOT coded here (v0.42's judge is OFF); the spirits judge is wired in judge_spirits_v0_46.py.

The v0.42 coder's probe map is its own probe file (osf/v42/prereg/probes_v0_42.jsonl); v0.46's predictor rows are
byte-identical to its v0.20-v0.23 rows (test_predictor_rows_byte_identical), so probe IDs resolve unchanged.

NO MODEL IS CALLED. No network.

Usage:
  python3 osf/v46/scripts/code_predictors_v0_46.py --dry-run             # synthetic v46_raw fixture, keyless
  python3 osf/v46/scripts/code_predictors_v0_46.py --raw osf/v46/data/v46_raw.jsonl --out osf/v46/data/coded
"""
import argparse
import csv
import json
import os
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
V42_CODER = ROOT / "osf" / "v42" / "scripts" / "code_t4_v0_42.py"
V42_CODER_BLOB = "2d36735d512cf9e13b74010ba5a7f655fc7de0bc"     # section 3.4 "blob 2d36735d" (commit 759f17e)
PY = sys.executable
SUBS = ("v20", "v21", "v22", "v23")
SUB_CATEGORY = {"v20": "skincare", "v21": "cosmetics", "v22": "cars", "v23": "spirits"}
KEY_ENV_MARKERS = ("API_KEY", "APIKEY", "_TOKEN", "SECRET", "CREDENTIAL")
KEY_ENV_PREFIXES = ("ANTHROPIC", "OPENAI", "GOOGLE", "GEMINI", "VERTEX", "AZURE", "AWS")


class CoderHalt(RuntimeError):
    pass


def git_blob(data):
    import hashlib
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def verify_coder(path=V42_CODER):
    if not Path(path).exists():
        raise CoderHalt(f"v0.42 coder not found: {path}")
    got = git_blob(Path(path).read_bytes())
    if got != V42_CODER_BLOB:
        raise CoderHalt(f"v0.42 coder changed: blob {got} != locked {V42_CODER_BLOB}")
    return got


def keyless_env(env=None):
    """A copy of the environment with every API-key / credential variable removed."""
    env = dict(os.environ if env is None else env)
    for k in list(env):
        ku = k.upper()
        if any(m in ku for m in KEY_ENV_MARKERS) or ku.startswith(KEY_ENV_PREFIXES):
            del env[k]
    return env


def predictor_lines(raw):
    """The predictor lines of v46_raw (part == "predictor"; for lines without `part`, phase A|B and condition S0)."""
    out = []
    for r in raw:
        part = r.get("part")
        if part == "predictor" or (part is None and r.get("phase") in ("A", "B") and r.get("condition") == "S0"):
            out.append(r)
    return out


def write_jsonl(rows, path):
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def run_v42_coder(raw_records, out_dir, timeout=600, log=print):
    """Code the predictor lines of `raw_records` with v0.42's locked coder into `out_dir`. Judge OFF, keyless.
    Returns (n_predictor_lines, coder stdout)."""
    verify_coder()
    pred = predictor_lines(raw_records)
    if not pred:
        raise CoderHalt("no predictor lines in the raw file")
    bad = sorted({r.get("substrate") for r in pred} - set(SUBS))
    if bad:
        raise CoderHalt(f"substrates outside v0.46's four: {bad}")
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="v46_pred_raw_") as tmp:
        p = Path(tmp) / "v46_predictor_lines.jsonl"
        write_jsonl(pred, p)
        cmd = [PY, str(V42_CODER), "--raw", str(p), "--out", str(out_dir)]
        assert "--judge" not in cmd
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, env=keyless_env(),
                           cwd=str(ROOT))
    if r.returncode != 0:
        raise CoderHalt(f"v0.42 coder exit {r.returncode}: {(r.stderr or r.stdout).strip()[-600:]}")
    log(f"[v46] v0.42 coder: {r.stdout.strip()}")
    return len(pred), r.stdout


def read_table(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# --------------------------------------------------------------------------- keyless dry run (synthetic fixture)
def fixture_raw(seed=46):
    """A synthetic v46_raw: every predictor call of the orientation panel (acquire_v0_46.build_specs, written by
    acquire_v0_46._record exactly as a collection would), plus three choice lines that must be left out."""
    import acquire_v0_46 as A
    import build_probes_v0_46 as B
    panel = A.make_panel(A.ORIENTATION_PANEL)
    specs = A.build_specs(A.load_probes(), panel)
    reg = B.registry_units()
    slot_ix = {m["model_id"]: i for i, m in enumerate(panel)}
    raw = []
    for s in specs:
        if s["v46"]["part"] == "predictor":
            names = [b for b, _c in reg[SUB_CATEGORY[s["substrate"]]]][:10]
            k = (slot_ix[s["model"]["model_id"]] + (s["run"] or 0) + seed) % len(names)
            if s["phase"] == "A":
                text = "No." if s["probe_id"].endswith(("3", "7")) else "Yes."
            else:
                order = names[k:] + names[:k]
                text = "Here are my picks:\n" + "\n".join(f"{i}. {b}" for i, b in enumerate(order[:6], 1))
        else:
            if sum(r.get("part") == "choice" for r in raw) >= 3:
                continue
            text = "A sensible pick.\nCHOICE: Toyota"
        out = {"text": text, "served_model": s["model"]["model_id"], "finish_reason": "end_turn",
               "tokens_in": 300, "tokens_out": 40, "tokens_thought": None, "paused_continued": False,
               "search": None}
        raw.append(A._record(s, out, "ok", None, 1, False, "2026-12-01T00:00:00+00:00",
                             "2026-12-01T00:00:01+00:00", []))
    return raw, panel


def dry_run(log=print):
    """Code the synthetic fixture with v0.42's coder (judge OFF, keyless) and feed predictors_v0_46. -> fails"""
    import predictors_v0_46 as PR
    fails = []
    raw, panel = fixture_raw()
    models = [m["model_id"] for m in panel]
    with tempfile.TemporaryDirectory(prefix="v46_coded_") as out:
        n, _so = run_v42_coder(raw, out, log=log)
        a = {s: read_table(Path(out) / f"{s}_phase_a.csv") for s in SUBS}
        b = {s: read_table(Path(out) / f"{s}_phase_b.csv") for s in SUBS}
        ca, cb = PR.read_coded_dir(out)
    n_a = Counter(r["phase"] for r in raw if r.get("part") == "predictor")
    log(f"  predictor lines {n} (A {n_a['A']}, B {n_a['B']}); choice lines left out "
        f"{sum(r.get('part') == 'choice' for r in raw)}")
    if n != 504:
        fails.append(f"predictor lines {n} != 504")
    for s in SUBS:
        calls_b = len({r["call_id"] for r in b[s]})
        log(f"  {s}: phase A rows {len(a[s])}, phase B rows {len(b[s])} over {calls_b} calls, "
            f"mentioned {sum(int(r['mentioned']) for r in b[s])}")
        want_a = 0 if s == "v23" else 72            # v23 recognition = the judge, OFF here
        if len(a[s]) != want_a:
            fails.append(f"{s} phase A rows {len(a[s])} != {want_a}")
        if calls_b != 54:                           # 6 frames x 3 models x 3 runs
            fails.append(f"{s} phase B calls {calls_b} != 54")
        if sum(int(r["mentioned"]) for r in b[s]) != 54 * 6:
            fails.append(f"{s} mentions != 6 per call")
    pred, meta = PR.compute(raw, ca, cb, models)
    by = Counter((k[0], v["P"] is not None) for k, v in pred.items())
    log(f"  predictors: answers {meta['answers']}, P defined per substrate "
        f"{ {s: by[(s, True)] for s in sorted({k[0] for k in pred})} }")
    if by[("v0.23", True)]:
        fails.append("v0.23 P defined without the judge")
    return fails


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dry-run", action="store_true", help="synthetic v46_raw fixture; keyless; no model called")
    ap.add_argument("--raw")
    ap.add_argument("--out")
    ap.add_argument("--judge", action="store_true", help="refused: the spirits judge is judge_spirits_v0_46.py")
    a = ap.parse_args(argv)
    if a.judge:
        print("[v46] --judge refused: v0.42's coder runs here with its judge OFF; no model is called.",
              file=sys.stderr)
        return 2
    try:
        verify_coder()
        if a.dry_run:
            print("[v46] v0.42 coder on a synthetic v46_raw (keyless; no model called)")
            fails = dry_run()
            print(f"[v46] predictor coding dry run {'PASS' if not fails else 'FAIL: ' + '; '.join(fails)}")
            return 1 if fails else 0
        if not (a.raw and a.out):
            ap.error("--raw and --out are required unless --dry-run")
        raw = [json.loads(ln) for ln in open(a.raw, encoding="utf-8") if ln.strip()]
        run_v42_coder(raw, a.out)
        return 0
    except CoderHalt as e:
        print(f"[v46] HALT: {e}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
