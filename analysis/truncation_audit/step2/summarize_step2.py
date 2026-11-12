#!/usr/bin/env python3
"""Step 2: one table of every re-checked test, locked vs variant (a) vs variant (b).
Reads the published verdict files and the variant outputs copied into results/; writes
results/verdict_table.csv. Every number in the table is read from those files (key given)."""
import csv
import json
import sys
from pathlib import Path

R = Path(__file__).resolve().parent / "results"
WT = Path(__file__).resolve().parents[3]
A20 = Path(sys.argv[1]) if len(sys.argv) > 1 else WT.parent / "aias-2.0"
FILES = {
    "v0.41": (WT / "osf/v41/v41_verdicts.json", R / "v41_variant_a_verdicts.json", R / "v41_variant_b_verdicts.json"),
    "v1.9": (A20 / "osf/methodology/v1_9/v1_9_verdicts.json", R / "v1_9_variant_a_verdicts.json",
             R / "v1_9_variant_b_verdicts.json"),
    "AIAS 2.0": (R / "aias20_variant_baseline.json", R / "aias20_variant_a.json", R / "aias20_variant_b.json"),
    "v0.34": (WT / "osf/v34/v34_verdicts.json", R / "v34_variant_a.json", R / "v34_variant_b.json"),
    "v1.8": (WT / "osf/v41/registries/v1_8_verdicts.json", R / "v1_8_variant_a.json", R / "v1_8_variant_b.json"),
}


def g(d, path):
    for k in path.split("/"):
        d = d[int(k)] if isinstance(d, list) else d[k]
    return d


def fmt(x):
    if isinstance(x, float):
        return f"{x:.4f}" if abs(x) >= 1e-3 else f"{x:.2e}"
    return str(x)


TESTS = [  # study, test, verdict key, [(label, statistic key)]
    ("v0.41", "H_Phi_LongHorizon (primary)", "verdicts/H_Phi_LongHorizon/verdict",
     [("rho", "verdicts/H_Phi_LongHorizon/rho"), ("p_perm", "verdicts/H_Phi_LongHorizon/p_perm"),
      ("p_frame", "verdicts/H_Phi_LongHorizon/frame_structure_null/p_frame"), ("n", "verdicts/H_Phi_LongHorizon/n")]),
    ("v0.41", "H_Presence_LongHorizon (primary)", "verdicts/H_Presence_LongHorizon/verdict",
     [("substrates rho>=0.70", "verdicts/H_Presence_LongHorizon/n_ge_070"),
      ("rho v0.19", "verdicts/H_Presence_LongHorizon/per_substrate/v0.19/rho"),
      ("rho v0.23", "verdicts/H_Presence_LongHorizon/per_substrate/v0.23/rho"),
      ("rho v0.20", "verdicts/H_Presence_LongHorizon/per_substrate/v0.20/rho"),
      ("rho v0.21", "verdicts/H_Presence_LongHorizon/per_substrate/v0.21/rho"),
      ("rho v0.22", "verdicts/H_Presence_LongHorizon/per_substrate/v0.22/rho")]),
    ("v0.41", "H_Horizon_Decay phi (secondary)", "verdicts/H_Horizon_Decay/phi/verdict",
     [("D", "verdicts/H_Horizon_Decay/phi/D"), ("ci_lo", "verdicts/H_Horizon_Decay/phi/ci95/0"),
      ("ci_hi", "verdicts/H_Horizon_Decay/phi/ci95/1"), ("n", "verdicts/H_Horizon_Decay/phi/n")]),
    ("v0.41", "H_Horizon_Decay pi_hat (secondary)", "verdicts/H_Horizon_Decay/pi_hat/verdict",
     [("D", "verdicts/H_Horizon_Decay/pi_hat/D"), ("ci_lo", "verdicts/H_Horizon_Decay/pi_hat/ci95/0"),
      ("ci_hi", "verdicts/H_Horizon_Decay/pi_hat/ci95/1"), ("n", "verdicts/H_Horizon_Decay/pi_hat/n")]),
    ("v0.41", "H_Drift_Dissociation (secondary)", "verdicts/H_Drift_Dissociation/verdict",
     [("rho", "verdicts/H_Drift_Dissociation/rho"), ("p_two_sided", "verdicts/H_Drift_Dissociation/p_perm_two_sided"),
      ("n", "verdicts/H_Drift_Dissociation/n")]),
    ("v0.41", "H_Phantom_LongPersistence (descriptive)", "verdicts/H_Phantom_LongPersistence/verdict",
     [("retained", "verdicts/H_Phantom_LongPersistence/pooled/retained_t3"),
      ("t2_phantom", "verdicts/H_Phantom_LongPersistence/pooled/t2_phantom"),
      ("proportion", "verdicts/H_Phantom_LongPersistence/pooled/proportion")]),
    ("v1.9", "H_Presence_Score_Reliability (primary)", "verdicts/H_Presence_Score_Reliability/verdict",
     [("rho", "verdicts/H_Presence_Score_Reliability/rho"), ("p_perm", "verdicts/H_Presence_Score_Reliability/p_perm"),
      ("n", "verdicts/H_Presence_Score_Reliability/n")]),
    ("v1.9", "H_Dissociation_t3 (primary)", "verdicts/H_Dissociation_t3/verdict",
     [("rho", "verdicts/H_Dissociation_t3/rho"), ("n", "verdicts/H_Dissociation_t3/n")]),
    ("v1.9", "H_Consistency_Reliability (primary)", "verdicts/H_Consistency_Reliability/verdict",
     [("rho", "verdicts/H_Consistency_Reliability/rho"), ("n", "verdicts/H_Consistency_Reliability/n"),
      ("p_frame", "verdicts/H_Consistency_Reliability/frame_structure_null/p_frame")]),
    ("v1.9", "H_NoComposite_t3 (descriptive)", "verdicts/H_NoComposite_t3/verdict",
     [("rho_A_P", "verdicts/H_NoComposite_t3/rho_A_P"), ("n", "verdicts/H_NoComposite_t3/n")]),
    ("AIAS 2.0", "section-5 class (from v1.9 + v0.41 verdicts)", "class/class",
     [("flags", "class/flags"), ("rho(C*,P) t1", "summaries/t1/rho_Cstar_P"),
      ("rho(C*,P) t2", "summaries/t2/rho_Cstar_P"), ("rho(C*,P) t3", "summaries/t3/rho_Cstar_P"),
      ("share not rated t3", "summaries/t3/share_not_rated"),
      ("retest C* t2->t3", "descriptive_retest_t2_t3/C_star/0"), ("retest P t2->t3", "descriptive_retest_t2_t3/P/0")]),
    ("v0.34", "H_CPC_Temporal_Stability (primary)", "verdicts/H_CPC_Temporal_Stability/verdict",
     [("substrates rho>=0.70", "verdicts/H_CPC_Temporal_Stability/n_conf_ge070"),
      ("substrates rho<0.50", "verdicts/H_CPC_Temporal_Stability/n_fals_lt050")] +
     [(f"rho {s}", f"verdicts/H_CPC_Temporal_Stability/per_substrate_rho/{s}")
      for s in ("v0.19", "v0.20", "v0.21", "v0.22", "v0.23")]),
    ("v0.34", "H_CPC_Drift_Beyond_Presence (primary gate)", "verdicts/H_CPC_Drift_Beyond_Presence/verdict",
     [("non-flagged substrates", "verdicts/H_CPC_Drift_Beyond_Presence/nonflagged_substrates"),
      ("residual rho>=0.50", "verdicts/H_CPC_Drift_Beyond_Presence/n_resid_ge050"),
      ("residual rho v0.19", "verdicts/H_CPC_Drift_Beyond_Presence/per_substrate_residual_rho/v0.19")]),
    ("v0.34", "H_Presence_Temporal_Stability (secondary)", "verdicts/H_Presence_Temporal_Stability/verdict",
     [("substrates rho>=0.80", "verdicts/H_Presence_Temporal_Stability/n_conf_ge080"),
      ("substrates rho<0.60", "verdicts/H_Presence_Temporal_Stability/n_fals_lt060")] +
     [(f"rho {s}", f"verdicts/H_Presence_Temporal_Stability/per_substrate_rho/{s}")
      for s in ("v0.19", "v0.20", "v0.21", "v0.22", "v0.23")]),
    ("v0.34", "H_Phantom_Temporal_Persistence (descriptive)", "verdicts/H_Phantom_Temporal_Persistence/verdict",
     [(f"{s} retained/t1", f"verdicts/H_Phantom_Temporal_Persistence/per_substrate/{s}/retained_t2")
      for s in ("v0.19", "v0.23")] +
     [(f"{s} t1 phantom", f"verdicts/H_Phantom_Temporal_Persistence/per_substrate/{s}/t1_phantom")
      for s in ("v0.19", "v0.23")]),
    ("v1.8", "H_CV_Reproduces", "verdicts/H_CV_Reproduces/verdict",
     [("rho", "verdicts/H_CV_Reproduces/stat/rho"), ("n", "verdicts/H_CV_Reproduces/stat/n")]),
    ("v1.8", "H_MeanIndependent (make-or-break)", "verdicts/H_MeanIndependent/verdict",
     [("pooled rho", "verdicts/H_MeanIndependent/stat/pooled/rho"), ("n", "verdicts/H_MeanIndependent/stat/pooled/n")]),
    ("v1.8", "H_LowRecallDefined", "verdicts/H_LowRecallDefined/verdict",
     [("gain set", "verdicts/H_LowRecallDefined/stat/gain_set_size"),
      ("phi-defined / >=1-surfacing", "verdicts/H_LowRecallDefined/stat/phi_defined"),
      ("n_nonzero", "verdicts/H_LowRecallDefined/stat/n_nonzero_surfacing"),
      ("CPC_raw-defined", "verdicts/H_LowRecallDefined/stat/cv_raw_defined"),
      ("brands at pi_hat=1 ceiling", "verdicts/H_LowRecallDefined/stat/n_saturated_ceiling")]),
    ("v1.8", "H_GradedRecognition", "verdicts/H_GradedRecognition/verdict", []),
    ("v1.8", "H_PositionalDissociation", "verdicts/H_PositionalDissociation/verdict",
     [("rho(phi,J)", "verdicts/H_PositionalDissociation/stat/rho"), ("n", "verdicts/H_PositionalDissociation/stat/n"),
      ("discordant", "verdicts/H_PositionalDissociation/stat/n_discordant_union")]),
    ("v1.8", "H_PhantomSignature (exploratory)", "verdicts/H_PhantomSignature/verdict",
     [("phantoms phi-defined", "verdicts/H_PhantomSignature/stat/n_phantom_defined")]),
    ("v1.8", "two-wave phi t1-t2 agreement (descriptive; v0.41 gate P2 reference)", None,
     [("rho", "two_wave_reproducibility/phi_t1_t2_rank_agreement/rho"),
      ("n", "two_wave_reproducibility/phi_t1_t2_rank_agreement/n")]),
]


def main():
    out = []
    for study, test, vkey, stats in TESTS:
        recs = [json.load(open(p)) for p in FILES[study]]
        row = {"study": study, "test": test}
        for lab, rec in zip(("locked", "a", "b"), recs):
            row[f"{lab}_verdict"] = "DESCRIPTIVE (no verdict)" if vkey is None else str(g(rec, vkey)).split(" (")[0]
            row[f"{lab}_statistics"] = "; ".join(f"{n}={fmt(g(rec, k))}" for n, k in stats)
        row["verdict_changes"] = "yes" if len({row["locked_verdict"], row["a_verdict"], row["b_verdict"]}) > 1 else "no"
        row["files"] = " | ".join(str(p) for p in FILES[study])
        out.append(row)
    with open(R / "verdict_table.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    for r in out:
        print(f"{r['study']:8} {r['test']:45} {r['locked_verdict']:10} {r['a_verdict']:10} {r['b_verdict']:10} change={r['verdict_changes']}")
        print(f"         L: {r['locked_statistics']}\n         a: {r['a_statistics']}\n         b: {r['b_statistics']}")


if __name__ == "__main__":
    main()
