"""v0.12 brand-format report chart variants.

Produces 2 NEW chart PDFs at 7.5-inch (6-col) width for the brand-format
report layout. The other 2 charts the brand-format report consumes are
reused directly from build_charts_v12.py output (already at 7.5" wide).

Output (4 PDFs total in ~/aias/osf/v12/figures/):
  Reused (already produced by build_charts_v12.py):
    chart_v12_h3_rank_shift_pmsoftware_t1.pdf    — Finding 1
    chart_v12_h4_partial_residual_running_t1.pdf — Finding 2

  NEW (produced by this script):
    chart_v12_threeregimes_scalemismatch_6col.pdf — Finding 3
    chart_v12_threeregimes_h6zones_6col.pdf       — Finding 4

The two new charts are forks of chart_scale_mismatch() and chart_h6_zones()
from build_charts_v12.py with figsize reduced from (9.0, variable) and
(11.0, 5.8) respectively to (7.5, variable) and (7.5, 4.7) to fit the
6-col brand-format width.

Run:
    python scripts/build_charts_v12_threeregimes.py
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

try:
    from adjustText import adjust_text
    HAVE_ADJUST_TEXT = True
except ImportError:
    HAVE_ADJUST_TEXT = False

# ============================================================================
# Brand constants (mirrors build_charts_v12.py)
# ============================================================================

INDIGO       = "#37237B"
PETRO        = "#6A6AB1"
COPPER_PLATE = "#F36C35"
TEXT         = "#231F20"
MUTED        = "#6B6967"
GRID         = "#CCCCCC"
GRID_SUBTLE  = "#E5E5E5"
ZONE_FILL    = "#F36C35"

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

# Reports omit the SSRN paper's full source line since the report has its
# own footer chrome. The chart's own source line is short and informational.
SOURCE_LINE = ("Source: Third System AI Presence Index v0.12 \u00b7 "
               "Acquisition 2026-05-11T10:33:22Z \u00b7 "
               "Pre-reg v0.12-prereg (commit ae4bd3a).")


def draw_title_and_subtitle(fig, title, subtitle, x=0.06, title_y=0.96,
                              subtitle_y=0.91, wrap_width=92):
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
# F3 (brand-format): Olive oil Scale-Mismatch at 7.5" wide
# ============================================================================

def chart_scale_mismatch_6col():
    """Brand-format variant of olive oil Scale-Mismatch viz.

    Reduces width from 9.0" (SSRN paper version) to 7.5" (6-col report
    layout). Slightly tighter horizontal spacing for inline labels.
    """
    df = mismatch_df.sort_values("ai_presence_t1_pct", ascending=True).copy()
    n = len(df)

    fig, ax = plt.subplots(figsize=(7.5, max(5.8, 0.4 * n + 2.4)))

    y_positions = np.arange(n)
    colors = [TIER_COLOR.get(t, MUTED) for t in df["market_tier"]]

    ax.barh(y_positions, df["ai_presence_t1_pct"], height=0.55,
            color=colors, alpha=0.80, edgecolor="white", linewidth=0.5, zorder=2)

    # 7.5" is narrower; trim inline text for readability
    for i, (_, row) in enumerate(df.iterrows()):
        ai_t1 = row["ai_presence_t1_pct"]
        disp = row["phase_b_disposition"]
        tr_t1 = row["trends_ww_t1_rescaled"]
        if disp == "EXCLUDED_E1a":
            ax.scatter([ai_t1 + 1.5], [i], marker="x", color=COPPER_PLATE,
                       s=70, linewidth=2, zorder=4)
            ax.text(ai_t1 + 4, i, "below display threshold",
                    fontsize=8, color=COPPER_PLATE, va="center",
                    style="italic", zorder=5)
        else:
            try:
                tr_val = float(tr_t1)
                ax.scatter([ai_t1 + 1.5], [i], marker="o", color="#2E7D32",
                           s=50, edgecolor="white", linewidth=0.8, zorder=4)
                ax.text(ai_t1 + 4, i, f"Trends = {tr_val:.1f}",
                        fontsize=8, color="#2E7D32", va="center", zorder=5)
            except (ValueError, TypeError):
                pass

        if row["scale_mismatch_case"]:
            ax.text(-1, i, "\u25B6", fontsize=10, color=COPPER_PLATE,
                    ha="right", va="center", weight="bold")

    ax.set_yticks(y_positions)
    ax.set_yticklabels(df["brand"], fontsize=9)
    ax.set_xlabel("AI Presence rate at t\u2081 (%)", color=TEXT)
    ax.set_xlim(-4, 100)
    ax.set_ylim(-0.7, n - 0.3)
    ax.grid(True, axis="x", color=GRID_SUBTLE, linewidth=0.5, zorder=0)

    for tier in ("incumbent", "mid-tier", "challenger"):
        ax.barh([], [], color=TIER_COLOR[tier], label=tier.capitalize())
    ax.scatter([], [], marker="o", color="#2E7D32", s=50,
               label="Trends signal (PASS)")
    ax.scatter([], [], marker="x", color=COPPER_PLATE, s=70, linewidth=2,
               label="Trends below display threshold (E1a)")
    ax.legend(loc="lower right", frameon=False, fontsize=8)

    sm = scoring["category_scale_mismatch_olive_oil"]
    pct = sm["scale_mismatch_index_pct"]
    n_sm = sm["n_scale_mismatch"]
    n_tot = sm["n_total"]

    title = "Olive oil \u2014 Category-Scale Mismatch"
    subtitle = (f"Scale-mismatch index: {n_sm} of {n_tot} matched-subset brands "
                f"({pct}%) have AI Presence \u2265 5% at either wave but Trends "
                f"below display threshold (marked \u25B6).")
    draw_title_and_subtitle(fig, title, subtitle, wrap_width=92)
    add_source(fig)
    fig.subplots_adjust(top=0.86, bottom=0.09, left=0.24, right=0.96)

    out = OUT_DIR / "chart_v12_threeregimes_scalemismatch_6col.pdf"
    fig.savefig(out, dpi=300)
    plt.close(fig)
    return out


# ============================================================================
# F4 (brand-format): Cross-category H6 zones at 7.5" wide
# ============================================================================

def chart_h6_zones_6col():
    """Brand-format variant of cross-category H6 zones panel.

    Reduces width from 11.0" (SSRN paper version) to 7.5" (6-col report
    layout). 2-panel side-by-side (PM | Running) is compressed; brand
    labels truncated where overlap risk is highest.
    """
    wave = "t1"
    fig, axes = plt.subplots(1, 2, figsize=(7.5, 4.7))

    for ax, cat in zip(axes, ["pmsoftware", "running"]):
        df_cat = paired[paired["category"] == cat].copy()
        df = df_cat[df_cat[f"trends_ww_{wave}_eligible"] & (~df_cat["e1a_excluded"])].copy()
        df = df.dropna(subset=[f"trends_ww_{wave}_mean", f"ai_{wave}_pct"])

        ax.grid(True, which="both", color=GRID_SUBTLE, linewidth=0.5, zorder=0)
        ax.set_yscale("log")

        LINEAR_AI_MIN = 50
        LINEAR_TR_MAX = 5
        TODOIST_AI_MAX = 5
        TODOIST_TR_MIN = 20

        ax.add_patch(Rectangle(
            (LINEAR_AI_MIN, 0.01), 100 - LINEAR_AI_MIN, LINEAR_TR_MAX - 0.01,
            facecolor=ZONE_FILL, alpha=0.10, edgecolor=ZONE_FILL,
            linestyle="--", linewidth=0.8, zorder=1,
        ))
        ax.add_patch(Rectangle(
            (-3, TODOIST_TR_MIN), TODOIST_AI_MAX - (-3), 10000 - TODOIST_TR_MIN,
            facecolor=ZONE_FILL, alpha=0.10, edgecolor=ZONE_FILL,
            linestyle="--", linewidth=0.8, zorder=1,
        ))
        # Tighter zone-label positioning at narrower width
        ax.text(75, 1.5, "Linear-style",
                ha="center", va="center", fontsize=7, color=COPPER_PLATE,
                style="italic", zorder=2)
        ax.text(2.5, 100, "Todoist-style",
                ha="center", va="center", fontsize=7, color=COPPER_PLATE,
                style="italic", zorder=2)

        for tier in ("incumbent", "mid-tier", "challenger"):
            sub = df[df["market_tier"] == tier]
            ax.scatter(sub[f"ai_{wave}_pct"], sub[f"trends_ww_{wave}_mean"],
                       color=TIER_COLOR[tier], s=55, alpha=0.9,
                       edgecolor="white", linewidth=1.0, zorder=3,
                       label=tier.capitalize() if ax is axes[0] else None)

        for _, row in df.iterrows():
            ai = row[f"ai_{wave}_pct"]
            tr = row[f"trends_ww_{wave}_mean"]
            in_linear = ai >= LINEAR_AI_MIN and tr <= LINEAR_TR_MAX
            in_todoist = ai <= TODOIST_AI_MAX and tr >= TODOIST_TR_MIN
            if in_linear or in_todoist:
                ax.scatter([ai], [tr], facecolor="none",
                           edgecolor=COPPER_PLATE, s=130, linewidth=1.8, zorder=4)

        texts = []
        for _, row in df.iterrows():
            t = ax.text(row[f"ai_{wave}_pct"], row[f"trends_ww_{wave}_mean"],
                        row["brand"], fontsize=6.5, color=TEXT,
                        ha="left", va="center", zorder=5)
            texts.append(t)
        if HAVE_ADJUST_TEXT and texts:
            adjust_text(
                texts, ax=ax,
                arrowprops=dict(arrowstyle="-", color=GRID, lw=0.4),
                expand=(1.05, 1.2),
                force_text=(0.3, 0.5),
                force_static=(0.15, 0.25),
                max_move=(12, 20),
                iter_lim=120,
            )

        ax.set_xlim(-3, 100)
        ax.set_ylim(0.5, 10000)
        ax.set_xlabel("AI Presence (%)", color=TEXT, fontsize=8)
        if ax is axes[0]:
            ax.set_ylabel("Trends rescaled (log)", color=TEXT, fontsize=8)
        ax.tick_params(axis='both', labelsize=8)

        cat_results = scoring["per_category"][cat]
        h6 = cat_results["h6_diagnostics"]
        h6_status = h6["h6a_status"]
        linear_b = h6["per_wave"][wave]["linear_style"]
        todoist_b = h6["per_wave"][wave]["todoist_style"]
        cat_label = "Project management software" if cat == "pmsoftware" else "Premium running shoes"
        ax.set_title(
            f"{cat_label}\nH6a: {h6_status}",
            color=TEXT, fontsize=9, loc="left", pad=4,
        )

    axes[0].legend(loc="lower right", frameon=False, fontsize=7)
    fig_title = "Three regimes: PM bidirectional, Running asymmetric"
    fig_subtitle = ("Linear-style brands (top-left: AI \u2265 50%, Trends \u2264 5) AND "
                    "Todoist-style brands (bottom-right: AI \u2264 5%, Trends \u2265 20). "
                    "PM software shows both; Running shows only Linear-style "
                    "(Brooks, Hoka) \u2014 boundary mismatch unidirectional.")
    draw_title_and_subtitle(fig, fig_title, fig_subtitle, x=0.03,
                              subtitle_y=0.88, wrap_width=130)
    add_source(fig, x=0.03)
    fig.subplots_adjust(top=0.72, bottom=0.12, left=0.07, right=0.97, wspace=0.18)

    out = OUT_DIR / "chart_v12_threeregimes_h6zones_6col.pdf"
    fig.savefig(out, dpi=300)
    plt.close(fig)
    return out


# ============================================================================
# Run
# ============================================================================

print()
print("Generating brand-format report charts...")
print(f"  F3 (Scale-Mismatch 6-col): {chart_scale_mismatch_6col().name}")
print(f"  F4 (H6 zones 6-col):       {chart_h6_zones_6col().name}")
print()
print(f"Reusing 2 existing SSRN paper charts at 6-col width:")
print(f"  F1: chart_v12_h3_rank_shift_pmsoftware_t1.pdf")
print(f"  F2: chart_v12_h4_partial_residual_running_t1.pdf")
print()
print(f"All 4 charts available at: {OUT_DIR}")
