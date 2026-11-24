#!/usr/bin/env python3
"""v0.44 paper figures (academic register): one figure per pre-registered primary test.

Every plotted value and every label number is read from papers/v0_44/v44_values.json (values_v0_44.py), by key;
nothing is typed. Figure titles say what is plotted and never repeat the finding's heading (CLAUDE.md chart
rule of Nov 9, 2026); one insight per chart in Indigo, everything else in neutrals (data-viz rules v2).

Run from the worktree root:  python3 scripts/build_charts_v44_paper.py
Outputs: reports/figs/v44/paper/fig_0N_<name>.pdf
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
OUT = ROOT / "reports/figs/v44/paper"

INDIGO = "#37237B"
IRIS = "#908EC5"
LAVENDER = "#BBB9DD"
GREY = "#6E6E6E"
LIGHT = "#CCCCCC"
INK = "#1A1A1A"
WARM_NEUTRAL = "#B8B0A6"
SOURCE = ("Source: AIAS™ v0.44, osf/v44/v44_verdicts.json and v44_unit_table.csv (score_v0_44.py --run); "
          "pre-registration v0.44-prereg-r1 (OSF ec6wh/v44). Third System™")
INDS = ["INS", "HOT", "GRO", "QSR", "APR", "PHA", "CVF", "FAS"]


def v(key):
    return VALUES[key]["value"]


def d(key):
    return VALUES[key]["display"]


def label(i):
    return v("reg.labels")[i]


def header(fig, title, subtitle):
    fig.text(0.02, 0.985, title, fontsize=12, fontweight="bold", color=INK, ha="left", va="top")
    fig.text(0.02, 0.937, subtitle, fontsize=8.5, color=GREY, ha="left", va="top")
    fig.add_artist(plt.Line2D([0.02, 0.98], [0.845, 0.845], color=INDIGO, linewidth=0.8))
    fig.text(0.02, 0.012, SOURCE, fontsize=6.5, color=GREY, fontstyle="italic", ha="left", va="bottom")


def save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / f"{name}.pdf"
    fig.savefig(p)
    plt.close(fig)
    print("wrote", p.relative_to(ROOT))


def clean(ax):
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis="both", labelsize=8)


def fig1_spread():
    order = sorted(INDS, key=lambda i: v(f"H_Spread.{i}.sd"))
    fig, ax = plt.subplots(figsize=(7.5, 4.4))
    fig.subplots_adjust(left=0.30, right=0.95, top=0.77, bottom=0.15)
    header(fig, "Standard deviation of recall Presence across the brands of each industry",
           "Population SD of $\\hat{\\pi}$ over non-ghost units (n per industry in brackets), with its percentile bootstrap "
           "95% interval\n(10,000 resamples within industry). Dashed line: the registered spread threshold, 0.15.")
    for y, i in enumerate(order):
        lo, hi = v(f"H_Spread.{i}.ci")
        sd = v(f"H_Spread.{i}.sd")
        ax.plot([0, 0.5], [y, y], color="#EFEFEF", linewidth=0.6, zorder=0)
        ax.plot([lo, hi], [y, y], color=IRIS, linewidth=2.2, solid_capstyle="round", zorder=2)
        ax.scatter([sd], [y], s=44, color=INDIGO, zorder=3)
        ax.text(hi + 0.008, y, d(f"H_Spread.{i}.sd"), fontsize=7.5, color=INK, va="center", ha="left")
    ax.axvline(0.15, color=GREY, linewidth=0.8, linestyle=(0, (3, 2)), zorder=1)
    ax.text(0.15, len(order) - 0.35, "0.15", fontsize=7.5, color=GREY, ha="center", va="bottom")
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels([f"{label(i)} ({d(f'H_Spread.{i}.n')})" for i in order], fontsize=8)
    ax.set_xlim(0, 0.5)
    ax.set_ylim(-0.6, len(order) - 0.1)
    ax.set_xlabel("SD of recall Presence ($\\hat{\\pi}$, 0–1)", fontsize=8.5, color=INK)
    clean(ax)
    save(fig, "fig_01_spread")


def fig2_tier():
    order = sorted(INDS, key=lambda i: v(f"H_Tier.{i}.rho"))
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    fig.subplots_adjust(left=0.30, right=0.84, top=0.77, bottom=0.23)
    header(fig, "Mean recall Presence of leaders, challengers and smaller brands, by industry",
           "Mean $\\hat{\\pi}$ per tier: L = eligible ranks 1–6, C = 7–14, S = 15 and below (ghosts excluded). "
           "Right: within-industry\nSpearman $\\rho$ of tier with $\\hat{\\pi}$ (descriptive). Industries ordered by that $\\rho$.")
    for y, i in enumerate(order):
        L, C, S = v(f"H_Tier.mean.{i}.L"), v(f"H_Tier.mean.{i}.C"), v(f"H_Tier.mean.{i}.S")
        ax.plot([0, 1], [y, y], color="#EFEFEF", linewidth=0.6, zorder=0)
        ax.plot([min(L, C, S), max(L, C, S)], [y, y], color=LIGHT, linewidth=1.2, zorder=1)
        ax.scatter([S], [y], s=40, color=LAVENDER, edgecolor=IRIS, linewidth=0.9, marker="s", zorder=3)
        ax.scatter([C], [y], s=40, color=IRIS, edgecolor=IRIS, marker="D", zorder=3)
        ax.scatter([L], [y], s=48, color=INDIGO, marker="o", zorder=4)
        ax.text(1.04, y, d(f"H_Tier.{i}.rho"), fontsize=7.5, color=INK, va="center", ha="left",
                transform=ax.get_yaxis_transform())
    ax.text(1.04, len(order) - 0.25, "$\\rho$", fontsize=8, color=GREY, va="bottom", ha="left",
            transform=ax.get_yaxis_transform())
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels([label(i) for i in order], fontsize=8)
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.6, len(order) - 0.1)
    ax.set_xlabel("Mean recall Presence ($\\hat{\\pi}$, 0–1)", fontsize=8.5, color=INK)
    h = [plt.Line2D([], [], marker="o", color=INDIGO, linestyle="", markersize=6, label="Leaders (L)"),
         plt.Line2D([], [], marker="D", color=IRIS, linestyle="", markersize=5.5, label="Challengers (C)"),
         plt.Line2D([], [], marker="s", markerfacecolor=LAVENDER, markeredgecolor=IRIS, linestyle="", markersize=6,
                    label="Smaller brands (S)")]
    ax.legend(handles=h, loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=3, fontsize=7.5, frameon=False)
    clean(ax)
    save(fig, "fig_02_tier")


def fig3_separation():
    pts = v("unit.rated_points")
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    fig.subplots_adjust(left=0.11, right=0.96, top=0.77, bottom=0.14)
    header(fig, f"Scaled Consistency against recall Presence for the {d('H_Sep.n')} rated brands",
           f"Each point is a brand; the test statistic is the pooled within-industry rank correlation, "
           f"$\\rho$ = {d('H_Sep.rho')} (bootstrap 95% interval\n{d('H_Sep.ci')}). "
           "Rated: $\\varphi$ defined in at least 2 of 3 runs and $\\hat{\\pi}$ at least 1/6.")
    xs = [p[1] for p in pts]
    ys = [p[2] for p in pts]
    ax.scatter(xs, ys, s=22, color=INDIGO, alpha=0.75, edgecolor="white", linewidth=0.4, zorder=3)
    ax.set_xlim(0, 1.02)
    ax.set_ylim(0, 102)
    ax.set_xlabel("Recall Presence ($\\hat{\\pi}$, 0–1)", fontsize=8.5, color=INK)
    ax.set_ylabel("Scaled Consistency ($C_{\\varphi}$, 0–100)", fontsize=8.5, color=INK)
    ax.grid(axis="y", color="#EFEFEF", linewidth=0.6)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(axis="both", labelsize=8)
    save(fig, "fig_03_separation")


def main():
    CS.setup()
    fig1_spread()
    fig2_tier()
    fig3_separation()


if __name__ == "__main__":
    main()
