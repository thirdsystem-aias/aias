#!/usr/bin/env python3
"""
v0.9 Re-Baseline chart generator (v14).

Standardized typography across all 9 charts using point-based offsets from
figure edges, so the visual hierarchy is consistent regardless of figure
height. This matches the v0.7 'Within-lab freshness' reference layout.

Layout pattern (all charts):
  - Title:     13pt bold, dark, baseline 18pt from figure top, x=0.02
  - Subtitle:  9.5pt italic gray, top of text 30pt from figure top
               (close gap to title — visual pairing)
  - [chart axes]
  - Source 1:  7.5pt italic gray, baseline 28pt from figure bottom
  - Source 2:  7pt   italic gray, baseline 14pt from figure bottom
  Both source lines start at x=0.02 to fit within figure width regardless
  of horizontal length.

Charts (mapped to paper sections):
  chart_v09_h1_drift_scatter_6col.pdf         §3.1 H1
  chart_v09_h2_leaderboard_6col.pdf           §3.2 H2
  chart_v09_h3_within_cat_variance_6col.pdf   §3.3 H3
  chart_v09_h4_mint_persistence_4col.pdf      §3.4 H4
  chart_v09_h5_pattern4_sensitivity_6col.pdf  §3.5 H5
  chart_v09_h6_cross_model_spread_6col.pdf    §3.6 H6
  chart_v09_pattern1_spread_6col.pdf          §3.7 post-hoc Pattern 1
  chart_v09_mode_distribution_6col.pdf        §3.8 mode distribution
  chart_v09_pattern_matrix_6col.pdf           sec 5 pattern matrix
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from statistics import mean, pstdev

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Rectangle

SCRIPT_DIR = Path(__file__).resolve().parent
AIAS_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(AIAS_ROOT))

from analyze_v09 import (  # noqa: E402
    load_all_data,
    per_brand_presence,
    filter_matched,
    filter_slot,
    pearson_r,
    spearman_rho,
    CATEGORIES,
    MATCHED_SUBSET,
    PHANTOM_BRAND,
    PHANTOM_BRAND_CATEGORY,
    SPANISH_OLIVE_OIL_THRESHOLD_PCT,
    KBEAUTY_THRESHOLD_PCT,
)

BRAND_JSON = AIAS_ROOT / "brand" / "third_system_brand.json"
DATA_ROOT = AIAS_ROOT / "data"
OUTPUT_DIR = SCRIPT_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


_FALLBACK_PALETTE = {
    "indigo": "#37237B",
    "indigo_50": "#9B91BD",
    "indigo_25": "#CDC8DE",
    "copper": "#F36C35",
    "petro": "#0E5C7C",
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
            for key, val in block.items():
                if isinstance(val, dict) and "hex" in val:
                    palette.setdefault(key, val["hex"])
    return palette


PALETTE = load_palette()


def register_fonts() -> str:
    candidates = [Path.home() / ".fonts" / "Akkurat", Path.home() / "Library" / "Fonts"]
    for d in candidates:
        if not d.exists():
            continue
        for ttf in d.glob("**/*Akkurat*.[ot]tf"):
            try:
                font_manager.fontManager.addfont(str(ttf))
            except Exception:
                pass
    sans_candidates = ["Akkurat Pro", "Akkurat", "Inter", "Helvetica", "Arial", "DejaVu Sans"]
    available = {f.name for f in font_manager.fontManager.ttflist}
    for c in sans_candidates:
        if c in available:
            return c
    return "DejaVu Sans"


SANS = register_fonts()
plt.rcParams.update({
    "font.family": SANS,
    "font.size": 9,
    "axes.titlesize": 10,
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "axes.edgecolor": PALETTE["soft_black"],
    "axes.labelcolor": PALETTE["soft_black"],
    "xtick.color": PALETTE["soft_black"],
    "ytick.color": PALETTE["soft_black"],
    "axes.spines.top": False,
    "axes.spines.right": False,
    "mathtext.fontset": "stix",
})


def save(fig, name: str):
    out = OUTPUT_DIR / name
    fig.savefig(out, bbox_inches=None, pad_inches=0.0, dpi=300)
    plt.close(fig)
    print(f"  wrote {out}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Title / subtitle / source helpers — point-based offsets for consistency
# across charts of different heights.
# ---------------------------------------------------------------------------

SOURCE_PROGRAM = "Third System AIAS measurement program · v0.9 Longitudinal Re-Baseline"
SOURCE_DATE = "8 May 2026"


def yt(pt, fig):
    """Convert pt offset from top edge of figure to figure-fraction y."""
    return 1.0 - pt / (fig.get_figheight() * 72.0)


def yb(pt, fig):
    """Convert pt offset from bottom edge of figure to figure-fraction y."""
    return pt / (fig.get_figheight() * 72.0)


def add_title_subtitle(fig, title, subtitle, *,
                       title_fontsize=13.0,
                       subtitle_fontsize=9.5,
                       title_pt=18, subtitle_top_pt=30):
    """Bold title and italic subtitle at figure level, tightly paired.

    The default offsets create the v0.7 'Within-lab freshness' look:
      - Title baseline at 18pt from top edge
      - Subtitle text TOP at 30pt from top edge (so subtitle sits just below
        the title with ~6pt visible gap given 13pt title height)
    """
    fig.text(0.02, yt(title_pt, fig), title,
             ha="left", va="bottom",
             fontsize=title_fontsize, fontweight="bold",
             color=PALETTE["soft_black"])
    fig.text(0.02, yt(subtitle_top_pt, fig), subtitle,
             ha="left", va="top",
             fontsize=subtitle_fontsize, fontstyle="italic",
             color=PALETTE["black_60"])


def add_source_line(fig, n_descriptor, *,
                    line1_pt=18, line2_pt=10):
    """Two-line source attribution at the figure bottom-left.

    Lines sit 8pt apart at baseline so they read as one compact footer
    block (visual row gap is ~1-2pt at 7pt font height — tight pairing,
    not two separated lines).

    Line 1 is a fixed program identifier shown across all charts.
    Line 2 is the chart-specific sample descriptor + date — different per
    chart so each footer carries useful sample-size context for that
    specific visual.
    """
    fig.text(0.02, yb(line1_pt, fig),
             "Source: Third System AIAS v0.9 Longitudinal Re-Baseline",
             ha="left", va="bottom",
             fontsize=7.5, color=PALETTE["black_60"], fontstyle="italic")
    fig.text(0.02, yb(line2_pt, fig),
             f"{n_descriptor} · {SOURCE_DATE}",
             ha="left", va="bottom",
             fontsize=7, color=PALETTE["black_60"], fontstyle="italic")


def standard_top(fig):
    """y of axes top: 55pt below figure top, leaving room for title+subtitle."""
    return yt(55, fig)


def standard_bottom(fig):
    """y of axes bottom: 65pt above figure bottom.

    The 65pt budget below the axes spine accommodates: ~37pt of x-axis area
    (4pt labelpad + 16pt tick labels + 4pt + 9pt xlabel + 4pt) above the
    source block, which itself occupies y=10 to ~y=26pt. This eliminates
    the source/x-axis collision that earlier 48-50pt budgets caused.
    """
    return yb(65, fig)


CATEGORY_DISPLAY = {
    "pm": "PM software",
    "running": "Running shoes",
    "oliveoil": "Olive oil",
    "skincare": "Skincare",
    "finance": "Personal finance",
}

T1 = r"$t_1$"
T2 = r"$t_2$"

MODE_ORDER = ["brand", "mixed", "component", "authority", "refusal"]
MODE_COLORS = {
    "brand":     PALETTE["indigo"],
    "mixed":     PALETTE["indigo_50"],
    "component": PALETTE.get("petro", "#0E5C7C"),
    "authority": PALETTE["copper"],
    "refusal":   PALETTE["black_40"],
}


def load_mode_classified(cat: str) -> list[dict]:
    path = DATA_ROOT / cat
    if not path.exists():
        return []
    files = sorted(path.glob("mode_classified_*.csv"))
    rows = []
    for fp in files:
        with open(fp) as f:
            rows.extend(csv.DictReader(f))
    return rows


def mode_share(rows) -> dict:
    counts = {m: 0 for m in MODE_ORDER}
    for r in rows:
        m = (r.get("primary_mode") or "").strip().lower()
        if m in counts:
            counts[m] += 1
    total = sum(counts.values()) or 1
    return {m: 100 * counts[m] / total for m in MODE_ORDER}


# ===========================================================================
# Chart 1 — H1 drift scatter
# ===========================================================================

def chart_h1_drift_scatter(data):
    fig, ax = plt.subplots(figsize=(7.50, 5.00))

    cat_colors = {
        "pm":       PALETTE["indigo"],
        "running":  PALETTE["copper"],
        "oliveoil": PALETTE.get("petro", "#0E5C7C"),
        "skincare": PALETTE["indigo_50"],
        "finance":  PALETTE["soft_black"],
    }

    points = []
    for cat in CATEGORIES:
        v06 = filter_matched(data[(cat, "v06")]["rows"])
        v09 = filter_matched(data[(cat, "v09")]["rows"])
        registry = data[(cat, "v09")]["registry"]
        bp_v06 = per_brand_presence(v06, registry)
        bp_v09 = per_brand_presence(v09, registry)
        for b in registry["all_brands"]:
            t1 = bp_v06[b]
            delta = bp_v09[b] - t1
            points.append((cat, b, t1, delta))

    ax.axhspan(-5, 5, color=PALETTE["indigo_25"], alpha=0.35, zorder=1,
               label="+/-5pp band (H1 noise floor)")
    ax.axhspan(-10, -5, color=PALETTE["indigo_25"], alpha=0.18, zorder=1)
    ax.axhspan(5, 10, color=PALETTE["indigo_25"], alpha=0.18, zorder=1,
               label="+/-10pp band")
    ax.axhline(0, color=PALETTE["soft_black"], linewidth=0.7, zorder=2)

    for cat in CATEGORIES:
        cat_points = [(t1, d) for c, _, t1, d in points if c == cat]
        if not cat_points:
            continue
        xs = [p[0] for p in cat_points]
        ys = [p[1] for p in cat_points]
        ax.scatter(xs, ys, s=22, alpha=0.75, color=cat_colors[cat],
                   edgecolors="white", linewidths=0.5, zorder=3,
                   label=CATEGORY_DISPLAY[cat])

    ax.set_xlim(0, 100)
    ax.set_ylim(-25, 25)
    ax.set_xlabel(f"{T1} Presence (%)")
    ax.set_ylabel(f"{T1} to {T2} delta (pp)")
    ax.legend(loc="upper right", frameon=False, ncol=2, fontsize=7.5)

    n5 = sum(1 for _, _, _, d in points if abs(d) <= 5)
    n10 = sum(1 for _, _, _, d in points if abs(d) <= 10)
    pct5 = 100 * n5 / len(points)
    pct10 = 100 * n10 / len(points)

    fig.subplots_adjust(left=0.10, right=0.97,
                        top=standard_top(fig), bottom=standard_bottom(fig))
    add_title_subtitle(fig,
                       "Per-brand drift across five categories: H1 confirmed",
                       f"{pct5:.1f}% within +/-5pp; {pct10:.1f}% within +/-10pp "
                       f"(matched subset, n={len(points)} brand-level deltas)")
    add_source_line(fig,
                    f"H1 drift: n={len(points)} brand-level deltas across 5 categories")
    save(fig, "chart_v09_h1_drift_scatter_6col.pdf")


# ===========================================================================
# Chart 2 — H2 leaderboard
# ===========================================================================

def _shorten(name: str, max_len: int = 26) -> str:
    if len(name) <= max_len:
        return name
    return name[: max_len - 1] + "."


def chart_h2_leaderboard(data):
    # Figsize 7.50x6.50: must fit the printable page area (~7.67" usable
    # height) with room for title block above and caption below when
    # rendered as a hero chart in the pattern flow. hspace 0.55 keeps
    # panels close enough that 5 stacked categories read as a single
    # leaderboard rather than 5 separate small charts.
    fig, axes = plt.subplots(len(CATEGORIES), 1, figsize=(7.50, 6.50),
                              gridspec_kw={"hspace": 0.55})

    for ax, cat in zip(axes, CATEGORIES):
        v06 = filter_matched(data[(cat, "v06")]["rows"])
        v09 = filter_matched(data[(cat, "v09")]["rows"])
        registry = data[(cat, "v09")]["registry"]
        bp_v06 = per_brand_presence(v06, registry)
        bp_v09 = per_brand_presence(v09, registry)

        v06_top5 = sorted(bp_v06.items(), key=lambda kv: kv[1], reverse=True)[:5]
        v09_top5 = sorted(bp_v09.items(), key=lambda kv: kv[1], reverse=True)[:5]
        union = []
        seen = set()
        for b, _ in v06_top5 + v09_top5:
            if b not in seen:
                union.append(b)
                seen.add(b)
        union = sorted(union, key=lambda b: bp_v09[b], reverse=True)
        v06_top3_brands = {b for b, _ in v06_top5[:3]}

        y_pos = list(range(len(union)))
        bar_h = 0.4
        t1_vals = [bp_v06[b] for b in union]
        t2_vals = [bp_v09[b] for b in union]

        ax.barh([y - bar_h / 2 for y in y_pos], t1_vals, height=bar_h,
                color=PALETTE["indigo_50"], label=f"{T1} (v0.6)")
        ax.barh([y + bar_h / 2 for y in y_pos], t2_vals, height=bar_h,
                color=PALETTE["indigo"], label=f"{T2} (v0.9)")

        ytick_labels = [
            f"* {_shorten(b)}" if b in v06_top3_brands else f"  {_shorten(b)}"
            for b in union
        ]
        ax.set_yticks(y_pos)
        ax.set_yticklabels(ytick_labels, fontsize=8, family="monospace")
        for tlabel, brand in zip(ax.get_yticklabels(), union):
            if brand in v06_top3_brands:
                tlabel.set_color(PALETTE["copper"])

        ax.invert_yaxis()
        ax.set_xlim(0, 100)
        ax.set_xlabel("Presence (%)" if cat == CATEGORIES[-1] else "")
        ax.set_title(CATEGORY_DISPLAY[cat], loc="left", fontsize=9.5,
                     fontweight="bold", pad=4)
        if cat == CATEGORIES[0]:
            ax.legend(loc="lower right", frameon=False, fontsize=7.5)

    fig.subplots_adjust(left=0.24, right=0.97,
                        top=yt(58, fig), bottom=yb(45, fig),
                        hspace=0.55)
    add_title_subtitle(fig,
                       "Top-of-leaderboard stable in all 5 categories: H2 confirmed (5/5)",
                       f"Top-3 brands at {T1} remained in top-5 at {T2} across every "
                       f"category   (* and copper = brand was in $t_1$ top-3)")
    add_source_line(fig,
                    "H2 leaderboard: top brands by Presence, n=96 per category-wave")
    save(fig, "chart_v09_h2_leaderboard_6col.pdf")


# ===========================================================================
# Chart 3 — H3 within-category variance
# ===========================================================================

def chart_h3_within_cat_variance(data):
    fig, ax = plt.subplots(figsize=(7.50, 4.30))

    var_t1 = {}
    var_t2 = {}
    for cat in CATEGORIES:
        registry = data[(cat, "v09")]["registry"]
        bp_v06 = per_brand_presence(filter_matched(data[(cat, "v06")]["rows"]), registry)
        bp_v09 = per_brand_presence(filter_matched(data[(cat, "v09")]["rows"]), registry)
        var_t1[cat] = pstdev(bp_v06[b] for b in registry["all_brands"])
        var_t2[cat] = pstdev(bp_v09[b] for b in registry["all_brands"])

    cats_sorted = sorted(CATEGORIES, key=lambda c: var_t2[c], reverse=True)
    x_pos = list(range(len(cats_sorted)))
    bar_w = 0.38
    t1_vals = [var_t1[c] for c in cats_sorted]
    t2_vals = [var_t2[c] for c in cats_sorted]

    ax.bar([x - bar_w / 2 for x in x_pos], t1_vals, width=bar_w,
           color=PALETTE["indigo_50"], label=f"{T1} (v0.6)",
           edgecolor="white", linewidth=0.5)
    ax.bar([x + bar_w / 2 for x in x_pos], t2_vals, width=bar_w,
           color=PALETTE["indigo"], label=f"{T2} (v0.9)",
           edgecolor="white", linewidth=0.5)

    for i, (t1, t2) in enumerate(zip(t1_vals, t2_vals)):
        ax.text(i - bar_w / 2, t1 + 0.4, f"{t1:.1f}", ha="center", va="bottom",
                fontsize=7.5, color=PALETTE["soft_black"])
        ax.text(i + bar_w / 2, t2 + 0.4, f"{t2:.1f}", ha="center", va="bottom",
                fontsize=7.5, color=PALETTE["soft_black"], fontweight="bold")

    ax.set_xticks(x_pos)
    ax.set_xticklabels([CATEGORY_DISPLAY[c] for c in cats_sorted], fontsize=8.5)
    ax.set_ylabel("Within-category brand-presence stdev (pp)")
    ax.set_ylim(0, max(max(t1_vals), max(t2_vals)) * 1.30)
    ax.legend(loc="upper right", frameon=False, fontsize=8)

    t1_rank = {c: r for r, c in enumerate(
        sorted(CATEGORIES, key=lambda c: var_t1[c], reverse=True), 1)}
    t2_rank = {c: r for r, c in enumerate(cats_sorted, 1)}
    rho = spearman_rho(t1_rank, t2_rank, CATEGORIES)

    fig.subplots_adjust(left=0.10, right=0.97,
                        top=standard_top(fig), bottom=standard_bottom(fig))
    add_title_subtitle(fig,
                       "Within-category brand-presence variance ordering preserves: H3 confirmed",
                       f"Spearman rho ({T1} vs {T2} ranking across 5 categories) = "
                       f"{rho:.2f}  (threshold 0.7+)")
    add_source_line(fig,
                    "H3 within-category brand-presence stdev, 5 categories × 2 waves")
    save(fig, "chart_v09_h3_within_cat_variance_6col.pdf")


# ===========================================================================
# Chart 4 — H4 Mint persistence (smaller chart, smaller title)
# ===========================================================================

def chart_h4_mint_persistence(data):
    # Figsize 3.55 x 3.20 to fit inline in column 1 of the 2-column non-hero
    # layout (BalancedColumns gives ~3.68" per column). Smaller than the rest
    # of the suite intentionally — the chart shows only two points + stability
    # band, which reads cleanly at this size.
    fig, ax = plt.subplots(figsize=(3.55, 3.20))

    cat = PHANTOM_BRAND_CATEGORY
    v06 = filter_matched(data[(cat, "v06")]["rows"])
    v09 = filter_matched(data[(cat, "v09")]["rows"])
    registry = data[(cat, "v09")]["registry"]
    bp_v06 = per_brand_presence(v06, registry)
    bp_v09 = per_brand_presence(v09, registry)
    t1 = bp_v06.get(PHANTOM_BRAND, 0)
    t2 = bp_v09.get(PHANTOM_BRAND, 0)

    ax.axhspan(t1 - 5, t1 + 5, color=PALETTE["indigo_25"], alpha=0.35,
               label="+/-5pp stability band")

    ax.plot([0, 1], [t1, t2], color=PALETTE["indigo"], linewidth=2.0,
            marker="o", markersize=8, markerfacecolor=PALETTE["indigo"],
            markeredgecolor="white", markeredgewidth=1.2, zorder=3)

    ax.text(0, t1 + 1.8, f"{t1:.1f}%", ha="center", fontsize=8.5,
            color=PALETTE["soft_black"], fontweight="bold")
    ax.text(1, t2 + 1.8, f"{t2:.1f}%", ha="center", fontsize=8.5,
            color=PALETTE["soft_black"], fontweight="bold")
    ax.text(0.5, (t1 + t2) / 2 - 4, f"delta = {t2 - t1:+.1f}pp",
            ha="center", fontsize=8, fontstyle="italic", color=PALETTE["soft_black"])

    ax.set_xticks([0, 1])
    ax.set_xticklabels([f"{T1}\n(29 Apr)", f"{T2}\n(7 May)"])
    ax.set_xlim(-0.3, 1.3)
    ax.set_ylim(0, max(t1, t2) * 1.45)
    ax.set_ylabel("Mint gross Presence (%)")
    ax.legend(loc="lower left", frameon=False, fontsize=7)

    # Use standard helpers — chart 4 follows the same layout pattern as the
    # rest of the suite, just at a smaller width since it shows only two
    # data points. Two-line tick labels still fit because standard_bottom
    # reserves 65pt below axes for x-axis content + source block.
    fig.subplots_adjust(left=0.16, right=0.96,
                        top=standard_top(fig), bottom=standard_bottom(fig))
    add_title_subtitle(fig,
                       "Mint persists at gross Presence: H4 stability",
                       f"{t1:.1f}% to {t2:.1f}% (delta {t2-t1:+.1f}pp; within +/-5pp band)")
    add_source_line(fig,
                    "H4 Mint gross Presence in personal finance, n=96 per wave")
    save(fig, "chart_v09_h4_mint_persistence_4col.pdf")


# ===========================================================================
# Chart 5 — H5 Pattern 4 sensitivity
# ===========================================================================

def chart_h5_pattern4_sensitivity(data):
    fig, ax = plt.subplots(figsize=(7.50, 4.40))

    olive_rows = filter_matched(data[("oliveoil", "v09")]["rows"])
    olive_reg = data[("oliveoil", "v09")]["registry"]
    olive_bp = per_brand_presence(olive_rows, olive_reg)

    skin_rows = filter_matched(data[("skincare", "v09")]["rows"])
    skin_reg = data[("skincare", "v09")]["registry"]
    skin_bp = per_brand_presence(skin_rows, skin_reg)

    spanish_strict = ["Castillo de Canena", "Núñez de Prado"]
    spanish_strict_in = [b for b in spanish_strict if b in olive_bp]
    strict_agg = sum(olive_bp[b] for b in spanish_strict_in) / len(spanish_strict_in) if spanish_strict_in else 0

    spanish_inclusive = spanish_strict + ["Graza"]
    spanish_inclusive_in = [b for b in spanish_inclusive if b in olive_bp]
    incl_agg = sum(olive_bp[b] for b in spanish_inclusive_in) / len(spanish_inclusive_in) if spanish_inclusive_in else 0

    kbeauty_brands = ["Beauty of Joseon"]
    kbeauty_in = [b for b in kbeauty_brands if b in skin_bp]
    kbeauty_agg = sum(skin_bp[b] for b in kbeauty_in) / len(kbeauty_in) if kbeauty_in else 0

    bars = [
        ("Spanish olive oil\n(strict, n=2)", strict_agg, SPANISH_OLIVE_OIL_THRESHOLD_PCT, PALETTE["indigo"]),
        ("Spanish olive oil\n(+ Graza, n=3)", incl_agg, SPANISH_OLIVE_OIL_THRESHOLD_PCT, PALETTE["indigo_50"]),
        ("K-beauty skincare\n(n=1)", kbeauty_agg, KBEAUTY_THRESHOLD_PCT, PALETTE["copper"]),
    ]

    xs = list(range(len(bars)))
    ax.bar(xs, [b[1] for b in bars], color=[b[3] for b in bars], width=0.55,
           edgecolor="white", linewidth=0.5)

    # Threshold dashed lines for ALL bars: Spanish 12.5pp on bars 1&2, K-beauty
    # 5pp on bar 3. The 12.5pp line crossing through bar 2 (14.2pp) is the
    # whole point — it's how the reader sees +Graza breaching the threshold.
    for i, (_, _, thr, _) in enumerate(bars):
        ax.hlines(thr, i - 0.32, i + 0.32, colors=PALETTE["soft_black"],
                  linewidth=1.5, linestyles="dashed")

    # ONE label per unique threshold value (not redundant per bar).
    # 12.5pp Spanish: in the gap after bar 2, at threshold height.
    #  5pp K-beauty: right of bar 3's dashed line (xlim extension gives room).
    ax.text(1.34, SPANISH_OLIVE_OIL_THRESHOLD_PCT,
            f"{SPANISH_OLIVE_OIL_THRESHOLD_PCT:.1f}pp threshold",
            va="center", ha="left", fontsize=7.5,
            color=PALETTE["soft_black"], fontstyle="italic")
    ax.text(2.34, KBEAUTY_THRESHOLD_PCT,
            f"{KBEAUTY_THRESHOLD_PCT:.1f}pp threshold",
            va="center", ha="left", fontsize=7.5,
            color=PALETTE["soft_black"], fontstyle="italic")

    for i, (_, val, thr, _) in enumerate(bars):
        passes = val <= thr
        verdict = "passes" if passes else "breach"
        color = PALETTE["soft_black"] if passes else PALETTE["copper"]
        label_y = max(val, thr) + 1.0
        ax.text(i, label_y, f"{val:.1f}pp\n{verdict}", ha="center", va="bottom",
                fontsize=8, fontweight="bold", color=color)

    ax.set_xticks(xs)
    ax.set_xticklabels([b[0] for b in bars], fontsize=8)
    ax.set_ylabel("Aggregate Presence (%)")
    ax.set_ylim(0, 20)
    # Explicit xlim — auto-fit clips at ~2.5, cutting off the "5.0pp
    # threshold" label that sits to the right of the K-beauty bar.
    ax.set_xlim(-0.55, 3.05)

    fig.subplots_adjust(left=0.10, right=0.97,
                        top=standard_top(fig), bottom=standard_bottom(fig))
    add_title_subtitle(fig,
                       "Pattern 4 (v0.6 sec 4.4 refined): discourse-language coverage, not country of origin",
                       "Strict passes both thresholds; +Graza breaches Spanish 12.5pp.")
    add_source_line(fig,
                    "H5 Pattern 4: Spanish + K-beauty aggregate Presence, n=96 per category")
    save(fig, "chart_v09_h5_pattern4_sensitivity_6col.pdf")


# ===========================================================================
# Chart 6 — H6 cross-model spread Pearson r
# ===========================================================================

def chart_h6_cross_model_spread(data):
    fig, ax = plt.subplots(figsize=(7.50, 4.10))

    rs = []
    for cat in CATEGORIES:
        v06 = data[(cat, "v06")]["rows"]
        v09 = data[(cat, "v09")]["rows"]
        registry = data[(cat, "v09")]["registry"]
        bp_sonnet_v06 = per_brand_presence(filter_slot(v06, "anthropic_sonnet"), registry)
        bp_mini_v06 = per_brand_presence(filter_slot(v06, "openai_mini"), registry)
        bp_sonnet_v09 = per_brand_presence(filter_slot(v09, "anthropic_sonnet"), registry)
        bp_mini_v09 = per_brand_presence(filter_slot(v09, "openai_mini"), registry)
        spread_v06 = [bp_sonnet_v06[b] - bp_mini_v06[b] for b in registry["all_brands"]]
        spread_v09 = [bp_sonnet_v09[b] - bp_mini_v09[b] for b in registry["all_brands"]]
        rs.append((cat, pearson_r(spread_v06, spread_v09)))

    rs.sort(key=lambda kv: kv[1], reverse=True)
    y_pos = list(range(len(rs)))
    labels = [CATEGORY_DISPLAY[c] for c, _ in rs]
    vals = [r for _, r in rs]
    colors = [PALETTE["indigo"] if v >= 0.7 else PALETTE["copper"] for v in vals]

    ax.barh(y_pos, vals, color=colors, height=0.55,
            edgecolor="white", linewidth=0.5)
    ax.axvline(0.7, color=PALETTE["soft_black"], linewidth=1.2, linestyle="dashed")
    ax.text(0.71, -0.55, "0.70 threshold", fontsize=7.5,
            fontstyle="italic", color=PALETTE["soft_black"], va="bottom")

    for i, v in enumerate(vals):
        ax.text(v + 0.012, i, f"{v:.2f}", va="center",
                fontsize=8.5, color=PALETTE["soft_black"], fontweight="bold")

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlim(0, 1.05)
    ax.set_ylim(len(rs) - 0.5, -0.95)
    ax.set_xlabel(f"Pearson r (sonnet-mini spread, {T1} vs {T2})")

    fig.subplots_adjust(left=0.18, right=0.97,
                        top=standard_top(fig), bottom=standard_bottom(fig))
    add_title_subtitle(fig,
                       "Cross-model spread stable in all 5 categories: H6 confirmed (5/5)",
                       f"Pearson r between sonnet-mini per-brand spread at "
                       f"{T1} vs {T2}; threshold 0.7+")
    add_source_line(fig,
                    "H6 cross-model spread (sonnet vs mini), per-brand across 5 categories")
    save(fig, "chart_v09_h6_cross_model_spread_6col.pdf")


# ===========================================================================
# Chart 7 — Post-hoc Pattern 1
# ===========================================================================

def chart_pattern1_spread(data):
    fig, ax = plt.subplots(figsize=(7.50, 4.40))

    spreads_t1 = {}
    spreads_t2 = {}
    for cat in CATEGORIES:
        registry = data[(cat, "v09")]["registry"]
        v06 = data[(cat, "v06")]["rows"]
        v09 = data[(cat, "v09")]["rows"]
        bp_sonnet_v06 = per_brand_presence(filter_slot(v06, "anthropic_sonnet"), registry)
        bp_mini_v06 = per_brand_presence(filter_slot(v06, "openai_mini"), registry)
        bp_sonnet_v09 = per_brand_presence(filter_slot(v09, "anthropic_sonnet"), registry)
        bp_mini_v09 = per_brand_presence(filter_slot(v09, "openai_mini"), registry)
        spreads_t1[cat] = mean(abs(bp_sonnet_v06[b] - bp_mini_v06[b])
                                for b in registry["all_brands"])
        spreads_t2[cat] = mean(abs(bp_sonnet_v09[b] - bp_mini_v09[b])
                                for b in registry["all_brands"])

    cats_sorted = sorted(CATEGORIES, key=lambda c: spreads_t2[c], reverse=True)
    x_pos = list(range(len(cats_sorted)))
    bar_w = 0.38
    t1_vals = [spreads_t1[c] for c in cats_sorted]
    t2_vals = [spreads_t2[c] for c in cats_sorted]

    ax.bar([x - bar_w / 2 for x in x_pos], t1_vals, width=bar_w,
           color=PALETTE["indigo_50"], label=f"{T1} (v0.6)",
           edgecolor="white", linewidth=0.5)
    ax.bar([x + bar_w / 2 for x in x_pos], t2_vals, width=bar_w,
           color=PALETTE["indigo"], label=f"{T2} (v0.9)",
           edgecolor="white", linewidth=0.5)

    for i, (t1, t2) in enumerate(zip(t1_vals, t2_vals)):
        ax.text(i - bar_w / 2, t1 + 0.3, f"{t1:.1f}", ha="center", va="bottom",
                fontsize=7.5, color=PALETTE["soft_black"])
        ax.text(i + bar_w / 2, t2 + 0.3, f"{t2:.1f}", ha="center", va="bottom",
                fontsize=7.5, color=PALETTE["soft_black"], fontweight="bold")

    ax.set_xticks(x_pos)
    ax.set_xticklabels([CATEGORY_DISPLAY[c] for c in cats_sorted], fontsize=8.5)
    ax.set_ylabel("Mean cross-model spread (pp)")
    ax.set_ylim(0, max(max(t1_vals), max(t2_vals)) * 1.30)
    ax.legend(loc="upper right", frameon=False, fontsize=8)

    t1_rank = {c: r for r, c in enumerate(
        sorted(CATEGORIES, key=lambda c: spreads_t1[c], reverse=True), 1)}
    t2_rank = {c: r for r, c in enumerate(cats_sorted, 1)}
    v06_predicted = ["finance", "oliveoil", "pm", "skincare", "running"]
    v06_rank = {c: r for r, c in enumerate(v06_predicted, 1)}
    rho_t1_t2 = spearman_rho(t1_rank, t2_rank, CATEGORIES)
    rho_t2_v06 = spearman_rho(t2_rank, v06_rank, CATEGORIES)

    fig.subplots_adjust(left=0.10, right=0.97,
                        top=standard_top(fig), bottom=standard_bottom(fig))
    add_title_subtitle(fig,
                       "Pattern 1 cross-model spread by category replicates v0.6 ordering (post-hoc)",
                       f"Spearman rho = {rho_t1_t2:.2f} ({T1} vs {T2});  "
                       f"= {rho_t2_v06:.2f} ({T2} vs v0.6 narrative ordering)")
    add_source_line(fig,
                    "Pattern 1 post-hoc: mean |sonnet - mini| spread per category")
    save(fig, "chart_v09_pattern1_spread_6col.pdf")


# ===========================================================================
# Chart 8 — Mode distribution (legend below; needs extra bottom margin)
# ===========================================================================

def chart_mode_distribution(data):
    fig, ax = plt.subplots(figsize=(7.50, 4.80))

    bar_w = 0.38
    x_pos = list(range(len(CATEGORIES)))

    shares_t1 = {}
    shares_t2 = {}
    for cat in CATEGORIES:
        all_rows = load_mode_classified(cat)
        if not all_rows:
            print(f"[mode_chart] no mode_classified data for {cat}", file=sys.stderr)
        t1_rows = [r for r in all_rows
                   if r.get("model_slot") in MATCHED_SUBSET and r.get("wave") == "v06"]
        t2_rows = [r for r in all_rows
                   if r.get("model_slot") in MATCHED_SUBSET and r.get("wave") == "v09"]
        shares_t1[cat] = mode_share(t1_rows)
        shares_t2[cat] = mode_share(t2_rows)
        print(f"[mode_chart] {cat}: t1 n={len(t1_rows)}, t2 n={len(t2_rows)}",
              file=sys.stderr)

    largest_shifts = []
    for cat in CATEGORIES:
        for mode in MODE_ORDER:
            delta = shares_t2[cat][mode] - shares_t1[cat][mode]
            if abs(delta) >= 5:
                largest_shifts.append((cat, mode, delta))
    largest_shifts.sort(key=lambda t: abs(t[2]), reverse=True)
    top_three = largest_shifts[:3]

    for i, cat in enumerate(CATEGORIES):
        bottom = 0
        for mode in MODE_ORDER:
            v = shares_t1[cat][mode]
            ax.bar(i - bar_w / 2, v, bottom=bottom, width=bar_w,
                   color=MODE_COLORS[mode], edgecolor="white", linewidth=0.5,
                   label=mode if i == 0 else None)
            bottom += v
        bottom = 0
        for mode in MODE_ORDER:
            v = shares_t2[cat][mode]
            ax.bar(i + bar_w / 2, v, bottom=bottom, width=bar_w,
                   color=MODE_COLORS[mode], edgecolor="white", linewidth=0.5)
            bottom += v

    ax.set_xticks(x_pos)
    ax.set_xticklabels([CATEGORY_DISPLAY[c] for c in CATEGORIES], fontsize=8.5)
    ax.set_ylabel("Mode share (%)")
    ax.set_ylim(0, 100)

    if top_three:
        shifts_str = "; ".join(
            f"{CATEGORY_DISPLAY[c]} {m} {d:+.1f}pp" for c, m, d in top_three
        )
    else:
        shifts_str = "all category-mode shifts within +/-5pp"

    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.10),
              frameon=False, ncol=5, fontsize=8)

    # Need extra bottom margin: legend below axes + two-line source
    # Extra bottom margin: x-axis labels + legend below (bbox_to_anchor=-0.10)
    # + 2-line source. Legend at -10% of axes height eats ~18-22pt; source
    # block 10-26pt; need ~85pt total clearance below axes spine.
    fig.subplots_adjust(left=0.10, right=0.97,
                        top=standard_top(fig), bottom=yb(90, fig))
    add_title_subtitle(fig,
                       "Mode-distribution shifts (matched subset; exploratory, sec 3.8)",
                       f"{T1} left, {T2} right per category. Largest shifts: {shifts_str}")
    add_source_line(fig,
                    "Mode-distribution shift: primary_mode share at t1 vs t2, n=96 per category")
    save(fig, "chart_v09_mode_distribution_6col.pdf")


# ===========================================================================
# Chart 9 — Pattern replication matrix (4-row honest-coverage)
# ===========================================================================

def chart_pattern_replication_matrix(data):
    fig, ax = plt.subplots(figsize=(7.50, 5.00))

    spreads_t2 = {}
    for cat in CATEGORIES:
        registry = data[(cat, "v09")]["registry"]
        v09 = data[(cat, "v09")]["rows"]
        bp_sonnet = per_brand_presence(filter_slot(v09, "anthropic_sonnet"), registry)
        bp_mini = per_brand_presence(filter_slot(v09, "openai_mini"), registry)
        spreads_t2[cat] = mean(abs(bp_sonnet[b] - bp_mini[b])
                                for b in registry["all_brands"])

    p4_values = {
        "pm": None, "running": None,
        "oliveoil": ("11.5pp", True),
        "skincare": ("1.0pp", True),
        "finance": None,
    }
    p6_values = {
        "pm": None, "running": None, "oliveoil": None, "skincare": None,
        "finance": ("41.7%", True),
    }

    brand_mode_share = {}
    for cat in CATEGORIES:
        all_rows = load_mode_classified(cat)
        t2_rows = [r for r in all_rows
                   if r.get("model_slot") in MATCHED_SUBSET and r.get("wave") == "v09"]
        share = mode_share(t2_rows)
        brand_mode_share[cat] = share["brand"]

    n_rows = 4
    n_cols = len(CATEGORIES)
    row_labels = [
        "Pattern 1\ncross-model\nspread",
        "Pattern 4\ndiscourse-\nlanguage bias",
        "Pattern 6\nphantom-\nbrand",
        "Brand-mode\nshare at $t_2$",
    ]
    p1_min, p1_max = 5.0, 18.0
    mode_min, mode_max = 0.0, 80.0

    for i in range(n_rows):
        for j, cat in enumerate(CATEGORIES):
            y = n_rows - 1 - i
            if i == 0:
                val = spreads_t2[cat]
                alpha = min(1.0, max(0.20, (val - p1_min) / (p1_max - p1_min)))
                color = PALETTE["indigo"]
                cell_text = f"{val:.1f}pp"
            elif i == 1:
                v = p4_values[cat]
                if v is None:
                    color = PALETTE["black_20"]; alpha = 0.30
                    cell_text = "not in\nscope"
                else:
                    color = PALETTE["copper"]; alpha = 0.85
                    cell_text = f"confirmed\n{v[0]}"
            elif i == 2:
                v = p6_values[cat]
                if v is None:
                    color = PALETTE["black_20"]; alpha = 0.30
                    cell_text = "not in\nscope"
                else:
                    color = PALETTE["copper"]; alpha = 0.85
                    cell_text = f"confirmed\n{v[0]}"
            else:
                val = brand_mode_share[cat]
                alpha = min(1.0, max(0.20, (val - mode_min) / (mode_max - mode_min)))
                color = PALETTE["indigo"]
                cell_text = f"{val:.0f}%"

            rect = Rectangle((j, y), 1, 1,
                             facecolor=color, alpha=alpha,
                             edgecolor="white", linewidth=2.5)
            ax.add_patch(rect)
            text_color = "white" if alpha > 0.55 else PALETTE["soft_black"]
            ax.text(j + 0.5, y + 0.5, cell_text,
                    ha="center", va="center", fontsize=8.5,
                    color=text_color, fontweight="bold")

    ax.set_xlim(0, n_cols)
    ax.set_ylim(0, n_rows)
    ax.set_xticks([j + 0.5 for j in range(n_cols)])
    ax.set_xticklabels([CATEGORY_DISPLAY[c] for c in CATEGORIES], fontsize=8.5)
    ax.set_yticks([n_rows - 1 - i + 0.5 for i in range(n_rows)])
    ax.set_yticklabels(row_labels, fontsize=8.5)
    ax.tick_params(left=False, bottom=False)
    ax.xaxis.tick_top()
    for spine in ax.spines.values():
        spine.set_visible(False)

    fig.subplots_adjust(left=0.18, right=0.97,
                        top=yt(70, fig), bottom=standard_bottom(fig))
    add_title_subtitle(fig,
                       "v0.6 pattern replication matrix at v0.9 (matched subset)",
                       "Cell intensity proportional to magnitude. "
                       "Patterns 2, 3, 5 not directly measured at v0.9 "
                       "(noted in sec 7 future research).")
    add_source_line(fig,
                    "Pattern replication matrix: v0.6 Patterns 1/4/6 + brand-mode share at t2")
    save(fig, "chart_v09_pattern_matrix_6col.pdf")


def build_all():
    print(f"[charts] loading data from analyze_v09...", file=sys.stderr)
    data = load_all_data()
    chart_h1_drift_scatter(data)
    chart_h2_leaderboard(data)
    chart_h3_within_cat_variance(data)
    chart_h4_mint_persistence(data)
    chart_h5_pattern4_sensitivity(data)
    chart_h6_cross_model_spread(data)
    chart_pattern1_spread(data)
    chart_mode_distribution(data)
    chart_pattern_replication_matrix(data)
    print(f"[charts] done. 9 PDFs in {OUTPUT_DIR}", file=sys.stderr)


if __name__ == "__main__":
    build_all()
