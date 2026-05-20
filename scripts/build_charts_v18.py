"""
build_charts_v18.py — v0.18 Chart Pipeline

Produces three matplotlib PDFs at locked figsize for the brand-format
report and SSRN paper figures. Chart order matches the v0.17 chart suite
(mention rate distribution / cell attrition / dissociation scatter).

Inputs:
  - data/phase_a/v0.18/phase_a_results.json   (from acquire_phase_a_v18.py)
  - data/phase_b/v0.18/phase_b_results.json   (from acquire_phase_b_v18.py)
  - data/verdicts/v0_18_verdict.json          (from score_v18.py)

Outputs:
  - reports/figs/v18/chart_01_mention_rate_distribution.pdf
  - reports/figs/v18/chart_02_cell_attrition.pdf
  - reports/figs/v18/chart_03_dissociation_scatter.pdf

Pre-reg lock:    v0.18-prereg-r1 @ commit 183386c
Branch:          v0.18-il-gradient
Predecessor:     scripts/build_charts_v17.py (Premium Kitchenware)

Style notes:
  - Figsize locked at (6.0, 4.0) inches per chart slot in the report layout
  - IL-gradient colormap aligns Cell C (medium IL) → Cell A (medium-high)
    → Cell B (high IL) with light → mid → dark Indigo (#37237B primary)
  - Akkurat font preferred; falls back to matplotlib default if unavailable
  - All chart text sized for legibility at the report's locked figure size
"""

import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # headless PDF backend
import matplotlib.pyplot as plt
import matplotlib.patches as patches


# ============================================================
# Configuration — LOCKED per v0.18-prereg-r1 and brand tokens
# ============================================================

PHASE = "v0.18"

# Locked chart figsize — must match report layout slot reservation
CHART_FIGSIZE = (6.0, 4.0)
CHART_DPI = 300

# Attribution footer — applied to every chart
SOURCE_LINE = (
    "Source: AIAS™ Presence Measurement Protocol v1.4 (SSRN 6799479) · "
    "v0.18-prereg-r1 · osf.io/ec6wh/v18/"
)
ATTRIBUTION_LINE = "Third\u00a0System™  ·  thirdsystem.ai"

# Brand colors — Third System brand tokens
# IL-gradient ordering: light (C, medium IL) → mid (A, medium-high) → dark (B, high IL)
INDIGO_PRIMARY = "#37237B"
CELL_COLORS = {
    "cell_c_mass_prestige":   "#B5A8D4",   # lighter — medium IL
    "cell_a_designer_niche":  "#6E5BA8",   # mid — medium-high IL
    "cell_b_indie_artisan":   "#37237B",   # primary — high IL
}
CELL_LABELS = {
    "cell_a_designer_niche":  "Cell A\nDesigner-niche\n(med-high IL)",
    "cell_b_indie_artisan":   "Cell B\nIndie/artisan\n(high IL)",
    "cell_c_mass_prestige":   "Cell C\nMass-prestige\n(medium IL)",
}
# Visual display order — IL-gradient ascending (left to right)
CELL_DISPLAY_ORDER = [
    "cell_c_mass_prestige",
    "cell_a_designer_niche",
    "cell_b_indie_artisan",
]

# Decision rule thresholds — per pre-reg
C1_PANEL_FLOOR = 12
DISSOCIATION_C_P_FLOOR = 5
DISSOCIATION_MENTION_CEILING = 2

# Matplotlib base style
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Akkurat Pro", "Akkurat", "Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 9,
    "axes.titlesize": 11,
    "axes.titleweight": "bold",
    "axes.labelsize": 9,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 0.6,
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
    "legend.fontsize": 8,
    "legend.frameon": False,
})


# ============================================================
# Chart chrome — subtitle + source footer (applied to every chart)
# ============================================================

def apply_chrome(fig, ax, title: str, subtitle: str) -> None:
    """
    Apply consistent chrome to a chart: bold title, italic subtitle below it,
    source line at bottom-left, Third System attribution at bottom-right.
    Title set via fig.suptitle / ax.text to allow the two-line title block.
    """
    # Title block: bold title, italic subtitle directly below
    ax.set_title("")  # clear any per-axes title; we lay out the block manually
    fig.suptitle(title, fontsize=11, fontweight="bold", y=0.985, ha="center")
    fig.text(
        0.5, 0.935, subtitle,
        fontsize=9, style="italic", color="#444444", ha="center",
    )
    # Source footer (bottom-left) and attribution (bottom-right)
    fig.text(
        0.02, 0.012, SOURCE_LINE,
        fontsize=6.5, color="#666666", ha="left",
    )
    fig.text(
        0.98, 0.012, ATTRIBUTION_LINE,
        fontsize=6.5, color="#666666", ha="right",
    )


# ============================================================
# Data loaders — fail-fast on missing inputs
# ============================================================

def load_json_required(path: Path, what: str) -> dict:
    if not path.exists():
        print(
            f"\n✗ Missing input: {what} expected at {path}\n"
            f"  Run upstream pipeline first:\n"
            f"    1. python scripts/acquire_phase_a_v18.py\n"
            f"    2. python scripts/acquire_phase_b_v18.py\n"
            f"    3. python scripts/score_v18.py\n",
            file=sys.stderr,
        )
        sys.exit(1)
    with path.open(encoding="utf-8") as f:
        return json.load(f)


# ============================================================
# Chart 1 — Mention rate distribution per cell
# ============================================================

def chart_mention_rate_distribution(phase_b: dict, output_path: Path) -> None:
    """
    Strip plot of per-brand Phase B mention counts (0..18) per cell.
    Iwachu-pattern dissociation threshold drawn as horizontal reference.
    """
    fig, ax = plt.subplots(figsize=CHART_FIGSIZE, dpi=CHART_DPI)

    for x_pos, cell_name in enumerate(CELL_DISPLAY_ORDER):
        cell = phase_b["cells"][cell_name]
        counts = [rec["mention_count"] for rec in cell["per_brand"]]
        color = CELL_COLORS[cell_name]
        # Strip plot with small horizontal jitter
        ax.scatter(
            [x_pos + (i - len(counts) / 2) * 0.04 for i in range(len(counts))],
            counts,
            color=color, s=42, alpha=0.85, edgecolors="white", linewidths=0.6,
        )

    # Iwachu-pattern mention-ceiling reference line
    ax.axhline(
        DISSOCIATION_MENTION_CEILING,
        color="#999999", linestyle=":", linewidth=0.8,
    )
    ax.text(
        len(CELL_DISPLAY_ORDER) - 0.5, DISSOCIATION_MENTION_CEILING + 0.3,
        f"Iwachu-pattern ceiling (≤ {DISSOCIATION_MENTION_CEILING}/18)",
        fontsize=7, color="#666666", ha="right", va="bottom",
    )

    ax.set_xticks(range(len(CELL_DISPLAY_ORDER)))
    ax.set_xticklabels([CELL_LABELS[c] for c in CELL_DISPLAY_ORDER], fontsize=8)
    ax.set_ylabel("Phase B mention count (max = 18)")
    ax.set_ylim(-0.5, 18.5)
    ax.set_yticks([0, 2, 6, 12, 18])

    apply_chrome(
        fig, ax,
        title="Phase B mention rate distribution per cell",
        subtitle=(
            "v0.18 indie fragrance — 24 brands × 3 cells, "
            "IL-gradient ascending C → A → B"
        ),
    )
    fig.tight_layout(rect=[0, 0.04, 1, 0.91])
    fig.savefig(output_path, format="pdf", bbox_inches="tight")
    plt.close(fig)


# ============================================================
# Chart 2 — Cell attrition (Phase A → Phase B)
# ============================================================

def chart_cell_attrition(phase_a: dict, phase_b: dict, output_path: Path) -> None:
    """
    Paired bars per cell: Phase A registered n vs Phase B mention-positive n.
    C1 floor (n ≥ 12 total) annotated as horizontal reference.
    """
    fig, ax = plt.subplots(figsize=CHART_FIGSIZE, dpi=CHART_DPI)

    bar_width = 0.36
    x_positions = list(range(len(CELL_DISPLAY_ORDER)))

    phase_a_ns, phase_b_ns = [], []
    for cell_name in CELL_DISPLAY_ORDER:
        a_brands = {r["brand"] for r in phase_a["cells"][cell_name]["per_brand"]}
        b_records = phase_b["cells"][cell_name]["per_brand"]
        b_positive = sum(1 for r in b_records if r["mention_count"] > 0)
        phase_a_ns.append(len(a_brands))
        phase_b_ns.append(b_positive)

    for x, cell_name in enumerate(CELL_DISPLAY_ORDER):
        color = CELL_COLORS[cell_name]
        ax.bar(x - bar_width / 2, phase_a_ns[x], bar_width,
               color=color, alpha=0.45, edgecolor="white", linewidth=0.6,
               label="Phase A registered" if x == 0 else None)
        ax.bar(x + bar_width / 2, phase_b_ns[x], bar_width,
               color=color, alpha=1.0, edgecolor="white", linewidth=0.6,
               label="Phase B mention-positive" if x == 0 else None)

    # C1 floor reference (per-cell equivalent share of n ≥ 12)
    c1_per_cell_equiv = C1_PANEL_FLOOR / len(CELL_DISPLAY_ORDER)
    ax.axhline(c1_per_cell_equiv, color="#999999", linestyle=":", linewidth=0.8)
    ax.text(
        len(CELL_DISPLAY_ORDER) - 0.5, c1_per_cell_equiv + 0.15,
        f"C1 per-cell equiv. (worldwide n ≥ {C1_PANEL_FLOOR} / 3)",
        fontsize=7, color="#666666", ha="right", va="bottom",
    )

    ax.set_xticks(x_positions)
    ax.set_xticklabels([CELL_LABELS[c] for c in CELL_DISPLAY_ORDER], fontsize=8)
    ax.set_ylabel("Brand count")
    ax.legend(loc="upper right")
    ax.set_ylim(0, 10)

    apply_chrome(
        fig, ax,
        title="Cell attrition: Phase A registered → Phase B mention-positive",
        subtitle=(
            "Light bars: Phase A panel (n=8/cell). Dark bars: brands with "
            "≥1 mention across 18 Phase B observations."
        ),
    )
    fig.tight_layout(rect=[0, 0.04, 1, 0.91])
    fig.savefig(output_path, format="pdf", bbox_inches="tight")
    plt.close(fig)


# ============================================================
# Chart 3 — Dissociation scatter
# ============================================================

def chart_dissociation_scatter(phase_a: dict, phase_b: dict, output_path: Path) -> None:
    """
    Scatter of Phase A C_P (x) vs Phase B mention count (y) per brand.
    Iwachu-pattern dissociation quadrant shaded.
    """
    fig, ax = plt.subplots(figsize=CHART_FIGSIZE, dpi=CHART_DPI)

    # Iwachu-pattern dissociation quadrant: C_P ≥ 5 ∧ mentions ≤ 2
    quadrant = patches.Rectangle(
        (DISSOCIATION_C_P_FLOOR - 0.5, -0.5),
        (6 + 0.5) - (DISSOCIATION_C_P_FLOOR - 0.5),
        DISSOCIATION_MENTION_CEILING + 0.5 - (-0.5),
        linewidth=0, facecolor="#FFE9C8", alpha=0.65, zorder=0,
    )
    ax.add_patch(quadrant)
    ax.text(
        5.95, DISSOCIATION_MENTION_CEILING - 0.05,
        "Iwachu-pattern\ndissociation quadrant",
        fontsize=7, color="#996633", ha="right", va="top",
        style="italic",
    )

    # Brand points colored by cell
    for cell_name in CELL_DISPLAY_ORDER:
        color = CELL_COLORS[cell_name]
        a_cell = phase_a["cells"][cell_name]
        b_cell = phase_b["cells"][cell_name]
        b_lookup = {r["brand"]: r["mention_count"] for r in b_cell["per_brand"]}
        xs, ys = [], []
        for a_rec in a_cell["per_brand"]:
            brand = a_rec["brand"]
            if brand in b_lookup:
                xs.append(a_rec["c_p_score"])
                ys.append(b_lookup[brand])
        ax.scatter(
            xs, ys,
            color=color, s=44, alpha=0.85,
            edgecolors="white", linewidths=0.7,
            label=cell_name.replace("cell_", "Cell ").replace("_", " ").title(),
            zorder=2,
        )

    # Iwachu reference annotation (v0.17 anchor: C_P=6, mentions=0)
    ax.scatter(
        [6], [0], marker="x", s=80, color="#444444", linewidth=1.4, zorder=3,
    )
    ax.text(
        5.85, 0.3, "Iwachu (v0.17)",
        fontsize=7, color="#444444", ha="right", va="bottom", style="italic",
    )

    ax.set_xlabel("Phase A C_P score (Recognition, max 6)")
    ax.set_ylabel("Phase B mention count (Recall, max 18)")
    ax.set_xlim(-0.3, 6.3)
    ax.set_ylim(-0.5, 18.5)
    ax.set_xticks(range(7))
    ax.set_yticks([0, 2, 6, 12, 18])
    ax.legend(loc="upper left", fontsize=7)

    apply_chrome(
        fig, ax,
        title="Recognition × Recall dissociation scatter — v0.18 panel",
        subtitle=(
            "Shaded quadrant: Iwachu-pattern (C_P ≥ 5 ∧ mentions ≤ 2). "
            "Black × = v0.17 Iwachu reference point."
        ),
    )
    fig.tight_layout(rect=[0, 0.04, 1, 0.91])
    fig.savefig(output_path, format="pdf", bbox_inches="tight")
    plt.close(fig)


# ============================================================
# Main
# ============================================================

def main():
    phase_a_path = Path(f"data/phase_a/{PHASE}/phase_a_results.json")
    phase_b_path = Path(f"data/phase_b/{PHASE}/phase_b_results.json")

    phase_a = load_json_required(phase_a_path, "Phase A results")
    phase_b = load_json_required(phase_b_path, "Phase B results")

    out_dir = Path("reports/figs/v18")
    out_dir.mkdir(parents=True, exist_ok=True)

    chart_mention_rate_distribution(
        phase_b, out_dir / "chart_01_mention_rate_distribution.pdf"
    )
    print(f"✓ chart_01_mention_rate_distribution.pdf")

    chart_cell_attrition(
        phase_a, phase_b, out_dir / "chart_02_cell_attrition.pdf"
    )
    print(f"✓ chart_02_cell_attrition.pdf")

    chart_dissociation_scatter(
        phase_a, phase_b, out_dir / "chart_03_dissociation_scatter.pdf"
    )
    print(f"✓ chart_03_dissociation_scatter.pdf")

    print(f"\nAll figures written to {out_dir}/")
    print("Next: build_report_v18.py (two-pass ReportLab overlay)")


if __name__ == "__main__":
    main()
