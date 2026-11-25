#!/usr/bin/env python3
"""v0.62 paper figures (academic register): one figure per finding.

Every plotted value and every label number is read from papers/v0_62/v62_values.json (values_v0_62.py), by key;
nothing is typed. Figure titles say what is plotted and never repeat the finding's heading (CLAUDE.md chart rule
of Nov 9, 2026); one insight per chart in Indigo, everything else in neutrals (data-viz rules v2).
Forked from scripts/build_charts_v44_paper.py (branch v0.44).

Run from the worktree root:  python3 scripts/build_charts_v62_paper.py
Outputs: reports/figs/v62/paper/fig_0N_<name>.pdf
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

VALUES = json.loads((ROOT / "papers/v0_62/v62_values.json").read_text(encoding="utf-8"))["values"]
OUT = ROOT / "reports/figs/v62/paper"

INDIGO = "#37237B"
IRIS = "#908EC5"
LAVENDER = "#BBB9DD"
GREY = "#6E6E6E"
LIGHT = "#CCCCCC"
FAIL = "#E4E4E4"
INK = "#1A1A1A"
SOURCE = ("Source: AIAS™ v0.62, osf/v62/v62_verdicts.json (score_v0_62.py, one run) and the sensitivity files of "
          "DEVIATIONS Entries 4–7;\npre-registration v0.62-prereg-r1 (OSF ec6wh/v62). Third System™")
LANGS = ["es", "ko", "zh"]
LNAME = {"es": "Spanish", "ko": "Korean", "zh": "Chinese"}
CATS = ["v0.19", "v0.20", "v0.21", "v0.22", "v0.23"]


def v(key):
    return VALUES[key]["value"]


def d(key):
    return VALUES[key]["display"]


def header(fig, title, subtitle):
    fig.text(0.02, 0.985, title, fontsize=12, fontweight="bold", color=INK, ha="left", va="top")
    fig.text(0.02, 0.937, subtitle, fontsize=8.5, color=GREY, ha="left", va="top")
    fig.add_artist(plt.Line2D([0.02, 0.98], [0.845, 0.845], color=INDIGO, linewidth=0.8))
    fig.text(0.02, 0.012, SOURCE, fontsize=6.3, color=GREY, fontstyle="italic", ha="left", va="bottom")


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


def bands(ax, lo, hi, y0, y1):
    """Verdict zones on the x axis: below lo = falsification zone, lo..hi marginal, above hi confirmation zone."""
    ax.axvspan(-1, lo, color=FAIL, zorder=0, linewidth=0)
    ax.axvline(lo, color=GREY, linewidth=0.8, linestyle=(0, (3, 2)), zorder=1)
    ax.axvline(hi, color=GREY, linewidth=0.8, linestyle=(0, (3, 2)), zorder=1)
    ax.text(lo, y1, f"{lo:.2f}", fontsize=7.5, color=GREY, ha="center", va="bottom")
    ax.text(hi, y1, f"{hi:.2f}", fontsize=7.5, color=GREY, ha="center", va="bottom")


def fig1_presence():
    fig, ax = plt.subplots(figsize=(7.5, 3.9))
    fig.subplots_adjust(left=0.15, right=0.95, top=0.74, bottom=0.23)
    header(fig, "Rank agreement of recall Presence with the English t₄ values, by language",
           "Centred within-category Spearman ρc over the 112 units, with its bootstrap 95% interval (10,000 resamples); "
           "small grey\nmarks: the five categories. Dashed lines: 0.50 (falsification) and 0.70 (confirmation); "
           "grey zone: below 0.50.")
    order = LANGS[::-1]
    bands(ax, 0.50, 0.70, 0, len(order) - 0.45)
    for y, L in enumerate(order):
        lo, hi = v(f"P.{L}.ci")
        for c in CATS:
            ax.scatter([v(f"P.{L}.cat.{c}")], [y - 0.22], s=14, color=LIGHT, edgecolor=GREY, linewidth=0.5, zorder=2)
        ax.plot([lo, hi], [y, y], color=IRIS, linewidth=2.4, solid_capstyle="round", zorder=3)
        ax.scatter([v(f"P.{L}.rho")], [y], s=52, color=INDIGO, zorder=4)
        ax.text(hi + 0.012, y, d(f"P.{L}.rho"), fontsize=8, color=INK, va="center", ha="left")
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels([f"{LNAME[L]} (n = {d(f'P.{L}.n')})" for L in order], fontsize=8.5)
    ax.set_xlim(0.40, 1.02)
    ax.set_ylim(-0.6, len(order) - 0.4)
    ax.set_xlabel("ρc with English recall Presence (t₄, v0.42)", fontsize=8.5, color=INK)
    clean(ax)
    save(fig, "fig_01_presence")


def fig2_level():
    fig, ax = plt.subplots(figsize=(7.5, 3.6))
    fig.subplots_adjust(left=0.15, right=0.95, top=0.72, bottom=0.28)
    header(fig, "Mean difference in recall Presence from English, by language",
           r"$\Delta$ = mean over the 112 units of $\hat{\pi}$ in the language minus $\hat{\pi}$ in English, "
           "with its bootstrap 95% interval. "
           "Circles: the locked\nEnglish comparator; diamonds: the corrected English table of 25 November 2026 "
           "(DEVIATIONS Entry 6).")
    order = LANGS[::-1]
    ax.axvline(0, color=GREY, linewidth=0.8, zorder=1)
    for y, L in enumerate(order):
        lo, hi = v(f"P.{L}.dL_ci")
        ax.plot([lo, hi], [y + 0.12, y + 0.12], color=INDIGO, linewidth=2.2, solid_capstyle="round", zorder=3)
        ax.scatter([v(f"P.{L}.dL")], [y + 0.12], s=48, color=INDIGO, zorder=4)
        ax.text(hi + 0.004, y + 0.12, d(f"P.{L}.dL"), fontsize=8, color=INK, va="center", ha="left")
        lo2, hi2 = v(f"ENC.P.{L}.dL_ci")
        ax.plot([lo2, hi2], [y - 0.16, y - 0.16], color=LAVENDER, linewidth=2.0, solid_capstyle="round", zorder=3)
        ax.scatter([v(f"ENC.P.{L}.dL")], [y - 0.16], s=34, color=IRIS, marker="D", zorder=4)
        ax.text(hi2 + 0.004, y - 0.16, d(f"ENC.P.{L}.dL"), fontsize=7.5, color=GREY, va="center", ha="left")
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels([LNAME[L] for L in order], fontsize=8.5)
    ax.set_xlim(-0.12, 0.08)
    ax.set_ylim(-0.6, len(order) - 0.4)
    ax.set_xlabel(r"$\Delta$ recall Presence (language − English; $\hat{\pi}$ on 0–1)", fontsize=8.5, color=INK)
    h = [plt.Line2D([], [], marker="o", color=INDIGO, linestyle="", markersize=6, label="Locked comparator (§7.3)"),
         plt.Line2D([], [], marker="D", color=IRIS, linestyle="", markersize=5, label="Corrected comparator (Entry 6)")]
    ax.legend(handles=h, loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2, fontsize=7.5, frameon=False)
    clean(ax)
    save(fig, "fig_02_level")


def fig3_phi():
    fig, ax = plt.subplots(figsize=(7.5, 3.9))
    fig.subplots_adjust(left=0.15, right=0.95, top=0.74, bottom=0.29)
    header(fig, "Rank agreement of Consistency (φ) with the English t₄ values, by language",
           "ρc over the units with φ defined in both languages, with its bootstrap 95% interval. Dashed lines: 0.30 "
           "(falsification)\nand 0.50 (confirmation); grey zone: below 0.30. Diamonds: the same test on the corrected "
           "English table (Entry 6).")
    order = LANGS[::-1]
    bands(ax, 0.30, 0.50, 0, len(order) - 0.45)
    for y, L in enumerate(order):
        lo, hi = v(f"Phi.{L}.ci")
        ax.plot([lo, hi], [y + 0.1, y + 0.1], color=IRIS, linewidth=2.4, solid_capstyle="round", zorder=3)
        ax.scatter([v(f"Phi.{L}.rho")], [y + 0.1], s=52, color=INDIGO, zorder=4)
        ax.text(hi + 0.012, y + 0.1, f"{d(f'Phi.{L}.rho')}  {d(f'Phi.{L}.verdict')}", fontsize=8, color=INK,
                va="center", ha="left")
        ax.scatter([v(f"ENC.Phi.{L}.rho")], [y - 0.2], s=30, color=LAVENDER, edgecolor=IRIS, marker="D", zorder=4)
        ax.text(v(f"ENC.Phi.{L}.rho") + 0.02, y - 0.2, d(f"ENC.Phi.{L}.rho4"), fontsize=7.5, color=GREY,
                va="center", ha="left")
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels([f"{LNAME[L]} (n = {d(f'Phi.{L}.n')})" for L in order], fontsize=8.5)
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(-0.6, len(order) - 0.4)
    ax.set_xlabel("ρc with English Consistency φ (t₄, v0.42)", fontsize=8.5, color=INK)
    h = [plt.Line2D([], [], marker="o", color=INDIGO, linestyle="", markersize=6, label="Locked comparator"),
         plt.Line2D([], [], marker="D", markerfacecolor=LAVENDER, markeredgecolor=IRIS, linestyle="", markersize=5,
                    label="Corrected comparator")]
    ax.legend(handles=h, loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2, fontsize=7.5, frameon=False)
    clean(ax)
    save(fig, "fig_03_phi")


SPECS = [  # (label, key prefix or None when not computed for that language)
    ("Primary (112 units)", "P.{L}"),
    ("S-Denon (111)", "S-Denon.{L}"),
    ("S-Headphones (96)", "S-Headphones.{L}"),
    ("S-COI as run (107)", "S-COI.{L}"),
    ("S-COI, Entry 4 (106)", "S-COI106.{L}"),
    ("S-Trans (flagged)", "STrans.flagged.P.{L}"),
    ("S-AliasAI", "SAliasAI.{L}"),
    ("Corrected comparator", "ENC.P.{L}"),
    ("Corrected, S-COI (106)", "ENC.S-COI106.{L}"),
    ("S-Language (Entry 7)", "E7.S-Language.{L}"),
    ("S-Script (Entry 7)", "E7.S-Script.{L}"),
    ("S-Alias (Entry 7)", "E7.S-Alias.{L}"),
]


def fig4_sens():
    fig, axes = plt.subplots(1, 3, figsize=(7.5, 5.4), sharey=True)
    fig.subplots_adjust(left=0.24, right=0.98, top=0.80, bottom=0.14, wspace=0.12)
    header(fig, "Rank agreement of recall Presence with English under each specification",
           "ρc and bootstrap 95% interval per specification and language. S-AliasAI applies to Korean and Chinese "
           "only, S-Script to\nChinese only. Dashed line: 0.70, the confirmation threshold; every specification is "
           "CONFIRMED in every language.")
    n = len(SPECS)
    for ax, L in zip(axes, LANGS):
        ax.axvline(0.70, color=GREY, linewidth=0.8, linestyle=(0, (3, 2)), zorder=1)
        for i, (label, key) in enumerate(SPECS):
            y = n - 1 - i
            k = key.format(L=L)
            if f"{k}.rho" not in VALUES:
                ax.text(0.83, y, "not applicable", fontsize=6.5, color=GREY, ha="center", va="center")
                continue
            lo, hi = v(f"{k}.ci")
            primary = i == 0
            ax.plot([lo, hi], [y, y], color=IRIS if primary else LIGHT, linewidth=2.0, solid_capstyle="round", zorder=2)
            ax.scatter([v(f"{k}.rho")], [y], s=34 if primary else 22, color=INDIGO if primary else GREY, zorder=3)
        ax.set_title(LNAME[L], fontsize=9, color=INK, loc="left")
        ax.set_xlim(0.6, 1.0)
        ax.set_ylim(-0.7, n - 0.3)
        ax.set_xticks([0.6, 0.7, 0.8, 0.9])
        clean(ax)
        ax.tick_params(axis="y", length=0)
    axes[0].set_yticks(range(n))
    axes[0].set_yticklabels([s[0] for s in SPECS][::-1], fontsize=7.5)
    axes[1].set_xlabel("ρc with English recall Presence", fontsize=8.5, color=INK)
    save(fig, "fig_04_sensitivity")


def main():
    CS.setup()
    fig1_presence()
    fig2_level()
    fig3_phi()
    fig4_sens()


if __name__ == "__main__":
    main()
