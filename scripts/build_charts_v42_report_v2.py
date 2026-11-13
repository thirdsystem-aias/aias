#!/usr/bin/env python3
"""
v0.42 t4 wave -- report-register charts in report design system v2 (Tier 1 flagship report).

Report-only copies of build_charts_v42.py's five report figures (MODE "report"): same data, same statistics, same
titles, subtitles and verdict lines; only the colour roles of design system v2 (third_system_brand.json
palette.measure_color_semantics, scripts/chart_style.py) and one source-line citation change. The paper's figures
(reports/figs/v42/chart_0N_*.pdf) are not touched.

  report_fig_01  Presence, retiring vs newest models     Presence = Indigo; categories by marker shape
  report_fig_02  Consistency, retiring vs newest models  Consistency = Rust #BD4718; categories by marker shape
  report_fig_03  Presence, search off vs on              Presence = Indigo; categories by marker shape; the zone
                                                         below 0.50 in the "zone beyond a limit" grey #E4E4E4
  report_fig_04  run-to-run agreement                    search off Indigo circles, search on Iris squares (shape
                                                         and legend carry the condition); value labels chart ink
  report_fig_05  brands below the recall floor           waves light to dark: retiring models only Lavender Grey
                                                         edged in Iris, both panels Iris, newest models only Indigo
Copper Plate (challengers only) is no longer used. Colour is never the only cue.

Source line: v0.41 is cited by its thirdsystem.ai/OSF copy, not SSRN 7685100 (submitted Nov 9, not posted), as the
AIAS 2.0 report r3 charts do (build_charts_aias_2_0_report_r3.py, Pablo, Nov 11, 11:32 pm (c)).

Usage:  PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_charts_v42_report_v2.py [--report-out DIR]
"""
import argparse
import sys
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_charts_v42 as B  # noqa: E402
import matplotlib.axes  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

cs, VV = B.cs, B.VV
MARKERS = {s: m for s, m in zip(VV.SUBS, ("o", "s", "^", "D", "v"))}
IRIS = cs.PALETTE["indigo_t2"]           # #908EC5
LAVENDER = cs.PALETTE["indigo_t3"]       # #BBB9DD
INK = "#1A1A1A"                          # chart ink: labels beside marks that fail 4.5:1
ZONE = "#E4E4E4"                         # zone beyond a limit
B.SOURCE = ("Source: AIAS™ v0.42, t₄ wave | pre-registration {tag} | t₃: v0.41 (thirdsystem.ai; OSF ec6wh/v41) | "
            "φ: Methodology v1.8 (SSRN 6963359) | Third System™")


@contextmanager
def category_markers(colour):
    """Every category's points in one role colour, told apart by marker shape (in VV.SUBS order)."""
    orig = matplotlib.axes.Axes.scatter
    state = {"i": 0}

    def scatter(self, *a, **kw):
        s = VV.SUBS[state["i"] % len(VV.SUBS)]
        state["i"] += 1
        kw["color"] = colour
        kw["marker"] = MARKERS[s]
        return orig(self, *a, **kw)
    saved = dict(B.SUBCOL)
    B.SUBCOL.update({s: colour for s in VV.SUBS})
    matplotlib.axes.Axes.scatter = scatter
    try:
        yield
    finally:
        matplotlib.axes.Axes.scatter = orig
        B.SUBCOL.clear(); B.SUBCOL.update(saved)


@contextmanager
def palette(**over):
    saved = {k: cs.PALETTE[k] for k in over}
    cs.PALETTE.update(over)
    try:
        yield
    finally:
        cs.PALETTE.update(saved)


def chart_04(V, rows, out_dirs):
    """build_charts_v42.chart_04 (report mode) with the condition carried by colour and marker shape."""
    rel = V["descriptives"]["1_run_reliability"]
    col = {"S0": cs.COLOR_PRESENCE, "S1": IRIS}
    mk = {"S0": "o", "S1": "s"}
    fig, ax = plt.subplots(figsize=(7.5, 3.9))
    ys = np.arange(len(VV.N3))[::-1]
    for y, m in zip(ys, VV.N3):
        for c in ("S0", "S1"):
            d = rel.get(f"{m}|{c}") or {}
            off = 0.14 if c == "S0" else -0.14
            if VV.has(d, ["rel1"]) and VV.has(d, ["rel3"]):
                ax.plot([d["rel1"], d["rel3"]], [y + off, y + off], color=col[c], lw=0.8, zorder=2)
            if VV.has(d, ["rel1"]):
                ax.plot([d["rel1"]], [y + off], mk[c], color=col[c], ms=6.5, zorder=3)
                ax.text(d["rel1"] - 0.012, y + off, VV.r2(d["rel1"]), fontsize=6.6, color=INK, ha="right",
                        va="center")
            if VV.has(d, ["rel3"]):
                ax.plot([d["rel3"]], [y + off], mk[c], mfc="white", mec=col[c], ms=6.5, zorder=3)
    ax.set_yticks(ys); ax.set_yticklabels([VV.MODEL_NAME[m] for m in VV.N3], fontsize=8.5)
    vals = [d.get(k) for d in rel.values() for k in ("rel1", "rel3") if VV.has(d, [k])]
    lo = min([0.0] + [v - 0.05 for v in vals])
    ax.set_xlim(lo, 1.04); ax.set_ylim(-0.6, len(VV.N3) - 0.4)
    ax.set_xlabel("agreement between repeated runs (1 = identical brand order)", fontsize=8.5)
    ax.tick_params(axis="x", labelsize=8)
    handles = [Line2D([], [], marker="o", ls="", color=col["S0"], label="search off, one run"),
               Line2D([], [], marker="s", ls="", color=col["S1"], label="search on, one run"),
               Line2D([], [], marker="o", ls="", mfc="white", mec=cs.GRAY, label="average of three runs (open)")]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.42, -0.24), ncol=3, fontsize=7.2, frameon=False)
    fig.subplots_adjust(top=0.74, bottom=0.30, left=0.17, right=0.97)
    B._header(fig, 4, "How alike the brand order is when the same model answers the same questions again.",
              "Filled marks: one run against another (value shown). Open marks: the average of three runs, which "
              "the scores use.")
    verdict = f"P4 {VV.REPORT_STATUS['DESCRIPTIVE']} — descriptive; no pass mark was set"
    B._save(fig, 4, verdict, B._tag(V), out_dirs)


def chart_05(V, rows, out_dirs):
    """build_charts_v42.chart_05 (report mode) with the wave tints, light (retiring) to dark (newest)."""
    d = V["descriptives"]["3_floor_persistence"]
    fig, ax = plt.subplots(figsize=(7.5, 3.7))
    if d.get("status") == "NOT_COMPUTED":
        ax.axis("off")
        ax.text(0.5, 0.5, "not computed: a model was excluded in search off (drop rule)", ha="center",
                transform=ax.transAxes, fontsize=9, color=cs.GRAY)
    else:
        b3, b4, both = d["below_floor_t3"], d["below_floor_t4"], d["below_both"]
        ax.barh(1, both, color=IRIS, height=0.5, zorder=2)
        ax.barh(1, b3 - both, left=both, color=LAVENDER, edgecolor=IRIS, linewidth=0.8, height=0.5, zorder=2)
        ax.barh(0, both, color=IRIS, height=0.5, zorder=2)
        ax.barh(0, b4 - both, left=both, color=cs.INDIGO, height=0.5, zorder=2)
        ax.text(b3 + 0.6, 1, f"{both} of {b3} still below", va="center", fontsize=8, color=INK)
        ax.text(b4 + 0.6, 0, f"{b4 - both} of {b4} were above before", va="center", fontsize=8, color=INK)
        ax.set_yticks([1, 0]); ax.set_yticklabels(["below on the retiring models", "below on the newest models"],
                                                  fontsize=8.5)
        ax.set_xlim(0, max(b3, b4) * 1.45 + 1); ax.set_ylim(-0.6, 1.6)
        ax.set_xlabel("brands (of 112)", fontsize=8.5); ax.tick_params(axis="x", labelsize=8)
        ax.legend(handles=[Patch(color=IRIS, label="below the floor on both panels"),
                           Patch(facecolor=LAVENDER, edgecolor=IRIS, label="below on the retiring models only"),
                           Patch(color=cs.INDIGO, label="below on the newest models only")],
                  loc="upper center", bbox_to_anchor=(0.45, -0.3), ncol=3, fontsize=7.2, frameon=False)
    fig.subplots_adjust(top=0.74, bottom=0.33, left=0.20, right=0.97)
    B._header(fig, 5, "Brands named less than once per model on average, on the retiring models and on the newest "
                      "models.", "Descriptive: no pass mark was set.")
    verdict = f"P5 {VV.REPORT_STATUS['DESCRIPTIVE']} — descriptive; no pass mark was set"
    B._save(fig, 5, verdict, B._tag(V), out_dirs)


def main(argv=None):
    ap = argparse.ArgumentParser(description="v0.42 report charts, design system v2")
    ap.add_argument("--verdicts", type=Path, default=ROOT / "osf/v42/v42_verdicts.json")
    ap.add_argument("--table", type=Path, default=ROOT / "osf/v42/v42_brand_table.csv")
    ap.add_argument("--report-out", type=Path, default=ROOT / "reports/figs/v42/report_v2")
    a = ap.parse_args(argv)
    src = VV.load_sources(a.verdicts, a.table)
    V, rows = src["verdicts"], src["table"]["rows"]
    if VV.is_synthetic(V):
        sys.exit("[v42 report charts v2] REFUSED: synthetic verdicts")
    B.MODE = "report"
    dirs = {"report": a.report_out}
    with category_markers(cs.COLOR_PRESENCE):
        B.chart_01(V, rows, dirs)
    with category_markers(cs.COLOR_CONSISTENCY):
        B.chart_02(V, rows, dirs)
    with category_markers(cs.COLOR_PRESENCE), palette(warm_t3=ZONE, warm_sec=INK):
        B.chart_03(V, rows, dirs)
    chart_04(V, rows, dirs)
    chart_05(V, rows, dirs)
    return 0


if __name__ == "__main__":
    sys.exit(main())
