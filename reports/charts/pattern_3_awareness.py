"""
Pattern 3 — AI brand visibility diverges from consumer awareness.

The published v0.6 finding: in four of five categories, brands with high
consumer awareness underperform their commercial position in AI mediation;
in personal finance the divergence inverts (small-user-base brands like
YNAB dominate while larger ones like Rocket Money trail).

We do NOT have consumer-awareness data in the leaderboards. Building a
true scatter would require commercial-scale data we don't measure. So
this chart works honestly within what we measure: it shows AI Presence
per brand, grouped by category, and highlights the brands the v0.6 report
names as the *divergent cases*. Body copy does the divergence interpretation.

Form: single-panel beeswarm. Five category rows, dots spread perpendicular
to avoid overlap. Highlighted brands (named as divergent in v0.6) appear
in Copper Plate; rest in Black 40. The eye lands on the highlighted brands
and reads their AI Presence value directly from the x-axis.

Renders to: reports/output/chart_p3_3col.pdf

Brand spec: third_system_brand.json schema 1.4
Data source: presence_index_v0.3_*.csv (most-recent leaderboard per category)
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

_THIS = Path(__file__).resolve()
_REPORTS = _THIS.parent.parent
if str(_REPORTS) not in sys.path:
    sys.path.insert(0, str(_REPORTS))

import chart_style as cs
import chart_utils as cu
import chart_data as cd


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Order top-to-bottom: categories where the divergence is sharpest first.
# This mirrors the editorial sequence in v0.6 Pattern 3 prose.
CATEGORY_ORDER = ["Skincare", "Olive Oil", "Running", "Finance", "PM"]

# Shorter category labels for the y-axis
CATEGORY_SHORT_LABELS = {
    "PM":        "PM Software",
    "Running":   "Running Shoes",
    "Olive Oil": "Olive Oil",
    "Skincare":  "Skincare",
    "Finance":   "Personal Finance",
}

# Brands the v0.6 report names as the divergent cases. Highlight these in
# Copper Plate; the rest sit in Black 40.
#
# The narrative pattern:
#   - Skincare:  La Mer, SK-II, Lancôme = "luxury heritage outranked by
#                drugstore CeraVe" (downward divergence)
#   - Olive Oil: Bertolli, Colavita, Goya, Filippo Berio = "supermarket
#                legacy brands outranked by DTC newcomers" (downward)
#   - Running:   Nike = "highest marketing budget, AI Presence rank 6"
#                (downward)
#   - Finance:   YNAB, Rocket Money = "1M users at #1; 5M users at #5
#                (Anthropic 0%)" (UPWARD for YNAB; downward for Rocket Money)
#   - PM:        (no strong divergence in v0.6; pattern is mild here)
DIVERGENT_BRANDS = {
    "La Mer", "SK-II", "Lancôme", "Lancome",
    "Bertolli", "Colavita", "Goya", "Filippo Berio",
    "Nike",
    "YNAB", "Rocket Money",
}

# Beeswarm spread settings
BEESWARM_WIDTH = 0.30   # half-height range for jitter within each row
DOT_SIZE = 28           # smaller than dumbbell — many dots per row
HIGHLIGHT_DOT_SIZE = 50  # larger for highlighted brands so eye finds them
ROW_SPACING = 1.0       # vertical distance between category rows

SOURCE_TEXT = "Source: Third System AI Presence Index v0.6 · n=96 per category"


# ---------------------------------------------------------------------------
# Data acquisition
# ---------------------------------------------------------------------------

def get_pattern3_data() -> dict[str, list[dict]]:
    """Load most-recent leaderboards per category. Returns dict mapping
    category key to list of brand row dicts (sorted by presence descending).
    """
    aias_root = _REPORTS.parent
    original_cwd = Path.cwd()
    try:
        import os
        os.chdir(aias_root)
        data, paths = cd.load_all_categories()
    finally:
        os.chdir(original_cwd)
    for cat in data:
        data[cat] = sorted(data[cat], key=lambda r: float(r["presence"]), reverse=True)
    return data


# ---------------------------------------------------------------------------
# Chart construction
# ---------------------------------------------------------------------------

def render(output_dir: Path | str | None = None) -> list[Path]:
    """Render Pattern 3 beeswarm chart and save to reports/output/.

    Returns the list of file paths written.
    """
    data = get_pattern3_data()

    # Validate required categories
    missing = [c for c in CATEGORY_ORDER if c not in data]
    if missing:
        raise RuntimeError(
            f"Missing leaderboards for: {missing}. "
            f"Pattern 3 requires presence_index_v0.3_*.csv files for all five categories."
        )

    # Font sizes for 4-col span — pull once and reuse below
    sizes = cs.font_sizes_for("4col")

    # ----- Figure setup -----
    # 4-column figsize (4.95" × 3.71") instead of 3-col inline. This chart
    # has 5 category rows × ~12 brands per row + label callouts; the 3-col
    # height is too tight for the beeswarm cluster + adjustText to resolve
    # cleanly. 4-col gives both more horizontal room for the data and more
    # vertical room per category row.
    fig, ax = plt.subplots(figsize=cs.FIGSIZE_4COL)
    cs.reserve_margins(fig, layout="single_panel")

    # ----- Per-category beeswarm rendering -----
    # Track names of highlighted brands we've already labeled to avoid
    # duplicate text annotations.
    annotated_brands: set[str] = set()
    label_texts = []  # Collected for adjustText collision resolution

    for row_idx, cat_key in enumerate(CATEGORY_ORDER):
        rows = data[cat_key]
        presence_vals = [float(r["presence"]) for r in rows]
        brand_names = [r["brand"] for r in rows]

        # Beeswarm offsets along the y-axis perpendicular
        y_offsets = cu.beeswarm_offsets(
            presence_vals,
            width=BEESWARM_WIDTH,
            bin_count=12,
        )
        y_positions = row_idx * ROW_SPACING + y_offsets

        # Color rule: divergent brands in Copper Plate, rest in Black 40
        is_divergent = [b in DIVERGENT_BRANDS for b in brand_names]

        # Draw all non-highlighted dots first (lower zorder) ...
        non_idx = [i for i, d in enumerate(is_divergent) if not d]
        if non_idx:
            ax.scatter(
                [presence_vals[i] for i in non_idx],
                [y_positions[i] for i in non_idx],
                s=DOT_SIZE,
                c=cs.BLACK_40,
                alpha=0.7,
                edgecolors="none",
                zorder=2,
            )

        # ... then highlighted dots on top with edge for visibility
        hi_idx = [i for i, d in enumerate(is_divergent) if d]
        if hi_idx:
            ax.scatter(
                [presence_vals[i] for i in hi_idx],
                [y_positions[i] for i in hi_idx],
                s=HIGHLIGHT_DOT_SIZE,
                c=cs.ACCENT_COPPER_PLATE,
                edgecolors=cs.COLOR_TEXT,
                linewidths=0.4,
                zorder=3,
            )

            # Label highlighted brands inline. Collect Text objects so
            # adjustText can resolve overlaps after all are placed.
            for i in hi_idx:
                brand = brand_names[i]
                if brand in annotated_brands:
                    continue
                annotated_brands.add(brand)
                # Place label to the LEFT of the dot when dot is near the
                # right edge (>=85), otherwise to the right. Prevents
                # clipping for brands like YNAB at 100%.
                if presence_vals[i] >= 85:
                    label_x = presence_vals[i] - 1.5
                    ha = "right"
                else:
                    label_x = presence_vals[i] + 1.5
                    ha = "left"
                t = ax.text(
                    label_x,
                    y_positions[i],
                    brand,
                    fontsize=sizes["data_label"],
                    color=cs.COLOR_TEXT,
                    ha=ha,
                    va="center",
                    fontweight="bold",
                    zorder=4,
                )
                label_texts.append(t)

    # ----- Axis setup -----
    y_ticks = [i * ROW_SPACING for i in range(len(CATEGORY_ORDER))]
    y_labels = [CATEGORY_SHORT_LABELS[c] for c in CATEGORY_ORDER]
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_labels, fontsize=sizes["axis_tick"])
    ax.set_ylim(-0.6, (len(CATEGORY_ORDER) - 1) * ROW_SPACING + 0.6)
    ax.invert_yaxis()  # first category at top
    ax.set_xlim(-5, 105)
    ax.set_xticks([0, 20, 40, 60, 80, 100])
    ax.set_xlabel("AI Presence (%)", fontsize=sizes["axis_label"])

    cs.style_axis_minimal(ax, orientation="horizontal_dot")

    # ----- Resolve label collisions -----
    # Many divergent brands cluster at low Presence in Skincare and Olive Oil
    # (La Mer, SK-II, Lancôme; Bertolli, Goya, Colavita, Filippo Berio).
    # adjustText spreads the labels apart while keeping connector lines
    # back to each brand's dot.
    cu.resolve_label_collisions(
        label_texts,
        ax=ax,
        force_text=(0.6, 1.2),    # stronger vertical force — labels can move
                                  # out of their category row's dot cluster
        force_points=(0.4, 0.6),
        expand_text=(1.05, 1.2),
        expand_points=(1.2, 1.4),
    )

    # ----- Editorial title + subtitle -----
    cs.editorial_title(
        ax,
        title="Discourse position outranks commercial scale",
        subtitle=(
            "AI Presence per brand, by category.\n"
            "Highlighted brands diverge from consumer awareness."
        ),
        column_span="4col",
    )

    cs.add_source(ax, SOURCE_TEXT)

    # ----- Save -----
    written = cu.save_chart(fig, pattern_id="p3", column_span="4", output_dir=output_dir)
    plt.close(fig)
    return written


if __name__ == "__main__":
    paths = render()
    print(f"Rendered Pattern 3:")
    for p in paths:
        print(f"  {p}")
