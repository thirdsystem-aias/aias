#!/usr/bin/env python3
"""
v0.26 chart builder — C_P × Amazon BSR scatter (Figure 1)
=========================================================
Discriminant-validity scatter referenced as Figure 1 in
papers/v0_26/v0_26_amazon_bsr_predictive_validity.md.

2x2 grid: kitchen knives (v0.16), audiophile headphones (v0.19),
skincare (v0.20), cosmetics (v0.21). One dot per listed brand.

Sources mirror score_v26.py:
    v0.16 → osf/v26/data/v16_cp_retrofit_aggregated.csv  (brand,cp,n_models)
    v0.19 → osf/v19/phase_a_results.csv  (aggregate recognition_yes by brand)
    v0.20 → osf/v20/v20_verdicts.json    (phase_a.per_brand.<brand>.cp)
    v0.21 → osf/v21/v21_verdicts.json    (same)
    BSR  → osf/v26/data/v26_bsr_<substrate>.csv  (listed brands only)

Output:
    reports/figs/v26/chart_26_cp_vs_bsr_scatter.pdf
"""

from collections import defaultdict
from pathlib import Path
import csv
import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import spearmanr

# Allow import of chart_style from scripts/
sys.path.insert(0, str(Path(__file__).resolve().parent))
import chart_style as cs

cs.setup()

AIAS_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = AIAS_ROOT / "reports" / "figs" / "v26"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PDF = OUT_DIR / "chart_26_cp_vs_bsr_scatter.pdf"

PHASE = "v0.26"

# Panel order, top-left → bottom-right
SUBSTRATES = [
    ("kitchen_knives",        "Kitchen knives (v0.16)"),
    ("audiophile_headphones", "Audiophile headphones (v0.19)"),
    ("skincare",              "Skincare (v0.20)"),
    ("cosmetics",             "Cosmetics (v0.21)"),
]


# -----------------------------------------------------------------------------
# C_P loaders (one per substrate, matching score_v26.py provenance)
# -----------------------------------------------------------------------------

def load_cp_kitchen_knives() -> dict[str, int]:
    p = AIAS_ROOT / "osf" / "v26" / "data" / "v16_cp_retrofit_aggregated.csv"
    out = {}
    with open(p) as f:
        for row in csv.DictReader(f):
            out[row["brand"]] = int(row["cp"])
    return out


def load_cp_audiophile() -> dict[str, int]:
    p = AIAS_ROOT / "osf" / "v19" / "phase_a_results.csv"
    counts: dict[str, int] = defaultdict(int)
    with open(p) as f:
        for row in csv.DictReader(f):
            counts[row["brand"]] += int(row["recognition_yes"])
    return dict(counts)


def load_cp_from_verdicts(verdicts_path: Path) -> dict[str, int]:
    with open(verdicts_path) as f:
        d = json.load(f)
    return {brand: entry["cp"] for brand, entry in d["phase_a"]["per_brand"].items()}


CP_LOADERS = {
    "kitchen_knives":        load_cp_kitchen_knives,
    "audiophile_headphones": load_cp_audiophile,
    "skincare":              lambda: load_cp_from_verdicts(AIAS_ROOT / "osf" / "v20" / "v20_verdicts.json"),
    "cosmetics":             lambda: load_cp_from_verdicts(AIAS_ROOT / "osf" / "v21" / "v21_verdicts.json"),
}


def load_bsr(substrate: str) -> dict[str, int]:
    """Listed brands only; absent rows skipped."""
    p = AIAS_ROOT / "osf" / "v26" / "data" / f"v26_bsr_{substrate}.csv"
    out = {}
    with open(p) as f:
        for row in csv.DictReader(f):
            if row.get("amazon_status") != "listed":
                continue
            try:
                out[row["brand"]] = int(row["bsr_rank"])
            except (ValueError, KeyError):
                continue
    return out


def merge_substrate(substrate: str) -> list[tuple[str, int, int]]:
    cp = CP_LOADERS[substrate]()
    bsr = load_bsr(substrate)
    return [(brand, cp[brand], bsr[brand]) for brand in cp if brand in bsr]


# -----------------------------------------------------------------------------
# Chart
# -----------------------------------------------------------------------------

def build():
    fig, axes = plt.subplots(2, 2, figsize=cs.FIGSIZE["hero_tall"])
    axes_flat = axes.flatten()

    rng = np.random.default_rng(seed=42)  # deterministic jitter

    for ax, (substrate, panel_title) in zip(axes_flat, SUBSTRATES):
        pairs = merge_substrate(substrate)
        if not pairs:
            ax.text(0.5, 0.5, "no data", ha="center", va="center",
                    transform=ax.transAxes, color=cs.GRAY,
                    fontsize=cs.FONT_SIZES["annotation"])
            ax.set_title(panel_title, fontsize=cs.FONT_SIZES["axis_label"],
                         color=cs.BLACK, loc="left", pad=4)
            ax.set_xticks([]); ax.set_yticks([])
            continue

        brands, cps, bsrs = zip(*pairs)
        cps_arr = np.array(cps, dtype=float)
        bsrs_arr = np.array(bsrs, dtype=float)

        # Slight horizontal jitter so points at same C_P don't overplot
        jitter = rng.uniform(-0.15, 0.15, size=len(cps_arr))
        x_plot = cps_arr + jitter

        ax.scatter(x_plot, bsrs_arr,
                   s=22, color=cs.INDIGO, alpha=0.75, edgecolors="none")

        ax.set_yscale("log")
        ax.set_xlim(-0.5, 6.5)
        ax.set_xticks([0, 1, 2, 3, 4, 5, 6])
        ax.set_xlabel(r"$C_P$ (0–6)", fontsize=cs.FONT_SIZES["axis_label"])
        ax.set_ylabel("BSR (log scale)", fontsize=cs.FONT_SIZES["axis_label"])
        ax.set_title(panel_title, fontsize=cs.FONT_SIZES["axis_label"],
                     color=cs.BLACK, loc="left", pad=4)
        ax.tick_params(axis="both", labelsize=cs.FONT_SIZES["axis_tick"])
        ax.grid(True, which="major", axis="y", linestyle=":",
                linewidth=0.5, color=cs.PALETTE["gray_light"], alpha=0.7)
        ax.set_axisbelow(True)

        # Annotation: ρ / p / n, or ceiling note for cosmetics
        if len(set(cps_arr)) <= 1:
            note = "ceiling: all $C_P=6$\n$\\rho$ undefined"
        else:
            rho, pval = spearmanr(cps_arr, bsrs_arr)
            note = f"$\\rho = {rho:+.3f}$\n$p = {pval:.3f}$\n$n = {len(brands)}$"
        ax.text(0.97, 0.97, note,
                transform=ax.transAxes, ha="right", va="top",
                fontsize=cs.FONT_SIZES["annotation"], color=cs.BLACK,
                bbox=dict(facecolor="white",
                          edgecolor=cs.PALETTE["gray_light"],
                          boxstyle="round,pad=0.3", linewidth=0.5))

    cs.add_header(
        fig,
        "AI Presence does not predict Amazon BSR",
        r"$C_P$ (0–6) vs. Amazon Best Sellers Rank by substrate",
        r"Listed brands only; one dot per brand. Spearman $\rho$ tests within-substrate monotonicity.",
    )
    cs.add_footer(
        fig,
        verdict=r"$\mathrm{H_{PV\_Primary}}$ FALSIFIED — 0 of 3 testable substrates met threshold.",
        phase=PHASE,
    )

    plt.subplots_adjust(top=0.84, bottom=0.11, left=0.09, right=0.97,
                        wspace=0.32, hspace=0.42)

    fig.savefig(OUT_PDF, **cs.SAVEFIG_PARAMS)
    print(f"✓ Wrote {OUT_PDF.relative_to(AIAS_ROOT)}  ({OUT_PDF.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
