#!/usr/bin/env python3
"""v0.40 report figures (managerial register, report design system v2 and data-viz rules v2).

One chart per finding. Each chart states its one insight on the chart in Indigo; everything else is in
warm neutrals. Titles say what is plotted and never repeat the finding's headline. Every plotted value
and label number is read from osf/v40/v40_values.json by key (display strings); nothing is typed.

Run from the repo or worktree root:  ~/aias/venv/bin/python scripts/build_charts_v40_report.py
Outputs: reports/figs/v40/report/report_fig_0N_<name>.pdf  (7.5 in wide = the report's content width)
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import chart_style as CS  # noqa: E402

VALUES = json.loads((ROOT / "osf/v40/v40_values.json").read_text(encoding="utf-8"))["values"]
OUT = ROOT / "reports/figs/v40/report"

INDIGO = "#37237B"
GREY = "#6E6E6E"
LIGHT = "#CCCCCC"
INK = "#1A1A1A"
SOURCE = "Source: Third System™, AIAS™ v0.40 (November 2026), pre-registered; values file osf/v40/v40_values.json."
W, H = 7.5, 3.3


def v(k):
    return VALUES[k]["value"]


def d(k):
    return VALUES[k]["display"]


def frame(title, insight):
    fig = plt.figure(figsize=(W, H))
    fig.text(0.0, 0.985, title, fontsize=10.5, fontweight="bold", color=INK, ha="left", va="top")
    fig.text(0.0, 0.905, insight, fontsize=9, color=INDIGO, ha="left", va="top")
    fig.text(0.0, 0.0, SOURCE, fontsize=6.5, color=GREY, ha="left", va="bottom")
    return fig


def save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / f"{name}.pdf"
    fig.savefig(p)
    plt.close(fig)
    print("wrote", p.relative_to(ROOT))


def clean(ax, left=False):
    for s in ("top", "right") + (("left",) if not left else ()):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis="both", labelsize=7.5, length=0)


def hdots(ax, rows, xlim, refs, xlabel, fmt):
    """rows: (label, value_key_base, highlighted)."""
    n = len(rows)
    for i, (lab, base, hi) in enumerate(rows):
        y = n - 1 - i
        x = v(base[0])
        ax.plot(xlim, [y, y], color="#EFEFEF", linewidth=0.6, zorder=0)
        ax.scatter([x], [y], s=52, zorder=3, color=INDIGO if hi else "white", edgecolor=INDIGO if hi else GREY,
                   linewidth=1.3)
        ax.text(x, y + 0.28, fmt(base), fontsize=7, color=INK if hi else GREY, ha="center", va="bottom")
    for xr, lab in refs:
        ax.axvline(xr, color=GREY, linewidth=0.8, linestyle=(0, (3, 2)))
        ax.text(xr, n + 0.1, lab, fontsize=6.8, color=GREY, ha="center", va="bottom")
    ax.set_yticks(range(n)[::-1])
    ax.set_yticklabels([r[0] for r in rows], fontsize=7.8)
    ax.set_xlim(*xlim)
    ax.set_ylim(-0.6, n + 0.7)
    ax.set_xlabel(xlabel, fontsize=7.8)
    clean(ax)


def r1():
    fig = frame("Rank correlation of market share with share of AI naming, by category and model group",
                "Banks track market share in every version; airlines drop below the bar when Sun Country "
                "counts inside Allegiant.")
    ax = fig.add_axes([0.30, 0.17, 0.66, 0.60])
    rows = [("Airlines, all nine models", ("H_Reinforce.airline.rho",), False),
            ("Airlines, older models", ("sensitivity.S-Arm.legacy.H_Reinforce.airline.rho",), False),
            ("Airlines, newest models", ("sensitivity.S-Arm.current.H_Reinforce.airline.rho",), False),
            ("Airlines, Sun Country in Allegiant", ("sensitivity.S-SunCountry.H_Reinforce_airline.rho",), True),
            ("Banks, all nine models", ("H_Reinforce.bank.rho",), False),
            ("Banks, older models", ("sensitivity.S-Arm.legacy.H_Reinforce.bank.rho",), False),
            ("Banks, newest models", ("sensitivity.S-Arm.current.H_Reinforce.bank.rho",), False)]
    hdots(ax, rows, (0, 1), [(v("thresholds.reinforce_rho"), "pass bar " + d("thresholds.reinforce_rho"))],
          "Spearman rank correlation (1 = same order as the market)", lambda b: d(b[0]))
    save(fig, "report_fig_01_share_order")


def r2():
    fig = frame("Leader's share of AI naming as a multiple of its market share",
                "Every version stays below the same-as-market line; the amplified line was out of reach at this "
                "answer breadth.")
    ax = fig.add_axes([0.30, 0.17, 0.66, 0.60])
    rows = [("American, all nine models", ("H_Amplify.airline.ratio",), True),
            ("American, older models", ("sensitivity.S-Arm.legacy.H_Amplify.airline.ratio",), False),
            ("American, newest models", ("sensitivity.S-Arm.current.H_Amplify.airline.ratio",), False),
            ("JPMorgan Chase, all nine models", ("H_Amplify.bank.ratio",), True),
            ("JPMorgan Chase, older models", ("sensitivity.S-Arm.legacy.H_Amplify.bank.ratio",), False),
            ("JPMorgan Chase, newest models", ("sensitivity.S-Arm.current.H_Amplify.bank.ratio",), False)]
    hdots(ax, rows, (0, 1.5), [(1.0, "same as market"), (v("thresholds.amplify_ratio"), "amplified " + d("thresholds.amplify_ratio"))],
          "Share of AI naming divided by market share", lambda b: d(b[0]))
    save(fig, "report_fig_02_leader_multiple")


def r3():
    fig = frame("Departed-brand and model pairs named in a recommendation without gone wording",
                f"{d('H_Afterlife.airline.rate')} of airline and {d('H_Afterlife.bank.rate')} of bank pairs: above the "
                f"floor, far below the bar.")
    ax = fig.add_axes([0.30, 0.17, 0.66, 0.60])
    rows = [("Airlines, all nine models", "H_Afterlife.airline"), ("Airlines, older models",
            "sensitivity.S-Arm.legacy.H_Afterlife.airline"), ("Airlines, newest models",
            "sensitivity.S-Arm.current.H_Afterlife.airline"), ("Banks, all nine models", "H_Afterlife.bank"),
            ("Banks, older models", "sensitivity.S-Arm.legacy.H_Afterlife.bank"),
            ("Banks, newest models", "sensitivity.S-Arm.current.H_Afterlife.bank")]
    n = len(rows)
    for i, (lab, b) in enumerate(rows):
        y = n - 1 - i
        r = v(b + ".rate")
        ax.barh(y, r, height=0.55, color=INDIGO if "all nine" in lab else LIGHT)
        ax.text(r + 0.004, y, f"{d(b + '.rate')}  ({d(b + '.afterlife_pairs')} of {d(b + '.pairs')} pairs)",
                fontsize=7, va="center", color=INK)
    for xr, lab in ((v("thresholds.afterlife_null"), "floor"), (v("thresholds.afterlife_rate"), "bar")):
        ax.axvline(xr, color=GREY, linewidth=0.8, linestyle=(0, (3, 2)))
        ax.text(xr, n - 0.35, lab, fontsize=6.8, color=GREY, ha="center", va="bottom")
    ax.set_yticks(range(n)[::-1])
    ax.set_yticklabels([r[0] for r in rows], fontsize=7.8)
    ax.set_xlim(0, 0.3)
    ax.set_ylim(-0.6, n + 0.2)
    ax.set_xticks([0, 0.05, 0.1, 0.2, 0.3])
    ax.set_xticklabels(["0%", "5%", "10%", "20%", "30%"])
    ax.set_xlabel("Share of departed-brand and model pairs named without saying the brand is gone", fontsize=7.8)
    clean(ax, left=True)
    save(fig, "report_fig_03_departed_named")


def r4():
    fig = frame("Correlation of months since exit (to each model's training cutoff) with how often the brand is named",
                "Negative in every model group; only the older models reach the strong-fade line.")
    ax = fig.add_axes([0.30, 0.17, 0.66, 0.60])
    rows = [("All nine models", ("H_Decay.rho", "H_Decay"), True),
            ("Older models", ("sensitivity.S-Arm.legacy.H_Decay.rho", "sensitivity.S-Arm.legacy.H_Decay"), False),
            ("Newest models (too few named)", ("sensitivity.S-Arm.current.H_Decay.rho",
                                               "sensitivity.S-Arm.current.H_Decay"), False)]
    hdots(ax, rows, (-0.6, 0.1), [(v("thresholds.decay_rho"), "strong fade " + d("thresholds.decay_rho")), (0.0, "no fade")],
          "Spearman rank correlation (negative = fades with time)",
          lambda b: f"{d(b[0])}  ({d(b[1] + '.pairs_present')} of {d(b[1] + '.pairs')} pairs named)")
    save(fig, "report_fig_04_fade")


def r5():
    fig = frame("Status answers with gone wording: departed against living brands, by model group",
                "Living brands draw the same wording far less often, and most often from the newest models.")
    ax = fig.add_axes([0.30, 0.17, 0.66, 0.60])
    specs = [("All nine models", "H_Flag"), ("Older models", "sensitivity.S-Arm.legacy.H_Flag"),
             ("Newest models", "sensitivity.S-Arm.current.H_Flag")]
    n = len(specs)
    for i, (lab, b) in enumerate(specs):
        y = n - 1 - i
        g, c = v(b + ".ghost_rate"), v(b + ".control_rate")
        ax.barh(y + 0.19, g, height=0.34, color=INDIGO)
        ax.barh(y - 0.19, c, height=0.34, color=LIGHT)
        ax.text(g + 0.01, y + 0.19, f"departed {d(b + '.ghost_rate')} ({d(b + '.ghost_flagged')} of "
                f"{d(b + '.ghost_answers')})", fontsize=7, va="center", color=INK)
        ax.text(c + 0.01, y - 0.19, f"living {d(b + '.control_rate')} ({d(b + '.control_flagged')} of "
                f"{d(b + '.control_answers')})", fontsize=7, va="center", color=INK)
    ax.set_yticks(range(n)[::-1])
    ax.set_yticklabels([s[0] for s in specs], fontsize=7.8)
    ax.set_xlim(0, 1.32)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"])
    ax.set_ylim(-0.6, n - 0.4)
    clean(ax, left=True)
    save(fig, "report_fig_05_status_answers")


def r6():
    fig = frame("Departed-brand status answers of the newest models, with web search on",
                f"Search changed few other cells: {d('H_Search.s1_only_flagged')} toward gone, "
                f"{d('H_Search.s0_only_flagged')} away from it.")
    ax = fig.add_axes([0.30, 0.17, 0.66, 0.60])
    labs = ["Late exits flagged, search on", "Flagged only with search on", "Flagged only with search off"]
    vals = [v("H_Search.post_cutoff_s1_flagged"), v("H_Search.s1_only_flagged"), v("H_Search.s0_only_flagged")]
    disp = [f"{d('H_Search.post_cutoff_s1_flagged')} of {d('H_Search.post_cutoff_cells')}",
            f"{d('H_Search.s1_only_flagged')} of {d('H_Search.paired_cells')}",
            f"{d('H_Search.s0_only_flagged')} of {d('H_Search.paired_cells')}"]
    for i, (x, t) in enumerate(zip(vals, disp)):
        y = 2 - i
        ax.barh(y, x, height=0.5, color=INDIGO if i == 0 else LIGHT)
        ax.text(x + 0.1, y, t, fontsize=7.5, va="center", color=INK)
    ax.set_yticks([2, 1, 0])
    ax.set_yticklabels(labs, fontsize=7.6)
    ax.set_xlim(0, 8)
    ax.set_ylim(-0.6, 2.6)
    ax.set_xlabel("Cells (one departed brand asked of one model)", fontsize=7.8)
    clean(ax, left=True)
    save(fig, "report_fig_06_search_status")


def main():
    CS.setup()
    plt.rcParams["axes.unicode_minus"] = False
    for f in (r1, r2, r3, r4, r5, r6):
        f()


if __name__ == "__main__":
    main()
