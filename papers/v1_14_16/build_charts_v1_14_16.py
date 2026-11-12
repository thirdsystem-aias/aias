#!/usr/bin/env python3
"""
AIAS Ranking closing paper (v1.14 + v1.16): chart builder.
One chart per finding; every plotted value is read from the locked output files
(no number is typed in by hand). Writes figures/fig_N.pdf next to this file.

Usage (from any directory):
  python3 papers/v1_14_16/build_charts_v1_14_16.py
"""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FIG = HERE / "figures"
FIG.mkdir(exist_ok=True)

M = ROOT / "osf" / "methodology"
V110 = json.loads((M / "v1_10/outputs/v1_10_verdicts.json").read_text())
V114 = json.loads((M / "v1_14/outputs/stage1/stage1_v1_14.json").read_text())
V114C = json.loads((M / "v1_14/calibration/calibration_v1_14.json").read_text())
V116 = json.loads((M / "v1_16/outputs/results_v1_16.json").read_text())

for d in (Path.home() / "Library/Fonts", Path.home() / ".fonts/Akkurat"):
    if d.exists():
        for f in d.glob("Akkurat*.otf"):
            font_manager.fontManager.addfont(str(f))
plt.rcParams["font.family"] = ["Akkurat Pro", "sans-serif"]
plt.rcParams["mathtext.fontset"] = "dejavusans"
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False

INDIGO = "#37237B"
VIOLET = "#8B6FC9"
CYAN = "#4FB3D9"
GRAY = "#6B6B6B"
LIGHT = "#E9E5F3"
FALS = "#EDEDED"
W, H = 7.2, 4.3
SRC = "tags v1.10-prereg-r2, v1.14-prereg-r2, v1.16-prereg-r1; OSF ec6wh"


def frame(title, subtitle, source):
    fig = plt.figure(figsize=(W, H))
    fig.text(0.06, 0.955, title, fontsize=12.5, fontweight="bold", color="black", va="top")
    fig.text(0.06, 0.885, subtitle, fontsize=9.5, color=GRAY, va="top")
    fig.add_artist(plt.Line2D([0.06, 0.96], [0.835, 0.835], color=INDIGO, lw=0.8))
    fig.text(0.06, 0.025, source, fontsize=7.5, color=GRAY, style="italic", va="bottom")
    ax = fig.add_axes([0.11, 0.17, 0.85, 0.6])
    return fig, ax


def bands(ax, lo=-0.25, hi=1.0):
    ax.axhspan(-0.30, 0.30, color=LIGHT, zorder=0)
    ax.axhspan(0.50, hi, color=FALS, zorder=0)
    ax.axhline(0.30, color=INDIGO, lw=0.6, ls=(0, (3, 2)))
    ax.axhline(0.50, color=GRAY, lw=0.6, ls=(0, (3, 2)))
    ax.axhline(0, color="black", lw=0.5)
    ax.set_ylim(lo, hi)


def point(ax, x, r, ci, n, color=INDIGO, label_n=True):
    ax.plot([x, x], ci, color=color, lw=1.6)
    ax.plot(x, r, "o", color=color, ms=7, zorder=5)
    ax.text(x + 0.08, r, f"{r:.3f}", fontsize=8.5, va="center", color="black")
    if label_n:
        ax.text(x, ci[0] - 0.04, f"n = {n}", fontsize=7.5, ha="center", va="top", color=GRAY)


def save(fig, name):
    fig.savefig(FIG / name)
    plt.close(fig)


# Fig 1: v1.14 Stage 1 at t4 (modal position)
fig, ax = frame("Modal-position Ranking score at t4: three correlations",
                "v1.14 Stage 1, newest panel (three models), rated units; 90% bootstrap intervals",
                "Source: osf/methodology/v1_14/outputs/stage1/stage1_v1_14.json; " + SRC)
bands(ax, -0.2, 0.8)
rows = [("H1: with Presence\n(search off)", V114["H1_Sep_Presence"]),
        ("H2: with Consistency\n(search off)", V114["H2_Sep_Consistency"]),
        ("H4_S1: with Presence\n(search on)", V114["H4_Sep_Presence_S1"])]
for i, (lab, h) in enumerate(rows):
    point(ax, i, h["rho"], h["ci90"], h["n"], INDIGO if i < 2 else VIOLET)
ax.set_xticks(range(3), [r[0] for r in rows], fontsize=9)
ax.set_xlim(-0.5, 2.6)
ax.set_ylabel(r"pooled within-category $\rho_w$", fontsize=9)
ax.text(2.55, 0.0, "confirmation band", fontsize=7.5, color=INDIGO, ha="right", va="bottom")
ax.text(2.55, 0.77, "falsification band", fontsize=7.5, color=GRAY, ha="right", va="top")
save(fig, "fig_1.pdf")


def by_wave(hkey, title, subtitle, fname, lo=-0.25, hi=0.8):
    fig, ax = frame(title, subtitle,
                    "Source: osf/methodology/v1_16/outputs/results_v1_16.json; " + SRC)
    bands(ax, lo, hi)
    waves = ["t1", "t2", "t3", "t4"]
    for i, w in enumerate(waves):
        h = V116[hkey]["per_wave"][w]
        point(ax, i, h["rho"], h["ci90"], h["n"], INDIGO if w != "t4" else VIOLET)
    labels = ["t1\nMay 2026", "t2\nJun 2026", "t3\nNov 2026", "t4\nNov 2026"]
    ax.set_xticks(range(4), labels, fontsize=9)
    ax.set_xlim(-0.5, 3.6)
    ax.set_ylabel(r"pooled within-category $\rho_w$", fontsize=9)
    ax.text(3.55, 0.0, "confirmation band", fontsize=7.5, color=INDIGO, ha="right", va="bottom")
    ax.text(3.55, hi - 0.03, "falsification band", fontsize=7.5, color=GRAY, ha="right", va="top")
    ax.text(-0.45, hi - 0.03, "legacy six-model panel (t1-t3); newest three-model panel (t4)",
            fontsize=7.5, color=GRAY, va="top")
    save(fig, fname)


by_wave("H1_Sep_Presence", "Precedence (PREC) against Presence, by wave",
        "v1.16 H1, search off, rated units; 90% bootstrap intervals", "fig_2.pdf")
by_wave("H2_Sep_Consistency", "Precedence (PREC) against Consistency, by wave",
        "v1.16 H2, search off, units rated on both; 90% bootstrap intervals", "fig_3.pdf")

# Fig 4: retest, observed against shuffled
fig, ax = frame("Retest correlation of PREC: observed and shuffled order",
                "v1.16 H3 (three weeks) and H5 (five months); shuffled = mean of 10,000 within-answer shuffles",
                "Source: osf/methodology/v1_16/outputs/results_v1_16.json; " + SRC)
ax.axhline(0, color="black", lw=0.5)
ax.axhline(0.50, color=GRAY, lw=0.6, ls=(0, (3, 2)))
ax.text(1.75, 0.51, "0.50 (confirmation threshold)", fontsize=7.5, color=GRAY, ha="right", va="bottom")
for i, (lab, key) in enumerate([("t1 to t2 (H3)", "H3_Retest_t1_t2"), ("t2 to t3 (H5)", "H5_Retest_t2_t3")]):
    h = V116[key]
    ax.bar(i - 0.18, h["rho"], width=0.34, color=INDIGO)
    ax.plot([i - 0.18, i - 0.18], h["ci90"], color="black", lw=1)
    ax.text(i - 0.18, h["ci90"][1] + 0.02, f"{h['rho']:.3f}\nn = {h['n']}", ha="center", va="bottom", fontsize=8)
    ax.bar(i + 0.18, h["shuffled_mean_rho"], width=0.34, color=CYAN)
    ax.text(i + 0.18, max(h["shuffled_mean_rho"], 0) + 0.02, f"{h['shuffled_mean_rho']:.4f}",
            ha="center", va="bottom", fontsize=8)
ax.set_xticks([0, 1], ["t1 to t2 (H3)", "t2 to t3 (H5)"], fontsize=9)
ax.set_ylim(-0.05, 1.15)
ax.set_xlim(-0.6, 1.8)
ax.set_ylabel(r"pooled within-category $\rho_w$", fontsize=9)
ax.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=INDIGO), plt.Rectangle((0, 0), 1, 1, color=CYAN)],
          labels=["observed", "shuffled (null mean)"], fontsize=8, frameon=False, loc="upper right")
save(fig, "fig_4.pdf")

# Fig 5: three statistics against Presence, by wave
fig, ax = frame("Correlation with Presence of three Ranking statistics, t1 to t4",
                "MNP (v1.10), MODE (v1.14) and PREC (v1.16); same units, rating floor and pooling",
                "Source: v1_10_verdicts.json; calibration_v1_14.json; stage1_v1_14.json; results_v1_16.json; OSF ec6wh")
bands(ax, -0.05, 0.8)
mnp = [V110["H1_Sep_Presence"]["per_wave"][w]["rho"] for w in ("t1", "t2", "t3")] + \
      [V114["sensitivities"]["S3_candidate_MNP"]["H1"]["rho"]]
mode = [V114C["H1_Sep_Presence"]["per_wave"][w]["rho"] for w in ("t1", "t2", "t3")] + [V114["H1_Sep_Presence"]["rho"]]
prec = [V116["H1_Sep_Presence"]["per_wave"][w]["rho"] for w in ("t1", "t2", "t3", "t4")]
x = range(4)
ax.plot(x, mnp, "-o", color=VIOLET, lw=1.4, ms=5, label="MNP (v1.10; t4 from v1.14 sensitivity S3)")
ax.plot(x, mode, "-s", color=CYAN, lw=1.4, ms=5, label="MODE (v1.14; t1-t3 calibration, t4 confirmatory)")
ax.plot(x, prec, "-o", color=INDIGO, lw=2.0, ms=6, label="PREC (v1.16)")
ax.set_xticks(range(4), ["t1", "t2", "t3", "t4"], fontsize=9)
ax.set_xlim(-0.3, 3.3)
ax.set_ylabel(r"$\rho_w$ with Presence", fontsize=9)
ax.legend(fontsize=7.5, frameon=False, loc="upper left")
save(fig, "fig_5.pdf")

# Fig 6: exploratory moderators
fig, ax = frame("Within-category correlation with Presence and first-position concentration",
                "v1.16 E1 (exploratory); one point per category and wave (20 cells), search off",
                "Source: results_v1_16.json, E1_moderators.cells; " + SRC)
ax.axhline(0, color="black", lw=0.5)
names = {"v0.19": "Headphones (16 brands)", "v0.20": "Skincare (24)", "v0.21": "Cosmetics (24)",
         "v0.22": "Automotive (24)", "v0.23": "Spirits (24)"}
style = {"v0.19": (INDIGO, "o"), "v0.20": (CYAN, "s"), "v0.21": (VIOLET, "^"),
         "v0.22": (GRAY, "D"), "v0.23": ("#B9A8E0", "v")}
for cat in names:
    cells = [c for c in V116["E1_moderators"]["cells"] if c["category"] == cat]
    c, mk = style[cat]
    ax.scatter([e["first_position_concentration"] for e in cells], [e["rho_PREC_P"] for e in cells],
               color=c, marker=mk, s=42, label=names[cat], zorder=3)
ax.set_xlabel("first-position concentration (share of rankable answers led by the modal first brand)", fontsize=8.5)
ax.set_ylabel(r"within-category Spearman $\rho$(PREC, P)", fontsize=9)
ax.set_ylim(-0.9, 1.0)
ax.legend(fontsize=7.5, frameon=False, loc="lower right", ncol=2)
save(fig, "fig_6.pdf")
print("charts written to", FIG)
