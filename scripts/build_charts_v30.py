#!/usr/bin/env python3
"""
build_charts_v30.py — AIAS 2.0 CPC instrument pilot, four figures.

Replaces the inherited v0.28 chart builder WHOLESALE. Reads the locked CPC
scores from osf/v30/data/v30_cpc.csv and the locked stats from
osf/v30/v30_cpc_verdicts.json (single-source); outputs to reports/figs/v30/.

  chart_30_coverage.pdf    (Fig 1) grouped bar: recall vs recognition coverage
  chart_30_confound.pdf    (Fig 2) scatter: cpc_raw vs recognition level L
  chart_30_correction.pdf  (Fig 3) two-panel skincare: raw vs corrected vs L
  chart_30_variation.pdf   (Fig 4) box+strip: cpc_corr by category

Uses chart_style.py (Akkurat Pro; Indigo #37237B primary; TS data-viz palette).
Build tooling — NOT a pre-reg artifact.
"""
import csv
import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import chart_style as cs

ROOT = Path.home() / "aias"
CSV_PATH = ROOT / "osf/v30/data/v30_cpc.csv"
VERDICTS = ROOT / "osf/v30/v30_cpc_verdicts.json"
FIG_DIR = ROOT / "reports/figs/v30"

SUB = {"v0.20": "skincare", "v0.21": "cosmetics", "v0.22": "automotive"}
ORDER = ["v0.20", "v0.21", "v0.22"]
CATCOLOR = {"v0.20": cs.INDIGO, "v0.21": cs.WARM, "v0.22": cs.TEAL}
RECOG_NEUTRAL = cs.PALETTE["gray_light"]
JITTER_SEED = 280400


def _f(x):
    if x is None or x == "" or x == "None":
        return None
    return float(x)


def load_rows():
    rows = []
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append({
                "brand": r["brand"], "substrate": r["substrate"],
                "mu": _f(r["mu"]), "sd_pop": _f(r["sd_pop"]),
                "cpc_raw": _f(r["cpc_raw"]), "cpc_corr": _f(r["cpc_corr"]),
                "cpc_resid": _f(r["cpc_resid"]),
                "L": int(float(r["L"])),
                "recall_defined": r["recall_defined"] == "True",
                "recog_defined": r["recog_defined"] == "True",
            })
    return rows


def by_sub(rows, sub):
    return [r for r in rows if r["substrate"] == sub]


def _adjust(fig, **kw):
    base = {"top": 0.80, "bottom": 0.19, "left": 0.11, "right": 0.96}
    base.update(kw)
    fig.subplots_adjust(**base)


def save(fig, stem):
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    out = FIG_DIR / f"{stem}.pdf"
    fig.savefig(out, **cs.SAVEFIG_PARAMS)
    plt.close(fig)
    print(f"  wrote {out}")


# ---------------------------------------------------------------------------
# Fig 1 — coverage grouped bar
# ---------------------------------------------------------------------------
def fig_coverage(rows):
    recall_cov, recog_cov = [], []
    for s in ORDER:
        rs = by_sub(rows, s)
        n = len(rs)
        recall_cov.append(100.0 * sum(r["recall_defined"] for r in rs) / n)
        recog_cov.append(100.0 * sum(r["recog_defined"] for r in rs) / n)

    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    x = np.arange(len(ORDER))
    w = 0.38
    ax.bar(x - w / 2, recall_cov, w, color=cs.INDIGO, label="recall-based consistency")
    ax.bar(x + w / 2, recog_cov, w, color=RECOG_NEUTRAL, label="recognition-based consistency")
    for xi, (rv, gv) in enumerate(zip(recall_cov, recog_cov)):
        ax.text(xi - w / 2, rv + 1.5, f"{rv:.0f}%", ha="center", va="bottom",
                fontsize=cs.FONT_SIZES["data_label"], color=cs.INDIGO, fontweight="bold")
        ax.text(xi + w / 2, gv + 1.5, f"{gv:.0f}%", ha="center", va="bottom",
                fontsize=cs.FONT_SIZES["data_label"], color=cs.GRAY)

    ci = ORDER.index("v0.21")
    ax.annotate("79% vs 0% —\nrecognition gives\nno signal at all",
                xy=(ci + w / 2, 3), xytext=(ci + 0.05, 46),
                fontsize=cs.FONT_SIZES["annotation"], color=cs.BLACK, ha="left",
                arrowprops=dict(arrowstyle="->", color=cs.GRAY, lw=0.8))

    ax.set_xticks(x)
    ax.set_xticklabels([SUB[s] for s in ORDER], fontsize=cs.FONT_SIZES["axis_tick"])
    ax.set_ylim(0, 100)
    ax.set_ylabel("% of brands with a defined consistency score",
                  fontsize=cs.FONT_SIZES["axis_label"])
    ax.legend(loc="upper right", fontsize=cs.FONT_SIZES["legend"])
    _adjust(fig)
    cs.add_header(fig, "Recall yields a consistency signal where recognition cannot",
                  "Share of 24 brands per category with a defined consistency score, by signal")
    cs.add_footer(fig, verdict="P1 Established — recall coverage 79% / 79% / 62% vs recognition 17% / 0% / 4%",
                  phase="v0.30")
    save(fig, "chart_30_coverage")


# ---------------------------------------------------------------------------
# Fig 2 — confound scatter
# ---------------------------------------------------------------------------
def fig_confound(rows, stats):
    rho_sk = stats["F2"]["v0.20"]["rho"]
    p_sk = stats["F2"]["v0.20"]["p"]
    rng = np.random.default_rng(JITTER_SEED)

    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    ymax = 0.0
    for s in ORDER:
        pts = [r for r in by_sub(rows, s) if r["recall_defined"] and r["cpc_raw"] is not None]
        xs = np.array([r["L"] for r in pts], float)
        ys = np.array([r["cpc_raw"] for r in pts], float)
        ymax = max(ymax, ys.max() if len(ys) else 0)
        jit = rng.uniform(-0.16, 0.16, size=len(xs)) if s != "v0.20" else np.zeros(len(xs))
        ax.scatter(xs + jit, ys, s=34, color=CATCOLOR[s], alpha=0.8,
                   edgecolor="white", linewidth=0.4, label=SUB[s], zorder=3)

    sk = [r for r in by_sub(rows, "v0.20") if r["recall_defined"] and r["cpc_raw"] is not None]
    sx = np.array([r["L"] for r in sk], float)
    sy = np.array([r["cpc_raw"] for r in sk], float)
    m, b = np.polyfit(sx, sy, 1)
    xline = np.linspace(sx.min(), sx.max(), 50)
    ax.plot(xline, m * xline + b, color=cs.INDIGO, lw=1.6, zorder=2)

    ax.set_xlim(-0.5, 6.7)
    ax.set_ylim(0, ymax * 1.18)
    ytop = ax.get_ylim()[1]
    ax.text(2.7, ytop * 0.93, f"skincare: rho = {rho_sk:.2f}  (p = {p_sk:.2f})",
            fontsize=cs.FONT_SIZES["annotation"], color=cs.INDIGO, fontweight="bold")
    ax.annotate("recognition saturated —\nbias untestable",
                xy=(6, ymax * 0.5), xytext=(3.9, ytop * 0.72),
                fontsize=cs.FONT_SIZES["annotation"], color=cs.BLACK, ha="left",
                arrowprops=dict(arrowstyle="->", color=cs.GRAY, lw=0.8))

    ax.set_xlabel("recognition level  L  (C_P, 0–6)", fontsize=cs.FONT_SIZES["axis_label"])
    ax.set_ylabel("raw consistency  (CPC_raw)", fontsize=cs.FONT_SIZES["axis_label"])
    ax.legend(loc="upper left", fontsize=cs.FONT_SIZES["legend"])
    _adjust(fig)
    cs.add_header(fig, "Raw consistency tracks prominence — where prominence still varies",
                  "Raw consistency vs recognition level, recall-defined brands, by category")
    cs.add_footer(fig, verdict="P2 Demonstrated where testable — confound present in skincare only",
                  phase="v0.30")
    save(fig, "chart_30_confound")


# ---------------------------------------------------------------------------
# Fig 3 — correction, two panels (skincare only)
# ---------------------------------------------------------------------------
def fig_correction(rows, stats):
    rho_raw = stats["F2"]["v0.20"]["rho"]
    rho_corr = stats["F3"]["v0.20"]["rho"]
    atten = stats["F3"]["v0.20"]["attenuation"]

    sk = [r for r in by_sub(rows, "v0.20") if r["recall_defined"]
          and r["cpc_raw"] is not None and r["cpc_corr"] is not None]
    L = np.array([r["L"] for r in sk], float)
    raw = np.array([r["cpc_raw"] for r in sk], float)
    corr = np.array([r["cpc_corr"] for r in sk], float)

    fig, (axL, axR) = plt.subplots(1, 2, figsize=cs.FIGSIZE["spread"], sharey=True)
    for ax, y, color, lab, rho, ns in [
        (axL, raw, cs.WARM, "raw  (CPC_raw)", rho_raw, ""),
        (axR, corr, cs.INDIGO, "corrected  (CPC_corr)", rho_corr, "  n.s."),
    ]:
        ax.scatter(L, y, s=36, color=color, alpha=0.85, edgecolor="white", linewidth=0.4, zorder=3)
        m, b = np.polyfit(L, y, 1)
        xline = np.linspace(L.min(), L.max(), 50)
        ax.plot(xline, m * xline + b, color=color, lw=1.6, zorder=2)
        ax.set_title(f"{lab}\nrho = {rho:.2f}{ns}", fontsize=cs.FONT_SIZES["subtitle"],
                     color=color, fontweight="bold")
        ax.set_xlabel("recognition level L (C_P)", fontsize=cs.FONT_SIZES["axis_label"])
    axL.set_ylabel("consistency", fontsize=cs.FONT_SIZES["axis_label"])

    fig.text(0.5, 0.85, f"{atten*100:.0f}% attenuation", ha="center", va="bottom",
             fontsize=cs.FONT_SIZES["data_label"], color=cs.BLACK, fontweight="bold")
    _adjust(fig, top=0.77, bottom=0.20, left=0.09, right=0.97, wspace=0.12)
    cs.add_header(fig, "The level-correction removes the prominence bias (skincare)",
                  "Skincare brands: raw vs level-corrected consistency against recognition level")
    cs.add_footer(fig, verdict=f"P3 Validated where testable — {atten*100:.0f}% attenuation, corrected rho n.s.",
                  phase="v0.30")
    save(fig, "chart_30_correction")


# ---------------------------------------------------------------------------
# Fig 4 — variation box + strip
# ---------------------------------------------------------------------------
def fig_variation(rows, stats):
    H = stats["F4"]["H"]
    rng = np.random.default_rng(JITTER_SEED)

    data, colors = [], []
    for s in ORDER:
        vals = [r["cpc_corr"] for r in by_sub(rows, s)
                if r["recall_defined"] and r["cpc_corr"] is not None]
        data.append(vals)
        colors.append(CATCOLOR[s])

    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    positions = np.arange(1, len(ORDER) + 1)
    bp = ax.boxplot(data, positions=positions, widths=0.5, patch_artist=True,
                    showfliers=False, medianprops=dict(color=cs.BLACK, lw=1.2),
                    whiskerprops=dict(color=cs.GRAY, lw=0.8),
                    capprops=dict(color=cs.GRAY, lw=0.8), boxprops=dict(lw=0.8))
    for patch, c in zip(bp["boxes"], colors):
        patch.set_facecolor(c); patch.set_alpha(0.22); patch.set_edgecolor(c)
    for i, (vals, c) in enumerate(zip(data, colors)):
        jit = rng.uniform(-0.13, 0.13, size=len(vals))
        ax.scatter(positions[i] + jit, vals, s=28, color=c, alpha=0.85,
                   edgecolor="white", linewidth=0.4, zorder=3)

    ax.set_xticks(positions)
    ax.set_xticklabels([SUB[s] for s in ORDER], fontsize=cs.FONT_SIZES["axis_tick"])
    ax.set_ylabel("corrected consistency (CPC_corr)", fontsize=cs.FONT_SIZES["axis_label"])
    ax.set_aspect("auto")
    ax.annotate(f"Kruskal–Wallis  H = {H:.2f},  p < 0.001",
                xy=(0.5, 0.97), xycoords="axes fraction", ha="center", va="top",
                fontsize=cs.FONT_SIZES["annotation"], color=cs.BLACK)
    _adjust(fig)
    cs.add_header(fig, "Consistency differs by category",
                  "Corrected consistency (CPC_corr) per recall-defined brand, by category")
    cs.add_footer(fig, verdict=f"P4 Established — H = {H:.2f}, p < 0.001 across the three categories",
                  phase="v0.30")
    save(fig, "chart_30_variation")


def main():
    rows = load_rows()
    v = json.load(open(VERDICTS))
    stats = {
        "F2": v["F2_H_CPC_LevelConfound"]["per_substrate"],
        "F3": v["F3_H_CPC_LevelCorrected"]["per_substrate"],
        "F4": {"H": v["F4_H_CPC_SubstrateVariation"]["kruskal_H"],
               "p": v["F4_H_CPC_SubstrateVariation"]["kruskal_p"]},
    }
    cs.setup()
    print("building v0.30 CPC figures ->", FIG_DIR)
    fig_coverage(rows)
    fig_confound(rows, stats)
    fig_correction(rows, stats)
    fig_variation(rows, stats)
    print("done.")


if __name__ == "__main__":
    main()
