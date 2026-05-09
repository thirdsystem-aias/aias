#!/usr/bin/env python3
"""
v0.10 Naive-Phantom Rate Longitudinal Stability — chart builder.

Reads scoring outputs from /Users/pablou/aias/osf/v10/analysis/.
Writes chart PDFs to /Users/pablou/aias/reports/output/chart_v10_*.pdf.

Charts:
  - chart_v10_h2_naive_caveated.pdf   — per-wave naive vs caveated breakdown
  - chart_v10_h3_decoupling.pdf       — gross vs naive directional change
  - chart_v10_valence_distribution.pdf — v0.7 5-class valence distribution by wave

Brand tokens loaded from /Users/pablou/aias/brand/third_system_brand.json (Indigo #37237B primary).
Font: Akkurat Pro auto-detected from ~/Library/Fonts and ~/.fonts; falls back to sans-serif.
Figsizes match v0.9's 6-column conventions (7.50 × 4.00 to 7.50 × 4.50).
"""

import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # headless
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# --- Paths ---
AIAS_ROOT = Path("/Users/pablou/aias")
V10_ROOT = AIAS_ROOT / "osf" / "v10"
BRAND_JSON = AIAS_ROOT / "brand" / "third_system_brand.json"
SCORING_JSON = V10_ROOT / "analysis" / "canonical_scoring.json"
CLASSIFICATIONS_CSV = V10_ROOT / "data" / "classifications.csv"
OUTPUT_DIR = AIAS_ROOT / "reports" / "output"


# --- Source line (consistent across all charts) ---
SOURCE_TEXT = (
    "Source: AIAS Presence Index v0.10 · Third System™. "
    "Mint × matched-subset (Sonnet 4.6, gpt-5.4-mini). "
    "n = 83 (t₁ = 43; t₂ = 40)."
)


def add_source(fig, palette):
    """Add a small italic source line at the bottom-left of the figure."""
    fig.text(
        0.02, 0.012, SOURCE_TEXT,
        fontsize=7.5, color=palette["anchor_black"], alpha=0.75,
        style="italic", ha="left", va="bottom",
    )


# ---------------------------------------------------------------------------
# Brand & typography
# ---------------------------------------------------------------------------

def load_palette() -> dict:
    """Load brand palette from third_system_brand.json."""
    with open(BRAND_JSON) as f:
        brand = json.load(f)
    p = brand["palette"]
    return {
        "indigo": p["primary_brand"]["indigo"]["hex"],
        "anchor_black": p["anchor_black"]["hex"],
        "paper": p["paper_off_white"]["hex"],
        "petro": p["brand_supporting"]["petro"]["hex"],
        "lavender": p["brand_supporting"]["lavender_grey"]["hex"],
    }


def setup_fonts():
    """Register Akkurat Pro from common macOS/Linux locations; fall back gracefully.

    Critical: after addfont(), query matplotlib for the *actual* internal family
    names — they often differ from the filename (e.g. file 'AkkuratPro-Bold.otf'
    may register under family 'Akkurat Pro' or 'Akkurat Pro Bold' depending on
    how the font was packaged).
    """
    from matplotlib import font_manager
    candidates = []
    for pattern in (
        "Library/Fonts/Akkurat*.otf",
        "Library/Fonts/Akkurat*.ttf",
        ".fonts/Akkurat*.otf",
        ".fonts/Akkurat*.ttf",
        ".fonts/Akkurat/*.otf",
        ".fonts/Akkurat/*.ttf",
    ):
        candidates.extend(Path.home().glob(pattern))

    registered_names = set()
    for p in candidates:
        try:
            font_manager.fontManager.addfont(str(p))
            prop = font_manager.FontProperties(fname=str(p))
            registered_names.add(prop.get_name())
        except Exception:
            pass

    if registered_names:
        # Pick a "regular-ish" family as primary: prefer non-light, non-bold,
        # non-italic faces. Then list all variants as fallbacks so weights
        # within charts can be matched to the right registered family.
        def _rank(name):
            n = name.lower()
            return (
                "light" in n,    # de-prioritize light family
                "bold" in n,     # de-prioritize bold family
                "italic" in n,   # de-prioritize italic family
                len(n),
            )
        ordered = sorted(registered_names, key=_rank)
        plt.rcParams["font.family"] = ordered + ["sans-serif"]
        print(f"[fonts] registered {len(candidates)} Akkurat file(s)")
        print(f"[fonts] internal family names detected: {sorted(registered_names)}")
        print(f"[fonts] font.family priority: {plt.rcParams['font.family'][:3]}…")
    else:
        plt.rcParams["font.family"] = ["sans-serif"]
        print("[fonts] Akkurat not found — falling back to system sans-serif")

    plt.rcParams["font.size"] = 10
    plt.rcParams["pdf.fonttype"] = 42  # embed TrueType for SSRN compatibility


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_scoring() -> dict:
    with open(SCORING_JSON) as f:
        return json.load(f)


def load_classifications() -> list:
    with open(CLASSIFICATIONS_CSV) as f:
        return list(csv.DictReader(f))


# ---------------------------------------------------------------------------
# Figure setup helpers
# ---------------------------------------------------------------------------

def setup_axes(ax, palette):
    """Apply consistent grid, spines, and background across all charts."""
    ax.set_facecolor("white")
    ax.grid(axis="x", color=palette["lavender"], alpha=0.35, linewidth=0.5)
    ax.set_axisbelow(True)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color(palette["anchor_black"])
        ax.spines[spine].set_linewidth(0.6)


# ---------------------------------------------------------------------------
# Chart 1 — H2 per-wave naive vs caveated
# ---------------------------------------------------------------------------

def chart_h2_naive_caveated(scoring, palette, output_dir):
    metrics = scoring["metrics_primary"]
    fig, ax = plt.subplots(figsize=(7.50, 4.00), dpi=200)
    fig.set_facecolor("white")
    setup_axes(ax, palette)

    waves = ["t1", "t2"]
    n_caveated = [metrics[w]["n_caveated"] for w in waves]
    n_naive = [metrics[w]["n_naive"] for w in waves]
    n_total = [metrics[w]["n_matched_mint"] for w in waves]
    r_naive = [metrics[w]["r_naive_pct"] for w in waves]

    y = [0, 1]
    bar_height = 0.42

    # Caveated bars (lavender_grey)
    ax.barh(
        y, n_caveated, bar_height,
        color=palette["lavender"], edgecolor=palette["anchor_black"], linewidth=0.5,
        label="Caveated (live_with_caveat / status_correction / historical_reference)",
    )
    # Naive bars (indigo) — stacked on the right
    ax.barh(
        y, n_naive, bar_height, left=n_caveated,
        color=palette["indigo"], edgecolor=palette["anchor_black"], linewidth=0.5,
        label="Naive (live_recommendation, no caveat)",
    )

    # Annotate inside caveated bars
    for i in range(len(waves)):
        ax.text(
            n_caveated[i] / 2, i,
            f"caveated: {n_caveated[i]}",
            ha="center", va="center", color="white", fontsize=11, fontweight="bold",
        )
        if n_naive[i] > 0:
            ax.text(
                n_caveated[i] + n_naive[i] + 1.5, i,
                f"naive: {n_naive[i]}",
                ha="left", va="center", color=palette["indigo"],
                fontsize=11, fontweight="bold",
            )
        # Right-side total + rate (pushed further right to clear the "naive: N" label)
        ax.text(
            n_total[i] + 16, i,
            f"n = {n_total[i]}    rₙ = {r_naive[i]:.2f}%",
            ha="left", va="center", color=palette["anchor_black"], fontsize=9.5,
        )

    ax.set_yticks(y)
    ax.set_yticklabels(["t₁  (v0.6 baseline)", "t₂  (v0.9 re-baseline)"], fontsize=11)
    ax.invert_yaxis()
    ax.set_xlabel("Matched-subset Mint mentions (Sonnet 4.6 + gpt-5.4-mini)", fontsize=10)
    ax.set_xlim(0, 75)
    ax.set_title(
        "H2 — Naive vs caveated phantom presence by wave",
        fontsize=12.5, fontweight="bold", color=palette["indigo"], pad=14, loc="left",
    )

    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.30),
              ncol=2, frameon=False, fontsize=9)

    add_source(fig, palette)
    plt.tight_layout()
    out = output_dir / "chart_v10_h2_naive_caveated.pdf"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✓ {out.name}  (7.50 × 4.00)")


# ---------------------------------------------------------------------------
# Chart 2 — H3 decoupling
# ---------------------------------------------------------------------------

def chart_h3_decoupling(scoring, palette, output_dir):
    metrics = scoring["metrics_primary"]
    h3 = scoring["hypotheses"]["H3_diagnostic"]

    fig, ax = plt.subplots(figsize=(7.50, 4.40), dpi=200)
    fig.set_facecolor("white")
    setup_axes(ax, palette)
    ax.grid(axis="y", color=palette["lavender"], alpha=0.35, linewidth=0.5)
    ax.grid(axis="x", visible=False)

    gross_t1 = h3["gross_presence_t1_pct"]
    gross_t2 = h3["gross_presence_t2_pct"]
    naive_t1 = metrics["t1"]["r_naive_pct"]
    naive_t2 = metrics["t2"]["r_naive_pct"]

    x = [0, 1]
    delta_gross = gross_t2 - gross_t1
    delta_naive = naive_t2 - naive_t1

    # Gross presence (petro)
    ax.plot(
        x, [gross_t1, gross_t2], "o-",
        color=palette["petro"], linewidth=2.5, markersize=10,
        label=f"Gross Presence  (Δ = {delta_gross:+.2f} pp)",
    )
    ax.annotate(f"{gross_t1:.2f}%", (0, gross_t1), textcoords="offset points",
                xytext=(-12, 10), ha="right", color=palette["petro"], fontweight="bold", fontsize=10)
    ax.annotate(f"{gross_t2:.2f}%", (1, gross_t2), textcoords="offset points",
                xytext=(12, 10), ha="left", color=palette["petro"], fontweight="bold", fontsize=10)

    # Naive rate (indigo)
    ax.plot(
        x, [naive_t1, naive_t2], "s-",
        color=palette["indigo"], linewidth=2.5, markersize=10,
        label=f"Naive rate  (Δ = {delta_naive:+.2f} pp)",
    )
    # Place naive labels ABOVE markers (not below) so 0.00% doesn't crowd the x-axis labels
    ax.annotate(f"{naive_t1:.2f}%", (0, naive_t1), textcoords="offset points",
                xytext=(-12, 10), ha="right", color=palette["indigo"], fontweight="bold", fontsize=10)
    ax.annotate(f"{naive_t2:.2f}%", (1, naive_t2), textcoords="offset points",
                xytext=(12, 10), ha="left", color=palette["indigo"], fontweight="bold", fontsize=10)

    ax.set_xticks(x)
    ax.set_xticklabels(["t₁  (v0.6 baseline)", "t₂  (v0.9 re-baseline)"], fontsize=11)
    ax.set_xlim(-0.35, 1.35)
    ax.set_ylim(-3, 52)
    ax.set_ylabel("Rate (%)", fontsize=10)
    ax.set_title(
        "H3 — Directional decoupling: gross down, naive up",
        fontsize=12.5, fontweight="bold", color=palette["indigo"], pad=14, loc="left",
    )

    ax.legend(loc="center right", frameon=False, fontsize=10)

    add_source(fig, palette)
    plt.tight_layout(rect=[0, 0.06, 1, 1])  # reserve bottom 6% for source line
    out = output_dir / "chart_v10_h3_decoupling.pdf"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✓ {out.name}  (7.50 × 4.40)")


# ---------------------------------------------------------------------------
# Chart 3 — v0.7 5-class valence distribution by wave
# ---------------------------------------------------------------------------

def chart_valence_distribution(classifications, palette, output_dir):
    fig, ax = plt.subplots(figsize=(7.50, 4.50), dpi=200)
    fig.set_facecolor("white")
    setup_axes(ax, palette)

    valence_classes = [
        "live_recommendation",
        "live_with_caveat",
        "status_correction",
        "historical_reference",
        "ambiguous",
    ]
    # Color order: naive distinct (indigo), then three caveat shades, then ambiguous neutral
    valence_colors = [
        palette["indigo"],         # naive
        palette["petro"],          # caveated subtypes
        palette["lavender"],       # status_correction
        palette["anchor_black"],   # historical_reference
        "#888888",                 # ambiguous — neutral grey
    ]

    waves = ["t1", "t2"]
    counts = {w: {v: 0 for v in valence_classes} for w in waves}
    for r in classifications:
        w = r.get("wave_v10")
        v = r.get("valence")
        if w in counts and v in counts[w]:
            counts[w][v] += 1

    y = [0, 1]
    bar_height = 0.42

    for i, w in enumerate(waves):
        left = 0
        for j, vc in enumerate(valence_classes):
            n = counts[w][vc]
            if n > 0:
                ax.barh(
                    y[i], n, bar_height, left=left,
                    color=valence_colors[j], edgecolor="white", linewidth=1.5,
                )
                if n >= 4:
                    text_color = "white" if vc != "live_with_caveat" else "white"
                    ax.text(
                        left + n / 2, y[i], str(n),
                        ha="center", va="center",
                        color=text_color, fontsize=10, fontweight="bold",
                    )
                left += n

    legend_labels = {
        "live_recommendation": "live_recommendation (→ naive)",
        "live_with_caveat": "live_with_caveat",
        "status_correction": "status_correction",
        "historical_reference": "historical_reference",
        "ambiguous": "ambiguous",
    }
    legend_patches = [
        Patch(facecolor=valence_colors[j], edgecolor="white",
              label=legend_labels[valence_classes[j]])
        for j in range(len(valence_classes))
    ]
    ax.legend(
        handles=legend_patches, loc="lower center",
        bbox_to_anchor=(0.5, -0.32), ncol=3, frameon=False, fontsize=9,
    )

    ax.set_yticks(y)
    ax.set_yticklabels(["t₁", "t₂"], fontsize=12)
    ax.invert_yaxis()
    ax.set_xlabel("Number of Mint-mentioning matched-subset responses", fontsize=10)
    ax.set_xlim(0, 50)
    ax.set_title(
        "v0.7 5-class valence distribution by wave",
        fontsize=12.5, fontweight="bold", color=palette["indigo"], pad=14, loc="left",
    )

    add_source(fig, palette)
    plt.tight_layout()
    out = output_dir / "chart_v10_valence_distribution.pdf"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✓ {out.name}  (7.50 × 4.50)")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 64)
    print("v0.10 chart builder — Naive-Phantom Rate Longitudinal Stability")
    print("=" * 64)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    setup_fonts()
    palette = load_palette()
    print(f"[brand] indigo={palette['indigo']}  petro={palette['petro']}  "
          f"lavender={palette['lavender']}")

    scoring = load_scoring()
    classifications = load_classifications()
    print(f"[data] {len(classifications)} classifications loaded")

    print("\nBuilding charts:")
    chart_h2_naive_caveated(scoring, palette, OUTPUT_DIR)
    chart_h3_decoupling(scoring, palette, OUTPUT_DIR)
    chart_valence_distribution(classifications, palette, OUTPUT_DIR)

    print(f"\nAll charts written to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
