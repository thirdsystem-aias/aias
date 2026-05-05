"""
Third System v0.6 — cross-category pattern matrix.
The aggregate visual: six patterns across five categories, scored on a 0-4 scale.
This is the executive-summary chart.
"""

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle
import numpy as np
from chart_style import (
    apply_style,
    BLACK_80, BLACK_60, BLACK_40, BLACK_20, BLACK_10,
    ACCENT_OCEAN, ACCENT_HONEY, ACCENT_COPPER_PLATE,
    ACCENT_PETRO, ACCENT_AQUA, ACCENT_TREE,
    COLOR_TEXT, COLOR_MUTED,
    editorial_title, add_source, style_axis_minimal,
)
from chart_data import load_all_categories, CATEGORY_LABELS, cep_brand_counts_for_category

apply_style()

# Per-category accent colors (matching Pattern 2 color system)
CATEGORY_ACCENT = {
    "PM":        ACCENT_PETRO,
    "Running":   ACCENT_TREE,
    "Olive Oil": ACCENT_HONEY,
    "Skincare":  ACCENT_AQUA,
    "Finance":   ACCENT_COPPER_PLATE,
}

CATEGORY_ORDER = ["PM", "Running", "Olive Oil", "Skincare", "Finance"]

# ============================================================================
# Scoring rubrics — each pattern returns (score 0-4, display_text) per category
# ============================================================================

def score_pattern1_variance(cat_rows):
    """Per-model variance: max top-brand spread."""
    spreads = []
    top_rows = sorted(cat_rows, key=lambda r: float(r["presence"]), reverse=True)[:8]
    for r in top_rows:
        try:
            a = float(r["presence_anthropic"])
            o = float(r["presence_openai"])
            spreads.append(abs(a - o))
        except (KeyError, ValueError):
            continue
    max_spread = max(spreads) if spreads else 0
    if max_spread <= 10:   score = 1
    elif max_spread <= 25: score = 2
    elif max_spread <= 50: score = 3
    else:                  score = 4
    return score, f"{max_spread:.0f}pt"


def score_pattern2_asymmetry(cat_key):
    """Comparison/Discovery asymmetry: count of off-diagonal brands."""
    cep_counts, cep_runs = cep_brand_counts_for_category(cat_key)
    if cep_counts is None:
        return 0, "n/a"
    comp_runs = cep_runs.get("COMPARISON", 0)
    disc_runs = cep_runs.get("DISCOVERY", 0)
    if comp_runs == 0 or disc_runs == 0:
        return 0, "n/a"
    all_brands = (set(cep_counts.get("COMPARISON", {}).keys()) |
                  set(cep_counts.get("DISCOVERY", {}).keys()))
    off_diagonal_count = 0
    for brand in all_brands:
        comp_pct = (cep_counts.get("COMPARISON", {}).get(brand, 0) / comp_runs) * 100
        disc_pct = (cep_counts.get("DISCOVERY", {}).get(brand, 0) / disc_runs) * 100
        if abs(comp_pct - disc_pct) >= 30:
            off_diagonal_count += 1
    if off_diagonal_count == 0:  score = 0
    elif off_diagonal_count <= 2: score = 1
    elif off_diagonal_count <= 4: score = 2
    elif off_diagonal_count <= 7: score = 3
    else:                         score = 4
    return score, f"{off_diagonal_count} brands"


def score_pattern3_awareness_divergence(cat_rows):
    """AI vs awareness divergence: count of brands where AI presence and tier disagree."""
    # Heuristic: incumbents at <30% Presence OR challengers at >50% Presence count as divergent
    divergent = 0
    for r in cat_rows:
        try:
            presence = float(r["presence"])
        except (KeyError, ValueError):
            continue
        tier = r.get("tier", "")
        if tier == "incumbent" and presence < 30:
            divergent += 1
        elif tier == "challenger" and presence > 50:
            divergent += 1
    if divergent == 0:   score = 0
    elif divergent <= 2: score = 2
    elif divergent <= 4: score = 3
    else:                score = 4
    return score, f"{divergent} brands"


def score_pattern4_language_bias(cat_key):
    """Discourse-language bias: only applies to Olive Oil and Skincare."""
    if cat_key == "Olive Oil":
        return 3, "Spanish < 25%"
    if cat_key == "Skincare":
        return 3, "Korean = 0%"
    return 0, "n/a"  # not applicable to other categories


def score_pattern5_default_reinforcement(cat_key):
    """Default Reinforcement: count of CEPs with a brand at 100%."""
    cep_counts, cep_runs = cep_brand_counts_for_category(cat_key)
    if cep_counts is None:
        return 0, "n/a"
    saturated_ceps = 0
    for cep, brand_counts in cep_counts.items():
        runs = cep_runs.get(cep, 0)
        if runs == 0:
            continue
        for brand, count in brand_counts.items():
            if count / runs >= 1.0:  # 100% mention rate
                saturated_ceps += 1
                break
    if saturated_ceps == 0:   score = 1
    elif saturated_ceps <= 1: score = 2
    elif saturated_ceps <= 3: score = 3
    else:                     score = 4
    return score, f"{saturated_ceps}/6 CEPs"


def score_pattern6_phantom(cat_key, cat_rows):
    """Phantom brand: only Mint in Finance currently."""
    if cat_key != "Finance":
        return 0, "n/a"
    for r in cat_rows:
        if r.get("brand") == "Mint":
            try:
                presence = float(r["presence"])
                if presence > 30:
                    return 4, f"Mint {presence:.0f}%"
            except (KeyError, ValueError):
                pass
    return 0, "n/a"


def score_response_modes(cat_key):
    """Response mode behavior: which modes are observed."""
    # Hard-coded from the audit data we collected earlier
    modes = {
        "PM":        ("B", "Brand only"),
        "Running":   ("B", "Brand only"),
        "Olive Oil": ("B/C", "Brand + Component"),
        "Skincare":  ("B/C/A", "All three modes"),
        "Finance":   ("B", "Brand only"),
    }
    label_short, label_long = modes.get(cat_key, ("B", "Brand only"))
    # Score by complexity: more modes = higher framework strain
    if "/A" in label_short:    score = 4
    elif "/" in label_short:   score = 3
    else:                      score = 1
    return score, label_short


# ============================================================================
# Build the matrix
# ============================================================================

def build_matrix():
    data, _ = load_all_categories()

    pattern_rows = [
        ("Pattern 1", "Per-model variance",
         lambda cat, rows: score_pattern1_variance(rows)),
        ("Pattern 2", "Comparison/Discovery asymmetry",
         lambda cat, rows: score_pattern2_asymmetry(cat)),
        ("Pattern 3", "AI vs awareness divergence",
         lambda cat, rows: score_pattern3_awareness_divergence(rows)),
        ("Pattern 4", "Discourse-language bias",
         lambda cat, rows: score_pattern4_language_bias(cat)),
        ("Pattern 5", "Default Reinforcement",
         lambda cat, rows: score_pattern5_default_reinforcement(cat)),
        ("Pattern 6", "Phantom brand presence",
         lambda cat, rows: score_pattern6_phantom(cat, rows)),
        ("Modes",     "Response-mode behavior",
         lambda cat, rows: score_response_modes(cat)),
    ]

    # Build matrix: rows = patterns, cols = categories
    score_matrix = np.zeros((len(pattern_rows), len(CATEGORY_ORDER)))
    label_matrix = [["" for _ in CATEGORY_ORDER] for _ in pattern_rows]

    for i, (pname, pdesc, scorer) in enumerate(pattern_rows):
        for j, cat in enumerate(CATEGORY_ORDER):
            cat_rows = data[cat]
            score, label = scorer(cat, cat_rows)
            score_matrix[i, j] = score
            label_matrix[i][j] = label

    return pattern_rows, score_matrix, label_matrix


# ============================================================================
# The chart
# ============================================================================

def chart_pattern_matrix():
    pattern_rows, score_matrix, label_matrix = build_matrix()

    n_patterns = len(pattern_rows)
    n_cats = len(CATEGORY_ORDER)

    fig = plt.figure(figsize=(13, 8.5))
    fig.subplots_adjust(top=0.82, bottom=0.10, left=0.28, right=0.95)
    ax = fig.add_subplot(111)

    # Each column gets its own color ramp from white to its accent
    for j, cat in enumerate(CATEGORY_ORDER):
        accent = CATEGORY_ACCENT[cat]
        cmap = mcolors.LinearSegmentedColormap.from_list(
            f"{cat}_ramp", ["#FFFFFF", accent]
        )
        for i in range(n_patterns):
            score = score_matrix[i, j]
            label = label_matrix[i][j]
            # Map 0-4 score to 0.0-1.0 intensity
            intensity = score / 4.0
            cell_color = cmap(intensity)
            # Draw cell
            rect = Rectangle((j - 0.5, i - 0.5), 1, 1,
                             facecolor=cell_color, edgecolor="white",
                             linewidth=2, zorder=2)
            ax.add_patch(rect)
            # Cell label — white text on dark cells, dark on light
            text_color = "white" if intensity > 0.55 else BLACK_80
            if label and label != "n/a":
                ax.text(j, i, label, ha="center", va="center",
                        fontsize=8.5, fontweight="bold",
                        color=text_color, zorder=3)
            elif label == "n/a":
                ax.text(j, i, "—", ha="center", va="center",
                        fontsize=10, color=BLACK_40, zorder=3)

    # Axes
    ax.set_xlim(-0.5, n_cats - 0.5)
    ax.set_ylim(-0.5, n_patterns - 0.5)
    ax.invert_yaxis()
    ax.set_xticks(range(n_cats))
    ax.set_xticklabels([CATEGORY_LABELS[c] for c in CATEGORY_ORDER],
                       fontsize=9.5, fontweight="bold")
    ax.xaxis.tick_top()
    ax.tick_params(axis="x", length=0, pad=8)

    # Y-axis: pattern labels with description
    yticks = list(range(n_patterns))
    ylabels = [f"{name}\n{desc}" for name, desc, _ in pattern_rows]
    ax.set_yticks(yticks)
    ax.set_yticklabels(ylabels, fontsize=9, color=BLACK_80)
    ax.tick_params(axis="y", length=0, pad=8)

    # Hide spines
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(False)

    # Color category headers by accent
    for tick, cat in zip(ax.get_xticklabels(), CATEGORY_ORDER):
        tick.set_color(CATEGORY_ACCENT[cat])

    # Bold the "Modes" row label visually distinct
    ax.get_yticklabels()[-1].set_fontstyle("italic")
    ax.get_yticklabels()[-1].set_color(BLACK_60)

    # Add a horizontal separator between patterns 6 and Modes
    ax.axhline(y=n_patterns - 1.5, color=BLACK_20, linewidth=1, alpha=0.6, zorder=1)

    # Legend / scoring guide at the bottom
    legend_y = 0.04
    legend_x_start = 0.28
    fig.text(legend_x_start, legend_y + 0.03, "Pattern strength:",
             fontsize=8.5, fontweight="bold", color=BLACK_80,
             ha="left", va="bottom")
    # Sample gradient using Ocean as illustration
    sample_cmap = mcolors.LinearSegmentedColormap.from_list(
        "sample", ["#FFFFFF", ACCENT_OCEAN]
    )
    for k, (intensity, label) in enumerate([
        (0.0, "Not present"),
        (0.25, "Weak"),
        (0.5, "Moderate"),
        (0.75, "Strong"),
        (1.0, "Very strong"),
    ]):
        x = legend_x_start + 0.10 + k * 0.10
        rect = Rectangle((x, legend_y), 0.025, 0.018,
                         facecolor=sample_cmap(intensity),
                         edgecolor=BLACK_40 if intensity == 0 else "none",
                         linewidth=0.5,
                         transform=fig.transFigure, zorder=3)
        fig.patches.append(rect)
        fig.text(x + 0.030, legend_y + 0.009, label,
                 fontsize=7.5, color=COLOR_MUTED,
                 ha="left", va="center")

    fig.text(legend_x_start, legend_y - 0.015,
             "Each column uses that category's accent color. Empty cells (—) indicate the pattern does not apply.",
             fontsize=7.5, color=COLOR_MUTED, fontstyle="italic",
             ha="left", va="top")

    editorial_title(
        fig,
        "Six framework patterns × five categories: how the framework holds.",
        "Cell intensity shows the strength of evidence for each pattern in each category. The bottom row summarizes which response modes were observed.",
        headline_y=0.95, subtitle_y=0.91, x=0.05,
    )
    add_source(fig, y=0.005, x=0.95)
    fig.savefig("chart_aggregate_matrix.pdf",
                bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)
    print("Saved: chart_aggregate_matrix.pdf")


if __name__ == "__main__":
    chart_pattern_matrix()
