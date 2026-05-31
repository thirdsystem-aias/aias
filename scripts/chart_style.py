"""
chart_style.py — Third System™ Chart Standard
AIAS™ Measurement Program

Reusable module for all AIAS chart builders. Codifies the Third System
brand data-viz system from third_system_brand.json so individual phase
chart scripts don't need to reinvent layout, colors, or positioning.

Usage:
    from chart_style import setup, add_header, add_footer, PALETTE, FIGSIZE

    setup()  # registers Akkurat Pro, sets rcParams
    fig, ax = plt.subplots(figsize=FIGSIZE["hero"])
    # ... build chart ...
    add_header(fig, "Title", "Subtitle", "Description")
    add_footer(fig, verdict="H_Something CONFIRMED — details.", phase="v0.24")
    fig.savefig(out, **SAVEFIG_PARAMS)

Source: third_system_brand.json schema v1.2
"""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# ============================================================
# 1. PALETTE — Third System data-viz families
# ============================================================

PALETTE = {
    # Indigo family (primary)
    "indigo":       "#37237B",   # indigo.accent — primary brand color
    "indigo_sec":   "#534F9E",   # indigo.secondary
    "indigo_t1":    "#6A6AB1",   # indigo.tertiary_1
    "indigo_t2":    "#908EC5",   # indigo.tertiary_2
    "indigo_t3":    "#BBB9DD",   # indigo.tertiary_3

    # Warm family (diverging pair with indigo)
    "warm":         "#F36C35",   # warm.accent
    "warm_sec":     "#712300",   # warm.secondary
    "warm_t1":      "#BD4718",   # warm.tertiary_1
    "warm_t2":      "#F79668",   # warm.tertiary_2
    "warm_t3":      "#FBBD9C",   # warm.tertiary_3

    # Teal family
    "teal":         "#08C3A5",   # teal.accent
    "teal_sec":     "#06423D",   # teal.secondary
    "teal_t1":      "#0A6B5B",   # teal.tertiary_1
    "teal_t2":      "#06927C",   # teal.tertiary_2
    "teal_t3":      "#99E4D7",   # teal.tertiary_3

    # Blue family
    "blue":         "#007EAE",   # blue.accent
    "blue_sec":     "#002B5F",   # blue.secondary
    "blue_t1":      "#005E92",   # blue.tertiary_1
    "blue_t2":      "#4F99C1",   # blue.tertiary_2
    "blue_t3":      "#A1C3DA",   # blue.tertiary_3

    # Green family
    "green":        "#A4C032",   # green.accent
    "green_sec":    "#2C3B0D",   # green.secondary
    "green_t1":     "#586A2E",   # green.tertiary_1
    "green_t2":     "#7B9234",   # green.tertiary_2
    "green_t3":     "#C5D582",   # green.tertiary_3

    # Magenta family
    "magenta":      "#C40067",   # magenta.accent
    "magenta_sec":  "#6A035C",   # magenta.secondary

    # Yellow family
    "yellow":       "#FFAC17",   # yellow.accent
    "yellow_sec":   "#4B2514",   # yellow.secondary

    # Neutrals
    "black":        "#1A1A1A",
    "gray":         "#888888",
    "gray_light":   "#CCCCCC",
    "white":        "#FFFFFF",
    "paper":        "#FAF7F2",   # off-white paper
}

# Shorthand aliases
INDIGO = PALETTE["indigo"]
WARM   = PALETTE["warm"]
TEAL   = PALETTE["teal"]
BLACK  = PALETTE["black"]
GRAY   = PALETTE["gray"]

# ============================================================
# 2. FIGSIZE — from brand chart_sizing_specifications
# ============================================================

FIGSIZE = {
    "1col":         (1.13, 1.13),
    "2col":         (2.41, 2.1),
    "3col":         (3.68, 2.85),
    "4col":         (4.95, 3.71),
    "hero":         (7.5, 5.0),     # 6-column hero (default)
    "hero_tall":    (7.5, 6.5),     # 6-column hero tall (15+ brands)
    "hero_short":   (7.5, 3.5),     # 6-column hero short (few categories)
    "spread":       (7.5, 4.5),     # two-panel spread
}

# ============================================================
# 3. FONT SIZE SCALING — by column span
# ============================================================

FONT_SIZES = {
    # 6-column hero (default for AIAS phase charts)
    "title":        13.0,
    "subtitle":     10.0,
    "description":  8.0,
    "axis_label":   9.0,
    "axis_tick":    8.5,
    "data_label":   8.5,
    "legend":       8.5,
    "annotation":   8.0,
    "source":       7.0,
    "verdict":      7.0,
}

# ============================================================
# 4. SAVEFIG PARAMS — standard output settings
# ============================================================

SAVEFIG_PARAMS = {
    "bbox_inches": "tight",
    "pad_inches":  0.15,
    "dpi":         300,
}

# ============================================================
# 5. FONT REGISTRATION
# ============================================================

def setup():
    """
    Register Akkurat Pro and set matplotlib rcParams.
    Call once at module import or script start.
    """
    font_dirs = [
        Path.home() / ".fonts" / "Akkurat",
        Path.home() / "Library" / "Fonts",
    ]
    for d in font_dirs:
        if d.exists():
            for f in list(d.glob("*.otf")) + list(d.glob("*.ttf")):
                fm.fontManager.addfont(str(f))

    plt.rcParams.update({
        "font.family":          ["Akkurat Pro", "sans-serif"],
        "axes.unicode_minus":   False,
        "font.size":            9,
        "axes.titlesize":       11,
        "axes.titleweight":     "bold",
        "axes.labelsize":       9,
        "axes.spines.top":      False,
        "axes.spines.right":    False,
        "axes.linewidth":       0.6,
        "xtick.major.width":    0.6,
        "ytick.major.width":    0.6,
        "xtick.major.size":     0,
        "ytick.major.size":     0,
        "legend.fontsize":      8,
        "legend.frameon":       True,
        "legend.framealpha":    0.9,
    })


# ============================================================
# 6. HEADER — title + subtitle + description (left-aligned)
# ============================================================

# Left margin for all text chrome
LEFT_X = 0.04

def _compute_positions(fig):
    """
    Compute title/subtitle/description/source y-positions from figure height.
    Derived from brand JSON title_subtitle_source_positioning formulas.
    """
    h = fig.get_figheight()
    title_y       = 1.0 - (0.10 / h)
    subtitle_y    = 1.0 - (0.35 / h)
    description_y = 1.0 - (0.55 / h)
    verdict_y     = 0.0 + (0.25 / h)
    source_y      = 0.0 + (0.10 / h)
    return title_y, subtitle_y, description_y, verdict_y, source_y


def add_header(fig, title, subtitle, description=""):
    """
    Left-aligned three-line header block.
    Title:       bold, FONT_SIZES["title"], black
    Subtitle:    regular, FONT_SIZES["subtitle"], gray
    Description: italic, FONT_SIZES["description"], gray (optional)
    """
    title_y, subtitle_y, description_y, _, _ = _compute_positions(fig)

    fig.text(LEFT_X, title_y, title,
             fontsize=FONT_SIZES["title"], fontweight="bold",
             color=BLACK, ha="left", va="top")
    fig.text(LEFT_X, subtitle_y, subtitle,
             fontsize=FONT_SIZES["subtitle"], color=GRAY,
             ha="left", va="top")
    if description:
        fig.text(LEFT_X, description_y, description,
                 fontsize=FONT_SIZES["description"], color=GRAY,
                 fontstyle="italic", ha="left", va="top")


# ============================================================
# 7. FOOTER — verdict + source (left-aligned)
# ============================================================

def add_footer(fig, verdict="", phase="v0.24",
               protocol="v1.6", entity="Third System\u2122"):
    """
    Bottom block: verdict line (indigo italic) + source line (gray).
    Source format: "Source: AIAS™ <phase> | Protocol <protocol> | <entity>"
    """
    _, _, _, verdict_y, source_y = _compute_positions(fig)

    source_text = (
        f"Source: AIAS\u2122 {phase} | Protocol {protocol} | {entity}"
    )

    if verdict:
        fig.text(LEFT_X, verdict_y, verdict,
                 fontsize=FONT_SIZES["verdict"], color=INDIGO,
                 fontstyle="italic", ha="left", va="bottom")

    fig.text(LEFT_X, source_y, source_text,
             fontsize=FONT_SIZES["source"], color=GRAY,
             ha="left", va="bottom")


# ============================================================
# 8. SUBPLOTS_ADJUST — standard margin reserves
# ============================================================

MARGINS = {
    "single":  {"top": 0.82, "bottom": 0.18, "left": 0.10, "right": 0.95},
    "two_panel": {"top": 0.82, "bottom": 0.20, "left": 0.07, "right": 0.97,
                  "wspace": 0.18},
    "tall_legend": {"top": 0.82, "bottom": 0.22, "left": 0.10, "right": 0.95},
}


# ============================================================
# 9. QUALITATIVE SCHEMES — for cell-coloring consistency
# ============================================================

def cell_colors(cells=("A", "B", "C", "D")):
    """
    Return a dict mapping cell labels to qualitative colors.
    Default 4-cell scheme uses indigo/warm/teal/gray.
    """
    scheme = [INDIGO, WARM, TEAL, PALETTE["gray_light"]]
    return {c: scheme[i] for i, c in enumerate(cells)}


def diverging_pair():
    """
    Return the canonical Indigo ↔ Warm diverging pair.
    Use for R_cat vs R_cult, before/after, positive/negative.
    """
    return INDIGO, WARM
