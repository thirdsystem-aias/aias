#!/usr/bin/env python3
"""Chart of the v0.43 predictive-validity brief (TS-BR-v0.43-r1): one chart, one insight (data-viz rules v2).

Insight (Indigo): all three Presence tests sit below zero with 90% intervals whose upper ends fall under the 0.10
falsification bound; Consistency (warm grey) spans zero. Thin whiskers: 95% intervals; thick bars: 90% intervals.
The confirmation line 0.15 is dashed; the zone at or above it is light grey. Every plotted value is read from
v43_stage1_verdicts.json through reports/brief_v0_43_values.py; the lines come from the locked scorer's decision
lines. The title says what is plotted and repeats no finding heading.

Run from the worktree root:  AIAS_ROOT=$PWD ~/aias/venv/bin/python scripts/build_chart_brief_v0_43.py
Output: reports/figs/v043/brief/brief_fig_01_tests_intervals.pdf (at most 7.5 in wide = content width)
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
import brief_v0_43_values as BV  # noqa: E402

OUT = ROOT / "reports/figs/v043/brief/brief_fig_01_tests_intervals.pdf"
INDIGO = "#37237B"
GREY = "#6E6E6E"
WARM = "#8C8279"
ZONE = "#E4E4E4"
INK = "#1A1A1A"
W, H = 7.3, 2.3
TICKS = [-0.4, -0.2, 0, 0.2, 0.4]
TICK_LABELS = ["−0.4", "−0.2", "0", "0.2", "0.4"]
LABELS = {"H_Pred_Presence": "Presence (main test)", "H_Pred_Presence_SA": "Presence, seasonally adjusted",
          "H_Pred_Presence_Momentum": "Presence, earlier trend held fixed",
          "H_Pred_Consistency": "Consistency, at equal Presence"}
KEYS = {"H_Pred_Presence": "P", "H_Pred_Presence_SA": "SA", "H_Pred_Presence_Momentum": "M", "H_Pred_Consistency": "C"}


def build():
    v, src = BV.load()
    rules = BV.scorer_rules()
    conf, fals = rules["CONF"][0], rules["FALS"][0]
    rows = BV.chart_data(src)
    used = []

    fig = plt.figure(figsize=(W, H))
    fig.text(0.0, 0.985, "Partial rank correlation of each June score with the later change in search interest",
             fontsize=10, fontweight="bold", color=INK, ha="left", va="top")
    fig.text(0.0, 0.905, f"All three Presence results lie below zero, with 90% intervals ending under "
             f"{v.vals['FALS']}; Consistency spans zero.", fontsize=9, color=INDIGO, ha="left", va="top")
    fig.text(0.0, 0.0, "Source: Third System™, AIAS™ v0.43 Stage 1, v43_stage1_verdicts.json. Thick bars: 90% "
             "intervals; thin lines: 95% intervals.", fontsize=6.5, color=GREY, ha="left", va="bottom")

    ax = fig.add_axes([0.30, 0.2, 0.50, 0.56])
    xmin, xmax = -0.5, 0.5
    ax.axvspan(conf, xmax, color=ZONE, zorder=0, linewidth=0)
    ax.axvline(conf, color=GREY, linewidth=0.8, linestyle=(0, (3, 2)), zorder=1)
    ax.axvline(fals, color=GREY, linewidth=0.8, zorder=1)
    ax.axvline(0, color="#CCCCCC", linewidth=0.6, zorder=1)
    n = len(rows)
    for i, r in enumerate(rows):
        y = n - i
        col = WARM if r["test"] == "H_Pred_Consistency" else INDIGO
        ax.plot(r["ci95"], [y, y], color=col, linewidth=0.8, zorder=2, solid_capstyle="butt")
        ax.plot(r["ci90"], [y, y], color=col, linewidth=3.2, alpha=0.55, zorder=2, solid_capstyle="butt")
        ax.scatter([r["rho"]], [y], s=34, color=col, zorder=3, edgecolor="white", linewidth=0.6)
        cons = r["test"] == "H_Pred_Consistency"  # its label sits left of the point, clear of the 0.10 line
        ax.text(r["rho"] - (0.015 if cons else 0), y + 0.2, v.vals[f"RHO_{KEYS[r['test']]}"], fontsize=7.0,
                color=col, ha="right" if cons else "center", va="bottom", fontweight="bold")
        ax.text(xmin - 0.02, y, LABELS[r["test"]], fontsize=7.2, color=INK, ha="right", va="center", clip_on=False)
        used += [(r["test"], "rho", r["rho"]), (r["test"], "ci90", r["ci90"]), (r["test"], "ci95", r["ci95"])]
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(0.4, n + 0.7)
    ax.set_yticks([])
    ax.set_xticks(TICKS)
    ax.set_xticklabels(TICK_LABELS, fontsize=7.2, color=GREY)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#CCCCCC")
    ax.tick_params(axis="both", length=0)
    ax.text(xmax + 0.02, n - 0.2, f"{v.vals['CONF']} or more: confirms\n(with p under {v.vals['ALPHA']})",
            fontsize=6.8, color=INK, ha="left", va="center", clip_on=False)
    ax.text(xmax + 0.02, 1.4, f"Upper 90% end under\n{v.vals['FALS']}: falsified", fontsize=6.8, color=INK,
            ha="left", va="center", clip_on=False)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, transparent=True)
    plt.close(fig)
    return OUT, used


if __name__ == "__main__":
    out, used = build()
    print("wrote", out.relative_to(ROOT), len(used), "plotted values")
