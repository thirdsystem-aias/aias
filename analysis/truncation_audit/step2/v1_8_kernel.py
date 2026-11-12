#!/usr/bin/env python3
"""Step 2 (SENSITIVITY ONLY, not a replacement of the v1.8 record): v1.8 verdicts with a
per-substrate keep list.

score_v1_8.py (branch v1.8) writes fixed paths and asserts M = 6, so the instrument table is
rebuilt with score_v41's kernel (load_wave + wave_metrics with a keep list; v0.41 gate P1 shows
it reproduces v1.8's 112 phi rows on the full panel), and the verdicts are then taken by the
LOCKED v1.8 functions, imported unchanged from a scratch copy of the v1.8 branch file
(git show v1.8:scripts/score_v1_8.py, its prereg module alongside): cvcpc_of (CPC_raw, CPC_corr),
framing_membership (v0.35 roster, v0.36 stratum), verdicts (H_CV_Reproduces, H_MeanIndependent,
H_LowRecallDefined, H_GradedRecognition, H_PositionalDissociation, H_PhantomSignature) and
_spearman (two-wave phi t1-t2 agreement, as in two_wave_reproducibility).

  --mode baseline | a | b   --v18mod DIR (scratch copy)   --out FILE
Run with AIAS_ROOT=<truncation-audit worktree>. Writes only --out (and --table).
"""
import os
import sys
from pathlib import Path

WT = Path(__file__).resolve().parents[3]
os.environ.setdefault("AIAS_ROOT", str(WT))
sys.path.insert(0, str(WT / "osf/v41/scripts"))
import score_v41 as S  # noqa: E402  (HOME shim re-exec; ~/aias -> AIAS_ROOT)

import argparse  # noqa: E402
import csv  # noqa: E402
import json  # noqa: E402

import score_v0_31 as S31  # noqa: E402

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


def instrument_table(V18, wm, kb):
    """score_v1_8.build_instrument_table's row layout: k, pi_hat, phi from the kernel
    (wave_metrics with the keep list); J from v1.8's own frame extraction
    (score_v1_8.stage0_frame_surfacing, t1) restricted to the kept models and taken with
    score_v1_8.jaccard_of in v1.8's model order (the kernel's J equals it to 1e-16 but its
    model order differs, which moves ties in the phi-J Spearman); CPC_raw / CPC_corr from
    score_v1_8.cvcpc_of. All substrates are frame-resolved in the v1.8 record."""
    frames, resolved = V18.stage0_frame_surfacing(PANEL)
    assert all(resolved.get(s) for s in S.OMNI), resolved
    table = []
    for s in S.OMNI:
        kept = {PANEL[i] for i in kb[s]}
        for b, m in wm[s].items():
            vec = m["k"]
            J, nJ = V18.jaccard_of({mm: fs for mm, fs in frames[s].get(b, {}).items() if mm in kept}) \
                if b in frames[s] else (None, 0)
            table.append({"substrate": s, "brand": b, "cell": m["cell"], "k_per_model": list(vec),
                          "pi_hat": m["pi_hat"], "mu": m["pi_hat"], "phi": m["phi"],
                          "phi_partition": m["phi_partition"], "phi_defined": m["phi_partition"] == "defined",
                          "J": J, "J_n_models": nJ, "J_defined": J is not None,
                          "J_frame_resolved_substrate": True, **V18.cvcpc_of(vec)})
    return table


NUM = ("pi_hat", "phi", "J", "mu_count", "sd_pop", "cpc_raw", "cpc_corr")
EXACT = ("phi_partition", "phi_defined", "J_defined", "J_n_models", "cpc_raw_defined", "cpc_corr_defined")


def compare_table(table, ref_csv):
    ref = {(r["substrate"], r["brand"]): r for r in csv.DictReader(open(ref_csv, newline=""))}
    mine = {(r["substrate"], r["brand"]): r for r in table}
    probs, maxd = [], 0.0
    if set(ref) != set(mine):
        probs.append("key sets differ")
    for k in sorted(set(ref) & set(mine)):
        r, m = ref[k], mine[k]
        if json.loads(r["k_per_model"]) != m["k_per_model"]:
            probs.append(f"{k} k")
        for f in EXACT:
            if r[f] != ("" if m[f] is None else str(m[f])):
                probs.append(f"{k} {f}: {r[f]} vs {m[f]}")
        for f in NUM:
            if (r[f] == "") != (m[f] is None):
                probs.append(f"{k} {f} definedness")
            elif r[f] != "":
                maxd = max(maxd, abs(float(r[f]) - m[f]))
    return {"rows": len(mine), "problems": probs[:20], "max_abs_diff": maxd}


def compare_tree(a, b, path="", tol=1e-12):
    out = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in set(a) | set(b):
            if k not in a or k not in b:
                out.append(f"{path}/{k} missing")
            else:
                out += compare_tree(a[k], b[k], f"{path}/{k}", tol)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            out.append(f"{path} length {len(a)} vs {len(b)}")
        else:
            for i, (x, y) in enumerate(zip(a, b)):
                out += compare_tree(x, y, f"{path}[{i}]", tol)
    elif isinstance(a, float) and isinstance(b, (int, float)) and not isinstance(b, bool):
        if abs(a - b) > tol:
            out.append(f"{path}: {a} vs {b}")
    elif a != b:
        out.append(f"{path}: {a!r} vs {b!r}")
    return out


def main():
    import numpy as np
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", required=True, choices=["baseline", "a", "b"])
    ap.add_argument("--v18mod", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--table")
    a = ap.parse_args()
    sys.path.insert(0, str(Path(a.v18mod) / "prereg"))
    sys.path.insert(0, str(Path(a.v18mod)))
    import score_v1_8 as V18
    kb = keep_lists(a.mode)
    gates, t1, t2 = S.run_gates()
    wm1, wm2 = wave_metrics_ps(t1, kb), wave_metrics_ps(t2, kb)
    V18._cv_parity_check()
    table = instrument_table(V18, wm1, kb)
    members, v35_phantom = V18.framing_membership(table)
    ref = json.load(open(S.REF_DIR / "v1_8_verdicts.json"))
    verds = V18.verdicts(table, members, v35_phantom, ref["reconciliation_gate"], {s: True for s in S.OMNI})
    pairs = []
    for sub in S.OMNI:
        for b in (set(wm1[sub]) & set(wm2[sub])):
            if wm1[sub][b]["phi"] is not None and wm2[sub][b]["phi"] is not None:
                pairs.append((wm1[sub][b]["phi"], wm2[sub][b]["phi"]))
    x, y = zip(*pairs)
    two = {"phi_t1_t2_rank_agreement": V18._spearman(np.array(x, float), np.array(y, float)), "n_pairs": len(pairs)}
    out = {"SENSITIVITY_ONLY": "not a replacement of the v1.8 record", "mode": a.mode,
           "keep_by_substrate": {s: [PANEL[i] for i in kb[s]] for s in S.OMNI},
           "two_wave_reproducibility": two, "verdicts": verds}
    if a.mode == "baseline":
        out["baseline_check"] = {
            "instrument_table_vs_frozen": compare_table(table, S.REF_DIR / "v1_8_instrument_table.csv"),
            "verdicts_vs_frozen_tol_1e-12": compare_tree(ref["verdicts"], json.loads(json.dumps(S._clean(verds)))),
            "two_wave_vs_frozen_tol_1e-12": compare_tree(ref["two_wave_reproducibility"], json.loads(json.dumps(S._clean(two))))}
    json.dump(S._clean(out), open(a.out, "w"), indent=2, allow_nan=False)
    if a.table:
        cols = list(table[0])
        with open(a.table, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            for r in table:
                w.writerow({k: ("" if v is None else (json.dumps(v) if k == "k_per_model" else v)) for k, v in r.items()})
    print(a.mode, {k: v["verdict"] for k, v in verds.items()}, two["phi_t1_t2_rank_agreement"])
    if "baseline_check" in out:
        print(json.dumps(S._clean(out["baseline_check"]), indent=1)[:1500])
    return 0


if __name__ == "__main__":
    sys.exit(main())
