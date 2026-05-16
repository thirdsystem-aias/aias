"""v0.16 chart generation for the brand-format report and SSRN paper.

Produces five PDF charts visualising the v0.16 kitchen knives registry-expansion
result against the pre-registered H_Regime4_replication_knives conditions on the
28-brand panel (six traditions; new french cell n=4).

Carries v0.14 chart conventions forward (Third System brand spec 1.4):
  - Akkurat Pro + STIX mathtext, pdf.fonttype=42
  - Tradition-coloring for brand-level points (replaces v0.14 premium_tier)
  - 7.5" wide hero figsizes (6-column page grid)
  - Title 13pt bold + subtitle 9.5pt muted + source 7.5pt italic muted
  - adjustText with graceful fallback for label collision
  - 300 DPI vector PDF output

Convention evolutions from v0.14:
  1. Chart 4 colour-codes by tradition (six-level: chinese / japanese /
     british / indian / us_specialty / french) instead of v0.14's
     premium_tier (luxury / specialty / mainstream-premium).
  2. New Chart 5 — six-panel small-multiples by tradition cell, supporting
     reviewer questions about within-cell AI–Trends pattern distribution
     (per mega-prompt scope item).
  3. Chart 1 narrative shifts from v0.14's "kitchen knives joins Regime 4" to
     v0.16's "kitchen knives on the expanded panel" — outcome-neutral until
     acquisition lands tomorrow.
  4. Axis/panel labels updated: "controlling for age + tradition"
     (v0.14 used "age + tier"; v0.16 uses age + tradition six-level dummies
     per pre-reg sec. 3).

Charts produced:
  chart_v16_regime4_canonical.pdf            (HEADLINE — H_Regime4_replication_knives)
  chart_v16_per_category_rho_comparison.pdf  (6-cat construct validity)
  chart_v16_primary_vs_sensitivity.pdf       (Tea Box-excluded robustness)
  chart_v16_kitchen_knives_per_brand.pdf        (within-category, tradition-coloured)
  chart_v16_kitchen_knives_per_tradition.pdf    (NEW: six-panel small-multiples)

Run:
    python3 ~/aias/scripts/build_charts_v16.py
"""
import json
import textwrap
from pathlib import Path

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import rcParams
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D

try:
    from adjustText import adjust_text
    HAVE_ADJUST_TEXT = True
except ImportError:
    HAVE_ADJUST_TEXT = False

# ============================================================================
# Brand constants (mirrors build_charts_v13.py)
# ============================================================================

INDIGO       = "#37237B"
AMETHYST     = "#534F9E"
PETRO        = "#6A6AB1"
IRIS         = "#908EC5"
LAVENDER     = "#BBB9DD"
COPPER_PLATE = "#F36C35"
TEXT         = "#231F20"
MUTED        = "#6B6967"
GRID         = "#CCCCCC"
GRID_SUBTLE  = "#E5E5E5"
PASS_GREEN   = "#2E7D32"

# v0.16 tradition palette (chart 4 + chart 5; six tradition cells)
# Brand spec 1.5 -> palette.data_viz.schemes.qualitative_standard, first 6.
# Canonical ordered palette for nominal data where no point is inherently
# most important; colorblind-tested for Deuteranopia/Protanopia/Tritanopia.
# Indigo is intentionally reserved for chrome (title, headlines) per the
# spec rule against using Indigo as both chart series and brand anchor in
# the same view.
TRADITION_COLOR = {
    "japanese":             "#002B5F",   # Navy (qualitative_standard position 2)
    "german":               "#FFAC17",   # Honey (position 3)
    "french":               "#6A035C",   # Maroon (position 6) — preserves v0.15 french color
    "american_specialty":   "#DE8BA5",   # Sherbet (position 5)
    "chinese":              "#4F99C1",   # Water Jet (position 1)
}

TRADITION_LABEL = {
    "japanese":             "Japanese",
    "german":               "German",
    "french":               "French",
    "american_specialty":   "American specialty",
    "chinese":              "Chinese",
}

# TRADITION_LEVELS mirrors score_v16.py / pre-reg sec. 2 cell order
TRADITION_LEVELS = ["japanese", "german", "french", "american_specialty", "chinese"]

# Regime palette (chart 1 — category-level coloring)
REGIME_COLOR = {
    "Regime 1": INDIGO,
    "Regime 2": PETRO,
    "Regime 4": COPPER_PLATE,
    "Regime 3": MUTED,
}

# ============================================================================
# Font setup
# ============================================================================

def setup_font():
    for path in [Path.home() / ".fonts", Path.home() / "Library" / "Fonts"]:
        if path.exists():
            for fp in list(path.glob("Akkurat*.[ot]tf")) + list(path.glob("Inter*.[ot]tf")):
                try:
                    fm.fontManager.addfont(str(fp))
                except Exception:
                    pass
    available = {f.name for f in fm.fontManager.ttflist}
    for c in ("Akkurat Pro", "Akkurat Pro Regular", "Akkurat", "Inter"):
        if c in available:
            return c
    return "DejaVu Sans"


FONT = setup_font()
print(f"# Font in use: {FONT}")
print(f"# adjustText available: {HAVE_ADJUST_TEXT}")

rcParams["font.family"]       = [FONT, "sans-serif"]
rcParams["mathtext.fontset"]  = "stix"
rcParams["axes.linewidth"]    = 0.6
rcParams["axes.edgecolor"]    = MUTED
rcParams["axes.labelcolor"]   = TEXT
rcParams["xtick.color"]       = MUTED
rcParams["ytick.color"]       = MUTED
rcParams["xtick.labelsize"]   = 8.5
rcParams["ytick.labelsize"]   = 8.5
rcParams["axes.labelsize"]    = 9
rcParams["axes.titlesize"]    = 10
rcParams["axes.spines.top"]   = False
rcParams["axes.spines.right"] = False
rcParams["pdf.fonttype"]      = 42


# ============================================================================
# Paths and data
# ============================================================================

V13_ROOT = Path.home() / "aias" / "osf" / "v13"   # historical baseline (5 cats)
V15_ROOT = Path.home() / "aias" / "osf" / "v16"   # primary

V13_SCORING_PATH = V13_ROOT / "analysis" / "canonical_scoring.json"
V15_SCORING_PATH = V15_ROOT / "analysis" / "canonical_scoring.json"
V15_PAIRED_PATH  = V15_ROOT / "analysis" / "per_brand_paired.csv"
V15_REGIME4_PATH = V15_ROOT / "analysis" / "h_regime4_robustness.csv"
V15_HCC_PATH     = V15_ROOT / "analysis" / "h_coverage_closure.csv"

OUT_DIR = V15_ROOT / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ---- Load v0.13 scoring (multi-category historical baseline) --------------
with V13_SCORING_PATH.open() as f:
    v13_scoring = json.load(f)

# ---- Load v0.16 scoring (single-category, registry-expanded) --------------
with V15_SCORING_PATH.open() as f:
    v16_scoring = json.load(f)


def get_v16_correlations(wave_key):
    """Return (spearman_rho, partial_spearman_rho) for v0.16 kitchen knives at wave.

    score_v16.py emits this canonical structure (per Section 4 of the port):
      scoring["primary_analysis"]["correlations"][wave_key]

    Additional fallbacks kept for forward compatibility with hand-edited
    or restructured scoring JSONs.
    """
    # Canonical v0.16 structure
    if "primary_analysis" in v16_scoring and "correlations" in v16_scoring["primary_analysis"]:
        c = v16_scoring["primary_analysis"]["correlations"][wave_key]
        return c["spearman_rho"], c["partial_spearman_rho"]
    # Fallbacks
    if "per_category" in v16_scoring:
        if "kitchen_knives" in v16_scoring["per_category"]:
            c = v16_scoring["per_category"]["kitchen_knives"]["correlations"][wave_key]
            return c["spearman_rho"], c["partial_spearman_rho"]
    if "primary" in v16_scoring and "correlations" in v16_scoring["primary"]:
        c = v16_scoring["primary"]["correlations"][wave_key]
        return c["spearman_rho"], c["partial_spearman_rho"]
    if "correlations" in v16_scoring:
        c = v16_scoring["correlations"][wave_key]
        return c["spearman_rho"], c["partial_spearman_rho"]
    raise KeyError(f"Cannot locate v0.16 correlations for {wave_key} in scoring JSON")


def get_v16_sensitivity_correlations(wave_key):
    """Return (rho, partial_rho) for Tea Box-excluded sensitivity. Falls back
    to None if not present (chart 3 will skip that overlay)."""
    # Canonical v0.16 structure
    if ("tea_box_excluded_sensitivity" in v16_scoring
            and "correlations" in v16_scoring["tea_box_excluded_sensitivity"]):
        c = v16_scoring["tea_box_excluded_sensitivity"]["correlations"].get(wave_key)
        if c is not None:
            return c.get("spearman_rho"), c.get("partial_spearman_rho")
    # Fallbacks
    if "sensitivity" in v16_scoring and "tea_box_excluded" in v16_scoring["sensitivity"]:
        if wave_key in v16_scoring["sensitivity"]["tea_box_excluded"]:
            c = v16_scoring["sensitivity"]["tea_box_excluded"][wave_key]
            return c.get("spearman_rho"), c.get("partial_spearman_rho")
    if "tea_box_excluded" in v16_scoring:
        if wave_key in v16_scoring["tea_box_excluded"]:
            c = v16_scoring["tea_box_excluded"][wave_key]
            return c.get("spearman_rho"), c.get("partial_spearman_rho")
    return None, None


# ---- Load v0.14 per-brand paired data --------------------------------------
paired = pd.read_csv(V15_PAIRED_PATH)
for col in paired.columns:
    if any(tok in col for tok in ["eligible", "sparse", "excluded",
                                    "is_pivot", "is_phantom", "is_alternate"]):
        paired[col] = paired[col].apply(
            lambda x: str(x).strip().lower() == "true" if pd.notna(x) else False
        )

# Column-name compatibility: v0.14 schema uses 'canonical', v0.13 used 'brand'
BRAND_COL = "canonical" if "canonical" in paired.columns else "brand"

SOURCE_LINE = ("Source: Third System AI Presence Index v0.16 \u00b7 "
               "Google Trends acquisition [TBD post-acquisition] \u00b7 "
               "Pre-reg locked at v0.16-prereg (commit 511e339).")

# v0.13 + v0.14 category metadata (for chart 1, chart 2)
CATEGORY_LABELS = {
    "pmsoftware": "Project management software",
    "running":    "Premium running shoes",
    "oliveoil":   "Premium olive oil",
    "skincare":   "Premium facial skincare",
    "finance":    "Personal finance apps",
    "kitchenknives": "Kitchen knives",
}

CATEGORY_SHORT = {
    "pmsoftware": "PM software",
    "running":    "Running shoes",
    "oliveoil":   "Olive oil",
    "skincare":   "Skincare",
    "finance":    "Finance apps",
    "kitchenknives": "Kitchen knives",
}

CATEGORY_PIVOT = {
    "pmsoftware": "Asana",
    "running":    "Asics",
    "oliveoil":   "California Olive Ranch",
    "skincare":   "CeraVe",
    "finance":    "YNAB",
    "kitchenknives": "Victorinox",
}

CATEGORY_REGIME = {
    "pmsoftware": "Regime 1",
    "running":    "Regime 2",
    "oliveoil":   "Regime 3",
    "skincare":   "Regime 4",
    "finance":    "Regime 4",
    "kitchenknives": "Regime 4",
}

# Categories with v0.13 data for cross-comparison plots
V13_CATS = ["pmsoftware", "running", "oliveoil", "skincare", "finance"]


def get_v13_correlations(cat, wave_key):
    """Return (spearman_rho, partial_spearman_rho) for a v0.13 category."""
    c = v13_scoring["per_category"][cat]["correlations"][wave_key]
    return c["spearman_rho"], c["partial_spearman_rho"]


def get_v13_us_rho(cat, wave_key):
    """Return US-sensitivity bivariate ρ for a v0.13 category (chart 2)."""
    return v13_scoring["per_category"][cat]["correlations"][wave_key]["spearman_rho"]


# ============================================================================
# Shared chart elements
# ============================================================================

def draw_title_and_subtitle(fig, title, subtitle, x=0.06, title_y=0.96,
                              subtitle_y=0.91, wrap_width=130):
    fig.text(x, title_y, title, ha="left", va="top",
             fontsize=13, color=TEXT, weight="bold")
    wrapped_subtitle = textwrap.fill(subtitle, width=wrap_width,
                                       break_long_words=False,
                                       break_on_hyphens=False)
    fig.text(x, subtitle_y, wrapped_subtitle, ha="left", va="top",
             fontsize=9.5, color=MUTED)


def add_source(fig, x=0.06, y=0.025):
    fig.text(x, y, SOURCE_LINE, ha="left", va="top",
             fontsize=7.5, color=MUTED, style="italic")


# ============================================================================
# CHART 1: Regime 4 canonical classification (HEADLINE)
# ============================================================================

def chart_regime4_canonical():
    """Headline v0.14 chart.

    Plots each v0.13 + v0.14 category in (bivariate ρ × partial ρ) space —
    the canonical post-v0.14 visualization of the H_Regime4_replication
    condition framework. The Regime 4 zone is bounded by |bivariate ρ| < 0.35
    AND partial ρ < 0 (the v0.14 pre-reg conditions C2 + C3 in worldwide
    primary form).

    Skincare and finance migrate from positive bivariate to negative partial
    (their t1→t2 connectors cross the y=0 partial axis). Kitchen knives sits in
    Regime 4 at both waves with no migration — bivariate is already negative.
    All three Regime 4 cases cluster in the lower-left quadrant.
    """
    fig, ax = plt.subplots(figsize=(7.5, 6.5))

    # ---- Background regime zones (v0.14 canonical condition definitions) ---
    # Regime 4: |bivariate| < 0.35 AND partial < 0
    ax.add_patch(Rectangle((-0.35, -0.50), 0.70, 0.50,
                            facecolor=COPPER_PLATE, alpha=0.10,
                            edgecolor=COPPER_PLATE, linewidth=0.6,
                            linestyle="--", zorder=1))
    # Regime 1: bivariate ∈ [0.35, 0.65], partial ∈ [0.2, 0.65]
    ax.add_patch(Rectangle((0.35, 0.20), 0.30, 0.45,
                            facecolor=INDIGO, alpha=0.07,
                            edgecolor=INDIGO, linewidth=0.6,
                            linestyle="--", zorder=1))
    # Regime 2: bivariate > 0.65, partial ∈ [0.2, 0.65]
    ax.add_patch(Rectangle((0.65, 0.20), 0.30, 0.45,
                            facecolor=PETRO, alpha=0.10,
                            edgecolor=PETRO, linewidth=0.6,
                            linestyle="--", zorder=1))

    # ---- Threshold reference lines -----------------------------------------
    for x_th in (-0.35, 0.35, 0.65):
        ax.axvline(x_th, color=GRID, linewidth=0.5, linestyle=":", zorder=1)
    ax.axhline(0.0, color=MUTED, linewidth=0.6, linestyle="-", zorder=1)
    # Identity line y = x (bivariate == partial; covariates do nothing)
    ax.plot([-0.95, 0.95], [-0.95, 0.95],
            color=GRID_SUBTLE, linewidth=0.6, linestyle=":", zorder=1)
    ax.text(0.85, 0.78, "y = x", fontsize=7, color=MUTED,
            style="italic", ha="left", va="center", zorder=2)

    # ---- Regime zone labels (top of zones — data points cluster in middle) -
    ax.text(0.50, 0.62, "Regime 1\nMarginal direct",
            ha="center", va="top", fontsize=8, color=INDIGO,
            style="italic", zorder=2)
    ax.text(0.80, 0.62, "Regime 2\nAge-mediated strong",
            ha="center", va="top", fontsize=8, color=PETRO,
            style="italic", zorder=2)
    ax.text(0.00, -0.40, "Regime 4 (canonical, AIAS Protocol v1.2)\nCovariate-saturated weak",
            ha="center", va="center", fontsize=8, color=COPPER_PLATE,
            style="italic", zorder=2)

    # ---- Plot v0.13 categories --------------------------------------------
    texts = []
    plotted = []

    for cat in V13_CATS:
        if cat == "oliveoil":
            continue  # n=8, descriptive-only per §3.6a; not on canonical plot
        try:
            rho_t1, prho_t1 = get_v13_correlations(cat, "ww_t1")
            rho_t2, prho_t2 = get_v13_correlations(cat, "ww_t2")
        except KeyError:
            continue
        color = REGIME_COLOR[CATEGORY_REGIME[cat]]
        plotted.append((cat, rho_t1, prho_t1, rho_t2, prho_t2, color, False))

    # ---- Plot v0.16 kitchen knives (registry-expanded panel) -----------------
    pt_rho_t1, pt_prho_t1 = get_v16_correlations("ww_t1")
    pt_rho_t2, pt_prho_t2 = get_v16_correlations("ww_t2")
    plotted.append(("kitchenknives", pt_rho_t1, pt_prho_t1,
                    pt_rho_t2, pt_prho_t2, REGIME_COLOR["Regime 4"], True))

    for cat, rho_t1, prho_t1, rho_t2, prho_t2, color, is_v14 in plotted:
        # Connector line t1 → t2
        ax.plot([rho_t1, rho_t2], [prho_t1, prho_t2],
                color=color, alpha=0.55, linewidth=1.2, zorder=3)
        # t1: open marker
        ax.scatter([rho_t1], [prho_t1], s=90, facecolor="white",
                   edgecolor=color, linewidth=2.0, zorder=4)
        # t2: filled marker (star for v0.14 kitchen knives to highlight the new finding)
        marker = "*" if is_v14 else "o"
        size   = 220 if is_v14 else 90
        ax.scatter([rho_t2], [prho_t2], s=size, facecolor=color,
                   edgecolor="white" if is_v14 else color,
                   linewidth=1.2 if is_v14 else 1.0, zorder=5)

        label = CATEGORY_SHORT[cat]
        if is_v14:
            label = label + "  (v0.16)"
        t = ax.text(rho_t2, prho_t2, "  " + label,
                    fontsize=9.5, color=TEXT,
                    weight="bold" if is_v14 else "normal",
                    ha="left", va="center", zorder=6)
        texts.append(t)

    if HAVE_ADJUST_TEXT and texts:
        adjust_text(
            texts, ax=ax,
            arrowprops=dict(arrowstyle="-", color=GRID, lw=0.4),
            expand=(1.15, 1.4),
            force_text=(0.4, 0.7),
            force_static=(0.2, 0.3),
            max_move=(20, 30),
            iter_lim=150,
        )

    # ---- Legend ------------------------------------------------------------
    legend_elements = [
        Line2D([0], [0], marker="o", color="w", markerfacecolor="white",
               markeredgecolor=TEXT, markeredgewidth=1.8, markersize=9,
               label="t₁ (open)"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor=TEXT,
               markeredgecolor=TEXT, markersize=9,
               label="t₂ (filled)"),
        Line2D([0], [0], marker="*", color="w", markerfacecolor=COPPER_PLATE,
               markeredgecolor="white", markeredgewidth=1.2, markersize=15,
               label="Kitchen knives, v0.16"),
    ]
    ax.legend(handles=legend_elements, loc="lower right",
              frameon=False, fontsize=8.5)

    # ---- Axes --------------------------------------------------------------
    ax.set_xlim(-0.45, 0.95)
    ax.set_ylim(-0.50, 0.65)
    ax.set_xlabel(r"Bivariate Spearman $\rho$ (AI Presence × Trends, Worldwide)",
                  color=TEXT)
    ax.set_ylabel(r"Partial Spearman $\rho$ (controlling for age, tradition)",
                  color=TEXT)
    ax.grid(True, axis="both", color=GRID_SUBTLE, linewidth=0.4, zorder=0)

    # ---- Title / subtitle / source ----------------------------------------
    title = "H_Regime4_replication_knives — kitchen knives on the expanded panel (v0.16)"
    subtitle = ("Each category at (bivariate ρ × partial ρ), worldwide, with t₁→t₂ "
                "connectors. The Regime 4 zone (AIAS Protocol v1.2 canonical): "
                "|bivariate ρ| < 0.35 AND partial ρ < 0. v0.13 categories shown "
                "for historical baseline; kitchen knives (v0.16) is the registry-"
                "expanded reading on 28 brands across six traditions. C2 reads "
                "ρ(AI, Trends) directly per pre-reg sec. 4 (corrected from v0.14 "
                "Condition 2 wording).")
    draw_title_and_subtitle(fig, title, subtitle, x=0.06,
                            title_y=0.96, subtitle_y=0.92, wrap_width=92)
    add_source(fig, x=0.06, y=0.025)

    fig.subplots_adjust(top=0.78, bottom=0.10, left=0.10, right=0.96)

    out = OUT_DIR / "chart_v16_regime4_canonical.pdf"
    fig.savefig(out, dpi=300)
    plt.close(fig)
    return out


# ============================================================================
# CHART 2: Per-category bivariate / partial / US ρ comparison (extended)
# ============================================================================

def chart_per_category_rho_comparison():
    """Six categories × three indicator series (bivariate WW ρ, partial WW ρ,
    US ρ for sensitivity), each at t1 (open) and t2 (filled). Extends v0.13's
    chart 2 with kitchen knives as a sixth row.
    """
    cats = ["pmsoftware", "oliveoil", "running", "skincare", "finance", "kitchenknives"]
    fig, ax = plt.subplots(figsize=(7.5, 7.2))

    y_positions = np.arange(len(cats))[::-1]
    row_height = 0.18

    for i, cat in enumerate(cats):
        y = y_positions[i]
        try:
            if cat == "kitchenknives":
                rho_ww_t1,  prho_ww_t1 = get_v16_correlations("ww_t1")
                rho_ww_t2,  prho_ww_t2 = get_v16_correlations("ww_t2")
                rho_us_t1,  _          = get_v16_correlations("us_t1")
                rho_us_t2,  _          = get_v16_correlations("us_t2")
            else:
                rho_ww_t1,  prho_ww_t1 = get_v13_correlations(cat, "ww_t1")
                rho_ww_t2,  prho_ww_t2 = get_v13_correlations(cat, "ww_t2")
                rho_us_t1,  _          = get_v13_correlations(cat, "us_t1")
                rho_us_t2,  _          = get_v13_correlations(cat, "us_t2")
        except KeyError:
            continue

        # Bivariate WW (primary): INDIGO
        ax.scatter([rho_ww_t1], [y + row_height], s=85, facecolor="white",
                   edgecolor=INDIGO, linewidth=1.8, zorder=4)
        ax.scatter([rho_ww_t2], [y + row_height], s=85, facecolor=INDIGO,
                   edgecolor=INDIGO, linewidth=1.0, zorder=4)
        # Partial WW (secondary): PETRO
        ax.scatter([prho_ww_t1], [y], s=70, facecolor="white",
                   edgecolor=PETRO, linewidth=1.6, zorder=4)
        ax.scatter([prho_ww_t2], [y], s=70, facecolor=PETRO,
                   edgecolor=PETRO, linewidth=1.0, zorder=4)
        # Bivariate US (sensitivity): MUTED
        ax.scatter([rho_us_t1], [y - row_height], s=55, facecolor="white",
                   edgecolor=MUTED, linewidth=1.4, zorder=4)
        ax.scatter([rho_us_t2], [y - row_height], s=55, facecolor=MUTED,
                   edgecolor=MUTED, linewidth=1.0, zorder=4)

        # Regime tag at right edge of row
        regime = CATEGORY_REGIME[cat]
        ax.text(1.05, y, regime, fontsize=8.5,
                color=REGIME_COLOR[regime], ha="left", va="center",
                style="italic")

        # Highlight v0.14 row with subtle background
        if cat == "kitchenknives":
            ax.axhspan(y - 0.45, y + 0.45,
                       facecolor=COPPER_PLATE, alpha=0.05, zorder=0)

        # Row divider
        if i < len(cats) - 1:
            ax.axhline(y - 0.55, color=GRID_SUBTLE, linewidth=0.4, zorder=1)

    # Threshold reference lines
    for thresh, color in [(0.35, GRID),
                          (0.5,  INDIGO),
                          (0.65, PETRO)]:
        ax.axvline(thresh, color=color, linewidth=0.5, linestyle=":", zorder=1)
        ax.text(thresh, len(cats) - 0.4, f"{thresh:g}", fontsize=7.5,
                color=color, ha="center", va="bottom", style="italic")
    ax.axvline(0.0, color=MUTED, linewidth=0.4, zorder=1)

    # Legend at bottom
    legend_elements = [
        Line2D([0], [0], marker="o", color="w", markerfacecolor=INDIGO,
               markeredgecolor=INDIGO, markersize=9,
               label=r"Bivariate WW $\rho$"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor=PETRO,
               markeredgecolor=PETRO, markersize=8,
               label=r"Partial WW $\rho$ (controlling for age, tradition)"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor=MUTED,
               markeredgecolor=MUTED, markersize=7,
               label=r"Bivariate US $\rho$ (sensitivity)"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor="white",
               markeredgecolor=TEXT, markeredgewidth=1.6, markersize=8,
               label="Open = t₁ · Filled = t₂"),
    ]
    ax.legend(handles=legend_elements, loc="lower center",
              bbox_to_anchor=(0.5, -0.22), ncol=2,
              frameon=False, fontsize=8.5,
              handletextpad=0.4, columnspacing=2.0)

    ax.set_xlim(-1.10, 1.20)
    ax.set_ylim(-0.7, len(cats) - 0.3)
    ax.set_yticks(y_positions)
    ax.set_yticklabels([CATEGORY_LABELS[c] for c in cats],
                       fontsize=10, color=TEXT, weight="bold")
    ax.tick_params(axis="y", length=0, pad=8)
    ax.set_xlabel(r"Spearman $\rho$ (AI Presence × Trends)", color=TEXT)
    ax.spines["left"].set_visible(False)
    ax.grid(True, axis="x", color=GRID_SUBTLE, linewidth=0.4, zorder=0)

    title = "Per-category construct validity — v0.13 plus v0.16 (kitchen knives)"
    subtitle = ("Bivariate WW ρ (indigo) measures the AI Presence × Trends rank "
                "co-movement. Partial WW ρ (petro) controls for brand age and "
                "tradition (six-level dummies, k=6 expected). Bivariate US ρ (grey) "
                "is the US-region sensitivity. Open markers = t₁; filled = t₂. "
                "Kitchen knives (v0.16, highlighted row) is the registry-expanded "
                "reading on 28 brands.")
    draw_title_and_subtitle(fig, title, subtitle, x=0.06,
                            title_y=0.96, subtitle_y=0.92, wrap_width=92)
    add_source(fig, x=0.06, y=0.025)

    fig.subplots_adjust(top=0.82, bottom=0.20, left=0.30, right=0.92)

    out = OUT_DIR / "chart_v16_per_category_rho_comparison.pdf"
    fig.savefig(out, dpi=300)
    plt.close(fig)
    return out


# ============================================================================
# CHART 3: H_Discourse_Language_carryforward — discourse-language pair scatter
# ============================================================================

def chart_discourse_language_pair():
    """v0.16 chart 3 — H_Discourse_Language_carryforward visualization.

    Two-panel scatter (t1 left, t2 right). Per-brand AI Presence under:
        x: English-anchored prompt (knives_b3_en_jp)
        y: Japanese-language prompt (knives_b4_ja_01)

    Japanese tradition cell only (anchor cell for v0.8 finding,
    SSRN 6728000).

    Verdict zones (per pre-reg §2):
        rho < 0.85          -> CARRY-FORWARD CONFIRMED
        rho in [0.85, 0.95) -> CARRY-FORWARD WEAKENED
        rho >= 0.95         -> CARRY-FORWARD FALSIFIED-favorable
        n < 5               -> INCONCLUSIVE

    Data sources:
      - canonical_scoring.json["H_Discourse_Language_carryforward"]
        for verdict + rho + japanese_brands_in_panel
      - results_enriched_kitchen_knives_*.csv for per-brand presence
        re-computation (mirrors score_v16.compute_presence_by_prompt)
    """
    import pandas as pd

    hdl = v16_scoring.get("H_Discourse_Language_carryforward", {})
    if not hdl:
        print("  SKIP chart_discourse_language_pair: H_Discourse_Language_"
              "carryforward not in canonical_scoring.json")
        return None

    status         = hdl.get("status", "INDETERMINATE")
    en_prompt      = hdl.get("en_prompt_id", "knives_b3_en_jp")
    ja_prompt      = hdl.get("ja_prompt_id", "knives_b4_ja_01")
    japanese_brands = hdl.get("japanese_brands_in_panel", [])

    if not japanese_brands:
        print("  SKIP chart_discourse_language_pair: no Japanese-cell brands")
        return None

    # Locate enrichment CSV (mirrors score_v16.py)
    enriched_dir = Path.home() / "aias" / "data" / "kitchen_knives"
    enriched_candidates = sorted(
        enriched_dir.glob("results_enriched_kitchen_knives_*.csv"))
    if not enriched_candidates:
        print(f"  SKIP chart_discourse_language_pair: no enrichment CSV at "
              f"{enriched_dir}")
        return None
    enriched = pd.read_csv(enriched_candidates[-1])

    # Same matched-models + wave splits as score_v16.py
    MATCHED_MODELS = {"claude-sonnet-4-6", "gpt-5.4-mini"}
    T1_RUN_IDX = {1, 2, 3, 4}
    T2_RUN_IDX = {5, 6, 7, 8}

    df = enriched[enriched["model_slot"].isin(MATCHED_MODELS)]
    df = df[df["prompt_id"].isin([en_prompt, ja_prompt])]
    df = df[df["brand"].isin(japanese_brands)]

    fig, axes = plt.subplots(1, 2, figsize=(7.5, 4.7),
                              sharex=True, sharey=True)

    for i, (wave, ax, run_set) in enumerate(
            zip(("t1", "t2"), axes, (T1_RUN_IDX, T2_RUN_IDX))):
        wave_df = df[df["run_idx"].isin(run_set)]
        en_vals, ja_vals, labels = [], [], []
        for brand in japanese_brands:
            en_rows = wave_df[(wave_df["brand"] == brand)
                               & (wave_df["prompt_id"] == en_prompt)]
            ja_rows = wave_df[(wave_df["brand"] == brand)
                               & (wave_df["prompt_id"] == ja_prompt)]
            if len(en_rows) == 0 or len(ja_rows) == 0:
                continue
            en_vals.append(en_rows["ai_brand_mentioned"].mean() * 100)
            ja_vals.append(ja_rows["ai_brand_mentioned"].mean() * 100)
            labels.append(brand)

        # Identity line y = x
        ax.plot([0, 100], [0, 100], color=GRID_SUBTLE, linewidth=0.6,
                linestyle=":", zorder=1)

        if en_vals:
            ax.scatter(en_vals, ja_vals, s=85,
                       facecolor=TRADITION_COLOR["japanese"],
                       edgecolor="white", linewidth=1.2, zorder=4)

            texts = []
            for x, y, name in zip(en_vals, ja_vals, labels):
                t = ax.text(x, y, " " + name, fontsize=8.5, color=TEXT,
                            ha="left", va="center", zorder=5)
                texts.append(t)
            if HAVE_ADJUST_TEXT and texts:
                adjust_text(
                    texts, ax=ax,
                    arrowprops=dict(arrowstyle="-", color=GRID, lw=0.4),
                    expand=(1.1, 1.3), iter_lim=100)

        # Annotate rho + n
        wave_data = hdl.get("waves", {}).get(wave, {})
        rho = wave_data.get("rho")
        n   = wave_data.get("n")
        rho_text = f"$\\rho$ = {rho:.3f}" if rho is not None else r"$\rho$ = N/A"
        n_text   = f"  n = {n}" if n is not None else ""
        ax.text(0.05, 0.95, rho_text + n_text,
                transform=ax.transAxes, fontsize=10, color=TEXT,
                va="top", ha="left", weight="bold")

        ax.set_title("Wave $t_1$" if i == 0 else "Wave $t_2$",
                     color=TEXT, weight="bold")
        ax.set_xlabel(f"AI Presence — English ({en_prompt})",
                      color=TEXT, fontsize=9)
        if i == 0:
            ax.set_ylabel(f"AI Presence — Japanese ({ja_prompt})",
                          color=TEXT, fontsize=9)
        ax.set_xlim(-5, 105)
        ax.set_ylim(-5, 105)
        ax.grid(True, color=GRID_SUBTLE, linewidth=0.4)

    title = f"H_Discourse_Language_carryforward — Japanese cell — {status}"
    subtitle = (
        "Per-brand AI Presence: English-anchored prompt (x) vs Japanese-"
        "language prompt (y), Japanese tradition cell. v0.8 finding "
        "(SSRN 6728000) tested under v1.2 protocol with corrected eligibility "
        "filtering. $\\rho$ < 0.85 = CARRY-FORWARD CONFIRMED; $\\rho$ in "
        "[0.85, 0.95) = WEAKENED; $\\rho$ $\\geq$ 0.95 = FALSIFIED-favorable. "
        "Identity line y = x for reference."
    )
    draw_title_and_subtitle(fig, title, subtitle, x=0.06,
                            title_y=0.96, subtitle_y=0.91, wrap_width=92)
    add_source(fig, x=0.06, y=0.020)

    fig.subplots_adjust(top=0.78, bottom=0.13, left=0.10, right=0.96,
                        wspace=0.10)

    out = OUT_DIR / "chart_v16_discourse_language_pair.pdf"
    fig.savefig(out, dpi=300)
    plt.close(fig)
    return out


# ============================================================================
# CHART 4: Kitchen knives per-brand AI × Trends scatter
# ============================================================================

def chart_kitchen_knives_per_brand():
    """Two-panel scatter (t1 left, t2 right) of the v0.16 kitchen knives panel
    in (AI Presence % × Trends rescaled mean) space. Coloured by tradition
    (six-level: chinese / japanese / british / indian / us_specialty / french).
    Annotates the top AI Presence brands and the Trends pivot to make the
    divergence visible. The registry-expanded panel (n=28) includes the new
    french cell flagship Mariage Frères.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.5, 5.8), sharey=True)

    # ANNOTATE: top AI Presence brands + Victorinox (pivot, low AI)
    ANNOTATE = {"Harney & Sons", "Yunnan Sourcing", "Ippodo Tea",
                "Victorinox", "Rishi Tea", "TWG Tea", "Mariage Frères"}

    # Filter to eligible brands (not e1a-excluded)
    eligible = paired[~paired.get("e1a_excluded", False)].copy()

    plotted_tiers = set()

    for ax, wave in zip([ax1, ax2], ("t1", "t2")):
        elig_col = f"trends_ww_{wave}_eligible"
        mean_col = f"trends_ww_{wave}_mean"
        ai_col   = f"ai_{wave}_pct"

        sub = eligible[eligible.get(elig_col, False)].copy()
        sub = sub.dropna(subset=[mean_col, ai_col])

        if "tradition" not in sub.columns:
            # Defensive fallback; score_v16.py emits tradition per Section 2
            sub["tradition"] = None

        # Plot per tradition (six cells in pre-reg sec. 2 order)
        texts = []
        for trad in TRADITION_LEVELS:
            trad_sub = sub[sub["tradition"] == trad]
            if len(trad_sub) == 0:
                continue
            color = TRADITION_COLOR.get(trad, MUTED)
            label = TRADITION_LABEL.get(trad, trad) if (ax is ax1 and trad not in plotted_tiers) else None
            if label:
                plotted_tiers.add(trad)
            ax.scatter(trad_sub[ai_col], trad_sub[mean_col],
                       color=color, s=70, alpha=0.85,
                       edgecolor="white", linewidth=0.8, zorder=3,
                       label=label)
            for _, row in trad_sub.iterrows():
                brand = row[BRAND_COL]
                if brand not in ANNOTATE:
                    continue
                if brand == "Yunnan Sourcing":
                    # Panel-aware placement. t1 has room to the right of the
                    # dot; t2's dot is in the middle-right of the panel near
                    # Rishi Tea, so the label goes directly above instead.
                    if wave == "t2":
                        xy_offset = (0, 14)
                        ha_align = "center"
                    else:
                        xy_offset = (10, 12)
                        ha_align = "left"
                    ax.annotate(
                        str(brand),
                        xy=(row[ai_col], row[mean_col]),
                        xytext=xy_offset, textcoords="offset points",
                        fontsize=8.5, color=TEXT,
                        ha=ha_align, va="bottom", zorder=6,
                        arrowprops=dict(arrowstyle="-", color=GRID, lw=0.4,
                                        shrinkA=0, shrinkB=4),
                    )
                else:
                    t = ax.text(row[ai_col], row[mean_col],
                                "  " + str(brand),
                                fontsize=8.5, color=TEXT,
                                ha="left", va="center", zorder=5)
                    texts.append(t)

        if HAVE_ADJUST_TEXT and texts:
            adjust_text(
                texts, ax=ax,
                arrowprops=dict(arrowstyle="-", color=GRID, lw=0.4),
                expand=(1.15, 1.4),
                force_text=(0.4, 0.7),
                max_move=(15, 25),
                iter_lim=120,
            )

        # Wave callout (top-right; top-left would collide with Victorinox/Tea Box)
        rho, prho = get_v16_correlations(f"ww_{wave}")
        wave_label = "t₁ (29 April 2026)" if wave == "t1" else "t₂ (7 May 2026)"
        callout = (f"{wave_label}\n"
                   r"$\rho$(AI, Trends) = " + f"{rho:+.3f}\n"
                   "Partial " + r"$\rho$ = " + f"{prho:+.3f}")
        ax.text(0.96, 0.96, callout,
                transform=ax.transAxes, fontsize=8.5, color=TEXT,
                ha="right", va="top", weight="bold",
                bbox=dict(facecolor="white", edgecolor=GRID,
                          boxstyle="round,pad=0.5", linewidth=0.5))

        ax.set_xlabel("AI Presence (% of responses, MATCHED_MODELS)", color=TEXT)
        if wave == "t1":
            ax.set_ylabel("Trends rescaled mean (per E1b)", color=TEXT)
        ax.grid(True, color=GRID_SUBTLE, linewidth=0.4, zorder=0)
        ax.set_xlim(left=0)
        # Extend right side for label space (Yunnan Sourcing at far right edge)
        right_lim = ax.get_xlim()[1]
        ax.set_xlim(0, right_lim * 1.15)
        ax.set_ylim(bottom=0)

    # Shared tradition legend at bottom (six cells in two rows of three)
    ax1.legend(loc="lower center", bbox_to_anchor=(1.10, -0.45),
               ncol=3, frameon=False, fontsize=8.5,
               handletextpad=0.4, columnspacing=2.0)

    title = "Kitchen knives — AI Presence × Trends, per-brand scatter"
    subtitle = ("Each point is a brand at one wave; eligible (E1a + E1b) brands "
                "only. Coloured by tradition (six-level: chinese / japanese / "
                "british / indian / us_specialty / french). The registry-expanded "
                "panel includes 28 brands stratified across six tradition cells, "
                "with the new french cell n=4 (Mariage Frères, Palais des Thés, "
                "Kusmi, Dammann Frères).")
    draw_title_and_subtitle(fig, title, subtitle, x=0.06,
                            title_y=0.96, subtitle_y=0.91, wrap_width=92)
    add_source(fig, x=0.06, y=0.025)

    fig.subplots_adjust(top=0.78, bottom=0.30, left=0.09, right=0.97,
                        wspace=0.12)

    out = OUT_DIR / "chart_v16_kitchen_knives_per_brand.pdf"
    fig.savefig(out, dpi=300)
    plt.close(fig)
    return out


# ============================================================================
# CHART 5: Kitchen knives AI x Trends, per-tradition small-multiples (v0.16 NEW)
# ============================================================================

def chart_kitchen_knives_per_tradition():
    """Six-panel small-multiples (one per tradition cell) showing the v0.16
    kitchen knives panel in (AI Presence x Trends) space within each cell.

    Each panel includes both t1 (filled marker) and t2 (open marker) for
    every eligible brand in that tradition. Shared axes enable direct
    cross-tradition visual comparison of the AI-Trends pattern.

    Layout: 2 rows x 3 cols. Cell order from TRADITION_LEVELS (pre-reg sec. 2):
      [chinese,  japanese, british ]
      [indian,   us_spec,  french  ]
    """
    fig, axes = plt.subplots(2, 3, figsize=(7.5, 7.2),
                              sharex=False, sharey=False)
    flat_axes = axes.flatten()

    eligible = paired[~paired.get("e1a_excluded", False)].copy()

    for idx, trad in enumerate(TRADITION_LEVELS):
        ax = flat_axes[idx]
        color = TRADITION_COLOR.get(trad, MUTED)
        label = TRADITION_LABEL.get(trad, trad)

        trad_sub = eligible[eligible.get("tradition") == trad].copy()
        n_in_cell = len(trad_sub)

        # Plot t1 (filled circle, on color) and t2 (open circle, white fill)
        for wave, mfc in [("t1", color), ("t2", "white")]:
            elig_col = f"trends_ww_{wave}_eligible"
            mean_col = f"trends_ww_{wave}_mean"
            ai_col   = f"ai_{wave}_pct"
            wave_sub = trad_sub[trad_sub.get(elig_col, False)].copy()
            wave_sub = wave_sub.dropna(subset=[mean_col, ai_col])
            if len(wave_sub) == 0:
                continue
            ax.scatter(
                wave_sub[ai_col], wave_sub[mean_col],
                facecolors=mfc, edgecolors=color, linewidth=1.4,
                s=55, alpha=0.90, zorder=3,
            )

        # Label every brand (use t1 position if eligible, else t2);
        # adjustText handles in-panel collisions with dots + other labels
        texts = []
        for _, row in trad_sub.iterrows():
            elig_t1 = row.get("trends_ww_t1_eligible", False)
            elig_t2 = row.get("trends_ww_t2_eligible", False)
            t1_ai, t1_tr = row.get("ai_t1_pct"), row.get("trends_ww_t1_mean")
            t2_ai, t2_tr = row.get("ai_t2_pct"), row.get("trends_ww_t2_mean")
            if elig_t1 and pd.notna(t1_ai) and pd.notna(t1_tr):
                x, y = t1_ai, t1_tr
            elif elig_t2 and pd.notna(t2_ai) and pd.notna(t2_tr):
                x, y = t2_ai, t2_tr
            else:
                continue
            texts.append(ax.text(x, y, str(row[BRAND_COL]),
                                 fontsize=7, color=TEXT,
                                 ha="left", va="center", zorder=4))

        if HAVE_ADJUST_TEXT and texts:
            adjust_text(
                texts, ax=ax,
                arrowprops=dict(arrowstyle="-", color=GRID, lw=0.4),
                expand=(1.4, 1.8),
                force_text=(0.7, 1.0),
                max_move=(20, 30),
                iter_lim=200,
            )

        ax.set_title(f"{label}  (n={n_in_cell})",
                     fontsize=10, color=color, weight="bold",
                     loc="left", pad=4)
        ax.grid(True, color=GRID_SUBTLE, linewidth=0.4, zorder=0)

    # Shared axis labels on bottom-row x and left-column y
    for ax in axes[1, :]:
        ax.set_xlabel("AI Presence (%)", color=TEXT, fontsize=9)
    for ax in axes[:, 0]:
        ax.set_ylabel("Trends rescaled mean", color=TEXT, fontsize=9)

    # Wave legend (t1 filled vs t2 open)
    legend_elements = [
        Line2D([0], [0], marker="o", color="w", markerfacecolor=MUTED,
               markeredgecolor=MUTED, markersize=8,
               label=r"t$_1$ (filled)"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor="white",
               markeredgecolor=MUTED, markeredgewidth=1.4, markersize=8,
               label=r"t$_2$ (open)"),
    ]
    # Reserve extra bottom margin so xlabels and legend don't collide
    # at the reduced 7.2" figure height (default 10% margin too tight).
    fig.subplots_adjust(bottom=0.13)

    fig.legend(handles=legend_elements, loc="lower center",
               bbox_to_anchor=(0.5, 0.005), ncol=2, frameon=False,
               fontsize=9, handletextpad=0.4, columnspacing=2.5)

    title = "Kitchen knives — per-tradition AI x Trends pattern (v0.16)"
    subtitle = ("Six-panel small-multiples of the v0.16 panel (28 brands "
                "across six tradition cells; new french cell shown bottom-"
                "right). Filled markers = t1, open markers = t2. Per-panel "
                "axes (magnitudes vary substantially across cells); panel "
                "titles show the in-cell brand count.")
    draw_title_and_subtitle(fig, title, subtitle, x=0.06,
                            title_y=0.97, subtitle_y=0.925, wrap_width=92)
    add_source(fig, x=0.06, y=0.012)

    fig.subplots_adjust(top=0.80, bottom=0.10, left=0.09, right=0.97,
                        wspace=0.25, hspace=0.40)

    out = OUT_DIR / "chart_v16_kitchen_knives_per_tradition.pdf"
    fig.savefig(out, dpi=300)
    plt.close(fig)
    return out


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    print()
    print("Generating v0.16 chart suite...")
    print(f"  Output: {OUT_DIR}")
    print()
    p1 = chart_regime4_canonical()
    print(f"  HEADLINE  {p1.name}")
    p2 = chart_per_category_rho_comparison()
    print(f"  per_cat   {p2.name}")
    p3 = chart_discourse_language_pair()
    print(f"  discourse    {p3.name}")
    p4 = chart_kitchen_knives_per_brand()
    print(f"  per_brand {p4.name}")
    p5 = chart_kitchen_knives_per_tradition()
    print(f"  per_trad  {p5.name}")
    print()
    print("v0.16 chart build complete.")
