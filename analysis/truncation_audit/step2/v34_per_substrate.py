#!/usr/bin/env python3
"""Step 2 (SENSITIVITY ONLY, not a replacement of osf/v34/v34_verdicts.json): v0.34 (t1 -> t2)
with Gemini 2.5 Flash removed from the per-brand recall/recognition vectors of chosen substrates.

score_v34.py reads and writes ~/aias (fixed paths, six-model PANEL). Run this ONLY with HOME
pointing at a scratch tree whose aias/ mirrors what it reads (scripts, prereg, osf/v19..v23,
osf/v34/data, osf/methodology/v1_7/data); the script refuses otherwise. It imports the locked
score_v34 from that mirror and replaces three module functions before calling score():
  wave_t1, wave_t2  -> the locked extractors, then Flash's entry dropped from the recall and
                       recog vectors of the chosen substrates (cv_cpc and c_p take any length)
  saturated         -> the locked rule with the model count taken from the vectors instead of a
                       literal 6 (identical for six models; needed for five)
Everything else (Spearman, permutation nulls, seed, thresholds, verdict rules) is score_v34's.

  --mode baseline | a (v0.19 and v0.23) | b (all substrates)   --out FILE
"""
import sys
from pathlib import Path

ROOT = Path.home() / "aias"
if "_runner_tmp" not in str(ROOT.resolve()):
    sys.exit(f"refusing: ~/aias resolves to {ROOT.resolve()}; run with HOME=<scratch mirror>")
sys.path.insert(0, str(ROOT / "scripts"))
import score_v34 as V34  # noqa: E402

import argparse  # noqa: E402
import json  # noqa: E402

FL = V34.PANEL.index("gemini-2.5-flash")
SUBS = {"baseline": (), "a": ("v0.19", "v0.23"), "b": tuple(V34.OMNI)}


def drop(wave, subs):
    out = {}
    for s, d in wave.items():
        if s in subs:
            out[s] = {b: {"recall": [x for i, x in enumerate(v["recall"]) if i != FL],
                          "recog": [x for i, x in enumerate(v["recog"]) if i != FL]} for b, v in d.items()}
        else:
            out[s] = d
    return out


def saturated_m(brands, wave, defined_keys):
    """score_v34.saturated; range(6) replaced by the vectors' model count."""
    if not defined_keys:
        return False, []
    nm = len(wave[defined_keys[0]]["recog"])
    rates = []
    for mi in range(nm):
        rec = sum(1 for b in defined_keys if wave[b]["recog"][mi] == 1)
        rates.append(rec / len(defined_keys))
    return all(r >= 0.90 for r in rates), rates


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", required=True, choices=list(SUBS))
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    subs = SUBS[a.mode]
    w1, w2 = V34.wave_t1, V34.wave_t2
    V34.wave_t1 = lambda: drop(w1(), subs)
    V34.wave_t2 = lambda: drop(w2(), subs)
    V34.saturated = saturated_m
    out = V34.score()
    out["SENSITIVITY_ONLY"] = "not a replacement of osf/v34/v34_verdicts.json"
    out["flash_dropped_in"] = list(subs)
    json.dump(V34._clean(out), open(a.out, "w"), indent=2, allow_nan=False)
    print(f"wrote {a.out}")
    for tag, v in out["verdicts"].items():
        print(f"  {tag}: {v['verdict']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
