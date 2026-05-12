"""v0.13 chart generation for the brand-format report and SSRN paper.

Produces four PDF charts visualising the v0.13 five-category construct-validity
expansion's findings: H7 falsification surfacing a fourth empirical regime; H8
Mint phantom-persistence canonical confirmation; per-category construct-
validity heterogeneity; pooled cross-category rank-alignment.

Follows the v0.12 chart conventions (Third System brand spec 1.4):
  - Akkurat Pro + STIX mathtext, pdf.fonttype=42
  - Tier-coloring for brand-level points (Indigo / Petro / Copper Plate)
  - 6-column page grid figsizes (7.5" wide hero / hero_tall / spread)
  - Title 13pt bold + subtitle 9.5pt muted + source 7.5pt italic muted
  - adjustText with graceful fallback for brand-label collision avoidance
  - 300 DPI vector PDF output with savefig pad_inches=0.15

One deliberate convention deviation:
  - The four-regime scatter (chart 1) plots one point per CATEGORY, not per
    brand. Tier-coloring does not apply at the category level. Points are
    colored by H7 regime classification (Indigo=Regime 1, Petro=Regime 2,
    Copper Plate=Regime 4 provisional, Muted=Regime 3 descriptive). The
    deviation is documented in the chart's subtitle.

Charts produced (output filenames mirror v0.12 convention):
  chart_v13_h7_fourregime_classification.pdf  (HEADLINE — H7 finding)
  chart_v13_per_category_rho_comparison.pdf   (5-cat construct-validity)
  chart_v13_h8_mint_phantom.pdf               (H8 canonical confirmation)
  chart_v13_pooled_rank_scatter.pdf           (cross-category pooled ρ)

Run:
    pip install adjustText   # one-time, if not installed
    python3 ~/aias/scripts/build_charts_v13.py
"""
import json
import textwrap
from pathlib import Path

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import rcParams
from matplotlib.patches import Rectangle, FancyBboxPatch
from matplotlib.lines import Line2D
from scipy import stats

try:
    from adjustText import adjust_text
    HAVE_ADJUST_TEXT = True
except ImportError:
    HAVE_ADJUST_TEXT = False

# ============================================================================
# Brand constants (mirrors build_charts_v12.py)
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
PASS_GREEN   = "#2E7D32"   # v0.12 convention for satisfied/PASS callouts

TIER_COLOR = {
    "incumbent":  INDIGO,
    "mid-tier":   PETRO,
    "challenger": COPPER_PLATE,
}

# Regime palette for the four-regime scatter (chart 1 only — see docstring)
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
PAIRED   = V13_ROOT / "analysis" / "per_brand_paired.csv"
SCORING  = V13_ROOT / "analysis" / "canonical_scoring.json"
OUT_DIR  = V13_ROOT / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

paired = pd.read_csv(PAIRED)
with SCORING.open() as f:
    scoring = json.load(f)

for col in paired.columns:
    if any(tok in col for tok in ["eligible", "sparse", "excluded",
                                    "is_pivot", "is_phantom"]):
        paired[col] = paired[col].apply(
            lambda x: str(x).strip().lower() == "true" if pd.notna(x) else False
        )

SOURCE_LINE = ("Source: Third System AI Presence Index v0.13 · "
               "Google Trends acquisition 2026-05-11T21:45:28Z · "
               "Pre-reg locked at v0.13-prereg (commit 1a6294d).")

CATEGORY_LABELS = {
    "pmsoftware": "Project management software",
    "running":    "Premium running shoes",
    "oliveoil":   "Premium olive oil",
    "skincare":   "Premium facial skincare",
    "finance":    "Personal finance apps",
}

CATEGORY_SHORT = {
    "pmsoftware": "PM software",
    "running":    "Running shoes",
    "oliveoil":   "Olive oil",
    "skincare":   "Skincare",
    "finance":    "Finance apps",
}

CATEGORY_PIVOT = {
    "pmsoftware": "Asana",
    "running":    "Asics",
    "oliveoil":   "California Olive Ranch",
    "skincare":   "CeraVe",
    "finance":    "YNAB",
}

# H7 regime classifications drawn directly from canonical scoring output
CATEGORY_REGIME = {
    "pmsoftware": "Regime 1",
    "running":    "Regime 2",
    "oliveoil":   "Regime 3",  # descriptive-only per §3.6a
    "skincare":   "Regime 4",  # provisional, unclassifiable vs pre-reg taxonomy
    "finance":    "Regime 4",
}


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
# CHART 1: H7 four-regime classification scatter (HEADLINE)
# ============================================================================

def chart_h7_fourregime_classification():
    """Headline v0.13 chart.

    Plots each category in (bivariate ρ × decrement) space. Three regimes
    are pre-registered (background zones); two new categories (skincare,
    finance) fall outside all three, defining a provisional fourth regime.
    Each category point is colored by its H7 classification — a category-
    level deviation from the brand-level tier-coloring convention.
    """
    fig, ax = plt.subplots(figsize=(7.5, 6.5))

    # ---- Background regime zones --------------------------------------------
    # Regime 1: ρ ∈ [0.35, 0.65], decrement ≤ 0.15
    ax.add_patch(Rectangle((0.35, -0.20), 0.30, 0.35,
                            facecolor=INDIGO, alpha=0.07,
                            edgecolor=INDIGO, linewidth=0.6,
                            linestyle="--", zorder=1))
    # Regime 2: ρ > 0.65, decrement > 0.25
    ax.add_patch(Rectangle((0.65, 0.25), 0.30, 0.40,
                            facecolor=PETRO, alpha=0.10,
                            edgecolor=PETRO, linewidth=0.6,
                            linestyle="--", zorder=1))
    # Regime 4 (provisional): ρ ∈ [-0.10, 0.35], decrement ∈ [0.25, 0.55]
    ax.add_patch(Rectangle((-0.10, 0.25), 0.45, 0.40,
                            facecolor=COPPER_PLATE, alpha=0.08,
                            edgecolor=COPPER_PLATE, linewidth=0.6,
                            linestyle="--", zorder=1))

    # ---- Threshold reference lines ------------------------------------------
    for x_th in (0.35, 0.65):
        ax.axvline(x_th, color=GRID, linewidth=0.5, linestyle=":", zorder=1)
    for y_th in (0.15, 0.25):
        ax.axhline(y_th, color=GRID, linewidth=0.5, linestyle=":", zorder=1)
    ax.axhline(0.0, color=GRID_SUBTLE, linewidth=0.4, zorder=1)

    # ---- Regime zone labels (in-zone text) ----------------------------------
    ax.text(0.50, -0.10, "Regime 1\nMarginal direct",
            ha="center", va="center", fontsize=8, color=INDIGO,
            style="italic", zorder=2)
    ax.text(0.80, 0.55, "Regime 2\nAge-mediated strong",
            ha="center", va="center", fontsize=8, color=PETRO,
            style="italic", zorder=2)
    ax.text(0.10, 0.55, "Regime 4 (provisional)\nCovariate-saturated weak",
            ha="center", va="center", fontsize=8, color=COPPER_PLATE,
            style="italic", zorder=2)

    # ---- Plot category points -----------------------------------------------
    texts = []
    for cat, res in scoring["per_category"].items():
        if cat == "oliveoil":
            continue  # descriptive-only, annotated separately
        rho_t1  = res["correlations"]["ww_t1"]["spearman_rho"]
        rho_t2  = res["correlations"]["ww_t2"]["spearman_rho"]
        prho_t1 = res["correlations"]["ww_t1"]["partial_spearman_rho"]
        prho_t2 = res["correlations"]["ww_t2"]["partial_spearman_rho"]
        dec_t1 = rho_t1 - prho_t1
        dec_t2 = rho_t2 - prho_t2
        color  = REGIME_COLOR[CATEGORY_REGIME[cat]]

        # Connector line t1 → t2
        ax.plot([rho_t1, rho_t2], [dec_t1, dec_t2],
                color=color, alpha=0.55, linewidth=1.2, zorder=3)
        # t1: open marker
        ax.scatter([rho_t1], [dec_t1], s=90, facecolor="white",
                   edgecolor=color, linewidth=2.0, zorder=4)
        # t2: filled marker
        ax.scatter([rho_t2], [dec_t2], s=90, facecolor=color,
                   edgecolor=color, linewidth=1.0, zorder=4)

        # Place a single label at the t2 (filled) position
        t = ax.text(rho_t2, dec_t2, "  " + CATEGORY_SHORT[cat],
                    fontsize=9.5, color=TEXT, weight="bold",
                    ha="left", va="center", zorder=5)
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

    # ---- Legend (t1 / t2 markers) ------------------------------------------
    legend_elements = [
        Line2D([0], [0], marker="o", color="w", markerfacecolor="white",
               markeredgecolor=TEXT, markeredgewidth=1.8, markersize=9,
               label="t₁ (29 April 2026)"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor=TEXT,
               markeredgecolor=TEXT, markersize=9,
               label="t₂ (7 May 2026)"),
    ]
    ax.legend(handles=legend_elements, loc="lower right",
              frameon=False, fontsize=8.5)

    # ---- Axes ---------------------------------------------------------------
    ax.set_xlim(-0.15, 0.95)
    ax.set_ylim(-0.20, 0.65)
    ax.set_xlabel(r"Bivariate Spearman $\rho$ (AI Presence × Trends, Worldwide)",
                  color=TEXT)
    ax.set_ylabel("Covariate decrement (bivariate " + r"$\rho$" +
                  " − partial " + r"$\rho$" + ", after age + tier control)",
                  color=TEXT)
    ax.grid(True, axis="both", color=GRID_SUBTLE, linewidth=0.4, zorder=0)

    # ---- Title / subtitle / source -----------------------------------------
    title = "H7 — Four-regime classification of v0.13 categories"
    subtitle = ("Each category at bivariate ρ × covariate decrement. Three "
                "regimes pre-registered (background zones); skincare and "
                "finance fall outside all three, defining a provisional fourth "
                "pattern (Covariate-saturated weak). Olive oil routes to Regime 3 "
                "descriptive-only per §3.6a (n=8, below n=10 floor) and is not "
                "plotted. Points colored by H7 classification.")
    draw_title_and_subtitle(fig, title, subtitle, x=0.06,
                            title_y=0.96, subtitle_y=0.92, wrap_width=92)
    add_source(fig, x=0.06, y=0.025)

    fig.subplots_adjust(top=0.82, bottom=0.12, left=0.10, right=0.96)

    out = OUT_DIR / "chart_v13_h7_fourregime_classification.pdf"
    fig.savefig(out, dpi=300)
    plt.close(fig)
    return out


# ============================================================================
# CHART 2: Per-category bivariate, partial, US ρ comparison
# ============================================================================

def chart_per_category_rho_comparison():
    """Five categories × three indicator series (bivariate WW ρ, partial WW ρ,
    US ρ for sensitivity), each at t1 (open) and t2 (filled). Shows that the
    per-category construct-validity outcomes diverge structurally across the
    panel — drives the four-regime conclusion.
    """
    cats = ["pmsoftware", "oliveoil", "running", "skincare", "finance"]
    fig, ax = plt.subplots(figsize=(7.5, 6.5))

    y_positions = np.arange(len(cats))[::-1]
    row_height = 0.18

    for i, cat in enumerate(cats):
        y = y_positions[i]
        res = scoring["per_category"][cat]
        rho_ww_t1   = res["correlations"]["ww_t1"]["spearman_rho"]
        rho_ww_t2   = res["correlations"]["ww_t2"]["spearman_rho"]
        prho_ww_t1  = res["correlations"]["ww_t1"]["partial_spearman_rho"]
        prho_ww_t2  = res["correlations"]["ww_t2"]["partial_spearman_rho"]
        rho_us_t1   = res["correlations"]["us_t1"]["spearman_rho"]
        rho_us_t2   = res["correlations"]["us_t2"]["spearman_rho"]

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

    # Legend at bottom (below x-axis label, with enough clearance)
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
              bbox_to_anchor=(0.5, -0.24), ncol=2,
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

    # Title / subtitle / source
    title = "Per-category construct validity — bivariate, partial, US sensitivity"
    subtitle = ("Bivariate WW ρ (indigo) measures the AI Presence × Trends "
                "rank co-movement. Partial WW ρ (petro) controls for brand "
                "age and tier. Bivariate US ρ (grey) is the US-region "
                "sensitivity. Open markers = t₁; filled = t₂.")
    draw_title_and_subtitle(fig, title, subtitle, x=0.06,
                            title_y=0.96, subtitle_y=0.92, wrap_width=92)
    add_source(fig, x=0.06, y=0.025)

    fig.subplots_adjust(top=0.84, bottom=0.20, left=0.32, right=0.92)

    out = OUT_DIR / "chart_v13_per_category_rho_comparison.pdf"
    fig.savefig(out, dpi=300)
    plt.close(fig)
    return out


# ============================================================================
# CHART 3: H8 Mint phantom-persistence canonical confirmation
# ============================================================================

def chart_h8_mint_phantom():
    """H8 canonical confirmation visualization. Two-panel layout: left shows
    Mint's AI Presence vs Trends magnitudes at both waves; right shows the
    three pre-registered conditions and their satisfaction status.
    """
    h8 = scoring["cross_category"]["H8"]
    ai_t1 = h8["condition_1_ai_above_5pct"]["ai_t1_pct"]
    ai_t2 = h8["condition_1_ai_above_5pct"]["ai_t2_pct"]
    ai_rank_t1 = h8["condition_2_ai_top5"]["rank_t1"]
    ai_rank_t2 = h8["condition_2_ai_top5"]["rank_t2"]

    fig, (ax_left, ax_right) = plt.subplots(
        1, 2, figsize=(7.5, 5.5),
        gridspec_kw={"width_ratios": [1.0, 1.1]})

    # ---- LEFT: AI Presence vs Trends magnitude bars ------------------------
    metrics = ["AI Presence t₂", "AI Presence t₁",
               "Trends mean t₂",  "Trends mean t₁"]
    values  = [ai_t2, ai_t1, 0.0, 0.0]
    colors  = [INDIGO, INDIGO, MUTED, MUTED]
    y_pos = np.arange(len(metrics))

    ax_left.barh(y_pos, values, color=colors, height=0.55,
                 edgecolor="none", zorder=3)

    for i, (m, v) in enumerate(zip(metrics, values)):
        if v > 0:
            ax_left.text(v + 1.5, i, f"{v:.1f}%", fontsize=8.5,
                         color=TEXT, va="center", ha="left", weight="bold")
        else:
            ax_left.text(2.0, i, "below E1b display threshold",
                         fontsize=7.5, color=MUTED, va="center",
                         ha="left", style="italic")

    # 5% floor reference (C1)
    ax_left.axvline(5.0, color=COPPER_PLATE, linewidth=0.6,
                    linestyle=":", zorder=2)
    ax_left.text(5.0, len(metrics) - 0.35, "C1 floor (5%)",
                 fontsize=7, color=COPPER_PLATE, ha="center",
                 va="bottom", style="italic")

    ax_left.set_yticks(y_pos)
    ax_left.set_yticklabels(metrics, fontsize=9)
    ax_left.set_xlim(0, 55)
    ax_left.set_xlabel("Magnitude (% for AI Presence; rescaled mean for Trends)",
                       fontsize=8.5, color=TEXT)
    ax_left.spines["left"].set_visible(False)
    ax_left.spines["bottom"].set_color(MUTED)
    ax_left.tick_params(axis="y", length=0)
    ax_left.grid(True, axis="x", color=GRID_SUBTLE, linewidth=0.4, zorder=0)

    # ---- RIGHT: Three condition rows ---------------------------------------
    ax_right.axis("off")

    conditions = [
        ("C1", "AI Presence ≥ 5% at both waves",
         f"t₁: {ai_t1:.1f}%   ·   t₂: {ai_t2:.1f}%"),
        ("C2", "AI rank in top-5 at both waves",
         f"t₁: rank {ai_rank_t1}   ·   t₂: rank {ai_rank_t2}"),
        ("C3", "NOT Trends top-5 at either wave",
         "Mint not E1b-eligible at either wave;\ntrivially satisfied per §11"),
    ]

    # H8 verdict header — single line, no overlap
    ax_right.text(0.05, 0.95, "H8 verdict",
                  fontsize=8.5, color=MUTED, ha="left", va="top",
                  transform=ax_right.transAxes)
    ax_right.text(0.05, 0.88, "CONFIRMED",
                  fontsize=15, color=INDIGO, weight="bold",
                  ha="left", va="top", transform=ax_right.transAxes)
    # Horizontal rule
    ax_right.plot([0.05, 0.95], [0.78, 0.78],
                  color=GRID, linewidth=0.5, transform=ax_right.transAxes,
                  clip_on=False)

    # Condition rows
    row_height = 0.21
    y_base = 0.70
    for i, (tag, label, detail) in enumerate(conditions):
        y = y_base - i * row_height
        # Tag pill (small rounded rect with tag inside)
        pill = FancyBboxPatch((0.05, y - 0.060), 0.07, 0.075,
                              boxstyle="round,pad=0.012",
                              facecolor=COPPER_PLATE, edgecolor="none",
                              transform=ax_right.transAxes, clip_on=False,
                              zorder=4)
        ax_right.add_patch(pill)
        ax_right.text(0.085, y - 0.022, tag, fontsize=9,
                      color="white", weight="bold", ha="center", va="center",
                      transform=ax_right.transAxes, zorder=5)
        # Condition label
        ax_right.text(0.16, y - 0.005, label, fontsize=9.5, color=TEXT,
                      weight="bold", ha="left", va="top",
                      transform=ax_right.transAxes)
        # Detail (muted)
        ax_right.text(0.16, y - 0.060, detail, fontsize=8, color=MUTED,
                      ha="left", va="top", transform=ax_right.transAxes,
                      style="italic")
        # Status checkmark (filled circle in COPPER_PLATE — satisfied)
        ax_right.scatter([0.93], [y - 0.025], s=140, color=COPPER_PLATE,
                         edgecolor="white", linewidth=1.0,
                         transform=ax_right.transAxes, clip_on=False, zorder=4)

    # Footer note
    ax_right.text(0.05, 0.04, "All three conditions satisfied → H8 CONFIRMED",
                  fontsize=7.5, color=MUTED, style="italic",
                  ha="left", va="bottom", transform=ax_right.transAxes)

    # ---- Title / subtitle / source ----------------------------------------
    title = "H8 — Mint phantom-persistence canonical confirmation"
    subtitle = ("Mint (Intuit, shutdown Sept 2025) retains substantial AI "
                "Presence with no Trends signal at both v0.13 measurement "
                "waves. All three pre-registered conditions hold; this is "
                "the cleanest phantom-persistence anchor in the programme to date.")
    draw_title_and_subtitle(fig, title, subtitle, x=0.06,
                            title_y=0.96, subtitle_y=0.91, wrap_width=92)
    add_source(fig, x=0.06, y=0.025)

    fig.subplots_adjust(top=0.74, bottom=0.13, left=0.16, right=0.97,
                        wspace=0.22)

    out = OUT_DIR / "chart_v13_h8_mint_phantom.pdf"
    fig.savefig(out, dpi=300)
    plt.close(fig)
    return out


# ============================================================================
# CHART 4: Pooled cross-category rank scatter
# ============================================================================

def chart_pooled_rank_scatter():
    """Two-panel pooled rank scatter (t₁ left, t₂ right). Brands plotted at
    rank-within-category positions; tier-colored per v0.12 convention.
    Pooled ρ annotated in each panel.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.5, 5.5),
                                    sharey=True)

    max_rank_overall = 0
    for ax, wave in zip([ax1, ax2], ("t1", "t2")):
        for cat in ["pmsoftware", "running", "skincare", "finance"]:
            cat_df = paired[(paired["category"] == cat) &
                            (~paired["e1a_excluded"])].copy()
            elig = cat_df[cat_df[f"trends_ww_{wave}_eligible"]].copy()
            elig = elig.dropna(subset=[f"trends_ww_{wave}_mean",
                                        f"ai_{wave}_pct"])
            if len(elig) < 2:
                continue
            elig["ai_rank"]     = stats.rankdata(elig[f"ai_{wave}_pct"])
            elig["trends_rank"] = stats.rankdata(elig[f"trends_ww_{wave}_mean"])
            max_rank_overall = max(max_rank_overall,
                                    elig["ai_rank"].max(),
                                    elig["trends_rank"].max())

            for tier in ("incumbent", "mid-tier", "challenger"):
                sub = elig[elig["market_tier"] == tier]
                if len(sub) == 0:
                    continue
                ax.scatter(sub["ai_rank"], sub["trends_rank"],
                           color=TIER_COLOR[tier], s=55, alpha=0.85,
                           edgecolor="white", linewidth=0.8, zorder=3,
                           label=tier.capitalize() if (ax is ax1 and
                                                       cat == "pmsoftware") else None)

        # Diagonal reference
        ax.plot([1, max_rank_overall + 1], [1, max_rank_overall + 1],
                color=GRID, linestyle=":", linewidth=0.7, zorder=1)

        # Pooled ρ callout
        pooled = scoring["pooled_sensitivity"][wave]
        rho = pooled["rho"]
        p   = pooled["p_two_tailed"]
        n   = pooled["n"]
        wave_label = "t₁ (29 April 2026)" if wave == "t1" else "t₂ (7 May 2026)"
        callout = (f"{wave_label}\n"
                   r"Pooled $\rho$ = " + f"{rho:.3f}\n"
                   f"n = {n}    p = {p:.4f}")
        ax.text(0.04, 0.96, callout,
                transform=ax.transAxes, fontsize=8.5, color=TEXT,
                ha="left", va="top", weight="bold",
                bbox=dict(facecolor="white", edgecolor=GRID,
                          boxstyle="round,pad=0.5", linewidth=0.5))

        ax.set_xlabel("AI Presence rank (within category)", color=TEXT)
        if wave == "t1":
            ax.set_ylabel("Trends rank (within category)", color=TEXT)
        ax.grid(True, color=GRID_SUBTLE, linewidth=0.4, zorder=0)

    # Shared tier legend at bottom
    ax1.legend(loc="lower center", bbox_to_anchor=(1.10, -0.22),
               ncol=3, frameon=False, fontsize=8.5,
               handletextpad=0.4, columnspacing=2.5)

    # Title / subtitle / source
    title = "Pooled cross-category rank alignment"
    subtitle = ("Rank-within-category, stacked across the four confirmatory "
                "categories (PM software, running, skincare, finance). "
                "Despite heterogeneous within-category outcomes, the pooled "
                "rank-order alignment is moderately strong and stable across waves.")
    draw_title_and_subtitle(fig, title, subtitle, x=0.06,
                            title_y=0.96, subtitle_y=0.92, wrap_width=92)
    add_source(fig, x=0.06, y=0.025)

    fig.subplots_adjust(top=0.78, bottom=0.17, left=0.09, right=0.97,
                        wspace=0.12)

    out = OUT_DIR / "chart_v13_pooled_rank_scatter.pdf"
    fig.savefig(out, dpi=300)
    plt.close(fig)
    return out


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    print()
    print("Generating v0.13 chart suite...")
    print(f"  Output: {OUT_DIR}")
    print()
    p1 = chart_h7_fourregime_classification()
    print(f"  HEADLINE  {p1.name}")
    p2 = chart_per_category_rho_comparison()
    print(f"  per_cat   {p2.name}")
    p3 = chart_h8_mint_phantom()
    print(f"  H8        {p3.name}")
    p4 = chart_pooled_rank_scatter()
    print(f"  pooled    {p4.name}")
    print()
    print("v0.13 chart build complete.")
