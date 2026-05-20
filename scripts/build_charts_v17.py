#!/usr/bin/env python3
"""
build_charts_v17.py — Matplotlib chart pipeline for v0.17 figures.

Renders three PDF figures from data in reports/v17_kitchenware_content.py:

    Figure 1: fig1_mention_rates.pdf
        Phase B mention rate distribution across the 15-brand panel.
        Horizontal bar chart, sorted descending, color-coded by cell.
        Embedded location: SSRN paper §5.1 (Mentionability tier verdicts).

    Figure 2: fig2_dissociation.pdf
        Phase A C_P score vs Phase B mention rate scatter for the 4 tested
        pivots. Iwachu highlighted as the canonical dissociation case.
        Embedded location: SSRN paper §6.1 (Iwachu canonical case).

    Figure 3: fig3_cell_collapse.pdf
        Per-cell pre-Phase-A vs post-Phase-B brand survival summary.
        Paired bar chart with worldwide n subtitle.
        Embedded location: SSRN paper §5.3 (C1 floor breach).

Output: papers/v0_17/figures/

Brand tokens: Third System Indigo (#37237B primary). Akkurat font with
sans-serif fallback. Output PDFs are sized for both pandoc \\includegraphics
embedding (SSRN paper) and ReportLab two-pass overlay (brand-format report).

Usage:
    python scripts/build_charts_v17.py
"""

import sys
from pathlib import Path

ROOT = Path.home() / "aias"
sys.path.insert(0, str(ROOT / "reports"))

import matplotlib
matplotlib.use("Agg")  # No display required
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
from matplotlib.patches import Patch

from v17_kitchenware_content import (
    load_phase_a_scores,
    load_phase_b_mention_rates,
    CELL_COUNTS,
    C1_FLOOR,
    TOTAL_PRE,
    TOTAL_POST,
)


# ============================================================================
# Output paths
# ============================================================================

FIGURES_DIR = ROOT / "papers" / "v0_17" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================================
# Third System brand tokens
# ============================================================================

INDIGO       = "#37237B"  # Primary — Third System brand
INDIGO_LIGHT = "#7D6CB8"  # Lighter Indigo
TEAL         = "#3A7C8A"  # Secondary
ROSE         = "#A8485F"  # Tertiary
GOLD         = "#C9A96E"  # Accent
GREY_900     = "#1A1A1A"  # Text and axes
GREY_500     = "#808080"  # Threshold lines
GREY_300     = "#BFBFBF"  # Light grid
GREY_200     = "#D9D9D9"  # Background bars

CELL_COLORS = {
    "european": INDIGO,
    "american": TEAL,
    "japanese": ROSE,
}


# ============================================================================
# Font setup — Akkurat with sans-serif fallback
# ============================================================================

def setup_fonts() -> str:
    """Register Akkurat if available; otherwise fall back to sans-serif."""
    candidates = [
        Path.home() / "Library" / "Fonts" / "Akkurat-Regular.ttf",
        Path.home() / "Library" / "Fonts" / "AkkuratPro-Regular.otf",
        Path.home() / ".fonts" / "Akkurat" / "Akkurat-Regular.ttf",
    ]
    for c in candidates:
        if c.exists():
            try:
                fm.fontManager.addfont(str(c))
                plt.rcParams["font.family"] = "Akkurat"
                return f"Akkurat ({c.name})"
            except Exception:
                pass
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Helvetica", "Arial", "DejaVu Sans"]
    return "sans-serif fallback"


def setup_rcparams() -> None:
    """Configure matplotlib rcParams for AIAS academic-paper figure style."""
    plt.rcParams["axes.labelcolor"]  = GREY_900
    plt.rcParams["axes.edgecolor"]   = GREY_500
    plt.rcParams["xtick.color"]      = GREY_900
    plt.rcParams["ytick.color"]      = GREY_900
    plt.rcParams["axes.spines.top"]   = False
    plt.rcParams["axes.spines.right"] = False
    plt.rcParams["axes.titlesize"]   = 10
    plt.rcParams["axes.labelsize"]   = 10
    plt.rcParams["xtick.labelsize"]  = 9
    plt.rcParams["ytick.labelsize"]  = 9
    plt.rcParams["legend.fontsize"]  = 9


# ============================================================================
# Figure 1 — Phase B mention-rate distribution (15-brand horizontal bar)
# ============================================================================

def fig1_mention_rates() -> Path:
    data = load_phase_b_mention_rates()
    brands  = [d[0] for d in data]
    rates   = [d[2] for d in data]
    tiers   = [d[3] for d in data]
    colors  = [CELL_COLORS[d[1]] for d in data]

    fig, ax = plt.subplots(figsize=(6.5, 5.8))
    y_pos = np.arange(len(brands))
    ax.barh(y_pos, rates, color=colors, edgecolor=GREY_900, linewidth=0.4)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(brands)
    ax.invert_yaxis()  # Highest rate at top
    ax.set_xlabel("Phase B mention rate (mentions / 18 cells)")
    ax.set_xlim(0, 1.05)

    # PASS threshold reference at 1/6
    ax.axvline(1/6, color=GREY_500, linestyle="--", linewidth=1, alpha=0.7)
    ax.text(1/6 + 0.012, -0.4, "PASS threshold (1/6)",
            fontsize=8, color=GREY_500, va="top")

    # Tier annotations on excluded/marginal bars
    for i, (brand, cell, rate, tier) in enumerate(data):
        if tier == "PASS_E5":
            ax.text(rate + 0.015, i, "PASS_E5",
                    fontsize=7.5, color=GREY_900, va="center", style="italic")
        elif tier == "EXCLUDED_E1a":
            ax.text(0.012, i, "EXCLUDED",
                    fontsize=7.5, color="white", va="center",
                    bbox=dict(facecolor=GREY_900, edgecolor="none", pad=1.5))

    # Cell legend
    legend_elements = [
        Patch(facecolor=INDIGO, label="European cell"),
        Patch(facecolor=TEAL,   label="American cell"),
        Patch(facecolor=ROSE,   label="Japanese cell"),
    ]
    ax.legend(handles=legend_elements, loc="lower right", frameon=False)

    plt.tight_layout()
    out = FIGURES_DIR / "fig1_mention_rates.pdf"
    plt.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"  Wrote: {out.relative_to(ROOT)}")
    return out


# ============================================================================
# Figure 2 — Phase A vs Phase B dissociation scatter
# ============================================================================

def fig2_dissociation() -> Path:
    scores = load_phase_a_scores()
    rates  = {b: r for (b, c, r, t) in load_phase_b_mention_rates()}

    # The four pivots that received Phase A measurement
    pivots = [
        ("Le Creuset", "european"),
        ("All-Clad",   "american"),
        ("Iwachu",     "japanese"),
        ("Vermicular", "japanese"),
    ]

    fig, ax = plt.subplots(figsize=(6.5, 5.8))

    for brand, cell in pivots:
        color = CELL_COLORS[cell]
        x = scores.get(brand, 0)
        if brand == "Vermicular":
            # Vermicular failed at Phase A and was descoped before Phase B.
            # Plot at x=4 (its actual C_P score), y=-0.06 (below-axis indicator).
            ax.scatter([x], [-0.06], marker="x", s=140,
                       color=GREY_500, linewidths=2.2, zorder=3)
            ax.annotate(f"{brand}\n(C_P FAIL, descoped)",
                        xy=(x, -0.06), xytext=(x + 0.25, 0.07),
                        fontsize=8, color=GREY_500, ha="left",
                        arrowprops=dict(arrowstyle="-", color=GREY_500, lw=0.6))
            continue

        y = rates.get(brand, 0)
        ax.scatter([x], [y], s=220, color=color, edgecolor=GREY_900,
                   linewidth=1.4, zorder=3)

        if brand == "Iwachu":
            # The canonical dissociation case — highlight with annotation
            ax.annotate(brand, xy=(x, y), xytext=(x - 0.25, y + 0.06),
                        fontsize=11, color=color, fontweight="bold", ha="right")
            ax.annotate("Recognition × Recall dissociation:\n"
                        "full recognition (6/6), zero recall (0/18)",
                        xy=(x, y), xytext=(4.5, 0.27),
                        fontsize=9, color=color, ha="left", style="italic",
                        arrowprops=dict(arrowstyle="->", color=color, lw=1.0))
        else:
            ax.annotate(brand, xy=(x, y), xytext=(x - 0.25, y - 0.05),
                        fontsize=10, color=color, ha="right")

    # Threshold reference lines
    ax.axvline(5, color=GREY_500, linestyle="--", linewidth=1, alpha=0.6)
    ax.text(5.08, 0.98, "Phase A supermajority (5/6)",
            fontsize=8, color=GREY_500, va="top", rotation=90)
    ax.axhline(1/6, color=GREY_500, linestyle="--", linewidth=1, alpha=0.6)
    ax.text(0.2, 1/6 + 0.012, "Phase B PASS (1/6)",
            fontsize=8, color=GREY_500, ha="left")

    ax.set_xlabel("Phase A C_P anchoring score (out of 6 reference LLMs)")
    ax.set_ylabel("Phase B mention rate (mentions / 18 cells)")
    ax.set_xlim(-0.5, 6.6)
    ax.set_ylim(-0.18, 1.15)
    ax.set_xticks(range(7))
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])

    # Quadrant labels (semantic)
    ax.text(0.3, 1.08, "Low recognition\n+ high recall\n(empty quadrant)",
            fontsize=7, color=GREY_500, ha="left", style="italic", alpha=0.7)
    ax.text(6.3, 1.08, "Full Presence\n(recognition + recall)",
            fontsize=7, color=GREY_500, ha="right", style="italic", alpha=0.7)
    ax.text(6.3, -0.12, "Recognition only\n(dissociation)",
            fontsize=7, color=GREY_500, ha="right", style="italic", alpha=0.7)

    legend_elements = [
        Patch(facecolor=INDIGO, label="European cell pivot"),
        Patch(facecolor=TEAL,   label="American cell pivot"),
        Patch(facecolor=ROSE,   label="Japanese cell pivot"),
    ]
    ax.legend(handles=legend_elements, loc="center right",
              frameon=False, fontsize=8)

    plt.tight_layout()
    out = FIGURES_DIR / "fig2_dissociation.pdf"
    plt.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"  Wrote: {out.relative_to(ROOT)}")
    return out


# ============================================================================
# Figure 3 — Per-cell collapse summary
# ============================================================================

def fig3_cell_collapse() -> Path:
    cells = ["European", "American", "Japanese"]
    pre   = [CELL_COUNTS["european"]["pre"],
             CELL_COUNTS["american"]["pre"],
             CELL_COUNTS["japanese"]["pre"]]
    post  = [CELL_COUNTS["european"]["post"],
             CELL_COUNTS["american"]["post"],
             CELL_COUNTS["japanese"]["post"]]

    x = np.arange(len(cells))
    width = 0.36

    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    bars_pre  = ax.bar(x - width/2, pre, width,
                        label="Pre-Phase A (registered panel)",
                        color=GREY_300, edgecolor=GREY_900, linewidth=0.5)
    bars_post = ax.bar(x + width/2, post, width,
                        label="Post-Phase B (operational panel)",
                        color=INDIGO, edgecolor=GREY_900, linewidth=0.5)

    # Bar value labels
    for bars in [bars_pre, bars_post]:
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, h + 0.12,
                    str(int(h)), ha="center", fontsize=10, color=GREY_900)

    ax.set_xticks(x)
    ax.set_xticklabels(cells)
    ax.set_ylabel("Brand count")
    ax.set_ylim(0, 8.0)

    # Worldwide-n + C1 floor as subtitle
    ax.set_title(
        f"Worldwide n: pre-Phase-A {TOTAL_PRE}, post-Phase-B {TOTAL_POST}    "
        f"(C1 floor: {C1_FLOOR}; BREACHED by {C1_FLOOR - TOTAL_POST})",
        fontsize=9, color=GREY_900, pad=10, style="italic"
    )

    ax.legend(loc="upper right", frameon=False)
    ax.grid(axis="y", linestyle=":", color=GREY_300, alpha=0.6)
    ax.set_axisbelow(True)

    plt.tight_layout()
    out = FIGURES_DIR / "fig3_cell_collapse.pdf"
    plt.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"  Wrote: {out.relative_to(ROOT)}")
    return out


# ============================================================================
# Main
# ============================================================================

def main() -> None:
    font_used = setup_fonts()
    setup_rcparams()

    print("v0.17 chart build")
    print("=" * 60)
    print(f"  Font:        {font_used}")
    print(f"  Output dir:  {FIGURES_DIR.relative_to(ROOT)}")
    print(f"  Brand color: Third System Indigo {INDIGO}")
    print()

    fig1_mention_rates()
    fig2_dissociation()
    fig3_cell_collapse()

    print()
    print("=" * 60)
    print(f"Done — 3 figures in {FIGURES_DIR.relative_to(ROOT)}")
    print(f"Next: rebuild SSRN paper to embed via \\includegraphics:")
    print(f"  python scripts/build_paper_v0_17.py")


if __name__ == "__main__":
    main()
