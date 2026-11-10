#!/usr/bin/env python3
"""
precision_v1_11.py - AIAS v1.11: precision of the H1 statistics under the J2 coverage of section 7
(SYNTHETIC valences only; no model call, no judge output, no real valence, no P, C* or R).

Why J2 judges a 10% sample of E windows and not all of them (PRE_REGISTRATION section 7):
  (1) Krippendorff's alpha (ordinal) on synthetic two-judge valence pairs built to sit near the
      CONFIRMED threshold (alpha ~ 0.67-0.70), with a valence mix weighted to 0 and +1: 95%
      bootstrap half-width for the pair counts J2's design gives (R + F + the E sample, the E sample
      alone) and for the alternatives (E at 5%, 20%, 100%).
  (2) Brand-level rho_w(S_J1, S_J2): it is computed on F units only, which J2 judges in full, so its
      precision does not depend on the E share. The number of (substrate, wave, brand) cells with at
      least 6 F windows (the n floor) is counted from the frozen U0 unit table (structure only), and
      the Fisher-z 95% half-width at rho = 0.80 is reported for that n.
Writes prereg/precision_v1_11.json. Run: python3 osf/methodology/v1_11/scoping/precision_v1_11.py
"""
import json
import math
import random
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts"))
import score_v1_11 as S  # noqa: E402

SEED = 111030
N_BOOT = 1000
MIX = {-2: 0.01, -1: 0.04, 0: 0.45, 1: 0.40, 2: 0.10}     # synthetic valence mix (assumption)


def synth_pairs(n, p_same, rng):
    vals, w = list(MIX), list(MIX.values())
    out = []
    for _ in range(n):
        a = rng.choices(vals, w)[0]
        b = a if rng.random() < p_same else max(-2, min(2, a + rng.choice((-1, 1))))
        out.append((a, b))
    return out


def half_width(pairs, rng):
    n = len(pairs)
    boots = sorted(S.krippendorff_alpha_ordinal([pairs[rng.randrange(n)] for _ in range(n)]) for _ in range(N_BOOT))
    return (boots[int(0.975 * N_BOOT) - 1] - boots[int(0.025 * N_BOOT)]) / 2


def main() -> int:
    units = [u for u in S.read_units(S.PREREG_DIR / S.UNITS_NAME) if u["judged"]]
    n_rf = sum(1 for u in units if u["block"] in ("R", "F"))
    n_e = sum(1 for u in units if u["block"] == "E")
    f_cells = Counter((u["category"], u["wave"], u["brand"]) for u in units if u["block"] == "F")
    rated = sum(1 for v in f_cells.values() if v >= S.N_FLOOR)
    rng = random.Random(SEED)
    lo_p, hi_p = 0.0, 1.0                            # p_same giving population alpha ~ 0.68 (bisection)
    for _ in range(14):
        p_same = (lo_p + hi_p) / 2
        a = S.krippendorff_alpha_ordinal(synth_pairs(20000, p_same, random.Random(SEED + 1)))
        lo_p, hi_p = (p_same, hi_p) if a < 0.68 else (lo_p, p_same)
    p_same = round((lo_p + hi_p) / 2, 4)
    alpha_pop = S.krippendorff_alpha_ordinal(synth_pairs(20000, p_same, random.Random(SEED + 1)))
    rows = {}
    for label, share in (("E 5%", 0.05), ("E 10% (design)", 0.10), ("E 20%", 0.20), ("E 100%", 1.0)):
        n_es = round(share * n_e)
        pooled = synth_pairs(n_rf + n_es, p_same, rng)
        e_only = synth_pairs(n_es, p_same, rng)
        rows[label] = {"pairs_pooled": n_rf + n_es, "alpha_pooled_ci95_half_width": round(half_width(pooled, rng), 4),
                       "pairs_E_block": n_es, "alpha_E_block_ci95_half_width": round(half_width(e_only, rng), 4)}
    z_se = 1 / math.sqrt(rated - 3)
    lo, hi = math.tanh(math.atanh(0.80) - 1.96 * z_se), math.tanh(math.atanh(0.80) + 1.96 * z_se)
    doc = {"phase": S.PHASE_ID, "kind": "synthetic precision check (no model call, no real valence)",
           "seed": SEED, "bootstrap_draws": N_BOOT, "synthetic_valence_mix": MIX, "p_same_valence": p_same,
           "synthetic_alpha_population": round(alpha_pop, 4), "judged_units": {"R+F": n_rf, "E": n_e},
           "alpha_precision": rows,
           "brand_rho": {"F_brand_wave_cells_with_at_least_6_windows": rated, "fisher_z_ci95_at_rho_0_80":
                         [round(lo, 3), round(hi, 3)], "note": "F is judged in full by J2: independent of the E share"},
           "thresholds": {"alpha_confirmed": S.ALPHA_CONFIRMED_MIN, "alpha_falsified_below": S.ALPHA_FALSIFIED_BELOW,
                          "brand_rho_confirmed": S.BRAND_AGREE_CONFIRMED_MIN,
                          "brand_rho_falsified_below": S.BRAND_AGREE_FALSIFIED_BELOW}}
    out = S.PREREG_DIR / "precision_v1_11.json"
    out.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(doc, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
