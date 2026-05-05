"""
Pattern 4 — Heritage geography reinforces algorithmic bias.

Two-panel spread (FIGSIZE_SPREAD = 7.5 × 4.5). Left panel = Olive Oil,
right panel = Skincare. Each panel is a strip plot:

  - Y-axis: country of origin, sorted by mean AI Presence (descending)
  - X-axis: AI Presence (%)
  - Each dot = one brand from that country
  - Color: heritage countries (Indigo) vs newer producer countries
    (Copper Plate). Color carries the editorial claim.

The structural claim: heritage countries (Italy for olive oil, France/Korea
for skincare) cluster at the top of each panel with high AI Presence;
newer producer countries (USA/California, Australia for olive oil; USA
for skincare) cluster at the bottom with lower AI Presence. The chart
makes this visible by sort order + color encoding.

Renders to: reports/output/chart_p4_spread.pdf

Brand spec: third_system_brand.json schema 1.4
Data source: most-recent leaderboard per category
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
# Brand → country mapping (hard-coded; switch to data column if added later)
# ---------------------------------------------------------------------------

# OLIVE OIL country origins. Heritage = Mediterranean producers with
# centuries of cultural association; Newer = California/Australia DTC era.
OLIVE_OIL_COUNTRY = {
    # Italy — heritage
    "Frantoio Muraglia":   "Italy",
    "Frescobaldi Laudemio": "Italy",
    "Bertolli":            "Italy",
    "Colavita":            "Italy",
    "Filippo Berio":       "Italy",
    "Lucini":              "Italy",
    "Olio Verde":          "Italy",
    "Manni":               "Italy",
    "Colonna":             "Italy",
    "Partanna":            "Italy",
    # Spain — heritage
    "Castillo de Canena":  "Spain",
    "Goya":                "Spain",
    "Núñez de Prado":      "Spain",
    "Nunez de Prado":      "Spain",   # accent-stripped variant
    # Greece — heritage
    "Kosterina":           "Greece",
    # USA / California — newer
    "California Olive Ranch": "USA",
    "Brightland":          "USA",
    "Graza":               "USA",
    "McEvoy Ranch":        "USA",
    "Fly By Jing":         "USA",     # US DTC condiment brand (newer producer)
    # Australia — newer
    "Cobram Estate":       "Australia",
}

# SKINCARE country origins. Heritage = European luxury (France) + East Asian
# tradition (Korea, Japan); Newer = US-founded brands and DTC entrants.
SKINCARE_COUNTRY = {
    # France — heritage
    "La Roche-Posay":   "France",
    "Lancôme":          "France",
    "Lancome":          "France",
    "La Mer":           "France",
    "Bioderma":         "France",
    "Avène":            "France",
    "Avene":            "France",     # accent-stripped variant
    "Kiehl's":          "France",     # Kiehl's is L'Oréal Paris-owned, France-claim
    "Kiehls":           "France",
    # Germany — Eu-luxury heritage
    "Augustinus Bader": "Germany",
    "Eucerin":          "Germany",
    # Korea — heritage
    "Sulwhasoo":        "Korea",
    "AmorePacific":     "Korea",
    "Beauty of Joseon": "Korea",
    # Japan — heritage
    "SK-II":            "Japan",
    "Tatcha":           "Japan",
    # USA — newer
    "CeraVe":           "USA",
    "Drunk Elephant":   "USA",
    "Skinceuticals":    "USA",
    "Cetaphil":         "USA",
    "Paula's Choice":   "USA",
    "Paulas Choice":    "USA",
    "Vanicream":        "USA",
    "Estée Lauder":     "USA",
    "Estee Lauder":     "USA",
    "Clinique":         "USA",
    "Neutrogena":       "USA",
    "First Aid Beauty": "USA",
    "EltaMD":           "USA",
    "Aveeno":           "USA",
    "The Ordinary":     "USA",        # parent DECIEM is Canadian/Estée; commonly tagged USA
    "Youth to the People": "USA",
    "Olay":             "USA",
    "Origins":          "USA",
    "Dermalogica":      "USA",
    "Murad":            "USA",
    "Glossier":         "USA",
    "Sunday Riley":     "USA",
}

# Heritage classification per category — defines the color encoding.
HERITAGE_COUNTRIES = {
    "Olive Oil": {"Italy", "Spain", "Greece"},
    "Skincare":  {"France", "Korea", "Japan", "Germany"},
}


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DOT_SIZE = 36
COUNTRY_LINE_COLOR = "#dddddd"

SOURCE_TEXT = "Source: Third System AI Presence Index v0.6 · n=96 per category · 30 Apr 2026"


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

def get_pattern4_data() -> dict[str, list[dict]]:
    """Load most-recent leaderboards for Olive Oil and Skincare,
    annotate each brand with its country of origin.

    Returns a dict mapping category to list of brand row dicts:
      {brand, presence, tier, country, is_heritage}

    Brands without a known country mapping are dropped (with a warn).
    """
    aias_root = _REPORTS.parent
    original_cwd = Path.cwd()
    try:
        import os
        os.chdir(aias_root)
        leaderboards, _ = cd.load_all_categories()
    finally:
        os.chdir(original_cwd)

    out: dict[str, list[dict]] = {}
    for cat in ("Olive Oil", "Skincare"):
        if cat not in leaderboards:
            print(f"  [warn] Pattern 4: no leaderboard for {cat} — skipping")
            continue
        country_map = OLIVE_OIL_COUNTRY if cat == "Olive Oil" else SKINCARE_COUNTRY
        heritage_set = HERITAGE_COUNTRIES[cat]

        rows = []
        unmapped = []
        for r in leaderboards[cat]:
            brand = r["brand"]
            country = country_map.get(brand)
            if country is None:
                unmapped.append(brand)
                continue
            rows.append({
                "brand": brand,
                "presence": float(r["presence"]),
                "tier": r.get("tier", ""),
                "country": country,
                "is_heritage": country in heritage_set,
            })
        if unmapped:
            print(f"  [warn] Pattern 4 [{cat}]: no country mapping for: "
                  f"{', '.join(unmapped)}")
        out[cat] = rows
    return out


# ---------------------------------------------------------------------------
# Per-panel rendering
# ---------------------------------------------------------------------------

def _render_panel(ax, rows: list[dict], category_label: str,
                  heritage_set: set[str], sizes: dict) -> None:
    """Render one category strip plot.

    Y rows = countries, sorted by mean AI Presence descending.
    Each dot = one brand. Color encodes heritage vs newer.
    """
    if not rows:
        ax.text(50, 50, "no data", ha="center", va="center",
                fontsize=sizes["axis_tick"], color=cs.COLOR_MUTED)
        return

    # Group brands by country
    by_country: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_country[r["country"]].append(r)

    # Sort countries by mean Presence DESCENDING
    country_means = {
        c: float(np.mean([b["presence"] for b in brands]))
        for c, brands in by_country.items()
    }
    sorted_countries = sorted(country_means, key=country_means.get, reverse=True)

    # Set up Y axis: country labels with brand-count parenthetical
    n_countries = len(sorted_countries)
    y_positions = list(range(n_countries))
    y_labels = []
    for c in sorted_countries:
        n = len(by_country[c])
        y_labels.append(f"{c} (n={n})")

    # X axis setup
    ax.set_xlim(-3, 105)
    ax.set_xticks([0, 20, 40, 60, 80, 100])
    ax.set_xlabel("AI Presence (%)", fontsize=sizes["axis_label"])

    # Y axis
    ax.set_yticks(y_positions)
    ax.set_yticklabels(y_labels, fontsize=sizes["axis_tick"])
    ax.set_ylim(-0.6, n_countries - 0.4)
    ax.invert_yaxis()  # Highest-mean country on TOP

    # Subtle horizontal line per row to anchor reading
    for y in y_positions:
        ax.axhline(y=y, color=COUNTRY_LINE_COLOR, linewidth=0.4,
                   zorder=1, alpha=0.6)

    # Mean-marker per country: a small vertical tick at the country mean,
    # so readers can compare country-level summary alongside individual dots
    for i, c in enumerate(sorted_countries):
        mean_x = country_means[c]
        ax.plot([mean_x, mean_x], [i - 0.25, i + 0.25],
                color=cs.BLACK_60, linewidth=1.2, zorder=2)

    # Plot brand dots — heritage in Indigo, newer in Copper Plate.
    # Apply 1D vertical jitter PER ROW so brands at similar Presence values
    # don't stack. axis="y" mode: dots that share an x-value get fanned
    # along the y-axis within the row's narrow band; x stays at the brand's
    # actual Presence value.
    for i, c in enumerate(sorted_countries):
        is_heritage_country = c in heritage_set
        color = cs.ACCENT_INDIGO if is_heritage_country else cs.ACCENT_COPPER_PLATE

        country_brands = by_country[c]
        xs = np.array([b["presence"] for b in country_brands])
        ys = np.full(len(xs), float(i))  # all start at row center

        # Jitter parameters tuned against real data:
        # - threshold=5 catches all close-but-not-identical brand clusters
        #   (e.g., Filippo 1.0, Bertolli 2.1, Colavita 4.2 all chain together)
        # - spread=0.32 fans clustered dots ±0.32 y-units inside the row band
        #   (row is 1 unit tall, so spread stays inside while being visible)
        if len(xs) > 1:
            jx, jy = cu.jitter_overlapping_points(
                xs, ys,
                threshold=5.0,
                spread=0.32,
                axis="y",
            )
        else:
            jx, jy = xs, ys

        ax.scatter(
            jx, jy,
            s=DOT_SIZE,
            c=color,
            edgecolors=cs.COLOR_TEXT, linewidths=0.4,
            alpha=0.9, zorder=3,
        )

    # Panel title
    ax.set_title(category_label,
                 fontsize=sizes["subtitle"], fontweight="bold",
                 color=cs.COLOR_TEXT, loc="left", pad=4)

    cs.style_axis_minimal(ax, orientation="horizontal_dot")


# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------

def render(output_dir: Path | str | None = None) -> list[Path]:
    """Render Pattern 4 two-panel spread."""
    data = get_pattern4_data()
    if not data:
        raise RuntimeError(
            "No Pattern 4 data — need leaderboards for Olive Oil and Skincare."
        )

    # Two panels side by side at FIGSIZE_SPREAD (7.5 × 4.5)
    fig, axes = plt.subplots(
        nrows=1, ncols=2,
        figsize=cs.FIGSIZE_SPREAD,
    )
    sizes = cs.font_sizes_for("6col")  # spread uses 6col font sizing

    # Manual margins — multi-panel pattern (don't use bbox='tight')
    fig.subplots_adjust(
        top=0.78,       # room for figure title + 2-line subtitle
        bottom=0.22,    # room for x-axis labels + legend + source line
        left=0.13,      # room for country labels (longest: "California (USA)")
        right=0.97,
        wspace=0.42,    # horizontal between panels — generous (long y-labels)
    )

    if "Olive Oil" in data:
        _render_panel(axes[0], data["Olive Oil"], "Olive Oil",
                      HERITAGE_COUNTRIES["Olive Oil"], sizes)
    if "Skincare" in data:
        _render_panel(axes[1], data["Skincare"], "Skincare",
                      HERITAGE_COUNTRIES["Skincare"], sizes)

    # Figure-level title + 2-line subtitle
    fig.text(
        0.04, 0.965,
        "Heritage geography reinforces algorithmic bias",
        fontsize=sizes["title"], fontweight="bold",
        color=cs.COLOR_TEXT, ha="left", va="top",
    )
    fig.text(
        0.04, 0.92,
        "AI Presence per brand, grouped by country of origin. "
        "Countries sorted by mean Presence descending.",
        fontsize=sizes["subtitle"], color=cs.COLOR_MUTED,
        ha="left", va="top",
    )
    fig.text(
        0.04, 0.89,
        "Heritage producer countries (Indigo) cluster at top; "
        "newer producers (Copper Plate) trail.",
        fontsize=sizes["subtitle"], color=cs.COLOR_MUTED,
        ha="left", va="top",
    )

    # Inline color legend — placed in the wspace gap or inside the chart area
    # to avoid colliding with the subtitle. We use the upper-RIGHT area of
    # the figure but BELOW the title/subtitle band, anchoring to the right
    # edge of the right panel.
    from matplotlib.lines import Line2D
    legend_elems = [
        Line2D([0], [0], marker="o", color="w",
               markerfacecolor=cs.ACCENT_INDIGO,
               markeredgecolor=cs.COLOR_TEXT, markeredgewidth=0.4,
               markersize=8, label="Heritage producer"),
        Line2D([0], [0], marker="o", color="w",
               markerfacecolor=cs.ACCENT_COPPER_PLATE,
               markeredgecolor=cs.COLOR_TEXT, markeredgewidth=0.4,
               markersize=8, label="Newer producer"),
        Line2D([0], [0], color=cs.BLACK_60, linewidth=1.2,
               label="Country mean"),
    ]
    # Place legend at the BOTTOM of the figure, between the panels and the
    # source line. ncol=3 keeps it on a single horizontal row.
    fig.legend(
        handles=legend_elems,
        loc="lower center",
        bbox_to_anchor=(0.5, 0.06),
        fontsize=sizes["legend"],
        frameon=False,
        ncol=3,
    )

    # Source line
    fig.text(
        0.04, 0.025, SOURCE_TEXT,
        fontsize=sizes["source_caption"], color=cs.COLOR_MUTED,
        style="italic", ha="left", va="bottom",
    )

    # Save (no bbox='tight' — would eat reserved margins)
    if output_dir is None:
        output_dir = _REPORTS / "output"
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_pdf = output_dir / "chart_p4_spread.pdf"
    fig.savefig(output_pdf, dpi=cs.DPI_PRINT, pad_inches=cs.PAD_INCHES)
    plt.close(fig)
    return [output_pdf]


if __name__ == "__main__":
    paths = render()
    print(f"Rendered Pattern 4 (country origin two-panel spread):")
    for p in paths:
        print(f"  {p}")
