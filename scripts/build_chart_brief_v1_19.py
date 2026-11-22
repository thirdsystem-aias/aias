#!/usr/bin/env python3
"""Chart of the Coverage Paper B brief (TS-BR-v1.19-r1): one chart, one insight (data-viz rules v2).

Insight (Indigo): Paper A's own split of the situations sits near the top of the 64 balanced splits; the reliability
from the median correlation is below the 0.50 line. Other splits in warm grey; the zone below the 0.30 line is the
fail zone (#E4E4E4). Every plotted value is read from v119_verdicts.json through reports/brief_v1_19_values.py; the
lines come from the locked scorer's constants. The title says what is plotted and repeats no finding heading.

Run from the worktree root:  AIAS_ROOT=$PWD ~/aias/venv/bin/python scripts/build_chart_brief_v1_19.py
Output: reports/figs/v119/brief/brief_fig_01_split_reliability.pdf (at most 7.5 in wide = content width)
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
import brief_v1_19_values as BV  # noqa: E402

OUT = ROOT / "reports/figs/v119/brief/brief_fig_01_split_reliability.pdf"
INDIGO = "#37237B"
GREY = "#6E6E6E"
WARM = "#8C8279"
FAIL_ZONE = "#E4E4E4"
INK = "#1A1A1A"
PAPER = "#FAF7F2"
W, H = 7.3, 2.4
TICKS = [-0.25, 0, 0.25, 0.5, 0.75]
TICK_LABELS = ["−0.25", "0", "0.25", "0.50", "0.75"]


def build():
    v, src = BV.load()
    k = BV.scorer_constants()
    line, low = k["REL_CONF"], k["REL_FALS"]
    rows = BV.chart_data(src)
    med = float(src["verdicts"]["H32_SetSampling"]["rel_median"])
    used = []

    fig = plt.figure(figsize=(W, H))
    fig.text(0.0, 0.985, f"Split-half reliability of the Coverage score for each of the {v.vals['SPLITS']} balanced "
             "ways to halve the situations", fontsize=10, fontweight="bold", color=INK, ha="left", va="top")
    fig.text(0.0, 0.905, f"Paper A's own split ({v.vals['REL_A']}) sits near the top; the median correlation gives "
             f"{v.vals['REL_MED']}, under the {v.vals['REL_LINE']} line.", fontsize=9, color=INDIGO, ha="left",
             va="top")
    fig.text(0.0, 0.0, "Source: Third System™, AIAS™ Methodology v1.19 (Coverage Paper B), v119_verdicts.json. "
             f"Reliability 2r/(1+r) per split; {v.vals['SPLIT_NMIN']}–{v.vals['SPLIT_NMAX']} brands rated on "
             "both halves.", fontsize=6.5, color=GREY, ha="left", va="bottom")

    ax = fig.add_axes([0.075, 0.2, 0.70, 0.56])
    n = len(rows)
    ymin, ymax = -0.3, 0.8
    ax.axhspan(ymin, low, color=FAIL_ZONE, zorder=0, linewidth=0)
    ax.axhline(low, color=GREY, linewidth=0.8, zorder=1)
    ax.axhline(line, color=GREY, linewidth=0.8, linestyle=(0, (3, 2)), zorder=1)
    ax.axhline(med, color=INDIGO, linewidth=0.9, alpha=0.7, zorder=1)
    ax.axhline(0, color="#CCCCCC", linewidth=0.6, zorder=1)
    for i, r in enumerate(rows):
        a = r["paper_A"]
        ax.scatter([i + 1], [r["rel"]], s=40 if a else 16, color=INDIGO if a else WARM, zorder=3 if a else 2,
                   edgecolor="white", linewidth=0.6)
        used.append((r["split"], r["rel"]))
        if a:
            ax.text(i + 1, r["rel"] + 0.05, f"Paper A's split, {v.vals['REL_A']}", fontsize=7.2, color=INDIGO,
                    ha="right", va="bottom", fontweight="bold")
    ax.set_xlim(0, n + 1)
    ax.set_ylim(ymin, ymax)
    ax.set_xticks([])
    ax.set_xlabel(f"The {v.vals['SPLITS']} splits, from lowest to highest reliability", fontsize=7.4, color=GREY)
    ax.set_yticks(TICKS)
    ax.set_yticklabels(TICK_LABELS, fontsize=7.2, color=GREY)
    ax.set_ylabel("Split-half reliability", fontsize=7.4, color=GREY)
    for s in ("top", "right", "bottom"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color("#CCCCCC")
    ax.tick_params(axis="both", length=0)
    tx = n + 2.5
    ax.text(tx, line + 0.01, f"{v.vals['REL_LINE']}: required", fontsize=6.8, color=INK, ha="left", va="bottom",
            clip_on=False)
    ax.text(tx, med - 0.01, f"{v.vals['REL_MED']}: median correlation", fontsize=6.8, color=INDIGO, ha="left",
            va="top", clip_on=False)
    ax.text(tx, low - 0.04, f"Below {v.vals['REL_LOW']}: the\nband that fails", fontsize=6.8, color=INK, ha="left",
            va="top", clip_on=False)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, transparent=True)
    plt.close(fig)
    return OUT, used


if __name__ == "__main__":
    out, used = build()
    print("wrote", out.relative_to(ROOT), len(used), "plotted values")
