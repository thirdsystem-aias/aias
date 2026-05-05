"""
Pattern 1 — AI Presence varies meaningfully across models.

Visualizes the structural relationship between discourse fragmentation
and per-model variance: brands in fragmented-discourse categories
(personal finance, olive oil, PM software) show wide spreads between
Anthropic and OpenAI; brands in converged-discourse categories
(running shoes, skincare) cluster near zero spread.

Form: dumbbell plot. One row per brand. Two dots per row (Anthropic
in Indigo, OpenAI in Petro), connected by a thin Black 40 line whose
length IS the variance. Brands sorted by spread descending — most
variant at top.

Punchline: Rocket Money. 71-point spread (Anthropic 0%, OpenAI 71%) —
the largest single-brand variance in the v0.6 dataset. Highlighted in
Copper Plate to mark it as the dataset's most striking case.

Renders to: reports/output/chart_p1_3col.pdf

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

# Show one row per category — the brand with the largest absolute spread
# in each category. Order top-to-bottom by spread magnitude.
CATEGORY_ORDER_BY_FRAGMENTATION = [
    # Most fragmented discourse → largest expected variance, listed first
    "Finance",
    "Olive Oil",
    "PM",
    "Running",
    "Skincare",  # Most converged discourse → smallest expected variance
]

# Shorter category names for chart labels (the brand spec category labels
# are full names suitable for body copy; chart axes need shorter forms).
CATEGORY_SHORT_LABELS = {
    "PM":        "PM Software",
    "Running":   "Running Shoes",
    "Olive Oil": "Olive Oil",
    "Skincare":  "Skincare",
    "Finance":   "Personal Finance",
}

# Brand to highlight as the punchline (largest single-brand variance)
HIGHLIGHT = "Rocket Money"

# Source attribution
SOURCE_TEXT = "Source: Third System AI Presence Index v0.6 · n=96 per category"
VERSION = "v0.6"
VERSION_DATE = "30 Apr 2026"


# ---------------------------------------------------------------------------
# Data acquisition
# ---------------------------------------------------------------------------

def get_top_variance_brand(rows: list[dict]) -> dict:
    """Find the brand with the largest |Anthropic - OpenAI| spread.

    Restrict to brands with non-trivial overall presence (≥10%) so we
    don't pick noise — a brand with 1% presence on one model and 0% on
    the other has a 1-point spread, not informative.
    """
    candidates = [r for r in rows if float(r["presence"]) >= 10.0]
    if not candidates:
        candidates = rows  # Fallback if no brand clears 10%

    def spread(r):
        return abs(float(r["presence_anthropic"]) - float(r["presence_openai"]))

    return max(candidates, key=spread)


def get_pattern1_data() -> list[dict]:
    """Load most-recent leaderboards and pick the top-variance brand
    from each category. Returns a list of brand row dicts annotated
    with category_label and category_key.
    """
    aias_root = _REPORTS.parent
    original_cwd = Path.cwd()
    try:
        import os
        os.chdir(aias_root)
        data, paths = cd.load_all_categories()
    finally:
        os.chdir(original_cwd)

    rows = []
    for cat in CATEGORY_ORDER_BY_FRAGMENTATION:
        if cat not in data:
            continue
        top = get_top_variance_brand(data[cat])
        annotated = dict(top)
        annotated["category_key"] = cat
        annotated["category_label"] = cd.CATEGORY_LABELS[cat]
        rows.append(annotated)
    return rows


# ---------------------------------------------------------------------------
# Chart construction
# ---------------------------------------------------------------------------

def render(output_dir: Path | str | None = None) -> list[Path]:
    """Render Pattern 1 dumbbell chart and save to reports/output/.

    Returns the list of file paths written.
    """
    rows = get_pattern1_data()
    if not rows:
        raise RuntimeError(
            "No category data found. Pattern 1 requires presence_index_v0.3_*.csv "
            "files for at least one category."
        )

    # Sort by spread descending (largest spread at top after invert_yaxis)
    rows.sort(
        key=lambda r: abs(float(r["presence_anthropic"]) - float(r["presence_openai"])),
        reverse=True,
    )

    # Extract data — use SHORT category labels for chart readability
    labels = [f'{r["brand"]} ({CATEGORY_SHORT_LABELS[r["category_key"]]})' for r in rows]
    anthropic_vals = [float(r["presence_anthropic"]) for r in rows]
    openai_vals = [float(r["presence_openai"]) for r in rows]
    brand_names = [r["brand"] for r in rows]

    # ----- Figure setup -----
    fig, ax = plt.subplots(figsize=cs.FIGSIZE_3COL_INLINE)
    cs.reserve_margins(fig, layout="single_panel")

    y = np.arange(len(rows))

    # ----- Connecting lines (the "dumbbell bar") -----
    # Drawn first, behind the dots. Use Black 40 — visible but recessive.
    for yi, a, o in zip(y, anthropic_vals, openai_vals):
        ax.plot(
            [a, o], [yi, yi],
            color=cs.BLACK_40,
            linewidth=1.5,
            zorder=1,
            solid_capstyle="round",
        )

    # ----- Dots (Anthropic + OpenAI per row) -----
    # Highlight Rocket Money in Copper Plate; others in Indigo + Petro pair.
    anthropic_colors = [
        cs.ACCENT_COPPER_PLATE if b == HIGHLIGHT else cs.ACCENT_INDIGO
        for b in brand_names
    ]
    openai_colors = [
        cs.ACCENT_COPPER_PLATE if b == HIGHLIGHT else cs.PETRO
        for b in brand_names
    ]

    ax.scatter(anthropic_vals, y, s=60, c=anthropic_colors, zorder=3,
               edgecolors=cs.COLOR_TEXT, linewidths=0.4, label="Anthropic")
    ax.scatter(openai_vals, y, s=60, c=openai_colors, zorder=3,
               edgecolors=cs.COLOR_TEXT, linewidths=0.4, marker="s", label="OpenAI")

    # ----- Value annotations on the right side -----
    # The right side of the chart (x≈85→105) is empty for most rows because
    # no brand reaches 100% on both models. Use that whitespace to show the
    # numeric spread, so readers can read magnitudes directly.
    SPREAD_LABEL_X = 108  # Just outside xlim=(−5, 105) so we extend past edge
    for yi, a, o, b in zip(y, anthropic_vals, openai_vals, brand_names):
        spread_pts = abs(a - o)
        # Format like "0→71  (71 pt)" — shows both endpoints + magnitude
        lo, hi = (a, o) if a <= o else (o, a)
        text = f"{int(round(lo))}→{int(round(hi))}   {int(round(spread_pts))} pt"
        # Use Copper Plate text for highlighted brand; muted gray for others
        text_color = cs.ACCENT_COPPER_PLATE if b == HIGHLIGHT else cs.COLOR_MUTED
        ax.text(
            SPREAD_LABEL_X, yi, text,
            ha="left", va="center",
            fontsize=cs.FONT_SIZES_3COL["data_label"],
            color=text_color,
            fontweight="bold" if b == HIGHLIGHT else "normal",
        )

    # ----- Axis setup -----
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=cs.FONT_SIZES_3COL["axis_tick"])
    ax.invert_yaxis()  # largest spread at top
    # xlim extended to make room for spread-value labels on the right.
    # Tick labels still only go 0-100; the extension is whitespace + annotations.
    ax.set_xlim(-5, 145)
    # Restrict x-tick labels to the meaningful 0-100 range
    ax.set_xticks([0, 20, 40, 60, 80, 100])
    ax.set_xlabel("AI Presence (%)", fontsize=cs.FONT_SIZES_3COL["axis_label"])

    # Use 'plot' orientation so we get light gridlines on both axes —
    # helpful for reading the dot positions on the x-axis.
    cs.style_axis_minimal(ax, orientation="horizontal_dot")

    # Hide the bottom x-axis spine — tick marks alone are sufficient,
    # the line is visual noise. Also hide the left spine (the brand
    # labels mark the rows; no line needed).
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)

    # ----- Legend (below the x-axis label, in the bottom margin) -----
    from matplotlib.lines import Line2D
    legend_elems = [
        Line2D([0], [0], marker="o", color="w", markerfacecolor=cs.ACCENT_INDIGO,
               markeredgecolor=cs.COLOR_TEXT, markeredgewidth=0.4, markersize=7,
               label="Anthropic"),
        Line2D([0], [0], marker="s", color="w", markerfacecolor=cs.PETRO,
               markeredgecolor=cs.COLOR_TEXT, markeredgewidth=0.4, markersize=7,
               label="OpenAI"),
    ]
    ax.legend(
        handles=legend_elems,
        loc="upper left",
        bbox_to_anchor=(0.0, -0.22),  # well below the x-axis label
        ncol=2,
        fontsize=cs.FONT_SIZES_3COL["legend"],
        frameon=False,
    )

    # ----- Editorial title + subtitle -----
    cs.editorial_title(
        ax,
        title="Per-model variance, by category",
        subtitle=(
            "Top-variance brand from each category.\n"
            "Spread tracks discourse fragmentation."
        ),
        column_span="3col_inline",
    )

    cs.add_source(ax, SOURCE_TEXT)

    # ----- Save (single-panel, can use bbox_inches='tight') -----
    written = cu.save_chart(fig, pattern_id="p1", column_span="3", output_dir=output_dir)
    plt.close(fig)
    return written


if __name__ == "__main__":
    paths = render()
    print(f"Rendered Pattern 1:")
    for p in paths:
        print(f"  {p}")
