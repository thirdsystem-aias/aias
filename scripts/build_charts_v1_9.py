#!/usr/bin/env python3
"""
v1.9 Two-Component Composite Calibration — report-register figure builder.
House style via scripts/chart_style.py (forked from build_charts_v41.py).

  report_fig_01  Stage 1 grid: K1 and K2 for all eight candidates, t1 and t2   (P1)
  report_fig_02  Why: spread of Presence vs rated Consistency, t3              (P2)
  report_fig_03  Stage 2: the two reported scores, five months, blind          (P3)

Inputs (locked): osf/methodology/v1_9/prereg/v1_9_calibration.json (Stage 1),
osf/methodology/v1_9/v1_9_verdicts.json (Stage 2), and the descriptive per-brand table
osf/methodology/v1_9/v1_9_unit_table.csv (descriptives_v1_9.py; reproduces the locked
K1/K2 and retest values). Nothing is re-scored here; every labelled statistic comes from
the two JSON files.

Output: reports/figs/v1_9/report/report_fig_0N.pdf. The paper carries tables, not figures.
"""
import csv
import json
import os
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(os.environ.get("AIAS_ROOT", str(Path.home() / "aias")))
sys.path.insert(0, str(ROOT / "scripts"))
import chart_style as cs  # noqa: E402
cs.setup()

SOURCE_PHASE = "v1.9 (Two-Component Composite Calibration)"
PROTOCOL = "v1.9-prereg-r1"
OUT = ROOT / "reports/figs/v1_9/report"
OUT.mkdir(parents=True, exist_ok=True)
M9 = ROOT / "osf/methodology/v1_9"

CAL = json.load(open(M9 / "prereg/v1_9_calibration.json"))
VER = json.load(open(M9 / "v1_9_verdicts.json"))
H = VER["verdicts"]
ROWS = list(csv.DictReader(open(M9 / "v1_9_unit_table.csv", newline="")))

INDIGO, GRAY = cs.PALETTE["indigo"], cs.PALETTE["gray"]
T1C, T2C = cs.PALETTE["indigo_t2"], cs.PALETTE["indigo"]

LABEL = {"C_phi": "φ", "C_phiJ": "φ + J", "FLOOR": "floor", "SHRINK": "shrink", "ADD": "average", "MOD": "multiply"}

VERDICT = {
    1: "P1 NOT SUPPORTED: no combined score passed all three tests; every candidate failed at least one.",
    2: "P2 SUPPORTED: Presence spreads across the whole scale while rated Consistency sits high, so an average follows Presence.",
    3: "P3 SUPPORTED: both reported scores held their order over five months and stayed separate (tested blind).",
}


def _save(fig, key, name):
    cs.add_footer(fig, verdict=VERDICT[key], phase=SOURCE_PHASE, protocol=PROTOCOL)
    fig.savefig(OUT / f"{name}.pdf", **cs.SAVEFIG_PARAMS)
    plt.close(fig)
    print(f"  wrote {name}.pdf")


# ============================================================ fig1
def chart_01():
    cands = CAL["candidates"]
    labels = [f"{LABEL[c['consistency']]} · {LABEL[c['low_count']]} · {LABEL[c['form']]}" for c in cands]
    y = np.arange(len(cands))[::-1]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.5, 4.6), sharey=True)
    for ax, k, lim, xl, title in (
            (a1, "K1", 0.50, (0.0, 0.85), "Consistency vs Presence\n(must stay at or below 0.50)"),
            (a2, "K2", 0.95, (0.92, 1.0), "Single score vs Presence\n(must stay at or below 0.95)")):
        for i, c in enumerate(cands):
            v1, v2 = abs(c["t1"][k]["rho"]), abs(c["t2"][k]["rho"])
            ax.plot([v1, v2], [y[i], y[i]], color=cs.PALETTE["gray_light"], lw=1.2, zorder=1)
            ax.scatter([v1], [y[i]], s=34, color=T1C, zorder=3, label="May" if i == 0 else None)
            ax.scatter([v2], [y[i]], s=34, color=T2C, zorder=3, label="June" if i == 0 else None)
        ax.axvline(lim, color=cs.PALETTE["warm"], lw=1.0, ls="--", zorder=2)
        ax.axvspan(lim, xl[1], color=cs.PALETTE["warm_t3"], alpha=0.25, zorder=0, lw=0)
        ax.set_xlim(*xl)
        ax.set_title(title, fontsize=8.6, color=cs.PALETTE["black"], loc="left")
        ax.tick_params(labelsize=8)
        ax.set_xlabel("rank correlation (absolute value)", fontsize=8.5)
    a1.set_yticks(y)
    a1.set_yticklabels(labels, fontsize=8)
    a1.legend(loc="upper right", fontsize=7.6, frameon=False)
    a2.text(0.02, 0.985, "shaded = fails", transform=a2.transAxes, ha="left", va="top",
            fontsize=7.2, color=GRAY, fontstyle="italic")
    fig.subplots_adjust(top=0.72, bottom=0.19, left=0.25, right=0.97, wspace=0.08)
    cs.add_header(fig, "No single score passed",
                  "The eight pre-specified ways to combine the two scores, tested on the May and June waves.",
                  "Each row: Consistency score · rule for brands with few mentions · how the two scores are combined.")
    _save(fig, 1, "report_fig_01")


# ============================================================ fig2
def chart_02():
    t3 = [r for r in ROWS if r["wave"] == "t3"]
    P = np.array([float(r["P"]) for r in t3])
    C = np.array([float(r["C_star"]) for r in t3 if r["C_star"]])
    n_un = len(t3) - len(C)
    bins = np.arange(0, 105, 5)
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(7.5, 4.6), sharex=True)
    a1.hist(P, bins=bins, color=cs.PALETTE["indigo_t2"], edgecolor="white", lw=0.6)
    a2.hist(C, bins=bins, color=INDIGO, edgecolor="white", lw=0.6)
    for ax, txt in ((a1, f"Presence, all {len(P)} brands"),
                    (a2, f"Consistency, the {len(C)} brands named six or more times ({n_un} not rated)")):
        ax.text(0.01, 0.95, txt, transform=ax.transAxes, ha="left", va="top", fontsize=8.4, color=cs.PALETTE["black"])
        ax.set_ylabel("brands", fontsize=8.5)
        ax.tick_params(labelsize=8)
        ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    for ax, v in ((a1, P), (a2, C)):
        lo, hi = np.percentile(v, [10, 90])
        ax.axvspan(lo, hi, color=cs.PALETTE["indigo_t3"], alpha=0.25, lw=0, zorder=0)
        right = hi < 85
        ax.text(hi + 1 if right else lo - 1, ax.get_ylim()[1] * 0.55, f"middle 80%:\n{lo:.0f} to {hi:.0f}",
                fontsize=7.4, color=GRAY, ha="left" if right else "right", va="center")
    a2.set_xlim(0, 100)
    a2.set_xlabel("score (0 to 100)", fontsize=8.5)
    fig.subplots_adjust(top=0.78, bottom=0.18, left=0.09, right=0.97, hspace=0.18)
    cs.add_header(fig, "Why one number repeats Presence",
                  "Distribution of each score across the five categories, November 2026.",
                  "Averaging a score that spreads wide with one that sits high ranks brands by the wide one.")
    _save(fig, 2, "report_fig_02")


# ============================================================ fig3
def chart_03():
    p = H["H_Presence_Score_Reliability"]; d = H["H_Dissociation_t3"]; c = H["H_Consistency_Reliability"]
    fn = c["frame_structure_null"]
    rows = [
        ("Presence keeps its order\n(June to November)", p["rho"], 0.80, "pass mark 0.80", None, p["n"]),
        ("Consistency keeps its order\n(June to November)", c["rho"], 0.50, "pass mark 0.50", fn, c["n"]),
        ("Consistency vs Presence\n(November)", abs(d["rho"]), 0.30, "limit 0.30", None, d["n"]),
    ]
    fig, ax = plt.subplots(figsize=(7.5, 3.9))
    ys = [2, 1, 0]
    for yy, (lab, v, mark, mtxt, null, n) in zip(ys, rows):
        ax.plot([0, 1], [yy, yy], color=cs.PALETTE["gray_light"], lw=0.8, zorder=0)
        if null:
            ax.plot([null["null_mean"], null["null_p95"]], [yy, yy], color=cs.PALETTE["indigo_t3"], lw=7,
                    solid_capstyle="butt", zorder=1)
            ax.text((null["null_mean"] + null["null_p95"]) / 2, yy - 0.22,
                    f"questions alone: {null['null_mean']:.2f} to {null['null_p95']:.2f}",
                    ha="center", va="top", fontsize=7.2, color=GRAY)
        ax.plot([mark, mark], [yy - 0.16, yy + 0.16], color=cs.PALETTE["warm"], lw=1.4, zorder=2)
        ax.text(mark, yy + 0.2, mtxt, ha="center", va="bottom", fontsize=7.2, color=cs.PALETTE["warm_t1"])
        ax.scatter([v], [yy], s=70, color=INDIGO, zorder=3)
        ax.text(v, yy - 0.22 if not null else yy + 0.2, f"{v:.2f}  (n = {n})",
                ha="center", va="top" if not null else "bottom", fontsize=8, color=INDIGO, fontweight="bold")
    ax.set_yticks(ys)
    ax.set_yticklabels([r[0] for r in rows], fontsize=8.2)
    ax.set_xlim(0, 1); ax.set_ylim(-0.6, 2.6)
    ax.set_xlabel("rank correlation", fontsize=8.5)
    ax.tick_params(axis="x", labelsize=8)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis="y", length=0)
    fig.subplots_adjust(top=0.74, bottom=0.21, left=0.25, right=0.97)
    cs.add_header(fig, "Two reliable scores, kept apart",
                  "Blind check on the November wave, under the rules fixed before it was collected.",
                  "Shaded band: how stable Consistency looks from the structure of the questions alone (average to 95th percentile).")
    _save(fig, 3, "report_fig_03")


if __name__ == "__main__":
    print("building v1.9 report figures -> reports/figs/v1_9/report/")
    chart_01(); chart_02(); chart_03()
    print("done")
