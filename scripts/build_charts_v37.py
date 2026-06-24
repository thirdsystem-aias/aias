#!/usr/bin/env python3
"""
v0.37 Identity-Load (IL-Direct) × CPC — figure builder (register-neutral).

THREE confirmatory figures for a powered-null / dissociation result (a null does
NOT get a positive finding's figure set):

  chart_02_precise_null       primary rho vs the detectable-effect threshold —
                              the visual answer to "underpowered?" (it was not)
  chart_03_dissociation       IL → Presence (v1.6, cell-level) vs IL → phi-Consistency
                              (v0.37, brand-level): same moderator, opposite outcomes.
                              CROSS-PHASE — annotated + visually seamed, never one analysis.
  chart_01_floor_not_ceiling  recognition (C_P) × recall (pi_hat): the excluded units
                              are recognized-but-unrecalled (floor, not ceiling).

SSOT: osf/v37/v37_verdicts.json — every plotted number, EXCEPT two labelled inputs:
  - Fig 2 Presence-side delta  ← v1.6 H_IdentityLoad_Direct (cross-phase; SSRN ID pending)
  - Fig 3 C_P recognition axis ← osf/methodology/v1_7/data/v1_7_cpc.csv (dual-source)
Both carry explicit in-figure source notes; neither is from the verdicts file.

Outputs reports/figs/v37/chart_0N_*.pdf (+ _preview.png), copied to osf/v37/figures/.
"""
import sys, json, csv, shutil
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path.home() / "aias"
sys.path.insert(0, str(ROOT / "scripts"))
import chart_style as cs
cs.setup()

SOURCE_PHASE = "v0.37 (Identity-Load × CPC)"
PROTOCOL = "v0.37-prereg-r2"
FIG_DIR = ROOT / "reports/figs/v37"
DEPOSIT_DIR = ROOT / "osf/v37/figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)
DEPOSIT_DIR.mkdir(parents=True, exist_ok=True)

LO, HI = 0.15, 0.30  # locked verdict thresholds (v0.37-prereg-r2)

# ---- SSOT: v37 verdicts file --------------------------------------------- #
V = json.load(open(ROOT / "osf/v37/v37_verdicts.json"))
VD = V["verdicts"]
PRI = VD["H_IL_Consistency"]
PAR = VD["H_IL_Presence_Robustness"]
RN = PRI["realized_n"]
FORK = RN["fork_a_saturation_diagnostic"]
TRIO = ["v0.20", "v0.21", "v0.22"]
CAT = {"v0.20": "skincare", "v0.21": "cosmetics", "v0.22": "automotive"}

RHO = PRI["stat"]["rho"]
P_PERM = PRI["stat"]["p_perm"]
N = PRI["stat"]["n"]
RHO_P = PAR["stat"]["rho_partial"]
P_PERM_P = PAR["stat"]["p_perm"]
# detectable effect: critical two-sided Spearman |rho| at p=.05 (= the 1.96/sqrt(n-1)
# band-coherence quantity the n-floor was derived from). At n it is < 0.30, so a
# CONFIRMED-band effect was REACHABLE. It is also the analytic 95% CI half-width.
RHO_CRIT = 1.96 / np.sqrt(N - 1)

N_FLOOR = sum(FORK[s]["n_zero_floor"] for s in TRIO)          # 19 true-zeros
N_CEIL = sum(FORK[s]["n_saturation_ceiling"] for s in TRIO)   # 0 ceiling
N_ANALY = sum(FORK[s]["n_analyzable"] for s in TRIO)          # 53

# ---- cross-phase constant (NOT from verdicts file) ----------------------- #
# v1.6 H_IdentityLoad_Direct, v0.21 Cell B: delta = mean(R_cult) - mean(R_cat).
# A DIFFERENT phase, DIFFERENT granularity (cell, not brand). SSRN ID pending.
V16_DELTA, V16_CILO, V16_CIHI = 7.12, 4.75, 10.25
V16_NOTE = "v1.6 H_IdentityLoad_Direct · v0.21 Cell B · cell-level · SSRN ID pending verification"


def load_cp_pi():
    """Fig 3 recognition axis (dual-source): per-brand C_P + pi_hat for the trio,
    from osf/methodology/v1_7/data/v1_7_cpc.csv (NOT the verdicts file)."""
    rows = []
    for r in csv.DictReader(open(ROOT / "osf/methodology/v1_7/data/v1_7_cpc.csv")):
        if r["substrate"] in CAT:
            pi = sum(json.loads(r["r_per_model"])) / 36.0
            rows.append({"cp": float(r["C_P"]), "pi": pi, "excluded": pi <= 0.0})
    return rows


def pfmt(p):
    return "p < 0.0001" if p < 1e-4 else f"p = {p:.3f}"


def _save(fig, fname, verdict):
    cs.add_footer(fig, verdict=verdict, phase=SOURCE_PHASE, protocol=PROTOCOL)
    fig.savefig(FIG_DIR / f"{fname}.pdf", **cs.SAVEFIG_PARAMS)
    fig.savefig(FIG_DIR / f"{fname}_preview.png", dpi=130, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    print(f"  wrote {fname}.pdf")


# ============================================================ chart_01
def chart_02_precise_null():
    """Detectable-effect threshold FOREGROUNDED; near-zero estimate with a CI that
    excludes the CONFIRMED band -> precise null, not silent."""
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    ax.axvspan(-LO, LO, color=cs.PALETTE["gray_light"], alpha=0.28, zorder=0)
    ax.axvline(0.0, color=cs.GRAY, lw=1.0, zorder=1)
    # FOREGROUNDED reference marks — these carry the "powered" message
    # reference lines CAPPED below the label row (no strike-through)
    for xv in (-HI, HI):
        ax.vlines(xv, -1.0, 1.0, color=cs.INDIGO, lw=1.6, ls="--", zorder=2)
    for xv in (-RHO_CRIT, RHO_CRIT):
        ax.vlines(xv, -1.0, 1.0, color=cs.WARM, lw=1.4, ls=":", zorder=2)
    # band labels — top row, horizontally separated; detectable note on its own row
    ax.text(0.0, 1.58, f"FALSIFIED |ρ|<{LO:.2f}", ha="center", va="bottom",
            fontsize=7.2, color=cs.GRAY)
    ax.text(HI, 1.58, f"CONFIRMED |ρ| >= {HI:.2f}", ha="center", va="bottom",
            fontsize=7.6, color=cs.INDIGO, fontweight="bold")
    ax.text(0.0, 1.16, f"detectable effect reachable — critical |ρ|≈{RHO_CRIT:.2f} at p=.05 (n={N})",
            ha="center", va="bottom", fontsize=7.2, color=cs.WARM, fontweight="bold")
    # observed estimate with analytic 95% CI (half-width = critical |rho|)
    ax.errorbar(RHO, 0, xerr=RHO_CRIT, fmt="o", ms=11, color=cs.BLACK,
                ecolor=cs.BLACK, elinewidth=2.0, capsize=5, capthick=2.0, zorder=4)
    ax.text(RHO, -0.42, f"observed ρ(IL-Direct, φ) = {RHO:+.3f}   ({pfmt(P_PERM)})",
            ha="center", va="top", fontsize=8.6, color=cs.BLACK, fontweight="bold")
    ax.text(RHO, -0.74,
            f"95% CI [{RHO-RHO_CRIT:+.2f}, {RHO+RHO_CRIT:+.2f}] excludes the ±{HI:.2f} CONFIRMED band",
            ha="center", va="top", fontsize=7.6, color=cs.GRAY, fontstyle="italic")
    ax.set_xlim(-0.46, 0.46); ax.set_ylim(-1.05, 1.95)
    ax.set_yticks([]); ax.set_xticks([-0.4, -0.3, -0.15, 0, 0.15, 0.3, 0.4])
    ax.tick_params(labelsize=7.4)
    ax.set_xlabel("pooled within-substrate Spearman ρ(IL-Direct, φ)", fontsize=9)
    fig.subplots_adjust(top=0.78, bottom=0.26, left=0.05, right=0.97)
    cs.add_header(fig, "A precise null, not an absence of power",
                  f"The primary association against the detectable-effect threshold (n = {N}, above the floor of 45).",
                  "The critical |ρ| at p=.05 (≈0.27) is below the 0.30 CONFIRMED band — a band-level effect was reachable. The estimate sits at ~0 and its CI excludes the band.")
    _save(fig, "chart_02_precise_null",
          f"H_IL_Consistency FALSIFIED → CLEAN-NULL: ρ={RHO:+.3f}, {pfmt(P_PERM)}, n={N}; powered (detectable |ρ|≈{RHO_CRIT:.2f} < 0.30).")


# ============================================================ chart_02
def chart_03_dissociation():
    """Cross-phase paired panels — DISTINCT axes/units + a visual seam, so it can
    never read as one within-study analysis."""
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.8, 4.4))
    # --- LEFT: IL -> Presence (v1.6, cell-level) — delta-count axis -------- #
    axL.axhline(0.0, color=cs.GRAY, lw=1.0, zorder=1)
    axL.errorbar(0, V16_DELTA, yerr=[[V16_DELTA - V16_CILO], [V16_CIHI - V16_DELTA]],
                 fmt="o", ms=12, color=cs.INDIGO, ecolor=cs.INDIGO, elinewidth=2.2,
                 capsize=6, capthick=2.2, zorder=4)
    axL.text(0, V16_DELTA + 0.8, f"δ = {V16_DELTA:+.2f}\nCI [{V16_CILO:+.2f}, {V16_CIHI:+.2f}]",
             ha="center", va="bottom", fontsize=8.4, color=cs.INDIGO, fontweight="bold")
    axL.text(0, -1.4, "CONFIRMED — effect away from 0", ha="center", va="top",
             fontsize=8.0, color=cs.INDIGO, fontweight="bold")
    axL.set_xlim(-1, 1); axL.set_ylim(-2.5, 12.5); axL.set_xticks([])
    axL.set_ylabel("δ = mean(R_cult) − mean(R_cat)   [recall counts]", fontsize=8.2)
    axL.set_title("IL → Presence", fontsize=9.5, fontweight="bold", color=cs.INDIGO, pad=14)
    axL.text(0.5, 1.045, "v1.6 · cell-level · different phase", transform=axL.transAxes,
             ha="center", va="bottom", fontsize=7.0, color=cs.GRAY, fontstyle="italic")
    # --- RIGHT: IL -> phi-Consistency (v0.37, brand-level) — rho axis ------ #
    axR.axhline(0.0, color=cs.GRAY, lw=1.0, zorder=1)
    for yv in (-HI, HI):
        axR.axhline(yv, color=cs.GRAY, lw=0.8, ls="--", zorder=1)
    axR.scatter([0], [RHO], s=120, color=cs.BLACK, zorder=4)
    axR.scatter([0], [RHO_P], s=90, facecolor="white", edgecolor=cs.BLACK, linewidth=1.6, zorder=4)
    axR.text(0.12, RHO, f"raw {RHO:+.3f}", va="center", ha="left", fontsize=8.0, color=cs.BLACK)
    axR.text(0.12, RHO_P + 0.06, f"partial {RHO_P:+.3f}", va="center", ha="left", fontsize=8.0, color=cs.GRAY)
    axR.text(0, -0.40, "FALSIFIED → CLEAN-NULL — at 0", ha="center", va="top",
             fontsize=8.0, color=cs.BLACK, fontweight="bold")
    axR.text(0.0, HI + 0.01, f"±{HI:.2f} CONFIRMED band", ha="center", va="bottom",
             fontsize=6.8, color=cs.GRAY)
    axR.set_xlim(-0.6, 0.9); axR.set_ylim(-0.5, 0.5); axR.set_xticks([])
    axR.set_ylabel("Spearman ρ(IL-Direct, φ)", fontsize=8.2)
    axR.set_title("IL → φ-Consistency", fontsize=9.5, fontweight="bold", color=cs.BLACK, pad=14)
    axR.text(0.5, 1.045, "v0.37 · brand-level · this phase", transform=axR.transAxes,
             ha="center", va="bottom", fontsize=7.0, color=cs.GRAY, fontstyle="italic")
    # --- the visual seam: a dashed divider down the figure middle --------- #
    fig.subplots_adjust(top=0.74, bottom=0.18, left=0.10, right=0.97, wspace=0.42)
    fig.add_artist(plt.Line2D([0.525, 0.525], [0.20, 0.74], color=cs.WARM, lw=1.0,
                              ls=(0, (4, 3)), transform=fig.transFigure))
    fig.text(0.525, 0.165, "different measurement · not one analysis", ha="center", va="top",
             fontsize=6.8, color=cs.WARM, fontstyle="italic")
    cs.add_header(fig, "Identity load moves Presence, not Consistency — across the same trio",
                  "A confirmed Presence-side moderator (left) set against a powered Consistency null (right).",
                  f"Left input is cross-phase: {V16_NOTE}. Right is this phase (v37_verdicts.json).")
    _save(fig, "chart_03_dissociation",
          "Component dissociation: IL-Direct CONFIRMED on Presence (v1.6) and FALSIFIED→CLEAN-NULL on φ-Consistency (v0.37).")


# ============================================================ chart_03
def chart_01_floor_not_ceiling():
    """Recognition (C_P) × recall (pi_hat). Excluded true-zeros cluster at high C_P,
    zero recall — recognized but unrecalled. Dual-source (C_P ← v1_7_cpc.csv)."""
    rows = load_cp_pi()
    excl = [r for r in rows if r["excluded"]]
    analy = [r for r in rows if not r["excluded"]]
    # GUARD: plotted C_P split must match §3.1 (16/19 at 6/6, 17/19 ≥5) and the verdicts counts
    n_excl_cp6 = sum(1 for r in excl if r["cp"] >= 5.999)
    n_excl_cp_ge5 = sum(1 for r in excl if r["cp"] >= 5)
    assert len(excl) == N_FLOOR, f"excluded {len(excl)} != verdicts floor {N_FLOOR}"
    assert len(analy) == N_ANALY, f"analyzable {len(analy)} != verdicts {N_ANALY}"
    assert n_excl_cp6 == 16 and n_excl_cp_ge5 == 17, \
        f"C_P split {n_excl_cp6}/{n_excl_cp_ge5} != §3.1's 16/17 — figure/text would disagree"

    rng = np.random.default_rng(370037)
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    ax.axhspan(-0.02, 0.02, color=cs.WARM, alpha=0.12, zorder=0)
    ax.axhline(1.0, color=cs.GRAY, lw=0.9, ls="--", zorder=1)
    ax.text(6.55, 1.0, f"saturation ceiling (π̂=1): {N_CEIL} brands", va="bottom", ha="right",
            fontsize=7.4, color=cs.GRAY, fontstyle="italic")
    for r in analy:
        jx = (rng.random() - 0.5) * 0.28
        ax.scatter(r["cp"] + jx, r["pi"], s=26, color=cs.INDIGO, alpha=0.75,
                   edgecolor="white", linewidth=0.3, zorder=3)
    for r in excl:
        jx = (rng.random() - 0.5) * 0.28
        ax.scatter(r["cp"] + jx, 0.0, s=46, marker="X", color=cs.WARM,
                   edgecolor="white", linewidth=0.4, zorder=4)
    ax.text(6.0, 0.05,
            f"{N_FLOOR} excluded at recall floor (π̂=0) — {n_excl_cp6}/{N_FLOOR} at C_P=6/6:\nrecognized by all six models, recalled by none",
            ha="right", va="bottom", fontsize=7.6, color=cs.WARM, fontweight="bold")
    h_an = plt.Line2D([], [], marker="o", ls="", color=cs.INDIGO, label=f"analyzable (φ defined), n={N_ANALY}", ms=6)
    h_ex = plt.Line2D([], [], marker="X", ls="", color=cs.WARM, label=f"excluded true-zero (π̂=0), n={N_FLOOR}", ms=7)
    ax.legend(handles=[h_an, h_ex], loc="upper left", fontsize=7.4, framealpha=0.9)
    ax.set_xlim(-0.4, 6.6); ax.set_ylim(-0.06, 1.10)
    ax.set_xticks([0, 1, 2, 3, 4, 5, 6]); ax.tick_params(labelsize=7.6)
    ax.set_xlabel("recognition  C_P  (0–6, count of models recognizing the brand)", fontsize=9)
    ax.set_ylabel("recall  π̂  (surfacing rate, 0–1)", fontsize=9)
    fig.subplots_adjust(top=0.78, bottom=0.20, left=0.085, right=0.97)
    cs.add_header(fig, "The saturation bit at the recall floor, not the φ ceiling",
                  "Recognition × recall for the 72 trio brands; the pre-registration expected a ceiling exclusion.",
                  "Fork-A counts & IL-means: v37_verdicts.json. Recognition axis (C_P): osf/methodology/v1_7/data/v1_7_cpc.csv (dual-source).")
    _save(fig, "chart_01_floor_not_ceiling",
          f"Attrition floor-driven: {N_FLOOR} true-zeros excluded, {N_CEIL} at ceiling; the excluded are recognized-but-unrecalled.")


def main():
    chart_01_floor_not_ceiling()
    chart_02_precise_null()
    chart_03_dissociation()
    for pdf in sorted(FIG_DIR.glob("chart_0*.pdf")):
        shutil.copy(pdf, DEPOSIT_DIR / pdf.name)
        print(f"  deposited {pdf.name}")


if __name__ == "__main__":
    main()
