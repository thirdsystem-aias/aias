"""v0.14 chart generation for the brand-format report and SSRN paper.

Produces four PDF charts visualising the v0.14 premium tea finding:
H_Regime4_replication CONFIRMED, with premium tea as the third Regime 4
(covariate-saturated weak) datapoint joining skincare and finance from v0.13.

Mirrors v0.13 chart conventions (Third System brand spec 1.4):
  - Akkurat Pro + STIX mathtext, pdf.fonttype=42
  - Tier-coloring for brand-level points
  - 7.5" wide hero figsizes (6-column page grid)
  - Title 13pt bold + subtitle 9.5pt muted + source 7.5pt italic muted
  - adjustText with graceful fallback for label collision
  - 300 DPI vector PDF output

Two deliberate convention evolutions from v0.13:
  1. Chart 1 axes evolve from (bivariate ρ × covariate decrement) to
     (bivariate ρ × partial ρ). The v0.14 pre-reg condition framework
     (|bivariate ρ| < 0.35 AND partial ρ < 0) naturally classifies all
     three Regime 4 cases; the decrement-based view did not extend to
     premium tea (whose bivariate is already negative, yielding tiny
     decrement). The chart subtitle documents this evolution.
  2. Chart 4 uses premium_tier (luxury / specialty / mainstream-premium)
     instead of v0.13's market_tier (incumbent / mid-tier / challenger),
     reflecting the v0.14 category-specific tier schema.

Charts produced:
  chart_v14_regime4_canonical.pdf            (HEADLINE — H_Regime4_replication)
  chart_v14_per_category_rho_comparison.pdf  (6-cat construct-validity, extended)
  chart_v14_primary_vs_sensitivity.pdf       (Tea Box-excluded robustness)
  chart_v14_premium_tea_per_brand.pdf        (within-category AI × Trends scatter)

Run:
    python3 ~/aias/scripts/build_charts_v14.py
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

# v0.14 premium_tier palette (chart 4 only)
PREMIUM_TIER_COLOR = {
    "luxury":              INDIGO,
    "specialty":           COPPER_PLATE,
    "mainstream-premium":  PETRO,
    "mainstream premium":  PETRO,   # spelling tolerance
}

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

V13_ROOT = Path.home() / "aias" / "osf" / "v13"
V14_ROOT = Path.home() / "aias" / "osf" / "v14"

V13_SCORING_PATH = V13_ROOT / "analysis" / "canonical_scoring.json"
V14_SCORING_PATH = V14_ROOT / "analysis" / "canonical_scoring.json"
V14_PAIRED_PATH  = V14_ROOT / "analysis" / "per_brand_paired.csv"
V14_REGIME4_PATH = V14_ROOT / "analysis" / "h_regime4_replication.csv"

OUT_DIR = V14_ROOT / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ---- Load v0.13 scoring (multi-category) ----------------------------------
with V13_SCORING_PATH.open() as f:
    v13_scoring = json.load(f)

# ---- Load v0.14 scoring (single-category) ---------------------------------
with V14_SCORING_PATH.open() as f:
    v14_scoring = json.load(f)


def get_v14_correlations(wave_key):
    """Return (spearman_rho, partial_spearman_rho) for v0.14 premium tea at wave.

    score_v14.py emits this canonical structure:
      scoring["primary_analysis"]["correlations"][wave_key]

    Additional fallbacks are kept for forward compatibility with hand-edited
    or restructured scoring JSONs.
    """
    # Canonical v0.14 structure
    if "primary_analysis" in v14_scoring and "correlations" in v14_scoring["primary_analysis"]:
        c = v14_scoring["primary_analysis"]["correlations"][wave_key]
        return c["spearman_rho"], c["partial_spearman_rho"]
    # Fallbacks
    if "per_category" in v14_scoring:
        if "premium_tea" in v14_scoring["per_category"]:
            c = v14_scoring["per_category"]["premium_tea"]["correlations"][wave_key]
            return c["spearman_rho"], c["partial_spearman_rho"]
    if "primary" in v14_scoring and "correlations" in v14_scoring["primary"]:
        c = v14_scoring["primary"]["correlations"][wave_key]
        return c["spearman_rho"], c["partial_spearman_rho"]
    if "correlations" in v14_scoring:
        c = v14_scoring["correlations"][wave_key]
        return c["spearman_rho"], c["partial_spearman_rho"]
    raise KeyError(f"Cannot locate v0.14 correlations for {wave_key} in scoring JSON")


def get_v14_sensitivity_correlations(wave_key):
    """Return (rho, partial_rho) for Tea Box-excluded sensitivity. Falls back
    to None if not present (chart 3 will skip that overlay)."""
    # Canonical v0.14 structure
    if ("tea_box_excluded_sensitivity" in v14_scoring
            and "correlations" in v14_scoring["tea_box_excluded_sensitivity"]):
        c = v14_scoring["tea_box_excluded_sensitivity"]["correlations"].get(wave_key)
        if c is not None:
            return c.get("spearman_rho"), c.get("partial_spearman_rho")
    # Fallbacks
    if "sensitivity" in v14_scoring and "tea_box_excluded" in v14_scoring["sensitivity"]:
        if wave_key in v14_scoring["sensitivity"]["tea_box_excluded"]:
            c = v14_scoring["sensitivity"]["tea_box_excluded"][wave_key]
            return c.get("spearman_rho"), c.get("partial_spearman_rho")
    if "tea_box_excluded" in v14_scoring:
        if wave_key in v14_scoring["tea_box_excluded"]:
            c = v14_scoring["tea_box_excluded"][wave_key]
            return c.get("spearman_rho"), c.get("partial_spearman_rho")
    return None, None


# ---- Load v0.14 per-brand paired data --------------------------------------
paired = pd.read_csv(V14_PAIRED_PATH)
for col in paired.columns:
    if any(tok in col for tok in ["eligible", "sparse", "excluded",
                                    "is_pivot", "is_phantom", "is_alternate"]):
        paired[col] = paired[col].apply(
            lambda x: str(x).strip().lower() == "true" if pd.notna(x) else False
        )

# Column-name compatibility: v0.14 schema uses 'canonical', v0.13 used 'brand'
BRAND_COL = "canonical" if "canonical" in paired.columns else "brand"

SOURCE_LINE = ("Source: Third System AI Presence Index v0.14 · "
               "Google Trends acquisition 2026-05-12T15:54:30Z · "
               "Pre-reg locked at v0.14-prereg (commit b0ef30a).")

# v0.13 + v0.14 category metadata (for chart 1, chart 2)
CATEGORY_LABELS = {
    "pmsoftware": "Project management software",
    "running":    "Premium running shoes",
    "oliveoil":   "Premium olive oil",
    "skincare":   "Premium facial skincare",
    "finance":    "Personal finance apps",
    "premiumtea": "Premium tea",
}

CATEGORY_SHORT = {
    "pmsoftware": "PM software",
    "running":    "Running shoes",
    "oliveoil":   "Olive oil",
    "skincare":   "Skincare",
    "finance":    "Finance apps",
    "premiumtea": "Premium tea",
}

CATEGORY_PIVOT = {
    "pmsoftware": "Asana",
    "running":    "Asics",
    "oliveoil":   "California Olive Ranch",
    "skincare":   "CeraVe",
    "finance":    "YNAB",
    "premiumtea": "Twinings",
}

CATEGORY_REGIME = {
    "pmsoftware": "Regime 1",
    "running":    "Regime 2",
    "oliveoil":   "Regime 3",
    "skincare":   "Regime 4",
    "finance":    "Regime 4",
    "premiumtea": "Regime 4",
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
    (their t1→t2 connectors cross the y=0 partial axis). Premium tea sits in
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
    ax.text(0.00, -0.40, "Regime 4 (canonical, v0.14)\nCovariate-saturated weak",
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

    # ---- Plot v0.14 premium tea -------------------------------------------
    pt_rho_t1, pt_prho_t1 = get_v14_correlations("ww_t1")
    pt_rho_t2, pt_prho_t2 = get_v14_correlations("ww_t2")
    plotted.append(("premiumtea", pt_rho_t1, pt_prho_t1,
                    pt_rho_t2, pt_prho_t2, REGIME_COLOR["Regime 4"], True))

    for cat, rho_t1, prho_t1, rho_t2, prho_t2, color, is_v14 in plotted:
        # Connector line t1 → t2
        ax.plot([rho_t1, rho_t2], [prho_t1, prho_t2],
                color=color, alpha=0.55, linewidth=1.2, zorder=3)
        # t1: open marker
        ax.scatter([rho_t1], [prho_t1], s=90, facecolor="white",
                   edgecolor=color, linewidth=2.0, zorder=4)
        # t2: filled marker (star for v0.14 premium tea to highlight the new finding)
        marker = "*" if is_v14 else "o"
        size   = 220 if is_v14 else 90
        ax.scatter([rho_t2], [prho_t2], s=size, facecolor=color,
                   edgecolor="white" if is_v14 else color,
                   linewidth=1.2 if is_v14 else 1.0, zorder=5)

        label = CATEGORY_SHORT[cat]
        if is_v14:
            label = label + "  (v0.14)"
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
               label="Premium tea, v0.14"),
    ]
    ax.legend(handles=legend_elements, loc="lower right",
              frameon=False, fontsize=8.5)

    # ---- Axes --------------------------------------------------------------
    ax.set_xlim(-0.45, 0.95)
    ax.set_ylim(-0.50, 0.65)
    ax.set_xlabel(r"Bivariate Spearman $\rho$ (AI Presence × Trends, Worldwide)",
                  color=TEXT)
    ax.set_ylabel(r"Partial Spearman $\rho$ (controlling for age, tier)",
                  color=TEXT)
    ax.grid(True, axis="both", color=GRID_SUBTLE, linewidth=0.4, zorder=0)

    # ---- Title / subtitle / source ----------------------------------------
    title = "H_Regime4_replication CONFIRMED — premium tea joins the cluster"
    subtitle = ("Each category at (bivariate ρ × partial ρ), worldwide, with t₁→t₂ "
                "connectors. The Regime 4 zone is the v0.14 canonical definition: "
                "|bivariate ρ| < 0.35 AND partial ρ < 0. Skincare and finance migrate "
                "from positive bivariate to negative partial; premium tea (v0.14) "
                "sits in Regime 4 at both waves with bivariate already negative. "
                "Axes evolved from v0.13's (bivariate ρ × decrement) view, which did "
                "not extend to categories with already-negative bivariate.")
    draw_title_and_subtitle(fig, title, subtitle, x=0.06,
                            title_y=0.96, subtitle_y=0.92, wrap_width=92)
    add_source(fig, x=0.06, y=0.025)

    fig.subplots_adjust(top=0.78, bottom=0.10, left=0.10, right=0.96)

    out = OUT_DIR / "chart_v14_regime4_canonical.pdf"
    fig.savefig(out, dpi=300)
    plt.close(fig)
    return out


# ============================================================================
# CHART 2: Per-category bivariate / partial / US ρ comparison (extended)
# ============================================================================

def chart_per_category_rho_comparison():
    """Six categories × three indicator series (bivariate WW ρ, partial WW ρ,
    US ρ for sensitivity), each at t1 (open) and t2 (filled). Extends v0.13's
    chart 2 with premium tea as a sixth row.
    """
    cats = ["pmsoftware", "oliveoil", "running", "skincare", "finance", "premiumtea"]
    fig, ax = plt.subplots(figsize=(7.5, 8.0))

    y_positions = np.arange(len(cats))[::-1]
    row_height = 0.18

    for i, cat in enumerate(cats):
        y = y_positions[i]
        try:
            if cat == "premiumtea":
                rho_ww_t1,  prho_ww_t1 = get_v14_correlations("ww_t1")
                rho_ww_t2,  prho_ww_t2 = get_v14_correlations("ww_t2")
                rho_us_t1,  _          = get_v14_correlations("us_t1")
                rho_us_t2,  _          = get_v14_correlations("us_t2")
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
        if cat == "premiumtea":
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
               label=r"Partial WW $\rho$ (controlling for age, tier)"),
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

    title = "Per-category construct validity — v0.13 plus v0.14 (premium tea)"
    subtitle = ("Bivariate WW ρ (indigo) measures the AI Presence × Trends rank "
                "co-movement. Partial WW ρ (petro) controls for brand age and tier. "
                "Bivariate US ρ (grey) is the US-region sensitivity. Open markers = t₁; "
                "filled = t₂. Premium tea (v0.14, highlighted row) joins skincare and "
                "finance in the Regime 4 cluster.")
    draw_title_and_subtitle(fig, title, subtitle, x=0.06,
                            title_y=0.96, subtitle_y=0.92, wrap_width=92)
    add_source(fig, x=0.06, y=0.025)

    fig.subplots_adjust(top=0.82, bottom=0.20, left=0.30, right=0.92)

    out = OUT_DIR / "chart_v14_per_category_rho_comparison.pdf"
    fig.savefig(out, dpi=300)
    plt.close(fig)
    return out


# ============================================================================
# CHART 3: Primary vs Tea Box-excluded sensitivity
# ============================================================================

def chart_primary_vs_sensitivity():
    """Single-panel dot plot: 4 condition × 2 wave rows, primary (INDIGO)
    and Tea Box-excluded (PETRO) markers side by side per row. Shows the
    robustness of the Regime 4 verdict to Tea Box exclusion.
    """
    fig, ax = plt.subplots(figsize=(7.5, 6.8))

    # Collect primary values from v0.14 scoring
    rows = []
    for wave_key, wave_label in [("ww_t1", "Worldwide t₁"),
                                  ("ww_t2", "Worldwide t₂"),
                                  ("us_t1", "US t₁"),
                                  ("us_t2", "US t₂")]:
        try:
            rho_pri, prho_pri = get_v14_correlations(wave_key)
        except KeyError:
            rho_pri, prho_pri = None, None
        rho_sen, prho_sen = get_v14_sensitivity_correlations(wave_key)
        rows.append((wave_label, rho_pri, prho_pri, rho_sen, prho_sen))

    y_positions = np.arange(len(rows))[::-1]

    for i, (label, rho_pri, prho_pri, rho_sen, prho_sen) in enumerate(rows):
        y = y_positions[i]

        # Bivariate ρ — left half of plot (x in [-0.5, 0])
        x_offset_bi = -0.30
        if rho_pri is not None:
            ax.scatter([x_offset_bi + rho_pri], [y], s=100, facecolor=INDIGO,
                       edgecolor="white", linewidth=1.0, zorder=4,
                       label="Primary (n=17)" if i == 0 else None)
            ax.text(x_offset_bi + rho_pri, y + 0.16, f"{rho_pri:+.3f}",
                    fontsize=7.5, color=INDIGO, ha="center", va="bottom",
                    weight="bold")
        if rho_sen is not None:
            ax.scatter([x_offset_bi + rho_sen], [y], s=70, facecolor="white",
                       edgecolor=PETRO, linewidth=1.8, zorder=4,
                       label="Tea Box-excluded (n=16)" if i == 0 else None)
            ax.text(x_offset_bi + rho_sen, y - 0.22, f"{rho_sen:+.3f}",
                    fontsize=7.5, color=PETRO, ha="center", va="top",
                    style="italic")

        # Partial ρ — right half of plot (x in [0, +0.5])
        x_offset_pa = 0.40
        if prho_pri is not None:
            ax.scatter([x_offset_pa + prho_pri], [y], s=100, facecolor=INDIGO,
                       edgecolor="white", linewidth=1.0, zorder=4)
            ax.text(x_offset_pa + prho_pri, y + 0.16, f"{prho_pri:+.3f}",
                    fontsize=7.5, color=INDIGO, ha="center", va="bottom",
                    weight="bold")
        if prho_sen is not None:
            ax.scatter([x_offset_pa + prho_sen], [y], s=70, facecolor="white",
                       edgecolor=PETRO, linewidth=1.8, zorder=4)
            ax.text(x_offset_pa + prho_sen, y - 0.22, f"{prho_sen:+.3f}",
                    fontsize=7.5, color=PETRO, ha="center", va="top",
                    style="italic")

        # Row divider
        if i < len(rows) - 1:
            ax.axhline(y - 0.5, color=GRID_SUBTLE, linewidth=0.4, zorder=1)

    # Column separator
    ax.axvline(0.05, color=MUTED, linewidth=0.6, zorder=2)

    # Threshold reference: |bivariate| < 0.35 → at x_offset_bi ± 0.35
    ax.axvline(-0.30 + 0.35, color=GRID, linewidth=0.5, linestyle=":", zorder=1)
    ax.axvline(-0.30 - 0.35, color=GRID, linewidth=0.5, linestyle=":", zorder=1)
    # Centered bivariate origin
    ax.axvline(-0.30, color=GRID_SUBTLE, linewidth=0.4, linestyle="-", zorder=1)
    # Threshold reference: partial < 0 → at x_offset_pa (since partial=0 maps there)
    ax.axvline(0.40, color=COPPER_PLATE, linewidth=0.5, linestyle=":", zorder=1)

    # Panel labels (column headers)
    ax.text(-0.30, len(rows) - 0.3, "Bivariate ρ (AI × Trends)",
            fontsize=9, color=TEXT, weight="bold", ha="center", va="bottom")
    ax.text(-0.30 + 0.35, len(rows) - 0.45,
            r"$|\rho|<0.35$ (C2)", fontsize=7.5, color=GRID,
            ha="center", va="bottom", style="italic")
    ax.text(0.40, len(rows) - 0.3, "Partial ρ (controls: age, tier)",
            fontsize=9, color=TEXT, weight="bold", ha="center", va="bottom")
    ax.text(0.40, len(rows) - 0.45, r"$\rho<0$ (C3)",
            fontsize=7.5, color=COPPER_PLATE,
            ha="center", va="bottom", style="italic")

    ax.set_yticks(y_positions)
    ax.set_yticklabels([row[0] for row in rows],
                       fontsize=10, color=TEXT, weight="bold")
    ax.tick_params(axis="y", length=0, pad=8)
    ax.set_xticks([])  # x-axis is dual-panel; numbers shown via labels
    ax.set_xlim(-0.75, 0.85)
    ax.set_ylim(-0.7, len(rows) - 0.2)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)

    # Legend
    legend_elements = [
        Line2D([0], [0], marker="o", color="w", markerfacecolor=INDIGO,
               markeredgecolor="white", markeredgewidth=0.5, markersize=10,
               label="Primary (n=17, full panel)"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor="white",
               markeredgecolor=PETRO, markeredgewidth=1.8, markersize=9,
               label="Tea Box-excluded (n=16, sensitivity)"),
    ]
    ax.legend(handles=legend_elements, loc="lower center",
              bbox_to_anchor=(0.5, -0.10), ncol=2,
              frameon=False, fontsize=8.5,
              handletextpad=0.4, columnspacing=2.0)

    title = "Primary vs Tea Box-excluded sensitivity — H_Regime4_replication robust"
    subtitle = ("Each row shows bivariate ρ (left, vs C2 threshold |ρ|<0.35) and "
                "partial ρ (right, vs C3 threshold ρ<0) at one wave / region. "
                "Primary (indigo filled) uses the full eligible panel (n=17 ww, "
                "16-17 US). Tea Box-excluded (petro open) drops the brand whose "
                "rescaled Trends signal was confounded by generic 'tea box' gift-set "
                "language. Both panels satisfy C2 + C3 at every wave; the Regime 4 "
                "verdict does not depend on Tea Box.")
    draw_title_and_subtitle(fig, title, subtitle, x=0.06,
                            title_y=0.96, subtitle_y=0.91, wrap_width=92)
    add_source(fig, x=0.06, y=0.025)

    fig.subplots_adjust(top=0.74, bottom=0.13, left=0.21, right=0.95)

    out = OUT_DIR / "chart_v14_primary_vs_sensitivity.pdf"
    fig.savefig(out, dpi=300)
    plt.close(fig)
    return out


# ============================================================================
# CHART 4: Premium tea per-brand AI × Trends scatter
# ============================================================================

def chart_premium_tea_per_brand():
    """Two-panel scatter (t1 left, t2 right) of the v0.14 premium tea panel
    in (AI Presence % × Trends rescaled mean) space. Coloured by premium_tier
    (luxury / specialty / mainstream-premium). Annotates the top AI Presence
    brands and the Trends pivot to make the divergence visible.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.5, 5.8), sharey=True)

    # ANNOTATE: top AI Presence brands + Twinings (pivot, low AI)
    ANNOTATE = {"Harney & Sons", "Yunnan Sourcing", "Ippodo Tea",
                "Twinings", "Rishi Tea", "TWG Tea"}

    # Filter to eligible brands (not e1a-excluded)
    eligible = paired[~paired.get("e1a_excluded", False)].copy()

    plotted_tiers = set()

    for ax, wave in zip([ax1, ax2], ("t1", "t2")):
        elig_col = f"trends_ww_{wave}_eligible"
        mean_col = f"trends_ww_{wave}_mean"
        ai_col   = f"ai_{wave}_pct"

        sub = eligible[eligible.get(elig_col, False)].copy()
        sub = sub.dropna(subset=[mean_col, ai_col])

        if "premium_tier" not in sub.columns:
            # Fallback if column missing
            sub["premium_tier"] = "mainstream-premium"

        # Plot per tier
        texts = []
        for tier in ("luxury", "specialty", "mainstream-premium", "mainstream premium"):
            tier_sub = sub[sub["premium_tier"].astype(str).str.lower() == tier]
            if len(tier_sub) == 0:
                continue
            color = PREMIUM_TIER_COLOR.get(tier, MUTED)
            label = tier.capitalize() if (ax is ax1 and tier not in plotted_tiers) else None
            if label:
                plotted_tiers.add(tier)
            ax.scatter(tier_sub[ai_col], tier_sub[mean_col],
                       color=color, s=70, alpha=0.85,
                       edgecolor="white", linewidth=0.8, zorder=3,
                       label=label)
            for _, row in tier_sub.iterrows():
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

        # Wave callout (top-right; top-left would collide with Twinings/Tea Box)
        rho, prho = get_v14_correlations(f"ww_{wave}")
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

    # Shared tier legend at bottom
    ax1.legend(loc="lower center", bbox_to_anchor=(1.10, -0.22),
               ncol=3, frameon=False, fontsize=8.5,
               handletextpad=0.4, columnspacing=2.5)

    title = "Premium tea — AI Presence × Trends, per-brand scatter"
    subtitle = ("Each point is a brand at one wave; eligible (E1a + E1b) brands "
                "only. Coloured by premium_tier. Top AI Presence brands "
                "(Harney & Sons, Yunnan Sourcing, Ippodo) anchor the upper-x; "
                "the Trends pivot Twinings is lower-x, illustrating the Regime 4 "
                "decoupling — AI Presence ranks specialty/Asian brands that the "
                "Trends signal does not surface.")
    draw_title_and_subtitle(fig, title, subtitle, x=0.06,
                            title_y=0.96, subtitle_y=0.91, wrap_width=92)
    add_source(fig, x=0.06, y=0.025)

    fig.subplots_adjust(top=0.78, bottom=0.18, left=0.09, right=0.97,
                        wspace=0.12)

    out = OUT_DIR / "chart_v14_premium_tea_per_brand.pdf"
    fig.savefig(out, dpi=300)
    plt.close(fig)
    return out


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    print()
    print("Generating v0.14 chart suite...")
    print(f"  Output: {OUT_DIR}")
    print()
    p1 = chart_regime4_canonical()
    print(f"  HEADLINE  {p1.name}")
    p2 = chart_per_category_rho_comparison()
    print(f"  per_cat   {p2.name}")
    p3 = chart_primary_vs_sensitivity()
    print(f"  sensit    {p3.name}")
    p4 = chart_premium_tea_per_brand()
    print(f"  per_brand {p4.name}")
    print()
    print("v0.14 chart build complete.")
