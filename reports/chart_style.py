"""
chart_style.py — Third System chart styling foundation.

Sources every value from brand/third_system_brand.json. No hardcoded hex values.
No improvised figsize. No invented font sizes. Every chart in reports/charts/
imports from this module to inherit the brand-locked defaults.

Convention: this file is read-only at runtime — it loads the brand JSON at
import time and exposes constants. To change a color, edit the brand JSON.

Brand spec source: third_system_brand.json schema 1.4
"""

from __future__ import annotations

import json
import logging
import warnings
from pathlib import Path
from typing import Any

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.figure import Figure


# ---------------------------------------------------------------------------
# Brand JSON loading
# ---------------------------------------------------------------------------

# Resolve brand JSON path relative to this file:
#   reports/chart_style.py  -->  brand/third_system_brand.json
_THIS_DIR = Path(__file__).resolve().parent
_BRAND_JSON_PATH = _THIS_DIR.parent / "brand" / "third_system_brand.json"

if not _BRAND_JSON_PATH.exists():
    raise FileNotFoundError(
        f"Brand spec not found at {_BRAND_JSON_PATH}. "
        f"chart_style.py expects brand/third_system_brand.json one level up "
        f"from reports/. Check directory structure."
    )

with open(_BRAND_JSON_PATH) as _f:
    BRAND: dict[str, Any] = json.load(_f)

BRAND_SCHEMA_VERSION = BRAND["_meta"]["schema_version"]


def _hex_from_pcm(category: str, key: str) -> str:
    """Pull a hex value from palette.python_constant_mapping by path."""
    pcm = BRAND["palette"]["python_constant_mapping"]
    return pcm[category][key]["hex"]


# ---------------------------------------------------------------------------
# Color constants — sourced from python_constant_mapping
# ---------------------------------------------------------------------------

# Grayscale (six-step ramp)
BLACK_10 = _hex_from_pcm("grayscale", "BLACK_10")     # #E5E5E5
BLACK_20 = _hex_from_pcm("grayscale", "BLACK_20")     # #CCCCCC
BLACK_40 = _hex_from_pcm("grayscale", "BLACK_40")     # #999999
BLACK_60 = _hex_from_pcm("grayscale", "BLACK_60")     # #666666
BLACK_80 = _hex_from_pcm("grayscale", "BLACK_80")     # #333333
BLACK_100 = _hex_from_pcm("grayscale", "BLACK_100")   # #000000

# Accent — most-saturated tint per data viz family
ACCENT_INDIGO = _hex_from_pcm("accent_per_family", "ACCENT_INDIGO")               # #37237B
ACCENT_OCEAN = _hex_from_pcm("accent_per_family", "ACCENT_OCEAN")                 # #007EAE
ACCENT_TREE = _hex_from_pcm("accent_per_family", "ACCENT_TREE")                   # #A4C032
ACCENT_COPPER_PLATE = _hex_from_pcm("accent_per_family", "ACCENT_COPPER_PLATE")   # #F36C35
ACCENT_RUBINE = _hex_from_pcm("accent_per_family", "ACCENT_RUBINE")               # #C40067
ACCENT_AQUA = _hex_from_pcm("accent_per_family", "ACCENT_AQUA")                   # #08C3A5
ACCENT_HONEY = _hex_from_pcm("accent_per_family", "ACCENT_HONEY")                 # #FFAC17

# Indigo family (the brand identity, full ramp)
INDIGO = _hex_from_pcm("indigo_family_full", "INDIGO")                # #37237B
AMETHYST = _hex_from_pcm("indigo_family_full", "AMETHYST")            # #534F9E
PETRO = _hex_from_pcm("indigo_family_full", "PETRO")                  # #6A6AB1
IRIS = _hex_from_pcm("indigo_family_full", "IRIS")                    # #908EC5
LAVENDER_GREY = _hex_from_pcm("indigo_family_full", "LAVENDER_GREY")  # #BBB9DD

# Warm neutrals (five-step earth ramp)
NEUTRAL_1 = _hex_from_pcm("warm_neutrals", "NEUTRAL_1")  # #CEC2B4
NEUTRAL_2 = _hex_from_pcm("warm_neutrals", "NEUTRAL_2")  # #B7A99A — diverging midpoint
NEUTRAL_3 = _hex_from_pcm("warm_neutrals", "NEUTRAL_3")  # #A39382
NEUTRAL_4 = _hex_from_pcm("warm_neutrals", "NEUTRAL_4")  # #7A6855
NEUTRAL_5 = _hex_from_pcm("warm_neutrals", "NEUTRAL_5")  # #473729

# Semantic UI (text, muted text, grid lines, paper background)
COLOR_TEXT = _hex_from_pcm("semantic_ui", "COLOR_TEXT")               # #231F20
COLOR_MUTED = _hex_from_pcm("semantic_ui", "COLOR_MUTED")             # #6B6967
COLOR_GRID = _hex_from_pcm("semantic_ui", "COLOR_GRID")               # #CCCCCC
COLOR_GRID_SUBTLE = _hex_from_pcm("semantic_ui", "COLOR_GRID_SUBTLE") # #E5E5E5
COLOR_PAPER = _hex_from_pcm("semantic_ui", "COLOR_PAPER")             # #FAF7F2

# Tier semantics (the canonical AIPT encoding)
COLOR_INCUMBENT = _hex_from_pcm("tier_semantics", "COLOR_INCUMBENT")     # #37237B Indigo
COLOR_MIDTIER = _hex_from_pcm("tier_semantics", "COLOR_MIDTIER")         # #6A6AB1 Petro
COLOR_CHALLENGER = _hex_from_pcm("tier_semantics", "COLOR_CHALLENGER")   # #F36C35 Copper Plate

TIER_COLORS = {
    "incumbent": COLOR_INCUMBENT,
    "midtier": COLOR_MIDTIER,
    "challenger": COLOR_CHALLENGER,
}

# Additional recommended constants
BRAND_INDIGO = _hex_from_pcm("additional_recommended_constants", "BRAND_INDIGO")  # #37237B
MIDPOINT_NEUTRAL = _hex_from_pcm("additional_recommended_constants", "MIDPOINT_NEUTRAL")  # #B7A99A


# ---------------------------------------------------------------------------
# Chart palette schemes — derived from chart_palette_recommended /_extended
# ---------------------------------------------------------------------------

QUALITATIVE_RECOMMENDED = {
    "primary": ACCENT_INDIGO,
    "secondary_neutral": BLACK_20,
    "tertiary_neutral": BLACK_40,
    "quaternary_neutral": BLACK_60,
    "highlight_alternate": ACCENT_COPPER_PLATE,
}

# Ordered series for charts with 4+ qualitative categories
# Sourced from palette.chart_palette_extended.ordered_series
QUALITATIVE_STANDARD_ORDER: list[str] = [
    s["hex"] for s in BRAND["palette"]["chart_palette_extended"]["ordered_series"]
]


# ---------------------------------------------------------------------------
# Chart sizing — sourced from chart_construction_rules.chart_sizing_specifications
# ---------------------------------------------------------------------------

_SIZING = BRAND["chart_construction_rules"]["chart_sizing_specifications"]
_FIGSIZE_BY_SPAN = _SIZING["figsize_by_column_span"]

# Locked figsize tuples — every chart sources from these, no improvisation.
FIGSIZE_3COL_INLINE: tuple[float, float] = tuple(_FIGSIZE_BY_SPAN["3_column_inline"]["matplotlib_figsize"])
FIGSIZE_4COL: tuple[float, float] = tuple(_FIGSIZE_BY_SPAN["4_column"]["matplotlib_figsize"])
FIGSIZE_6COL_HERO: tuple[float, float] = tuple(_FIGSIZE_BY_SPAN["6_column_hero"]["matplotlib_figsize"])
FIGSIZE_6COL_TALL: tuple[float, float] = tuple(_FIGSIZE_BY_SPAN["6_column_hero_tall"]["matplotlib_figsize"])
FIGSIZE_6COL_SHORT: tuple[float, float] = tuple(_FIGSIZE_BY_SPAN["6_column_hero_short"]["matplotlib_figsize"])
FIGSIZE_2COL: tuple[float, float] = tuple(_FIGSIZE_BY_SPAN["2_column"]["matplotlib_figsize"])

# Two-panel spread (Pattern 4 country origin, etc.)
# Spread is 6_column_hero with wspace=0.18 between panels
FIGSIZE_SPREAD: tuple[float, float] = (7.5, 4.5)
SPREAD_WSPACE = 0.18


# ---------------------------------------------------------------------------
# Font size scaling — sourced from font_size_scaling.by_column_span
# ---------------------------------------------------------------------------

FONT_SIZES_3COL = _SIZING["font_size_scaling"]["default_3col_inline"]
FONT_SIZES_6COL = _SIZING["font_size_scaling"]["default_6col_hero"]


def _build_size_dict_from_table(col_index: int) -> dict[str, float]:
    """Pull a column's worth of sizes from the by_column_span table.

    Table columns: 1col=0, 2col=1, 3col=2, 4col=3, 6col=4 (index into the list).
    """
    table = _SIZING["font_size_scaling"]["by_column_span"]
    elements = ("title", "subtitle", "axis_label", "axis_tick",
                "data_label", "legend", "annotation", "source_caption")
    return {el: table[el][col_index] for el in elements}


# Pre-built size dicts for the spans we use most often
FONT_SIZES_2COL = _build_size_dict_from_table(1)
FONT_SIZES_4COL = _build_size_dict_from_table(3)


def font_sizes_for(column_span: str) -> dict[str, float]:
    """Return font-size dict for a given column span.

    Accepts: '1col', '2col', '3col', '3col_inline', '4col',
             '6col', '6col_hero', '6col_tall', '6col_short', 'spread'

    Each maps to the appropriate size table from the brand spec.
    Default fallback is 3col_inline.
    """
    span = column_span.lower()
    if span in ("6col", "6col_hero", "6col_tall", "6col_short", "spread"):
        return FONT_SIZES_6COL.copy()
    if span == "4col":
        return FONT_SIZES_4COL.copy()
    if span == "2col":
        return FONT_SIZES_2COL.copy()
    if span == "1col":
        return _build_size_dict_from_table(0)
    return FONT_SIZES_3COL.copy()


# ---------------------------------------------------------------------------
# DPI / output specifications
# ---------------------------------------------------------------------------

DPI_PRINT = _SIZING["dpi_targets"]["print"]["dpi"]              # 300
DPI_SCREEN_HIGH = _SIZING["dpi_targets"]["screen_high"]["dpi"]  # 144
DPI_SCREEN_STANDARD = _SIZING["dpi_targets"]["screen_standard"]["dpi"]  # 96
DPI_THUMBNAIL = _SIZING["dpi_targets"]["thumbnail"]["dpi"]      # 72
DPI_DEFAULT = DPI_PRINT  # print-first; downscales correctly for screen

# Figure padding for savefig — sourced from padding_and_bbox.savefig_params
_SAVEFIG_PARAMS = _SIZING["padding_and_bbox"]["savefig_params"]
PAD_INCHES = _SAVEFIG_PARAMS["pad_inches"]    # 0.15
BBOX_INCHES = _SAVEFIG_PARAMS["bbox_inches"]  # "tight"


# ---------------------------------------------------------------------------
# Typography — Akkurat Pro with Inter fallback
# ---------------------------------------------------------------------------

PRIMARY_FONT_FAMILY = BRAND["typography"]["primary_face"]  # "Akkurat Pro"
FALLBACK_FONT_FAMILY = "Inter"

_FONT_REGISTRATION_LOG: list[str] = []


def _register_fonts() -> str:
    """Attempt to register Akkurat Pro; fall back to Inter; document substitution.

    Returns the font family name actually configured.
    """
    available = {f.name for f in font_manager.fontManager.ttflist}

    if PRIMARY_FONT_FAMILY in available:
        _FONT_REGISTRATION_LOG.append(f"Using {PRIMARY_FONT_FAMILY} (registered).")
        return PRIMARY_FONT_FAMILY

    if FALLBACK_FONT_FAMILY in available:
        msg = (
            f"Akkurat Pro not available; falling back to {FALLBACK_FONT_FAMILY}. "
            f"Document this substitution in the rendering log."
        )
        _FONT_REGISTRATION_LOG.append(msg)
        warnings.warn(msg, UserWarning)
        return FALLBACK_FONT_FAMILY

    # Neither available — use matplotlib default but flag clearly
    msg = (
        f"Neither Akkurat Pro nor Inter installed. Using matplotlib default sans. "
        f"Charts will render but typography will not match brand spec. "
        f"To fix: install Inter (free) via Homebrew: `brew install --cask font-inter`"
    )
    _FONT_REGISTRATION_LOG.append(msg)
    warnings.warn(msg, UserWarning)
    return "DejaVu Sans"


CONFIGURED_FONT_FAMILY = _register_fonts()


def font_registration_log() -> list[str]:
    """Return the list of font registration messages logged at import time."""
    return _FONT_REGISTRATION_LOG.copy()


# ---------------------------------------------------------------------------
# Matplotlib rcParams — apply Third System defaults globally
# ---------------------------------------------------------------------------

def apply_third_system_rc() -> None:
    """Apply Third System default rcParams to matplotlib.

    Idempotent — safe to call multiple times. Charts that need to override
    a specific value should do so locally with ax.set_xxx() rather than
    mutating rcParams.
    """
    mpl.rcParams.update({
        # Typography — must register Akkurat Pro as a sans-serif family member,
        # NOT set font.family to the face name directly. Matplotlib's rcParams
        # treats font.family='Akkurat Pro' as a generic family lookup and silently
        # falls back; setting font.sans-serif=[face_name, fallback, ...] AND
        # font.family='sans-serif' is the working pattern.
        "font.family": "sans-serif",
        "font.sans-serif": [CONFIGURED_FONT_FAMILY, "Inter", "DejaVu Sans"],
        "font.size": FONT_SIZES_3COL["axis_tick"],

        # Colors
        "text.color": COLOR_TEXT,
        "axes.labelcolor": COLOR_TEXT,
        "axes.edgecolor": COLOR_GRID,
        "axes.titlecolor": COLOR_TEXT,
        "xtick.color": COLOR_MUTED,
        "ytick.color": COLOR_MUTED,
        "axes.facecolor": "white",
        "figure.facecolor": "white",

        # Spines — minimal editorial style: bottom + left only by default
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.spines.bottom": True,
        "axes.spines.left": True,
        "axes.linewidth": 0.5,

        # Grid — subtle horizontal grid only
        "axes.grid": True,
        "axes.grid.axis": "y",
        "grid.color": COLOR_GRID_SUBTLE,
        "grid.linewidth": 0.5,
        "grid.linestyle": "-",

        # Ticks — minimal
        "xtick.major.width": 0.5,
        "ytick.major.width": 0.5,
        "xtick.major.size": 3,
        "ytick.major.size": 3,
        "xtick.minor.size": 0,
        "ytick.minor.size": 0,
        "xtick.direction": "out",
        "ytick.direction": "out",

        # Legend
        "legend.frameon": False,
        "legend.fontsize": FONT_SIZES_3COL["legend"],

        # Saving
        "savefig.dpi": DPI_DEFAULT,
        "savefig.bbox": BBOX_INCHES,
        "savefig.pad_inches": PAD_INCHES,
        "pdf.fonttype": 42,  # TrueType in PDF (better cross-platform rendering)
        "ps.fonttype": 42,
    })


# Apply defaults at import time so any chart importing chart_style gets them
apply_third_system_rc()


# ---------------------------------------------------------------------------
# Subplots-adjust margins — sourced from spec
# ---------------------------------------------------------------------------

_SUBPLOTS_ADJUST = _SIZING["subplots_adjust_defaults"]

MARGINS_SINGLE_PANEL = {k: v for k, v in _SUBPLOTS_ADJUST["single_panel"].items() if not k.startswith("_")}
MARGINS_TWO_PANEL = {k: v for k, v in _SUBPLOTS_ADJUST["two_panel_landscape"].items() if not k.startswith("_")}
MARGINS_TALL_WITH_LEGEND = {k: v for k, v in _SUBPLOTS_ADJUST["tall_with_legend_below"].items() if not k.startswith("_")}


def reserve_margins(fig: Figure, layout: str = "single_panel") -> None:
    """Reserve top/bottom/left/right margins on a figure per brand spec.

    layout: 'single_panel' | 'two_panel_landscape' | 'tall_with_legend_below'

    Call this BEFORE editorial_title() and add_source() to ensure the title
    sits in reserved whitespace above the plot, not on top of the data.
    """
    if layout == "two_panel_landscape":
        fig.subplots_adjust(**MARGINS_TWO_PANEL)
    elif layout == "tall_with_legend_below":
        fig.subplots_adjust(**MARGINS_TALL_WITH_LEGEND)
    else:
        fig.subplots_adjust(**MARGINS_SINGLE_PANEL)


# ---------------------------------------------------------------------------
# Editorial helpers — title, subtitle, source attribution
# ---------------------------------------------------------------------------

def editorial_title(
    ax,
    title: str,
    subtitle: str | None = None,
    column_span: str = "3col_inline",
    pad: float = 14.0,
) -> None:
    """Place an editorial-style title (and optional subtitle) above an Axes.

    Uses axes-level title via ax.set_title() for compatibility with
    bbox_inches='tight'. Subtitle is added as figure-level text just above
    the axes, in muted gray.

    Multi-line subtitles are supported: pass a string with embedded '\\n'.
    Padding above the plot is automatically extended for each additional
    subtitle line so the bars/data don't crowd the subtitle.

    For the spec's positioning to look right, call reserve_margins(fig)
    BEFORE drawing data, so the plot has whitespace above for the title.
    """
    sizes = font_sizes_for(column_span)

    if subtitle:
        # Count subtitle lines for padding/positioning math
        subtitle_lines = subtitle.split("\n")
        n_lines = len(subtitle_lines)
        # Each line takes ~ subtitle font size + 2pt leading
        per_line_pt = sizes["subtitle"] + 2

        # Title pad: room for title + (n_lines × subtitle line height) + buffer
        ax.set_title(
            title,
            fontsize=sizes["title"],
            fontweight="bold",
            color=COLOR_TEXT,
            loc="left",
            pad=pad + (n_lines * per_line_pt) + 4,
        )

        # Subtitle as figure-level text positioned just below title.
        # First line sits closest to the axes top; subsequent lines stack above.
        ax_top_y = ax.get_position().y1
        ax_left_x = ax.get_position().x0
        fig = ax.figure
        fig_height_in = fig.get_figheight()

        # Convert per_line_pt to figure-fraction units
        per_line_fraction = (per_line_pt / 72.0) / fig_height_in
        # First line offset above axes (closest line)
        first_line_y = ax_top_y + (0.04 / fig_height_in)

        # Render each subtitle line. Lines display top→bottom in source order:
        # if subtitle = "Line A\nLine B", Line A appears above Line B.
        # We position from bottom up: last line at first_line_y, going up.
        for i, line in enumerate(reversed(subtitle_lines)):
            line_y = first_line_y + (i * per_line_fraction)
            fig.text(
                ax_left_x, line_y, line,
                ha="left", va="bottom",
                fontsize=sizes["subtitle"],
                color=COLOR_MUTED,
            )
    else:
        ax.set_title(
            title,
            fontsize=sizes["title"],
            fontweight="bold",
            color=COLOR_TEXT,
            loc="left",
            pad=pad,
        )


def add_source(
    ax_or_fig,
    source_text: str,
    column_span: str = "3col_inline",
) -> None:
    """Place a source-citation line below the plot area.

    Accepts either an Axes (places source under that axes) or a Figure
    (places source at bottom-left of figure). The Axes version is preferred
    because it auto-aligns to the plot's left edge.
    """
    sizes = font_sizes_for(column_span)

    # Detect whether ax_or_fig is an Axes or Figure
    if hasattr(ax_or_fig, "get_position"):
        # It's an Axes
        ax = ax_or_fig
        fig = ax.figure
        fig_height_in = fig.get_figheight()
        ax_bottom_y = ax.get_position().y0
        ax_left_x = ax.get_position().x0
        # Place source 0.50in below the axes bottom (gives room for x-axis tick labels + axis label)
        source_y = max(0.01, ax_bottom_y - (0.50 / fig_height_in))
        fig.text(
            ax_left_x, source_y, source_text,
            ha="left", va="bottom",
            fontsize=sizes["source_caption"],
            color=COLOR_MUTED,
            style="italic",
        )
    else:
        # It's a Figure — fall back to fixed bottom-left position
        fig = ax_or_fig
        fig_height = fig.get_figheight()
        source_y = 0.0 + (0.08 / fig_height)
        fig.text(
            0.02, source_y, source_text,
            ha="left", va="bottom",
            fontsize=sizes["source_caption"],
            color=COLOR_MUTED,
            style="italic",
        )


def add_version_stamp(
    ax_or_fig,
    version: str,
    date: str | None = None,
    column_span: str = "3col_inline",
) -> None:
    """Place a small version stamp in the bottom-right corner of the figure.

    Used to mark every chart with its report-version provenance —
    builds the visible versioning discipline the system needs.

    Example: add_version_stamp(ax, version="v0.6", date="30 Apr 2026")
    """
    sizes = font_sizes_for(column_span)
    stamp_text = version if version.startswith("v") else f"v{version}"
    if date:
        stamp_text = f"{stamp_text} · {date}"

    if hasattr(ax_or_fig, "get_position"):
        ax = ax_or_fig
        fig = ax.figure
        fig_height_in = fig.get_figheight()
        ax_bottom_y = ax.get_position().y0
        ax_right_x = ax.get_position().x1
        stamp_y = max(0.01, ax_bottom_y - (0.50 / fig_height_in))
        fig.text(
            ax_right_x, stamp_y, stamp_text,
            ha="right", va="bottom",
            fontsize=sizes["source_caption"],
            color=COLOR_MUTED,
        )
    else:
        fig = ax_or_fig
        fig_height = fig.get_figheight()
        stamp_y = 0.0 + (0.08 / fig_height)
        fig.text(
            0.98, stamp_y, stamp_text,
            ha="right", va="bottom",
            fontsize=sizes["source_caption"],
            color=COLOR_MUTED,
        )


# ---------------------------------------------------------------------------
# Axis styling helper
# ---------------------------------------------------------------------------

def style_axis_minimal(
    ax,
    *,
    show_yticks: bool = True,
    show_xticks: bool = True,
    orientation: str = "vertical_bar",
) -> None:
    """Apply minimal editorial axis styling to an Axes.

    Removes top/right spines (already global default), thins remaining spines,
    sets tick colors to muted gray. Use after creating a chart to ensure
    consistent visual weight across the report.

    orientation argument controls the gridline behavior:
      'vertical_bar' (default) — horizontal y-axis gridlines (good for comparing
        bar heights when bars run vertically)
      'horizontal_bar' — disables grid entirely (horizontal bars + horizontal
        gridlines = stripe-through-bar visual artifact)
      'horizontal_dot' — vertical x-axis gridlines only (for dumbbell/dot plots
        where rows are categorical brands and the x-axis is the data axis)
      'scatter' or 'plot' — light gridlines on both axes (helpful for
        reading scatter plots and line charts)
      'none' — no gridlines at all
    """
    for spine_name in ("top", "right"):
        ax.spines[spine_name].set_visible(False)
    for spine_name in ("bottom", "left"):
        ax.spines[spine_name].set_color(COLOR_GRID)
        ax.spines[spine_name].set_linewidth(0.5)

    if not show_xticks:
        ax.set_xticks([])
    if not show_yticks:
        ax.set_yticks([])

    # Grid behavior depends on chart orientation. We explicitly turn off ALL
    # grids first, then enable only what each orientation wants — otherwise
    # the global rcParams default (y-axis grid for vertical bars) leaks
    # through into orientations that should suppress it.
    ax.grid(False)
    if orientation == "horizontal_bar" or orientation == "none":
        pass  # All grids off — already done above
    elif orientation in ("scatter", "plot"):
        ax.grid(True, which="major", axis="both",
                color=COLOR_GRID_SUBTLE, linewidth=0.5, linestyle="-")
        ax.set_axisbelow(True)
    elif orientation == "horizontal_dot":
        # x-axis grid only — for dumbbell/dot plots where rows are categorical
        # (brands) and the data axis is horizontal. Vertical gridlines help
        # readers map dot positions to x-axis values; horizontal gridlines
        # would stripe through each row's data.
        ax.grid(True, which="major", axis="x",
                color=COLOR_GRID_SUBTLE, linewidth=0.5, linestyle="-")
        ax.set_axisbelow(True)
    else:  # 'vertical_bar' default — y-axis grid only
        ax.grid(True, which="major", axis="y",
                color=COLOR_GRID_SUBTLE, linewidth=0.5, linestyle="-")
        ax.set_axisbelow(True)


# ---------------------------------------------------------------------------
# Tier color lookup
# ---------------------------------------------------------------------------

def tier_color(tier: str) -> str:
    """Return the Third System tier color for a brand tier.

    tier: 'incumbent' | 'midtier' | 'challenger'
    Raises KeyError if the tier name is invalid — fail loudly rather than
    silently returning a default.
    """
    key = tier.lower().strip().replace("-", "").replace(" ", "")
    return TIER_COLORS[key]


# ---------------------------------------------------------------------------
# Output filename helper — enforces canonical naming convention
# ---------------------------------------------------------------------------

def canonical_chart_filename(pattern_id: str, column_span: str) -> str:
    """Build the canonical chart filename per brand spec.

    Format: chart_<pattern_id>_<col_span>col.pdf
    Example: canonical_chart_filename('p2', '6') -> 'chart_p2_6col.pdf'

    For special spans use the literal: 'spread' -> 'chart_p4_spread.pdf'
    """
    if column_span == "spread":
        return f"chart_{pattern_id}_spread.pdf"
    return f"chart_{pattern_id}_{column_span}col.pdf"


# ---------------------------------------------------------------------------
# Module-level summary (printable at import time for verification)
# ---------------------------------------------------------------------------

def print_summary() -> None:
    """Print a summary of loaded brand spec values. Useful for verification."""
    print(f"chart_style.py loaded from brand spec v{BRAND_SCHEMA_VERSION}")
    print(f"  Brand Indigo: {BRAND_INDIGO}")
    print(f"  Tier colors: incumbent={COLOR_INCUMBENT}, midtier={COLOR_MIDTIER}, challenger={COLOR_CHALLENGER}")
    print(f"  Grayscale: 10={BLACK_10} 20={BLACK_20} 40={BLACK_40} 60={BLACK_60} 80={BLACK_80} 100={BLACK_100}")
    print(f"  3-col inline figsize: {FIGSIZE_3COL_INLINE}")
    print(f"  6-col hero figsize: {FIGSIZE_6COL_HERO}")
    print(f"  Font: configured={CONFIGURED_FONT_FAMILY}, target={PRIMARY_FONT_FAMILY}")
    print(f"  DPI: print={DPI_PRINT}, screen_high={DPI_SCREEN_HIGH}, default={DPI_DEFAULT}")
    if _FONT_REGISTRATION_LOG:
        print(f"  Font registration log:")
        for line in _FONT_REGISTRATION_LOG:
            print(f"    - {line}")


if __name__ == "__main__":
    print_summary()
