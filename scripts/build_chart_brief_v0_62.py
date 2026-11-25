#!/usr/bin/env python3
"""Chart of the non-English wave brief (TS-BR-v0.62-r1): one chart, one insight (data-viz rules v2).

Insight (Indigo): in all three languages the agreement with the English order of brands lies above the 0.70 line the
plan set, and no 95% interval reaches the 0.50 zone (the Chinese interval starts just under 0.70). The zone under 0.50 (order not holding) is shaded #E4E4E4; the 0.70 line is dashed.
Every plotted value (rho_c and its 95% bootstrap interval) is read from v62_verdicts.json through
reports/brief_v0_62_values.py; the lines come from the locked scorer's constants. The title says what is plotted and
repeats no finding heading.

Run from the worktree root:  AIAS_ROOT=$PWD ~/aias/venv/bin/python scripts/build_chart_brief_v0_62.py
Output: reports/figs/v62/brief/brief_fig_01_presence_by_language.pdf (at most 7.5 in wide = content width)
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
import brief_v0_62_values as BV  # noqa: E402

OUT = ROOT / "reports/figs/v62/brief/brief_fig_01_presence_by_language.pdf"
INDIGO = "#37237B"
GREY = "#6E6E6E"
ZONE = "#E4E4E4"
INK = "#1A1A1A"
PAPER = "#FAF7F2"
W, H = 7.3, 1.95
TICKS = [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
TICK_LABELS = ["0.40", "0.50", "0.60", "0.70", "0.80", "0.90", "1.00"]


def build():
    v, src = BV.load()
    k = BV.module_constants(BV.SCORER)
    conf, fals = k["PRES"]
    if (BV.r2(conf), BV.r2(fals)) != (v.vals["PRES_CONF"], v.vals["PRES_FALS"]):
        raise SystemExit("chart lines differ from the printed decision lines")
    rows = BV.chart_data(src)
    used = []

    fig = plt.figure(figsize=(W, H))
    fig.text(0.0, 0.985, "Agreement with the English order of brands, by language asked",
             fontsize=10, fontweight="bold", color=INK, ha="left", va="top")
    fig.text(0.0, 0.885, f"All three languages lie above the {v.vals['PRES_CONF']} line the plan set; every "
             f"interval stays clear of the shaded zone.", fontsize=9, color=INDIGO, ha="left", va="top")
    if min(r["ci95"][0] for r in BV.chart_data(src)) <= fals:
        raise SystemExit("an interval reaches the shaded zone; the subtitle does not apply")
    fig.text(0.0, 0.0, "Source: Third System™, AIAS™ v0.62, v62_verdicts.json. Dots: centred within-category rank "
             "correlation; bars: 95% intervals; brand units in brackets.", fontsize=6.5, color=GREY, ha="left",
             va="bottom")

    ax = fig.add_axes([0.17, 0.21, 0.63, 0.53])
    xmin, xmax = 0.4, 1.0
    ax.axvspan(xmin, fals, color=ZONE, zorder=0, linewidth=0)
    ax.axvline(fals, color=GREY, linewidth=0.8, zorder=1)
    ax.axvline(conf, color=GREY, linewidth=0.8, linestyle=(0, (3, 2)), zorder=1)
    n = len(rows)
    for i, r in enumerate(rows):
        y = n - i
        ax.plot(r["ci95"], [y, y], color=INDIGO, linewidth=3.0, alpha=0.45, zorder=2, solid_capstyle="butt")
        ax.scatter([r["rho"]], [y], s=34, color=INDIGO, zorder=3, edgecolor="white", linewidth=0.6)
        ax.text(r["rho"], y + 0.22, v.vals[r["key"]], fontsize=7.0, color=INDIGO, ha="center", va="bottom",
                fontweight="bold", zorder=4,
                bbox={"boxstyle": "square,pad=0.08", "facecolor": PAPER, "edgecolor": "none"})
        nk = r["key"] + "_N"
        if str(r["n"]) != v.vals[nk].replace(",", ""):
            raise SystemExit(f"chart n for {r['key']} differs from the printed value")
        ax.text(xmin - 0.012, y, f"{r['label']} ({v.vals[nk]})", fontsize=7.2, color=INK, ha="right",
                va="center", clip_on=False)
        used += [(r["key"], "rho", r["rho"]), (r["key"], "ci95", r["ci95"]), (r["key"], "n", r["n"])]
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(0.4, n + 0.75)
    ax.set_yticks([])
    ax.set_xticks(TICKS)
    ax.set_xticklabels(TICK_LABELS, fontsize=7.2, color=GREY)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#CCCCCC")
    ax.tick_params(axis="both", length=0)
    ax.text(xmax + 0.012, n - 0.2, f"{v.vals['PRES_CONF']} or above\n(dashed): order holds", fontsize=6.8,
            color=INK, ha="left", va="center", clip_on=False)
    ax.text(xmax + 0.012, 1.2, f"Under {v.vals['PRES_FALS']}\n(shaded): does not hold", fontsize=6.8, color=INK,
            ha="left", va="center", clip_on=False)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, transparent=True)
    plt.close(fig)
    return OUT, used


if __name__ == "__main__":
    out, used = build()
    print("wrote", out.relative_to(ROOT), len(used), "plotted values")
