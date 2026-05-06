#!/usr/bin/env python3
"""
v0.8 Knives chart generator.

Produces six PDF charts at locked figsize for the v0.8 report. Outputs go to
<reports>/output/ and are picked up by build_report_v08.py via the
_slot_lookup table.

Charts:
  chart_v08_leaderboard_6col.pdf            7.50 \u00d7 7.50  (6_col_hero_xl)     knife leaderboard, lineage colored
  chart_v08_f1_lineage_aggregates_6col.pdf  7.50 \u00d7 3.50  (6_col_short)       lineage aggregates v1.0 vs v1.2
  chart_v08_f2_authorities_6col.pdf         7.50 \u00d7 3.75  (6_col_hero_short)  100% English-language authorities
  chart_v08_f3_within_lineage_6col.pdf      7.50 \u00d7 4.50  (6_col_hero)        within-Japanese 5x ratio + G\u00fcde 0%
  chart_v08_f4_per_cep_6col.pdf             7.50 \u00d7 3.75  (6_col_hero_short)  per-CEP \u00d7 lineage matrix
  chart_v08_f5_freshness_4col.pdf           3.68 \u00d7 2.85  (3_col_inline)      within-lab generational gaps

CRITICAL: bbox=None and pad_inches=0 on savefig so native figsize is preserved
exactly. The build_report_v08.py overlay relies on chart PDFs being at locked
dimensions; bbox_inches='tight' would invalidate the slot reservation.

Color palette pulled from third_system_brand.json. Falls back to hardcoded
constants if the JSON is missing.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Patch

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
AIAS_ROOT = SCRIPT_DIR.parent
BRAND_JSON = AIAS_ROOT / "brand" / "third_system_brand.json"
OUTPUT_DIR = SCRIPT_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Brand palette (loaded from JSON; fallback to constants if not found)
# ---------------------------------------------------------------------------

_FALLBACK_PALETTE = {
    "indigo": "#37237B",
    "indigo_50": "#9B91BD",
    "indigo_25": "#CDC8DE",
    "copper": "#F36C35",
    "soft_black": "#231F20",
    "paper": "#FAF7F2",
    "black_20": "#CCCCCC",
    "black_40": "#999999",
    "black_60": "#666666",
}


def load_palette() -> dict:
    if not BRAND_JSON.exists():
        print(f"[charts] brand JSON not found at {BRAND_JSON}; using fallback palette",
              file=sys.stderr)
        return _FALLBACK_PALETTE

    with open(BRAND_JSON) as f:
        brand = json.load(f)

    palette = dict(_FALLBACK_PALETTE)
    pb = brand.get("palette", {}).get("primary_brand", {})
    if "indigo" in pb:
        palette["indigo"] = pb["indigo"].get("hex", palette["indigo"])

    for block_name in ("brand_supporting", "data_viz_palette_sp_global"):
        block = brand.get("palette", {}).get(block_name, {})
        if isinstance(block, dict):
            def harvest(d):
                for k, v in d.items():
                    if isinstance(v, dict) and "hex" in v:
                        kl = k.lower()
                        if "copper" in kl:
                            palette["copper"] = v["hex"]
                        elif "soft" in kl and "black" in kl:
                            palette["soft_black"] = v["hex"]
                        elif kl == "paper" or "off-white" in kl or "paper" in kl:
                            palette["paper"] = v["hex"]
                    elif isinstance(v, dict):
                        harvest(v)
            harvest(block)

    return palette


PALETTE = load_palette()
INDIGO = PALETTE["indigo"]
INDIGO_50 = PALETTE["indigo_50"]
INDIGO_25 = PALETTE["indigo_25"]
COPPER = PALETTE["copper"]
SOFT_BLACK = PALETTE["soft_black"]
GRAY_20 = PALETTE["black_20"]
GRAY_40 = PALETTE["black_40"]
GRAY_60 = PALETTE["black_60"]


# ---------------------------------------------------------------------------
# Lineage color encoding (v0.8 specific)
# ---------------------------------------------------------------------------
#
# Japanese mass-market English-distributed: INDIGO (primary brand color)
# Japanese boundary / traditional:          INDIGO_50 (lighter primary)
# German mass-market English-distributed:   COPPER (highlight color)
# German boundary / limited-English:        a lighter copper (we mix here)
# American:                                 GRAY_60 (collapsed lineage)
# Hybrid (Miyabi, Japanese-branded German-owned): INDIGO_25 (very light primary)
# Shared (Victorinox, Mercer, Dexter):      GRAY_40 (neutral)

# Light copper for German boundary brands; computed inline from COPPER if
# no separate token exists. We use a pre-mixed hex that reads as ~50%
# saturation of the brand's copper.
COPPER_50 = "#F8B69A"   # light copper - 50% mixed with paper

LINEAGE_COLOR = {
    "japanese_mm":         INDIGO,
    "japanese_boundary":   INDIGO_50,
    "german_mm":           COPPER,
    "german_boundary":     COPPER_50,
    "american":            GRAY_60,
    "hybrid":              INDIGO_25,
    "shared":              GRAY_40,
}


# ---------------------------------------------------------------------------
# Font registration
# ---------------------------------------------------------------------------

def register_fonts() -> str:
    """Find Akkurat Pro on the host. Returns 'Akkurat Pro' if found,
    else 'Inter' if available, else DejaVu Sans with a warning."""
    candidate_dirs = [
        Path.home() / "Library" / "Fonts",
        Path("/Library/Fonts"),
        Path.home() / ".fonts" / "Akkurat",
        Path.home() / ".fonts",
        Path("/usr/share/fonts"),
    ]

    akkurat_files = []
    for d in candidate_dirs:
        if not d.exists():
            continue
        for ext in ("*.otf", "*.ttf", "*.OTF", "*.TTF"):
            for p in d.rglob(ext):
                if "akkurat" in p.name.lower():
                    akkurat_files.append(p)

    if akkurat_files:
        for fp in akkurat_files:
            try:
                font_manager.fontManager.addfont(str(fp))
            except Exception:
                pass
        for candidate in ("Akkurat Pro", "Akkurat", "AkkuratPro"):
            try:
                font_manager.findfont(candidate, fallback_to_default=False)
                print(f"[charts] using {candidate} ({len(akkurat_files)} files registered)")
                return candidate
            except Exception:
                continue

    try:
        font_manager.findfont("Inter", fallback_to_default=False)
        print("[charts] Akkurat Pro not found; using Inter")
        return "Inter"
    except Exception:
        pass

    print("[charts] WARNING: Akkurat Pro and Inter both unavailable. Falling back to DejaVu Sans.",
          file=sys.stderr)
    return "DejaVu Sans"


FONT_FAMILY = register_fonts()

plt.rcParams.update({
    "font.family": FONT_FAMILY,
    "font.size": 9,
    "axes.titlesize": 11,
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    # Text/axis colors switched from INDIGO to SOFT_BLACK so titles,
    # axis labels, tick labels, and any unspecified text default to a
    # dark-text convention. INDIGO is now reserved for data fills (bars,
    # dots) and data labels (per-bar value numbers); COPPER for accents.
    "axes.edgecolor": SOFT_BLACK,
    "axes.labelcolor": SOFT_BLACK,
    "axes.titlecolor": SOFT_BLACK,
    "xtick.color": SOFT_BLACK,
    "ytick.color": SOFT_BLACK,
    "text.color": SOFT_BLACK,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 0.6,
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
    "savefig.facecolor": "none",
    "axes.facecolor": "none",
    "figure.facecolor": "none",

    # See v07 builder for rationale: Type 3 outlines, no shared font ref
    # to prevent collision with ReportLab base PDF in pypdf overlay.
    "pdf.fonttype": 3,
    "ps.fonttype": 3,
    "pdf.use14corefonts": False,
})

SOURCE_LINE = "Source: Third System AI Presence Index v0.8  \u00b7  n=288 measurements (6 prompts \u00d7 6 models \u00d7 8 runs)  \u00b7  6 May 2026"


def save(fig, name: str):
    """Save at native figsize, no padding adjustment, so the slot reservation
    in build_report_v08.py matches exactly."""
    out = OUTPUT_DIR / name
    fig.savefig(str(out), format="pdf", bbox_inches=None, pad_inches=0,
                transparent=True)
    plt.close(fig)
    print(f"[charts] wrote {name}  ({out.stat().st_size / 1024:.1f} KB)")


# ===========================================================================
# Chart 0 \u2014 Knife brand leaderboard (6_col_hero_xl: 7.50 \u00d7 7.50)
#
# 22 brands ordered by Presence, colored by lineage. G\u00fcde at 0% included
# explicitly as the H5 control \u2014 the German boundary parallel that lets the
# leaderboard tell the within-lineage story directly.
# ===========================================================================

LEADERBOARD = [
    # (brand, presence_pct, lineage_key)
    ("W\u00fcsthof",         68.4, "german_mm"),
    ("Mac",                  66.3, "japanese_mm"),
    ("Victorinox",           63.9, "shared"),
    ("Shun",                 63.2, "japanese_mm"),
    ("Henckels",             55.6, "german_mm"),
    ("Tojiro",               53.8, "japanese_mm"),
    ("Global",               47.2, "japanese_mm"),
    ("Miyabi",               31.6, "hybrid"),
    ("Misono",               26.0, "japanese_mm"),
    ("Masamoto",             18.1, "japanese_boundary"),
    ("Takamura",             16.7, "japanese_boundary"),
    ("Mercer",               12.5, "shared"),
    ("Messermeister",        11.5, "german_mm"),
    ("Sakai Takayuki",       10.8, "japanese_boundary"),
    ("Konosuke",              9.7, "japanese_boundary"),
    ("Korin",                 8.3, "japanese_boundary"),
    ("Nigara Hamono",         5.9, "japanese_boundary"),
    ("Yu Kurosaki",           5.2, "japanese_boundary"),
    ("Yoshihiro",             3.8, "japanese_boundary"),
    ("Takeda",                3.5, "japanese_boundary"),
    ("Yoshikane",             3.5, "japanese_boundary"),
    ("G\u00fcde",             0.0, "german_boundary"),  # H5 control \u2014 must be visible
]


def chart_leaderboard():
    fig = plt.figure(figsize=(7.50, 7.50))
    # Axes y=0.15, height=0.74 — gives the bottom region (0..0.15)
    # enough room for x-axis tick labels (~0.12-0.14) AND the lineage
    # legend (~0.05-0.085) without collision. Top edge stays at 0.89
    # so title/subtitle layout is unchanged.
    ax = fig.add_axes([0.27, 0.15, 0.55, 0.74])

    names = [r[0] for r in LEADERBOARD]
    values = [r[1] for r in LEADERBOARD]
    lineages = [r[2] for r in LEADERBOARD]

    y = list(range(len(names)))[::-1]
    colors = [LINEAGE_COLOR[lk] for lk in lineages]

    ax.barh(y, values, color=colors, height=0.7, edgecolor="none")

    # Reference line at H1's calibration anchor (Wusthof + Henckels mean = 62%)
    ax.axvline(62, color=GRAY_60, linestyle=(0, (2, 3)), linewidth=0.8, zorder=0)
    ax.text(62, len(names) + 0.2, "W\u00fcsthof+Henckels mean (H5 anchor)",
            color=GRAY_60, fontsize=7.5, ha="center", style="italic")

    # Brand names on left
    for i, (n, lk) in enumerate(zip(names, lineages)):
        # Boldface mass-market and key controls; light for boundary tier
        weight = "bold" if lk in ("japanese_mm", "german_mm", "hybrid") else "normal"
        ax.text(-1, y[i], n, ha="right", va="center",
                fontsize=8.5, fontweight=weight, color=SOFT_BLACK)

    # Value labels on right of each bar
    for i, (v, lk) in enumerate(zip(values, lineages)):
        weight = "bold" if lk in ("japanese_mm", "german_mm") else "normal"
        if v > 0:
            ax.text(v + 1, y[i], f"{v:.1f}", ha="left", va="center",
                    fontsize=8, fontweight=weight, color=INDIGO)
        else:
            # G\u00fcde marker
            ax.scatter([0.4], [y[i]], s=14, color=COPPER, zorder=5)
            ax.text(2.5, y[i], "0.0", ha="left", va="center",
                    fontsize=8, fontweight="bold", color=COPPER)

    # Annotations on key brands.
    # Placed at x=30 (inside axes, well past the small bars they annotate
    # at 0.0, 16.7, 18.1) so they don't get clipped at the right edge.
    # Gray rather than indigo so they read as supporting context, not data.
    annotations = {
        "Masamoto": "outlier \u2014 US English distribution",
        "Takamura": "outlier \u2014 chef-endorsed in EN",
        "G\u00fcde":  "H5 control \u2014 0/288 mentions",
    }
    for i, n in enumerate(names):
        if n in annotations:
            ax.text(30, y[i], annotations[n], ha="left", va="center",
                    fontsize=7.5, style="italic", color=GRAY_60)

    ax.set_xlim(0, 100)
    ax.set_ylim(-0.6, len(names) - 0.4)
    ax.set_yticks([])
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"])
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color(SOFT_BLACK)
    ax.tick_params(axis="x", which="both", length=2)

    # Title and subtitle
    fig.text(0.05, 0.965, "AI Presence \u2014 Premium Kitchen Knives",
             fontsize=14, fontweight="bold", color=SOFT_BLACK, ha="left")
    fig.text(0.05, 0.935,
             "22 of 27 brands ordered by Presence, colored by lineage. G\u00fcde shown as H5 control.",
             fontsize=9, color=SOFT_BLACK, ha="left")

    # Lineage legend (figure-level, centered just above source line).
    # Previously placed at axes-relative bbox (1.0, -0.13) which rendered
    # below the figure boundary and got clipped.
    legend_elems = [
        Patch(facecolor=INDIGO,    label="Japanese (English-marketed)"),
        Patch(facecolor=INDIGO_50, label="Japanese (boundary)"),
        Patch(facecolor=COPPER,    label="German (English-marketed)"),
        Patch(facecolor=COPPER_50, label="German (boundary)"),
        Patch(facecolor=INDIGO_25, label="Hybrid (JP-branded, DE-owned)"),
        Patch(facecolor=GRAY_40,   label="Shared category"),
    ]
    fig.legend(handles=legend_elems, loc="lower center",
               bbox_to_anchor=(0.5, 0.055), ncol=3, frameon=False,
               fontsize=7, handlelength=1.2, handleheight=0.9,
               columnspacing=1.0)

    fig.text(0.05, 0.012, SOURCE_LINE, fontsize=7,
             style="italic", color=SOFT_BLACK, ha="left")

    save(fig, "chart_v08_leaderboard_6col.pdf")


# ===========================================================================
# Chart 1 (Finding 1) \u2014 Lineage aggregates (6_col_short: 7.50 \u00d7 3.50)
#
# Five vertical bars showing aggregate lineage Presence with the v1.0 vs v1.2
# Japanese registry split visible. The H1 disconfirmation lives in the gap
# between the two Japanese bars.
# ===========================================================================

LINEAGE_AGGREGATES = [
    # (label, value, color_key, sublabel)
    ("Japanese\nv1.0 locked\n(8 brands)",       36.2, "japanese_mm",       "registry locked"),
    ("Japanese\nv1.2 published\n(14 brands)",   18.5, "japanese_boundary", "post-revision"),
    ("German\n(5 brands)",                      27.3, "german_mm",         "stable across revisions"),
    ("American\n(5 brands)",                     0.6, "american",          "comparator collapsed"),
    ("Miyabi\nexploratory",                     31.6, "hybrid",            "n=1, JP-branded DE-owned"),
]


def chart_f1_lineage_aggregates():
    fig = plt.figure(figsize=(7.50, 3.50))
    # Increased bottom margin (0.20 \u2192 0.18) since sublabels removed; main
    # axes fits comfortably with x-tick labels only.
    ax = fig.add_axes([0.08, 0.18, 0.86, 0.55])

    labels = [r[0] for r in LINEAGE_AGGREGATES]
    values = [r[1] for r in LINEAGE_AGGREGATES]
    colors = [LINEAGE_COLOR[r[2]] for r in LINEAGE_AGGREGATES]

    x = list(range(len(labels)))
    ax.bar(x, values, color=colors, width=0.65, edgecolor="none")

    # Value labels above bars
    for i, v in enumerate(values):
        ax.text(i, v + 1.5, f"{v:.1f}%", ha="center", va="bottom",
                fontsize=11, fontweight="bold", color=INDIGO)

    # H1 threshold reference line at German aggregate
    ax.axhline(27.3, color=COPPER, linestyle=(0, (2, 3)), linewidth=0.8, zorder=0)
    ax.text(4.5, 28.5, "DE 27.3% \u2014 H1 anchor",
            ha="right", va="bottom", fontsize=7.5, style="italic", color=COPPER)

    # Registry-expansion callout: a simple bracket above bars 0\u20131 with
    # gap label. Bracket sits above the taller bar (36.2%) so it doesn't
    # collide with bar fills or value labels.
    bracket_y = 42
    ax.plot([0, 1], [bracket_y, bracket_y], color=GRAY_60, linewidth=0.8)
    ax.plot([0, 0], [38.5, bracket_y], color=GRAY_60, linewidth=0.8)
    ax.plot([1, 1], [21.0, bracket_y], color=GRAY_60, linewidth=0.8)
    ax.text(0.5, bracket_y + 0.5, "registry expansion: \u201317.7pp",
            ha="center", va="bottom", fontsize=7.5, style="italic", color=GRAY_60)

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8.5)
    ax.set_ylim(0, 48)
    ax.set_yticks([0, 10, 20, 30, 40])
    ax.set_yticklabels(["0%", "10%", "20%", "30%", "40%"], fontsize=8)
    ax.spines["bottom"].set_color(SOFT_BLACK)
    ax.tick_params(axis="x", length=0, pad=2)
    ax.tick_params(axis="y", length=2)

    # Title + subtitle
    fig.text(0.05, 0.93,
             "H1 disconfirmation: Japanese aggregate depends on registry",
             fontsize=12, fontweight="bold", color=SOFT_BLACK, ha="left")
    fig.text(0.05, 0.86,
             "At locked v1.0, JP aggregate is higher than DE. At expanded v1.2, JP falls below DE by 8.8pp.",
             fontsize=8.5, color=SOFT_BLACK, ha="left")

    fig.text(0.05, 0.025, SOURCE_LINE, fontsize=7,
             style="italic", color=SOFT_BLACK, ha="left")

    save(fig, "chart_v08_f1_lineage_aggregates_6col.pdf")


# ===========================================================================
# Chart 2 (Finding 2) \u2014 100% English authority infrastructure
# (6_col_hero_short: 7.50 \u00d7 3.75)
#
# Top 15 named authorities (publications + retailers + communities), with
# 100% English callout. The hero number is "262 / 262 \u00b7 100%".
# ===========================================================================

AUTHORITIES = [
    # (name, n_mentions, type)  \u2014 type unused in chart but documented
    ("Sur La Table",            27, "retailer"),
    ("Serious Eats",            22, "publication"),
    ("Williams Sonoma",         22, "retailer"),
    ("Wirecutter",              21, "publication"),
    ("Amazon",                  21, "retailer"),
    ("America's Test Kitchen",  13, "publication"),
    ("Japanese Knife Imports",  13, "retailer"),
    ("Knifewear",                8, "retailer"),
    ("Reddit",                   7, "community"),
    ("BladeHQ",                  7, "retailer"),
    ("Cook's Illustrated",       6, "publication"),
    ("Burrfection",              6, "community"),
    ("KnifeCenter",              6, "retailer"),
    ("ChefKnivestoGo",           5, "retailer"),
    ("Blade HQ",                 5, "retailer"),
]


def chart_f2_authorities():
    fig = plt.figure(figsize=(7.50, 3.75))

    # Hero stat block — aligned with title at figure x=0.04 (the title's
    # left edge). All text in this panel is left-aligned so the "1" of
    # 100% lines up vertically with the "T" of the title.
    hero_ax = fig.add_axes([0.04, 0.18, 0.18, 0.62])
    hero_ax.axis("off")

    # Hero number in COPPER for accent contrast against the indigo bars.
    # All text left-aligned at hero_ax x=0.0 so the leftmost glyph (the
    # "1" of 100%) sits at figure x=0.04, vertically aligning with the
    # title's left edge.
    hero_ax.text(0.0, 0.68, "100%",
                 ha="left", va="center", fontsize=42,
                 fontweight="bold", color=COPPER,
                 transform=hero_ax.transAxes)
    hero_ax.text(0.0, 0.46, "of authorities are",
                 ha="left", va="center", fontsize=10,
                 color=SOFT_BLACK, transform=hero_ax.transAxes)
    hero_ax.text(0.0, 0.38, "English-language",
                 ha="left", va="center", fontsize=10,
                 fontweight="bold", color=SOFT_BLACK,
                 transform=hero_ax.transAxes)
    hero_ax.text(0.0, 0.30, "262 of 262 mentions",
                 ha="left", va="center", fontsize=8,
                 style="italic", color=GRAY_60,
                 transform=hero_ax.transAxes)

    # Authority bar chart — pulled closer to the hero (x=0.42 vs prior
    # 0.55) to compress the dead space in the middle of the figure.
    # Authority labels (longest: "America's Test Kitchen") are rendered
    # at fontsize 7.5 so they fit in the narrower left-margin band.
    bar_ax = fig.add_axes([0.42, 0.15, 0.50, 0.65])

    names = [r[0] for r in AUTHORITIES]
    counts = [r[1] for r in AUTHORITIES]
    types = [r[2] for r in AUTHORITIES]

    type_colors = {
        "publication": INDIGO,
        "retailer":    INDIGO_50,
        "community":   INDIGO_25,
    }
    colors = [type_colors[t] for t in types]

    y = list(range(len(names)))[::-1]
    bar_ax.barh(y, counts, color=colors, height=0.7, edgecolor="none")

    # Names on left (fontsize 7.5 to fit the narrower left margin)
    for i, n in enumerate(names):
        bar_ax.text(-0.6, y[i], n, ha="right", va="center",
                    fontsize=7.5, color=SOFT_BLACK)

    # Counts on right
    for i, c in enumerate(counts):
        bar_ax.text(c + 0.4, y[i], str(c), ha="left", va="center",
                    fontsize=7.5, fontweight="bold", color=INDIGO)

    bar_ax.set_xlim(0, 32)
    bar_ax.set_ylim(-0.6, len(names) - 0.4)
    bar_ax.set_yticks([])
    bar_ax.set_xticks([0, 10, 20, 30])
    bar_ax.set_xticklabels(["0", "10", "20", "30"], fontsize=7)
    bar_ax.spines["left"].set_visible(False)
    bar_ax.spines["bottom"].set_color(SOFT_BLACK)
    bar_ax.tick_params(axis="x", length=2)

    # Legend for the bar chart's color encoding
    legend_elems = [
        Patch(facecolor=INDIGO,    label="Publication"),
        Patch(facecolor=INDIGO_50, label="Retailer"),
        Patch(facecolor=INDIGO_25, label="Community"),
    ]
    bar_ax.legend(handles=legend_elems, loc="lower right",
                  bbox_to_anchor=(1.0, -0.20), ncol=3, frameon=False,
                  fontsize=7, handlelength=1.2, handleheight=0.9,
                  columnspacing=1.0)

    # Thin vertical separator between hero block and bar chart.
    # Positioned at figure x=0.25 — past the hero panel right edge
    # (0.22) and before the longest authority label
    # ("America's Test Kitchen", left edge ~0.28). Spans most of the
    # chart height to echo the bar_ax y-extent.
    fig.add_artist(plt.Line2D([0.25, 0.25], [0.18, 0.80],
                              color=GRAY_40, linewidth=0.5,
                              transform=fig.transFigure))

    # Title + subtitle (top-left, spanning both panels)
    fig.text(0.04, 0.93,
             "The discourse infrastructure is exclusively English",
             fontsize=12, fontweight="bold", color=SOFT_BLACK, ha="left")
    fig.text(0.04, 0.87,
             "Top 15 named authorities. Even \u201cJapanese Knife Imports\u201d is a US-based English-language retailer.",
             fontsize=8, color=SOFT_BLACK, ha="left")

    fig.text(0.04, 0.025, SOURCE_LINE, fontsize=7,
             style="italic", color=SOFT_BLACK, ha="left")

    save(fig, "chart_v08_f2_authorities_6col.pdf")


# ===========================================================================
# Chart 3 (Finding 3) \u2014 Within-lineage variance (6_col_hero: 7.50 \u00d7 4.50)
#
# Two-panel chart showing the marketing-language-coverage mechanism operating
# within each major lineage. Top: within-Japanese 5x ratio (mass-market vs
# traditional, with Masamoto/Takamura outliers visible). Bottom: within-German
# parallel (W\u00fcsthof+Henckels mean vs G\u00fcde 0%).
# ===========================================================================

WITHIN_JAPANESE_GROUPS = [
    # (group_label, mean, brand_dots: list of (brand, value))
    ("Mass-market\n(Shun + Global)",
     55.2,
     [("Shun", 63.2), ("Global", 47.2)]),
    ("Traditional / boundary\nv1.0 locked (3 brands)",
     10.9,
     [("Masamoto", 18.1), ("Sakai Takayuki", 10.8), ("Yoshihiro", 3.8)]),
    ("Traditional / boundary\nv1.2 expanded (14 brands)",
     6.8,
     [("Masamoto", 18.1), ("Takamura", 16.7), ("Sakai Takayuki", 10.8),
      ("Yoshihiro", 3.8), ("Yoshikane", 3.5)]),  # representative dots
]

WITHIN_GERMAN_GROUPS = [
    ("Mass-market\n(W\u00fcsthof + Henckels)",
     62.0,
     [("W\u00fcsthof", 68.4), ("Henckels", 55.6)]),
    ("Boundary\n(G\u00fcde, H5 control)",
     0.0,
     [("G\u00fcde", 0.0)]),
]


def chart_f3_within_lineage():
    fig = plt.figure(figsize=(7.50, 4.50))

    # Two panels stacked. Slightly more vertical room per panel and bigger
    # gap between them so the group titles + H3/H5 subtitles have clear
    # space above their respective panels.
    top_ax    = fig.add_axes([0.21, 0.50, 0.65, 0.26])
    bottom_ax = fig.add_axes([0.21, 0.15, 0.65, 0.18])

    def panel(ax, groups, lineage_label):
        labels = [g[0] for g in groups]
        means  = [g[1] for g in groups]
        dots   = [g[2] for g in groups]

        y = list(range(len(groups)))[::-1]
        h = 0.40

        # Mean bars
        if "German" in lineage_label:
            bar_colors = [COPPER if "Mass-market" in lab else COPPER_50
                          for lab in labels]
        else:
            bar_colors = [INDIGO if "Mass-market" in lab else INDIGO_50
                          for lab in labels]
        ax.barh(y, means, color=bar_colors, height=h, edgecolor="none",
                alpha=0.55)

        # Mean value labels: fixed position past the longest bar so they
        # never collide with dots or annotations on top of bars.
        # Top panel max is 55.2 so we put labels at x=68; bottom panel max
        # is 62 so we put labels at x=72.
        label_x = 72 if "German" in lineage_label else 68
        for i, m in enumerate(means):
            if m > 0:
                ax.text(label_x, y[i], f"{m:.1f}% mean",
                        ha="left", va="center", fontsize=9.5,
                        fontweight="bold", color=INDIGO)
            else:
                ax.text(label_x, y[i],
                        "0.0% mean \u2014 zero of 288",
                        ha="left", va="center", fontsize=9,
                        fontweight="bold", color=COPPER)

        # Brand dots overlaid at smaller size + below bar centerline so
        # they don't visually merge with the bar fill.
        for i, brand_list in enumerate(dots):
            for brand, val in brand_list:
                ax.scatter([val], [y[i]], s=18, color=INDIGO,
                           edgecolor="white", linewidth=0.7, zorder=4)

        # Outlier annotation strategy: only label the highest-value outlier
        # per row, alternating above/below to avoid collisions when two
        # outliers fall close together.
        # v1.0 row (3 brands): label Masamoto above
        # v1.2 row (5+ brands): label Takamura above and Masamoto below,
        #   to separate the two outliers vertically
        for i, brand_list in enumerate(dots):
            row_label = labels[i]
            for brand, val in brand_list:
                if brand == "Masamoto" and "v1.0" in row_label:
                    ax.text(val, y[i] + 0.30, "Masamoto",
                            ha="center", va="bottom", fontsize=6.5,
                            color=GRAY_60, style="italic")
                elif brand == "Takamura" and "v1.2" in row_label:
                    ax.text(val, y[i] + 0.30, "Takamura",
                            ha="center", va="bottom", fontsize=6.5,
                            color=GRAY_60, style="italic")
                elif brand == "Masamoto" and "v1.2" in row_label:
                    ax.text(val, y[i] - 0.30, "Masamoto",
                            ha="center", va="top", fontsize=6.5,
                            color=GRAY_60, style="italic")

        # Group labels on left
        for i, lab in enumerate(labels):
            ax.text(-2, y[i], lab, ha="right", va="center",
                    fontsize=8, color=SOFT_BLACK)

        ax.set_xlim(0, 100)
        ax.set_ylim(-0.6, len(groups) - 0.4)
        ax.set_yticks([])
        ax.set_xticks([0, 25, 50, 75, 100])
        ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"], fontsize=7)
        ax.spines["left"].set_visible(False)
        ax.spines["bottom"].set_color(SOFT_BLACK)
        ax.tick_params(axis="x", length=2)

    panel(top_ax, WITHIN_JAPANESE_GROUPS, "Japanese")
    panel(bottom_ax, WITHIN_GERMAN_GROUPS, "German")

    # Group headers for each panel, positioned ABOVE the panels with
    # generous clearance so they don't collide with row labels.
    # Top-panel axes spans y=0.50\u20130.76; group title at 0.81 sits well above.
    # Bottom-panel axes spans y=0.15\u20130.33; group title at 0.40.
    fig.text(0.04, 0.81, "Within Japanese lineage",
             fontsize=10, fontweight="bold", color=SOFT_BLACK, ha="left")
    fig.text(0.04, 0.785, "H3: 44.3pp gap, 5x ratio",
             fontsize=7.5, style="italic", color=GRAY_60, ha="left")

    fig.text(0.04, 0.385, "Within German lineage",
             fontsize=10, fontweight="bold", color=SOFT_BLACK, ha="left")
    fig.text(0.04, 0.36, "H5: G\u00fcde at zero, ratio undefined",
             fontsize=7.5, style="italic", color=GRAY_60, ha="left")

    # Title + subtitle (figure-level)
    fig.text(0.04, 0.94,
             "The mechanism operates within every lineage",
             fontsize=12, fontweight="bold", color=SOFT_BLACK, ha="left")
    fig.text(0.04, 0.90,
             "Brand-level marketing-language coverage predicts AI Presence inside each lineage cohort.",
             fontsize=8.5, color=SOFT_BLACK, ha="left")

    fig.text(0.04, 0.025, SOURCE_LINE, fontsize=6.5,
             style="italic", color=SOFT_BLACK, ha="left")

    save(fig, "chart_v08_f3_within_lineage_6col.pdf")


# ===========================================================================
# Chart 4 (Finding 4) \u2014 Per-CEP \u00d7 lineage matrix
# (6_col_hero_short: 7.50 \u00d7 3.75)
#
# Heatmap-style matrix showing how each lineage performs across the six CEPs.
# The German collapse in p3 and saturation in p4 is the focal observation.
# ===========================================================================

# Matrix from analyzer output:
# Rows = lineages, Cols = CEPs (p1..p6)
PER_CEP_MATRIX = {
    # cep_label: {jp, de, us, hybrid}
    "p1\nFunctional":   {"japanese":  9.8, "german": 30.0, "american": 0.8, "hybrid":  4.2},
    "p2\nContextual":   {"japanese": 17.2, "german": 41.7, "american": 1.2, "hybrid": 39.6},
    "p3\nConstraint":   {"japanese": 21.3, "german":  2.1, "american": 0.0, "hybrid": 31.2},
    "p4\nIdentity":     {"japanese": 42.0, "german": 45.8, "american": 0.0, "hybrid": 50.0},
    "p5\nDiscovery":    {"japanese":  4.2, "german":  0.8, "american": 0.0, "hybrid":  0.0},
    "p6\nComparison":   {"japanese": 16.7, "german": 43.3, "american": 1.2, "hybrid": 64.6},
}

LINEAGE_ROWS = [
    # (lineage_key, display_label, color_key)
    ("japanese", "Japanese", "japanese_mm"),
    ("german",   "German",   "german_mm"),
    ("american", "American", "american"),
    ("hybrid",   "Miyabi",   "hybrid"),
]


def chart_f4_per_cep():
    fig = plt.figure(figsize=(7.50, 3.75))
    ax = fig.add_axes([0.16, 0.20, 0.78, 0.55])

    cep_labels = list(PER_CEP_MATRIX.keys())
    n_ceps = len(cep_labels)
    n_lineages = len(LINEAGE_ROWS)

    bar_w = 0.20  # group of 4 bars per CEP
    group_centers = list(range(n_ceps))

    for li, (lk, label, color_key) in enumerate(LINEAGE_ROWS):
        offsets = [c + (li - (n_lineages - 1) / 2) * bar_w for c in group_centers]
        values = [PER_CEP_MATRIX[c][lk] for c in cep_labels]
        ax.bar(offsets, values, width=bar_w * 0.92,
               color=LINEAGE_COLOR[color_key], edgecolor="none",
               label=label)

    # Highlight p3 column (German collapse)
    ax.axvspan(2 - 0.45, 2 + 0.45, color=GRAY_20, alpha=0.18, zorder=0)
    ax.text(2, 53, "German\ncollapses\nto 2.1%", ha="center", va="top",
            fontsize=7.5, style="italic", color=COPPER, fontweight="bold")

    ax.set_xticks(group_centers)
    ax.set_xticklabels(cep_labels, fontsize=8)
    ax.set_ylim(0, 55)
    ax.set_yticks([0, 10, 20, 30, 40, 50])
    ax.set_yticklabels(["0%", "10%", "20%", "30%", "40%", "50%"], fontsize=8)
    ax.spines["bottom"].set_color(SOFT_BLACK)
    ax.tick_params(axis="x", length=0, pad=4)
    ax.tick_params(axis="y", length=2)

    # Title + subtitle
    fig.text(0.05, 0.92,
             "The variance is in German. Japanese is the steady lineage.",
             fontsize=12, fontweight="bold", color=SOFT_BLACK, ha="left")
    fig.text(0.05, 0.86,
             "Per-CEP brand-surfacing rate by lineage. p3 (constraint) collapses German; p4 (identity) peaks both.",
             fontsize=8, color=SOFT_BLACK, ha="left")

    # Legend (bottom, compact)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.18), ncol=4,
              frameon=False, fontsize=8, handlelength=1.2, handleheight=0.9,
              columnspacing=1.5)

    fig.text(0.05, 0.025, SOURCE_LINE, fontsize=6.5,
             style="italic", color=SOFT_BLACK, ha="left")

    save(fig, "chart_v08_f4_per_cep_6col.pdf")


# ===========================================================================
# Chart 5 (Finding 5) \u2014 Within-lab freshness (3_col_inline: 3.68 \u00d7 2.85)
#
# Compact inline chart showing within-Anthropic and within-OpenAI generational
# pairs. Each pair has older model on top, newer on bottom; the lineage
# aggregate value shifts toward Japanese (boundary lineage) in the newer model.
# ===========================================================================

FRESHNESS_PAIRS = {
    # lab: [(model_label, japanese_aggregate_pct, is_newer)]
    "Anthropic": [
        ("Sonnet 4.6", 18.8, False),
        ("Opus 4.7",   21.1, True),
    ],
    "OpenAI": [
        ("gpt-5.4-mini", 15.0, False),
        ("gpt-5.5",      25.2, True),
    ],
}


def chart_f5_freshness():
    fig = plt.figure(figsize=(3.68, 2.85))

    top_ax    = fig.add_axes([0.30, 0.55, 0.58, 0.22])
    bottom_ax = fig.add_axes([0.30, 0.18, 0.58, 0.22])

    def mini_pair(ax, rows):
        labels = [r[0] for r in rows]
        values = [r[1] for r in rows]
        is_newer = [r[2] for r in rows]
        y = list(range(len(rows)))[::-1]
        h = 0.55
        colors = [INDIGO if n else INDIGO_50 for n in is_newer]
        ax.barh(y, values, color=colors, height=h, edgecolor="none")
        for i, v in enumerate(values):
            ax.text(v + 0.6, y[i], f"{v:.1f}%", va="center",
                    fontsize=7, fontweight="bold", color=INDIGO)
        for i, lab in enumerate(labels):
            weight = "bold" if is_newer[i] else "normal"
            ax.text(-0.6, y[i], lab, va="center", ha="right",
                    fontsize=7, fontweight=weight, color=SOFT_BLACK)
        # Gap annotation between rows
        gap = values[1] - values[0]
        if abs(gap) > 0.5:
            sign = "+" if gap > 0 else ""
            ax.text(max(values) + 6, 0.5, f"{sign}{gap:.1f}pp",
                    va="center", ha="left", fontsize=6.5,
                    style="italic", color=GRAY_60)

        ax.set_xlim(0, 32)
        ax.set_ylim(-0.55, len(rows) - 0.45)
        ax.set_yticks([])
        ax.set_xticks([0, 10, 20, 30])
        ax.set_xticklabels(["0%", "10%", "20%", "30%"], fontsize=6)
        ax.spines["left"].set_visible(False)
        ax.spines["bottom"].set_color(SOFT_BLACK)
        ax.tick_params(axis="x", length=2)

    mini_pair(top_ax, FRESHNESS_PAIRS["Anthropic"])
    mini_pair(bottom_ax, FRESHNESS_PAIRS["OpenAI"])

    fig.text(0.04, 0.81, "Anthropic", fontsize=8, fontweight="bold", color=SOFT_BLACK)
    fig.text(0.04, 0.78, "Sonnet 4.6 \u2192 Opus 4.7", fontsize=6.5, color=SOFT_BLACK)
    fig.text(0.04, 0.44, "OpenAI", fontsize=8, fontweight="bold", color=SOFT_BLACK)
    fig.text(0.04, 0.41, "mini \u2192 5.5 (newer)", fontsize=6.5, color=SOFT_BLACK)

    fig.text(0.04, 0.94, "Within-lab freshness",
             fontsize=10, fontweight="bold", color=SOFT_BLACK, ha="left")
    fig.text(0.04, 0.90,
             "Newer surfaces JP boundary more",
             fontsize=7, color=SOFT_BLACK, ha="left")

    fig.text(0.04, 0.04, "Source: AIPI v0.8  \u00b7  6 May 2026",
             fontsize=6, style="italic", color=SOFT_BLACK, ha="left")

    save(fig, "chart_v08_f5_freshness_4col.pdf")


# ===========================================================================
# Build all
# ===========================================================================

def build_all():
    print(f"[charts] palette: indigo={INDIGO}, copper={COPPER}, copper_50={COPPER_50}")
    print(f"[charts] font: {FONT_FAMILY}")
    print(f"[charts] output dir: {OUTPUT_DIR}")
    print()
    chart_leaderboard()
    chart_f1_lineage_aggregates()
    chart_f2_authorities()
    chart_f3_within_lineage()
    chart_f4_per_cep()
    chart_f5_freshness()
    print()
    print("[charts] done. 6 charts generated for build_report_v08.py")


if __name__ == "__main__":
    build_all()
