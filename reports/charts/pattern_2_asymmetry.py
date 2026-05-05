"""
Pattern 2 — The AI's answer depends on the question.

Reconstruction of the original parallel-chat hero scatter at the locked
brand-spec dimensions (7.5 × 6.5). The original was 9.5 × 8.0 with
annotation callouts in a right-side margin column — same approach,
scaled to fit the 6-column hero TALL profile.

Form: single-panel scatter occupying the LEFT ~65% of the figure.
The remaining RIGHT ~35% is an annotation column where labeled brands
get leader lines connecting their dot to a brief annotation in the
margin. This solves the density problem differently than small
multiples: instead of breaking the chart into 5 panels, it uses the
margin as overflow space for the labels that wouldn't fit inline.

Each brand:
  - One dot in the scatter, tier-colored
  - Diagonal y=x reference splits "Discovery-favoring" (above)
    from "Comparison-favoring" (below)
  - The most asymmetric brands get leader lines to a right-margin annotation

Cross-category — all ~80 brands across 5 categories on one set of axes.

Renders to: reports/output/chart_p2_6col.pdf

Brand spec: third_system_brand.json schema 1.4
Data source: results_enriched_*.csv (most-recent per category)
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

CATEGORY_KEYS = ["PM", "Running", "Olive Oil", "Skincare", "Finance"]

# Label policy: top-N most asymmetric brands GLOBALLY get margin annotations.
# Margin column has fixed vertical real estate, so 12-14 labels max.
MAX_ANNOTATIONS = 14
LABEL_DISTANCE_THRESHOLD = 25  # Min asymmetry to qualify

# CEP labels — all-caps in v0.6 enriched data
COMPARISON_CEPS = {"COMPARISON", "Comparison", "comparison", "compare", "Compare"}
DISCOVERY_CEPS = {"DISCOVERY", "Discovery", "discovery", "discover", "Discover"}

# Layout: scatter occupies LEFT portion, annotations occupy RIGHT portion.
# Tuned empirically — leaves a square scatter on left + ~35% margin column.
SCATTER_LEFT_FRAC = 0.08
SCATTER_RIGHT_FRAC = 0.62   # Scatter ends at 62% of fig width
ANNOTATION_LEFT_FRAC = 0.66 # Annotations start at 66% of fig width
ANNOTATION_RIGHT_FRAC = 0.97
SCATTER_BOTTOM_FRAC = 0.10
SCATTER_TOP_FRAC = 0.78  # Leave room for figure-level title/subtitle above

# Jitter for coincident points within the scatter
JITTER_THRESHOLD = 2.5
JITTER_SPREAD = 3.0

DOT_SIZE = 36
DOT_SIZE_LABELED = 70

SOURCE_TEXT = "Source: Third System AI Presence Index v0.6 · n=96 per category · 30 Apr 2026"


# ---------------------------------------------------------------------------
# Data acquisition
# ---------------------------------------------------------------------------

def get_pattern2_data() -> list[dict]:
    """Load enriched data and compute Comparison/Discovery presence per brand."""
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
        for cat in CATEGORY_KEYS:
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
                print(f"  [warn] {cat}: missing Comparison or Discovery CEP "
                      f"data (comp={comp_runs}, disc={disc_runs}) — skipping")
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
# Main render
# ---------------------------------------------------------------------------

def render(output_dir: Path | str | None = None) -> list[Path]:
    """Render Pattern 2 hero scatter with margin annotations."""
    rows = get_pattern2_data()
    if not rows:
        raise RuntimeError(
            "No Pattern 2 data found. Need results_enriched_*.csv files "
            "with Comparison and Discovery CEPs."
        )
    rows = [r for r in rows
            if r["comparison_pct"] > 0 or r["discovery_pct"] > 0]

    # ----- Figure: 6-col TALL (7.5 × 6.5), brand-spec locked -----
    fig = plt.figure(figsize=cs.FIGSIZE_6COL_TALL)
    sizes = cs.font_sizes_for("6col")

    # Manual axes positioning so we can reserve a right margin for annotations
    # [left, bottom, width, height] in figure-relative coords
    scatter_ax = fig.add_axes([
        SCATTER_LEFT_FRAC,
        SCATTER_BOTTOM_FRAC,
        SCATTER_RIGHT_FRAC - SCATTER_LEFT_FRAC,
        SCATTER_TOP_FRAC - SCATTER_BOTTOM_FRAC,
    ])

    # ----- Set scatter axis limits BEFORE diagonal -----
    scatter_ax.set_xlim(-3, 105)
    scatter_ax.set_ylim(-3, 105)
    scatter_ax.set_xticks([0, 20, 40, 60, 80, 100])
    scatter_ax.set_yticks([0, 20, 40, 60, 80, 100])

    cu.add_diagonal_reference(
        scatter_ax,
        color=cs.BLACK_20, linewidth=0.6, linestyle="--",
        lo=0, hi=100,
    )

    # ----- Jitter coincident points -----
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

    # ----- Determine which brands get margin annotations -----
    # Balance the two stacks: top-N most asymmetric in each direction.
    # This prevents one stack from dominating and gives the chart visual
    # symmetry around the diagonal.
    def _asymmetry(r):
        return abs(r["discovery_pct"] - r["comparison_pct"])

    eligible = [r for r in rows if _asymmetry(r) >= LABEL_DISTANCE_THRESHOLD]
    above_eligible = [r for r in eligible
                      if r["discovery_pct"] > r["comparison_pct"]]
    below_eligible = [r for r in eligible
                      if r["discovery_pct"] <= r["comparison_pct"]]

    # Top-N most asymmetric in each direction
    per_stack = MAX_ANNOTATIONS // 2  # 7 each = 14 total
    above_eligible.sort(key=_asymmetry, reverse=True)
    below_eligible.sort(key=_asymmetry, reverse=True)
    above_diag = above_eligible[:per_stack]
    below_diag = below_eligible[:per_stack]

    # CRITICAL: sort each stack by VERTICAL POSITION OF DOT so leader lines
    # don't cross. In each stack, the brand with the highest _plot_y goes
    # at the top of the margin annotation stack.
    above_diag.sort(key=lambda r: r["_plot_y"], reverse=True)
    below_diag.sort(key=lambda r: r["_plot_y"], reverse=True)

    annotated_keys = {(r["brand"], r["category_key"]) for r in above_diag + below_diag}

    # ----- Group by tier and scatter -----
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
        s = [DOT_SIZE_LABELED if (r["brand"], r["category_key"]) in annotated_keys
             else DOT_SIZE for r in trows]
        scatter_ax.scatter(
            comp, disc, s=s, c=color,
            edgecolors=cs.COLOR_TEXT, linewidths=0.4,
            alpha=0.85, zorder=3,
        )

    scatter_ax.set_xlabel("Comparison Presence (%)", fontsize=sizes["axis_label"])
    scatter_ax.set_ylabel("Discovery Presence (%)", fontsize=sizes["axis_label"])
    cs.style_axis_minimal(scatter_ax, orientation="scatter")
    scatter_ax.set_aspect("equal", adjustable="box")

    # ----- Right-margin annotation column -----
    # We're going to stack annotations vertically in the right margin and
    # draw leader lines from each margin annotation back to its dot in
    # the scatter. Annotations split into two stacks:
    #   - Top half: brands ABOVE diagonal (Discovery-favoring) — challengers
    #   - Bottom half: brands BELOW diagonal (Comparison-favoring) — incumbents
    # This makes the asymmetry direction structurally visible.
    # above_diag and below_diag already built above, sorted by _plot_y.

    # Allocate vertical space in figure-relative coords
    annot_y_top = SCATTER_TOP_FRAC - 0.02
    annot_y_bottom = SCATTER_BOTTOM_FRAC + 0.02
    annot_mid = (annot_y_top + annot_y_bottom) / 2.0

    def _place_annotations(brand_list, y_start, y_end, header_text, header_color):
        """Place a stack of annotations vertically between y_start and y_end."""
        if not brand_list:
            return
        n = len(brand_list)
        # Header at top of the stack
        fig.text(
            ANNOTATION_LEFT_FRAC,
            y_start,
            header_text,
            fontsize=sizes["legend"],
            fontweight="bold",
            color=header_color,
            ha="left",
            va="top",
            transform=fig.transFigure,
        )
        # Annotations start below header
        avail = (y_start - 0.025) - y_end
        spacing = avail / max(1, n)
        for i, r in enumerate(brand_list):
            # Y position in figure coords
            ann_fy = y_start - 0.03 - i * spacing
            # Annotation text
            text = f'{r["brand"]}'
            sub = f'{r["comparison_pct"]:.0f}% C  →  {r["discovery_pct"]:.0f}% D'
            fig.text(
                ANNOTATION_LEFT_FRAC + 0.01,
                ann_fy,
                text,
                fontsize=sizes["data_label"],
                fontweight="bold",
                color=cs.COLOR_TEXT,
                ha="left", va="top",
                transform=fig.transFigure,
            )
            fig.text(
                ANNOTATION_LEFT_FRAC + 0.01,
                ann_fy - 0.018,
                sub,
                fontsize=sizes["source_caption"],
                color=cs.COLOR_MUTED,
                ha="left", va="top",
                transform=fig.transFigure,
            )

            # Leader line from annotation back to dot in scatter axes
            # Convert dot data coords -> figure coords
            disp = scatter_ax.transData.transform((r["_plot_x"], r["_plot_y"]))
            dot_fx, dot_fy = fig.transFigure.inverted().transform(disp)

            # Annotation anchor point (left edge of text, mid-height of label)
            anchor_fx = ANNOTATION_LEFT_FRAC
            anchor_fy = ann_fy - 0.005

            # Draw thin leader line in figure coords
            line = plt.Line2D(
                [dot_fx, anchor_fx],
                [dot_fy, anchor_fy],
                transform=fig.transFigure,
                color=cs.BLACK_20,
                linewidth=0.4,
                linestyle="-",
                zorder=1,
            )
            fig.add_artist(line)

    # Place above-diagonal stack in TOP half of margin
    _place_annotations(
        above_diag,
        y_start=annot_y_top,
        y_end=annot_mid + 0.01,
        header_text="DISCOVERY-FAVORING  ↗",
        header_color=cs.COLOR_CHALLENGER,
    )

    # Place below-diagonal stack in BOTTOM half of margin
    _place_annotations(
        below_diag,
        y_start=annot_mid - 0.01,
        y_end=annot_y_bottom,
        header_text="COMPARISON-FAVORING  ↘",
        header_color=cs.COLOR_INCUMBENT,
    )

    # ----- Tier legend (compact, bottom of margin column) -----
    from matplotlib.lines import Line2D
    legend_elems = [
        Line2D([0], [0], marker="o", color="w",
               markerfacecolor=cs.COLOR_INCUMBENT,
               markeredgecolor=cs.COLOR_TEXT, markeredgewidth=0.4,
               markersize=8, label="Incumbent"),
        Line2D([0], [0], marker="o", color="w",
               markerfacecolor=cs.COLOR_MIDTIER,
               markeredgecolor=cs.COLOR_TEXT, markeredgewidth=0.4,
               markersize=8, label="Mid-tier"),
        Line2D([0], [0], marker="o", color="w",
               markerfacecolor=cs.COLOR_CHALLENGER,
               markeredgecolor=cs.COLOR_TEXT, markeredgewidth=0.4,
               markersize=8, label="Challenger"),
    ]
    legend_ax = fig.add_axes([
        ANNOTATION_LEFT_FRAC - 0.02,
        SCATTER_BOTTOM_FRAC - 0.04,
        0.30, 0.04,
    ])
    legend_ax.set_axis_off()
    legend_ax.legend(
        handles=legend_elems,
        loc="center left",
        ncol=3,
        fontsize=sizes["legend"],
        frameon=False,
        handletextpad=0.3,
        columnspacing=1.0,
    )

    # ----- Figure-level title + subtitle -----
    fig.text(
        SCATTER_LEFT_FRAC, 0.96,
        "The AI's answer depends on the question",
        fontsize=sizes["title"], fontweight="bold",
        color=cs.COLOR_TEXT, ha="left", va="top",
    )
    fig.text(
        SCATTER_LEFT_FRAC, 0.92,
        "Brands above the diagonal surface more in Discovery prompts; below it, "
        "more in Comparison.",
        fontsize=sizes["subtitle"],
        color=cs.COLOR_MUTED, ha="left", va="top",
    )
    fig.text(
        SCATTER_LEFT_FRAC, 0.895,
        "Cross-category — every measured brand plotted by its prompt-frame asymmetry.",
        fontsize=sizes["subtitle"],
        color=cs.COLOR_MUTED, ha="left", va="top",
    )

    # ----- Source line -----
    fig.text(
        SCATTER_LEFT_FRAC, 0.025, SOURCE_TEXT,
        fontsize=sizes["source_caption"], color=cs.COLOR_MUTED,
        style="italic", ha="left", va="bottom",
    )

    # ----- Save (no bbox='tight' — would eat reserved margins) -----
    if output_dir is None:
        output_dir = _REPORTS / "output"
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_pdf = output_dir / "chart_p2_6col.pdf"
    fig.savefig(output_pdf, dpi=cs.DPI_PRINT, pad_inches=cs.PAD_INCHES)
    plt.close(fig)
    return [output_pdf]


if __name__ == "__main__":
    paths = render()
    print(f"Rendered Pattern 2 (hero scatter with margin annotations):")
    for p in paths:
        print(f"  {p}")
