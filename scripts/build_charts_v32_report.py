#!/usr/bin/env python3
"""
v0.32 brand-format report figures — MANAGERIAL register (P1-P5 propositional).

Same data and visualizations as the academic build_charts_v32.py, restated in
managerial voice: plain-language titles/annotations (no H_* codes, no
CONFIRMED/FALSIFIED jargon), P-proposition footers. The mixed result is
restated, NOT softened. fig_03's sub-floor panel is re-badged "WATCH — not a
measured effect" to hold P4's discipline (the exploratory signal must never
read as confirmed).

Proposition mapping: report_fig_01 -> P1 & P3 · report_fig_02 -> P2 ·
report_fig_03 -> P4 · (P5 is the closing recommendation, not a figure.)

Outputs reports/figs/v32/report_fig_0{1,2,3}.pdf (+ .png for pre-flight view).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

sys.path.insert(0, str(Path(__file__).parent))
from chart_style import (setup, add_header, add_footer, PALETTE, FIGSIZE,
                         SAVEFIG_PARAMS, cell_colors, INDIGO, WARM, GRAY, BLACK)

ROOT = Path.home() / "aias"
V = json.load(open(ROOT / "osf" / "v32" / "v32_verdicts.json"))
OUTD = ROOT / "reports" / "figs" / "v32"
OUTD.mkdir(parents=True, exist_ok=True)
CELLC = cell_colors()
CELL_LABEL = {"A": "Heritage", "B": "Disruptor", "C": "Mass-Legacy", "D": "Defunct"}
PHASE = "v0.32"


def save(fig, n):
    pdf, png = OUTD / f"report_fig_0{n}.pdf", OUTD / f"report_fig_0{n}.png"
    fig.savefig(pdf, **SAVEFIG_PARAMS)
    fig.savefig(png, **SAVEFIG_PARAMS)
    plt.close(fig)
    print(f"  wrote {pdf.name} + {png.name}")


def pairwise():
    out = []
    for b, d in V["per_brand_cpc"].items():
        if d["cpc_A"] is not None and d["cpc_B"] is not None:
            out.append((b, d["cell"], d["cpc_A"], d["cpc_B"]))
    return out


# --- report_fig_01: P1 & P3 — standings hold broad order, but weakly ---------
def fig01():
    pw = pairwise()
    p = V["PRIMARY_H_ScoreRankStable"]
    fig, ax = plt.subplots(figsize=FIGSIZE["hero"])
    plt.subplots_adjust(top=0.80, bottom=0.16, left=0.11, right=0.96)
    lo, hi = 0.45, 1.0
    ax.plot([lo, hi], [lo, hi], ls="--", lw=0.9, color=GRAY, zorder=1)
    ax.text(hi - 0.005, hi - 0.02, "same standing", color=GRAY, fontsize=7,
            ha="right", va="top", fontstyle="italic")
    seen = set()
    for b, c, a, bb in pw:
        ax.scatter(a, bb, s=46, color=CELLC[c], edgecolor="white", linewidth=0.6,
                   zorder=3, label=(CELL_LABEL[c] if c not in seen else None))
        seen.add(c)
        ax.annotate(b, (a, bb), fontsize=6.2, color=BLACK, xytext=(3, 3),
                    textcoords="offset points")
    ax.set_xlim(lo, hi); ax.set_ylim(lo, hi)
    ax.set_xlabel("Consistency standing — older model panel")
    ax.set_ylabel("Consistency standing — current panel")
    ax.set_aspect("equal")
    ax.legend(loc="upper left", bbox_to_anchor=(0.02, 0.80), fontsize=7.5, framealpha=0.9)
    ax.text(0.03, 0.97,
            "Broad order holds (rank agreement = 0.71)\n"
            "but it is weak — the order shifts with the panel (see inset)",
            transform=ax.transAxes, ha="left", va="top", fontsize=8.5, color=INDIGO,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=INDIGO, lw=0.7))
    # LOO inset = the P3 evidence (panel only as stable as its most volatile family)
    loo = V["SENSITIVITY_leave_one_provider_out"]
    order = [("drop_openai", "drop OpenAI\n(largest jump)"), ("drop_anthropic", "drop Anthropic"),
             ("drop_google", "drop Google")]
    iax = fig.add_axes([0.60, 0.205, 0.30, 0.22])
    vals = [loo[k]["rho"] for k, _ in order]
    labs = [lab for _, lab in order]
    cols = [PALETTE["teal"] if v >= 0.70 else WARM for v in vals]
    iax.barh(range(len(vals)), vals, color=cols, height=0.62)
    iax.axvline(p["rho"], color=INDIGO, lw=1.0)
    for i, v in enumerate(vals):
        iax.text(v + 0.01, i, f"{v:.2f}", va="center", fontsize=6.5)
    iax.set_yticks(range(len(labs))); iax.set_yticklabels(labs, fontsize=6.2)
    iax.set_xlim(0, 1.0); iax.set_xticks([0, 0.5, 1.0]); iax.tick_params(labelsize=6)
    iax.set_title("drop one model family → order agreement", fontsize=6.5, loc="left")
    add_header(fig, "Standings hold their broad order across a model upgrade — but weakly",
               "Per-brand AI-consistency: older model panel vs current",
               "Treat a single reading as indicative, not definitive — the order shifts with the panel.")
    add_footer(fig, verdict="Propositions 1 & 3 — order broadly holds, weakly; instability concentrates in the largest version jump.",
               phase=PHASE, protocol="v1.7")
    save(fig, 1)


# --- report_fig_02: P2 — score not reproducible to the measure's resolution --
def fig02():
    pw = pairwise()
    s = V["SECONDARY_H_ScoreMagnitudeStable"]
    thr = s["threshold_0.5xSD"]
    rows = sorted([(b, c, bb - a) for b, c, a, bb in pw], key=lambda r: r[2])
    fig, ax = plt.subplots(figsize=FIGSIZE["hero_tall"])
    plt.subplots_adjust(top=0.82, bottom=0.14, left=0.20, right=0.96)
    ax.axvspan(-thr, thr, color=PALETTE["indigo_t3"], alpha=0.45, zorder=0,
               label=f"gap separating brands (±{thr:.2f})")
    for i, (b, c, d) in enumerate(rows):
        ax.barh(i, d, color=CELLC[c], height=0.66,
                edgecolor=(WARM if abs(d) > thr else "white"),
                linewidth=(1.1 if abs(d) > thr else 0.5), zorder=2)
    ax.axvline(0, color=BLACK, lw=0.8)
    ax.set_yticks(range(len(rows))); ax.set_yticklabels([b for b, _, _ in rows], fontsize=7.5)
    ax.set_xlabel("Change in consistency score, older → current panel")
    ax.set_xlim(-0.22, 0.24)
    ax.legend(loc="upper left", fontsize=7.5)
    ax.text(0.98, 0.04,
            f"Typical move ({s['mean_abs_dCPC']:.2f}) exceeds the gap separating brands ({thr:.2f}).\n"
            f"No overall up-or-down drift — brands reshuffle. Do not over-read period-over-period change.",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=8.2, color=INDIGO,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=INDIGO, lw=0.7))
    add_header(fig, "A consistency score is not reproducible across an upgrade",
               "Per-brand score change, older panel to current",
               "The typical shift is larger than the gap between brands — so period-over-period changes must not be over-read.")
    add_footer(fig, verdict="Proposition 2 — score not reproducible to the measure's own resolution.",
               phase=PHASE, protocol="v1.7")
    save(fig, 2)


# --- report_fig_03: P4 — emerging brands a movement to WATCH, not measured ---
def fig03():
    t = V["TERTIARY_H_EmergingInstability"]
    fig = plt.figure(figsize=FIGSIZE["hero_tall"])
    plt.subplots_adjust(top=0.80, bottom=0.12, left=0.12, right=0.95, hspace=0.55)
    # top — the measured test: no movement registered
    axt = fig.add_subplot(2, 1, 1)
    cells = ["A", "B", "C", "D"]
    rates = [t["cell_flip_rate"][c]["flip_rate"] or 0.0 for c in cells]
    axt.bar(range(4), rates, color=[CELLC[c] for c in cells], width=0.6)
    axt.set_ylim(0, 1.0); axt.set_xticks(range(4))
    axt.set_xticklabels([CELL_LABEL[c] for c in cells], fontsize=7.5)
    axt.set_ylabel("brands newly registered")
    for i in range(4):
        axt.text(i, 0.03, "0", ha="center", fontsize=9, color=BLACK, fontweight="bold")
    axt.set_title("Measured: no brand crossed the threshold in any group", fontsize=9, loc="left", color=BLACK)
    # bottom — WATCH: sub-threshold rise, demarcated so it can't read as measured
    axb = fig.add_subplot(2, 1, 2)
    axb.set_facecolor("#FBF1EC")
    emerging = ["Rivian", "Lucid", "Polestar", "Fisker"]
    mA = [float(np.mean(V["per_brand_cpc"][b]["counts_A"])) for b in emerging]
    mB = [float(np.mean(V["per_brand_cpc"][b]["counts_B"])) for b in emerging]
    x = np.arange(len(emerging)); w = 0.38
    axb.bar(x - w / 2, mA, w, color=PALETTE["gray_light"], label="older panel")
    axb.bar(x + w / 2, mB, w, color=WARM, label="current panel")
    axb.axhline(1.0, color=BLACK, lw=1.0, ls="--")
    axb.text(len(emerging) - 0.5, 1.02, "threshold this measure registers",
             ha="right", va="bottom", fontsize=7, color=BLACK)
    axb.set_xticks(x); axb.set_xticklabels(emerging, fontsize=7.5)
    axb.set_ylabel("AI recall (newer models)")
    axb.set_ylim(0, 1.4); axb.legend(loc="center right", fontsize=7.5)
    axb.add_patch(Rectangle((0, 0), 1, 1, transform=axb.transAxes, fill=False,
                            edgecolor=WARM, lw=1.4, ls=(0, (4, 3)), zorder=10, clip_on=False))
    axb.text(0.01, 0.98, "WATCH — not a measured effect", transform=axb.transAxes,
             ha="left", va="top", fontsize=8.5, color=WARM, fontweight="bold")
    axb.set_title("To watch: recall rising under newer models, still below the threshold",
                  fontsize=9, loc="left", color=WARM)
    add_header(fig, "Emerging brands are gaining AI recall — a movement to watch",
               "New-brand recall, older panel vs current",
               "Rising under newer models, but below the level this measure registers: watch it, do not yet act on it.")
    add_footer(fig, verdict="Proposition 4 — a signal to watch, not a measured effect.",
               phase=PHASE, protocol="v1.7")
    save(fig, 3)


if __name__ == "__main__":
    setup()
    print("building v0.32 MANAGERIAL report figures (P1-P5):")
    fig01(); fig02(); fig03()
    print("done.")
