#!/usr/bin/env python3
"""Chart of the Sentiment Paper A brief (TS-BR-v1.20-r1): one chart, one insight (data-viz rules v2).

Insight (Indigo): against Presence the within-category correlation reaches the 0.50 line at the third wave.
Consistency, the second series, is in warm grey; the zone at or above the line is the fail zone (#E4E4E4).
Every plotted value and label is read from v1_20_verdicts.json through reports/brief_v1_20_values.py; the lines
come from the locked scorer's constants. The title says what is plotted and does not repeat the brief's title.

Run from the worktree root:  AIAS_ROOT=$PWD ~/aias/venv/bin/python scripts/build_chart_brief_v1_20.py
Output: reports/figs/v120/brief/brief_fig_01_presence_overlap.pdf (7.5 in wide = content width)
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
import brief_v1_20_values as BV  # noqa: E402

OUT = ROOT / "reports/figs/v120/brief/brief_fig_01_presence_overlap.pdf"
INDIGO = "#37237B"
GREY = "#6E6E6E"
WARM = "#8C8279"
FAIL_ZONE = "#E4E4E4"
INK = "#1A1A1A"
PAPER = "#FAF7F2"  # report page ground (inside_page.ground); the chart is saved transparent
W, H = 7.5, 2.7
WAVE_LABEL = {"t1": "First wave", "t2": "Second wave", "t3": "Third wave"}


def build():
    v, src = BV.load()
    k = BV.scorer_constants()
    lo_line, hi_line = k["BAND_CONFIRMED_MAX"], k["BAND_FALSIFIED_MIN"]
    rows = BV.chart_data(src)
    used = []

    fig = plt.figure(figsize=(W, H))
    fig.text(0.0, 0.985, "Within-category rank correlation of the Sentiment score with Presence and with "
             "Consistency, by wave", fontsize=10, fontweight="bold", color=INK, ha="left", va="top")
    fig.text(0.0, 0.915, f"Against Presence it reaches the {v.vals['BAND_HI']} line at the third wave; "
             "against Consistency it stays near zero.", fontsize=9, color=INDIGO, ha="left", va="top")
    ns = sorted({r["n"] for r in rows["presence"]})
    fig.text(0.0, 0.0, f"Source: Third System™, AIAS™ Methodology v1.20 (Sentiment Paper A), v1_20_verdicts.json. "
             f"Bars: 95% bootstrap intervals; {BV.i0(ns[0])}–{BV.i0(ns[-1])} brands per wave.",
             fontsize=6.5, color=GREY, ha="left", va="bottom")
    used += [("source_n_min", ns[0]), ("source_n_max", ns[-1])]

    ax = fig.add_axes([0.075, 0.13, 0.70, 0.66])
    ymin, ymax = -0.45, 0.85
    ax.axhspan(hi_line, ymax, color=FAIL_ZONE, zorder=0, linewidth=0)
    ax.axhline(hi_line, color=GREY, linewidth=0.8, zorder=1)
    ax.axhline(lo_line, color=GREY, linewidth=0.8, linestyle=(0, (3, 2)), zorder=1)
    ax.axhline(0, color="#CCCCCC", linewidth=0.6, zorder=1)
    ax.text(2.62, hi_line + 0.03, f"{v.vals['BAND_HI']} and above:\nnot a separate score", fontsize=6.8,
            color=INK, ha="left", va="bottom")
    ax.text(2.62, lo_line - 0.03, f"{v.vals['BAND_LO']} and below:\nseparate", fontsize=6.8, color=INK,
            ha="left", va="top")
    for key, colour, dx, label in (("consistency", WARM, 0.12, "Consistency"), ("presence", INDIGO, -0.12, "Presence")):
        xs = []
        for i, r in enumerate(rows[key]):
            x = i + dx
            xs.append(x)
            ax.plot([x, x], [r["lo"], r["hi"]], color=colour, linewidth=1.4, alpha=0.55, zorder=2,
                    solid_capstyle="butt")
            ax.scatter([x], [r["rho"]], s=46, color=colour, zorder=3, edgecolor="white", linewidth=0.8)
            ax.text(x - 0.07 if key == "presence" else x + 0.07, r["rho"], BV.r3(r["rho"]).replace("-", "−"),
                    fontsize=7.2, color=INDIGO if key == "presence" else GREY,
                    ha="right" if key == "presence" else "left", va="center", zorder=4,
                    bbox=dict(facecolor=FAIL_ZONE if r["rho"] >= hi_line else PAPER, edgecolor="none", pad=0.6),
                    fontweight="bold" if (key == "presence" and r["wave"] == "t3") else "normal")
            used += [(f"{key}.{r['wave']}.rho", r["rho"]), (f"{key}.{r['wave']}.ci95", [r["lo"], r["hi"]])]
        ax.plot(xs, [r["rho"] for r in rows[key]], color=colour, linewidth=0.9, alpha=0.6, zorder=2)
        last = rows[key][-1]
        ax.text(2.5 if key == "presence" else 2.5, (last["hi"] + 0.04) if key == "presence" else (last["lo"] - 0.05),
                label, fontsize=7.8, color=colour if key == "presence" else GREY, ha="right",
                va="bottom" if key == "presence" else "top", fontweight="bold")
    ax.set_xticks(range(3))
    ax.set_xticklabels([WAVE_LABEL[w] for w in ("t1", "t2", "t3")], fontsize=7.8)
    ax.set_xlim(-0.5, 2.55)
    ax.set_ylim(ymin, ymax)
    ax.set_yticks([-0.25, 0, 0.25, 0.5, 0.75])
    ax.set_yticklabels(["−0.25", "0", "0.25", "0.50", "0.75"], fontsize=7.2, color=GREY)
    ax.set_ylabel("Rank correlation within category", fontsize=7.4, color=GREY)
    for s in ("top", "right", "bottom"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color("#CCCCCC")
    ax.tick_params(axis="both", length=0)
    ax.set_clip_on(False)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, transparent=True)
    plt.close(fig)
    return OUT, used


if __name__ == "__main__":
    out, used = build()
    print("wrote", out.relative_to(ROOT), len(used), "plotted values")
