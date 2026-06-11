#!/usr/bin/env python3
"""
v0.35 Naive-Phantom x CPC Omnibus — figure builder (register-neutral).

Six figures. Figure-internal text is register-neutral (construct names only —
"gate", "raw arm", "C_P control", "recall-mean control"; no H_* / P-N labels);
the host documents' captions carry register. SSOT: osf/v35/v35_verdicts.json —
every numeric value is pulled programmatically. The ONLY hardcoded numeric
constants are the locked verdict thresholds +/-0.15 / +/-0.30 (v0.35-prereg-r1)
and the 0.20/0.40 sensitivity-band note (also read back from the JSON).

  chart_01_gate_flip               gate: control flip -> UNDETERMINED (the headline)
  chart_02_recognition_saturation  why it flips: C_P inert where recognition saturates
  chart_03_raw_manipulation_check  raw arm + LOSO whiskers (labeled manipulation check)
  chart_04_cross_substrate_concordance  per-substrate deltas; unanimous but underpowered
  chart_05_t2_stability            t1 vs t2 replication of the whole structure (walled)
  chart_06_roster_attrition        roster / attrition (report figure; paper §2 table)

Outputs reports/figs/v35/chart_0N_*.pdf (+ _preview.png), copied to osf/v35/figures/.
"""
import sys, json, csv, shutil
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path.home() / "aias"
sys.path.insert(0, str(ROOT / "scripts"))
import chart_style as cs
cs.setup()

SOURCE_PHASE = "v0.35 (Naive-Phantom × CPC)"
PROTOCOL = "v0.35-prereg-r1"
FIG_DIR = ROOT / "reports/figs/v35"
DEPOSIT_DIR = ROOT / "osf/v35/figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)
DEPOSIT_DIR.mkdir(parents=True, exist_ok=True)

# locked verdict thresholds — the only hardcoded numeric constants
LO, HI = 0.15, 0.30   # locked verdict thresholds, v0.35-prereg-r1

OMNI = ["v0.19", "v0.20", "v0.21", "v0.22", "v0.23"]
CAT = {"v0.19": "headphones", "v0.20": "skincare", "v0.21": "cosmetics",
       "v0.22": "automotive", "v0.23": "spirits"}

# ---- SSOT ----------------------------------------------------------------- #
V = json.load(open(ROOT / "osf/v35/v35_verdicts.json"))
VD = V["verdicts"]
RAW = VD["H_Phantom_CPC_Signature"]
GATE = VD["H_Phantom_Beyond_Presence"]
CROSS = VD["H_Phantom_Cross_Substrate"]
T2 = VD["H_Phantom_t2_Stability"]
ENUM = V["enumeration"]
ATT = V["attrition"]
LOSO_RAW = V["sensitivity"]["loso_raw"]
THR = V["sensitivity"]["threshold_reruns"]
CP = GATE["control_C_P"]
RM = GATE["control_recall_mean"]

ROSTER = list(csv.DictReader(open(ROOT / "osf/v35/data/v35_phantom_roster.csv")))


def d2(x):
    return f"{x:+.2f}"


def pfmt(p):
    return "p<0.0001" if p < 1e-4 else f"p={p:.3f}"


def _save(fig, fname, verdict):
    cs.add_footer(fig, verdict=verdict, phase=SOURCE_PHASE, protocol=PROTOCOL)
    fig.savefig(FIG_DIR / f"{fname}.pdf", **cs.SAVEFIG_PARAMS)
    fig.savefig(FIG_DIR / f"{fname}_preview.png", dpi=130, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    print(f"  wrote {fname}.pdf")


def _bands(ax):
    """Verdict-threshold chrome on a delta x-axis: FALSIFIED |d|<0.15 (shaded),
    +/-0.30 CONFIRMED edges (dashed)."""
    ax.axvspan(-LO, LO, color=cs.PALETTE["gray_light"], alpha=0.30, zorder=0)
    for xv in (-HI, HI):
        ax.axvline(xv, color=cs.GRAY, lw=0.8, ls="--", zorder=1)
    for xv in (-LO, LO):
        ax.axvline(xv, color=cs.PALETTE["gray_light"], lw=0.8, ls=":", zorder=1)
    ax.axvline(0.0, color=cs.GRAY, lw=1.0, zorder=1)


# ============================================================ chart_01
def chart_01():
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    rows = [("C_P control", CP, cs.INDIGO), ("recall-mean control", RM, cs.WARM)]
    ys = [1, 0]
    _bands(ax)
    for y, (name, arm, col) in zip(ys, rows):
        d = arm["delta_resid"]
        ax.barh(y, d, height=0.46, color=col, edgecolor="white", linewidth=0.6, zorder=3)
        ax.text(-1.03, y + 0.30, name, va="bottom", ha="left", fontsize=9,
                color=cs.BLACK, fontweight="bold")
        end = d + (-0.02 if d < 0 else 0.02)
        ax.text(end, y, f"{d2(d)}   {arm['verdict']}   {pfmt(arm['mc_p_twosided'])}",
                va="center", ha=("right" if d < 0 else "left"), fontsize=8.4, color=col,
                fontweight="bold")
    # zone labels along the top
    ax.text(0.0, 1.62, "FALSIFIED  |δ|<0.15", ha="center", va="bottom",
            fontsize=6.8, color=cs.GRAY)
    ax.text(-(LO + HI) / 2, 1.62, "MARGINAL", ha="center", va="bottom", fontsize=6.8, color=cs.GRAY)
    ax.text(-0.66, 1.62, "CONFIRMED  |δ|>=0.30", ha="center", va="bottom",
            fontsize=6.8, color=cs.GRAY)
    ax.text(-0.52, -0.78,
            "Gate verdict: UNDETERMINED — control flip (pre-registered rule)",
            ha="center", va="center", fontsize=9.2, color=cs.INDIGO, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.5", fc="white", ec=cs.INDIGO, lw=1.0))
    ax.set_xlim(-1.05, 0.55); ax.set_ylim(-1.05, 1.95)
    ax.set_yticks([]); ax.set_xticks([-1.0, -0.5, 0.0, 0.5])
    ax.tick_params(labelsize=8)
    ax.set_xlabel("Cliff's δ on residualized CV-CPC  (phantom − non-phantom)", fontsize=9)
    fig.subplots_adjust(top=0.80, bottom=0.24, left=0.07, right=0.97)
    cs.add_header(fig, "The gate verdict depends on which control is used",
                  "Phantom vs non-phantom CV-CPC after within-substrate residualization, under each co-primary control.",
                  "Identical procedure, two controls: recognition (C_P) and recall-mean. The verdicts disagree — the flip is the finding.")
    _save(fig, "chart_01_gate_flip",
          f"Gate UNDETERMINED — C_P control {CP['verdict']} ({d2(CP['delta_resid'])}) vs recall-mean "
          f"{RM['verdict']} ({d2(RM['delta_resid'])}); pre-registered flip rule.")


# ============================================================ chart_02
def chart_02():
    analy = [r for r in ROSTER if r["group"] in ("phantom_analyzable", "non_phantom")]
    rng = np.random.default_rng(280400)
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.8, 4.6), sharey=True)
    const = CP["per_substrate_covariate_constant"]
    for ax, key, title, xlim, xticks in (
        (axL, "c_p", "Presence control: recognition count C_P (0–6)", (-0.5, 6.5), [0, 3, 6]),
        (axR, "mean_r", "Recall-mean control (per-model mean recall)", (-0.3, 6.5), [0, 3, 6])):
        for si, s in enumerate(OMNI):
            yrow = len(OMNI) - 1 - si
            pts = [r for r in analy if r["substrate"] == s]
            for r in pts:
                xv = float(r[key])
                ph = (r["flagged"] == "True")
                jit = (rng.random() - 0.5) * 0.5
                ax.scatter(xv, yrow + jit, s=24,
                           color=(cs.WARM if ph else cs.INDIGO), alpha=0.8,
                           edgecolor="white", linewidth=0.3, zorder=3)
            if ax is axL and const[s]:
                ax.text(3.0, yrow, "control no-op  (C_P constant)", va="center", ha="center",
                        fontsize=6.6, color=cs.GRAY, fontstyle="italic")
        ax.set_xlim(*xlim); ax.set_xticks(xticks); ax.tick_params(labelsize=7.5)
        ax.set_title(title, fontsize=8.2, fontweight="bold", color=cs.BLACK, pad=5)
    axL.set_yticks(range(len(OMNI)))
    axL.set_yticklabels([f"{s} {CAT[s]}" for s in reversed(OMNI)], fontsize=7.6)
    n_const = sum(1 for s in OMNI if const[s])
    h_ph = plt.Line2D([], [], marker="o", ls="", color=cs.WARM, label="phantom (analyzable)", markersize=6)
    h_no = plt.Line2D([], [], marker="o", ls="", color=cs.INDIGO, label="non-phantom", markersize=6)
    axR.legend(handles=[h_ph, h_no], loc="lower right", fontsize=7.4, framealpha=0.9)
    fig.subplots_adjust(top=0.78, bottom=0.16, left=0.13, right=0.975, wspace=0.08)
    cs.add_header(fig, "Why the gate flips: the recognition control is inert where it is saturated",
                  f"The {ATT['analysis_set_n']} analyzable units. Left: C_P collapses to a constant in "
                  f"{n_const} of {len(OMNI)} substrates. Right: recall-mean separates the groups everywhere.",
                  "A constant covariate cannot residualize anything out — the C_P control inherits the raw signal; recall-mean removes the axis that defines the flag.")
    _save(fig, "chart_02_recognition_saturation",
          f"Recognition saturated (C_P constant) in {n_const} of {len(OMNI)} substrates — the C_P control is a no-op there.")


# ============================================================ chart_03
def chart_03():
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    losos = [LOSO_RAW["per_leftout"][s]["delta"] for s in OMNI]
    lo_d, hi_d = min(losos), max(losos)
    d = RAW["cliffs_delta"]
    _bands(ax)
    y = 0.5
    ax.errorbar(d, y, xerr=[[d - lo_d], [hi_d - d]], fmt="o", color=cs.INDIGO,
                ms=13, capsize=6, elinewidth=2.0, mec="white", mew=0.8, zorder=4)
    ax.text(d, y + 0.16, f"pooled δ = {d2(d)}   {pfmt(RAW['mc_p_twosided'])}   {RAW['verdict']}",
            ha="center", va="bottom", fontsize=9, color=cs.INDIGO, fontweight="bold")
    ax.text((lo_d + hi_d) / 2, y - 0.18,
            f"leave-one-substrate-out range  [{d2(lo_d)}, {d2(hi_d)}]", ha="center", va="top",
            fontsize=7.4, color=cs.GRAY)
    hi20 = THR["hi_0.2"]; hi40 = THR["hi_0.4"]
    ax.text(0.0, 0.06,
            f"verdict unchanged at δ-thresholds {hi20['confirmed_threshold']:.2f} and "
            f"{hi40['confirmed_threshold']:.2f} ({hi20['H_Phantom_CPC_Signature']})",
            ha="center", va="bottom", fontsize=7.0, color=cs.GRAY, fontstyle="italic")
    ax.text(0.0, 0.92, "FALSIFIED", ha="center", va="top", fontsize=6.8, color=cs.GRAY)
    ax.text(-0.66, 0.92, "CONFIRMED  |δ|>=0.30", ha="center", va="top", fontsize=6.8, color=cs.GRAY)
    ax.set_xlim(-1.05, 0.35); ax.set_ylim(0.0, 1.0)
    ax.set_yticks([]); ax.set_xticks([-1.0, -0.5, 0.0])
    ax.tick_params(labelsize=8)
    ax.set_xlabel("Cliff's δ on CV-CPC  (phantom − non-phantom)", fontsize=9)
    fig.subplots_adjust(top=0.80, bottom=0.24, left=0.06, right=0.97)
    cs.add_header(fig, "Raw arm: a large phantom–non-phantom gap, by construction",
                  "Manipulation check — confirms the known mechanical recall-coupling, not a Consistency signature.",
                  f"Pooled Cliff's δ with leave-one-substrate-out whiskers. n={RAW['n_phantom_analyzable']} phantom vs "
                  f"{RAW['n_nonphantom']} non-phantom, {RAW['n_within_substrate_pairs']} within-substrate pairs.")
    _save(fig, "chart_03_raw_manipulation_check",
          f"Raw arm {RAW['verdict']} ({d2(d)}, {pfmt(RAW['mc_p_twosided'])}) — manipulation check only; LOSO-stable.")


# ============================================================ chart_04
def chart_04():
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    deltas = CROSS["per_substrate_delta_all"]
    ys = np.arange(len(OMNI))[::-1]
    v22_n = ENUM["v0.22"]["analyzable"]
    elig = set(CROSS["eligible_substrates"])
    for yy, s in zip(ys, OMNI):
        d = deltas[s]
        eligible = s in elig
        col = cs.INDIGO if eligible else cs.PALETTE["gray_light"]
        ax.barh(yy, d, height=0.6, color=col, hatch=(None if eligible else "//"),
                edgecolor=("white" if eligible else cs.GRAY), linewidth=0.6, zorder=3)
        ax.text(d - 0.02, yy, d2(d), va="center", ha="right", fontsize=8.2,
                color=(cs.INDIGO if eligible else cs.GRAY), fontweight="bold")
        lab = f"{s} {CAT[s]}" + ("" if eligible else f"   n={v22_n} analyzable — non-inferential")
        ax.text(0.02, yy, lab, va="center", ha="left", fontsize=7.8,
                color=(cs.BLACK if eligible else cs.GRAY))
    _bands(ax)
    p = CROSS["binomial_p_twosided"]
    neg = CROSS["n_negative"]; ne = len(elig)
    ax.text(-0.55, -1.0,
            f"{neg}/{ne} concordant (all phantoms lower); exact binomial floor p={p:.3f}\n"
            f"— significance unreachable at n={ne} substrates (pre-registered)",
            ha="center", va="center", fontsize=7.4, color=cs.GRAY,
            bbox=dict(boxstyle="round,pad=0.45", fc="white", ec=cs.GRAY, lw=0.8))
    ax.set_xlim(-1.12, 0.12); ax.set_ylim(-1.6, len(OMNI) - 0.3)
    ax.set_yticks([]); ax.set_xticks([-1.0, -0.5, 0.0])
    ax.tick_params(labelsize=8)
    ax.set_xlabel("Per-substrate Cliff's δ on CV-CPC  (raw arm)", fontsize=9)
    fig.subplots_adjust(top=0.80, bottom=0.24, left=0.05, right=0.97)
    cs.add_header(fig, "Per-substrate signs are unanimous but the test is structurally underpowered",
                  "Raw-arm per-substrate Cliff's δ. Eligible (>=4 analyzable phantoms) substrates in indigo.",
                  "v0.22 (hatched) has one analyzable phantom — pooled-only, non-inferential. Sign test runs on the four eligible substrates.")
    _save(fig, "chart_04_cross_substrate_concordance",
          f"Per-substrate δ {neg}/{ne} concordant negative; binomial floor p={p:.3f} (underpowered at n={ne}).")


# ============================================================ chart_05
def chart_05():
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    measures = [
        ("raw arm", RAW["cliffs_delta"], T2["raw_arm"]["cliffs_delta"]),
        ("C_P control", CP["delta_resid"], T2["gate_control_C_P"]["delta_resid"]),
        ("recall-mean control", RM["delta_resid"], T2["gate_control_recall_mean"]["delta_resid"]),
    ]
    _bands(ax)
    ys = np.arange(len(measures))[::-1]
    for j, (yy, (name, t1v, t2v)) in enumerate(zip(ys, measures)):
        ax.plot([t1v, t2v], [yy, yy], color=cs.PALETTE["gray_light"], lw=1.4, zorder=2)
        ax.scatter(t1v, yy, s=70, color=cs.INDIGO, marker="o", edgecolor="white",
                   linewidth=0.6, zorder=4, label=("t1" if j == 0 else None))
        ax.scatter(t2v, yy, s=70, color=cs.WARM, marker="^", edgecolor="white",
                   linewidth=0.6, zorder=4, label=("t2" if j == 0 else None))
        ax.text(-1.03, yy + 0.22, name, va="bottom", ha="left", fontsize=8.4,
                color=cs.BLACK, fontweight="bold")
        ax.text(min(t1v, t2v) - 0.03, yy, f"t1 {d2(t1v)} → t2 {d2(t2v)}", va="center",
                ha="right", fontsize=7.2, color=cs.GRAY)
    ax.legend(loc="lower left", fontsize=7.6, framealpha=0.9)
    ax.set_xlim(-1.05, 0.45); ax.set_ylim(-0.7, len(measures) - 0.2)
    ax.set_yticks([]); ax.set_xticks([-1.0, -0.5, 0.0])
    ax.tick_params(labelsize=8)
    ax.set_xlabel("Cliff's δ (raw / residualized)  (phantom − non-phantom)", fontsize=9)
    fig.subplots_adjust(top=0.80, bottom=0.22, left=0.06, right=0.97)
    cs.add_header(fig, "The whole structure — including the flip — reproduces at t2",
                  "Test-retest stability check; near-replica panel; descriptive only.",
                  "t1 (circles) vs t2 (triangles) for the raw arm and both gate controls. The recall-mean control sits near zero in both waves.")
    _save(fig, "chart_05_t2_stability",
          "Walled test-retest check: raw arm and both controls reproduce at t2 — the flip replicates; descriptive only.")


# ============================================================ chart_06  (report figure)
def chart_06():
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    xs = np.arange(len(OMNI))
    analyz = [ENUM[s]["analyzable"] for s in OMNI]
    excl = [ENUM[s]["excluded_allzero"] for s in OMNI]
    nonp = [ENUM[s]["non_phantom"] for s in OMNI]
    ax.bar(xs, analyz, width=0.62, color=cs.WARM, edgecolor="white", linewidth=0.6,
           label="phantom — analyzable", zorder=3)
    ax.bar(xs, excl, bottom=analyz, width=0.62, color=cs.PALETTE["gray_light"], edgecolor="white",
           linewidth=0.6, label="phantom — excluded (all-zero)", zorder=3)
    ax.bar(xs, nonp, bottom=np.add(analyz, excl), width=0.62, color=cs.INDIGO, edgecolor="white",
           linewidth=0.6, label="non-phantom", zorder=3)
    for x, s in zip(xs, OMNI):
        tot = ENUM[s]["brands"]
        elig = ENUM[s]["eligible_ge4"]
        tag = f"analyzable {ENUM[s]['analyzable']}  " + ("✓ eligible" if elig else "pooled-only")
        ax.text(x, tot + 0.4, tag, ha="center", va="bottom", fontsize=7.0,
                color=(cs.INDIGO if elig else cs.WARM), fontweight="bold")
    ax.axhline(4, color=cs.GRAY, lw=0.9, ls=":", zorder=2)
    ax.set_xticks(xs); ax.set_xticklabels([f"{s}\n{CAT[s]}" for s in OMNI], fontsize=7.6)
    ax.set_ylim(0, 28); ax.set_yticks([0, 8, 16, 24]); ax.tick_params(axis="y", labelsize=8)
    ax.set_ylabel("brand units", fontsize=9)
    ax.legend(loc="upper center", ncol=3, fontsize=7.2, framealpha=0.9, bbox_to_anchor=(0.5, 1.04))
    fig.subplots_adjust(top=0.78, bottom=0.16, left=0.08, right=0.97)
    cs.add_header(fig, "Roster and attrition by substrate",
                  f"{ATT['flagged']} phantom-flagged of {V['n_brand_units']} units; {ATT['excluded_all_zero']} excluded (all-zero recall, undefined CV); "
                  f"analysis set {ATT['analyzable_phantom']} analyzable vs {ATT['non_phantom']} non-phantom.",
                  "Per-substrate test requires >=4 analyzable phantoms; v0.22 (one) enters pooled analysis only.")
    _save(fig, "chart_06_roster_attrition",
          f"{ATT['flagged']} flagged, {ATT['analyzable_phantom']} analyzable, {ATT['excluded_all_zero']} all-zero excluded; "
          f"v0.22 pooled-only. (Report figure; paper renders as §2 table.)")


if __name__ == "__main__":
    print("building v0.35 figures -> reports/figs/v35/  (register-neutral)")
    chart_01(); chart_02(); chart_03(); chart_04(); chart_05(); chart_06()
    for pdf in sorted(FIG_DIR.glob("chart_0*.pdf")):
        shutil.copy(pdf, DEPOSIT_DIR / pdf.name)
        print(f"  deposited {pdf.name} -> osf/v35/figures/")
    print("done")
