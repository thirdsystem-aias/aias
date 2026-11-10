#!/usr/bin/env python3
"""
make_synthetic_t5.py -- SYNTHETIC t4 and t5 waves in the real formats (raw lines and coded tables), for the v0.45
tests and the dry run. Uses v0.42's own generator (osf/v42/scripts/tests/make_synthetic_t4.py, unchanged): the t5
wave is the same generator with December timestamps, written as t5_raw.jsonl. Never touches osf/v42/data or
osf/v45/data; no model is called. Outputs go to /tmp unless a directory is given.

  noisy(base, model, cond, run, seed, sd) -> k map: base k + rounded normal noise, clipped to 0..6 (run-to-run noise)
  wave(kfn, outdir, name, t0, fail=None) -> (raw, A, B) written to outdir/<name>_raw.jsonl and outdir/coded
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
V42_TESTS = HERE.parents[2] / "v42" / "scripts" / "tests"
sys.path.insert(0, str(HERE.parents[0]))
sys.path.insert(0, str(V42_TESTS))
import code_t5_v0_45 as K        # noqa: E402
import make_synthetic_t4 as M4   # noqa: E402
import numpy as np               # noqa: E402

C = K.C
MODELS = M4.MODELS
LEGACY_INDEX = {"claude-fable-5-2": 0, "gpt-6-astra": 2, "gemini-4-argon": 4}


def base_maps(t3):
    return {m: M4.from_t3(t3, i) for m, i in LEGACY_INDEX.items()}


def noisy(base, model, cond, run, seed, sd=0.8):
    rng = np.random.default_rng([seed, MODELS.index(model), 0 if cond == "S0" else 1, run])
    return {k: int(min(6, max(0, round(v + rng.normal(0, sd))))) for k, v in sorted(base.items())}


def wave(kfn, outdir, name, t0, fail=None, served=None, end=None):
    raw, A, B = M4.build(kfn, None, fail=fail, served=served, t0=t0)
    for r in raw:
        r["finished_utc"] = end or t0
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    with open(outdir / f"{name}_raw.jsonl", "w", encoding="utf-8") as f:
        for r in raw:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    C.write_tables(A, B, outdir / "coded")
    return raw, A, B


if __name__ == "__main__":
    import score_v0_42 as S
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/v45_synthetic")
    base = base_maps(S.load_t3_table())
    wave(lambda m, c, r: noisy(base[m], m, c, r, 4), out / "t4", "t4", "2026-11-12T00:00:00+00:00")
    wave(lambda m, c, r: noisy(base[m], m, c, r, 5), out / "t5", "t5", "2026-12-03T07:00:00+00:00")
    print(f"synthetic t4 and t5 written to {out}")
