"""
chart_utils.py — reusable chart-construction patterns.

Lives alongside chart_style.py. Where chart_style holds brand-spec-derived
constants (colors, figsize, fonts), chart_utils holds the *patterns* that
recur across charts: label-collision resolution, beeswarm spread, mode-aware
cell rendering, highlight helpers, and the canonical save routine.

These are NOT brand-spec material. They're the recurring techniques the
team has developed across earlier sessions and validated empirically.
When a new chart needs adjustText or beeswarm, it imports from here rather
than reinventing the helper.

Importing chart_style as cs is required — these utilities reference brand
constants (ACCENT_INDIGO, BLACK_20, etc.) for default styling.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence
import warnings

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.text import Text

import chart_style as cs


# ---------------------------------------------------------------------------
# adjustText — label collision resolution
# ---------------------------------------------------------------------------
#
# adjustText is the canonical Python library for resolving label overlaps in
# scatter plots, dot plots, and any chart where labeled points cluster. It
# iteratively moves text labels away from each other (and away from points)
# until they no longer overlap.
#
# We wrap it because:
#   1. The default arrowprops are ugly black solid lines; we want subtle gray.
#   2. Most charts want consistent move limits and force tuning.
#   3. Graceful fallback when adjustText isn't installed — we'd rather render
#      a chart with overlapping labels than fail.

try:
    from adjustText import adjust_text
    _ADJUSTTEXT_AVAILABLE = True
except ImportError:
    _ADJUSTTEXT_AVAILABLE = False
    warnings.warn(
        "adjustText not installed. Label-collision helpers will silently "
        "no-op. Install with: pip install adjustText",
        UserWarning,
    )


def resolve_label_collisions(
    texts: list[Text],
    ax: Axes | None = None,
    *,
    arrow_color: str | None = None,
    arrow_lw: float = 0.4,
    expand_points: tuple[float, float] = (1.2, 1.4),
    expand_text: tuple[float, float] = (1.05, 1.2),
    force_text: tuple[float, float] = (0.5, 0.8),
    force_points: tuple[float, float] = (0.4, 0.6),
) -> None:
    """Resolve overlapping text labels using adjustText.

    Pass the list of Text objects returned from ax.annotate() / ax.text()
    calls. The function moves them iteratively to minimize overlap, drawing
    a thin connector line from each label back to its anchor point.

    No-op (with a one-time warning) if adjustText isn't installed.

    Defaults tuned for Third System charts: small point clusters with
    ≤20 labels, moderate force values.
    """
    if not _ADJUSTTEXT_AVAILABLE or not texts:
        return

    if arrow_color is None:
        arrow_color = cs.COLOR_MUTED

    adjust_text(
        texts,
        ax=ax,
        arrowprops=dict(
            arrowstyle="-",
            color=arrow_color,
            lw=arrow_lw,
            alpha=0.6,
        ),
        expand_points=expand_points,
        expand_text=expand_text,
        force_text=force_text,
        force_points=force_points,
        only_move={"points": "y", "text": "xy"},
    )


# ---------------------------------------------------------------------------
# Beeswarm spread — perpendicular jitter for dot plots
# ---------------------------------------------------------------------------

def beeswarm_offsets(
    values: Sequence[float],
    *,
    width: float = 0.4,
    bin_count: int = 20,
) -> np.ndarray:
    """Compute perpendicular offsets for a 1D array of values to avoid overlap.

    Used in dot plots where multiple brands have similar Presence scores
    and need to be spread vertically (or horizontally) to remain readable.

    Algorithm:
      1. Bin the values along the data axis.
      2. Within each bin, alternate offsets above/below the centerline
         outward from zero, scaled to the bin's local density.

    Returns an array of perpendicular offsets, same length as values.
    Center the data around 0 by adding offsets to the brand's category
    position (e.g., y_offset + category_index).

    width: maximum perpendicular spread on either side of center.
    bin_count: granularity of binning along the data axis.
    """
    values = np.asarray(values, dtype=float)
    if len(values) == 0:
        return np.array([])

    # Bin values along the data axis
    vmin, vmax = float(np.min(values)), float(np.max(values))
    if vmax == vmin:
        bins = np.zeros(len(values), dtype=int)
    else:
        bin_edges = np.linspace(vmin, vmax, bin_count + 1)
        bins = np.clip(np.digitize(values, bin_edges) - 1, 0, bin_count - 1)

    offsets = np.zeros(len(values))
    # For each bin, assign alternating offsets within the bin's members
    for bin_idx in range(bin_count):
        members = np.where(bins == bin_idx)[0]
        if len(members) <= 1:
            continue
        # Sort members by their value within the bin (stable spread)
        members_sorted = members[np.argsort(values[members])]
        # Alternating outward: 0, +1, -1, +2, -2, ...
        local_offsets = np.zeros(len(members_sorted))
        for i in range(len(members_sorted)):
            if i == 0:
                local_offsets[i] = 0
            elif i % 2 == 1:
                local_offsets[i] = ((i + 1) // 2) * (width / max(1, len(members_sorted) // 2))
            else:
                local_offsets[i] = -((i + 1) // 2) * (width / max(1, len(members_sorted) // 2))
        offsets[members_sorted] = np.clip(local_offsets, -width, width)

    return offsets


# ---------------------------------------------------------------------------
# 2D jitter for coincident points
# ---------------------------------------------------------------------------

def jitter_overlapping_points(
    xs: Sequence[float],
    ys: Sequence[float],
    *,
    threshold: float = 1.0,
    spread: float = 1.5,
    axis: str = "both",
) -> tuple[np.ndarray, np.ndarray]:
    """Detect 2D-coincident points and spread them around shared center.

    Used for scatter plots where multiple data points share identical or
    near-identical (x, y) values — e.g., 4 brands all scoring 100% in
    Comparison and 100% in Discovery. Without jittering, those 4 dots
    stack on top of each other and only 1 is visible.

    Algorithm:
      1. Cluster points within `threshold` units of each other (axis-aware).
      2. For each cluster of N>1 points, distribute them along a line
         (1D mode) or around a circle (2D mode) around their mean position.

    Args:
        xs: array of x-coordinates
        ys: array of y-coordinates (same length)
        threshold: points within this distance are considered coincident.
                   Units depend on `axis`: for "both" this is Euclidean
                   distance; for "x"/"y" this is along the chosen axis only.
        spread: radius (or half-length) of the spread.
        axis: "both" (2D ring), "y" (1D vertical only — dots fan out along y
              keeping x unchanged), or "x" (1D horizontal only). Use "y" for
              category strip plots where x = data value should not be moved.

    Returns:
        (jittered_xs, jittered_ys) — same shape as input.

    Example (Pattern 4 — strip plot, fan out along y only):
        jx, jy = jitter_overlapping_points(
            xs=presence_values, ys=[row_index]*n,
            threshold=2.5, spread=0.30, axis="y"
        )
        ax.scatter(jx, jy, ...)  # x preserved, y fanned within row
    """
    xs = np.asarray(xs, dtype=float).copy()
    ys = np.asarray(ys, dtype=float).copy()
    if len(xs) == 0:
        return xs, ys

    n = len(xs)
    visited = np.zeros(n, dtype=bool)
    new_xs = xs.copy()
    new_ys = ys.copy()

    for i in range(n):
        if visited[i]:
            continue
        # Find all unvisited points "close" to point i — distance metric
        # depends on axis mode
        cluster = [i]
        for j in range(i + 1, n):
            if visited[j]:
                continue
            if axis == "y":
                # Cluster only by x-distance (we're spreading along y);
                # points with similar x get fanned vertically
                dist = abs(xs[j] - xs[i])
            elif axis == "x":
                dist = abs(ys[j] - ys[i])
            else:
                dist = np.hypot(xs[j] - xs[i], ys[j] - ys[i])
            if dist <= threshold:
                cluster.append(j)
        # Singletons stay put
        if len(cluster) == 1:
            visited[i] = True
            continue
        # Spread cluster
        cx = float(np.mean(xs[cluster]))
        cy = float(np.mean(ys[cluster]))
        m = len(cluster)
        for k, idx in enumerate(cluster):
            if axis == "y":
                # Fan out vertically along y — keep x at cluster mean
                # offsets: -spread, ..., +spread evenly distributed
                if m == 1:
                    offset = 0.0
                else:
                    offset = -spread + (2 * spread) * k / (m - 1)
                new_xs[idx] = xs[idx]  # preserve original x
                new_ys[idx] = cy + offset
            elif axis == "x":
                if m == 1:
                    offset = 0.0
                else:
                    offset = -spread + (2 * spread) * k / (m - 1)
                new_xs[idx] = cx + offset
                new_ys[idx] = ys[idx]  # preserve original y
            else:
                # 2D ring around cluster center
                angle = 2 * np.pi * k / m
                new_xs[idx] = cx + spread * np.cos(angle)
                new_ys[idx] = cy + spread * np.sin(angle)
            visited[idx] = True

    return new_xs, new_ys


# ---------------------------------------------------------------------------
# Mode-aware cell rendering — for the CEP heatmap
# ---------------------------------------------------------------------------
#
# The three response modes (Brand / Component / Authority) are visually
# distinct in the heatmap: solid fill for Brand mode, hatched for Component
# mode, different hatch for Authority. This helper returns the matplotlib
# styling parameters for a given mode classification.

MODE_BRAND = "brand"
MODE_COMPONENT = "component"
MODE_AUTHORITY = "authority"
MODE_EMPTY = "empty"

_MODE_STYLES = {
    MODE_BRAND: dict(hatch=None, edgecolor="none"),
    MODE_COMPONENT: dict(hatch="///", edgecolor=cs.BLACK_60),
    MODE_AUTHORITY: dict(hatch="...", edgecolor=cs.BLACK_60),
    MODE_EMPTY: dict(hatch=None, edgecolor="none"),
}


def mode_style(mode: str) -> dict[str, Any]:
    """Return matplotlib styling kwargs for a response mode.

    mode: 'brand' | 'component' | 'authority' | 'empty'

    Use as: ax.add_patch(Rectangle(..., **mode_style('component')))
    or pass via **mode_style(mode) to bar/scatter calls.

    Brand mode: solid fill, no hatch.
    Component mode: forward-slash hatch (signals 'ingredient/property frame').
    Authority mode: dot hatch (signals 'publication/source frame').
    Empty: same as brand (transparent fill).
    """
    return _MODE_STYLES.get(mode.lower(), _MODE_STYLES[MODE_EMPTY]).copy()


# ---------------------------------------------------------------------------
# Highlight-vs-rest color list — the most-used pattern in the brand spec
# ---------------------------------------------------------------------------

def highlight_colors(
    items: Sequence[str],
    highlight: str | Sequence[str],
    *,
    accent: str | None = None,
    rest: str | None = None,
) -> list[str]:
    """Return a color list with one (or more) highlighted items in accent.

    Default accent is ACCENT_INDIGO; default rest is BLACK_20. This is the
    Third System default chart pattern ("Indigo + grayscale for everything
    else") from the brand spec's qualitative_recommended scheme.

    items: ordered list of item names (e.g., brand names along an axis)
    highlight: single name OR list of names to highlight
    accent: override the highlight color (default ACCENT_INDIGO)
    rest: override the non-highlight color (default BLACK_20)

    Returns: list of hex strings, same length as items.

    Example:
        brands = ["YNAB", "Empower", "Mint", "EveryDollar"]
        colors = highlight_colors(brands, "Mint")
        ax.bar(brands, values, color=colors)
    """
    if accent is None:
        accent = cs.ACCENT_INDIGO
    if rest is None:
        rest = cs.BLACK_20

    if isinstance(highlight, str):
        highlight_set = {highlight}
    else:
        highlight_set = set(highlight)

    return [accent if item in highlight_set else rest for item in items]


def tier_colors_list(tiers: Sequence[str]) -> list[str]:
    """Return a color list mapping each tier to its canonical AIPT color.

    tiers: sequence of 'incumbent' | 'midtier' | 'challenger'
    Returns: list of hex strings, same length as input.

    Example:
        tiers = ["incumbent", "incumbent", "midtier", "challenger"]
        colors = tier_colors_list(tiers)
    """
    return [cs.tier_color(t) for t in tiers]


# ---------------------------------------------------------------------------
# Canonical save — wraps savefig with brand-spec params and filename
# ---------------------------------------------------------------------------

def save_chart(
    fig: Figure,
    pattern_id: str,
    column_span: str | int,
    output_dir: str | Path | None = None,
    *,
    medium: str = "print",
    formats: Sequence[str] = ("pdf",),
) -> list[Path]:
    """Save a chart to reports/output/ with canonical filename and brand-spec params.

    pattern_id: short identifier (e.g., 'p1', 'p2', 'leaderboard_finance')
    column_span: '3', '4', '6', 'spread', or integer 3/4/6
    output_dir: defaults to reports/output/ relative to chart_style location
    medium: 'print' (300 DPI) or 'screen' (144 DPI)
    formats: tuple of file formats — ('pdf',) by default; ('pdf', 'png') for both

    Returns: list of Path objects for the files written.

    Filename convention from brand spec:
      chart_<pattern_id>_<col_span>col.pdf  (default)
      chart_<pattern_id>_spread.pdf         (two-panel)
      chart_<pattern_id>_<col_span>col_<medium>.<ext>  (when medium specified)

    Example:
        save_chart(fig, 'p6', '3')
        # writes reports/output/chart_p6_3col.pdf at 300 DPI vector
    """
    # Normalize column_span to string
    span_str = str(column_span)

    # Resolve output directory
    if output_dir is None:
        # chart_style.py is in reports/, output_dir is reports/output/
        chart_style_path = Path(cs.__file__).resolve()
        output_dir = chart_style_path.parent / "output"
    else:
        output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Choose DPI based on medium
    if medium == "print":
        dpi = cs.DPI_PRINT
    elif medium == "screen":
        dpi = cs.DPI_SCREEN_HIGH
    else:
        raise ValueError(f"Unknown medium '{medium}'. Use 'print' or 'screen'.")

    # Build filename(s)
    written: list[Path] = []
    for fmt in formats:
        if span_str == "spread":
            base = f"chart_{pattern_id}_spread"
        else:
            base = f"chart_{pattern_id}_{span_str}col"
        # Suffix medium only when not the default ('print')
        if medium != "print":
            base = f"{base}_{medium}"
        filename = f"{base}.{fmt}"
        filepath = output_dir / filename
        fig.savefig(
            filepath,
            dpi=dpi,
            bbox_inches=cs.BBOX_INCHES,
            pad_inches=cs.PAD_INCHES,
        )
        written.append(filepath)

    return written


# ---------------------------------------------------------------------------
# Diagonal reference line — for scatter plots comparing two ratios
# ---------------------------------------------------------------------------

def add_diagonal_reference(
    ax: Axes,
    *,
    color: str | None = None,
    linewidth: float = 0.5,
    linestyle: str = "--",
    label: str | None = None,
    lo: float | None = None,
    hi: float | None = None,
) -> None:
    """Draw a y=x reference line across the chart's coordinate range.

    Used for "above/below the diagonal" interpretations: e.g., AI Presence
    vs Consumer Awareness scatter, where above = AI overperforms and below =
    AI underperforms.

    By default, reads xlim/ylim from the current axis. CRITICAL: call this
    AFTER `ax.set_xlim()` / `ax.set_ylim()` — otherwise matplotlib returns
    the default (0.0, 1.0) and the diagonal renders inside a tiny corner.

    Or pass explicit `lo` and `hi` to draw from (lo, lo) to (hi, hi)
    independent of axis state.
    """
    if color is None:
        color = cs.BLACK_20

    if lo is None or hi is None:
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        lo = max(xlim[0], ylim[0]) if lo is None else lo
        hi = min(xlim[1], ylim[1]) if hi is None else hi

        # Sanity check: if the resolved range is the matplotlib default
        # (0,1), the caller forgot to set axis limits before calling us.
        # Warn so the bug doesn't render silently.
        if hi - lo <= 1.5:
            import warnings
            warnings.warn(
                "add_diagonal_reference: axis range looks like matplotlib "
                "defaults (0,1). Did you call this BEFORE set_xlim/set_ylim? "
                f"Current resolved range: lo={lo}, hi={hi}. Pass explicit "
                "lo=, hi= to override.",
                UserWarning,
            )

    ax.plot(
        [lo, hi], [lo, hi],
        color=color,
        linewidth=linewidth,
        linestyle=linestyle,
        zorder=0,
        label=label,
    )


# ---------------------------------------------------------------------------
# Annotated callout — for highlighting a specific data point
# ---------------------------------------------------------------------------

def callout(
    ax: Axes,
    xy: tuple[float, float],
    text: str,
    *,
    offset: tuple[float, float] = (10, 10),
    column_span: str = "3col_inline",
    color: str | None = None,
    arrow: bool = True,
) -> Text:
    """Place an annotated callout near a data point.

    Used for "punchline" annotations like 'Mint shut down March 2024' or
    '71pt single-brand variance' — labels that explain why a particular
    point matters editorially.

    Returns the Text object so the caller can include it in an
    adjustText resolve call.
    """
    sizes = cs.font_sizes_for(column_span)
    if color is None:
        color = cs.COLOR_TEXT

    arrowprops = (
        dict(arrowstyle="-", color=cs.COLOR_MUTED, lw=0.4, alpha=0.7)
        if arrow else None
    )

    return ax.annotate(
        text,
        xy=xy,
        xytext=offset,
        textcoords="offset points",
        fontsize=sizes["annotation"],
        color=color,
        arrowprops=arrowprops,
    )


# ---------------------------------------------------------------------------
# Module summary
# ---------------------------------------------------------------------------

def print_summary() -> None:
    """Print a summary of available utilities."""
    print("chart_utils.py — reusable chart patterns")
    print(f"  adjustText available: {_ADJUSTTEXT_AVAILABLE}")
    print(f"  Functions:")
    print(f"    resolve_label_collisions(texts, ax)")
    print(f"    beeswarm_offsets(values, width)")
    print(f"    mode_style(mode)  # brand/component/authority/empty")
    print(f"    highlight_colors(items, highlight)")
    print(f"    tier_colors_list(tiers)")
    print(f"    save_chart(fig, pattern_id, column_span)")
    print(f"    add_diagonal_reference(ax)")
    print(f"    callout(ax, xy, text)")


if __name__ == "__main__":
    print_summary()
