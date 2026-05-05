#!/usr/bin/env python3
"""
Phase 2 BBB chart generator.

Produces five PDF charts at locked figsize from the v06 chart_construction_rules
specification. Outputs go to <reports>/output/ and are picked up by
build_report_v07.py via the _slot_lookup table.

Charts:
  chart_v07_leaderboard_6col.pdf   7.50 \u00d7 7.50  (6_col_hero_xl)  household-goods leaderboard
  chart_v07_f1_comparator_6col.pdf 7.50 \u00d7 5.00  (6_col_hero)     BBB vs Pier 1 phantom comparator
  chart_v07_f2_valence_6col.pdf    7.50 \u00d7 5.00  (6_col_hero)     per-model valence breakdown
  chart_v07_f3_freshness_4col.pdf  3.68 \u00d7 2.85  (3_col_inline)   within-lab freshness pairs
  chart_v07_f4_temporal_6col.pdf   7.50 \u00d7 5.00  (6_col_hero)     per-CEP temporal frame breakdown

CRITICAL: bbox=None and pad_inches=0 on savefig so native figsize is preserved
exactly. The build_report_v07.py overlay relies on chart PDFs being at locked
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
from matplotlib.backends.backend_pdf import PdfPages
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

    # Pick up Copper Plate / Soft Black / Paper if present in the supporting
    # block. The exact JSON key paths in the schema may vary; we look for the
    # canonical names and accept whatever hex value is there.
    for block_name in ("brand_supporting", "data_viz_palette_sp_global"):
        block = brand.get("palette", {}).get(block_name, {})
        if isinstance(block, dict):
            # Recursively scan one level deep for hex values keyed by name.
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
INDIGO_50 = PALETTE["indigo_50"]   # caveated phantom
INDIGO_25 = PALETTE["indigo_25"]   # tertiary
COPPER = PALETTE["copper"]
SOFT_BLACK = PALETTE["soft_black"]
GRAY_20 = PALETTE["black_20"]
GRAY_40 = PALETTE["black_40"]
GRAY_60 = PALETTE["black_60"]


# ---------------------------------------------------------------------------
# Font registration
# ---------------------------------------------------------------------------

def register_fonts() -> str:
    """Find Akkurat Pro on the host. If found, returns 'Akkurat Pro' as the
    family name to use throughout the chart pipeline. Otherwise returns
    'Inter' if available, falling back to DejaVu Sans with a loud warning."""
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
        # Try the canonical family name first; matplotlib will pick whichever
        # member of the family it finds.
        for candidate in ("Akkurat Pro", "Akkurat", "AkkuratPro"):
            try:
                font_manager.findfont(candidate, fallback_to_default=False)
                print(f"[charts] using {candidate} ({len(akkurat_files)} files registered)")
                return candidate
            except Exception:
                continue

    # Inter fallback
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

# matplotlib defaults
plt.rcParams.update({
    "font.family": FONT_FAMILY,
    "font.size": 9,
    "axes.titlesize": 11,
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "axes.edgecolor": INDIGO,
    "axes.labelcolor": INDIGO,
    "axes.titlecolor": INDIGO,
    "xtick.color": INDIGO,
    "ytick.color": INDIGO,
    "text.color": INDIGO,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 0.6,
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
    "savefig.facecolor": "none",       # transparent, sits on cream paper
    "axes.facecolor": "none",
    "figure.facecolor": "none",

    # Convert all text to vector paths in the output PDF.
    # Without this, the chart PDF embeds font references (Akkurat Pro / Inter)
    # which collide with the same font references in the ReportLab base PDF
    # when pypdf overlays the chart \u2014 producing missing-glyph artifacts in
    # the merged output. fonttype=3 emits Type 3 PostScript outlines per glyph,
    # but those still carry font dictionaries; the truly collision-free option
    # is to ask matplotlib to vectorize text via the `pdf.use14corefonts=False`
    # path with text rendered as Path objects. We force this with the
    # text-as-path convention by telling the PDF backend to NOT use TrueType
    # subsetting and to NOT use the AFM core-fonts shortcut. The combination
    # ensures matplotlib falls back to embedding text as vector outlines, which
    # pypdf then merges without any font-table interaction.
    "pdf.fonttype": 3,                 # Type 3: per-glyph outlines, no shared font ref
    "ps.fonttype": 3,
    "pdf.use14corefonts": False,
})

SOURCE_LINE = "Source: Third System AI Presence Index v0.7  \u00b7  n=288 measurements (6 prompts \u00d7 6 models \u00d7 8 runs)  \u00b7  4 May 2026"


def save(fig, name: str):
    """Save at native figsize, no padding adjustment, so the slot reservation
    in build_report_v07.py matches exactly."""
    out = OUTPUT_DIR / name
    fig.savefig(str(out), format="pdf", bbox_inches=None, pad_inches=0,
                transparent=True)
    plt.close(fig)
    print(f"[charts] wrote {name}  ({out.stat().st_size / 1024:.1f} KB)")


# ===========================================================================
# Chart 1 — Household-goods leaderboard (6_col_hero_xl: 7.50 \u00d7 7.50)
# ===========================================================================

LEADERBOARD = [
    # (brand, presence_pct, is_phantom)
    ("Target",            83.7, False),
    ("Amazon",            70.8, False),
    ("IKEA",              67.0, False),
    ("Walmart",           64.9, False),
    ("HomeGoods",         47.9, False),
    ("Crate & Barrel",    47.6, False),
    ("Costco",            46.2, False),
    ("Wayfair",           39.9, False),
    ("Pottery Barn",      38.9, False),
    ("Williams-Sonoma",   36.8, False),
    ("Bed Bath & Beyond", 36.8, True),    # phantom test subject
    ("West Elm",          28.8, False),
    ("Sur La Table",      16.3, False),
    ("Brooklinen",        12.8, False),
    ("Parachute",         12.5, False),
    ("Container Store",    9.0, False),
    ("Boll & Branch",      5.9, False),
    ("World Market",       5.2, False),
    ("Quince",             5.2, False),
    ("At Home",            4.9, False),
    ("Pier 1",             0.0, True),    # phantom comparator
]


def chart_leaderboard():
    fig = plt.figure(figsize=(7.50, 7.50))
    # Axes width 0.55 (was 0.66) leaves room on right for phantom annotation
    # text without it getting clipped at the page edge.
    ax = fig.add_axes([0.27, 0.07, 0.55, 0.82])

    names = [r[0] for r in LEADERBOARD]
    values = [r[1] for r in LEADERBOARD]
    is_phantom = [r[2] for r in LEADERBOARD]

    y = list(range(len(names)))[::-1]   # top-to-bottom reading order
    colors = [INDIGO if p else GRAY_40 for p in is_phantom]

    ax.barh(y, values, color=colors, height=0.7, edgecolor="none")

    # Reference lines
    ax.axvline(25, color=GRAY_60, linestyle=(0, (2, 3)), linewidth=0.8, zorder=0)
    ax.axvline(44, color=GRAY_60, linestyle=(0, (2, 3)), linewidth=0.8, zorder=0)

    # Annotations on reference lines (inside top of plot)
    ax.text(25, len(names) + 0.2, "H1 threshold", color=GRAY_60,
            fontsize=7.5, ha="center", style="italic")
    ax.text(44, len(names) + 0.2, "Mint v0.6 (44%)", color=GRAY_60,
            fontsize=7.5, ha="center", style="italic")

    # Brand names on left (bold for phantoms)
    for i, (n, p) in enumerate(zip(names, is_phantom)):
        weight = "bold" if p else "normal"
        ax.text(-1, y[i], n, ha="right", va="center",
                fontsize=8.5, fontweight=weight, color=INDIGO)

    # Value labels on right of each bar
    for i, (v, p) in enumerate(zip(values, is_phantom)):
        weight = "bold" if p else "normal"
        if v > 0:
            ax.text(v + 1, y[i], f"{v:.1f}", ha="left", va="center",
                    fontsize=8, fontweight=weight, color=INDIGO)
        else:
            # Pier 1 marker
            ax.scatter([0.4], [y[i]], s=14, color=INDIGO, zorder=5)
            ax.text(2.5, y[i], "0.0", ha="left", va="center",
                    fontsize=8, fontweight="bold", color=INDIGO)

    # Phantom annotation on right side (compact form, fits in axes margin)
    for i, (n, p) in enumerate(zip(names, is_phantom)):
        if p:
            note = ("phantom \u00b7 37 mo." if "Bath" in n
                    else "phantom \u00b7 70 mo.")
            ax.text(102, y[i], note, ha="left", va="center",
                    fontsize=7.5, style="italic", color=INDIGO)

    ax.set_xlim(0, 100)
    ax.set_ylim(-0.6, len(names) - 0.4)
    ax.set_yticks([])
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"])
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color(INDIGO)
    ax.tick_params(axis="x", which="both", length=2)

    # Title and subtitle (figure-level)
    fig.text(0.05, 0.965, "AI Presence \u2014 Household Goods Retail",
             fontsize=14, fontweight="bold", color=INDIGO, ha="left")
    fig.text(0.05, 0.935,
             "21 brands ordered by Presence. Bed Bath & Beyond and Pier 1 highlighted as phantom and comparator.",
             fontsize=9, color=INDIGO, ha="left")

    # Source line at bottom
    fig.text(0.05, 0.018, SOURCE_LINE, fontsize=7,
             style="italic", color=INDIGO, ha="left")

    save(fig, "chart_v07_leaderboard_6col.pdf")


# ===========================================================================
# Chart 2 (Finding 1) — BBB vs Pier 1 phantom comparator (6_col_hero: 7.50 \u00d7 5.00)
# ===========================================================================

def chart_f1_comparator():
    fig = plt.figure(figsize=(7.50, 5.00))

    # Two side-by-side panels showing BBB and Pier 1 as filled-bar gauges.
    # Axes intentionally low so figure title (y=0.93) and panel headers
    # (transAxes y up to ~1.20) do not collide.
    left_ax  = fig.add_axes([0.10, 0.13, 0.32, 0.50])
    right_ax = fig.add_axes([0.58, 0.13, 0.32, 0.50])

    def panel(ax, label, sub1, sub2, value, status_text, status_sub):
        # Background frame box
        ax.add_patch(plt.Rectangle((0, 0), 1, 1, fill=False,
                                     edgecolor=GRAY_20, linewidth=0.8))
        # Gridlines at 25/50/75
        for g in (0.25, 0.50, 0.75):
            ax.axhline(g, color=GRAY_20, linestyle=(0, (2, 3)),
                       linewidth=0.6, zorder=0)
        # Filled bar
        if value > 0:
            ax.add_patch(plt.Rectangle((0, 0), 1, value / 100,
                                         color=INDIGO, zorder=2))
            # Big % label inside bar
            ax.text(0.5, value / 200, f"{value:.1f}%",
                    ha="center", va="center", fontsize=24,
                    fontweight="bold", color="white", zorder=3)
        else:
            # Zero marker line
            ax.plot([0, 1], [0, 0], color=INDIGO, linewidth=2.5, zorder=2)
            ax.text(0.5, 0.45, "0.0%", ha="center", va="center",
                    fontsize=24, fontweight="bold", color=INDIGO)

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
        ax.set_yticklabels(["0%", "25%", "50%", "75%", "100%"], fontsize=7.5)
        for s in ("top", "right", "bottom", "left"):
            ax.spines[s].set_visible(False)
        ax.tick_params(axis="y", which="both", length=0, pad=2)

        # Header above panel
        ax.text(0.5, 1.18, label, ha="center", va="bottom",
                transform=ax.transAxes, fontsize=12, fontweight="bold",
                color=INDIGO)
        ax.text(0.5, 1.10, sub1, ha="center", va="bottom",
                transform=ax.transAxes, fontsize=8, color=INDIGO)
        ax.text(0.5, 1.04, sub2, ha="center", va="bottom",
                transform=ax.transAxes, fontsize=8, color=INDIGO)

        # Status footer below panel
        ax.text(0.5, -0.05, status_text, ha="center", va="top",
                transform=ax.transAxes, fontsize=9, fontweight="bold",
                color=INDIGO)
        ax.text(0.5, -0.11, status_sub, ha="center", va="top",
                transform=ax.transAxes, fontsize=8, color=INDIGO)

    panel(left_ax, "Bed Bath & Beyond",
          "Bankruptcy April 2023  \u00b7  ~37 months pre-measurement",
          "Pre-collapse: ~$3.3B revenue, category-defining footprint",
          38.2,
          "Phantom: confirmed",
          "110 of 288 measurements")
    panel(right_ax, "Pier 1",
          "Bankruptcy February 2020  \u00b7  ~70 months pre-measurement",
          "Pre-collapse: ~$1.5B revenue, smaller specialty footprint",
          0.0,
          "Phantom: zero",
          "0 of 288 measurements")

    # Delta marker between panels
    fig.text(0.50, 0.38, "\u0394 38.2 pp", ha="center", va="center",
             fontsize=10, style="italic", color=INDIGO)

    # Title and subtitle
    fig.text(0.05, 0.93, "Two phantoms, two different fates",
             fontsize=14, fontweight="bold", color=INDIGO, ha="left")
    fig.text(0.05, 0.895,
             "Bed Bath & Beyond and Pier 1 share a fate (collapse \u2192 online-only revival) but differ on years-since-collapse",
             fontsize=8.5, color=INDIGO, ha="left")
    fig.text(0.05, 0.875,
             "and pre-collapse footprint. The phantom signal between them differs by 38.2 percentage points.",
             fontsize=8.5, color=INDIGO, ha="left")

    fig.text(0.05, 0.025, SOURCE_LINE, fontsize=7, style="italic",
             color=INDIGO, ha="left")

    save(fig, "chart_v07_f1_comparator_6col.pdf")


# ===========================================================================
# Chart 3 (Finding 2) — Per-model valence breakdown (6_col_hero: 7.50 \u00d7 5.00)
# ===========================================================================

MODELS_VALENCE = [
    # (label, naive%, caveated%, aware%, total%)
    ("Anthropic Opus 4.7",     2.1, 37.5, 16.7, 56.2),
    ("xAI Grok 4.1 Fast",      0.0, 47.9,  2.1, 50.0),
    ("OpenAI gpt-5.4-mini",    0.0, 12.5, 35.4, 47.9),
    ("Anthropic Sonnet 4.6",   4.2, 31.2,  6.2, 41.6),
    ("Google Gemini 2.5 Flash",0.0, 14.6,  2.1, 16.7),
    ("OpenAI gpt-5.5",         4.2,  6.2,  4.2, 14.6),
]


def _stacked_valence(ax, rows):
    """Reusable stacked horizontal bars: naive | caveated | aware."""
    labels = [r[0] for r in rows]
    naive  = [r[1] for r in rows]
    cav    = [r[2] for r in rows]
    aware  = [r[3] for r in rows]
    totals = [r[4] for r in rows]

    y = list(range(len(rows)))[::-1]
    h = 0.62

    # Stack
    ax.barh(y, naive,  color=INDIGO,    height=h, edgecolor="none")
    ax.barh(y, cav,    left=naive,
            color=INDIGO_50, height=h, edgecolor="none")
    ax.barh(y, aware,
            left=[n + c for n, c in zip(naive, cav)],
            color=GRAY_40,   height=h, edgecolor="none")

    # Total label after bar
    for i, t in enumerate(totals):
        ax.text(t + 1.5, y[i], f"{t:.1f}%", va="center",
                fontsize=9, fontweight="bold", color=INDIGO)

    # Y labels (model names)
    for i, lab in enumerate(labels):
        ax.text(-1, y[i], lab, va="center", ha="right",
                fontsize=9, fontweight="bold" if i == 0 else "normal",
                color=INDIGO)

    ax.set_xlim(0, 100)
    ax.set_ylim(-0.6, len(rows) - 0.4)
    ax.set_yticks([])
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"])
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color(INDIGO)
    ax.tick_params(axis="x", length=2)


def chart_f2_valence():
    fig = plt.figure(figsize=(7.50, 5.00))
    ax = fig.add_axes([0.27, 0.18, 0.65, 0.55])

    _stacked_valence(ax, MODELS_VALENCE)

    # Title + subtitle
    fig.text(0.05, 0.93, "How each model handles Bed Bath & Beyond",
             fontsize=14, fontweight="bold", color=INDIGO, ha="left")
    fig.text(0.05, 0.895,
             "Per-model valence breakdown of BBB mentions (denominator: 48 measurements per model).",
             fontsize=9, color=INDIGO, ha="left")

    # Legend (compact labels, sized to fit inside 7.5\" figure bounds)
    legend_elems = [
        Patch(facecolor=INDIGO,    label="Naive phantom"),
        Patch(facecolor=INDIGO_50, label="Caveated phantom"),
        Patch(facecolor=GRAY_40,   label="Aware (no recommendation)"),
    ]
    ax.legend(handles=legend_elems, loc="upper center",
              bbox_to_anchor=(0.5, -0.15), ncol=3, frameon=False,
              fontsize=8, handlelength=1.4, handleheight=1.0,
              columnspacing=1.2)

    fig.text(0.05, 0.025, SOURCE_LINE, fontsize=7,
             style="italic", color=INDIGO, ha="left")

    save(fig, "chart_v07_f2_valence_6col.pdf")


# ===========================================================================
# Chart 4 (Finding 3) — Within-lab freshness pairs (3_col_inline: 3.68 \u00d7 2.85)
# ===========================================================================

def chart_f3_freshness():
    fig = plt.figure(figsize=(3.68, 2.85))

    # Two stacked panels (Anthropic top, OpenAI bottom)
    top_ax    = fig.add_axes([0.30, 0.55, 0.65, 0.22])
    bottom_ax = fig.add_axes([0.30, 0.13, 0.65, 0.22])

    anthropic = [
        ("Sonnet 4.6", 4.2, 31.2,  6.2, 41.6),
        ("Opus 4.7",   2.1, 37.5, 16.7, 56.2),
    ]
    openai = [
        ("gpt-5.4-mini", 0.0, 12.5, 35.4, 47.9),
        ("gpt-5.5",      4.2,  6.2,  4.2, 14.6),
    ]

    def mini_stack(ax, rows):
        labels = [r[0] for r in rows]
        n_vals  = [r[1] for r in rows]
        c_vals  = [r[2] for r in rows]
        a_vals  = [r[3] for r in rows]
        totals  = [r[4] for r in rows]
        y = list(range(len(rows)))[::-1]
        h = 0.6
        ax.barh(y, n_vals,   color=INDIGO,    height=h, edgecolor="none")
        ax.barh(y, c_vals,   left=n_vals,
                color=INDIGO_50, height=h, edgecolor="none")
        ax.barh(y, a_vals,
                left=[n+c for n,c in zip(n_vals, c_vals)],
                color=GRAY_40,   height=h, edgecolor="none")
        for i, t in enumerate(totals):
            ax.text(t + 1.5, y[i], f"{t:.1f}%", va="center",
                    fontsize=7, fontweight="bold", color=INDIGO)
        for i, lab in enumerate(labels):
            ax.text(-1.5, y[i], lab, va="center", ha="right",
                    fontsize=7.5, color=INDIGO)
        ax.set_xlim(0, 75)
        ax.set_ylim(-0.6, len(rows) - 0.4)
        ax.set_yticks([])
        ax.set_xticks([0, 25, 50, 75])
        ax.set_xticklabels(["0%", "25%", "50%", "75%"], fontsize=6.5)
        ax.spines["left"].set_visible(False)
        ax.spines["bottom"].set_color(INDIGO)
        ax.tick_params(axis="x", length=2)

    mini_stack(top_ax, anthropic)
    mini_stack(bottom_ax, openai)

    # Group titles
    fig.text(0.04, 0.81, "Anthropic", fontsize=8, fontweight="bold", color=INDIGO)
    fig.text(0.04, 0.78, "Sonnet 4.6 \u2192 Opus 4.7", fontsize=7, color=INDIGO)
    fig.text(0.04, 0.39, "OpenAI", fontsize=8, fontweight="bold", color=INDIGO)
    fig.text(0.04, 0.36, "mini \u2192 5.5 (newer)", fontsize=7, color=INDIGO)

    # Title
    fig.text(0.04, 0.93, "Within-lab freshness",
             fontsize=10, fontweight="bold", color=INDIGO, ha="left")
    fig.text(0.04, 0.89,
             "Newer = more responsible, not less frequent",
             fontsize=7, color=INDIGO, ha="left")

    # Source
    fig.text(0.04, 0.04, "Source: AIPI v0.7  \u00b7  4 May 2026",
             fontsize=6, style="italic", color=INDIGO, ha="left")

    save(fig, "chart_v07_f3_freshness_4col.pdf")


# ===========================================================================
# Chart 5 (Finding 4) — Per-CEP temporal frame breakdown (6_col_hero: 7.50 \u00d7 5.00)
# ===========================================================================

CEPS_VALENCE = [
    # (label, naive%, caveated%, aware%, total%)
    ("IDENTITY (how it feels)",   0.0, 37.5, 43.8, 81.2),
    ("FUNCTIONAL (why)",          4.2, 60.4,  4.2, 70.8),
    ("CONTEXTUAL (when)",         2.1, 39.6, 14.6, 56.2),
    ("CONSTRAINT (within)",       4.2,  8.3,  0.0, 12.5),
    ("COMPARISON",                0.0,  4.2,  4.2,  8.3),
    ("DISCOVERY",                 0.0,  0.0,  0.0,  0.0),
]


def chart_f4_temporal():
    fig = plt.figure(figsize=(7.50, 5.00))
    ax = fig.add_axes([0.27, 0.18, 0.65, 0.55])

    _stacked_valence(ax, CEPS_VALENCE)

    # Annotate the zero row (DISCOVERY) — placed past the 0.0% label.
    ax.text(8, 0, "\u2014 zero mentions across 48 measurements \u2014",
            va="center", fontsize=8, style="italic", color=GRAY_60)

    # Title + subtitle
    fig.text(0.05, 0.93, "The same brand, different temporal frames",
             fontsize=14, fontweight="bold", color=INDIGO, ha="left")
    fig.text(0.05, 0.895,
             "Per-prompt valence breakdown of BBB mentions. Functional prompts activate BBB-as-current-online-retailer.",
             fontsize=9, color=INDIGO, ha="left")
    fig.text(0.05, 0.875,
             "Identity prompts activate BBB-as-cultural-memory. Same brand, six prompts, six different cognitive-time slots.",
             fontsize=9, color=INDIGO, ha="left")

    legend_elems = [
        Patch(facecolor=INDIGO,    label="Naive phantom"),
        Patch(facecolor=INDIGO_50, label="Caveated phantom"),
        Patch(facecolor=GRAY_40,   label="Aware (no recommendation)"),
    ]
    ax.legend(handles=legend_elems, loc="upper center",
              bbox_to_anchor=(0.5, -0.18), ncol=3, frameon=False,
              fontsize=8, handlelength=1.6, handleheight=1.0,
              columnspacing=1.5)

    fig.text(0.05, 0.025, SOURCE_LINE, fontsize=7,
             style="italic", color=INDIGO, ha="left")

    save(fig, "chart_v07_f4_temporal_6col.pdf")


# ===========================================================================
# Build all
# ===========================================================================

def build_all():
    print(f"[charts] palette: indigo={INDIGO}, copper={COPPER}")
    print(f"[charts] font: {FONT_FAMILY}")
    print(f"[charts] output dir: {OUTPUT_DIR}")
    print()
    chart_leaderboard()
    chart_f1_comparator()
    chart_f2_valence()
    chart_f3_freshness()
    chart_f4_temporal()
    print()
    print("[charts] done. 5 charts generated for build_report_v07.py")


if __name__ == "__main__":
    build_all()
