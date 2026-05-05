"""
Pattern 2 — Small-multiples version.

ALTERNATIVE FORM. The primary Pattern 2 chart (`pattern_2_asymmetry.py`)
uses a single-panel hero scatter with right-margin annotation column.
This file holds the small-multiples version: a 2×3 grid of category
panels, with the 6th cell holding a "How to read" legend.

Both forms render to chart_p2_6col.pdf if run directly. To keep both
available without overwriting, this version saves to:
    reports/output/chart_p2_6col_smallmultiples.pdf

Why two forms?
- Hero form: shows ALL brands on one set of axes; cross-category
  positions directly comparable; margin annotations for the 14 most
  asymmetric brands. Better for a single-glance impression.
- Small-multiples form: each category in its own panel; cross-category
  claim shown by repetition of the same upper-left/lower-right pattern
  across all 5 panels. Better for systematic per-category reading.

Use whichever fits the report layout best. If unsure, start with the
hero (it's the canonical 6-col chart slot).

Renders to: reports/output/chart_p2_6col_smallmultiples.pdf
"""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

_THIS = Path(__file__).resolve()
_REPORTS = _THIS.parent.parent
if str(_REPORTS) not in sys.path:
    sys.path.insert(0, str(_REPORTS))

import chart_style as cs
import chart_utils as cu
import chart_data as cd


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PANEL_ORDER = ["PM", "Running", "Olive Oil", "Skincare", "Finance"]

CATEGORY_SHORT_LABELS = {
    "PM":        "PM Software",
    "Running":   "Running Shoes",
    "Olive Oil": "Olive Oil",
    "Skincare":  "Skincare",
    "Finance":   "Personal Finance",
}

# Per-panel labeling
LABELS_PER_PANEL = 2
LABEL_DISTANCE_THRESHOLD = 25

# Aggressive jitter — small panels need ring spread of ~6pt to separate dots
JITTER_THRESHOLD = 3.0
JITTER_SPREAD = 6.0

# CEP labels — all-caps in v0.6 enriched data
COMPARISON_CEPS = {"COMPARISON", "Comparison", "comparison", "compare", "Compare"}
DISCOVERY_CEPS = {"DISCOVERY", "Discovery", "discovery", "discover", "Discover"}

DOT_SIZE = 35
DOT_SIZE_LABELED = 60

SOURCE_TEXT = "Source: Third System AI Presence Index v0.6 · n=96 per category · 30 Apr 2026"


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

def get_pattern2_data() -> list[dict]:
    aias_root = _REPORTS.parent
    original_cwd = Path.cwd()
    try:
        import os
        os.chdir(aias_root)
        leaderboards, _ = cd.load_all_categories()

        tier_by_brand: dict[str, dict[str, str]] = {}
        for cat, brand_rows in leaderboards.items():
            tier_by_brand[cat] = {r["brand"]: r.get("tier", "") for r in brand_rows}

        all_rows = []
        for cat in PANEL_ORDER:
            if cat not in leaderboards:
                continue
            cep_counts, cep_runs = cd.cep_brand_counts_for_category(cat)
            if not cep_counts:
                continue

            comp_counts = defaultdict(int)
            comp_runs = 0
            disc_counts = defaultdict(int)
            disc_runs = 0
            for cep, brand_counts in cep_counts.items():
                if cep in COMPARISON_CEPS:
                    comp_runs += cep_runs[cep]
                    for b, c in brand_counts.items():
                        comp_counts[b] += c
                elif cep in DISCOVERY_CEPS:
                    disc_runs += cep_runs[cep]
                    for b, c in brand_counts.items():
                        disc_counts[b] += c

            if comp_runs == 0 or disc_runs == 0:
                print(f"  [warn] {cat}: missing Comparison/Discovery CEP — skipping")
                continue

            all_brands = set(comp_counts.keys()) | set(disc_counts.keys())
            for brand in all_brands:
                tier = tier_by_brand.get(cat, {}).get(brand, "challenger") or "challenger"
                overall = next(
                    (float(r["presence"]) for r in leaderboards[cat]
                     if r["brand"] == brand), 0.0)
                all_rows.append({
                    "brand": brand,
                    "category_key": cat,
                    "tier": tier,
                    "comparison_pct": 100.0 * comp_counts.get(brand, 0) / comp_runs,
                    "discovery_pct": 100.0 * disc_counts.get(brand, 0) / disc_runs,
                    "overall_presence": overall,
                })
    finally:
        os.chdir(original_cwd)

    return all_rows


# ---------------------------------------------------------------------------
# Per-panel rendering
# ---------------------------------------------------------------------------

def _render_panel(ax, rows: list[dict], category_label: str, sizes: dict) -> None:
    rows = [r for r in rows
            if r["comparison_pct"] > 0 or r["discovery_pct"] > 0]
    if not rows:
        ax.text(50, 50, "no data",
                ha="center", va="center", fontsize=sizes["axis_tick"],
                color=cs.COLOR_MUTED)
        return

    ax.set_xlim(-3, 105)
    ax.set_ylim(-3, 105)
    ax.set_xticks([0, 50, 100])
    ax.set_yticks([0, 50, 100])

    cu.add_diagonal_reference(ax, color=cs.BLACK_20,
                              linewidth=0.5, linestyle="--",
                              lo=0, hi=100)

    # Per-panel jitter
    raw_x = np.array([r["comparison_pct"] for r in rows])
    raw_y = np.array([r["discovery_pct"] for r in rows])
    jit_x, jit_y = cu.jitter_overlapping_points(
        raw_x, raw_y,
        threshold=JITTER_THRESHOLD,
        spread=JITTER_SPREAD,
    )
    for r, jx, jy in zip(rows, jit_x, jit_y):
        r["_plot_x"] = float(jx)
        r["_plot_y"] = float(jy)

    def _asymmetry(r):
        return abs(r["discovery_pct"] - r["comparison_pct"])
    candidates = sorted(
        [r for r in rows if _asymmetry(r) >= LABEL_DISTANCE_THRESHOLD],
        key=_asymmetry, reverse=True,
    )
    labeled_brands = {r["brand"] for r in candidates[:LABELS_PER_PANEL]}

    by_tier = defaultdict(list)
    for r in rows:
        tk = r["tier"].lower().strip().replace("-", "").replace(" ", "")
        if tk not in {"incumbent", "midtier", "challenger"}:
            tk = "challenger"
        by_tier[tk].append(r)

    for tier_key, color in [("midtier", cs.COLOR_MIDTIER),
                            ("incumbent", cs.COLOR_INCUMBENT),
                            ("challenger", cs.COLOR_CHALLENGER)]:
        trows = by_tier.get(tier_key, [])
        if not trows:
            continue
        comp = [r["_plot_x"] for r in trows]
        disc = [r["_plot_y"] for r in trows]
        s = [DOT_SIZE_LABELED if r["brand"] in labeled_brands else DOT_SIZE
             for r in trows]
        ax.scatter(comp, disc, s=s, c=color,
                   edgecolors=cs.COLOR_TEXT, linewidths=0.4,
                   alpha=0.85, zorder=3)

    label_texts = []
    for r in rows:
        if r["brand"] not in labeled_brands:
            continue
        if r["_plot_x"] >= 80:
            x_offset = -1.5; ha = "right"
        else:
            x_offset = 1.5; ha = "left"
        t = ax.text(r["_plot_x"] + x_offset,
                    r["_plot_y"] + 1.5,
                    r["brand"],
                    fontsize=sizes["data_label"],
                    color=cs.COLOR_TEXT,
                    ha=ha, va="bottom",
                    fontweight="bold", zorder=5)
        label_texts.append(t)

    cu.resolve_label_collisions(label_texts, ax=ax,
                                force_text=(0.6, 1.0),
                                force_points=(0.4, 0.6),
                                expand_text=(1.05, 1.2),
                                expand_points=(1.2, 1.4))

    ax.set_title(category_label,
                 fontsize=sizes["subtitle"], fontweight="bold",
                 color=cs.COLOR_TEXT, loc="left", pad=4)

    cs.style_axis_minimal(ax, orientation="scatter")
    ax.set_aspect("equal", adjustable="box")


# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------

def render(output_dir: Path | str | None = None) -> list[Path]:
    rows = get_pattern2_data()
    if not rows:
        raise RuntimeError(
            "No Pattern 2 data found. Need results_enriched_*.csv files."
        )

    rows_by_cat: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        rows_by_cat[r["category_key"]].append(r)

    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=cs.FIGSIZE_6COL_TALL)
    sizes = cs.font_sizes_for("6col")

    fig.subplots_adjust(top=0.85, bottom=0.09,
                        left=0.075, right=0.97,
                        hspace=0.42, wspace=0.22)

    flat_axes = axes.flatten()
    for i, cat_key in enumerate(PANEL_ORDER):
        _render_panel(flat_axes[i], rows_by_cat.get(cat_key, []),
                      CATEGORY_SHORT_LABELS[cat_key], sizes)

    legend_ax = flat_axes[5]; legend_ax.set_axis_off()
    from matplotlib.lines import Line2D
    legend_elems = [
        Line2D([0], [0], marker="o", color="w",
               markerfacecolor=cs.COLOR_INCUMBENT,
               markeredgecolor=cs.COLOR_TEXT, markeredgewidth=0.4,
               markersize=11, label="Incumbent\nheritage market leader"),
        Line2D([0], [0], marker="o", color="w",
               markerfacecolor=cs.COLOR_MIDTIER,
               markeredgecolor=cs.COLOR_TEXT, markeredgewidth=0.4,
               markersize=11, label="Mid-tier\nestablished, smaller share"),
        Line2D([0], [0], marker="o", color="w",
               markerfacecolor=cs.COLOR_CHALLENGER,
               markeredgecolor=cs.COLOR_TEXT, markeredgewidth=0.4,
               markersize=11, label="Challenger\nDTC, niche, or emerging"),
        Line2D([0], [0], color=cs.BLACK_20, linewidth=0.8, linestyle="--",
               label="y = x reference\nequal in both frames"),
    ]
    legend_ax.legend(
        handles=legend_elems, loc="center left",
        bbox_to_anchor=(0.0, 0.5),
        fontsize=sizes["legend"], frameon=False,
        title="How to read",
        title_fontsize=sizes["axis_label"],
        labelspacing=1.4, handletextpad=0.8,
    )

    fig.text(0.5, 0.055,
             "Comparison Presence (%) — forced choice across category",
             ha="center", va="bottom",
             fontsize=sizes["axis_label"], color=cs.COLOR_TEXT)
    fig.text(0.012, 0.5,
             "Discovery Presence (%) — emerging-brand prompts",
             ha="left", va="center", rotation=90,
             fontsize=sizes["axis_label"], color=cs.COLOR_TEXT)

    fig.text(0.075, 0.97,
             "The AI's answer depends on the question",
             fontsize=sizes["title"], fontweight="bold",
             color=cs.COLOR_TEXT, ha="left", va="top")
    fig.text(0.075, 0.935,
             "Brands above the diagonal surface more in Discovery prompts; "
             "below it, more in Comparison.",
             fontsize=sizes["subtitle"], color=cs.COLOR_MUTED,
             ha="left", va="top")
    fig.text(0.075, 0.91,
             "The asymmetry pattern repeats across all five categories.",
             fontsize=sizes["subtitle"], color=cs.COLOR_MUTED,
             ha="left", va="top")
    fig.text(0.075, 0.018, SOURCE_TEXT,
             fontsize=sizes["source_caption"], color=cs.COLOR_MUTED,
             style="italic", ha="left", va="bottom")

    if output_dir is None:
        output_dir = _REPORTS / "output"
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    # NOTE: distinct filename so it doesn't overwrite the hero version
    output_pdf = output_dir / "chart_p2_6col_smallmultiples.pdf"
    fig.savefig(output_pdf, dpi=cs.DPI_PRINT, pad_inches=cs.PAD_INCHES)
    plt.close(fig)
    return [output_pdf]


if __name__ == "__main__":
    paths = render()
    print(f"Rendered Pattern 2 (small-multiples version):")
    for p in paths:
        print(f"  {p}")
