"""
Leaderboards Panel — five-category view of AI Presence rankings.

Five subplots stacked vertically, one per measured category:
  PM Software, Running Shoes, Olive Oil, Skincare, Personal Finance.

Each panel shows the top 5 brands by AI Presence in that category.
The #1 brand in each panel is highlighted in Indigo; the rest are in
Black 60. This applies the brand spec's qualitative_recommended scheme
(single accent + grayscale) consistently across panels.

This is the "what we measured" chart — the orientation view that runs
in the report's opening pages, before any pattern analysis. Readers
go to individual category snapshots for full leaderboards.

Renders to: reports/output/chart_leaderboards_6col.pdf

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

# Display order (top-to-bottom in the figure). Mirrors the order in which
# categories were measured in v0.6: PM first (inaugural), Running second,
# Olive Oil third, Skincare fourth, Finance fifth.
CATEGORY_ORDER = ["PM", "Running", "Olive Oil", "Skincare", "Finance"]

# Top N brands per category panel
TOP_N = 5

# Source attribution (versioned)
SOURCE_TEXT = "Source: Third System AI Presence Index v0.6 · n=96 measurements per category"
VERSION = "v0.6"
VERSION_DATE = "30 Apr 2026"


# ---------------------------------------------------------------------------
# Data acquisition
# ---------------------------------------------------------------------------

def get_all_leaderboards() -> tuple[dict, dict]:
    """Load most-recent leaderboard per category.

    Returns (data_dict, paths_dict) where data_dict maps category key
    to list of brand row dicts, sorted by presence descending.
    """
    aias_root = _REPORTS.parent
    original_cwd = Path.cwd()
    try:
        import os
        os.chdir(aias_root)
        data, paths = cd.load_all_categories()
    finally:
        os.chdir(original_cwd)

    # Sort each category by presence descending so top-N is just a slice
    for cat in data:
        data[cat] = sorted(data[cat], key=lambda r: float(r["presence"]), reverse=True)
    return data, paths


# ---------------------------------------------------------------------------
# Chart construction
# ---------------------------------------------------------------------------

def render(output_dir: Path | str | None = None) -> list[Path]:
    """Render leaderboards panel and save to reports/output/.

    Returns the list of file paths written.
    """
    data, paths = get_all_leaderboards()

    # Validate all five categories are present
    missing = [c for c in CATEGORY_ORDER if c not in data]
    if missing:
        raise RuntimeError(
            f"Missing leaderboards for: {missing}. "
            f"Need presence_index_v0.3_*.csv files for all five categories."
        )

    # ----- Figure: 6-col hero, 5 panels stacked vertically -----
    # Tall layout to fit five panels. Use the 6_column_hero_tall figsize
    # if it exists, else extend the standard hero figsize.
    fig_width = cs.FIGSIZE_6COL_HERO[0]   # 7.5"
    fig_height = 9.0                       # tall enough for 5 panels at ~1.6" each

    fig, axes = plt.subplots(
        nrows=len(CATEGORY_ORDER),
        ncols=1,
        figsize=(fig_width, fig_height),
        sharex=True,  # all panels share the 0–100% x-axis
    )

    # Manual margins because this is a non-standard 5-panel layout —
    # reserve_margins assumes single_panel by default.
    # top=0.88 reserves room for figure-level title + subtitle (2 lines)
    #   plus a clean gap before the first panel's category title
    # bottom=0.07 reserves room for x-axis label AND source/version line
    fig.subplots_adjust(
        top=0.88,
        bottom=0.07,
        left=0.18,
        right=0.95,
        hspace=0.55,
    )

    # ----- Per-panel rendering -----
    for ax, category_key in zip(axes, CATEGORY_ORDER):
        rows = data[category_key][:TOP_N]
        brands = [r["brand"] for r in rows]
        presence = [float(r["presence"]) for r in rows]

        # Highlight #1 in Indigo, others in Black 60.
        # rows is already sorted descending, so brands[0] is the leader.
        leader = brands[0]
        colors = cu.highlight_colors(brands, leader, accent=cs.ACCENT_INDIGO, rest=cs.BLACK_60)

        y = np.arange(len(brands))
        ax.barh(y, presence, color=colors, height=0.7)
        ax.invert_yaxis()  # rank #1 at top
        ax.set_yticks(y)
        ax.set_yticklabels(brands, fontsize=cs.FONT_SIZES_6COL["axis_tick"])
        ax.set_xlim(0, 105)

        # Add value labels at the end of each bar (small, muted)
        for yi, val in zip(y, presence):
            ax.text(val + 1.5, yi, f"{val:.0f}",
                    va="center", ha="left",
                    fontsize=cs.FONT_SIZES_6COL["data_label"],
                    color=cs.COLOR_MUTED)

        # Per-panel category label (acts as subtitle for each panel).
        # Place at the top-left of each panel so readers can scan vertically.
        ax.set_title(
            cd.CATEGORY_LABELS[category_key],
            fontsize=cs.FONT_SIZES_6COL["subtitle"],
            fontweight="bold",
            color=cs.COLOR_TEXT,
            loc="left",
            pad=6,
        )

        cs.style_axis_minimal(ax, orientation="horizontal_bar")
        # Suppress x-axis tick labels except on the bottom panel
        if ax is not axes[-1]:
            ax.tick_params(axis="x", labelbottom=False)

    # ----- Bottom panel: x-axis label only on the last subplot -----
    axes[-1].set_xlabel("AI Presence (%)", fontsize=cs.FONT_SIZES_6COL["axis_label"])

    # ----- Figure-level title + subtitle (above all panels) -----
    # Position: y=0.96 / 0.935 with top margin at 0.88 leaves comfortable
    # gap before the first panel's category title
    sizes = cs.FONT_SIZES_6COL
    fig.text(
        0.18, 0.965,
        "AI Presence leaderboards across five categories",
        fontsize=sizes["title"], fontweight="bold",
        color=cs.COLOR_TEXT, ha="left", va="top",
    )
    fig.text(
        0.18, 0.93,
        "Top 5 brands per category by Presence score. The leader in each panel is highlighted in Indigo.",
        fontsize=sizes["subtitle"], color=cs.COLOR_MUTED,
        ha="left", va="top",
    )

    # ----- Source line + version stamp at the bottom -----
    # y=0.01 sits in the bottom margin, below the x-axis label
    fig.text(
        0.18, 0.01, SOURCE_TEXT,
        fontsize=sizes["source_caption"], color=cs.COLOR_MUTED,
        style="italic", ha="left", va="bottom",
    )
    fig.text(
        0.95, 0.01, f"{VERSION} · {VERSION_DATE}",
        fontsize=sizes["source_caption"], color=cs.COLOR_MUTED,
        ha="right", va="bottom",
    )

    # ----- Save with explicit margins (no bbox_inches='tight' for multi-panel) -----
    # cu.save_chart() applies bbox_inches='tight' which tightens the figure to
    # whatever's drawn. For multi-panel charts with manual subplots_adjust
    # margins, that retightening eats our reserved space at the bottom.
    # Save manually here, preserving the layout we set above.
    if output_dir is None:
        output_dir = _REPORTS / "output"
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_pdf = output_dir / "chart_leaderboards_6col.pdf"
    fig.savefig(
        output_pdf,
        dpi=cs.DPI_PRINT,
        # Note: NOT using bbox_inches='tight' — preserves our manual margins.
        pad_inches=cs.PAD_INCHES,
    )
    plt.close(fig)
    return [output_pdf]


if __name__ == "__main__":
    paths = render()
    print(f"Rendered Leaderboards Panel:")
    for p in paths:
        print(f"  {p}")
