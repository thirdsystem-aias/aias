"""
Pattern 8 — Aggregate Matrix.

The report's master summary chart. Six framework patterns × five
categories + one Modes row at the bottom. Each cell shows a concrete
data label (e.g. "9 brands", "Spanish < 25%", "6/6 CEPs") and a 5-step
intensity shading (Not present → Very strong) that encodes how strong
the pattern is in that category.

This differs from a generic heatmap in two important ways:

  1. Each cell holds a **categorical evidence tag** — not a 0-100 score.
     The reader sees the actual finding ("9 brands show asymmetry"),
     not a derived number requiring interpretation. This makes the
     chart a self-contained summary of the report's findings.

  2. Each column uses **its own category accent color** at varying
     opacity (driven by intensity). This visually separates categories
     while keeping shading meaningful within each column. Avoids the
     "every cell uses Indigo" flatness that loses category identity.

The Modes row shows response-mode codes ("B", "B/C", "B/C/A") observed
in each category — Brand mention vs Component framing vs Authority
citation.

Cell labels and intensities are populated from MATRIX_CONTENT, a
dict-of-dicts at the top of the file. v0.6 values match the published
report; future versions edit this dict.

Renders to: reports/output/chart_aggregate_6col.pdf
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

_THIS = Path(__file__).resolve()
_REPORTS = _THIS.parent.parent
if str(_REPORTS) not in sys.path:
    sys.path.insert(0, str(_REPORTS))

import chart_style as cs
import chart_utils as cu


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

CATEGORIES_DISPLAY_ORDER = ["PM", "Running", "Olive Oil", "Skincare", "Finance"]

# Column header labels — kept short so each line fits within one column width
# at FIGSIZE_6COL_TALL. The full category names appear in the report body;
# headers just need to be unambiguous and scannable.
CATEGORY_LABELS = {
    "PM":        "Project Mgmt\nSoftware",
    "Running":   "Running\nShoes",
    "Olive Oil": "Premium\nOlive Oil",
    "Skincare":  "Premium\nSkincare",
    "Finance":   "Personal\nFinance Apps",
}

# Each category gets its own accent color. Cell intensity = opacity of
# this color. This makes each column visually distinct while keeping
# the strength-shading semantics intact within each column.
#
# Color assignments use distinct hues across the spectrum so adjacent
# columns never look similar:
#   PM        — Indigo (cool purple)
#   Running   — Tree green (warm green)
#   Olive Oil — Honey (warm yellow)
#   Skincare  — Copper Plate (warm orange)
#   Finance   — Ocean (cool blue)
CATEGORY_COLORS = {
    "PM":        cs.ACCENT_INDIGO,        # #37237B
    "Running":   cs.ACCENT_TREE,          # #A4C032 — green, clearly distinct from Indigo
    "Olive Oil": cs.ACCENT_HONEY if hasattr(cs, "ACCENT_HONEY") else cs.ACCENT_COPPER_PLATE,
    "Skincare":  cs.ACCENT_COPPER_PLATE,  # #F36C35
    "Finance":   cs.ACCENT_OCEAN if hasattr(cs, "ACCENT_OCEAN") else cs.COLOR_INCUMBENT,
}

# Pattern rows. (key, full label including pattern name and descriptor)
PATTERN_ROWS = [
    ("p1", "Pattern 1",                 "Per-model variance"),
    ("p2", "Pattern 2",                 "Comparison/Discovery asymmetry"),
    ("p3", "Pattern 3",                 "AI vs awareness divergence"),
    ("p4", "Pattern 4",                 "Discourse-language bias"),
    ("p5", "Pattern 5",                 "Default Reinforcement"),
    ("p6", "Pattern 6",                 "Phantom brand presence"),
    ("modes", "Modes",                  "Response-mode behavior"),
]

# Intensity scale — 0 (not present) to 4 (very strong). Drives cell opacity.
INTENSITY_SCALE = {
    0: ("Not present",  0.00),
    1: ("Weak",         0.20),
    2: ("Moderate",     0.45),
    3: ("Strong",       0.70),
    4: ("Very strong",  0.95),
}

# v0.6 cell content. Each cell: (label, intensity 0-4).
# Intensity 0 = "—" rendered, no fill.
# Edit this dict to update the chart for new report versions.
#
# Pattern 1 — Per-model variance (in points, the cross-model spread)
# Pattern 2 — # brands showing Comparison/Discovery asymmetry
# Pattern 3 — # brands with AI/awareness divergence
# Pattern 4 — Discourse-language bias finding (or "—" if N/A)
# Pattern 5 — Default Reinforcement (CEPs where it holds)
# Pattern 6 — Phantom brand presence (named brand + rate, or "—")
# Modes — observed response-mode codes (B = Brand, C = Component, A = Authority)
MATRIX_CONTENT: dict[str, dict[str, tuple[str, int]]] = {
    "PM": {
        "p1":   ("42pt",        2),
        "p2":   ("9 brands",    4),
        "p3":   ("2 brands",    1),
        "p4":   ("—",           0),
        "p5":   ("6/6 CEPs",    4),
        "p6":   ("—",           0),
        "modes":("B",           2),
    },
    "Running": {
        "p1":   ("29pt",        1),
        "p2":   ("9 brands",    4),
        "p3":   ("2 brands",    1),
        "p4":   ("—",           0),
        "p5":   ("6/6 CEPs",    4),
        "p6":   ("—",           0),
        "modes":("B",           2),
    },
    "Olive Oil": {
        "p1":   ("40pt",        2),
        "p2":   ("5 brands",    2),
        "p3":   ("4 brands",    2),
        "p4":   ("Spanish < 25%", 3),
        "p5":   ("5/6 CEPs",    3),
        "p6":   ("—",           0),
        "modes":("B/C",         3),
    },
    "Skincare": {
        "p1":   ("23pt",        1),
        "p2":   ("7 brands",    3),
        "p3":   ("8 brands",    4),
        "p4":   ("Korean = 0%", 4),
        "p5":   ("4/6 CEPs",    2),
        "p6":   ("—",           0),
        "modes":("B/C/A",       4),
    },
    "Finance": {
        "p1":   ("71pt",        4),
        "p2":   ("4 brands",    2),
        "p3":   ("5 brands",    2),
        "p4":   ("—",           0),
        "p5":   ("6/6 CEPs",    4),
        "p6":   ("Mint 44%",    3),
        "modes":("B",           2),
    },
}

SOURCE_TEXT = "Source: Third System AI Presence Index v0.6 · April 2026"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _hex_to_rgba(hex_color: str, alpha: float) -> tuple[float, float, float, float]:
    """Convert hex color + alpha to matplotlib RGBA tuple."""
    rgb = mcolors.to_rgb(hex_color)
    return (rgb[0], rgb[1], rgb[2], alpha)


# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------

def render(output_dir: Path | str | None = None) -> list[Path]:
    """Render Pattern 8 aggregate matrix."""
    n_rows = len(PATTERN_ROWS)              # 7 (6 patterns + Modes)
    n_cols = len(CATEGORIES_DISPLAY_ORDER)  # 5

    # 6-col TALL hero — fits 7 rows × 5 cols comfortably with row labels
    fig = plt.figure(figsize=cs.FIGSIZE_6COL_TALL)
    sizes = cs.font_sizes_for("6col")

    # Vertical budget (top → bottom):
    #   0.96  title
    #   0.93  subtitle line 1
    #   0.90  subtitle line 2
    #   0.86  matrix top edge (column headers sit just above)
    #   0.18  matrix bottom edge
    #   0.10  intensity legend
    #   0.025 source
    matrix_left = 0.22       # tighter — row labels don't need as much room as I gave them
    matrix_right = 0.97
    matrix_top_y = 0.78      # leaves room for title/subtitle band + col headers
    matrix_bot_y = 0.18

    matrix_ax = fig.add_axes([
        matrix_left, matrix_bot_y,
        matrix_right - matrix_left, matrix_top_y - matrix_bot_y,
    ])

    # ----- Draw cells -----
    for i, (pkey, _label, _sub) in enumerate(PATTERN_ROWS):
        # Row position — first pattern at top, Modes row at bottom
        y = n_rows - 1 - i
        # Modes row gets a subtle visual separator: insert a small gap above
        is_modes_row = (pkey == "modes")
        for j, cat in enumerate(CATEGORIES_DISPLAY_ORDER):
            content = MATRIX_CONTENT[cat][pkey]
            label_text, intensity = content
            base_color = CATEGORY_COLORS[cat]
            _name, alpha = INTENSITY_SCALE[intensity]
            face = _hex_to_rgba(base_color, alpha) if intensity > 0 else _hex_to_rgba("#FFFFFF", 0.0)

            # Slight gap above modes row to set it apart visually
            cell_bottom = y + (-0.04 if is_modes_row else 0)
            cell_height = 1.0 if not is_modes_row else 0.96

            rect = plt.Rectangle(
                (j, cell_bottom),
                1, cell_height,
                facecolor=face,
                edgecolor=cs.COLOR_PAPER,
                linewidth=1.2,
                zorder=2,
            )
            matrix_ax.add_patch(rect)

            # Cell label — color flips with intensity for legibility on darker fills
            text_color = cs.COLOR_PAPER if intensity >= 3 else cs.COLOR_TEXT
            text_weight = "bold" if intensity >= 3 else "normal"
            matrix_ax.text(
                j + 0.5, cell_bottom + cell_height / 2,
                label_text,
                ha="center", va="center",
                fontsize=sizes["data_label"],
                color=text_color,
                fontweight=text_weight,
                zorder=3,
            )

    # Set up axis bounds
    matrix_ax.set_xlim(0, n_cols)
    matrix_ax.set_ylim(-0.05, n_rows)
    matrix_ax.set_xticks([])
    matrix_ax.set_yticks([])
    for spine in matrix_ax.spines.values():
        spine.set_visible(False)
    matrix_ax.grid(False)

    # ----- Column headers (above matrix, in each column's accent color) -----
    for j, cat in enumerate(CATEGORIES_DISPLAY_ORDER):
        color = CATEGORY_COLORS[cat]
        matrix_ax.text(
            j + 0.5,
            n_rows + 0.20,
            CATEGORY_LABELS[cat],
            ha="center", va="bottom",
            fontsize=sizes["axis_label"],
            color=color,
            fontweight="bold",
            transform=matrix_ax.transData,
        )

    # ----- Row labels (left of matrix, two-line: pattern name + descriptor) -----
    for i, (pkey, label, sub) in enumerate(PATTERN_ROWS):
        y = n_rows - 1 - i
        is_modes_row = (pkey == "modes")
        cell_bottom = y + (-0.04 if is_modes_row else 0)
        cell_height = 1.0 if not is_modes_row else 0.96
        center_y = cell_bottom + cell_height / 2

        # Pattern label (bold) above descriptor (normal)
        matrix_ax.text(
            -0.06, center_y + 0.16,
            label,
            ha="right", va="center",
            fontsize=sizes["axis_tick"],
            color=cs.COLOR_TEXT,
            fontweight="bold",
            transform=matrix_ax.transData,
        )
        matrix_ax.text(
            -0.06, center_y - 0.16,
            sub,
            ha="right", va="center",
            fontsize=sizes["source_caption"],
            color=cs.COLOR_MUTED,
            transform=matrix_ax.transData,
        )

    # ----- Intensity legend (5 swatches below matrix) -----
    legend_y_top = matrix_bot_y - 0.03
    legend_y_bot = legend_y_top - 0.04
    legend_label_y = legend_y_bot - 0.025

    legend_ax = fig.add_axes([
        matrix_left, legend_y_bot,
        matrix_right - matrix_left, legend_y_top - legend_y_bot,
    ])
    legend_ax.set_axis_off()
    legend_ax.set_xlim(0, 1)
    legend_ax.set_ylim(0, 1)

    # 5 swatches using neutral Indigo, evenly spaced
    legend_swatch_color = cs.ACCENT_INDIGO
    legend_label = "Pattern strength:"
    fig.text(
        0.04, legend_y_top + 0.005,
        legend_label,
        fontsize=sizes["axis_tick"],
        color=cs.COLOR_MUTED,
        fontweight="bold",
        ha="left", va="bottom",
    )

    swatch_width = 0.07  # in figure-relative units
    swatch_gap = 0.005
    swatch_block_left = 0.16
    for level in range(5):
        _name, alpha = INTENSITY_SCALE[level]
        x = swatch_block_left + level * (swatch_width + swatch_gap)
        # Swatch
        rect = plt.Rectangle(
            (x, legend_y_bot + 0.01),
            swatch_width, legend_y_top - legend_y_bot - 0.01,
            facecolor=_hex_to_rgba(legend_swatch_color, alpha) if alpha > 0 else "#FFFFFF",
            edgecolor=cs.COLOR_GRID if alpha == 0 else "none",
            linewidth=0.5,
            transform=fig.transFigure,
        )
        fig.patches.append(rect)
        # Label below swatch
        fig.text(
            x + swatch_width / 2,
            legend_label_y,
            _name,
            ha="center", va="top",
            fontsize=sizes["source_caption"],
            color=cs.COLOR_MUTED,
        )

    # ----- Footer note (right of legend) -----
    fig.text(
        0.97, legend_y_top + 0.005,
        "Empty cells (—) indicate the pattern does not apply to this category.",
        fontsize=sizes["source_caption"],
        color=cs.COLOR_MUTED,
        style="italic",
        ha="right", va="bottom",
    )

    # ----- Title + 2-line subtitle -----
    fig.text(
        0.04, 0.965,
        "Six framework patterns × five categories: how the framework holds",
        fontsize=sizes["title"], fontweight="bold",
        color=cs.COLOR_TEXT, ha="left", va="top",
    )
    fig.text(
        0.04, 0.93,
        "Cell intensity shows the strength of evidence for each pattern in each category.",
        fontsize=sizes["subtitle"], color=cs.COLOR_MUTED,
        ha="left", va="top",
    )
    fig.text(
        0.04, 0.905,
        "The bottom row summarizes which response modes were observed.",
        fontsize=sizes["subtitle"], color=cs.COLOR_MUTED,
        ha="left", va="top",
    )

    # Source line
    fig.text(
        0.04, 0.018, SOURCE_TEXT,
        fontsize=sizes["source_caption"], color=cs.COLOR_MUTED,
        style="italic", ha="left", va="bottom",
    )

    # Save (no bbox='tight' — would eat reserved row/legend margins)
    if output_dir is None:
        output_dir = _REPORTS / "output"
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_pdf = output_dir / "chart_aggregate_6col.pdf"
    fig.savefig(output_pdf, dpi=cs.DPI_PRINT, pad_inches=cs.PAD_INCHES)
    plt.close(fig)
    return [output_pdf]


if __name__ == "__main__":
    paths = render()
    print(f"Rendered Pattern 8 (aggregate matrix, content-driven):")
    for p in paths:
        print(f"  {p}")
