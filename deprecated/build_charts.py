"""
Third System cross-category charts (five-category version) — heatmap rebuild.
The heatmap now distinguishes brand-mode cells from component-mode and authority-mode
cells, so empty-canonical cells aren't misread as zero presence.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import matplotlib.colors as mcolors
import numpy as np
from chart_style import (
    apply_style,
    BLACK_80, BLACK_60, BLACK_40, BLACK_20, BLACK_10,
    ACCENT_OCEAN, ACCENT_HONEY, ACCENT_COPPER_PLATE, ACCENT_RUBINE,
    NEUTRAL_3,
    COLOR_TEXT, COLOR_MUTED, COLOR_GRID,
    TIER_COLORS, COLOR_INCUMBENT, COLOR_MIDTIER, COLOR_CHALLENGER,
    editorial_title, add_source, style_axis_minimal, tier_color,
)
from chart_data import (
    load_all_categories, CATEGORY_LABELS, cep_brand_counts_for_category,
    load_enriched_for_category,
)

apply_style()

ATLANTIC = "#005E92"
CATEGORY_ORDER = ["PM", "Running", "Olive Oil", "Skincare", "Finance"]


# ============================================================================
# Mode classification helper
# ============================================================================
# Threshold: if >50% of empty-canonical responses for a (cat, cep, model) cell
# contain ingredient/format tokens => component mode.
# If >50% contain publication/source tokens => authority mode.
# Otherwise the cell is brand mode (use Presence rate).

INGREDIENT_TOKENS = {
    # skincare
    "spf 30+", "vitamin c", "tretinoin", "retinol", "retinal", "niacinamide",
    "hyaluronic acid", "peptides", "lactic acid", "glycolic acid",
    "adapalene", "sunscreen", "salicylic acid", "azelaic acid", "ceramides",
    # olive oil
    "evoo", "extra virgin olive oil", "light olive oil", "refined olive oil",
    "olive oil", "single-origin", "estate-bottled", "estate-bottled evoo",
    "organic evoo", "gourmet finishing oils", "pdo", "pgi",
}
AUTHORITY_TOKENS = {
    # publications, communities, retailers, competitions
    "allure", "byrdie", "vogue", "wwd beauty", "sephora", "ulta",
    "reddit", "r/skincareaddiction",
    "olive oil times", "flos olei", "nyiooc", "nyiooc world olive oil competition",
    "new york international olive oil competition",
    "bon appétit", "bon appetit", "saveur", "zingerman's", "zingermans",
}


def classify_mode(unknown_tokens):
    """Returns 'component', 'authority', or 'mixed' based on token content."""
    if not unknown_tokens:
        return None
    n_total = len(unknown_tokens)
    n_ingredient = sum(1 for t in unknown_tokens
                       if t.strip().lower() in INGREDIENT_TOKENS)
    n_authority = sum(1 for t in unknown_tokens
                      if t.strip().lower() in AUTHORITY_TOKENS)
    if n_ingredient / n_total > 0.5:
        return "component"
    if n_authority / n_total > 0.5:
        return "authority"
    return "mixed"


def cell_mode_for_category(category_key, cep_name):
    """
    Determines if this category-CEP cell is dominated by component or authority mode.
    Returns 'component', 'authority', or None (brand mode).
    """
    enriched = load_enriched_for_category(category_key)
    if not enriched:
        return None
    cep_rows = [r for r in enriched if r.get("cep") == cep_name]
    if not cep_rows:
        return None

    empty_canonical_rows = [r for r in cep_rows
                            if not r.get("brands_canonical", "").strip()]
    if len(empty_canonical_rows) < len(cep_rows) * 0.4:
        # Less than 40% of rows are mode-switched. Treat as brand mode.
        return None

    # Aggregate all unknown tokens across the empty rows
    all_tokens = []
    for r in empty_canonical_rows:
        unknowns = r.get("brands_unknown", "")
        if unknowns:
            all_tokens.extend([t.strip() for t in unknowns.split("|") if t.strip()])

    return classify_mode(all_tokens)


# ============================================================================
# Heatmap with mode awareness
# ============================================================================

def chart_cep_heatmap():
    cep_order = [
        "FUNCTIONAL_WHY", "CONTEXTUAL_WHEN", "CONSTRAINT_WITH",
        "IDENTITY_HOW_FEELING", "DISCOVERY", "COMPARISON",
    ]
    cep_short = {
        "FUNCTIONAL_WHY": "Functional",
        "CONTEXTUAL_WHEN": "Contextual",
        "CONSTRAINT_WITH": "Constraint",
        "IDENTITY_HOW_FEELING": "Identity",
        "DISCOVERY": "Discovery",
        "COMPARISON": "Comparison",
    }

    # Sequential blue ramp for brand-mode cells
    ocean_cmap = mcolors.LinearSegmentedColormap.from_list(
        "ocean_seq", ["#FFFFFF", "#E0EEF6", "#A1C3DA", ACCENT_OCEAN]
    )

    # Mode marker colors (light, distinct from blue ramp)
    COMPONENT_FILL = "#F5EBD8"   # warm pale yellow
    COMPONENT_HATCH_COLOR = "#A88947"
    AUTHORITY_FILL = "#EAE4EE"   # pale lavender
    AUTHORITY_HATCH_COLOR = "#7B6890"

    data, _ = load_all_categories()

    fig, axes = plt.subplots(5, 1, figsize=(11.5, 17.5))
    fig.subplots_adjust(top=0.91, bottom=0.06, left=0.18, right=0.92, hspace=0.85)

    last_im = None
    for ax, cat in zip(axes, CATEGORY_ORDER):
        cep_counts, cep_runs = cep_brand_counts_for_category(cat)
        if cep_counts is None:
            ax.text(0.5, 0.5, f"No CEP data for {cat}",
                    ha="center", va="center", transform=ax.transAxes,
                    color=COLOR_MUTED, fontsize=9)
            ax.axis("off")
            continue

        # Top 8 brands by total mentions across CEPs
        brand_totals = {}
        for cep in cep_order:
            for brand, count in cep_counts.get(cep, {}).items():
                brand_totals[brand] = brand_totals.get(brand, 0) + count
        top_brands = sorted(brand_totals.items(), key=lambda x: x[1], reverse=True)[:8]
        brand_names = [b for b, _ in top_brands]

        # Build matrix and per-row mode classification
        matrix = np.zeros((len(cep_order), len(brand_names)))
        row_modes = []
        for i, cep in enumerate(cep_order):
            runs = cep_runs.get(cep, 0)
            mode = cell_mode_for_category(cat, cep)
            row_modes.append(mode)
            if mode is not None:
                # Mode-switched row — leave matrix at 0; we'll overlay later
                continue
            if runs == 0:
                continue
            for j, brand in enumerate(brand_names):
                count = cep_counts.get(cep, {}).get(brand, 0)
                matrix[i, j] = (count / runs) * 100

        # Mask rows that are mode-switched, so imshow won't draw them in blue
        masked = np.ma.array(matrix)
        for i, mode in enumerate(row_modes):
            if mode is not None:
                masked[i, :] = np.ma.masked

        im = ax.imshow(masked, cmap=ocean_cmap, vmin=0, vmax=100, aspect="auto")
        last_im = im

        # Draw value annotations in brand-mode cells
        for i in range(matrix.shape[0]):
            if row_modes[i] is not None:
                continue
            for j in range(matrix.shape[1]):
                val = matrix[i, j]
                txtcolor = "white" if val > 55 else BLACK_80
                ax.text(j, i, f"{val:.0f}", ha="center", va="center",
                        fontsize=7, color=txtcolor)

        # Overlay mode-switched rows with hatching + label
        for i, mode in enumerate(row_modes):
            if mode is None:
                continue
            n_cols = len(brand_names)
            if mode == "component":
                fill = COMPONENT_FILL
                hatch_color = COMPONENT_HATCH_COLOR
                label = "component mode"
            elif mode == "authority":
                fill = AUTHORITY_FILL
                hatch_color = AUTHORITY_HATCH_COLOR
                label = "authority mode"
            else:
                fill = "#EEEEEE"
                hatch_color = BLACK_60
                label = "mixed mode"

            # Draw a single rectangle spanning the whole row
            from matplotlib.patches import Rectangle
            rect = Rectangle(
                (-0.5, i - 0.5), n_cols, 1,
                facecolor=fill, edgecolor="white", linewidth=0,
                hatch="///", zorder=2,
            )
            rect.set_edgecolor(hatch_color)
            ax.add_patch(rect)

            # Cover with a clean fill on top of hatch in the center for readability
            cover = Rectangle(
                (n_cols / 2 - 1.4, i - 0.18), 2.8, 0.36,
                facecolor="white", edgecolor=hatch_color, linewidth=0.6,
                zorder=3,
            )
            ax.add_patch(cover)
            ax.text(n_cols / 2 - 0.5, i, label, ha="center", va="center",
                    fontsize=8, color=hatch_color, fontstyle="italic",
                    fontweight="bold", zorder=4)

        ax.set_xticks(range(len(brand_names)))
        ax.set_xticklabels(brand_names, rotation=30, ha="right", fontsize=7.5)
        ax.set_yticks(range(len(cep_order)))
        ax.set_yticklabels([cep_short[c] for c in cep_order], fontsize=7.5)

        ax.set_title(CATEGORY_LABELS[cat], fontsize=10, fontweight="bold",
                     loc="left", pad=10, color="#1A1A1A")
        ax.tick_params(colors=COLOR_MUTED, length=0)
        for spine in ax.spines.values():
            spine.set_visible(False)

        ax.grid(False)
        ax.set_axisbelow(False)

    if last_im is not None:
        cbar_ax = fig.add_axes([0.30, 0.025, 0.40, 0.012])
        cbar = fig.colorbar(last_im, cax=cbar_ax, orientation="horizontal")
        cbar.set_label("Brand-mode mention rate (%)", fontsize=8,
                       color=COLOR_MUTED, labelpad=4)
        cbar.ax.tick_params(labelsize=7, colors=COLOR_MUTED, length=2)
        cbar.outline.set_visible(False)

    # Mode legend below colorbar
    fig.text(0.30, 0.005, "Component mode",
             fontsize=7.5, color=COMPONENT_HATCH_COLOR, fontweight="bold",
             ha="left", va="bottom", style="italic")
    fig.text(0.55, 0.005, "Authority mode",
             fontsize=7.5, color=AUTHORITY_HATCH_COLOR, fontweight="bold",
             ha="left", va="bottom", style="italic")

    editorial_title(
        fig,
        "When the prompt frame matches the discourse, AI gives the same answer.",
        "Brand-mode mention rate by CEP. Hatched rows show component or authority mode.",
        headline_y=0.97, subtitle_y=0.948, x=0.05,
    )
    add_source(fig, y=0.01, x=0.92)
    fig.savefig("chart_cep_heatmap.pdf", bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)
    print("Saved: chart_cep_heatmap.pdf")


# ============================================================================
# Re-export the other two charts unchanged so build_charts.py still works
# ============================================================================

def chart_leaderboards():
    data, _ = load_all_categories()
    fig, axes = plt.subplots(1, 5, figsize=(15, 6.5))
    fig.subplots_adjust(top=0.78, bottom=0.10, left=0.04, right=0.98, wspace=0.55)

    for ax, cat in zip(axes, CATEGORY_ORDER):
        rows = data[cat]
        top = sorted(rows, key=lambda r: float(r["presence"]), reverse=True)[:10]
        labels = [r["brand"] for r in top]
        values = [float(r["presence"]) for r in top]
        colors = [tier_color(r["tier"]) for r in top]

        y_pos = list(range(len(labels)))
        ax.barh(y_pos, values, color=colors, height=0.65, edgecolor="none")
        ax.set_yticks(y_pos)
        ax.set_yticklabels(labels, fontsize=7.5)
        ax.invert_yaxis()
        ax.set_xlim(0, 110)
        ax.set_xticks([0, 50, 100])
        ax.tick_params(axis="x", labelsize=7)

        for i, v in enumerate(values):
            ax.text(v + 2, i, f"{v:.0f}", va="center",
                    fontsize=6.5, color=COLOR_MUTED)
        ax.set_title(CATEGORY_LABELS[cat], fontsize=9.5, fontweight="bold",
                     loc="left", pad=8, color="#1A1A1A")
        ax.grid(axis="x", color=BLACK_10, linewidth=0.5, alpha=0.8)
        ax.grid(axis="y", visible=False)
        style_axis_minimal(ax)

    legend_elements = [
        mpatches.Patch(color=COLOR_INCUMBENT,  label="Incumbent"),
        mpatches.Patch(color=COLOR_MIDTIER,    label="Mid-tier"),
        mpatches.Patch(color=COLOR_CHALLENGER, label="Challenger"),
    ]
    fig.legend(handles=legend_elements, loc="lower center",
               bbox_to_anchor=(0.5, 0.01), ncol=3,
               frameon=False, fontsize=8.5)

    editorial_title(
        fig,
        "AI Presence leaders across five categories",
        "Top 10 brands by mention rate per category",
        headline_y=0.96, subtitle_y=0.92, x=0.04,
    )
    add_source(fig, y=0.05, x=0.97)
    fig.savefig("chart_leaderboards.pdf", bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)
    print("Saved: chart_leaderboards.pdf")


def chart_per_model_variance():
    data, _ = load_all_categories()
    all_variances = []
    for cat, rows in data.items():
        for r in rows:
            try:
                a = float(r["presence_anthropic"])
                o = float(r["presence_openai"])
                presence = float(r["presence"])
            except (KeyError, ValueError):
                continue
            if presence < 5:
                continue
            spread = abs(a - o)
            all_variances.append({
                "brand": r["brand"], "category": cat, "tier": r["tier"],
                "anthropic": a, "openai": o, "spread": spread, "presence": presence,
            })
    top = sorted(all_variances, key=lambda x: x["spread"], reverse=True)[:18]

    fig = plt.figure(figsize=(10, 7.5))
    fig.subplots_adjust(top=0.82, bottom=0.10, left=0.30, right=0.94)
    ax = fig.add_subplot(111)

    max_spread = max(t["spread"] for t in top)

    for i, t in enumerate(top):
        is_max = (t["spread"] == max_spread)
        y = i
        if is_max:
            line_color = ACCENT_COPPER_PLATE
            ant_color = ACCENT_COPPER_PLATE
            oai_color = ACCENT_COPPER_PLATE
            line_width = 3.0
        else:
            line_color = BLACK_20
            ant_color = ATLANTIC
            oai_color = ACCENT_HONEY
            line_width = 1.8

        x_low  = min(t["anthropic"], t["openai"])
        x_high = max(t["anthropic"], t["openai"])
        ax.plot([x_low, x_high], [y, y],
                color=line_color, linewidth=line_width,
                zorder=2, solid_capstyle="round")
        ax.scatter([t["anthropic"]], [y], s=85 if is_max else 60,
                   color=ant_color, marker="s", zorder=4,
                   edgecolor="white", linewidth=1.0)
        ax.scatter([t["openai"]], [y], s=85 if is_max else 60,
                   color=oai_color, marker="o", zorder=4,
                   edgecolor="white", linewidth=1.0)
        spread_x = x_high + 2
        spread_color = ACCENT_COPPER_PLATE if is_max else COLOR_MUTED
        spread_weight = "bold" if is_max else "normal"
        ax.text(spread_x, y, f"{t['spread']:.0f}pt",
                fontsize=7.5, color=spread_color, fontweight=spread_weight,
                va="center", ha="left")

    yticklabels = [f"{t['brand']}  ·  {t['category']}" for t in top]
    ax.set_yticks(list(range(len(top))))
    ax.set_yticklabels(yticklabels, fontsize=8)
    ax.invert_yaxis()
    for i, t in enumerate(top):
        if t["spread"] == max_spread:
            ax.get_yticklabels()[i].set_color(ACCENT_COPPER_PLATE)
            ax.get_yticklabels()[i].set_fontweight("bold")

    ax.set_xlim(-3, 115)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xlabel("AI Presence (%)", color=COLOR_MUTED, labelpad=10)
    ax.grid(axis="x", color=BLACK_10, linewidth=0.5, alpha=0.8)
    ax.grid(axis="y", visible=False)
    style_axis_minimal(ax)

    legend_elements = [
        mlines.Line2D([], [], marker="s", color="w", markerfacecolor=ATLANTIC,
                      markersize=9, label="Anthropic", linestyle="None",
                      markeredgecolor="white"),
        mlines.Line2D([], [], marker="o", color="w", markerfacecolor=ACCENT_HONEY,
                      markersize=9, label="OpenAI", linestyle="None",
                      markeredgecolor="white"),
    ]
    ax.legend(handles=legend_elements, loc="lower right",
              frameon=False, fontsize=8.5)

    editorial_title(
        fig,
        "Rocket Money: 71 points apart across two AIs.",
        "The 18 largest per-model variances across all five categories, sorted by spread",
        headline_y=0.96, subtitle_y=0.92,
    )
    add_source(fig, y=0.04)
    fig.savefig("chart_per_model_variance.pdf",
                bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)
    print("Saved: chart_per_model_variance.pdf")


if __name__ == "__main__":
    chart_leaderboards()
    chart_per_model_variance()
    chart_cep_heatmap()
    print("\nThree charts updated. Heatmap now distinguishes brand / component / authority modes.")
