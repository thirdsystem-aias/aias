#!/usr/bin/env python3
"""v0.44 report figures (managerial register, report design system v2 and data-viz rules v2).

One chart per finding (P1-P5). Each chart states its one insight on the chart in Indigo; everything else is in
neutrals. Titles say what is plotted and never repeat or paraphrase the finding's headline. Every plotted value and
label number is read by key from papers/v0_44/v44_values.json (the paper's values file) or
reports/v44_report_values.json (v44_report_values.py, computed from the scored files); nothing is typed.
Colour is never the only cue: markers differ in shape and carry value labels.

Run from the repo or worktree root:  ~/aias/venv/bin/python scripts/build_charts_v44_report.py
Outputs: reports/figs/v44/report/report_fig_0N_<name>.pdf  (7.5 in wide = the report's content width)
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

VALUES = json.loads((ROOT / "papers/v0_44/v44_values.json").read_text(encoding="utf-8"))["values"]
_RV = json.loads((ROOT / "reports/v44_report_values.json").read_text(encoding="utf-8"))["values"]
assert not set(VALUES) & set(_RV)
VALUES.update(_RV)
OUT = ROOT / "reports/figs/v44/report"
SOURCE = (f"Source: Third System™, AIAS™ v0.44 ({VALUES['rv.collection_month']['display']}), pre-registered "
          "(osf.io/ec6wh, v44); values files in github.com/thirdsystem-aias/aias, branch v0.44.")

INDIGO = "#37237B"
IRIS = "#908EC5"
LAVENDER = "#BBB9DD"
GREY = "#6E6E6E"
LIGHT = "#CCCCCC"
INK = "#1A1A1A"
W, H = 7.5, 3.3
INDS = ["INS", "HOT", "GRO", "QSR", "APR", "PHA", "CVF", "FAS"]


def v(k):
    return VALUES[k]["value"]


def d(k):
    return VALUES[k]["display"]


def label(i):
    return v("reg.labels")[i]


def frame(title, insight, h=H):
    fig = plt.figure(figsize=(W, h))
    fig.text(0.0, 0.985, title, fontsize=10.5, fontweight="bold", color=INK, ha="left", va="top")
    fig.text(0.0, 1 - 0.095 * H / h, insight, fontsize=9, color=INDIGO, ha="left", va="top")
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


def r1():
    fig = frame("Spread of AI naming rates across each industry's brands (standard deviation, 95% interval)",
                f"Widest spread in {d('H_Spread.sd_max_ind')}, narrowest in {d('H_Spread.sd_min_ind')}; "
                f"every interval clears the dashed line.")
    ax = fig.add_axes([0.33, 0.17, 0.63, 0.62])
    order = sorted(INDS, key=lambda i: v(f"H_Spread.{i}.sd"))
    for y, i in enumerate(order):
        lo, hi = v(f"H_Spread.{i}.ci")
        ax.plot([0, 0.5], [y, y], color="#EFEFEF", linewidth=0.6, zorder=0)
        ax.plot([lo, hi], [y, y], color=LAVENDER, linewidth=2.4, solid_capstyle="round", zorder=2)
        ax.scatter([v(f"H_Spread.{i}.sd")], [y], s=40, color=INDIGO, zorder=3)
        ax.text(hi + 0.008, y, d(f"H_Spread.{i}.sd"), fontsize=7, color=INK, va="center", ha="left")
    ax.axvline(v("rv.threshold.spread_sd"), color=GREY, linewidth=0.8, linestyle=(0, (3, 2)), zorder=1)
    ax.text(v("rv.threshold.spread_sd"), len(order) - 0.3, "pre-set bar " + d("rv.threshold.spread_sd"), fontsize=6.8, color=GREY, ha="center", va="bottom",
            bbox=dict(facecolor="white", edgecolor="none", pad=0.4), zorder=4)
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels([f"{label(i)} ({d(f'H_Spread.{i}.n')} brands)" for i in order], fontsize=7.6)
    ax.set_xlim(0, 0.5)
    ax.set_ylim(-0.6, len(order) + 0.4)
    ax.set_xlabel("Standard deviation of the brands' naming rates (dot) and its 95% interval (bar)", fontsize=7.6)
    clean(ax)
    save(fig, "report_fig_01_spread")


def r2():
    fig = frame("Average AI naming rate of leaders, challengers and smaller brands, by industry",
                f"Clearest order in {d('H_Tier.ind_rho_max_ind')} ({d('H_Tier.ind_rho_max')}), weakest in "
                f"{d('H_Tier.ind_rho_min_ind')} ({d('H_Tier.ind_rho_min')}).", h=3.6)
    ax = fig.add_axes([0.33, 0.20, 0.55, 0.58])
    order = sorted(INDS, key=lambda i: v(f"H_Tier.{i}.rho"))
    for y, i in enumerate(order):
        L, C, S = v(f"H_Tier.mean.{i}.L"), v(f"H_Tier.mean.{i}.C"), v(f"H_Tier.mean.{i}.S")
        ax.plot([0, 1], [y, y], color="#EFEFEF", linewidth=0.6, zorder=0)
        ax.plot([min(L, C, S), max(L, C, S)], [y, y], color=LIGHT, linewidth=1.2, zorder=1)
        ax.scatter([S], [y], s=34, color="white", edgecolor=GREY, linewidth=1.0, marker="s", zorder=3)
        ax.scatter([C], [y], s=34, color=IRIS, edgecolor=IRIS, marker="D", zorder=3)
        ax.scatter([L], [y], s=44, color=INDIGO, marker="o", zorder=4)
        ax.text(1.03, y, d(f"H_Tier.{i}.rho"), fontsize=7, color=INK, va="center", ha="left",
                transform=ax.get_yaxis_transform())
    ax.text(1.03, len(order) - 0.3, "rank corr.", fontsize=6.8, color=GREY, va="bottom", ha="left",
            transform=ax.get_yaxis_transform())
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels([label(i) for i in order], fontsize=7.6)
    ax.set_xlim(-0.025, 1)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_ylim(-0.6, len(order) + 0.2)
    ax.set_xlabel("Average naming rate of the tier's brands (0 = never named, 1 = named in every answer cell)",
                  fontsize=7.6)
    h = [plt.Line2D([], [], marker="o", color=INDIGO, linestyle="", markersize=6, label="Leaders"),
         plt.Line2D([], [], marker="D", color=IRIS, linestyle="", markersize=5.5, label="Challengers"),
         plt.Line2D([], [], marker="s", markerfacecolor="white", markeredgecolor=GREY, linestyle="", markersize=6,
                    label="Smaller brands")]
    ax.legend(handles=h, loc="upper center", bbox_to_anchor=(0.5, -0.19), ncol=3, fontsize=7.2, frameon=False)
    clean(ax)
    save(fig, "report_fig_02_tier_means")


def r3():
    pts = v("unit.rated_points")
    fig = frame(f"Consistency score against AI naming rate, {d('H_Sep.n')} rated brands",
                "Rated brands sit high on Consistency at every naming rate, from the least to the most named.")
    ax = fig.add_axes([0.10, 0.19, 0.86, 0.58])
    ax.scatter([p[1] for p in pts], [p[2] for p in pts], s=18, color=INDIGO, alpha=0.75, edgecolor="white",
               linewidth=0.4, zorder=3)
    ax.set_xlim(0, 1.02)
    ax.set_ylim(0, 102)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xlabel("Naming rate (0 = never named, 1 = named in every answer cell)", fontsize=7.6)
    ax.set_ylabel("Consistency (0–100)", fontsize=7.6)
    ax.grid(axis="y", color="#EFEFEF", linewidth=0.6)
    clean(ax, left=True)
    save(fig, "report_fig_03_consistency_scatter")


def r4():
    fig = frame("Share of brands with full recognition and a naming rate of zero, by market tier",
                f"{d('rv.gap.share.S')} of smaller brands ({d('D2.gap.S')} of {d('rv.tier.n.S')}) against "
                f"{d('D2.gap.L')} of {d('rv.tier.n.L')} leaders.")
    ax = fig.add_axes([0.20, 0.17, 0.74, 0.62])
    rows = [("Leaders", "L"), ("Challengers", "C"), ("Smaller brands", "S"), ("Departed brands", "G")]
    n = len(rows)
    for i, (lab, t) in enumerate(rows):
        y = n - 1 - i
        s = v(f"rv.gap.share.{t}")
        ax.barh(y, s, height=0.55, color=INDIGO if t == "S" else LIGHT)
        ax.text(s + 0.01, y, f"{d(f'rv.gap.share.{t}')}  ({d(f'D2.gap.{t}')} of {d(f'rv.tier.n.{t}')})",
                fontsize=7.2, va="center", color=INK)
    ax.set_yticks(range(n)[::-1])
    ax.set_yticklabels([r[0] for r in rows], fontsize=7.8)
    ax.set_xlim(0, 0.75)
    ax.set_xticks([0, 0.25, 0.5, 0.75])
    ax.set_xticklabels(["0%", "25%", "50%", "75%"])
    ax.set_ylim(-0.6, n - 0.4)
    ax.set_xlabel(f"Share of the tier's brands (recognised by all {d('rv.models.n')} models, naming rate 0)",
                  fontsize=7.6)
    clean(ax, left=True)
    save(fig, "report_fig_04_known_not_named")


def r5():
    fig = frame("Rank agreement of AI naming between models, and between one model's runs",
                f"Lowest: {d('rv.agree.min_pair')} ({d('rv.agree.min')}); each model agrees with its own runs "
                f"more than with any other model.")
    assert v("rv.rel1.min") > v("rv.agree.max")
    ax = fig.add_axes([0.33, 0.17, 0.63, 0.62])
    rows = [("Claude Fable 5.2 and GPT-6 Astra", "D5.claude-fable-5-2.gpt-6-astra", False),
            ("Claude Fable 5.2 and Gemini 4 Argon", "D5.claude-fable-5-2.gemini-4-argon", False),
            ("GPT-6 Astra and Gemini 4 Argon", "D5.gpt-6-astra.gemini-4-argon", False),
            ("Claude Fable 5.2, run to run", "D4.claude-fable-5-2.rel1", True),
            ("GPT-6 Astra, run to run", "D4.gpt-6-astra.rel1", True),
            ("Gemini 4 Argon, run to run", "D4.gemini-4-argon.rel1", True)]
    n = len(rows)
    for i, (lab, k, run) in enumerate(rows):
        y = n - 1 - i
        x = v(k)
        ax.plot([0.5, 1.0], [y, y], color="#EFEFEF", linewidth=0.6, zorder=0)
        ax.scatter([x], [y], s=44, zorder=3, marker="D" if run else "o",
                   color=INDIGO if run else "white", edgecolor=INDIGO, linewidth=1.2)
        ax.text(x - 0.008, y, d(k), fontsize=7, color=INK, ha="right", va="center")
    ax.axhline(2.5, color=LIGHT, linewidth=0.6)
    ax.set_yticks(range(n)[::-1])
    ax.set_yticklabels([r[0] for r in rows], fontsize=7.6)
    ax.set_xlim(0.5, 1.0)
    ax.set_ylim(-0.6, n - 0.4)
    ax.set_xlabel("Rank correlation of how often each brand is named, 1 = same order (circle: two models; "
                  "diamond: one model's runs)", fontsize=7.2)
    clean(ax)
    save(fig, "report_fig_05_agreement")


def main():
    CS.setup()
    plt.rcParams["axes.unicode_minus"] = False
    for f in (r1, r2, r3, r4, r5):
        f()


if __name__ == "__main__":
    main()
