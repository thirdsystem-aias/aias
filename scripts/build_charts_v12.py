"""v0.12 chart generation for the brand-format report and SSRN paper.

Produces PDF charts visualising the v0.12 three-category construct-validity
expansion's headline finding: three distinct empirical regimes of the
AI Availability / Mental Availability relationship across categories.

Charts (locked figsizes per Third System brand spec):

  HEADLINE — Cross-category comparison
    F1, F2  — Cross-category H1 scatter, t1 / t2 (3-panel: PM | Running | Olive)

  REPLICATION — PM software (v0.11 replicates)
    F3, F4  — PM rank-shift slope, t1 / t2
    F5, F6  — PM partial residual (H4), t1 / t2

  NEW FINDING — Running shoes (strong ρ + asymmetric boundary mismatch)
    F7, F8  — Running rank-shift slope, t1 / t2
    F9, F10 — Running partial residual (H4 — age mediation), t1 / t2

  H6 DIAGNOSTICS — Linear-style / Todoist-style zones
    F11, F12 — H6 zone panel (PM + Running 2-up), t1 / t2

  CATEGORY-SCALE MISMATCH — Olive oil (descriptive arm)
    F13 — Scale-Mismatch matched-subset bar viz with Trends-state markers

Tie-break convention for rank-shift charts:
  - ai_rank breaks ties on AI Presence by trends_mean (desc).
  - trends_rank breaks ties on Trends by ai_pct (desc).
  Each brand thus gets a unique rank in each dimension.

Optional dependency: adjustText. Falls back to fixed offsets if absent.

Run:
    pip install adjustText   # one-time, if not installed
    python scripts/build_charts_v12.py
"""
import json
from pathlib import Path

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import rcParams
from matplotlib.patches import Rectangle
from scipy import stats

try:
    from adjustText import adjust_text
    HAVE_ADJUST_TEXT = True
except ImportError:
    HAVE_ADJUST_TEXT = False

# ============================================================================
# Brand constants
# ============================================================================

INDIGO       = "#37237B"
PETRO        = "#6A6AB1"
COPPER_PLATE = "#F36C35"
TEXT         = "#231F20"
MUTED        = "#6B6967"
GRID         = "#CCCCCC"
GRID_SUBTLE  = "#E5E5E5"
ZONE_FILL    = "#F36C35"  # Copper plate, low alpha for H6 zones

TIER_COLOR = {
    "incumbent": INDIGO,
    "mid-tier":  PETRO,
    "challenger": COPPER_PLATE,
}

# Below-display-threshold y-coordinate for E1a brands in cross-category scatter
BELOW_THRESH_Y = 0.3


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
rcParams["xtick.labelsize"]   = 9
rcParams["ytick.labelsize"]   = 9
rcParams["axes.labelsize"]    = 10
rcParams["axes.titlesize"]    = 12
rcParams["axes.spines.top"]   = False
rcParams["axes.spines.right"] = False
rcParams["pdf.fonttype"]      = 42


# ============================================================================
# Paths and data
# ============================================================================

V12_ROOT = Path.home() / "aias" / "osf" / "v12"
PAIRED   = V12_ROOT / "analysis" / "per_brand_paired.csv"
SCORING  = V12_ROOT / "analysis" / "canonical_scoring.json"
SCALE_MISMATCH = V12_ROOT / "analysis" / "category_scale_mismatch_table.csv"
OUT_DIR  = V12_ROOT / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

paired = pd.read_csv(PAIRED)
mismatch_df = pd.read_csv(SCALE_MISMATCH)
with SCORING.open() as f:
    scoring = json.load(f)

# Coerce boolean columns that pandas may read as object dtype
for col in paired.columns:
    if any(tok in col for tok in ["eligible", "sparse", "excluded", "is_pivot"]):
        paired[col] = paired[col].apply(
            lambda x: str(x).strip().lower() == "true" if pd.notna(x) else False
        )

SOURCE_LINE = ("Source: Third System AI Presence Index v0.12 · "
               "Google Trends acquisition 2026-05-11T10:33:22Z · "
               "Pre-reg locked at v0.12-prereg (commit ae4bd3a).")

CATEGORY_LABELS = {
    "pmsoftware": "Project management software",
    "running": "Premium running shoes",
    "oliveoil": "Premium olive oil",
}

CATEGORY_PIVOT = {
    "pmsoftware": "Asana",
    "running": "Asics",
    "oliveoil": "California Olive Ranch",
}


def draw_title_and_subtitle(fig, title, subtitle, x=0.06, title_y=0.96, subtitle_y=0.91):
    fig.text(x, title_y, title, ha="left", va="top",
             fontsize=13, color=TEXT, weight="bold")
    fig.text(x, subtitle_y, subtitle, ha="left", va="top",
             fontsize=9.5, color=MUTED)


def add_source(fig, x=0.06, y=0.025):
    fig.text(x, y, SOURCE_LINE, ha="left", va="top",
             fontsize=7.5, color=MUTED, style="italic")


def get_cat_paired(cat):
    """Return paired data for one category (excludes E1a unless flagged)."""
    return paired[paired["category"] == cat].copy()


# ============================================================================
# F1 / F2: Cross-category scatter (3-panel headline)
# ============================================================================

def chart_cross_category_scatter(wave):
    fig, axes = plt.subplots(1, 3, figsize=(11.0, 5.0))

    # Panels: PM | Running | Olive
    categories = ["pmsoftware", "running", "oliveoil"]

    # Compute global y-axis log range from all data so panels share scale
    all_trends_vals = []
    for cat in categories:
        df_cat = get_cat_paired(cat)
        elig = df_cat[df_cat[f"trends_ww_{wave}_eligible"] & (~df_cat["e1a_excluded"])]
        v = elig[f"trends_ww_{wave}_mean"].dropna()
        v = v[v > 0]
        all_trends_vals.extend(v.tolist())

    y_min = max(0.5, min(all_trends_vals) * 0.5) if all_trends_vals else 1
    y_max = max(all_trends_vals) * 2.0 if all_trends_vals else 1000

    for ax, cat in zip(axes, categories):
        cat_label = CATEGORY_LABELS[cat]
        pivot_name = CATEGORY_PIVOT[cat]
        df_cat = get_cat_paired(cat)

        ax.grid(True, which="both", color=GRID_SUBTLE, linewidth=0.5, zorder=0)

        # Eligible non-E1a brands as scatter points
        elig = df_cat[df_cat[f"trends_ww_{wave}_eligible"] & (~df_cat["e1a_excluded"])].copy()
        elig = elig.dropna(subset=[f"trends_ww_{wave}_mean", f"ai_{wave}_pct"])

        for tier in ("incumbent", "mid-tier", "challenger"):
            sub = elig[elig["market_tier"] == tier]
            ax.scatter(sub[f"ai_{wave}_pct"], sub[f"trends_ww_{wave}_mean"],
                       color=TIER_COLOR[tier], s=70, alpha=0.9,
                       edgecolor="white", linewidth=1.0, zorder=3,
                       label=tier.capitalize() if ax is axes[0] else None)

        # For olive oil only: plot E1a-excluded brands at a below-threshold y-level
        if cat == "oliveoil":
            ax.axhline(BELOW_THRESH_Y * 2.5, color=MUTED, linewidth=0.5,
                       linestyle="--", alpha=0.5, zorder=1)
            ax.text(99, BELOW_THRESH_Y * 2.5, "  ↓ below display threshold",
                    fontsize=7, color=MUTED, ha="right", va="bottom", style="italic")
            e1a_brands = df_cat[df_cat["e1a_excluded"]].copy()
            for tier in ("incumbent", "mid-tier", "challenger"):
                sub = e1a_brands[e1a_brands["market_tier"] == tier]
                if len(sub) > 0:
                    ax.scatter(sub[f"ai_{wave}_pct"], [BELOW_THRESH_Y] * len(sub),
                               marker="x", color=TIER_COLOR[tier], s=60,
                               linewidth=1.5, zorder=3)

        # Brand labels (eligible PASS + E1a)
        texts = []
        for _, row in elig.iterrows():
            t = ax.text(row[f"ai_{wave}_pct"], row[f"trends_ww_{wave}_mean"],
                        row["brand"], fontsize=7, color=TEXT,
                        ha="left", va="center", zorder=5)
            texts.append(t)
        if cat == "oliveoil":
            e1a_brands = df_cat[df_cat["e1a_excluded"]]
            for _, row in e1a_brands.iterrows():
                t = ax.text(row[f"ai_{wave}_pct"], BELOW_THRESH_Y,
                            row["brand"], fontsize=7, color=TEXT,
                            ha="left", va="center", zorder=5)
                texts.append(t)

        if HAVE_ADJUST_TEXT and texts:
            adjust_text(
                texts, ax=ax,
                arrowprops=dict(arrowstyle="-", color=GRID, lw=0.4),
                expand=(1.05, 1.2),
                force_text=(0.3, 0.5),
                force_static=(0.15, 0.25),
                max_move=(15, 25),
                iter_lim=150,
            )

        ax.set_yscale("log")
        ax.set_xlim(-3, 100)
        ax.set_ylim(y_min, y_max)
        ax.set_xlabel("AI Presence rate (%)", color=TEXT, fontsize=9)
        if ax is axes[0]:
            ax.set_ylabel(f"Trends rescaled mean (log; pivot ≡ 100)",
                          color=TEXT, fontsize=9)

        # Per-category subtitle with ρ
        cat_results = scoring["per_category"][cat]
        if cat_results["descriptive_only"]:
            corr = cat_results["correlations"][f"ww_{wave}"]
            n = corr["n"]
            rho = corr["spearman_rho"]
            if rho is not None:
                ax_subtitle = f"{cat_label}\nn={n} (PASS subset); ρ={rho:.2f} (descriptive)"
            else:
                ax_subtitle = f"{cat_label}\n(descriptive-only)"
        else:
            corr = cat_results["correlations"][f"ww_{wave}"]
            n = corr["n"]
            rho = corr["spearman_rho"]
            p1t = corr["spearman_p_one_tailed"]
            ax_subtitle = f"{cat_label}\nn={n}; ρ={rho:.3f}, p₁ₜ={p1t:.3g}"
        ax.set_title(ax_subtitle, color=TEXT, fontsize=10, loc="left", pad=8)

    # Shared legend
    axes[0].legend(loc="lower right", frameon=False, fontsize=8)

    # Overall figure title
    title_wave = "t₁" if wave == "t1" else "t₂"
    fig_title = (f"H1 — AI Presence × Google Trends across three categories, "
                 f"{title_wave} (Worldwide)")
    fig_subtitle = ("Three distinct empirical regimes: marginal correlation with "
                    "bidirectional boundary mismatch (PM software); strong correlation "
                    "with age-mediated structure (running shoes); scale mismatch — "
                    "many brands AI-present, Trends-undetectable (olive oil).")
    draw_title_and_subtitle(fig, fig_title, fig_subtitle, x=0.03)
    add_source(fig, x=0.03)

    fig.subplots_adjust(top=0.78, bottom=0.13, left=0.06, right=0.98, wspace=0.25)

    out = OUT_DIR / f"chart_v12_h1_cross_category_scatter_{wave}.pdf"
    fig.savefig(out, dpi=300)
    plt.close(fig)
    return out


# ============================================================================
# F3-F8: Per-category single scatter (still useful for per-cat narrative)
# ============================================================================
# Skipped — covered by cross-category panel. Per-cat detail handled via
# rank-shift (boundary mismatch) and partial residual (covariate structure).


# ============================================================================
# Per-category rank-shift slope chart
# ============================================================================

def chart_rank_shift(cat, wave):
    df_cat = get_cat_paired(cat)
    df = df_cat[df_cat[f"trends_ww_{wave}_eligible"] & (~df_cat["e1a_excluded"])].copy()
    df = df.dropna(subset=[f"trends_ww_{wave}_mean", f"ai_{wave}_pct"]).copy()

    ai_sorted = df.sort_values(
        [f"ai_{wave}_pct", f"trends_ww_{wave}_mean"], ascending=[False, False]
    ).reset_index(drop=True)
    ai_rank_map = dict(zip(ai_sorted["brand"], ai_sorted.index + 1))

    tr_sorted = df.sort_values(
        [f"trends_ww_{wave}_mean", f"ai_{wave}_pct"], ascending=[False, False]
    ).reset_index(drop=True)
    trends_rank_map = dict(zip(tr_sorted["brand"], tr_sorted.index + 1))

    df["ai_rank"] = df["brand"].map(ai_rank_map)
    df["trends_rank"] = df["brand"].map(trends_rank_map)
    df["abs_diff"] = (df["trends_rank"] - df["ai_rank"]).abs()
    n = len(df)
    extreme_threshold = max(5, int(n * 0.35))  # adaptive: ~35% of n

    fig, ax = plt.subplots(figsize=(7.5, max(5.5, 0.45 * n + 2)))
    x_left, x_right = 0.0, 1.0

    for _, row in df.sort_values("abs_diff").iterrows():
        y_ai = -row["ai_rank"]
        y_trends = -row["trends_rank"]
        color = TIER_COLOR.get(row["market_tier"], MUTED)
        is_extreme = row["abs_diff"] >= extreme_threshold
        lw = 2.2 if is_extreme else 1.0
        alpha = 0.95 if is_extreme else 0.5
        line_color = COPPER_PLATE if is_extreme else color
        ax.plot([x_left, x_right], [y_ai, y_trends],
                color=line_color, alpha=alpha, linewidth=lw,
                zorder=4 if is_extreme else 2)

    for _, row in df.iterrows():
        y_ai = -row["ai_rank"]
        y_trends = -row["trends_rank"]
        color = TIER_COLOR.get(row["market_tier"], MUTED)
        ax.scatter([x_left], [y_ai], color=color, s=55, zorder=5,
                   edgecolor="white", linewidth=1.0)
        ax.scatter([x_right], [y_trends], color=color, s=55, zorder=5,
                   edgecolor="white", linewidth=1.0)
        ax.text(x_left - 0.03, y_ai, row["brand"],
                ha="right", va="center", fontsize=9, color=TEXT)
        ax.text(x_right + 0.03, y_trends, row["brand"],
                ha="left", va="center", fontsize=9, color=TEXT)

    header_y = 0.2
    ax.text(x_left, header_y, "AI Presence rank",
            ha="center", va="bottom", fontsize=11, color=TEXT, weight="bold")
    ax.text(x_right, header_y, "Trends rank",
            ha="center", va="bottom", fontsize=11, color=TEXT, weight="bold")

    ax.set_xlim(-0.45, 1.45)
    ax.set_ylim(-(n + 0.8), 1.0)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])

    for tier in ("incumbent", "mid-tier", "challenger"):
        ax.scatter([], [], color=TIER_COLOR[tier], s=55,
                   label=tier.capitalize())
    ax.plot([], [], color=COPPER_PLATE, linewidth=2.2,
            label=f"Extreme divergence (|Δrank| ≥ {extreme_threshold})")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.05),
              ncol=4, frameon=False, fontsize=9)

    title_wave = "t₁" if wave == "t1" else "t₂"
    cat_label = CATEGORY_LABELS[cat]
    title = f"H3 — AI Presence rank vs Trends rank ({cat_label}, {title_wave})"
    subtitle = ("Lines connect each brand's rank by AI Presence (left) to its "
                "rank by Trends (right). Steep slopes = construct divergence. "
                "Ties broken by the other variable.")
    draw_title_and_subtitle(fig, title, subtitle)
    add_source(fig)
    fig.subplots_adjust(top=0.86, bottom=0.08, left=0.02, right=0.98)

    out = OUT_DIR / f"chart_v12_h3_rank_shift_{cat}_{wave}.pdf"
    fig.savefig(out, dpi=300)
    plt.close(fig)
    return out


# ============================================================================
# Per-category partial-residual scatter (H4)
# ============================================================================

def chart_partial_residual(cat, wave):
    df_cat = get_cat_paired(cat)
    df = df_cat[df_cat[f"trends_ww_{wave}_eligible"] & (~df_cat["e1a_excluded"])].copy()
    df = df.dropna(subset=[f"trends_ww_{wave}_mean", f"ai_{wave}_pct",
                            "brand_age_years", "tier_ordinal"]).copy()
    n = len(df)
    if n < 4:
        # Not enough for residual scatter
        print(f"  Skipping partial residual for {cat} {wave}: n={n} too small")
        return None

    x = df[f"ai_{wave}_pct"].values.astype(float)
    y = df[f"trends_ww_{wave}_mean"].values.astype(float)
    z1 = df["brand_age_years"].values.astype(float)
    z2 = df["tier_ordinal"].values.astype(float)
    xr = stats.rankdata(x)
    yr = stats.rankdata(y)
    z1r = stats.rankdata(z1)
    z2r = stats.rankdata(z2)
    Z = np.column_stack([np.ones(n), z1r, z2r])

    def resid(t):
        coef, *_ = np.linalg.lstsq(Z, t, rcond=None)
        return t - Z @ coef

    df = df.assign(x_resid=resid(xr), y_resid=resid(yr))

    fig, ax = plt.subplots(figsize=(7.5, 5.3))
    ax.grid(True, color=GRID_SUBTLE, linewidth=0.5, zorder=0)
    ax.axhline(0, color=GRID, linewidth=0.6, zorder=1)
    ax.axvline(0, color=GRID, linewidth=0.6, zorder=1)

    for tier in ("incumbent", "mid-tier", "challenger"):
        sub = df[df["market_tier"] == tier]
        ax.scatter(sub["x_resid"], sub["y_resid"],
                   color=TIER_COLOR.get(tier, MUTED), s=85, alpha=0.9,
                   edgecolor="white", linewidth=1.2, zorder=3,
                   label=tier.capitalize())

    texts = []
    for _, row in df.iterrows():
        t = ax.text(row["x_resid"], row["y_resid"], row["brand"],
                    fontsize=8, color=TEXT, ha="left", va="center", zorder=5)
        texts.append(t)

    if HAVE_ADJUST_TEXT:
        adjust_text(
            texts, ax=ax,
            arrowprops=dict(arrowstyle="-", color=GRID, lw=0.5),
            expand=(1.1, 1.3),
            force_text=(0.4, 0.6),
            force_static=(0.2, 0.3),
            max_move=(20, 30),
            iter_lim=200,
        )

    cat_results = scoring["per_category"][cat]
    corr = cat_results["correlations"][f"ww_{wave}"]
    pr = corr["partial_spearman_rho"]
    pp = corr["partial_spearman_p_one_tailed"]
    bi = corr["spearman_rho"]

    ax.set_xlabel("AI Presence rank residual (after age + tier control)", color=TEXT)
    ax.set_ylabel("Trends rank residual (after age + tier control)", color=TEXT)

    title_wave = "t₁" if wave == "t1" else "t₂"
    cat_label = CATEGORY_LABELS[cat]
    title = f"H4 — Covariate-controlled construct validity ({cat_label}, {title_wave})"
    mediation_pct = round(100 * (bi - pr) / bi, 0) if bi and bi > 0 else None
    if mediation_pct is not None:
        subtitle = (f"Rank residuals after OLS on age + tier. "
                    f"Bivariate ρ = {bi:.3f} → partial ρ = {pr:.3f} "
                    f"(age+tier mediates {mediation_pct:.0f}% of bivariate; p₁ₜ = {pp:.4f}).")
    else:
        subtitle = (f"Rank residuals after OLS on age + tier.\n"
                    f"Partial Spearman ρ = {pr:.3f}  (p₁ₜ = {pp:.4f}).")
    draw_title_and_subtitle(fig, title, subtitle)
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    add_source(fig)
    fig.subplots_adjust(top=0.82, bottom=0.13, left=0.10, right=0.96)

    out = OUT_DIR / f"chart_v12_h4_partial_residual_{cat}_{wave}.pdf"
    fig.savefig(out, dpi=300)
    plt.close(fig)
    return out


# ============================================================================
# H6 diagnostic-zone panel (PM + Running 2-up)
# ============================================================================

def chart_h6_zones(wave):
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 5.2))

    for ax, cat in zip(axes, ["pmsoftware", "running"]):
        df_cat = get_cat_paired(cat)
        df = df_cat[df_cat[f"trends_ww_{wave}_eligible"] & (~df_cat["e1a_excluded"])].copy()
        df = df.dropna(subset=[f"trends_ww_{wave}_mean", f"ai_{wave}_pct"])

        ax.grid(True, which="both", color=GRID_SUBTLE, linewidth=0.5, zorder=0)
        ax.set_yscale("log")

        # H6 thresholds from canonical scoring
        LINEAR_AI_MIN = 50
        LINEAR_TR_MAX = 5
        TODOIST_AI_MAX = 5
        TODOIST_TR_MIN = 20

        # Shade Linear-style zone (top-left): x≥50, y≤5
        ax.add_patch(Rectangle(
            (LINEAR_AI_MIN, 0.01), 100 - LINEAR_AI_MIN, LINEAR_TR_MAX - 0.01,
            facecolor=ZONE_FILL, alpha=0.10, edgecolor=ZONE_FILL,
            linestyle="--", linewidth=0.8, zorder=1,
        ))
        # Shade Todoist-style zone (bottom-right): x≤5, y≥20
        ax.add_patch(Rectangle(
            (-3, TODOIST_TR_MIN), TODOIST_AI_MAX - (-3), 10000 - TODOIST_TR_MIN,
            facecolor=ZONE_FILL, alpha=0.10, edgecolor=ZONE_FILL,
            linestyle="--", linewidth=0.8, zorder=1,
        ))
        # Zone labels
        ax.text(75, 1.5, "Linear-style\n(AI ≥ 50% AND Trends ≤ 5)",
                ha="center", va="center", fontsize=8, color=COPPER_PLATE,
                style="italic", zorder=2)
        ax.text(2.5, 100, "Todoist-style\n(AI ≤ 5% AND Trends ≥ 20)",
                ha="center", va="center", fontsize=8, color=COPPER_PLATE,
                style="italic", zorder=2)

        # Brand markers
        for tier in ("incumbent", "mid-tier", "challenger"):
            sub = df[df["market_tier"] == tier]
            ax.scatter(sub[f"ai_{wave}_pct"], sub[f"trends_ww_{wave}_mean"],
                       color=TIER_COLOR[tier], s=70, alpha=0.9,
                       edgecolor="white", linewidth=1.0, zorder=3,
                       label=tier.capitalize() if ax is axes[0] else None)

        # Highlight brands in either zone
        for _, row in df.iterrows():
            ai = row[f"ai_{wave}_pct"]
            tr = row[f"trends_ww_{wave}_mean"]
            in_linear = ai >= LINEAR_AI_MIN and tr <= LINEAR_TR_MAX
            in_todoist = ai <= TODOIST_AI_MAX and tr >= TODOIST_TR_MIN
            if in_linear or in_todoist:
                ax.scatter([ai], [tr], facecolor="none",
                           edgecolor=COPPER_PLATE, s=180, linewidth=2.0, zorder=4)

        # Labels for all brands
        texts = []
        for _, row in df.iterrows():
            t = ax.text(row[f"ai_{wave}_pct"], row[f"trends_ww_{wave}_mean"],
                        row["brand"], fontsize=7, color=TEXT,
                        ha="left", va="center", zorder=5)
            texts.append(t)
        if HAVE_ADJUST_TEXT and texts:
            adjust_text(
                texts, ax=ax,
                arrowprops=dict(arrowstyle="-", color=GRID, lw=0.4),
                expand=(1.05, 1.2),
                force_text=(0.3, 0.5),
                force_static=(0.15, 0.25),
                max_move=(15, 25),
                iter_lim=150,
            )

        ax.set_xlim(-3, 100)
        ax.set_ylim(0.5, 10000)
        ax.set_xlabel("AI Presence rate (%)", color=TEXT, fontsize=9)
        if ax is axes[0]:
            ax.set_ylabel("Trends rescaled mean (log; pivot ≡ 100)",
                          color=TEXT, fontsize=9)

        cat_results = scoring["per_category"][cat]
        h6 = cat_results["h6_diagnostics"]
        h6_status = h6["h6a_status"]
        linear_b = h6["per_wave"][wave]["linear_style"]
        todoist_b = h6["per_wave"][wave]["todoist_style"]
        ax.set_title(
            f"{CATEGORY_LABELS[cat]}\nH6a: {h6_status}  "
            f"(Linear={linear_b or '∅'};  Todoist={todoist_b or '∅'})",
            color=TEXT, fontsize=10, loc="left", pad=8,
        )

    axes[0].legend(loc="lower right", frameon=False, fontsize=8)
    title_wave = "t₁" if wave == "t1" else "t₂"
    fig_title = (f"H6 — Diagnostic-case detection across categories, {title_wave} (Worldwide)")
    fig_subtitle = ("Linear-style brands have high AI Presence but low Trends signal; "
                    "Todoist-style brands have the inverse pattern. H6 cross-category "
                    "requires both styles in 2-of-2 applicable categories.")
    draw_title_and_subtitle(fig, fig_title, fig_subtitle, x=0.03)
    add_source(fig, x=0.03)
    fig.subplots_adjust(top=0.80, bottom=0.13, left=0.06, right=0.98, wspace=0.20)

    out = OUT_DIR / f"chart_v12_h6_zones_{wave}.pdf"
    fig.savefig(out, dpi=300)
    plt.close(fig)
    return out


# ============================================================================
# Category-Scale Mismatch viz (olive oil matched subset)
# ============================================================================

def chart_scale_mismatch():
    # Sort by t1 AI Presence descending
    df = mismatch_df.sort_values("ai_presence_t1_pct", ascending=True).copy()
    n = len(df)

    fig, ax = plt.subplots(figsize=(9.0, max(5.5, 0.4 * n + 2)))

    # Horizontal bars at t1 AI Presence
    y_positions = np.arange(n)
    colors = [TIER_COLOR.get(t, MUTED) for t in df["market_tier"]]

    # Light bar showing AI Presence
    ax.barh(y_positions, df["ai_presence_t1_pct"], height=0.55,
            color=colors, alpha=0.80, edgecolor="white", linewidth=0.5, zorder=2,
            label="AI Presence t₁ (%)")

    # Right edge markers: Trends state
    for i, (_, row) in enumerate(df.iterrows()):
        ai_t1 = row["ai_presence_t1_pct"]
        disp = row["phase_b_disposition"]
        tr_t1 = row["trends_ww_t1_rescaled"]
        if disp == "EXCLUDED_E1a":
            # Red × marker indicating below threshold
            ax.scatter([ai_t1 + 1.5], [i], marker="x", color=COPPER_PLATE,
                       s=70, linewidth=2, zorder=4)
            ax.text(ai_t1 + 4, i, "below display threshold",
                    fontsize=8, color=COPPER_PLATE, va="center",
                    style="italic", zorder=5)
        else:
            # Green circle with rescaled value
            try:
                tr_val = float(tr_t1)
                ax.scatter([ai_t1 + 1.5], [i], marker="o", color="#2E7D32",
                           s=50, edgecolor="white", linewidth=0.8, zorder=4)
                ax.text(ai_t1 + 4, i, f"Trends rescaled = {tr_val:.1f}",
                        fontsize=8, color="#2E7D32", va="center", zorder=5)
            except (ValueError, TypeError):
                pass

        # Mark scale-mismatch cases with annotation
        if row["scale_mismatch_case"]:
            ax.text(-1, i, "▶", fontsize=10, color=COPPER_PLATE,
                    ha="right", va="center", weight="bold")

    ax.set_yticks(y_positions)
    ax.set_yticklabels(df["brand"], fontsize=9)
    ax.set_xlabel("AI Presence rate at t₁ (%)", color=TEXT)
    ax.set_xlim(-4, 100)
    ax.set_ylim(-0.7, n - 0.3)
    ax.grid(True, axis="x", color=GRID_SUBTLE, linewidth=0.5, zorder=0)

    # Legend
    for tier in ("incumbent", "mid-tier", "challenger"):
        ax.barh([], [], color=TIER_COLOR[tier], label=tier.capitalize())
    ax.scatter([], [], marker="o", color="#2E7D32", s=50,
               label="Trends signal (PASS)")
    ax.scatter([], [], marker="x", color=COPPER_PLATE, s=70, linewidth=2,
               label="Trends below display threshold (E1a)")
    ax.legend(loc="lower right", frameon=False, fontsize=8)

    # Compute scale-mismatch index
    sm = scoring["category_scale_mismatch_olive_oil"]
    n_sm = sm["n_scale_mismatch"]
    n_tot = sm["n_total"]
    pct = sm["scale_mismatch_index_pct"]

    title = "Category-Scale Mismatch Finding — Premium olive oil"
    subtitle = (f"Matched-subset olive oil brands ranked by AI Presence (t₁). "
                f"Scale-mismatch index: {n_sm}/{n_tot} = {pct}% "
                f"(brands with AI Presence ≥ 5% AND Trends below display threshold "
                f"are marked ▶).")
    draw_title_and_subtitle(fig, title, subtitle)
    add_source(fig)
    fig.subplots_adjust(top=0.88, bottom=0.10, left=0.22, right=0.96)

    out = OUT_DIR / "chart_v12_scale_mismatch_olive_oil.pdf"
    fig.savefig(out, dpi=300)
    plt.close(fig)
    return out


# ============================================================================
# Run all
# ============================================================================

print()
print("Generating charts...")

generated = []

# F1, F2: cross-category headline scatter
generated.append(("F1", chart_cross_category_scatter("t1")))
generated.append(("F2", chart_cross_category_scatter("t2")))

# F3, F4: PM rank-shift
generated.append(("F3", chart_rank_shift("pmsoftware", "t1")))
generated.append(("F4", chart_rank_shift("pmsoftware", "t2")))

# F5, F6: PM partial residual
generated.append(("F5", chart_partial_residual("pmsoftware", "t1")))
generated.append(("F6", chart_partial_residual("pmsoftware", "t2")))

# F7, F8: Running rank-shift
generated.append(("F7", chart_rank_shift("running", "t1")))
generated.append(("F8", chart_rank_shift("running", "t2")))

# F9, F10: Running partial residual
generated.append(("F9", chart_partial_residual("running", "t1")))
generated.append(("F10", chart_partial_residual("running", "t2")))

# F11, F12: H6 zones
generated.append(("F11", chart_h6_zones("t1")))
generated.append(("F12", chart_h6_zones("t2")))

# F13: Scale-Mismatch viz (single wave — t1 primary)
generated.append(("F13", chart_scale_mismatch()))

print()
for label, path in generated:
    if path is not None:
        print(f"  {label}: {path.name}")
    else:
        print(f"  {label}: (skipped — insufficient data)")
print()
print(f"All charts written to: {OUT_DIR}")
