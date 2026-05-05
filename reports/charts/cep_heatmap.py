"""
Pattern 5 — Default Reinforcement intensity across discourse-prompt alignment.

Brand × CEP heatmap. Rows = top 8 brands in the featured category,
columns = 6 CEPs. Cell intensity (Indigo gradient) = mention rate
(0–100%) for that brand in that CEP. Cells annotated with the rate
when ≥10% to keep low-noise cells clean.

The editorial claim: rows that are UNIFORMLY DARK across all CEPs
indicate Default Reinforcement — the same brands surface regardless
of prompt frame. Rows with high variance (dark in some CEPs, light
in others) indicate Conditional Reweighting.

Mode-aware shading infrastructure (mode_style helper in chart_utils)
is wired in but unused in v0.6 because the enriched data does not yet
classify mentions by mode. When the v0.6 → v0.7 enrichment adds a
mode column (brand / component / authority / empty), the per-cell
hatching activates automatically via the MODE_BY_CELL hook.

Featured category: PM Software (cleanest tier separation, full 16-run
coverage across all 6 CEPs).

Renders to: reports/output/chart_p5_3col.pdf  (3-column inline chart)

Brand spec: third_system_brand.json schema 1.4
Data source: most-recent results_enriched_*.csv, scoped to PM
"""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
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

FEATURED_CATEGORY = "PM"
FEATURED_CATEGORY_LABEL = "PM Software"
TOP_N_BRANDS = 8

# CEP display order — left to right reflects rough "discourse intensity":
# Functional/Comparison are most direct; Identity/Discovery are most
# inferential. This ordering makes Default Reinforcement visually obvious
# (uniform darkness across all columns).
#
# Each CEP is matched by its leading word (case-insensitive) so we accept
# both ALL_CAPS_WITH_UNDERSCORES (real v0.6 data — "FUNCTIONAL_WHY") and
# Title Case (older test data — "Functional").
CEP_ORDER = [
    "FUNCTIONAL_WHY",
    "COMPARISON",
    "CONSTRAINT_WITH",
    "CONTEXTUAL_WHEN",
    "DISCOVERY",
    "IDENTITY_HOW_FEELING",
]
CEP_DISPLAY_LABELS = {
    "FUNCTIONAL_WHY":         "Functional",
    "COMPARISON":             "Comparison",
    "CONSTRAINT_WITH":        "Constraint",
    "CONTEXTUAL_WHEN":        "Contextual",
    "DISCOVERY":              "Discovery",
    "IDENTITY_HOW_FEELING":   "Identity",
}

# Resolve "Functional" or "FUNCTIONAL_WHY" or "functional" to the same
# canonical key. Used to sort observed CEPs into CEP_ORDER regardless of
# the source data's casing convention.
def _cep_canonical_key(observed_cep: str) -> str | None:
    """Return the CEP_ORDER key matching observed_cep, or None."""
    if not observed_cep:
        return None
    head = observed_cep.upper().split("_")[0]  # "FUNCTIONAL_WHY" -> "FUNCTIONAL"
    head = head.split()[0]                      # "Functional why" -> "FUNCTIONAL"
    for canonical in CEP_ORDER:
        if canonical.split("_")[0] == head:
            return canonical
    return None

# Cell annotation threshold — only label cells ≥ this percent
ANNOTATION_THRESHOLD = 10

# Default Reinforcement criteria — bold the brand label when both:
#   - spread (max - min mention rate across CEPs) < SPREAD_THRESHOLD
#   - mean mention rate >= MEAN_THRESHOLD
# A "reinforced" brand has consistent visibility across all prompt frames.
# Tune these to match how your real data clusters.
DEFAULT_REINFORCEMENT_SPREAD_THRESHOLD = 35  # percentage points
DEFAULT_REINFORCEMENT_MEAN_THRESHOLD = 40    # percentage points

# v0.7 hook: when enriched data ships per-cell mode classification,
# populate this dict and the chart will pick up hatching automatically.
# Format: {(brand, cep): "brand"|"component"|"authority"|"empty"}
MODE_BY_CELL: dict[tuple[str, str], str] = {}

SOURCE_TEXT = "Source: Third System AI Presence Index v0.6 · n=96 · 30 Apr 2026"


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

def get_pattern5_data(category: str = FEATURED_CATEGORY) -> dict:
    """Load CEP-level mention rates for the featured category.

    Returns a dict:
      {
        "brands": [list of top-N brand names],
        "ceps":   [list of CEPs in display order],
        "matrix": np.ndarray of shape (N, M) with mention rates 0–100,
        "n_runs_per_cep": {cep: int},
      }
    """
    aias_root = _REPORTS.parent
    original_cwd = Path.cwd()
    try:
        import os
        os.chdir(aias_root)
        cep_counts, cep_runs = cd.cep_brand_counts_for_category(category)
    finally:
        os.chdir(original_cwd)

    if not cep_counts:
        raise RuntimeError(f"No CEP data for category {category}")

    # Map observed CEP keys to canonical keys (handles both casing conventions)
    canonical_cep_counts: dict[str, dict[str, int]] = {}
    canonical_cep_runs: dict[str, int] = {}
    for observed_cep, brand_counts in cep_counts.items():
        canonical = _cep_canonical_key(observed_cep)
        if canonical is None:
            print(f"  [warn] Pattern 5: unrecognized CEP '{observed_cep}' — skipping")
            continue
        # Merge counts under canonical key (handles duplicates if any)
        if canonical not in canonical_cep_counts:
            canonical_cep_counts[canonical] = defaultdict(int)
            canonical_cep_runs[canonical] = 0
        for b, c in brand_counts.items():
            canonical_cep_counts[canonical][b] += c
        canonical_cep_runs[canonical] += cep_runs[observed_cep]

    # Compute total mentions per brand to pick top-N
    total_by_brand = defaultdict(int)
    for cep, brand_counts in canonical_cep_counts.items():
        for b, c in brand_counts.items():
            total_by_brand[b] += c
    top_brands = sorted(total_by_brand, key=total_by_brand.get, reverse=True)[:TOP_N_BRANDS]

    # Filter CEPs to ones present in this category, in display order
    present_ceps = [c for c in CEP_ORDER if c in canonical_cep_counts]

    # Build matrix
    n_brands = len(top_brands)
    n_ceps = len(present_ceps)
    matrix = np.zeros((n_brands, n_ceps), dtype=float)
    for i, brand in enumerate(top_brands):
        for j, cep in enumerate(present_ceps):
            count = canonical_cep_counts[cep].get(brand, 0)
            runs = canonical_cep_runs[cep]
            if runs > 0:
                matrix[i, j] = 100.0 * count / runs

    return {
        "brands": top_brands,
        "ceps": present_ceps,
        "matrix": matrix,
        "n_runs_per_cep": dict(canonical_cep_runs),
    }


# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------

def render(output_dir: Path | str | None = None) -> list[Path]:
    """Render Pattern 5 CEP heatmap."""
    data = get_pattern5_data(FEATURED_CATEGORY)
    brands = data["brands"]
    ceps = data["ceps"]
    matrix = data["matrix"]

    # 3-column inline figsize per brand spec
    fig, ax = plt.subplots(figsize=cs.FIGSIZE_3COL_INLINE)
    sizes = cs.font_sizes_for("3col_inline")

    # Manual margins — heatmap needs no horizontal grid; bottom for x-tick
    # rotation, left for brand labels, top for title/subtitle
    fig.subplots_adjust(
        top=0.74,        # leave room for title + 2-line subtitle ABOVE the matrix
        bottom=0.26,     # rotated CEP labels + source line
        left=0.24,       # brand labels (longest: "GitHub Projects")
        right=0.88,      # leave room for colorbar
    )

    # Colormap: white → ACCENT_INDIGO. Use light grey for zero so empty
    # cells are visually distinct from low-mention cells.
    cmap = mcolors.LinearSegmentedColormap.from_list(
        "indigo_intensity",
        [cs.BLACK_10, cs.ACCENT_INDIGO],
        N=256,
    )

    n_brands, n_ceps = matrix.shape

    # Draw heatmap manually (instead of imshow) so we can apply per-cell
    # mode hatching when the v0.7 data lands.
    norm = mcolors.Normalize(vmin=0, vmax=100)
    for i in range(n_brands):
        for j in range(n_ceps):
            value = matrix[i, j]
            face = cmap(norm(value))
            mode = MODE_BY_CELL.get((brands[i], ceps[j]), "brand")
            style_kwargs = cu.mode_style(mode)
            rect = plt.Rectangle(
                (j, n_brands - 1 - i),  # invert y so first brand is on top
                1, 1,
                facecolor=face,
                edgecolor=cs.COLOR_PAPER if not style_kwargs.get("edgecolor") else style_kwargs["edgecolor"],
                linewidth=0.6,
                hatch=style_kwargs.get("hatch"),
                zorder=2,
            )
            ax.add_patch(rect)

            # Annotate cells ≥ threshold with their value.
            # Text color flips with cell intensity for legibility.
            if value >= ANNOTATION_THRESHOLD:
                text_color = cs.COLOR_PAPER if value >= 55 else cs.COLOR_TEXT
                ax.text(
                    j + 0.5, n_brands - 1 - i + 0.5,
                    f"{int(round(value))}",
                    ha="center", va="center",
                    fontsize=sizes["data_label"],
                    color=text_color,
                    fontweight="bold" if value >= 55 else "normal",
                    zorder=3,
                )

    # Axes setup
    ax.set_xlim(0, n_ceps)
    ax.set_ylim(0, n_brands)
    # Note: no set_aspect("equal") here — cells fill available area
    # rectangularly. Square cells would force the matrix to shrink to fit
    # the most constrained dimension, leaving large empty space.

    # CEP labels at bottom
    ax.set_xticks(np.arange(n_ceps) + 0.5)
    ax.set_xticklabels(
        [CEP_DISPLAY_LABELS.get(c, c) for c in ceps],
        rotation=35, ha="right", fontsize=sizes["axis_tick"],
        color=cs.COLOR_TEXT,
    )
    ax.tick_params(axis="x", which="both", length=0, pad=2)

    # Brand labels on left — first brand at top
    ax.set_yticks(np.arange(n_brands) + 0.5)
    ax.set_yticklabels(
        list(reversed(brands)),
        fontsize=sizes["axis_tick"], color=cs.COLOR_TEXT,
    )
    ax.tick_params(axis="y", which="both", length=0, pad=2)

    # Identify Default Reinforcement signature brands (low spread + high mean)
    spreads = matrix.max(axis=1) - matrix.min(axis=1)
    means = matrix.mean(axis=1)
    reinforced_idx = [i for i in range(n_brands)
                      if spreads[i] < DEFAULT_REINFORCEMENT_SPREAD_THRESHOLD
                      and means[i] >= DEFAULT_REINFORCEMENT_MEAN_THRESHOLD]
    # Bold the y-tick labels for reinforced brands
    for i, label in enumerate(ax.get_yticklabels()):
        # Reverse-mapped index since labels are in reversed order
        original_i = n_brands - 1 - i
        if original_i in reinforced_idx:
            label.set_fontweight("bold")
            label.set_color(cs.ACCENT_INDIGO)

    # Hide all spines and gridlines
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(False)

    # Colorbar — placed to the right of the heatmap
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar_ax = fig.add_axes([0.90, 0.26, 0.022, 0.48])
    cbar = fig.colorbar(sm, cax=cbar_ax)
    cbar.set_ticks([0, 25, 50, 75, 100])
    cbar.set_ticklabels(["0", "25", "50", "75", "100%"])
    cbar.ax.tick_params(labelsize=sizes["axis_tick"], length=0, pad=2)
    cbar.outline.set_visible(False)

    # Title + 2-line subtitle (3-col widths: ≤45 chars per line)
    fig.text(
        0.04, 0.96,
        "Default Reinforcement signature",
        fontsize=sizes["title"], fontweight="bold",
        color=cs.COLOR_TEXT, ha="left", va="top",
    )
    fig.text(
        0.04, 0.90,
        f"{FEATURED_CATEGORY_LABEL}: top {TOP_N_BRANDS} brands × 6 CEPs",
        fontsize=sizes["subtitle"], color=cs.COLOR_MUTED,
        ha="left", va="top",
    )
    fig.text(
        0.04, 0.85,
        "Bold rows = brands surfacing across all CEPs.",
        fontsize=sizes["subtitle"], color=cs.COLOR_MUTED,
        ha="left", va="top",
    )

    # Source line
    fig.text(
        0.04, 0.025, SOURCE_TEXT,
        fontsize=sizes["source_caption"], color=cs.COLOR_MUTED,
        style="italic", ha="left", va="bottom",
    )

    # Save (no bbox='tight' — would eat the reserved colorbar margin)
    if output_dir is None:
        output_dir = _REPORTS / "output"
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_pdf = output_dir / "chart_p5_3col.pdf"
    fig.savefig(output_pdf, dpi=cs.DPI_PRINT, pad_inches=cs.PAD_INCHES)
    plt.close(fig)
    return [output_pdf]


if __name__ == "__main__":
    paths = render()
    print(f"Rendered Pattern 5 (CEP heatmap, {FEATURED_CATEGORY_LABEL}):")
    for p in paths:
        print(f"  {p}")
