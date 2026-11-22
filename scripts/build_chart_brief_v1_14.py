#!/usr/bin/env python3
"""Chart of the Ranking closing brief (TS-BR-v1.14-r1): one chart, one insight (data-viz rules v2).

Insight (Indigo): precedence's correlation with Presence sits inside the 0.30 line at the first and last wave and
above it at the two middle ones; its correlation with Consistency (warm grey) stays low at every wave. The zone at
or above the 0.50 line is the fail zone (#E4E4E4). Every plotted value is read from results_v1_16.json through
reports/brief_v1_14_values.py; the lines come from the locked scorer's constants. The title says what is plotted and
repeats no finding heading.

Run from the worktree root:  AIAS_ROOT=$PWD ~/aias/venv/bin/python scripts/build_chart_brief_v1_14.py
Output: reports/figs/v114/brief/brief_fig_01_presence_by_wave.pdf (at most 7.5 in wide = content width)
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
import brief_v1_14_values as BV  # noqa: E402

OUT = ROOT / "reports/figs/v114/brief/brief_fig_01_presence_by_wave.pdf"
INDIGO = "#37237B"
GREY = "#6E6E6E"
WARM = "#8C8279"
FAIL_ZONE = "#E4E4E4"
INK = "#1A1A1A"
W, H = 7.3, 2.3
TICKS = [0, 0.25, 0.5, 0.75]
TICK_LABELS = ["0", "0.25", "0.50", "0.75"]
XLAB = ["Wave 1\nsix models", "Wave 2\nthree weeks on", "Wave 3\nfive months on", "Wave 4\nnewest three models"]


def build():
    v, src = BV.load()
    k = BV.scorer_constants()
    line, fals = k["SEP_CONF"], k["SEP_FALS"]
    rows, extra = BV.chart_data(src)
    used = []

    fig = plt.figure(figsize=(W, H))
    fig.text(0.0, 0.985, "Within-category correlation of precedence with Presence and with Consistency, wave by wave",
             fontsize=10, fontweight="bold", color=INK, ha="left", va="top")
    fig.text(0.0, 0.905, f"With Presence: under {v.vals['SEP_CONF']} at the first and last wave, above it in "
             "between. With Consistency: low at every wave.", fontsize=9, color=INDIGO, ha="left", va="top")
    fig.text(0.0, 0.0, "Source: Third System™, AIAS™ Methodology v1.16, results_v1_16.json. Pooled within-category "
             "Spearman correlation; search off unless marked.", fontsize=6.5, color=GREY, ha="left", va="bottom")

    ax = fig.add_axes([0.075, 0.2, 0.70, 0.56])
    ymin, ymax = -0.02, 0.8
    ax.axhspan(fals, ymax, color=FAIL_ZONE, zorder=0, linewidth=0)
    ax.axhline(fals, color=GREY, linewidth=0.8, zorder=1)
    ax.axhline(line, color=GREY, linewidth=0.8, linestyle=(0, (3, 2)), zorder=1)
    ax.axhline(0, color="#CCCCCC", linewidth=0.6, zorder=1)
    xs = list(range(1, len(rows) + 1))
    ax.plot(xs, [r["presence"] for r in rows], color=INDIGO, linewidth=1.0, alpha=0.5, zorder=2)
    ax.plot(xs, [r["consistency"] for r in rows], color=WARM, linewidth=1.0, alpha=0.5, zorder=2)
    for i, r in enumerate(rows):
        x = i + 1
        ax.scatter([x], [r["presence"]], s=34, color=INDIGO, zorder=3, edgecolor="white", linewidth=0.6)
        ax.scatter([x], [r["consistency"]], s=22, color=WARM, zorder=3, edgecolor="white", linewidth=0.6)
        ax.text(x - 0.07, r["presence"], v.vals[f"P{x}"], fontsize=7.2, color=INDIGO, ha="right", va="center",
                fontweight="bold")
        used += [(r["wave"], "presence", r["presence"]), (r["wave"], "consistency", r["consistency"])]
    s1 = extra["prec_s1"]
    ax.scatter([4], [s1], s=30, facecolor="white", edgecolor=INDIGO, linewidth=1.0, zorder=3)
    ax.text(4.08, s1, f"search on, {v.vals['H4']}", fontsize=6.8, color=INDIGO, ha="left", va="center")
    used.append(("t4", "presence_search_on", s1))
    ax.set_xlim(0.5, 4.5)
    ax.set_ylim(ymin, ymax)
    ax.set_xticks(xs)
    ax.set_xticklabels(XLAB, fontsize=7.0, color=GREY)
    ax.set_yticks(TICKS)
    ax.set_yticklabels(TICK_LABELS, fontsize=7.2, color=GREY)
    ax.set_ylabel("Correlation", fontsize=7.4, color=GREY)
    for s in ("top", "right", "bottom"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color("#CCCCCC")
    ax.tick_params(axis="both", length=0)
    tx = 4.62
    ax.text(tx, fals + 0.02, f"{v.vals['SEP_FALS']} or more: fails", fontsize=6.8, color=INK, ha="left",
            va="bottom", clip_on=False)
    ax.text(tx, line, f"{v.vals['SEP_CONF']}: separate score", fontsize=6.8, color=INK, ha="left",
            va="center", clip_on=False)
    ax.text(tx, 0.20, "Dark: with Presence", fontsize=6.8, color=INDIGO, ha="left", va="center",
            clip_on=False, fontweight="bold")
    ax.text(tx, 0.09, "Light: with Consistency", fontsize=6.8, color=WARM, ha="left", va="center",
            clip_on=False, fontweight="bold")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, transparent=True)
    plt.close(fig)
    return OUT, used


if __name__ == "__main__":
    out, used = build()
    print("wrote", out.relative_to(ROOT), len(used), "plotted values")
