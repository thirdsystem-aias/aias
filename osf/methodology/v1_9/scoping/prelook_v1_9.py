#!/usr/bin/env python3
"""
prelook_v1_9.py — scoping look for v1.9 on the FROZEN t1/t2 waves (already in the record;
no t3 data). Informs the candidate set and the selection rule; it is not a v1.9 result.

P   = v0.25 presence_composite = 100 * (C_P/6 + R_cat/18 + R_cult/18) / 3
      = 100 * (C_P/6 + 2*pi_hat) / 3   (channel-agnostic identity; all five substrates)
C   = 100 * (1 - phi / phi_max), phi_max = F*M/(M-1) = 7.2 (all-or-nothing per model)
      pi_hat = 1 -> C = 100 (no dispersion); pi_hat = 0 -> C undefined
"""
import os
import sys
from pathlib import Path

_root = Path(os.environ.get("AIAS_ROOT", str(Path.home() / "aias")))
sys.path.insert(0, str(_root / "osf/v41/scripts"))
import score_v41 as S   # noqa: E402  (re-executes with the ~/aias shim if needed)

import json             # noqa: E402
import numpy as np      # noqa: E402

PHI_MAX = S.F * S.M / (S.M - 1)


def table(wave):
    w = S.wave_metrics(wave, list(range(S.M)))
    rows = []
    for s in S.OMNI:
        for b, m in w[s].items():
            P = 100 * (m["C_P"] / 6 + 2 * m["pi_hat"]) / 3
            if m["pi_hat"] >= 1:
                C = 100.0
            elif m["phi"] is None:
                C = None
            else:
                C = 100 * (1 - m["phi"] / PHI_MAX)
            rows.append({"s": s, "b": b, "P": P, "C": C, "phi": m["phi"], "J": m["J"],
                         "pi": m["pi_hat"], "mentions": sum(m["k"]), "C_P": m["C_P"]})
    return rows


def rho(rows, a, b, pooled_within=True):
    r = [x for x in rows if x[a] is not None and x[b] is not None]
    g = [x["s"] for x in r]
    f = S.pooled_within_rho if pooled_within else (lambda x, y, g: S.spearman(x, y))
    return round(f([x[a] for x in r], [x[b] for x in r], g), 3), len(r)


def main():
    t1 = table(S.load_wave(S.LAYOUT["t1"]))
    t2 = table(S.load_wave(S.LAYOUT["t2"]))
    out = {}
    out["n_units"] = len(t1)
    out["C_defined_t1"] = sum(1 for r in t1 if r["C"] is not None)
    out["never_recalled_t1"] = sum(1 for r in t1 if r["mentions"] == 0)
    out["saturated_t1"] = sum(1 for r in t1 if r["pi"] >= 1)
    out["rho_C_P_t1_within"] = rho(t1, "C", "P")
    out["rho_C_P_t2_within"] = rho(t2, "C", "P")
    out["rho_phi_J_t1_pooled"] = rho(t1, "phi", "J", False)
    # low-count behaviour: C by total mentions
    by = {}
    for r in t1:
        if r["C"] is not None:
            key = "1-2" if r["mentions"] <= 2 else "3-6" if r["mentions"] <= 6 else "7-18" if r["mentions"] <= 18 else "19-36"
            by.setdefault(key, []).append(r["C"])
    out["C_by_total_mentions_t1"] = {k: {"n": len(v), "mean_C": round(float(np.mean(v)), 1)} for k, v in sorted(by.items())}
    # test-retest t1 -> t2
    key2 = {(r["s"], r["b"]): r for r in t2}
    def retest(field, pooled_within=True):
        pairs = [(r, key2[(r["s"], r["b"])]) for r in t1 if (r["s"], r["b"]) in key2
                 and r[field] is not None and key2[(r["s"], r["b"])][field] is not None]
        x = [a[field] for a, _ in pairs]; y = [b[field] for _, b in pairs]; g = [a["s"] for a, _ in pairs]
        f = S.pooled_within_rho if pooled_within else (lambda x, y, g: S.spearman(x, y))
        return round(f(x, y, g), 3), len(pairs)
    for r in t1 + t2:
        r["A_add"] = (r["P"] + r["C"]) / 2 if r["C"] is not None else r["P"]
        r["A_mult"] = r["P"] * (r["C"] / 100) if r["C"] is not None else 0.0
    out["retest_t1_t2_within"] = {f: retest(f) for f in ("P", "C", "A_add", "A_mult")}
    out["rho_A_add_P_t1"] = rho(t1, "A_add", "P")
    out["rho_A_mult_P_t1"] = rho(t1, "A_mult", "P")
    # discontinuity example: never recalled vs recalled once (additive form)
    zero = [r["A_add"] for r in t1 if r["mentions"] == 0]
    once = [r["A_add"] for r in t1 if r["mentions"] == 1]
    out["A_add_never_recalled_mean"] = round(float(np.mean(zero)), 1) if zero else None
    out["A_add_recalled_once_mean"] = round(float(np.mean(once)), 1) if once else None
    out["n_recalled_once"] = len(once)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
