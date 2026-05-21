"""
build_charts_v19.py — v0.19 Chart Pipeline

Produces three matplotlib PDFs at locked figsize for the v0.19 brand-format
report and SSRN paper figures. Substrate: audiophile headphones, two-cell
Heritage × Boutique design with uniform Identity Load tier across cells
(split by audiophile headphone product-line emergence year, threshold 2008).

Inputs:
  - osf/v19/panel_registry_v0_19.csv     (locked 16-brand panel)
  - osf/v19/phase_a_results.csv          (96 rows, post-acquisition)
  - osf/v19/phase_b_results.csv          (576 rows, post-acquisition)

Outputs:
  - reports/figs/v19/chart_01_cp_distribution.pdf
  - reports/figs/v19/chart_02_dissociation_scatter.pdf
  - reports/figs/v19/chart_03_channel_asymmetry.pdf

Pre-reg lock:    v0.19-prereg-r1 @ commit 2cbd36c
Branch:          v0.18-il-gradient (working trunk)
Predecessor:     scripts/build_charts_v18.py (Indie Fragrance)

Story-shape changes from v0.18:
  - Two cells (Heritage / Boutique), not three. No IL-gradient ordering —
    cells are same-IL, split by audiophile headphone product-line emergence
    year (Heritage: pre-2008; Boutique: post-2008).
  - Chart 1 replaces v0.18's mention-rate-distribution with a C_P
    distribution chart. v0.19's headline is the Recognition ceiling, not
    Recall sparsity. C2 modal share annotated per cell.
  - Chart 2 keeps the dissociation scatter but extends it with cumulative
    anchor-base reference markers: v0.17 Iwachu (single ×) and v0.18's
    9 cases (background ghost points), so the v1.4 construct's empirical
    base growth is visible.
  - Chart 3 is new for v0.19. v0.18's cultural-footprint sensitivity
    finding promoted to a load-bearing chart slot. Category-anchored
    Recall vs cultural-footprint Recall scatter with Type 1 and Type 2
    quadrants drawn ex-ante.
"""

import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches


# ============================================================
# Configuration — LOCKED per v0.19-prereg-r1 and brand tokens
# ============================================================

PHASE = "v0.19"

CHART_FIGSIZE = (7.5, 5.5)
CHART_DPI = 300

SOURCE_LINE = (
    "Source: AIAS\u2122 Presence Measurement Protocol v1.4 (SSRN 6799479) \u00b7 "
    "v0.19-prereg-r1 \u00b7 osf.io/ec6wh/v19/"
)
ATTRIBUTION_LINE = "Third\u00a0System\u2122  \u00b7  thirdsystem.ai"

# Brand colors — indigo family
# Same-IL cells; family-internal differentiation (Boutique = primary, where
# the action is; Heritage = mid-indigo as comparison)
INDIGO_PRIMARY = "#37237B"
PETRO          = "#6A6AB1"
LAVENDER_GREY  = "#BBB9DD"
GHOST_GREY     = "#BFBFBF"

CELL_COLORS = {
    "A_Heritage":  PETRO,
    "B_Boutique":  INDIGO_PRIMARY,
}
CELL_LABELS = {
    "A_Heritage":  "Cell A\nHeritage\n(pre-2008 audiophile)",
    "B_Boutique":  "Cell B\nBoutique\n(post-2008 audiophile)",
}
CELL_DISPLAY_ORDER = ["A_Heritage", "B_Boutique"]

# Decision rule thresholds (locked at v0.19-prereg-r1)
C1_PANEL_FLOOR = 12
C2_MODAL_SHARE_MAX = 0.50
DISSOCIATION_C_P_FLOOR = 5
DISSOCIATION_MENTION_CEILING = 2
TYPE1_CATEGORY_FLOOR = 5
TYPE1_CULTURAL_CEILING = 2
TYPE2_CATEGORY_CEILING = 2
TYPE2_CULTURAL_FLOOR = 5

# Phase B frame routing (matches thresholds_v0_19.json)
LOAD_BEARING_FRAMES = {"q1_audiophile", "q2_enthusiast", "q3_reference"}
SENSITIVITY_FRAMES = {"q4_famous", "q5_popular", "q6_iconic"}

# Cumulative anchor base for chart 2 background reference
V017_IWACHU = {"brand": "Iwachu", "c_p": 6, "mentions": 0}
V018_IWACHU_CASES = [
    {"brand": "Comme des Garcons Parfums", "c_p": 5, "mentions": 2},
    {"brand": "Memo Paris",                "c_p": 6, "mentions": 0},
    {"brand": "Etat Libre d'Orange",       "c_p": 6, "mentions": 1},
    {"brand": "D.S. & Durga",              "c_p": 6, "mentions": 2},
    {"brand": "Boy Smells",                "c_p": 5, "mentions": 0},
    {"brand": "Heretic Parfum",            "c_p": 6, "mentions": 0},
    {"brand": "Vyrao",                     "c_p": 6, "mentions": 0},
    {"brand": "Phlur",                     "c_p": 5, "mentions": 0},
    {"brand": "Snif",                      "c_p": 5, "mentions": 0},
]


# Matplotlib base style — matches v0.18 conventions
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
    """Bold title at top, italic subtitle below, source/attribution at bottom."""
    ax.set_title("")
    fig.suptitle(title, fontsize=11, fontweight="bold", y=0.96, ha="center")
    fig.text(0.5, 0.90, subtitle,
             fontsize=9, style="italic", color="#444444",
             ha="center", va="top")
    fig.text(0.02, 0.012, SOURCE_LINE,
             fontsize=6.5, color="#666666", ha="left")
    fig.text(0.98, 0.012, ATTRIBUTION_LINE,
             fontsize=6.5, color="#666666", ha="right")


# ============================================================
# Data loaders — fail-fast on missing inputs
# ============================================================

def load_registry(path: Path):
    brand_to_cell = {}
    cell_to_brands = defaultdict(list)
    with path.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            brand_to_cell[row["brand"]] = row["cell"]
            cell_to_brands[row["cell"]].append(row["brand"])
    return brand_to_cell, dict(cell_to_brands)


def load_phase_a(path: Path):
    cp = defaultdict(int)
    with path.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if int(row["recognition_yes"]) == 1:
                cp[row["brand"]] += 1
    return dict(cp)


def load_phase_b(path: Path):
    lb = defaultdict(int)
    sens = defaultdict(int)
    with path.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if int(row["mentioned"]) != 1:
                continue
            if row["frame"] in LOAD_BEARING_FRAMES:
                lb[row["brand"]] += 1
            elif row["frame"] in SENSITIVITY_FRAMES:
                sens[row["brand"]] += 1
    return dict(lb), dict(sens)


def require_path(path: Path, what: str) -> None:
    if not path.exists():
        print(
            f"\n\u2717 Missing input: {what} expected at {path}\n"
            f"  Run upstream pipeline first:\n"
            f"    1. python3 run_v0_19.py phase-a\n"
            f"    2. python3 run_v0_19.py phase-b\n"
            f"    3. python3 acquire_v0_19.py parse-phase-a phase_a_responses.jsonl\n"
            f"    4. python3 acquire_v0_19.py parse-phase-b phase_b_responses.jsonl\n",
            file=sys.stderr,
        )
        sys.exit(1)


# ============================================================
# Chart 1 — C_P distribution per cell (Recognition)
# ============================================================

def chart_cp_distribution(brand_to_cell, cell_to_brands, cp, output_path):
    fig, ax = plt.subplots(figsize=CHART_FIGSIZE, dpi=CHART_DPI)

    for x_pos, cell_name in enumerate(CELL_DISPLAY_ORDER):
        brands_in_cell = cell_to_brands.get(cell_name, [])
        scores = [cp.get(b, 0) for b in brands_in_cell]
        color = CELL_COLORS[cell_name]
        n = len(scores)

        ax.scatter(
            [x_pos + (i - n / 2) * 0.045 for i in range(n)],
            scores,
            color=color, s=80, alpha=0.88,
            edgecolors="white", linewidths=0.9,
        )

        if scores:
            counts = Counter(scores)
            modal_value, modal_count = counts.most_common(1)[0]
            modal_share = modal_count / n
            verdict = "PASS" if modal_share < C2_MODAL_SHARE_MAX else "FAIL"
            verdict_color = "#1B6E3F" if verdict == "PASS" else "#A02828"
            ax.text(x_pos, -1.3,
                    f"C_P modal share = {modal_share:.3f}",
                    fontsize=8.5, color="#444444", ha="center", va="top")
            ax.text(x_pos, -2.05,
                    f"C2: {verdict}",
                    fontsize=9, fontweight="bold", color=verdict_color,
                    ha="center", va="top")

    ax.axhline(6, color="#999999", linestyle=":", linewidth=0.6, alpha=0.5)
    ax.text(len(CELL_DISPLAY_ORDER) - 0.5, 6.18,
            "C_P ceiling (6/6)",
            fontsize=7, color="#666666", ha="right", va="bottom")

    ax.set_xticks(range(len(CELL_DISPLAY_ORDER)))
    ax.set_xticklabels([CELL_LABELS[c] for c in CELL_DISPLAY_ORDER], fontsize=8)
    ax.set_ylabel("Phase A C_P score (Recognition, max = 6)")
    ax.set_ylim(-2.6, 6.7)
    ax.set_yticks([0, 1, 2, 3, 4, 5, 6])

    apply_chrome(
        fig, ax,
        title="Phase A Recognition (C_P) distribution per cell",
        subtitle=(
            "v0.19 audiophile headphones \u2014 16 brands \u00d7 2 same-IL cells. "
            "C2 fails if C_P modal share \u2265 0.50."
        ),
    )
    fig.tight_layout(rect=[0, 0.055, 1, 0.86])
    fig.savefig(output_path, format="pdf", bbox_inches="tight")
    plt.close(fig)


# ============================================================
# Chart 2 — Dissociation scatter (cumulative across substrates)
# ============================================================

def chart_dissociation_scatter(brand_to_cell, cp, lb_mentions, output_path):
    fig, ax = plt.subplots(figsize=CHART_FIGSIZE, dpi=CHART_DPI)

    quadrant = patches.Rectangle(
        (DISSOCIATION_C_P_FLOOR - 0.5, -0.5),
        (6 + 0.5) - (DISSOCIATION_C_P_FLOOR - 0.5),
        DISSOCIATION_MENTION_CEILING + 0.5 - (-0.5),
        linewidth=0, facecolor="#FFE9C8", alpha=0.65, zorder=0,
    )
    ax.add_patch(quadrant)

    # v0.18 ghost cases (background reference)
    v18_x = [c["c_p"] for c in V018_IWACHU_CASES]
    v18_y = [c["mentions"] for c in V018_IWACHU_CASES]
    ax.scatter(
        v18_x, v18_y,
        color=GHOST_GREY, s=36, alpha=0.65, marker="o",
        edgecolors="white", linewidths=0.5,
        label=f"v0.18 cases (n = {len(V018_IWACHU_CASES)})",
        zorder=1,
    )

    # v0.17 Iwachu reference
    ax.scatter(
        [V017_IWACHU["c_p"]], [V017_IWACHU["mentions"]],
        marker="x", s=90, color="#333333", linewidth=1.7,
        label="v0.17 Iwachu",
        zorder=3,
    )

    # v0.19 brands by cell
    for cell_name in CELL_DISPLAY_ORDER:
        color = CELL_COLORS[cell_name]
        xs, ys = [], []
        for brand, c in brand_to_cell.items():
            if c == cell_name:
                xs.append(cp.get(brand, 0))
                ys.append(lb_mentions.get(brand, 0))
        ax.scatter(
            xs, ys,
            color=color, s=64, alpha=0.92,
            edgecolors="white", linewidths=0.9,
            label=f"v0.19 {cell_name.replace('_', ' ')} (n = {len(xs)})",
            zorder=2,
        )

    ax.set_xlabel("Phase A C_P score (Recognition, max = 6)")
    ax.set_ylabel("Phase B category-anchored mentions (max = 18)")
    ax.set_xlim(-0.3, 6.3)
    ax.set_ylim(-0.8, 18.5)
    ax.set_xticks(range(7))
    ax.set_yticks([0, 2, 6, 12, 18])
    ax.legend(loc="upper left", fontsize=7)

    apply_chrome(
        fig, ax,
        title="Recognition \u00d7 Recall dissociation \u2014 cumulative anchor base",
        subtitle=(
            "Shaded quadrant: Iwachu-pattern (C_P \u2265 5 AND mentions \u2264 2). "
            "v0.19 contributes 3 cases to a base spanning 3 substrate families."
        ),
    )
    fig.tight_layout(rect=[0, 0.045, 1, 0.86])
    fig.savefig(output_path, format="pdf", bbox_inches="tight")
    plt.close(fig)


# ============================================================
# Chart 3 — Channel asymmetry
# ============================================================

def chart_channel_asymmetry(brand_to_cell, lb_mentions, sens_mentions, output_path):
    fig, ax = plt.subplots(figsize=CHART_FIGSIZE, dpi=CHART_DPI)

    # Type 1 quadrant (lower-right)
    type1_rect = patches.Rectangle(
        (TYPE1_CATEGORY_FLOOR - 0.5, -0.5),
        18.5 - (TYPE1_CATEGORY_FLOOR - 0.5),
        TYPE1_CULTURAL_CEILING + 0.5 - (-0.5),
        linewidth=0, facecolor="#E5DDF5", alpha=0.55, zorder=0,
    )
    ax.add_patch(type1_rect)
    ax.text(13.0, 1.2,
            "Type 1\ncategory-channel-preferred",
            fontsize=8, color="#37237B", ha="center", va="center",
            style="italic", zorder=1)

    # Type 2 quadrant (upper-left)
    type2_rect = patches.Rectangle(
        (-0.5, TYPE2_CULTURAL_FLOOR - 0.5),
        TYPE2_CATEGORY_CEILING + 0.5 - (-0.5),
        18.5 - (TYPE2_CULTURAL_FLOOR - 0.5),
        linewidth=0, facecolor="#FFE9C8", alpha=0.55, zorder=0,
    )
    ax.add_patch(type2_rect)
    ax.text(1.0, 13.0,
            "Type 2\ncultural-channel-preferred\n(0 cases)",
            fontsize=8, color="#888888", ha="center", va="center",
            style="italic", zorder=1)

    for cell_name in CELL_DISPLAY_ORDER:
        color = CELL_COLORS[cell_name]
        xs, ys = [], []
        for brand, c in brand_to_cell.items():
            if c == cell_name:
                xs.append(lb_mentions.get(brand, 0))
                ys.append(sens_mentions.get(brand, 0))
        ax.scatter(
            xs, ys,
            color=color, s=64, alpha=0.92,
            edgecolors="white", linewidths=0.9,
            label=f"v0.19 {cell_name.replace('_', ' ')} (n = {len(xs)})",
            zorder=2,
        )

    ax.set_xlabel("Category-anchored mentions (q1\u2013q3 \u00d7 6 models, max = 18)")
    ax.set_ylabel("Cultural-footprint mentions (q4\u2013q6 \u00d7 6 models, max = 18)")
    ax.set_xlim(-0.8, 18.5)
    ax.set_ylim(-0.8, 18.5)
    ax.set_xticks([0, 2, 5, 10, 15, 18])
    ax.set_yticks([0, 2, 5, 10, 15, 18])
    ax.legend(loc="upper right", fontsize=7)

    apply_chrome(
        fig, ax,
        title="Channel asymmetry: category-anchored vs cultural-footprint Recall",
        subtitle=(
            "Type 1: 3 v0.19 cases (Audeze, HiFiMan, Dan Clark Audio). "
            "Type 2: 0 cases \u2014 panel composition limit, not absent pathway."
        ),
    )
    fig.tight_layout(rect=[0, 0.045, 1, 0.86])
    fig.savefig(output_path, format="pdf", bbox_inches="tight")
    plt.close(fig)


# ============================================================
# Main
# ============================================================

def main():
    base_dir = Path("osf/v19")
    registry_path = base_dir / "panel_registry_v0_19.csv"
    phase_a_path  = base_dir / "phase_a_results.csv"
    phase_b_path  = base_dir / "phase_b_results.csv"

    require_path(registry_path, "panel registry")
    require_path(phase_a_path,  "Phase A results")
    require_path(phase_b_path,  "Phase B results")

    brand_to_cell, cell_to_brands = load_registry(registry_path)
    cp = load_phase_a(phase_a_path)
    lb, sens = load_phase_b(phase_b_path)

    out_dir = Path("reports/figs/v19")
    out_dir.mkdir(parents=True, exist_ok=True)

    chart_cp_distribution(
        brand_to_cell, cell_to_brands, cp,
        out_dir / "chart_01_cp_distribution.pdf",
    )
    print("\u2713 chart_01_cp_distribution.pdf")

    chart_dissociation_scatter(
        brand_to_cell, cp, lb,
        out_dir / "chart_02_dissociation_scatter.pdf",
    )
    print("\u2713 chart_02_dissociation_scatter.pdf")

    chart_channel_asymmetry(
        brand_to_cell, lb, sens,
        out_dir / "chart_03_channel_asymmetry.pdf",
    )
    print("\u2713 chart_03_channel_asymmetry.pdf")

    print(f"\nAll figures written to {out_dir}/")
    print("Next: build_report_v19.py (two-pass ReportLab overlay)")


if __name__ == "__main__":
    main()
