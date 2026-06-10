#!/usr/bin/env python3
"""
v0.34 CPC Longitudinal t1->t2 Stability — figure builder (paper register).
Forked from build_charts_v33.py; house style via chart_style.py.

  chart_01_cpc_t1_t2_stability   H_CPC_Temporal_Stability (PRIMARY, CONFIRMED 4/5)
  chart_02_residual_gate_saturation  H_CPC_Drift_Beyond_Presence (PRIMARY gate, MARGINAL)
  chart_03_presence_stability    H_Presence_Temporal_Stability (SECONDARY, MARGINAL cap)
  chart_04_phantom_persistence   H_Phantom_Temporal_Persistence (TERTIARY, descriptive)

Per-brand points reuse score_v34.wave_t1/wave_t2 + cv_cpc/c_p (no logic dup).
Scalars (rho/p/flags/phantom) read from osf/v34/v34_verdicts.json.
Outputs reports/figs/v34/chart_0N_<topic>.pdf  (+ _preview.png for inspection).
"""
import sys, json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path.home() / "aias"
sys.path.insert(0, str(ROOT / "scripts"))
import chart_style as cs
cs.setup()
import score_v34 as SC

SOURCE_PHASE = "v0.34 (CPC Longitudinal t1->t2 Stability)"
PROTOCOL = "v0.34-prereg-r1"
OUT = {"paper": ROOT / "reports/figs/v34", "report": ROOT / "reports/figs/v34/report"}
for _d in OUT.values():
    _d.mkdir(parents=True, exist_ok=True)
MODE = "paper"   # set by main loop; selects footer register + filename

# Per-chart metadata: paper (H_*) vs report (P-register) footers + filenames.
# Identical plots; only footer text and filename differ (v0.33 dual-register pattern).
META = {
    1: {"paper": "chart_01_cpc_t1_t2_stability", "report": "report_fig_01",
        "paper_v": "H_CPC_Temporal_Stability: CONFIRMED — rho >= 0.70 in 4/5 substrates (MC permutation, 10k draws)",
        "report_v": "P1 SUPPORTED — recall-consistency standings held in four of five categories; the miss is the smallest, most fragmented panel."},
    2: {"paper": "chart_02_residual_gate_saturation", "report": "report_fig_02",
        "paper_v": "H_CPC_Drift_Beyond_Presence: MARGINAL — residual rho >= 0.50 in 1/5 informative substrates (4/5 saturation-flagged)",
        "report_v": "P2 NOT ESTABLISHED — the independence test could only run where recognition varies; four of five categories sat at the recognition ceiling."},
    3: {"paper": "chart_03_presence_stability", "report": "report_fig_03",
        "paper_v": "H_Presence_Temporal_Stability: MARGINAL — 3/5 measurable (all rho >= 0.80); 2/5 rank-degenerate at ceiling",
        "report_v": "P3 SUPPORTED WHERE MEASURABLE — recognition standings held wherever there was a ranking to hold; two categories were a constant ceiling, both waves."},
    4: {"paper": "chart_04_phantom_persistence", "report": "report_fig_04",
        "paper_v": "H_Phantom_Temporal_Persistence: descriptive — pooled retention 56/57 = 0.98 (no threshold)",
        "report_v": "P4 OBSERVED — brands below the recall floor stayed there, 56 of 57; AI invisibility is a standing condition, not a bad week."},
}
OMNI = ["v0.19", "v0.20", "v0.21", "v0.22", "v0.23"]
CAT = {"v0.19": "headphones", "v0.20": "skincare", "v0.21": "cosmetics",
       "v0.22": "automotive", "v0.23": "spirits"}

V = json.load(open(ROOT / "osf/v34/v34_verdicts.json"))
PS = V["per_substrate"]

# per-brand waves (reuse scoring extraction verbatim)
T1 = SC.wave_t1()
T2 = SC.wave_t2()


def _save(fig, key):
    m = META[key]
    verdict = m["paper_v"] if MODE == "paper" else m["report_v"]
    fname = m[MODE]
    cs.add_footer(fig, verdict=verdict, phase=SOURCE_PHASE, protocol=PROTOCOL)
    fig.savefig(OUT[MODE] / f"{fname}.pdf", **cs.SAVEFIG_PARAMS)
    if MODE == "paper":   # preview PNG for inspection (paper register only)
        fig.savefig(OUT[MODE] / f"{fname}_preview.png", dpi=120, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    print(f"  [{MODE}] wrote {fname}.pdf")


def _pairs_cpc(s):
    """(cvcpc_t1, cvcpc_t2) for brands defined (>=floor) in BOTH waves."""
    w1, w2 = T1[s], T2[s]
    xs, ys = [], []
    for b in w1:
        if b not in w2:
            continue
        a, c = SC.cv_cpc(w1[b]["recall"]), SC.cv_cpc(w2[b]["recall"])
        if a is not None and c is not None:
            xs.append(a); ys.append(c)
    return np.array(xs), np.array(ys)


def _pairs_cp(s):
    w1, w2 = T1[s], T2[s]
    xs, ys = [], []
    for b in w1:
        if b not in w2:
            continue
        xs.append(SC.c_p(w1[b]["recog"])); ys.append(SC.c_p(w2[b]["recog"]))
    return np.array(xs), np.array(ys)


# ============================================================ fig1
def chart_01():
    fig, axes = plt.subplots(1, 5, figsize=(8.6, 3.2))
    for ax, s in zip(axes, OMNI):
        d = PS[s]["cpc"]; rho = d["rho"]; p = d["mc_p"]; n = d["n_defined_both"]
        miss = not (rho is not None and rho >= 0.70)
        col = cs.WARM if miss else cs.INDIGO
        x, y = _pairs_cpc(s)
        ax.plot([0, 1], [0, 1], color=cs.PALETTE["gray_light"], lw=0.8, ls="--", zorder=1)
        ax.scatter(x, y, s=26, color=col, alpha=0.8, edgecolor="white", linewidth=0.4, zorder=3)
        ax.set_xlim(0, 1.02); ax.set_ylim(0, 1.02)
        ax.set_xticks([0, 0.5, 1.0]); ax.set_yticks([0, 0.5, 1.0])
        ax.tick_params(labelsize=6.5)
        ax.set_title(f"{s} {CAT[s]}", fontsize=7.6, fontweight="bold", color=col, pad=4)
        mark = "miss" if miss else "pass"
        ptxt = f"p={p:.3f}" if p is not None else "p=n/a"
        ax.text(0.04, 0.96, f"ρ={rho:.2f}\n{ptxt}\nn={n}\n{mark}",
                transform=ax.transAxes, ha="left", va="top",
                fontsize=6.6, color=col,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=col, lw=0.6))
        if s == "v0.19":
            ax.set_ylabel("CV-CPC  t2", fontsize=8)
        ax.set_xlabel("t1", fontsize=7.5)
    fig.subplots_adjust(top=0.60, bottom=0.26, left=0.055, right=0.985, wspace=0.32)
    cs.add_header(fig, "CV-CPC rank order holds from t1 to t2 in four of five substrates",
                  "Per-brand CV-CPC at t1 vs t2; identity diagonal dashed. Defined both waves (mean recall >= 1.0).",
                  "Indigo = passes 0.70 criterion; warm = miss (v0.19, rho=0.42, n.s., n=8).")
    _save(fig, 1)


# ============================================================ fig2
def chart_02():
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    ys = np.arange(len(OMNI))[::-1]
    bw = 0.36
    for i, s in enumerate(OMNI):
        yy = ys[i]
        raw = PS[s]["cpc"]["rho"]
        res = PS[s]["gate"]["residual_rho"]
        flagged = PS[s]["gate"]["saturation_flagged"]
        raw_col = cs.PALETTE["gray_light"] if flagged else cs.INDIGO
        res_col = cs.PALETTE["indigo_t2"] if flagged else cs.WARM
        hatch = "//" if flagged else None
        ax.barh(yy + bw / 2, raw, height=bw, color=raw_col, hatch=hatch,
                edgecolor=cs.GRAY if flagged else "white", linewidth=0.5, zorder=3)
        ax.barh(yy - bw / 2, res, height=bw, color=res_col, hatch=hatch,
                edgecolor=cs.GRAY if flagged else "white", linewidth=0.5, zorder=3)
        if flagged:
            ax.text(max(raw, res) + 0.02, yy, "residual = raw  (C_P constant: residualization no-op)",
                    va="center", ha="left", fontsize=6.6, color=cs.GRAY, fontstyle="italic")
        else:
            dd = PS[s]["gate"]["rho_delta_cpc_cp"]
            ax.text(0.02, yy + bw / 2, "raw", va="center", ha="left", fontsize=6.4,
                    color="white", fontweight="bold")
            ax.text(0.02, yy - bw / 2, "residual", va="center", ha="left", fontsize=6.4,
                    color="white", fontweight="bold")
            ax.text(max(raw, res) + 0.02, yy,
                    f"informative: residual {res:.2f} > raw {raw:.2f};  drift-coupling ρ={dd:.2f}",
                    va="center", ha="left", fontsize=6.8, color=cs.WARM, fontweight="bold")
        ax.text(-0.02, yy, f"{s} {CAT[s]}", va="center", ha="right",
                fontsize=8, color=cs.BLACK)
    ax.axvline(0.50, color=cs.GRAY, lw=1.0, ls=":", zorder=2)
    ax.text(0.50, len(OMNI) - 0.32, "0.50 gate criterion", ha="center", va="bottom",
            fontsize=6.8, color=cs.GRAY)
    ax.set_xlim(0, 1.55); ax.set_ylim(-0.7, len(OMNI) - 0.2)
    ax.set_yticks([]); ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.tick_params(labelsize=8)
    ax.set_xlabel("Spearman ρ (t1 to t2 stability)", fontsize=9)
    fig.subplots_adjust(top=0.80, bottom=0.20, left=0.12, right=0.97)
    cs.add_header(fig, "The Beyond-Presence gate is informative in only one substrate",
                  "Raw vs Presence-residualized CV-CPC stability. rho(dCV-CPC, dC_P) is null wherever C_P is constant.",
                  "Hatched/muted = recognition-saturated (v0.20-v0.23): residual = raw. v0.19 is the lone informative substrate.")
    _save(fig, 2)


# ============================================================ fig3
def chart_03():
    fig, axes = plt.subplots(1, 5, figsize=(8.6, 3.2))
    rng = np.random.default_rng(280400)
    for ax, s in zip(axes, OMNI):
        rho = PS[s]["presence"]["rho"]
        degenerate = rho is None
        if degenerate:
            ax.text(0.5, 0.56, "C_P constant\n6/6, both waves", transform=ax.transAxes,
                    ha="center", va="center", fontsize=7.8, color=cs.GRAY, fontweight="bold")
            ax.text(0.5, 0.27, "exact match 100%", transform=ax.transAxes,
                    ha="center", va="center", fontsize=7.2, color=cs.TEAL, fontstyle="italic")
            ax.set_xticks([]); ax.set_yticks([])
            for sp in ax.spines.values():
                sp.set_edgecolor(cs.PALETTE["gray_light"])
            ax.set_title(f"{s} {CAT[s]}", fontsize=7.6, fontweight="bold", color=cs.GRAY, pad=4)
        else:
            x, y = _pairs_cp(s)
            jx = (rng.random(len(x)) - 0.5) * 0.22
            jy = (rng.random(len(y)) - 0.5) * 0.22
            ax.plot([0, 6], [0, 6], color=cs.PALETTE["gray_light"], lw=0.8, ls="--", zorder=1)
            ax.scatter(x + jx, y + jy, s=22, color=cs.INDIGO, alpha=0.7,
                       edgecolor="white", linewidth=0.3, zorder=3)
            ax.set_xlim(-0.4, 6.4); ax.set_ylim(-0.4, 6.4)
            ax.set_xticks([0, 3, 6]); ax.set_yticks([0, 3, 6]); ax.tick_params(labelsize=6.5)
            pass80 = "pass" if rho >= 0.80 else "miss"
            ax.text(0.04, 0.96, f"ρ={rho:.2f} {pass80}", transform=ax.transAxes,
                    ha="left", va="top", fontsize=6.8, color=cs.INDIGO,
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=cs.INDIGO, lw=0.6))
            ax.set_title(f"{s} {CAT[s]}", fontsize=7.6, fontweight="bold", color=cs.INDIGO, pad=4)
        if s == "v0.19":
            ax.set_ylabel("C_P  t2", fontsize=8)
        if not degenerate:
            ax.set_xlabel("t1", fontsize=7.5)
    fig.subplots_adjust(top=0.60, bottom=0.26, left=0.055, right=0.985, wspace=0.32)
    cs.add_header(fig, "Presence is stable where measurable; saturated to a constant in two substrates",
                  "Per-brand C_P (0-6) at t1 vs t2; 0.80 criterion. Degenerate panels shown honestly (no fabricated rho).",
                  "v0.21 & v0.23: C_P at the 6/6 recognition ceiling both waves — rank-degenerate; exact-match supplement instead.")
    _save(fig, 3)


# ============================================================ fig4
def chart_04():
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    labels = [f"{s}\n{CAT[s]}" for s in OMNI] + ["pooled"]
    props, fracs, t1tot, rettot = [], [], 0, 0
    for s in OMNI:
        ph = PS[s]["phantom"]
        props.append(ph["proportion"]); fracs.append(f"{ph['retained_t2']}/{ph['t1_phantom']}")
        t1tot += ph["t1_phantom"]; rettot += ph["retained_t2"]
    props.append(rettot / t1tot); fracs.append(f"{rettot}/{t1tot}")
    xs = np.arange(len(labels))
    cols = [cs.INDIGO] * len(OMNI) + [cs.WARM]
    ax.bar(xs, props, color=cols, edgecolor="white", linewidth=0.6, width=0.66, zorder=3)
    for x, pr, fr in zip(xs, props, fracs):
        ax.text(x, pr + 0.012, f"{pr:.2f}", ha="center", va="bottom",
                fontsize=8, fontweight="bold", color=cs.BLACK)
        ax.text(x, pr / 2, fr, ha="center", va="center", fontsize=7.2,
                color="white", fontweight="bold")
    ax.annotate("the single flip (v0.21: 9/10)", xy=(2, 0.905), xytext=(2.15, 0.62),
                fontsize=6.8, color=cs.GRAY,
                arrowprops=dict(arrowstyle="->", color=cs.GRAY, lw=0.7))
    ax.set_ylim(0, 1.14); ax.set_xticks(xs); ax.set_xticklabels(labels, fontsize=7.6)
    ax.set_yticks([0, 0.5, 1.0]); ax.tick_params(axis="y", labelsize=8)
    ax.set_ylabel("t1→t2 phantom retention", fontsize=9)
    fig.subplots_adjust(top=0.80, bottom=0.18, left=0.10, right=0.96)
    cs.add_header(fig, "Phantom status is near-perfectly persistent across the interval",
                  "Share of t1 below-recall-floor (phantom) brands retaining phantom status at t2.",
                  "Descriptive (tertiary); no confirmation threshold. Pooled 56/57.")
    _save(fig, 4)


if __name__ == "__main__":
    print("building v0.34 figures (dual register) -> reports/figs/v34/{,report/}")
    for _m in ("paper", "report"):
        MODE = _m
        chart_01(); chart_02(); chart_03(); chart_04()
    print("done")
