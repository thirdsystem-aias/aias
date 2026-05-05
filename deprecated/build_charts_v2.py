"""
Third System v0.6 charts — Patterns 1, 3, 6.
Pattern 3 now uses beeswarm spread within each category row.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from chart_style import (
    apply_style,
    BLACK_100, BLACK_80, BLACK_60, BLACK_40, BLACK_20, BLACK_10,
    ACCENT_OCEAN, ACCENT_HONEY, ACCENT_COPPER_PLATE, ACCENT_COPPER,
    ACCENT_RUBINE, ACCENT_AQUA, ACCENT_PETRO, ACCENT_TREE,
    NEUTRAL_3, NEUTRAL_4,
    COLOR_TEXT, COLOR_MUTED, COLOR_SUBDUED, COLOR_GRID,
    TIER_COLORS, COLOR_INCUMBENT, COLOR_MIDTIER, COLOR_CHALLENGER,
    COLOR_HIGHLIGHT_NEGATIVE, COLOR_HIGHLIGHT_POSITIVE, COLOR_PHANTOM,
    SIZE_SCATTER, SIZE_TALL,
    editorial_title, add_source, style_axis_minimal, tier_color,
)
from chart_data import load_all_categories, CATEGORY_LABELS

apply_style()


# ============================================================================
# Beeswarm helper
# ============================================================================

def compute_beeswarm_offsets(x_values, x_threshold=2.8, y_step=0.085, max_y=0.40):
    """
    Greedy beeswarm algorithm.
    For each x_value, find the smallest y-offset that doesn't collide with
    previously placed points. Returns list of y-offsets in input order.
    """
    n = len(x_values)
    if n == 0:
        return []
    sorted_indices = sorted(range(n), key=lambda i: x_values[i])

    # Candidate offsets: 0, +step, -step, +2*step, -2*step, ...
    candidates = [0.0]
    k = 1
    while k * y_step <= max_y:
        candidates.append(k * y_step)
        candidates.append(-k * y_step)
        k += 1

    placed = []  # list of (x, y_offset)
    offsets = [0.0] * n

    for idx in sorted_indices:
        x = x_values[idx]
        chosen = candidates[0]
        for cand in candidates:
            collision = False
            for px, py in placed:
                if abs(px - x) < x_threshold and abs(py - cand) < y_step * 0.9:
                    collision = True
                    break
            if not collision:
                chosen = cand
                break
        offsets[idx] = chosen
        placed.append((x, chosen))
    return offsets


# ============================================================================
# PATTERN 1 (unchanged from previous version)
# ============================================================================

def chart_pattern1_coherence_vs_variance():
    data, _ = load_all_categories()

    category_metrics = []
    for cat_key, rows in data.items():
        top_rows = sorted(rows, key=lambda r: float(r["presence"]), reverse=True)[:8]
        spreads = []
        for r in top_rows:
            try:
                a = float(r["presence_anthropic"])
                o = float(r["presence_openai"])
                spreads.append(abs(a - o))
            except (KeyError, ValueError):
                continue
        max_spread = max(spreads) if spreads else 0
        category_metrics.append({"category": cat_key, "max_spread": max_spread})

    coherence_scores = {
        "Finance": 1.0, "PM": 2.0, "Olive Oil": 2.5,
        "Running": 4.0, "Skincare": 5.0,
    }
    label_offsets = {
        "Finance": (14, 0), "PM": (14, 0), "Olive Oil": (14, 0),
        "Running": (14, 0), "Skincare": (-14, 0),
    }
    label_alignments = {
        "Finance": "left", "PM": "left", "Olive Oil": "left",
        "Running": "left", "Skincare": "right",
    }

    fig = plt.figure(figsize=(8.5, 5.8))
    fig.subplots_adjust(top=0.78, bottom=0.13, left=0.10, right=0.95)
    ax = fig.add_subplot(111)

    sorted_pts = sorted(category_metrics, key=lambda x: coherence_scores[x["category"]])
    xs_line = [coherence_scores[m["category"]] for m in sorted_pts]
    ys_line = [m["max_spread"] for m in sorted_pts]
    ax.plot(xs_line, ys_line, color=BLACK_20, linewidth=1, linestyle="--",
            alpha=0.8, zorder=1)

    for m in category_metrics:
        cat = m["category"]
        x = coherence_scores[cat]
        y = m["max_spread"]
        is_highlight = (cat == "Finance")
        color = ACCENT_COPPER_PLATE if is_highlight else BLACK_60
        size = 320 if is_highlight else 160
        ax.scatter([x], [y], s=size, color=color, zorder=3,
                   edgecolor="white", linewidth=2)

        offset = label_offsets[cat]
        ha = label_alignments[cat]
        weight = "bold" if is_highlight else "normal"
        labelcolor = ACCENT_COPPER_PLATE if is_highlight else BLACK_80
        label = CATEGORY_LABELS[cat]
        ax.annotate(label,
                    xy=(x, y),
                    xytext=offset, textcoords="offset points",
                    fontsize=9, fontweight=weight, color=labelcolor,
                    ha=ha, va="center")
        ax.annotate(f"{y:.0f} pt spread",
                    xy=(x, y),
                    xytext=(offset[0], offset[1] - 14), textcoords="offset points",
                    fontsize=8, color=COLOR_MUTED,
                    ha=ha, va="center")

    ax.set_xlim(0.3, 5.7)
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.set_xticklabels(["Very low", "Low", "Medium", "High", "Very high"], fontsize=8.5)
    ax.set_ylim(0, max([m["max_spread"] for m in category_metrics]) * 1.25)
    ax.set_xlabel("Discourse coherence", color=COLOR_MUTED, labelpad=10)
    ax.set_ylabel("Maximum per-model spread (percentage points)",
                  color=COLOR_MUTED, labelpad=10)
    ax.grid(axis="y", color=BLACK_10, linewidth=0.5, alpha=0.8)
    ax.grid(axis="x", visible=False)
    style_axis_minimal(ax)

    editorial_title(
        fig,
        "Two AIs agree about skincare. They barely agree about personal finance.",
        "Per-model variance scales inversely with the coherence of category discourse",
        headline_y=0.95, subtitle_y=0.89,
    )
    add_source(fig)
    fig.savefig("chart_p1_coherence_variance.pdf", bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)
    print("Saved: chart_p1_coherence_variance.pdf")


# ============================================================================
# PATTERN 6 (unchanged from previous version)
# ============================================================================

def chart_pattern6_phantom_mint():
    data, _ = load_all_categories()
    rows = data["Finance"]
    top = sorted(rows, key=lambda r: float(r["presence"]), reverse=True)[:10]

    labels = [r["brand"] for r in top]
    values = [float(r["presence"]) for r in top]

    colors = []
    for r in top:
        if r["brand"] == "Mint":
            colors.append(ACCENT_COPPER_PLATE)
        else:
            colors.append(tier_color(r["tier"]))

    fig = plt.figure(figsize=(8.5, 5.8))
    fig.subplots_adjust(top=0.76, bottom=0.10, left=0.20, right=0.96)
    ax = fig.add_subplot(111)

    y_pos = list(range(len(labels)))
    ax.barh(y_pos, values, color=colors, height=0.65, edgecolor="none")
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlim(0, 118)
    ax.set_xticks([0, 25, 50, 75, 100])

    for i, v in enumerate(values):
        is_mint = labels[i] == "Mint"
        weight = "bold" if is_mint else "normal"
        textcolor = ACCENT_COPPER_PLATE if is_mint else COLOR_MUTED
        ax.text(v + 1.5, i, f"{v:.0f}", va="center",
                fontsize=8, color=textcolor, fontweight=weight)

    if "Mint" in labels:
        mint_idx = labels.index("Mint")
        mint_value = values[mint_idx]
        ax.annotate(
            "Mint shut down March 2024.\nIn measurements taken two\nyears later, AI mentioned\nit in 44% of responses.",
            xy=(mint_value + 2, mint_idx),
            xytext=(70, mint_idx + 1.5),
            fontsize=9, color=ACCENT_COPPER_PLATE, fontweight="bold",
            ha="left", va="center",
            arrowprops=dict(arrowstyle="-", color=ACCENT_COPPER_PLATE,
                            linewidth=1.2, connectionstyle="arc3,rad=-0.25"))

    ax.set_xlabel("AI Presence (%)", color=COLOR_MUTED, labelpad=8)
    ax.grid(axis="x", color=BLACK_10, linewidth=0.5, alpha=0.8)
    ax.grid(axis="y", visible=False)
    style_axis_minimal(ax)

    legend_elements = [
        mpatches.Patch(color=COLOR_INCUMBENT,  label="Incumbent"),
        mpatches.Patch(color=COLOR_MIDTIER,    label="Mid-tier"),
        mpatches.Patch(color=COLOR_CHALLENGER, label="Challenger"),
        mpatches.Patch(color=ACCENT_COPPER_PLATE, label="Phantom (defunct)"),
    ]
    ax.legend(handles=legend_elements, loc="lower right",
              frameon=False, fontsize=7.5)

    editorial_title(
        fig,
        "In AI mediation, brands die slowly.",
        "A defunct application still ranks fifth in personal finance recommendations",
        headline_y=0.95, subtitle_y=0.89,
    )
    add_source(fig)
    fig.savefig("chart_p6_phantom_mint.pdf", bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)
    print("Saved: chart_p6_phantom_mint.pdf")


# ============================================================================
# PATTERN 3: Awareness divergence — DOT PLOT WITH BEESWARM SPREAD
# ============================================================================

def chart_pattern3_awareness_divergence():
    """
    Five rows. Within each row, dots are spread vertically using beeswarm
    so overlapping x-positions don't stack. Tier grayscale + accent for outliers.
    """
    data, _ = load_all_categories()

    downward_outliers = {
        "Nike", "Bertolli", "Goya", "La Mer", "SK-II",
        "Lancome", "Estee Lauder", "Olay", "Filippo Berio", "Colavita",
    }
    upward_outliers = {
        "YNAB", "Linear", "Brightland", "Norda", "CeraVe",
        "Cobram Estate", "Hoka", "Monarch Money",
    }

    category_order = ["Finance", "Olive Oil", "PM", "Running", "Skincare"]
    row_height = 1.15
    y_positions = {
        cat: (len(category_order) - 1 - i) * row_height
        for i, cat in enumerate(category_order)
    }

    fig = plt.figure(figsize=(9.5, 7.5))
    fig.subplots_adjust(top=0.80, bottom=0.13, left=0.13, right=0.96)
    ax = fig.add_subplot(111)

    for cat in category_order:
        rows = data[cat]
        y_base = y_positions[cat]

        # Filter to non-zero presence brands and collect plot data
        plot_data = []
        for r in rows:
            try:
                presence = float(r["presence"])
            except (KeyError, ValueError):
                continue
            if presence == 0:
                continue
            plot_data.append((presence, r))

        if not plot_data:
            continue

        # Compute beeswarm offsets to spread overlapping dots
        presences = [p for p, _ in plot_data]
        y_offsets = compute_beeswarm_offsets(presences,
                                             x_threshold=3.0,
                                             y_step=0.09,
                                             max_y=0.42)

        # Plot each brand with its computed y-offset
        outlier_positions = []  # for label collision tracking
        for (presence, r), offset in zip(plot_data, y_offsets):
            brand = r["brand"]
            tier = r["tier"]
            is_down = brand in downward_outliers
            is_up   = brand in upward_outliers
            is_outlier = is_down or is_up

            if is_down:
                color = ACCENT_COPPER_PLATE
            elif is_up:
                color = ACCENT_OCEAN
            else:
                color = tier_color(tier)

            size = 120 if is_outlier else 50
            zorder = 5 if is_outlier else 2
            alpha = 1.0 if is_outlier else 0.55
            edgecolor = "white" if is_outlier else "none"
            edgewidth = 1.2 if is_outlier else 0

            actual_y = y_base + offset
            ax.scatter([presence], [actual_y], s=size, color=color,
                       alpha=alpha, edgecolor=edgecolor,
                       linewidth=edgewidth, zorder=zorder)

            if is_outlier:
                # Decide label side: above if dot is in upper half of row,
                # below if in lower half. With beeswarm this distributes labels naturally.
                if offset >= 0:
                    label_y_pts = 11
                    va = "bottom"
                else:
                    label_y_pts = -11
                    va = "top"

                # Check for label collision with previously placed outlier labels
                # in this category
                label_x = presence
                conflict = False
                for ox, oy_pts, ova in outlier_positions:
                    if abs(ox - label_x) < 7 and (
                        (va == "bottom" and ova == "bottom") or
                        (va == "top" and ova == "top")
                    ):
                        conflict = True
                        break
                if conflict:
                    # Flip side
                    label_y_pts = -label_y_pts
                    va = "top" if va == "bottom" else "bottom"

                outlier_positions.append((label_x, label_y_pts, va))

                ax.annotate(
                    brand,
                    xy=(presence, actual_y),
                    xytext=(0, label_y_pts),
                    textcoords="offset points",
                    fontsize=7.8, color=color, fontweight="bold",
                    ha="center", va=va,
                )

    ax.set_yticks([y_positions[c] for c in category_order])
    ax.set_yticklabels([CATEGORY_LABELS[c] for c in category_order], fontsize=9)
    ax.set_ylim(-0.7, (len(category_order) - 1) * row_height + 0.7)

    ax.set_xlim(-3, 105)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xlabel("AI Presence (%)", color=COLOR_MUTED, labelpad=10)

    ax.grid(axis="x", color=BLACK_10, linewidth=0.5, alpha=0.8)
    ax.grid(axis="y", visible=False)

    # Subtle horizontal separator lines between category rows
    for i in range(1, len(category_order)):
        y_line = (i - 0.5) * row_height
        ax.axhline(y=y_line, color=BLACK_10, linewidth=0.4, alpha=0.6, zorder=0)

    style_axis_minimal(ax)

    legend_elements = [
        mlines.Line2D([], [], marker='o', color='w', markerfacecolor=COLOR_INCUMBENT,
                     markersize=7, label='Incumbent', linestyle='None'),
        mlines.Line2D([], [], marker='o', color='w', markerfacecolor=COLOR_MIDTIER,
                     markersize=7, label='Mid-tier', linestyle='None'),
        mlines.Line2D([], [], marker='o', color='w', markerfacecolor=COLOR_CHALLENGER,
                     markersize=7, label='Challenger', linestyle='None'),
        mlines.Line2D([], [], marker='o', color='w', markerfacecolor=ACCENT_COPPER_PLATE,
                     markersize=9, label='Underperforms tier', linestyle='None'),
        mlines.Line2D([], [], marker='o', color='w', markerfacecolor=ACCENT_OCEAN,
                     markersize=9, label='Outperforms tier', linestyle='None'),
    ]
    ax.legend(handles=legend_elements, loc="lower center",
              bbox_to_anchor=(0.5, -0.18), ncol=5,
              frameon=False, fontsize=8)

    editorial_title(
        fig,
        "Brand awareness and AI visibility have come apart.",
        "Across five categories, named brands sit far from where their tier predicts",
        headline_y=0.96, subtitle_y=0.91,
    )
    add_source(fig, y=0.01)
    fig.savefig("chart_p3_awareness_divergence.pdf",
                bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)
    print("Saved: chart_p3_awareness_divergence.pdf")


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    chart_pattern1_coherence_vs_variance()
    chart_pattern6_phantom_mint()
    chart_pattern3_awareness_divergence()
    print("\nThree charts: Pattern 3 now has beeswarm spread within categories.")
