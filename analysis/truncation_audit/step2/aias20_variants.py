#!/usr/bin/env python3
"""Step 2 (SENSITIVITY ONLY, not a replacement of osf/aias_2_0/*): AIAS 2.0 summaries and the
section-5 class with a PER-SUBSTRATE keep list in every wave, from the builder's own functions
(aias_2_0_synthesis_data.wave_rows / summarize / classify, score_v1_9.retest).

The stock builder keeps t1/t2 on the full panel (parity A1-A5 against the locked Stage 1) and
takes the t3 panel from the v1.9 verdicts' panel_used, panel-wide. This wrapper applies the
variant's keep list to t1, t2 and t3 alike (so A1-A5 are not re-checked for (a)/(b): Stage 1 is
full panel by construction), and classifies with the variant's own v0.41 and v1.9 verdict files.

  --mode baseline|a|b  --t3 DIR  --v41 FILE --v19 FILE  --out JSON
Run with AIAS_ROOT=<aias-2.0 worktree>. Writes only --out.
"""
import os
import sys
from pathlib import Path

_root = Path(os.environ["AIAS_ROOT"])
sys.path.insert(0, str(_root / "scripts"))
import aias_2_0_synthesis_data as B  # noqa: E402  (imports score_v1_9 -> score_v41: HOME shim re-exec)

import argparse  # noqa: E402
import json  # noqa: E402

import score_v0_31 as S31  # noqa: E402

S, V19 = B.S, B.V19
PANEL = S31.PANEL
FULL = list(range(S.M))
NOFL = [i for i in FULL if PANEL[i] != "gemini-2.5-flash"]


def keep_lists(mode):
    return {"baseline": {s: FULL for s in S.OMNI},
            "a": {s: (NOFL if s in ("v0.19", "v0.23") else FULL) for s in S.OMNI},
            "b": {s: NOFL for s in S.OMNI}}[mode]


def wave_metrics_ps(wave, kb):
    cache, out = {}, {}
    for s in S.OMNI:
        key = tuple(kb[s])
        if key not in cache:
            cache[key] = S.wave_metrics(wave, list(key))
        out[s] = cache[key][s]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", required=True, choices=["baseline", "a", "b"])
    ap.add_argument("--t3", required=True)
    ap.add_argument("--v41", required=True)
    ap.add_argument("--v19", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    kb = keep_lists(a.mode)
    gates, t1, t2 = S.run_gates()
    base = Path(a.t3).resolve()
    t3 = S.load_wave(S._layout(base, base / "v23"))
    rows = {w: B.wave_rows(wave_metrics_ps(x, kb)) for w, x in (("t1", t1), ("t2", t2), ("t3", t3))}
    summ = {w: B.summarize(r) for w, r in rows.items()}
    relC, nC = V19.retest(rows["t2"], rows["t3"], "C")
    relP, nP = V19.retest(rows["t2"], rows["t3"], "P")
    v41, v19 = json.load(open(a.v41)), json.load(open(a.v19))
    out = {"SENSITIVITY_ONLY": "not a replacement of osf/aias_2_0/aias_2_0_synthesis_data.json",
           "mode": a.mode, "keep_by_substrate": {s: [PANEL[i] for i in kb[s]] for s in S.OMNI},
           "v41_file": a.v41, "v19_file": a.v19, "summaries": summ,
           "descriptive_retest_t2_t3": {"C_star": [relC, nC], "P": [relP, nP]},
           "rho_Cstar_P_t3_matches_v19": abs(summ["t3"]["rho_Cstar_P"] - v19["verdicts"]["H_Dissociation_t3"]["rho"])
           <= B.PARITY_TOL,
           "class": B.classify(v19, v41)}
    json.dump(S._clean(out), open(a.out, "w"), indent=2, allow_nan=False)
    print(a.mode, "class", out["class"]["class"], out["class"]["flags"],
          {w: round(summ[w]["rho_Cstar_P"], 4) for w in summ}, "retest C*", round(relC, 4), nC)
    return 0


if __name__ == "__main__":
    sys.exit(main())
