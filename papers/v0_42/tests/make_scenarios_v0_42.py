#!/usr/bin/env python3
"""
make_scenarios_v0_42.py -- SYNTHETIC t4 scenarios for testing the v0.42 paper/report pipeline (never real data).

Writes DIR/<scenario>/t4_raw.jsonl + DIR/<scenario>/coded/ with osf/v42/scripts/tests/make_synthetic_t4.build (the
scorer's own synthetic writer, real formats), then the scorer is run on each with `score_v0_42.py --synthetic`.
Refuses any DIR inside the repository (outputs belong under /tmp/t4_pipeline_test/).

Scenarios (k maps from the locked t3 counts of three legacy models, indices 0, 2, 4):
  copy   every model, condition and run = its t3 counts (the scorer's own synthetic default)
  noisy  per (model, condition, run) a share of brands has its k permuted within substrate
         (search off 30%, search on 55%; different seed per run), so runs, conditions and generations differ

Usage: python3 papers/v0_42/tests/make_scenarios_v0_42.py /tmp/t4_pipeline_test/synth [copy noisy]
"""
import sys
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "osf/v42/scripts/tests"))
sys.path.insert(0, str(ROOT / "osf/v42/scripts"))
import make_synthetic_t4 as MS  # noqa: E402
import score_v0_42 as S  # noqa: E402

FRAC = {"S0": 0.30, "S1": 0.55}


def scenario_kfn(name, t3):
    L = {m: MS.from_t3(t3, i) for m, i in zip(MS.MODELS, (0, 2, 4))}
    if name == "copy":
        return lambda m, c, r: L[m]
    if name == "noisy":
        return lambda m, c, r: MS.mixed(L[m], FRAC[c], zlib.crc32(f"{m}|{c}|{r}".encode()) % 100000)
    raise SystemExit(f"unknown scenario {name}")


def main():
    base = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/t4_pipeline_test/synth").resolve()
    if str(base).startswith(str(ROOT.resolve())):
        raise SystemExit(f"REFUSED: {base} is inside the repository; synthetic outputs go to /tmp")
    t3 = S.load_t3_table()
    for name in (sys.argv[2:] or ["copy", "noisy"]):
        raw, A, B = MS.build(scenario_kfn(name, t3), base / name)
        print(f"{name}: {len(raw)} raw calls, {len(A)} Phase A rows, {len(B)} Phase B rows -> {base / name}")


if __name__ == "__main__":
    main()
