#!/usr/bin/env python3
"""
v0.29 chart builder — 4 figures for the brand-format report
============================================================

Figure 1 — chart_26_cp_vs_bsr_scatter.pdf
    2x2 scatter: C_P × BSR per substrate (the headline discriminant figure).
    Also referenced as Figure 1 by the SSRN paper.

Figure 2 — chart_26_cosmetics_ceiling.pdf
    Horizontal bar of 24 cosmetics brands sorted by BSR, all at C_P = 6.
    Visualizes the natural experiment behind Pattern 2 (the ceiling).

Figure 3 — chart_26_convergent_vs_discriminant.pdf
    Two-panel side-by-side: v0.25 C_P × Google Trends (convergent, ρ ≈ +0.74)
    next to v0.29 pooled C_P × BSR (discriminant, ρ ≈ 0).
    Visualizes Pattern 3 (convergent + discriminant = construct validity).

Figure 4 — chart_26_skincare_dgp_contrast.pdf
    Horizontal bar of skincare brands sorted by BSR, color-coded by cell
    (Cell A prestige / Cell B celeb-cult / Cell C clinical). Demonstrates
    Pattern 4: within constant C_P, channel-fit drives BSR.

Sources mirror score_v29.py:
    v0.16 → osf/v29/data/v16_cp_retrofit_aggregated.csv  (brand,cp,n_models)
    v0.19 → osf/v19/phase_a_results.csv  (aggregate recognition_yes by brand)
    v0.20 → osf/v20/v20_verdicts.json    (phase_a.per_brand.<brand>.{cp,cell})
    v0.21 → osf/v21/v21_verdicts.json    (same)
    v0.25 → osf/v25/data/v25_merged_presence_trends.csv  (brand,C_P,trends_normalized)
    BSR  → osf/v29/data/v29_bsr_<substrate>.csv  (listed brands only)
"""

from collections import defaultdict
from pathlib import Path
import csv
import json
import sys

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import spearmanr

# Allow import of chart_style from scripts/
sys.path.insert(0, str(Path(__file__).resolve().parent))
import chart_style as cs

cs.setup()

AIAS_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = AIAS_ROOT / "reports" / "figs" / "v29"
OUT_DIR.mkdir(parents=True, exist_ok=True)

OUT_PDF_SCATTER     = OUT_DIR / "chart_26_cp_vs_bsr_scatter.pdf"
OUT_PDF_CEILING     = OUT_DIR / "chart_26_cosmetics_ceiling.pdf"
OUT_PDF_CONVERGENT  = OUT_DIR / "chart_26_convergent_vs_discriminant.pdf"
OUT_PDF_SKINCARE    = OUT_DIR / "chart_26_skincare_dgp_contrast.pdf"

PHASE = "v0.29"

# Panel order for the 2x2 scatter
SUBSTRATES = [
    ("kitchen_knives",        "Kitchen knives (v0.16)"),
    ("audiophile_headphones", "Audiophile headphones (v0.19)"),
    ("skincare",              "Skincare (v0.20)"),
    ("cosmetics",             "Cosmetics (v0.21)"),
]


# -----------------------------------------------------------------------------
# C_P loaders (one per substrate, matching score_v29.py provenance)
# -----------------------------------------------------------------------------

def load_cp_kitchen_knives() -> dict[str, int]:
    p = AIAS_ROOT / "osf" / "v29" / "data" / "v16_cp_retrofit_aggregated.csv"
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
    p = AIAS_ROOT / "osf" / "v29" / "data" / f"v29_bsr_{substrate}.csv"
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


def load_v25_convergent() -> list[tuple[str, float, float]]:
    """v0.25 B2B SaaS: (brand, presence_composite, trends_normalized).

    Uses presence_composite (v1.5 multi-component AI Availability, 0-100)
    rather than raw C_P because all 24 v0.25 brands scored C_P = 6 (ceiling) —
    the paper's reported ρ = 0.741 was on presence_composite × trends.
    """
    p = AIAS_ROOT / "osf" / "v25" / "data" / "v25_merged_presence_trends.csv"
    out = []
    with open(p) as f:
        for row in csv.DictReader(f):
            try:
                out.append((row["brand"],
                            float(row["presence_composite"]),
                            float(row["trends_normalized"])))
            except (ValueError, KeyError):
                continue
    return out


def load_skincare_with_cells() -> list[tuple[str, int, str]]:
    """v0.20 skincare: (brand, cp, cell) for each brand in phase_a/per_brand."""
    p = AIAS_ROOT / "osf" / "v20" / "v20_verdicts.json"
    with open(p) as f:
        d = json.load(f)
    return [(b, e["cp"], e["cell"]) for b, e in d["phase_a"]["per_brand"].items()]


# -----------------------------------------------------------------------------
# Figure 1 — 2x2 C_P × BSR scatter (existing)
# -----------------------------------------------------------------------------

def build_scatter():
    fig, axes = plt.subplots(2, 2, figsize=cs.FIGSIZE["hero_tall"])
    axes_flat = axes.flatten()

    rng = np.random.default_rng(seed=42)

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

    fig.savefig(OUT_PDF_SCATTER, **cs.SAVEFIG_PARAMS)
    plt.close(fig)
    print(f"✓ Wrote {OUT_PDF_SCATTER.relative_to(AIAS_ROOT)}  ({OUT_PDF_SCATTER.stat().st_size} bytes)")


# -----------------------------------------------------------------------------
# Figure 2 — cosmetics ceiling horizontal bar
# -----------------------------------------------------------------------------

def build_cosmetics_ceiling():
    cp = CP_LOADERS["cosmetics"]()
    bsr = load_bsr("cosmetics")
    pairs = [(b, bsr[b]) for b in cp if b in bsr]
    pairs.sort(key=lambda x: x[1])  # ascending BSR (best at top)

    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero_tall"])
    brands, bsrs = zip(*pairs)
    y_pos = np.arange(len(brands))

    ax.barh(y_pos, bsrs, color=cs.INDIGO, alpha=0.85, edgecolor="none", height=0.7)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(brands, fontsize=cs.FONT_SIZES["data_label"])
    ax.set_xscale("log")
    ax.set_xlabel("Amazon BSR (log scale — lower = more sales)",
                  fontsize=cs.FONT_SIZES["axis_label"])
    ax.tick_params(axis="both", labelsize=cs.FONT_SIZES["axis_tick"])
    ax.invert_yaxis()
    ax.grid(True, which="major", axis="x", linestyle=":",
            linewidth=0.5, color=cs.PALETTE["gray_light"], alpha=0.7)
    ax.set_axisbelow(True)

    ax.text(0.97, 0.04,
            "All 24 brands score\n$C_P$ = 6 in Phase A",
            transform=ax.transAxes, ha="right", va="bottom",
            fontsize=cs.FONT_SIZES["annotation"], color=cs.BLACK,
            bbox=dict(facecolor="white",
                      edgecolor=cs.PALETTE["gray_light"],
                      boxstyle="round,pad=0.4", linewidth=0.5))

    cs.add_header(
        fig,
        "Cosmetics ceiling: identical AI Presence, vast BSR spread",
        "24 cosmetics brands sorted by Amazon Best Sellers Rank",
        "Maybelline (BSR 12) to Anastasia Beverly Hills (BSR 29,364) — a 2,400-to-1 sales-velocity ratio at constant $C_P$.",
    )
    cs.add_footer(fig, verdict="Pattern 2: The ceiling demonstrates construct independence.", phase=PHASE)

    plt.subplots_adjust(top=0.85, bottom=0.09, left=0.24, right=0.96)
    fig.savefig(OUT_PDF_CEILING, **cs.SAVEFIG_PARAMS)
    plt.close(fig)
    print(f"✓ Wrote {OUT_PDF_CEILING.relative_to(AIAS_ROOT)}  ({OUT_PDF_CEILING.stat().st_size} bytes)")


# -----------------------------------------------------------------------------
# Figure 3 — convergent (v0.25) vs discriminant (v0.29) two-panel comparison
# -----------------------------------------------------------------------------

def build_convergent_discriminant():
    from scipy.stats import rankdata
    v25 = load_v25_convergent()
    v29_pairs = []
    for substrate, _ in SUBSTRATES:
        cp = CP_LOADERS[substrate]()
        bsr = load_bsr(substrate)
        sub_pairs = [(b, cp[b], bsr[b]) for b in cp if b in bsr]
        if len(sub_pairs) < 2:
            continue
        # Within-substrate BSR percentile (smaller BSR = better = lower pct);
        # matches score_v29.py's canonical pooled analysis.
        ranks = rankdata([p[2] for p in sub_pairs], method="average")
        pct = (ranks - 1) / (len(ranks) - 1) * 100
        for (b, c, _), pp in zip(sub_pairs, pct):
            v29_pairs.append((b, c, pp))

    fig, axes = plt.subplots(1, 2, figsize=cs.FIGSIZE["hero"])
    rng = np.random.default_rng(seed=42)

    # Left — convergent (v0.25 B2B SaaS); presence_composite × trends
    presence25 = np.array([d[1] for d in v25], dtype=float)
    trends25 = np.array([d[2] for d in v25], dtype=float)
    rho25, p25 = spearmanr(presence25, trends25)
    axes[0].scatter(presence25, trends25, s=22, color=cs.INDIGO,
                    alpha=0.80, edgecolors="none")
    axes[0].set_xlim(0, 100)
    axes[0].set_xlabel("AIAS Presence (v1.5 composite, 0–100)",
                       fontsize=cs.FONT_SIZES["axis_label"])
    axes[0].set_ylabel("Google Trends search interest", fontsize=cs.FONT_SIZES["axis_label"])
    axes[0].set_title("Convergent: v0.25 B2B SaaS", fontsize=cs.FONT_SIZES["axis_label"],
                      color=cs.BLACK, loc="left", pad=4)
    axes[0].tick_params(axis="both", labelsize=cs.FONT_SIZES["axis_tick"])
    axes[0].grid(True, which="major", linestyle=":",
                 linewidth=0.5, color=cs.PALETTE["gray_light"], alpha=0.7)
    axes[0].set_axisbelow(True)
    axes[0].text(0.05, 0.97,
                 f"$\\rho = {rho25:+.3f}$\n$p = {p25:.3f}$\n$n = {len(presence25)}$",
                 transform=axes[0].transAxes, ha="left", va="top",
                 fontsize=cs.FONT_SIZES["annotation"], color=cs.BLACK,
                 bbox=dict(facecolor="white",
                           edgecolor=cs.PALETTE["gray_light"],
                           boxstyle="round,pad=0.3", linewidth=0.5))

    # Right — discriminant (v0.29 pooled across 4 substrates)
    cps26 = np.array([d[1] for d in v29_pairs], dtype=float)
    bsrs26 = np.array([d[2] for d in v29_pairs], dtype=float)
    rho26, p26 = spearmanr(cps26, bsrs26)
    jitter26 = rng.uniform(-0.15, 0.15, size=len(cps26))
    axes[1].scatter(cps26 + jitter26, bsrs26, s=22, color=cs.WARM,
                    alpha=0.70, edgecolors="none")
    axes[1].set_xlim(-0.5, 6.5)
    axes[1].set_ylim(-5, 105)
    axes[1].set_xticks([0, 1, 2, 3, 4, 5, 6])
    axes[1].set_xlabel(r"$C_P$ (v0.29)", fontsize=cs.FONT_SIZES["axis_label"])
    axes[1].set_ylabel("BSR percentile by substrate", fontsize=cs.FONT_SIZES["axis_label"])
    axes[1].set_title("Discriminant: v0.29 pooled cross-substrate",
                      fontsize=cs.FONT_SIZES["axis_label"], color=cs.BLACK, loc="left", pad=4)
    axes[1].tick_params(axis="both", labelsize=cs.FONT_SIZES["axis_tick"])
    axes[1].grid(True, which="major", axis="y", linestyle=":",
                 linewidth=0.5, color=cs.PALETTE["gray_light"], alpha=0.7)
    axes[1].set_axisbelow(True)
    axes[1].text(0.05, 0.97,
                 f"$\\rho = {rho26:+.3f}$\n$p = {p26:.3f}$\n$n = {len(cps26)}$",
                 transform=axes[1].transAxes, ha="left", va="top",
                 fontsize=cs.FONT_SIZES["annotation"], color=cs.BLACK,
                 bbox=dict(facecolor="white",
                           edgecolor=cs.PALETTE["gray_light"],
                           boxstyle="round,pad=0.3", linewidth=0.5))

    cs.add_header(
        fig,
        "Convergent + discriminant: the boundary of AI Presence",
        "Same construct, opposing relationships with related vs unrelated outcomes",
        "Left: v0.25 B2B SaaS (indigo). Right: v0.29 pooled, within-substrate BSR percentile (warm).",
    )
    cs.add_footer(
        fig,
        verdict="Pattern 3: v0.25 + v0.29 jointly satisfy Campbell–Fiske construct validity.",
        phase=PHASE,
    )

    plt.subplots_adjust(top=0.82, bottom=0.13, left=0.08, right=0.97, wspace=0.32)
    fig.savefig(OUT_PDF_CONVERGENT, **cs.SAVEFIG_PARAMS)
    plt.close(fig)
    print(f"✓ Wrote {OUT_PDF_CONVERGENT.relative_to(AIAS_ROOT)}  ({OUT_PDF_CONVERGENT.stat().st_size} bytes)")


# -----------------------------------------------------------------------------
# Figure 4 — skincare DGP contrast (cell-coded horizontal bar)
# -----------------------------------------------------------------------------

def build_skincare_dgp():
    skincare = load_skincare_with_cells()
    bsr = load_bsr("skincare")
    pairs = [(b, cp, cell, bsr[b]) for b, cp, cell in skincare if b in bsr]
    pairs.sort(key=lambda x: x[3])  # ascending BSR (best at top)

    cell_color = {
        "A": cs.WARM,    # Prestige
        "B": cs.TEAL,    # Celebrity DTC / cult
        "C": cs.INDIGO,  # Clinical
    }
    cell_label = {
        "A": "Cell A — Prestige",
        "B": "Cell B — Celebrity / cult",
        "C": "Cell C — Clinical",
    }

    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero_tall"])
    brands = [p[0] for p in pairs]
    bsrs = [p[3] for p in pairs]
    colors_list = [cell_color[p[2]] for p in pairs]
    y_pos = np.arange(len(brands))

    ax.barh(y_pos, bsrs, color=colors_list, alpha=0.85, edgecolor="none", height=0.7)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(brands, fontsize=cs.FONT_SIZES["data_label"])
    ax.set_xscale("log")
    ax.set_xlabel("Amazon BSR (log scale — lower = more sales)",
                  fontsize=cs.FONT_SIZES["axis_label"])
    ax.tick_params(axis="both", labelsize=cs.FONT_SIZES["axis_tick"])
    ax.invert_yaxis()
    ax.grid(True, which="major", axis="x", linestyle=":",
            linewidth=0.5, color=cs.PALETTE["gray_light"], alpha=0.7)
    ax.set_axisbelow(True)

    # Legend, cells present in the data only
    present_cells = sorted(set(p[2] for p in pairs))
    legend_handles = [mpatches.Patch(color=cell_color[c], label=cell_label[c])
                      for c in present_cells]
    ax.legend(handles=legend_handles, loc="lower right",
              fontsize=cs.FONT_SIZES["legend"], frameon=True, framealpha=0.95)

    cs.add_header(
        fig,
        "Skincare: brand channel-fit drives BSR, not AI Presence",
        "23 skincare brands sorted by Amazon BSR, color-coded by panel cell",
        "Clinical (Cell C) brands dominate Amazon; prestige (Cell A) brands rank orders of magnitude lower at equal $C_P$.",
    )
    cs.add_footer(
        fig,
        verdict="Pattern 4: Different data-generating processes within constant $C_P$.",
        phase=PHASE,
    )

    plt.subplots_adjust(top=0.84, bottom=0.09, left=0.24, right=0.96)
    fig.savefig(OUT_PDF_SKINCARE, **cs.SAVEFIG_PARAMS)
    plt.close(fig)
    print(f"✓ Wrote {OUT_PDF_SKINCARE.relative_to(AIAS_ROOT)}  ({OUT_PDF_SKINCARE.stat().st_size} bytes)")


if __name__ == "__main__":
    build_scatter()
    build_cosmetics_ceiling()
    build_convergent_discriminant()
    build_skincare_dgp()
