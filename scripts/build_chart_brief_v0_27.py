#!/usr/bin/env python3
"""Chart of the brief of the combined v0.27 + v0.28 paper (TS-BR-v0.27-r2): one chart, one insight (data-viz rules v2).

Insight: the three gating rank correlations with their 95% intervals, each against its own pre-registered lines.
Study 1 (convergent, higher means agreement): the zone at or above the 0.60 confirmation line is light grey, the
0.30 falsification line is solid. Study 2 (discriminant, lower means distinct): the dashed line is the 0.50
distinct ceiling, the zone at or above the 0.74 reducibility line is light grey. Indigo marks the registered result
of each row's test; the familiarity row is warm grey (undetermined). Every plotted value is read from the two
verdict files through reports/brief_v0_27_values.py; the lines come from the locked scorers' decision lines. The
title says what is plotted and repeats no finding heading.

Run from the worktree root:  AIAS_ROOT=$PWD ~/aias/venv/bin/python scripts/build_chart_brief_v0_27.py
Output: reports/figs/v027/brief/brief_fig_01_three_tests.pdf (at most 7.5 in wide = content width)
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
import brief_v0_27_values as BV  # noqa: E402

OUT = ROOT / "reports/figs/v027/brief/brief_fig_01_three_tests.pdf"
INDIGO = "#37237B"
GREY = "#6E6E6E"
WARM = "#8C8279"
ZONE = "#E4E4E4"
INK = "#1A1A1A"
W, H = 7.3, 2.2
TICKS = [-0.25, 0, 0.25, 0.5, 0.75, 1.0]
TICK_LABELS = ["−0.25", "0", "0.25", "0.50", "0.75", "1"]
LABELS = {"P": "Study 1: with the tool's Share of Voice", "R": "Study 2: with people's recognition",
          "F": "Study 2: with people's familiarity"}
Y = {"P": 3.0, "R": 1.55, "F": 0.75}


def build():
    v, src = BV.load()
    rules = BV.scorer_rules()
    conf, fals, ceil, bench = (rules[k][0] for k in ("CONF", "FALS", "CEIL", "BENCH"))
    rows = BV.chart_data(src)
    used = []

    fig = plt.figure(figsize=(W, H))
    fig.text(0.0, 0.985, "Rank correlation of Presence with each outside measure, with 95% intervals",
             fontsize=10, fontweight="bold", color=INK, ha="left", va="top")
    fig.text(0.0, 0.905, f"Share of Voice falls under {v.vals['FALS']}; recognition stays clear of "
             f"{v.vals['BENCH']}; the familiarity interval crosses every band.", fontsize=9, color=INDIGO,
             ha="left", va="top")
    fig.text(0.0, 0.0, "Source: Third System™, AIAS™ v0.27 and v0.28, v0.27_verdicts.json and v28_verdicts.json. "
             "Grey zones: confirmed (Study 1) and reducible (Study 2).", fontsize=6.5, color=GREY, ha="left",
             va="bottom")

    ax = fig.add_axes([0.33, 0.17, 0.47, 0.62])
    xmin, xmax = -0.25, 1.0
    # Study 1 band (convergent)
    ax.fill_between([conf, xmax], 2.45, 3.55, color=ZONE, linewidth=0, zorder=0)
    ax.plot([fals, fals], [2.45, 3.55], color=GREY, linewidth=0.8, zorder=1)
    # Study 2 band (discriminant)
    ax.fill_between([bench, xmax], 0.3, 2.0, color=ZONE, linewidth=0, zorder=0)
    ax.plot([ceil, ceil], [0.3, 2.0], color=GREY, linewidth=0.8, linestyle=(0, (3, 2)), zorder=1)
    ax.axvline(0, color="#CCCCCC", linewidth=0.6, zorder=1)
    ax.axhline(2.22, color="#CCCCCC", linewidth=0.5, zorder=1)
    for r in rows:
        y = Y[r["key"]]
        col = WARM if r["verdict"] == "UNDETERMINED" else INDIGO
        ax.plot(r["ci"], [y, y], color=col, linewidth=2.6, alpha=0.55, zorder=2, solid_capstyle="butt")
        ax.scatter([r["rho"]], [y], s=34, color=col, zorder=3, edgecolor="white", linewidth=0.6)
        # Study 1's value sits left of its point, clear of the 0.30 line drawn through the point
        left = r["key"] == "P"
        ax.text(r["rho"] - (0.025 if left else 0), y + 0.16, v.vals[f"{r['key']}_RHO"], fontsize=7.0, color=col,
                ha="right" if left else "center", va="bottom", fontweight="bold")
        ax.text(xmin - 0.03, y, LABELS[r["key"]], fontsize=7.2, color=INK, ha="right", va="center", clip_on=False)
        used += [(r["key"], "rho", r["rho"]), (r["key"], "ci", r["ci"])]
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(0.3, 3.55)
    ax.set_yticks([])
    ax.set_xticks(TICKS)
    ax.set_xticklabels(TICK_LABELS, fontsize=7.2, color=GREY)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#CCCCCC")
    ax.tick_params(axis="both", length=0)
    ax.text(xmax + 0.03, 3.25, f"{v.vals['CONF']} or more: confirms", fontsize=6.8, color=INK, ha="left",
            va="center", clip_on=False)
    ax.text(xmax + 0.03, 2.8, f"Under {v.vals['FALS']}: falsified", fontsize=6.8, color=INK, ha="left",
            va="center", clip_on=False)
    # one block for both Study 2 rows (the bands are the same for both), centred between them
    ax.text(xmax + 0.03, 1.15, f"Under {v.vals['CEIL']}: distinct\n{v.vals['BENCH']} or more: reducible",
            fontsize=6.8, color=INK, ha="left", va="center", clip_on=False, linespacing=1.6)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, transparent=True)
    plt.close(fig)
    return OUT, used


if __name__ == "__main__":
    out, used = build()
    print("wrote", out.relative_to(ROOT), len(used), "plotted values")
