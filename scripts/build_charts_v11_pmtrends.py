"""v0.11 chart generation for the brand-format report and SSRN paper.

Produces 4 PDF charts at locked figsizes per the Third System brand spec.

  F1 — Scatter t1: AI Presence x Trends (Worldwide), brand-labeled, log-y
  F2 — Scatter t2: same shape; visual H2 stability evidence
  F3 — Rank-shift slope chart at t1: AI rank vs Trends rank per brand
  F4 — Partial-correlation residual scatter at t1 (H4 visualization)

Tie-break convention for F3:
  - ai_rank breaks ties on AI Presence by trends_mean (desc), so the
    higher-Trends brand among a tie gets the better AI rank position.
  - trends_rank breaks ties on Trends by ai_pct (desc), symmetrically.
  - Each brand thus gets a unique rank in each dimension, avoiding label
    stacking at the same y-coordinate.

Optional dependency: adjustText for force-directed label repulsion in
scatter charts. Falls back to fixed offsets if not installed.

Run:
    pip install adjustText   # one-time
    python scripts/build_charts_v11_pmtrends.py
"""
import json
from pathlib import Path

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import rcParams
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

TIER_COLOR = {
    "incumbent": INDIGO,
    "mid-tier":  PETRO,
    "challenger": COPPER_PLATE,
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

V11_ROOT = Path.home() / "aias" / "osf" / "v11"
PAIRED   = V11_ROOT / "analysis" / "per_brand_paired.csv"
SCORING  = V11_ROOT / "analysis" / "canonical_scoring.json"
OUT_DIR  = V11_ROOT / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

paired = pd.read_csv(PAIRED)
with SCORING.open() as f:
    scoring = json.load(f)

SOURCE_LINE = ("Source: Third System AI Presence Index v0.11 · "
               "Google Trends acquisition 2026-05-10 · "
               "Pre-reg locked at v0.11-prereg (commit f20ade8).")


def draw_title_and_subtitle(fig, title, subtitle):
    """Place title at y=0.96, subtitle at y=0.91, both va='top' for predictable layout."""
    fig.text(0.06, 0.96, title, ha="left", va="top",
             fontsize=13, color=TEXT, weight="bold")
    fig.text(0.06, 0.91, subtitle, ha="left", va="top",
             fontsize=9.5, color=MUTED)


def add_source(fig):
    fig.text(0.06, 0.025, SOURCE_LINE, ha="left", va="top",
             fontsize=7.5, color=MUTED, style="italic")


# ============================================================================
# F1 / F2: scatter AI x Trends per wave
# ============================================================================

def chart_scatter(wave):
    df = paired[paired[f"trends_ww_{wave}_eligible"]].copy()
    df = df.dropna(subset=[f"trends_ww_{wave}_mean", f"ai_{wave}_pct"])

    fig, ax = plt.subplots(figsize=(7.5, 5.0))
    ax.grid(True, which="both", color=GRID_SUBTLE, linewidth=0.5, zorder=0)

    for tier in ("incumbent", "mid-tier", "challenger"):
        sub = df[df["market_tier"] == tier]
        ax.scatter(sub[f"ai_{wave}_pct"], sub[f"trends_ww_{wave}_mean"],
                   color=TIER_COLOR[tier], s=85, alpha=0.9,
                   edgecolor="white", linewidth=1.2, zorder=3,
                   label=tier.capitalize())

    # Build label list. Defer positioning to adjustText if available.
    texts = []
    for _, row in df.iterrows():
        t = ax.text(row[f"ai_{wave}_pct"], row[f"trends_ww_{wave}_mean"],
                    row["brand"], fontsize=8, color=TEXT,
                    ha="left", va="center", zorder=5)
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
    else:
        # Fallback: simple alternating offsets.
        for i, t in enumerate(texts):
            dx, dy = (8, 4) if i % 2 == 0 else (8, -8)
            t.set_position((t.get_position()[0], t.get_position()[1]))
            t.set_x(t.get_position()[0])

    ax.set_yscale("log")
    ax.set_xlim(-3, 100)
    ax.set_xlabel("AI Presence rate (%)", color=TEXT)
    ax.set_ylabel("Google Trends rescaled mean (log scale; Asana ≡ 100)",
                  color=TEXT)

    corr = scoring["correlations"][f"ww_{wave}"]
    n   = corr["n"]
    rho = corr["spearman_rho"]
    p1t = corr["spearman_p_one_tailed"]
    r   = corr["pearson_r"]

    title_wave = "t₁" if wave == "t1" else "t₂"
    title = f"H1 — AI Presence × Google Trends, {title_wave} (Worldwide)"
    subtitle = (f"n = {n}.   Spearman ρ = {rho:.3f}  (p₁ₜ = {p1t:.4f}).   "
                f"Pearson r = {r:.3f} (sensitivity).")
    draw_title_and_subtitle(fig, title, subtitle)

    ax.legend(loc="lower right", frameon=False, fontsize=9)
    add_source(fig)

    fig.subplots_adjust(top=0.82, bottom=0.13, left=0.10, right=0.96)

    out = OUT_DIR / f"chart_v11_h1_scatter_{wave}_6col.pdf"
    fig.savefig(out, dpi=300)
    plt.close(fig)
    return out


# ============================================================================
# F3: rank-shift slope chart
# ============================================================================

def chart_rank_shift(wave="t1"):
    df = paired[paired[f"trends_ww_{wave}_eligible"]].copy()
    df = df.dropna(subset=[f"trends_ww_{wave}_mean", f"ai_{wave}_pct"]).copy()

    # Unique ranks with deterministic tie-breaking by the OTHER variable.
    # ai_rank: sort by ai_pct desc, then trends_mean desc (tied-on-AI brands
    # with higher trends get the better ai_rank). Symmetric for trends_rank.
    ai_sorted = df.sort_values(
        [f"ai_{wave}_pct", f"trends_ww_{wave}_mean"], ascending=[False, False]
    ).reset_index(drop=True)
    ai_rank_map = dict(zip(ai_sorted["brand"], ai_sorted.index + 1))

    tr_sorted = df.sort_values(
        [f"trends_ww_{wave}_mean", f"ai_{wave}_pct"], ascending=[False, False]
    ).reset_index(drop=True)
    trends_rank_map = dict(zip(tr_sorted["brand"], tr_sorted.index + 1))

    df["ai_rank"]     = df["brand"].map(ai_rank_map)
    df["trends_rank"] = df["brand"].map(trends_rank_map)
    df["abs_diff"]    = (df["trends_rank"] - df["ai_rank"]).abs()
    n = len(df)

    fig, ax = plt.subplots(figsize=(7.5, 6.5))
    x_left, x_right = 0.0, 1.0

    # Lines: draw non-extreme first (lower z), extreme on top.
    for _, row in df.sort_values("abs_diff").iterrows():
        y_ai     = -row["ai_rank"]
        y_trends = -row["trends_rank"]
        color = TIER_COLOR[row["market_tier"]]
        is_extreme = row["abs_diff"] >= 8
        lw    = 2.4 if is_extreme else 1.0
        alpha = 0.95 if is_extreme else 0.5
        line_color = COPPER_PLATE if is_extreme else color
        ax.plot([x_left, x_right], [y_ai, y_trends],
                color=line_color, alpha=alpha, linewidth=lw,
                zorder=4 if is_extreme else 2)

    # Markers + labels.
    for _, row in df.iterrows():
        y_ai     = -row["ai_rank"]
        y_trends = -row["trends_rank"]
        color = TIER_COLOR[row["market_tier"]]
        ax.scatter([x_left],  [y_ai],     color=color, s=55, zorder=5,
                   edgecolor="white", linewidth=1.0)
        ax.scatter([x_right], [y_trends], color=color, s=55, zorder=5,
                   edgecolor="white", linewidth=1.0)
        ax.text(x_left - 0.03,  y_ai,     row["brand"],
                ha="right", va="center", fontsize=9, color=TEXT)
        ax.text(x_right + 0.03, y_trends, row["brand"],
                ha="left",  va="center", fontsize=9, color=TEXT)

    # Column headers inside the axes.
    header_y = 0.2
    ax.text(x_left,  header_y, "AI Presence rank",
            ha="center", va="bottom", fontsize=11, color=TEXT, weight="bold")
    ax.text(x_right, header_y, "Trends rank",
            ha="center", va="bottom", fontsize=11, color=TEXT, weight="bold")

    ax.set_xlim(-0.45, 1.45)
    ax.set_ylim(-(n + 0.8), 1.0)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])

    # Tier + extreme legend (below the figure).
    for tier in ("incumbent", "mid-tier", "challenger"):
        ax.scatter([], [], color=TIER_COLOR[tier], s=55,
                   label=tier.capitalize())
    ax.plot([], [], color=COPPER_PLATE, linewidth=2.4,
            label="Extreme divergence (|Δrank| ≥ 8)")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.05),
              ncol=4, frameon=False, fontsize=9)

    title_wave = "t₁" if wave == "t1" else "t₂"
    title = (f"H3 — AI Presence rank vs Google Trends rank, "
             f"{title_wave} (Worldwide)")
    subtitle = ("Lines connect each brand's rank by AI Presence (left) to "
                "its rank by Trends (right). Steep slopes = construct divergence. "
                "Ties broken by the other variable.")
    draw_title_and_subtitle(fig, title, subtitle)
    add_source(fig)

    fig.subplots_adjust(top=0.86, bottom=0.08, left=0.02, right=0.98)

    out = OUT_DIR / f"chart_v11_h3_rank_shift_{wave}_6col.pdf"
    fig.savefig(out, dpi=300)
    plt.close(fig)
    return out


# ============================================================================
# F4: partial residual scatter
# ============================================================================

def chart_partial_residual(wave="t1"):
    df = paired[paired[f"trends_ww_{wave}_eligible"]].copy()
    df = df.dropna(subset=[f"trends_ww_{wave}_mean", f"ai_{wave}_pct",
                            "brand_age_years", "tier_ordinal"]).copy()
    n = len(df)

    x  = df[f"ai_{wave}_pct"].values.astype(float)
    y  = df[f"trends_ww_{wave}_mean"].values.astype(float)
    z1 = df["brand_age_years"].values.astype(float)
    z2 = df["tier_ordinal"].values.astype(float)

    xr  = stats.rankdata(x)
    yr  = stats.rankdata(y)
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
                   color=TIER_COLOR[tier], s=85, alpha=0.9,
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

    corr = scoring["correlations"][f"ww_{wave}"]
    pr = corr["partial_spearman_rho"]
    pp = corr["partial_spearman_p_one_tailed"]

    ax.set_xlabel("AI Presence rank residual (after age + tier control)",
                  color=TEXT)
    ax.set_ylabel("Trends rank residual (after age + tier control)",
                  color=TEXT)

    title_wave = "t₁" if wave == "t1" else "t₂"
    title = (f"H4 — Covariate-controlled construct validity, "
             f"{title_wave} (Worldwide)")
    subtitle = ("Rank residuals after OLS on rank-transformed brand age + competitive density.\n"
                f"Partial Spearman ρ = {pr:.3f}  (p₁ₜ = {pp:.4f}).")
    draw_title_and_subtitle(fig, title, subtitle)

    ax.legend(loc="lower right", frameon=False, fontsize=9)
    add_source(fig)
    fig.subplots_adjust(top=0.82, bottom=0.13, left=0.10, right=0.96)

    out = OUT_DIR / f"chart_v11_h4_partial_residual_{wave}_6col.pdf"
    fig.savefig(out, dpi=300)
    plt.close(fig)
    return out


# ============================================================================
# Run
# ============================================================================

print()
print("Generating charts...")
print(f"  F1: {chart_scatter('t1').name}")
print(f"  F2: {chart_scatter('t2').name}")
print(f"  F3: {chart_rank_shift('t1').name}")
print(f"  F4: {chart_partial_residual('t1').name}")
print()
print(f"All charts written to: {OUT_DIR}")
