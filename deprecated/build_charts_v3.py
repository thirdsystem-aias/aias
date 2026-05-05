"""
Third System v0.6 charts — Patterns 2 and 4.
Pattern 2: small multiples scatter, one panel per category.
Pattern 4: country-of-origin small multiples for Olive Oil and Skincare.
S&P palette + tier grayscale + Akkurat Pro typography.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from matplotlib.patches import Rectangle
from collections import defaultdict
from chart_style import (
    apply_style,
    BLACK_80, BLACK_60, BLACK_40, BLACK_20, BLACK_10,
    ACCENT_OCEAN, ACCENT_HONEY, ACCENT_COPPER_PLATE, ACCENT_RUBINE,
    ACCENT_PETRO, ACCENT_AQUA, ACCENT_TREE,
    NEUTRAL_3, NEUTRAL_4,
    COLOR_TEXT, COLOR_MUTED, COLOR_GRID,
    TIER_COLORS, COLOR_INCUMBENT, COLOR_MIDTIER, COLOR_CHALLENGER,
    editorial_title, add_source, style_axis_minimal, tier_color,
    editorial_callout,
)
from chart_data import (
    load_all_categories, CATEGORY_LABELS,
    cep_brand_counts_for_category,
)

try:
    from adjustText import adjust_text
    HAS_ADJUST_TEXT = True
except ImportError:
    HAS_ADJUST_TEXT = False
    print("Note: adjustText not available; using basic placement")

apply_style()

# ============================================================================
# Country-of-origin lookup
# ============================================================================

BRAND_COUNTRY = {
    # Olive Oil
    "California Olive Ranch": "US", "Cobram Estate": "Australia", "Brightland": "US",
    "Frantoio Muraglia": "Italy", "Graza": "US", "Kosterina": "US",
    "Frescobaldi Laudemio": "Italy", "Castillo de Canena": "Spain",
    "Núñez de Prado": "Spain", "Manni": "Italy", "McEvoy Ranch": "US",
    "Colonna": "Italy", "Bertolli": "Italy", "Colavita": "Italy",
    "Goya": "Spain", "Filippo Berio": "Italy", "Carbonell": "Spain",
    "Pompeian": "Spain", "Lucini": "Italy",
    # Skincare
    "CeraVe": "US", "La Roche-Posay": "France", "Vanicream": "US",
    "Neutrogena": "US", "Cetaphil": "US", "Eucerin": "Germany",
    "EltaMD": "US", "Paula's Choice": "US", "First Aid Beauty": "US",
    "Avène": "France", "Bioderma": "France", "Aveeno": "US",
    "Drunk Elephant": "US", "Skinceuticals": "US", "Tatcha": "US",
    "Augustinus Bader": "UK", "Youth to the People": "US",
    "Beauty of Joseon": "Korea", "La Mer": "US", "SK-II": "Japan",
    "Lancôme": "France", "Estée Lauder": "US", "Clinique": "US",
    "Olay": "US", "Kiehl's": "US", "Glossier": "US",
    "Sunday Riley": "US", "The Ordinary": "Canada",
    "Origins": "US", "Dermalogica": "US", "Murad": "US",
}

COUNTRY_ORDER_OO = ["US", "Australia", "Italy", "Spain"]
COUNTRY_ORDER_SK = ["US", "UK", "France", "Germany", "Japan", "Korea"]
ENGLISH_LANGUAGE_OO = {"US", "Australia"}
ENGLISH_LANGUAGE_SK = {"US", "UK"}


# ============================================================================
# PATTERN 2: Small multiples scatter — one panel per category
# ============================================================================

def chart_pattern2_comparison_vs_discovery():
    """
    Five small-multiple scatter panels, one per category, in a 2x3 grid.
    Bottom-right slot used for legend + how-to-read note.
    Each panel: Comparison-prompt (x) vs Discovery-prompt (y), shaded zones,
    diagonal reference, top 5 outliers labeled.
    """
    cats = ["PM", "Running", "Olive Oil", "Skincare", "Finance"]
    cat_colors = {
        "PM":        ACCENT_PETRO,
        "Running":   ACCENT_TREE,
        "Olive Oil": ACCENT_HONEY,
        "Skincare":  ACCENT_AQUA,
        "Finance":   ACCENT_COPPER_PLATE,
    }

    cat_brand_data = {}
    for cat in cats:
        cep_counts, cep_runs = cep_brand_counts_for_category(cat)
        if cep_counts is None:
            cat_brand_data[cat] = []
            continue
        comp_runs = cep_runs.get("COMPARISON", 0)
        disc_runs = cep_runs.get("DISCOVERY", 0)
        if comp_runs == 0 or disc_runs == 0:
            cat_brand_data[cat] = []
            continue
        all_brands = (set(cep_counts.get("COMPARISON", {}).keys()) |
                      set(cep_counts.get("DISCOVERY", {}).keys()))
        rows = []
        for brand in all_brands:
            comp_pct = (cep_counts.get("COMPARISON", {}).get(brand, 0) / comp_runs) * 100
            disc_pct = (cep_counts.get("DISCOVERY", {}).get(brand, 0) / disc_runs) * 100
            if comp_pct == 0 and disc_pct == 0:
                continue
            rows.append({
                "brand": brand,
                "comparison": comp_pct, "discovery": disc_pct,
                "off_diagonal": abs(comp_pct - disc_pct),
            })
        cat_brand_data[cat] = rows

    fig, axes = plt.subplots(2, 3, figsize=(13.5, 9.0))
    fig.subplots_adjust(top=0.85, bottom=0.07, left=0.06, right=0.97,
                        wspace=0.30, hspace=0.42)

    panel_positions = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1)]

    for cat, (row, col) in zip(cats, panel_positions):
        ax = axes[row, col]
        rows = cat_brand_data[cat]
        color = cat_colors[cat]

        ax.add_patch(Rectangle((50, 0), 55, 30,
                               facecolor=ACCENT_COPPER_PLATE, alpha=0.06, zorder=0))
        ax.add_patch(Rectangle((0, 50), 30, 55,
                               facecolor=ACCENT_OCEAN, alpha=0.06, zorder=0))

        ax.plot([0, 100], [0, 100], color=BLACK_20, linewidth=0.5,
                linestyle="--", alpha=0.5, zorder=1)

        for r in rows:
            x, y = r["comparison"], r["discovery"]
            is_outlier = r["off_diagonal"] >= 30 and max(x, y) >= 25
            size = 70 if is_outlier else 30
            alpha = 1.0 if is_outlier else 0.45
            ax.scatter([x], [y], s=size, color=color, alpha=alpha,
                       edgecolor="white" if is_outlier else "none",
                       linewidth=0.8, zorder=4 if is_outlier else 2)

        outliers = sorted(
            [r for r in rows if r["off_diagonal"] >= 30 and max(r["comparison"], r["discovery"]) >= 25],
            key=lambda r: -r["off_diagonal"]
        )[:5]

        text_labels = []
        for r in outliers:
            t = ax.text(r["comparison"], r["discovery"], r["brand"],
                        fontsize=7.5, color=color, fontweight="bold",
                        ha="center", va="center", zorder=5)
            text_labels.append(t)

        if HAS_ADJUST_TEXT and text_labels:
            adjust_text(
                text_labels, ax=ax,
                expand=(1.4, 1.6),
                force_text=(0.5, 0.7),
                arrowprops=dict(arrowstyle="-", color=BLACK_60, lw=0.4, alpha=0.5),
            )

        ax.set_xlim(-3, 105)
        ax.set_ylim(-3, 105)
        ax.set_xticks([0, 50, 100])
        ax.set_yticks([0, 50, 100])
        ax.tick_params(axis="both", labelsize=7)
        ax.set_title(CATEGORY_LABELS[cat], fontsize=10, fontweight="bold",
                     loc="left", pad=8, color=BLACK_80)
        ax.grid(axis="both", color=BLACK_10, linewidth=0.3, alpha=0.6)
        style_axis_minimal(ax)

        if col == 0:
            ax.set_ylabel("Discovery (%)", fontsize=8, color=COLOR_MUTED, labelpad=4)
        if row == 1:
            ax.set_xlabel("Comparison (%)", fontsize=8, color=COLOR_MUTED, labelpad=4)
        if row == 0 and col == 2:
            ax.set_xlabel("Comparison (%)", fontsize=8, color=COLOR_MUTED, labelpad=4)

    # Legend / how-to-read panel in slot (1, 2)
    legend_ax = axes[1, 2]
    legend_ax.axis("off")

    legend_ax.text(0.05, 0.92, "How to read",
                   fontsize=10, fontweight="bold", color=BLACK_80,
                   transform=legend_ax.transAxes, ha="left", va="top")

    legend_ax.text(0.05, 0.83,
                   "Each dot is a brand. X = Comparison-prompt\n"
                   "mention rate. Y = Discovery-prompt rate.",
                   fontsize=8, color=COLOR_MUTED,
                   transform=legend_ax.transAxes, ha="left", va="top")

    legend_ax.add_patch(Rectangle((0.05, 0.58), 0.10, 0.06,
                                   facecolor=ACCENT_OCEAN, alpha=0.30,
                                   transform=legend_ax.transAxes))
    legend_ax.text(0.18, 0.61, "Discovery-only zone",
                   fontsize=8.5, fontweight="bold", color=ACCENT_OCEAN,
                   transform=legend_ax.transAxes, ha="left", va="center")
    legend_ax.text(0.18, 0.54, "Brands AI surfaces only when asked",
                   fontsize=7.5, color=COLOR_MUTED, fontstyle="italic",
                   transform=legend_ax.transAxes, ha="left", va="center")

    legend_ax.add_patch(Rectangle((0.05, 0.40), 0.10, 0.06,
                                   facecolor=ACCENT_COPPER_PLATE, alpha=0.30,
                                   transform=legend_ax.transAxes))
    legend_ax.text(0.18, 0.43, "Comparison-only zone",
                   fontsize=8.5, fontweight="bold", color=ACCENT_COPPER_PLATE,
                   transform=legend_ax.transAxes, ha="left", va="center")
    legend_ax.text(0.18, 0.36, "Incumbents AI defaults to",
                   fontsize=7.5, color=COLOR_MUTED, fontstyle="italic",
                   transform=legend_ax.transAxes, ha="left", va="center")

    legend_ax.text(0.05, 0.22,
                   "The pattern repeats across all five\n"
                   "categories: brands cluster in the corners,\n"
                   "not on the diagonal.",
                   fontsize=8.5, color=BLACK_80, fontweight="bold",
                   transform=legend_ax.transAxes, ha="left", va="top")

    editorial_title(
        fig,
        "AI gives different answers when you ask different questions.",
        "Each category shows the same Comparison-vs-Discovery asymmetry — incumbents bottom-right, challengers upper-left",
        headline_y=0.96, subtitle_y=0.92, x=0.05,
    )
    add_source(fig, y=0.01, x=0.97)
    fig.savefig("chart_p2_comparison_discovery.pdf",
                bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)
    print("Saved: chart_p2_comparison_discovery.pdf")


# ============================================================================
# PATTERN 4: Country-of-origin small multiples
# ============================================================================

def chart_pattern4_country_origin():
    data, _ = load_all_categories()

    fig, axes = plt.subplots(1, 2, figsize=(14, 7.0))
    fig.subplots_adjust(top=0.78, bottom=0.16, left=0.07, right=0.97, wspace=0.22)

    panels = [
        ("Olive Oil", COUNTRY_ORDER_OO, ENGLISH_LANGUAGE_OO, axes[0]),
        ("Skincare", COUNTRY_ORDER_SK, ENGLISH_LANGUAGE_SK, axes[1]),
    ]

    notable_oo = {
        "California Olive Ranch", "Brightland", "Cobram Estate",
        "Goya", "Castillo de Canena",
        "Bertolli", "Filippo Berio", "Frantoio Muraglia",
    }
    notable_sk = {
        "CeraVe", "Neutrogena", "Vanicream",
        "La Roche-Posay", "Avène",
        "Beauty of Joseon", "SK-II", "Lancôme",
        "Augustinus Bader",
    }

    for cat_key, country_order, english_set, ax in panels:
        rows = data[cat_key]
        mapped = []
        unmapped = []
        for r in rows:
            try:
                presence = float(r["presence"])
            except (KeyError, ValueError):
                continue
            country = BRAND_COUNTRY.get(r["brand"])
            if country is None:
                unmapped.append(r["brand"])
                continue
            if country not in country_order:
                continue
            mapped.append({
                "brand": r["brand"], "country": country,
                "presence": presence, "tier": r["tier"],
            })
        if unmapped:
            print(f"[{cat_key}] Unmapped brands skipped: {unmapped}")

        notable = notable_oo if cat_key == "Olive Oil" else notable_sk
        country_to_x = {c: i for i, c in enumerate(country_order)}

        english_x_indices = [country_to_x[c] for c in country_order if c in english_set]
        if english_x_indices:
            min_x = min(english_x_indices) - 0.45
            max_x = max(english_x_indices) + 0.45
            ax.add_patch(Rectangle(
                (min_x, -3), max_x - min_x, 108,
                facecolor=ACCENT_OCEAN, alpha=0.08, zorder=0,
            ))
            ax.text((min_x + max_x) / 2, 102, "ENGLISH-LANGUAGE ORIGIN",
                    fontsize=8, fontweight="bold", color=ACCENT_OCEAN,
                    alpha=0.75, ha="center", va="top", zorder=1)

        by_country = defaultdict(list)
        for m in mapped:
            by_country[m["country"]].append(m)

        import random
        text_labels = []
        for country, group in by_country.items():
            x_center = country_to_x[country]
            group_sorted = sorted(group, key=lambda m: m["presence"])
            for j, m in enumerate(group_sorted):
                random.seed(hash(m["brand"]) & 0xFFFF)
                jitter_range = 0.32
                jitter = random.uniform(-jitter_range, jitter_range)
                x = x_center + jitter
                y = m["presence"]
                is_notable = m["brand"] in notable
                color = tier_color(m["tier"])
                size = 130 if is_notable else 55
                alpha = 1.0 if is_notable else 0.4
                edgecolor = "white" if is_notable else "none"
                edgewidth = 1.2 if is_notable else 0
                zorder = 4 if is_notable else 2
                ax.scatter([x], [y], s=size, color=color, alpha=alpha,
                           edgecolor=edgecolor, linewidth=edgewidth, zorder=zorder)
                if is_notable:
                    t = ax.text(x, y, m["brand"], fontsize=7.8,
                                color=BLACK_80, fontweight="bold",
                                ha="center", va="center", zorder=5)
                    text_labels.append(t)

        if HAS_ADJUST_TEXT and text_labels:
            adjust_text(
                text_labels, ax=ax,
                expand=(1.2, 1.4),
                arrowprops=dict(arrowstyle="-", color=BLACK_60, lw=0.4, alpha=0.5),
            )

        ax.set_xticks(list(country_to_x.values()))
        ax.set_xticklabels(country_order, fontsize=9.5, fontweight="bold")
        ax.set_xlim(-0.6, len(country_order) - 0.4)
        ax.set_ylim(-3, 108)
        ax.set_yticks([0, 25, 50, 75, 100])
        ax.set_ylabel("AI Presence (%)", color=COLOR_MUTED, labelpad=10)
        ax.set_title(CATEGORY_LABELS[cat_key], fontsize=11, fontweight="bold",
                     loc="left", pad=10, color="#1A1A1A")
        ax.grid(axis="y", color=BLACK_10, linewidth=0.5, alpha=0.7)
        ax.grid(axis="x", visible=False)
        style_axis_minimal(ax)

    legend_elements = [
        mlines.Line2D([], [], marker="o", color="w",
                      markerfacecolor=COLOR_INCUMBENT,
                      markersize=8, label="Incumbent", linestyle="None",
                      markeredgecolor="white"),
        mlines.Line2D([], [], marker="o", color="w",
                      markerfacecolor=COLOR_MIDTIER,
                      markersize=8, label="Mid-tier", linestyle="None",
                      markeredgecolor="white"),
        mlines.Line2D([], [], marker="o", color="w",
                      markerfacecolor=COLOR_CHALLENGER,
                      markersize=8, label="Challenger", linestyle="None",
                      markeredgecolor="white"),
    ]
    fig.legend(handles=legend_elements, loc="lower center",
               bbox_to_anchor=(0.5, 0.02), ncol=3,
               frameon=False, fontsize=9)

    editorial_title(
        fig,
        "AI underperforms brands whose discourse is non-English.",
        "Spanish olive oil and Korean skincare brands cluster at the bottom of their categories",
        headline_y=0.96, subtitle_y=0.92, x=0.05,
    )
    add_source(fig, y=0.005, x=0.97)
    fig.savefig("chart_p4_country_origin.pdf",
                bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)
    print("Saved: chart_p4_country_origin.pdf")


if __name__ == "__main__":
    chart_pattern2_comparison_vs_discovery()
    chart_pattern4_country_origin()
    print("\nPattern 2 (small multiples) and Pattern 4 charts generated.")
