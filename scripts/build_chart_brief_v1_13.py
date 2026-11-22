#!/usr/bin/env python3
"""Chart of the Grounding Paper A brief (TS-BR-v1.13-r1): one chart, one insight (data-viz rules v2).

Insight (Indigo): both Presence readings lie between the 0.30 line a separate score must stay within and the 0.50
line that fails it. Consistency, Coverage and Ranking (reported only) in warm grey; the zones beyond 0.50 are the
fail zones (#E4E4E4); the 0.30 lines are dashed. Every plotted value (rho_w and its 90% interval) is read from
v1_13_verdicts.json through reports/brief_v1_13_values.py; the lines come from the locked scorer's constants. The
title says what is plotted and repeats no finding heading.

Run from the worktree root:  AIAS_ROOT=$PWD ~/aias/venv/bin/python scripts/build_chart_brief_v1_13.py
Output: reports/figs/v113/brief/brief_fig_01_separability_legs.pdf (at most 7.5 in wide = content width)
"""
import os
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(os.environ.get("AIAS_ROOT") or Path(__file__).resolve().parents[1]).resolve()
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "reports"))
import chart_style as CS  # noqa: E402,F401  (registers Akkurat Pro, rcParams)
import brief_v1_13_values as BV  # noqa: E402

OUT = ROOT / "reports/figs/v113/brief/brief_fig_01_separability_legs.pdf"
INDIGO = "#37237B"
GREY = "#6E6E6E"
WARM = "#8C8279"
ZONE = "#E4E4E4"
INK = "#1A1A1A"
PAPER = "#FAF7F2"  # page ground behind value labels that sit on a line
W, H = 7.3, 2.3
TICKS = [-0.5, -0.3, 0, 0.3, 0.5]
TICK_LABELS = ["−0.50", "−0.30", "0", "0.30", "0.50"]


def build():
    v, src = BV.load()
    k = BV.scorer_constants()
    lo, hi = k["SEP_CONFIRM"], k["SEP_FALSIFY"]
    rows = BV.chart_data(src)
    used = []

    fig = plt.figure(figsize=(W, H))
    fig.text(0.0, 0.985, "Within-category rank correlation of the Grounding score with each other measure",
             fontsize=10, fontweight="bold", color=INK, ha="left", va="top")
    fig.text(0.0, 0.905, f"Both Presence readings lie past the {v.vals['SEP_LO']} line a separate score must stay "
             f"within, short of the {v.vals['SEP_HI']} that fails it.", fontsize=9, color=INDIGO, ha="left",
             va="top")
    fig.text(0.0, 0.0, "Source: Third System™, AIAS™ Methodology v1.13 (Grounding Paper A), v1_13_verdicts.json. "
             "Dots: correlation; bars: 90% intervals; brands in brackets.", fontsize=6.5, color=GREY, ha="left",
             va="bottom")

    ax = fig.add_axes([0.27, 0.17, 0.53, 0.62])
    xmin, xmax = -0.72, 0.72
    ax.axvspan(xmin, -hi, color=ZONE, zorder=0, linewidth=0)
    ax.axvspan(hi, xmax, color=ZONE, zorder=0, linewidth=0)
    for x in (-hi, hi):
        ax.axvline(x, color=GREY, linewidth=0.8, zorder=1)
    for x in (-lo, lo):
        ax.axvline(x, color=GREY, linewidth=0.8, linestyle=(0, (3, 2)), zorder=1)
    ax.axvline(0, color="#CCCCCC", linewidth=0.6, zorder=1)
    n = len(rows)
    for i, r in enumerate(rows):
        y = n - i
        col = INDIGO if r["role"] == "presence" else WARM
        ax.plot(r["ci90"], [y, y], color=col, linewidth=3.0, alpha=0.45, zorder=2, solid_capstyle="butt")
        ax.scatter([r["rho"]], [y], s=34, color=col, zorder=3, edgecolor="white", linewidth=0.6,
                   marker="o" if r["role"] != "reported" else "D")
        ax.text(r["rho"], y + 0.2, v.vals[r["key"]], fontsize=7.0, color=col, ha="center", va="bottom",
                fontweight="bold", zorder=4,
                bbox={"boxstyle": "square,pad=0.08", "facecolor": PAPER, "edgecolor": "none"})
        nk = {"H1_S1": "H1_N", "H1_S0": "H1_N0", "H2_S1": "H2_N1", "H2_S0": "H2_N0", "H6": "H6_N",
              "H4": "H4_N"}[r["key"]]
        if str(r["n"]) != v.vals[nk]:
            raise SystemExit(f"chart n for {r['key']} differs from the printed value")
        ax.text(xmin - 0.03, y, f"{r['label']} ({v.vals[nk]})", fontsize=7.2, color=INK, ha="right", va="center",
                clip_on=False)
        used += [(r["key"], "rho", r["rho"]), (r["key"], "ci90", r["ci90"]), (r["key"], "n", r["n"])]
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(0.4, n + 0.75)
    ax.set_yticks([])
    ax.set_xticks(TICKS)
    ax.set_xticklabels(TICK_LABELS, fontsize=7.2, color=GREY)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#CCCCCC")
    ax.tick_params(axis="both", length=0)
    ax.text(xmax + 0.03, n - 0.3, f"Within ±{v.vals['SEP_LO']}\n(dashed): separate", fontsize=6.8, color=INK,
            ha="left", va="center", clip_on=False)
    ax.text(xmax + 0.03, 1.7, f"Beyond ±{v.vals['SEP_HI']}\n(shaded): not separate", fontsize=6.8, color=INK,
            ha="left", va="center", clip_on=False)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, transparent=True)
    plt.close(fig)
    return OUT, used


if __name__ == "__main__":
    out, used = build()
    print("wrote", out.relative_to(ROOT), len(used), "plotted values")
