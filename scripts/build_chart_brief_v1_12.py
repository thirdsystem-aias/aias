#!/usr/bin/env python3
"""Chart of the Coverage Paper A brief (TS-BR-v1.12-r1): one chart, one insight (data-viz rules v2).

Insight (Indigo): the rate-adjusted Coverage score stays inside the separate band against Presence, Consistency and
naming rate; the raw count of situations (grey, sensitivity S1) follows Presence and naming rate into the zone at or
beyond the not-separate line (#E4E4E4). Every plotted value and label is read from v112_verdicts.json through
reports/brief_v1_12_values.py; the lines come from the locked scorer's constants. The title says what is plotted and
does not repeat the brief's title or any finding heading.

Run from the worktree root:  AIAS_ROOT=$PWD ~/aias/venv/bin/python scripts/build_chart_brief_v1_12.py
Output: reports/figs/v112/brief/brief_fig_01_coverage_separability.pdf (7.5 in wide = content width)
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
import brief_v1_12_values as BV  # noqa: E402

OUT = ROOT / "reports/figs/v112/brief/brief_fig_01_coverage_separability.pdf"
INDIGO = "#37237B"
GREY = "#6E6E6E"
WARM = "#8C8279"
FAIL_ZONE = "#E4E4E4"
INK = "#1A1A1A"
PAPER = "#FAF7F2"  # report page ground (inside_page.ground); the chart is saved transparent
W, H = 7.5, 2.4
TICKS = [-0.5, -0.25, 0, 0.25, 0.5, 0.75, 1.0]
TICK_LABELS = ["−0.50", "−0.25", "0", "0.25", "0.50", "0.75", "1.00"]


def build():
    v, src = BV.load()
    k = BV.scorer_constants()
    lo_line, hi_line = k["SEP_CONF"], k["SEP_FALS"]
    rows = BV.chart_data(src)
    used = []

    fig = plt.figure(figsize=(W, H))
    fig.text(0.0, 0.985, "Within-category rank correlation of two Coverage measures with Presence, Consistency "
             "and naming rate", fontsize=10, fontweight="bold", color=INK, ha="left", va="top")
    fig.text(0.0, 0.915, f"The rate-adjusted score stays inside ±{v.vals['BAND_LO']} on all three; the raw "
             "count of situations follows Presence and naming rate.", fontsize=9, color=INDIGO, ha="left", va="top")
    ns = sorted({r["n"] for r in rows})
    rn = sorted({r["raw_n"] for r in rows})
    fig.text(0.0, 0.0, "Source: Third System™, AIAS™ Methodology v1.12 (Coverage Paper A), v112_verdicts.json. "
             f"Bars: 95% intervals. Brands: {BV.i0(ns[0])}–{BV.i0(ns[-1])} (score), "
             f"{BV.i0(rn[0])}–{BV.i0(rn[-1])} (raw count).", fontsize=6.5, color=GREY, ha="left", va="bottom")
    used += [("n_min", ns[0]), ("n_max", ns[-1]), ("raw_n_min", rn[0]), ("raw_n_max", rn[-1])]

    ax = fig.add_axes([0.12, 0.23, 0.64, 0.55])
    xmin, xmax = -0.55, 1.02
    for a, b in ((hi_line, xmax), (xmin, -hi_line)):
        ax.axvspan(a, b, color=FAIL_ZONE, zorder=0, linewidth=0)
    for x in (hi_line, -hi_line):
        ax.axvline(x, color=GREY, linewidth=0.8, zorder=1)
    for x in (lo_line, -lo_line):
        ax.axvline(x, color=GREY, linewidth=0.8, linestyle=(0, (3, 2)), zorder=1)
    ax.axvline(0, color="#CCCCCC", linewidth=0.6, zorder=1)
    ys = [2, 1, 0]
    for y, r in zip(ys, rows):
        ax.plot([r["lo"], r["hi"]], [y + 0.12, y + 0.12], color=INDIGO, linewidth=1.4, alpha=0.55, zorder=2,
                solid_capstyle="butt")
        ax.scatter([r["rho"]], [y + 0.12], s=46, color=INDIGO, zorder=3, edgecolor="white", linewidth=0.8)
        ax.text(r["rho"], y + 0.32, BV.m3(r["rho"]), fontsize=7.2, color=INDIGO, ha="center", va="bottom", zorder=4,
                bbox=dict(facecolor=PAPER, edgecolor="none", pad=0.6))
        ax.scatter([r["raw"]], [y - 0.16], s=40, color=WARM, zorder=3, edgecolor="white", linewidth=0.8)
        inzone = abs(r["raw"]) >= hi_line
        right = r["raw"] < 0.85  # labels near the axis end go to the left of the point
        ax.text(r["raw"] + (0.035 if right else -0.035), y - 0.16, BV.m3(r["raw"]), fontsize=7.2, color=GREY,
                ha="left" if right else "right", va="center",
                zorder=4, bbox=dict(facecolor=FAIL_ZONE if inzone else PAPER, edgecolor="none", pad=0.6))
        used += [(f"{r['leg']}.rho_w", r["rho"]), (f"{r['leg']}.ci95", [r["lo"], r["hi"]]), (f"{r['leg']}.raw", r["raw"])]
    ax.set_yticks(ys)
    ax.set_yticklabels([r["label"] for r in rows], fontsize=7.8, color=INK)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(-0.6, 2.75)
    ax.set_xticks(TICKS)
    ax.set_xticklabels(TICK_LABELS, fontsize=7.2, color=GREY)
    ax.set_xlabel("Rank correlation within category", fontsize=7.4, color=GREY)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#CCCCCC")
    ax.tick_params(axis="both", length=0)
    # legend and line notes, right of the plot
    from matplotlib.lines import Line2D
    for yy, col, lab, tc in ((0.74, INDIGO, "Rate-adjusted score", INDIGO), (0.66, WARM, "Raw count of situations", GREY)):
        fig.add_artist(Line2D([0.792], [yy], marker="o", markersize=6, color=col, markeredgecolor="white",
                              linestyle="none", transform=fig.transFigure))
        fig.text(0.805, yy, lab, fontsize=7.4, color=tc, ha="left", va="center", fontweight="bold")
    fig.text(0.785, 0.50, f"Inside ±{v.vals['BAND_LO']} (dashed):\nseparate", fontsize=6.8, color=INK,
             ha="left", va="center")
    fig.text(0.785, 0.34, f"±{v.vals['BAND_HI']} and beyond (grey):\nnot a separate score", fontsize=6.8,
             color=INK, ha="left", va="center")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, transparent=True)
    plt.close(fig)
    return OUT, used


if __name__ == "__main__":
    out, used = build()
    print("wrote", out.relative_to(ROOT), len(used), "plotted values")
