"""Dry-run record, pre-registration section 11: the two earlier versions of world A (indep, resid) at the recorded seed
and five further seeds, with the truth check (rho_w(v, P) on the rated units). Synthetic data only."""
import sys, tempfile
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "scripts"))
import score_v1_16 as V

orig = V._syn_latents


def make(kind):
    def lat(seed, world):
        rng = np.random.default_rng(seed)
        out = {}
        for s, n in V.SYN_SIZES.items():
            u = rng.normal(0, 1, n)
            z = rng.normal(0, 1, n)
            if kind == "resid":
                uc = u - u.mean()
                z = z - z.mean() - uc * (uc @ (z - z.mean())) / (uc @ uc)
                z = z / z.std()
            names = (["Denon"] if s == "v0.19" else []) + [f"Zq{s[-2:]}b{j:02d}" for j in range(n - (s == "v0.19"))]
            out[s] = (names, u, z)
        return out
    return lat


for kind in ("indep", "resid"):
    V._syn_latents = make(kind)
    for seed in (116100, 1, 2, 3, 4, 5):
        with tempfile.TemporaryDirectory() as td:
            pins = V.build_synthetic(Path(td), "A_independent_precedence", seed)
            inp = V.load_inputs(Path(td), pins)
            res = V.analyse(inp, log=lambda m: None, n_shuffle=1, n_perm=1, boot=False, sensitivities=False)
            tr = V._truth(res, seed, "A_independent_precedence")
            h1 = {w: v["rho"] for w, v in res["H1_Sep_Presence"]["per_wave"].items()}
            gap = [h1[w] - tr[w]["rho_true_v_P"] for w in V.SEP_WAVES]
            print(kind, seed, "H1", [round(h1[w], 3) for w in V.SEP_WAVES], "truth",
                  [round(tr[w]["rho_true_v_P"], 3) for w in V.SEP_WAVES], "gap", [round(g, 3) for g in gap])
