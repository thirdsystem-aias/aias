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


def crosses(ax, text, xs, pad=0.004):
    """True when the rendered text's horizontal extent contains any of the data x positions xs."""
    ax.figure.canvas.draw()
    bb = text.get_window_extent(ax.figure.canvas.get_renderer()).transformed(ax.transData.inverted())
    span = ax.get_xlim()[1] - ax.get_xlim()[0]
    return any(bb.x0 - pad * span <= xr <= bb.x1 + pad * span for xr in xs)


def hdots(ax, rows, xlim, refs, xlabel, fmt, fix=False):
    """rows: (label, value_key_base, highlighted)."""
    n = len(rows)
    ax.set_xlim(*xlim)
    ax.set_ylim(-0.6, n + 0.7)
    for i, (lab, base, hi) in enumerate(rows):
        y = n - 1 - i
        x = v(base[0])
        ax.plot(xlim, [y, y], color="#EFEFEF", linewidth=0.6, zorder=0)
        ax.scatter([x], [y], s=52, zorder=3, color=INDIGO if hi else "white", edgecolor=INDIGO if hi else GREY,
                   linewidth=1.3)
        off = (xlim[1] - xlim[0]) * 0.015
        t = ax.text(x + off, y + 0.12, fmt(base), fontsize=7, color=INK if hi else GREY, ha="left", va="bottom")
        if fix and crosses(ax, t, [r[0] for r in refs]):      # r2: never let a value label sit on a reference line
            t.set_ha("right")
            t.set_x(x - off)
    for xr, lab in refs:
        ax.axvline(xr, color=GREY, linewidth=0.8, linestyle=(0, (3, 2)))
        # r2: reference-line label sits above the plot area, clear of the dots and their labels
        if fix:
            ax.text(xr, 1.0, lab, fontsize=6.8, color=GREY, ha="center", va="bottom",
                    transform=ax.get_xaxis_transform(), zorder=4)
        else:
            ax.text(xr, n + 0.1, lab, fontsize=6.8, color=GREY, ha="center", va="bottom",
                    bbox=dict(facecolor="white", edgecolor="none", pad=0.4), zorder=4)
    ax.set_yticks(range(n)[::-1])
    ax.set_yticklabels([r[0] for r in rows], fontsize=7.8)
    ax.set_xlim(*xlim)
    ax.set_ylim(-0.6, n + 0.7)
    ax.set_xlabel(xlabel, fontsize=7.8)
    clean(ax)


def r1():
    fig = frame("Rank correlation of market share with share of AI naming, by category and model group",
                "Banks stay above the bar in every version; airlines fall below it for the newest models and "
                "with Sun Country grouped with Allegiant.")
    ax = fig.add_axes([0.30, 0.17, 0.66, 0.60])
    rows = [("Airlines, all nine models", ("H_Reinforce.airline.rho",), False),
            ("Airlines, older models", ("sensitivity.S-Arm.legacy.H_Reinforce.airline.rho",), False),
            ("Airlines, newest models", ("sensitivity.S-Arm.current.H_Reinforce.airline.rho",), True),
            ("Airlines, Sun Country with Allegiant", ("sensitivity.S-SunCountry.H_Reinforce_airline.rho",), True),
            ("Banks, all nine models", ("H_Reinforce.bank.rho",), False),
            ("Banks, older models", ("sensitivity.S-Arm.legacy.H_Reinforce.bank.rho",), False),
            ("Banks, newest models", ("sensitivity.S-Arm.current.H_Reinforce.bank.rho",), False)]
    hdots(ax, rows, (0, 1), [(v("thresholds.reinforce_rho"), "pass bar " + d("thresholds.reinforce_rho"))],
          "Spearman rank correlation (1 = same order as the market)", lambda b: d(b[0]), fix=True)
    save(fig, "report_fig_01_share_order")


def r2():
    # dot: the scored multiple (verdict file); tick: the most it could reach at the observed breadth of answers
    # (post-scoring check, DEVIATIONS Entry 2; values ceiling.specs.*)
    fig = frame("Leader's share of AI naming as a multiple of its market share, and the most it could reach",
                "Each tick marks a leader named in every answer; only the newest models' airline tick passes the "
                "amplified line.")
    ax = fig.add_axes([0.30, 0.17, 0.66, 0.60])
    rows = [("American, all nine models", "H_Amplify.airline", "ceiling.specs.all_nine.airline"),
            ("American, older models", "sensitivity.S-Arm.legacy.H_Amplify.airline", "ceiling.specs.legacy.airline"),
            ("American, newest models", "sensitivity.S-Arm.current.H_Amplify.airline", "ceiling.specs.current.airline"),
            ("JPMorgan Chase, all nine models", "H_Amplify.bank", "ceiling.specs.all_nine.bank"),
            ("JPMorgan Chase, older models", "sensitivity.S-Arm.legacy.H_Amplify.bank", "ceiling.specs.legacy.bank"),
            ("JPMorgan Chase, newest models", "sensitivity.S-Arm.current.H_Amplify.bank", "ceiling.specs.current.bank")]
    xlim = (0, 1.6)
    n = len(rows)
    ax.set_xlim(*xlim)
    ax.set_ylim(-0.6, n + 0.7)
    for i, (lab, base, cb) in enumerate(rows):
        assert v(base + ".k") == v(cb + ".k") and v(base + ".n") == v(cb + ".n"), (base, cb)
        y = n - 1 - i
        hi = "all nine" in lab
        x, c = v(base + ".ratio"), v(cb + ".ceiling_ratio")
        ax.plot(xlim, [y, y], color="#EFEFEF", linewidth=0.6, zorder=0)
        ax.plot([x, c], [y, y], color=LIGHT, linewidth=1.6, zorder=1, solid_capstyle="butt")
        ax.plot([c, c], [y - 0.28, y + 0.28], color=INDIGO if hi else GREY, linewidth=1.8, zorder=2)
        ax.scatter([x], [y], s=52, zorder=3, color="white", edgecolor=INDIGO if hi else GREY, linewidth=1.3)
        ax.text(x, y + 0.3, d(base + ".ratio"), fontsize=7, color=INK if hi else GREY, ha="center", va="bottom")
        mt = ax.text(c + 0.02, y, "most " + d(cb + ".ceiling_ratio"), fontsize=7, color=INDIGO if hi else GREY,
                     ha="left", va="center", zorder=4)
        refs2 = (1.0, v("thresholds.amplify_ratio"))
        for _ in range(2):   # r2: keep the label off the reference lines: start it just past the line it would cross
            hit = [xr for xr in refs2 if xr >= c and crosses(ax, mt, (xr,))]
            if not hit:
                break
            mt.set_x(max(hit) + 0.02)
    for xr, lab in ((1.0, "same as market"), (v("thresholds.amplify_ratio"), "amplified " + d("thresholds.amplify_ratio"))):
        ax.axvline(xr, color=GREY, linewidth=0.8, linestyle=(0, (3, 2)))
        ax.text(xr, 1.0, lab, fontsize=6.8, color=GREY, ha="center", va="bottom",
                transform=ax.get_xaxis_transform(), zorder=4)
    ax.set_yticks(range(n)[::-1])
    ax.set_yticklabels([r[0] for r in rows], fontsize=7.8)
    ax.set_xlim(*xlim)
    ax.set_ylim(-0.6, n + 0.7)
    ax.set_xlabel("Share of AI naming divided by market share (dot: scored; tick: highest possible)", fontsize=7.8)
    clean(ax)
    save(fig, "report_fig_02_leader_multiple")


def r3():
    fig = frame("Departed-brand and model pairs named in a recommendation without gone wording",
                "All nine models together sit between floor and bar in both categories; two model groups fall below the floor.")
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
                fontsize=7, va="center", color=INK, bbox=dict(facecolor="white", edgecolor="none", pad=0.3), zorder=4)
    for xr, lab in ((v("thresholds.afterlife_null"), "floor"), (v("thresholds.afterlife_rate"), "bar")):
        ax.axvline(xr, color=GREY, linewidth=0.8, linestyle=(0, (3, 2)))
        ax.text(xr, n - 0.35, lab, fontsize=6.8, color=GREY, ha="center", va="bottom",
                bbox=dict(facecolor="white", edgecolor="none", pad=0.4), zorder=4)
    ax.set_yticks(range(n)[::-1])
    ax.set_yticklabels([r[0] for r in rows], fontsize=7.8)
    ax.set_xlim(0, 0.3)
    ax.set_ylim(-0.6, n + 0.2)
    ax.set_xticks([0, 0.1, 0.2, 0.3])
    ax.set_xticklabels(["0%", "10%", "20%", "30%"])
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
    fig = frame("Departed-brand status cells of the newest models, search off against search on",
                f"The paired comparison needed at least {d('thresholds.search_min_discordant')} changed cells; it "
                f"found {d('H_Search.s1_only_flagged')} toward gone and {d('H_Search.s0_only_flagged')} away.")
    ax = fig.add_axes([0.30, 0.17, 0.66, 0.60])
    labs = ["Late exits flagged, search on", "Flagged only with search on", "Flagged only with search off"]
    rows = [(v("H_Search.post_cutoff_s1_flagged"), v("H_Search.post_cutoff_cells"),
             f"{d('H_Search.post_cutoff_s1_flagged')} of {d('H_Search.post_cutoff_cells')} late-exit cells"),
            (v("H_Search.s1_only_flagged"), v("H_Search.paired_cells"),
             f"{d('H_Search.s1_only_flagged')} of {d('H_Search.paired_cells')} cells"),
            (v("H_Search.s0_only_flagged"), v("H_Search.paired_cells"),
             f"{d('H_Search.s0_only_flagged')} of {d('H_Search.paired_cells')} cells")]
    for i, (k, n, txt) in enumerate(rows):
        y = 2 - i
        ax.barh(y, k / n, height=0.5, color=LIGHT if i == 0 else INDIGO)   # r2: the changed cells are the insight
        ax.text(k / n + 0.01, y, txt, fontsize=7.5, va="center", color=INK)
    ax.set_yticks([2, 1, 0])
    ax.set_yticklabels(labs, fontsize=7.6)
    ax.set_xlim(0, 1.25)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"])
    ax.set_ylim(-0.6, 2.6)
    ax.set_xlabel("Share of the cells in each group (one departed brand asked of one model)", fontsize=7.8)
    clean(ax, left=True)
    save(fig, "report_fig_06_search_status")


def main():
    CS.setup()
    plt.rcParams["axes.unicode_minus"] = False
    for f in (r1, r2, r3, r4, r5, r6):
        f()


if __name__ == "__main__":
    main()
