"""
Pattern 6 — Phantom Brand Presence (Personal Finance).

Mint, Intuit's personal finance app, was decommissioned in March 2024. By
April 2026, when this measurement was taken, Mint had not been a live
application for 25 months. Yet AI mentioned Mint in 44% of responses about
personal finance — placing fifth among brands with non-zero Presence,
ahead of multiple live applications (Rocket Money, EveryDollar, Quicken
Simplifi, PocketGuard).

Per-model breakdown reveals AI training-data freshness asymmetry:
  Anthropic: 65% Presence (heavy lag — pre-shutdown corpus weighting)
  OpenAI:    23% Presence (less lag — but still mentioning a defunct brand)

This is the chart. Single accent (Indigo on Mint) + grayscale (every other
brand). Two side-by-side bars per brand: Anthropic and OpenAI, grouped.
The visual emphasizes Mint's persistent presence relative to live brands.

Renders to: reports/output/chart_p6_3col.pdf

Brand spec: third_system_brand.json schema 1.4
Data source: presence_index_v0.3_*.csv (most-recent finance leaderboard)
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Ensure parent directory (reports/) is on path so chart_style/utils import
_THIS = Path(__file__).resolve()
_REPORTS = _THIS.parent.parent
if str(_REPORTS) not in sys.path:
    sys.path.insert(0, str(_REPORTS))

import chart_style as cs
import chart_utils as cu
import chart_data as cd


# ---------------------------------------------------------------------------
# Data acquisition
# ---------------------------------------------------------------------------

def get_finance_data() -> tuple[list[dict], str]:
    """Load the most-recent finance leaderboard.

    Returns (rows, source_path). Raises if finance not found.
    """
    # chart_data.load_all_categories assumes CWD has the CSVs at the root.
    # Switch CWD to aias/ root briefly so the glob works.
    aias_root = _REPORTS.parent
    original_cwd = Path.cwd()
    try:
        import os
        os.chdir(aias_root)
        data, paths = cd.load_all_categories()
    finally:
        os.chdir(original_cwd)

    if "Finance" not in data:
        raise RuntimeError(
            "No Finance category found in leaderboards. "
            "Pattern 6 requires presence_index_v0.3_*.csv with YNAB or Monarch Money."
        )
    return data["Finance"], paths["Finance"]


# ---------------------------------------------------------------------------
# Chart construction
# ---------------------------------------------------------------------------

# How many brands to show. We want Mint visible alongside the top live brands
# so the contrast is legible. Top 8 by total presence is enough.
TOP_N = 8
HIGHLIGHT = "Mint"

# Source attribution shown at chart bottom — kept short so it doesn't collide
# with the version stamp on the right.
SOURCE_TEXT = "Source: Third System AI Presence Index v0.6 · n=96 per category"
VERSION = "v0.6"
VERSION_DATE = "30 Apr 2026"


def render(output_dir: Path | str | None = None) -> list[Path]:
    """Render Pattern 6 chart and save to reports/output/.

    Returns the list of file paths written.
    """
    rows, source_path = get_finance_data()

    # Sort by total presence, take top N (always include Mint even if outside top N)
    rows_sorted = sorted(rows, key=lambda r: float(r["presence"]), reverse=True)
    top = rows_sorted[:TOP_N]
    if not any(r["brand"] == HIGHLIGHT for r in top):
        # Mint outside top — add it
        mint_row = next((r for r in rows if r["brand"] == HIGHLIGHT), None)
        if mint_row:
            top.append(mint_row)

    # Extract paired data: anthropic and openai per brand
    brands = [r["brand"] for r in top]
    pres_anthropic = [float(r["presence_anthropic"]) for r in top]
    pres_openai = [float(r["presence_openai"]) for r in top]

    # ----- Figure setup -----
    fig, ax = plt.subplots(figsize=cs.FIGSIZE_3COL_INLINE)
    cs.reserve_margins(fig, layout="single_panel")

    # ----- Bars: grouped horizontal, two bars per brand -----
    # Anthropic on top, OpenAI on bottom — they share a brand row
    y = np.arange(len(brands))
    bar_height = 0.38

    # Color rule: Mint highlighted in Indigo (Anthropic darker, OpenAI lighter).
    # All other brands in Black 60 / Black 20 (darker = Anthropic; lighter = OpenAI).
    # This single-accent + neutral pairing is the brand-spec default.
    anthropic_colors = [cs.ACCENT_INDIGO if b == HIGHLIGHT else cs.BLACK_60 for b in brands]
    openai_colors = [cs.PETRO if b == HIGHLIGHT else cs.BLACK_20 for b in brands]

    bars_a = ax.barh(y - bar_height/2, pres_anthropic, bar_height,
                     color=anthropic_colors, label="Anthropic")
    bars_o = ax.barh(y + bar_height/2, pres_openai, bar_height,
                     color=openai_colors, label="OpenAI")

    # ----- Axis setup -----
    ax.set_yticks(y)
    ax.set_yticklabels(brands, fontsize=cs.FONT_SIZES_3COL["axis_tick"])
    ax.invert_yaxis()  # top brand at top
    ax.set_xlim(0, 105)
    ax.set_xlabel("AI Presence (%)", fontsize=cs.FONT_SIZES_3COL["axis_label"])
    cs.style_axis_minimal(ax, orientation="horizontal_bar")

    # ----- Legend (compact, top-right of plot area) -----
    # Use proxy artists so legend swatches use the highlight color (Indigo / Petro)
    # rather than gray which would be visually ambiguous.
    from matplotlib.patches import Patch
    legend_elems = [
        Patch(facecolor=cs.ACCENT_INDIGO, label="Anthropic"),
        Patch(facecolor=cs.PETRO, label="OpenAI"),
    ]
    ax.legend(
        handles=legend_elems,
        loc="lower right",
        fontsize=cs.FONT_SIZES_3COL["legend"],
        frameon=False,
    )

    # ----- Editorial title + subtitle -----
    cs.editorial_title(
        ax,
        title="Phantom brand presence",
        subtitle=(
            "Mint shut down March 2024.\n"
            "25 months later, AI still mentions it 44% of the time."
        ),
        column_span="3col_inline",
    )

    # Note: deliberately no inline callout near Mint. The subtitle already
    # says "shut down March 2024" and the Indigo/Petro highlight is the
    # only colored pair in the chart — the reader's eye finds it without
    # an annotation. Adding a callout collides with the legend and
    # over-explains what color already communicates.

    # ----- Source line (contains version — no separate stamp needed at 3-col) -----
    # At 6-col hero we'd add a version stamp; at 3-col inline the source line
    # is enough and a stamp would collide.
    cs.add_source(ax, SOURCE_TEXT)

    # ----- Save using canonical helper -----
    written = cu.save_chart(fig, pattern_id="p6", column_span="3", output_dir=output_dir)
    plt.close(fig)
    return written


if __name__ == "__main__":
    paths = render()
    print(f"Rendered Pattern 6:")
    for p in paths:
        print(f"  {p}")
