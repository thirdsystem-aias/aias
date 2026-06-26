#!/usr/bin/env python3
"""
v0.37 Identity-Load (IL-Direct) × CPC — DUAL-REGISTER figure builder.

Two registers from one pipeline (v0.34 dual-register pattern):

  paper  -> reports/figs/v37/        chart_0N_<topic>.pdf   (academic: ρ, φ, H_*, the
            confirmatory set the SSRN paper references; FROZEN, do not alter bodies)
  report -> reports/figs/v37/report/ report_fig_0N_<topic>.pdf  (managerial: academic
            VOCABULARY translated to plain language — but the quantitative SCAFFOLD
            retained, the cross-phase seam intact, provenance kept in plain form)

The report register goes deeper than v0.34 (which translated only the footer): our
two-register discipline forbids academic VOICE in the managerial deck, not merely the
H_ footer label. So in report mode the chart BODIES translate too — ρ→"association",
φ→"consistency", H_IdentityLoad_Direct→gone, "FALSIFIED→CLEAN-NULL"→"no effect",
"CONFIRMED band"→"a real-effect size" — while the numbers (−0.008, the detectable
threshold mark, the ±scale) STAY, because the scaffold is what makes the powered null
credible. Translate the words, keep the evidence.

Paper register (P1 confirmatory set, 3 figures):
  chart_01_floor_not_ceiling  recognition × recall; excluded units recognized-not-recalled
  chart_02_precise_null       estimate vs the detectable-effect threshold (powered)
  chart_03_dissociation       IL→Presence (v1.6, cell) vs IL→φ (v0.37, brand): cross-phase

Report register (4 figures — adds the report-only cross-substrate descriptive):
  report_fig_01_dissociation  identity moves visibility, not consistency (P1)
  report_fig_02_precise_null  a real absence, not a weak test (P2)
  report_fig_03_cross_substrate  no category is the exception (P3) — report-only
  report_fig_04_floor         recognized, but never named (P4)

SSOT: osf/v37/v37_verdicts.json — every plotted number, EXCEPT two labelled inputs:
  - dissociation Presence-side delta ← v1.6 H_IdentityLoad_Direct (cross-phase)
  - floor recognition axis           ← osf/methodology/v1_7/data/v1_7_cpc.csv (dual-source)
Both carry explicit in-figure source notes (plain-language in report register).
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
REPORT_DIR = FIG_DIR / "report"
DEPOSIT_DIR = ROOT / "osf/v37/figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)
DEPOSIT_DIR.mkdir(parents=True, exist_ok=True)

OUT = {"paper": FIG_DIR, "report": REPORT_DIR}
MODE = "paper"   # set by main(); selects register (filenames + footer + body vocabulary)

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
RHO_CRIT = 1.96 / np.sqrt(N - 1)   # detectable |rho| at p=.05; also the 95% CI half-width

N_FLOOR = sum(FORK[s]["n_zero_floor"] for s in TRIO)          # 19 true-zeros
N_CEIL = sum(FORK[s]["n_saturation_ceiling"] for s in TRIO)   # 0 ceiling
N_ANALY = sum(FORK[s]["n_analyzable"] for s in TRIO)          # 53

# ---- cross-phase constant (NOT from verdicts file) ----------------------- #
V16_DELTA, V16_CILO, V16_CIHI = 7.12, 4.75, 10.25
V16_NOTE = "v1.6 H_IdentityLoad_Direct · v0.21 Cell B · cell-level · SSRN ID pending verification"


def load_cp_pi():
    """Floor figure recognition axis (dual-source): per-brand C_P + pi_hat for the trio,
    from osf/methodology/v1_7/data/v1_7_cpc.csv (NOT the verdicts file)."""
    rows = []
    for r in csv.DictReader(open(ROOT / "osf/methodology/v1_7/data/v1_7_cpc.csv")):
        if r["substrate"] in CAT:
            pi = sum(json.loads(r["r_per_model"])) / 36.0
            rows.append({"cp": float(r["C_P"]), "pi": pi, "excluded": pi <= 0.0})
    return rows


def pfmt(p):
    return "p < 0.0001" if p < 1e-4 else f"p = {p:.3f}"


def _save(fig, fname_paper, fname_report, verdict_paper, verdict_report):
    fname = fname_paper if MODE == "paper" else fname_report
    verdict = verdict_paper if MODE == "paper" else verdict_report
    outdir = OUT[MODE]
    cs.add_footer(fig, verdict=verdict, phase=SOURCE_PHASE, protocol=PROTOCOL)
    fig.savefig(outdir / f"{fname}.pdf", **cs.SAVEFIG_PARAMS)
    fig.savefig(outdir / f"{fname}_preview.png", dpi=130, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    print(f"  [{MODE}] wrote {fname}.pdf")


# ============================================================ precise null (P2)
def chart_02_precise_null():
    """Detectable-effect threshold FOREGROUNDED; near-zero estimate with a CI that
    excludes the real-effect band -> a precise, powered null, not a silent one.
    Report register: same number line + threshold marks (scaffold kept), academic
    vocabulary (ρ/φ/FALSIFIED/CONFIRMED) translated to plain language."""
    R = MODE == "report"
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    ax.axvspan(-LO, LO, color=cs.PALETTE["gray_light"], alpha=0.28, zorder=0)
    ax.axvline(0.0, color=cs.GRAY, lw=1.0, zorder=1)
    for xv in (-HI, HI):          # the real-effect threshold
        ax.vlines(xv, -1.0, 1.0, color=cs.INDIGO, lw=1.6, ls="--", zorder=2)
    for xv in (-RHO_CRIT, RHO_CRIT):   # the within-reach (detectable) mark
        ax.vlines(xv, -1.0, 1.0, color=cs.WARM, lw=1.4, ls=":", zorder=2)
    # top band labels
    if R:
        ax.text(0.0, 1.58, "no measurable effect", ha="center", va="bottom",
                fontsize=7.2, color=cs.GRAY)
        ax.text(HI, 1.58, "a real-effect size", ha="center", va="bottom",
                fontsize=7.6, color=cs.INDIGO, fontweight="bold")
        ax.text(0.0, 1.16, f"an effect this big was well within reach ({N} brands)",
                ha="center", va="bottom", fontsize=7.2, color=cs.WARM, fontweight="bold")
    else:
        ax.text(0.0, 1.58, f"FALSIFIED |ρ|<{LO:.2f}", ha="center", va="bottom",
                fontsize=7.2, color=cs.GRAY)
        ax.text(HI, 1.58, f"CONFIRMED |ρ| >= {HI:.2f}", ha="center", va="bottom",
                fontsize=7.6, color=cs.INDIGO, fontweight="bold")
        ax.text(0.0, 1.16, f"detectable effect reachable — critical |ρ|≈{RHO_CRIT:.2f} at p=.05 (n={N})",
                ha="center", va="bottom", fontsize=7.2, color=cs.WARM, fontweight="bold")
    # observed estimate with analytic 95% CI (half-width = critical |rho|) — SCAFFOLD
    ax.errorbar(RHO, 0, xerr=RHO_CRIT, fmt="o", ms=11, color=cs.BLACK,
                ecolor=cs.BLACK, elinewidth=2.0, capsize=5, capthick=2.0, zorder=4)
    if R:
        ax.text(RHO, -0.42, f"measured association = {RHO:+.3f}   (essentially zero)",
                ha="center", va="top", fontsize=8.6, color=cs.BLACK, fontweight="bold")
        ax.text(RHO, -0.74, "the range of uncertainty stays short of a real-effect size",
                ha="center", va="top", fontsize=7.6, color=cs.GRAY, fontstyle="italic")
        ax.set_xlabel("association between identity load and cross-model consistency  (−1 to +1)", fontsize=9)
    else:
        ax.text(RHO, -0.42, f"observed ρ(IL-Direct, φ) = {RHO:+.3f}   ({pfmt(P_PERM)})",
                ha="center", va="top", fontsize=8.6, color=cs.BLACK, fontweight="bold")
        ax.text(RHO, -0.74,
                f"95% CI [{RHO-RHO_CRIT:+.2f}, {RHO+RHO_CRIT:+.2f}] excludes the ±{HI:.2f} CONFIRMED band",
                ha="center", va="top", fontsize=7.6, color=cs.GRAY, fontstyle="italic")
        ax.set_xlabel("pooled within-substrate Spearman ρ(IL-Direct, φ)", fontsize=9)
    ax.set_xlim(-0.46, 0.46); ax.set_ylim(-1.05, 1.95)
    ax.set_yticks([]); ax.set_xticks([-0.4, -0.3, -0.15, 0, 0.15, 0.3, 0.4])
    ax.tick_params(labelsize=7.4)
    fig.subplots_adjust(top=0.78, bottom=0.26, left=0.05, right=0.97)
    if R:
        cs.add_header(fig, "A real absence, not a weak test",
                      f"The measured association against the size of effect this test could have caught ({N} brands).",
                      "An effect big enough to matter was within reach — the estimate still sits at zero.")
    else:
        cs.add_header(fig, "A precise null, not an absence of power",
                      f"The primary association against the detectable-effect threshold (n = {N}, above the floor of 45).",
                      "The critical |ρ| at p=.05 (≈0.27) is below the 0.30 CONFIRMED band — a band-level effect was reachable. The estimate sits at ~0 and its CI excludes the band.")
    _save(fig, "chart_02_precise_null", "report_fig_02_precise_null",
          f"H_IL_Consistency FALSIFIED → CLEAN-NULL: ρ={RHO:+.3f}, {pfmt(P_PERM)}, n={N}; powered (detectable |ρ|≈{RHO_CRIT:.2f} < 0.30).",
          f"P2 — a real absence: the measured association is essentially zero ({RHO:+.3f}), and an effect big enough to matter was well within the test's reach ({N} brands).")


# ============================================================ dissociation (P1)
def chart_03_dissociation():
    """Cross-phase paired panels — DISTINCT axes/units + a visual seam, so it can never
    read as one within-study analysis. Report register translates the vocabulary but
    KEEPS the cross-phase seam in plain language (the honest bound is the same in both
    registers; only the words change)."""
    R = MODE == "report"
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.8, 4.4))
    # --- LEFT: Identity -> Presence/Visibility (v1.6, cell-level) ---------- #
    axL.axhline(0.0, color=cs.GRAY, lw=1.0, zorder=1)
    axL.errorbar(0, V16_DELTA, yerr=[[V16_DELTA - V16_CILO], [V16_CIHI - V16_DELTA]],
                 fmt="o", ms=12, color=cs.INDIGO, ecolor=cs.INDIGO, elinewidth=2.2,
                 capsize=6, capthick=2.2, zorder=4)
    if R:
        axL.text(0, V16_DELTA + 0.8, f"+{V16_DELTA:.1f}\n(clearly above zero)",
                 ha="center", va="bottom", fontsize=8.4, color=cs.INDIGO, fontweight="bold")
        axL.text(0, -1.4, "a clear, confirmed effect", ha="center", va="top",
                 fontsize=8.0, color=cs.INDIGO, fontweight="bold")
        axL.set_ylabel("how much more identity-led brands get named  [naming counts]", fontsize=8.2)
        axL.set_title("Identity → Visibility", fontsize=9.5, fontweight="bold", color=cs.INDIGO, pad=14)
        axL.text(0.5, 1.045, "from earlier work · whether AI names a brand", transform=axL.transAxes,
                 ha="center", va="bottom", fontsize=7.0, color=cs.GRAY, fontstyle="italic")
    else:
        axL.text(0, V16_DELTA + 0.8, f"δ = {V16_DELTA:+.2f}\nCI [{V16_CILO:+.2f}, {V16_CIHI:+.2f}]",
                 ha="center", va="bottom", fontsize=8.4, color=cs.INDIGO, fontweight="bold")
        axL.text(0, -1.4, "CONFIRMED — effect away from 0", ha="center", va="top",
                 fontsize=8.0, color=cs.INDIGO, fontweight="bold")
        axL.set_ylabel("δ = mean(R_cult) − mean(R_cat)   [recall counts]", fontsize=8.2)
        axL.set_title("IL → Presence", fontsize=9.5, fontweight="bold", color=cs.INDIGO, pad=14)
        axL.text(0.5, 1.045, "v1.6 · cell-level · different phase", transform=axL.transAxes,
                 ha="center", va="bottom", fontsize=7.0, color=cs.GRAY, fontstyle="italic")
    axL.set_xlim(-1, 1); axL.set_ylim(-2.5, 12.5); axL.set_xticks([])
    # --- RIGHT: Identity -> Consistency (v0.37, brand-level) --------------- #
    axR.axhline(0.0, color=cs.GRAY, lw=1.0, zorder=1)
    for yv in (-HI, HI):
        axR.axhline(yv, color=cs.GRAY, lw=0.8, ls="--", zorder=1)
    axR.scatter([0], [RHO], s=120, color=cs.BLACK, zorder=4)
    axR.scatter([0], [RHO_P], s=90, facecolor="white", edgecolor=cs.BLACK, linewidth=1.6, zorder=4)
    if R:
        axR.text(0.12, RHO, f"{RHO:+.3f} measured", va="center", ha="left", fontsize=8.0, color=cs.BLACK)
        axR.text(0.12, RHO_P + 0.06, f"{RHO_P:+.3f} adjusted", va="center", ha="left", fontsize=8.0, color=cs.GRAY)
        axR.text(0, -0.40, "no effect — sits at zero", ha="center", va="top",
                 fontsize=8.0, color=cs.BLACK, fontweight="bold")
        axR.text(0.0, HI + 0.01, "a real-effect size", ha="center", va="bottom",
                 fontsize=6.8, color=cs.GRAY)
        axR.set_ylabel("association with cross-model consistency  (−1 to +1)", fontsize=8.2)
        axR.set_title("Identity → Consistency", fontsize=9.5, fontweight="bold", color=cs.BLACK, pad=14)
        axR.text(0.5, 1.045, "this study · how consistently AI names it", transform=axR.transAxes,
                 ha="center", va="bottom", fontsize=7.0, color=cs.GRAY, fontstyle="italic")
    else:
        axR.text(0.12, RHO, f"raw {RHO:+.3f}", va="center", ha="left", fontsize=8.0, color=cs.BLACK)
        axR.text(0.12, RHO_P + 0.06, f"partial {RHO_P:+.3f}", va="center", ha="left", fontsize=8.0, color=cs.GRAY)
        axR.text(0, -0.40, "FALSIFIED → CLEAN-NULL — at 0", ha="center", va="top",
                 fontsize=8.0, color=cs.BLACK, fontweight="bold")
        axR.text(0.0, HI + 0.01, f"±{HI:.2f} CONFIRMED band", ha="center", va="bottom",
                 fontsize=6.8, color=cs.GRAY)
        axR.set_ylabel("Spearman ρ(IL-Direct, φ)", fontsize=8.2)
        axR.set_title("IL → φ-Consistency", fontsize=9.5, fontweight="bold", color=cs.BLACK, pad=14)
        axR.text(0.5, 1.045, "v0.37 · brand-level · this phase", transform=axR.transAxes,
                 ha="center", va="bottom", fontsize=7.0, color=cs.GRAY, fontstyle="italic")
    axR.set_xlim(-0.6, 0.9); axR.set_ylim(-0.5, 0.5); axR.set_xticks([])
    # --- the visual seam — KEPT in both registers ------------------------- #
    fig.subplots_adjust(top=0.74, bottom=0.18, left=0.10, right=0.97, wspace=0.42)
    fig.add_artist(plt.Line2D([0.525, 0.525], [0.20, 0.74], color=cs.WARM, lw=1.0,
                              ls=(0, (4, 3)), transform=fig.transFigure))
    seam = "two different measurements · not one study" if R else "different measurement · not one analysis"
    fig.text(0.525, 0.165, seam, ha="center", va="top",
             fontsize=6.8, color=cs.WARM, fontstyle="italic")
    if R:
        cs.add_header(fig, "Identity moves visibility, not consistency",
                      "A confirmed effect on whether AI names a brand (left), set against no effect on how consistently it does (right).",
                      "Different measurements from different studies, shown side by side — not one analysis. The visibility finding is from earlier work; the consistency finding is from this study.")
    else:
        cs.add_header(fig, "Identity load moves Presence, not Consistency — across the same trio",
                      "A confirmed Presence-side moderator (left) set against a powered Consistency null (right).",
                      f"Left input is cross-phase: {V16_NOTE}. Right is this phase (v37_verdicts.json).")
    _save(fig, "chart_03_dissociation", "report_fig_01_dissociation",
          "Component dissociation: IL-Direct CONFIRMED on Presence (v1.6) and FALSIFIED→CLEAN-NULL on φ-Consistency (v0.37).",
          "P1 — identity positioning moves whether AI names a brand (a confirmed, earlier finding) but not how consistently it does so across models (this study): two different measurements, not one.")


# ============================================================ floor (P4)
def chart_01_floor_not_ceiling():
    """Recognition × recall. Excluded units cluster at high recognition, zero recall —
    recognized but never named. Recognition axis is dual-source (a prior measurement);
    report register keeps that provenance in plain language."""
    R = MODE == "report"
    rows = load_cp_pi()
    excl = [r for r in rows if r["excluded"]]
    analy = [r for r in rows if not r["excluded"]]
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
    ceil_txt = (f"none always-named: {N_CEIL} brands" if R
                else f"saturation ceiling (π̂=1): {N_CEIL} brands")
    ax.text(6.55, 1.0, ceil_txt, va="bottom", ha="right",
            fontsize=7.4, color=cs.GRAY, fontstyle="italic")
    for r in analy:
        jx = (rng.random() - 0.5) * 0.28
        ax.scatter(r["cp"] + jx, r["pi"], s=26, color=cs.INDIGO, alpha=0.75,
                   edgecolor="white", linewidth=0.3, zorder=3)
    for r in excl:
        jx = (rng.random() - 0.5) * 0.28
        ax.scatter(r["cp"] + jx, 0.0, s=46, marker="X", color=cs.WARM,
                   edgecolor="white", linewidth=0.4, zorder=4)
    if R:
        ax.text(2.9, 0.60,
                f"{N_FLOOR} recognized but never named — {n_excl_cp6} of {N_FLOOR}\nknown to all six models, yet named by none",
                ha="center", va="center", fontsize=7.6, color=cs.WARM, fontweight="bold")
        h_an = plt.Line2D([], [], marker="o", ls="", color=cs.INDIGO, label=f"scored for consistency, {N_ANALY}", ms=6)
        h_ex = plt.Line2D([], [], marker="X", ls="", color=cs.WARM, label=f"recognized but never named, {N_FLOOR}", ms=7)
        ax.set_xlabel("how many of the six models recognize the brand  (0–6)", fontsize=9)
        ax.set_ylabel("how often the models actually name it  (0–1)", fontsize=9)
    else:
        ax.text(6.0, 0.05,
                f"{N_FLOOR} excluded at recall floor (π̂=0) — {n_excl_cp6}/{N_FLOOR} at C_P=6/6:\nrecognized by all six models, recalled by none",
                ha="right", va="bottom", fontsize=7.6, color=cs.WARM, fontweight="bold")
        h_an = plt.Line2D([], [], marker="o", ls="", color=cs.INDIGO, label=f"analyzable (φ defined), n={N_ANALY}", ms=6)
        h_ex = plt.Line2D([], [], marker="X", ls="", color=cs.WARM, label=f"excluded true-zero (π̂=0), n={N_FLOOR}", ms=7)
        ax.set_xlabel("recognition  C_P  (0–6, count of models recognizing the brand)", fontsize=9)
        ax.set_ylabel("recall  π̂  (surfacing rate, 0–1)", fontsize=9)
    ax.legend(handles=[h_an, h_ex], loc="upper left", fontsize=7.4, framealpha=0.9)
    ax.set_xlim(-0.4, 6.6); ax.set_ylim(-0.06, 1.10)
    ax.set_xticks([0, 1, 2, 3, 4, 5, 6]); ax.tick_params(labelsize=7.6)
    fig.subplots_adjust(top=0.78, bottom=0.20, left=0.085, right=0.97)
    if R:
        cs.add_header(fig, "Recognized, but never named",
                      "How many models know each brand (across) vs how often they name it (up).",
                      "Recognition data is from an earlier program measurement.")
    else:
        cs.add_header(fig, "The saturation bit at the recall floor, not the φ ceiling",
                      "Recognition × recall for the 72 trio brands; the pre-registration expected a ceiling exclusion.",
                      "Fork-A counts & IL-means: v37_verdicts.json. Recognition axis (C_P): osf/methodology/v1_7/data/v1_7_cpc.csv (dual-source).")
    _save(fig, "chart_01_floor_not_ceiling", "report_fig_04_floor",
          f"Attrition floor-driven: {N_FLOOR} true-zeros excluded, {N_CEIL} at ceiling; the excluded are recognized-but-unrecalled.",
          f"P4 — {N_FLOOR} of 72 brands are recognized but never named (most known to all six models); consistency can only be measured where there is naming.")


# ============================================================ cross-substrate (P3, report-only)
def report_chart_03_cross_substrate():
    """Per-category association: three categories disagree in sign, all near zero.
    REPORT-ONLY (the paper ships 3 confirmatory figures; this descriptive figure
    lives only in the managerial register — two-register figure divergence)."""
    XS = VD["H_IL_Cross_Substrate"]["per_substrate"]
    items = [(CAT[s], XS[s]["rho"], XS[s]["n"]) for s in TRIO]  # SSOT order
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    ax.axvspan(-LO, LO, color=cs.PALETTE["gray_light"], alpha=0.28, zorder=0)
    for xv in (-HI, HI):
        ax.axvline(xv, color=cs.INDIGO, lw=1.4, ls="--", zorder=1)
    ax.axvline(0.0, color=cs.GRAY, lw=1.2, zorder=2)
    ax.text(HI, len(items) - 0.34, "a real-effect size", ha="center", va="bottom",
            fontsize=7.0, color=cs.INDIGO)
    ys = list(range(len(items)))[::-1]
    for y, (name, rho, n) in zip(ys, items):
        ax.hlines(y, 0.0, rho, color=(cs.WARM if rho < 0 else cs.INDIGO), lw=2.2, zorder=3)
        ax.scatter(rho, y, s=92, color=cs.BLACK, zorder=4)
        ax.text(rho + (0.014 if rho >= 0 else -0.014), y, f"{rho:+.3f}",
                va="center", ha=("left" if rho >= 0 else "right"),
                fontsize=8.6, color=cs.BLACK, fontweight="bold")
        ax.text(0.0, y + 0.27, f"{name}  ·  {n} brands", va="bottom", ha="center",
                fontsize=8.2, color=cs.GRAY)
    ax.set_yticks([]); ax.set_ylim(-0.7, len(items) - 0.05)
    ax.set_xlim(-0.40, 0.40)
    ax.set_xticks([-0.3, -0.15, 0, 0.15, 0.3]); ax.tick_params(labelsize=7.6)
    ax.set_xlabel("association between identity load and consistency, per category  (−1 to +1)", fontsize=9)
    fig.subplots_adjust(top=0.78, bottom=0.20, left=0.05, right=0.97)
    cs.add_header(fig, "No category is the exception",
                  "Each category on its own (three categories — shown to answer the question directly, not as a statistical test).",
                  "The associations disagree in direction and all sit near zero: no overall effect, and no category-specific effect being masked.")
    _save(fig, "report_fig_03_cross_substrate", "report_fig_03_cross_substrate",
          "report-only",
          "P3 — run category by category, the three disagree in direction and all sit near zero: no overall effect, and none hiding in any single category.")


def main():
    global MODE
    # PAPER register — the 3 confirmatory figures the SSRN paper references.
    MODE = "paper"
    chart_01_floor_not_ceiling()
    chart_02_precise_null()
    chart_03_dissociation()
    for pdf in sorted(FIG_DIR.glob("chart_0*.pdf")):
        shutil.copy(pdf, DEPOSIT_DIR / pdf.name)
        print(f"  deposited {pdf.name}")
    # REPORT register — managerial-vocabulary variants + the report-only cross-substrate.
    MODE = "report"
    chart_03_dissociation()        # -> report_fig_01_dissociation
    chart_02_precise_null()        # -> report_fig_02_precise_null
    report_chart_03_cross_substrate()  # -> report_fig_03_cross_substrate (report-only)
    chart_01_floor_not_ceiling()   # -> report_fig_04_floor


if __name__ == "__main__":
    main()
