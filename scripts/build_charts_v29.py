#!/usr/bin/env python3
"""
v0.29 (CV.05) chart builder — synthesis figures for the Campbell-Fiske baseline
===============================================================================

CV.05 is a SYNTHESIS phase: no acquisition, no per-brand v0.29 data. The figures
assemble the inherited verdicts (osf/v29/v29_verdicts.json) and the one component
per-point dataset that exists as-is (v0.25's merged convergent CSV). The v0.26
discriminant side is drawn from its INHERITED summary statistic (rho, p, n) — the
synthesis asserts the component's locked result, it does not re-merge and re-plot
v0.26's 88 points (that analysis belongs to v0.26, not v0.29).

Figures (written to reports/figs/v29/):
  chart_29_mtmm_gap.pdf
      The 2x2 MTMM read as a gap: |rho_convergent| and |rho_discriminant| against
      the three decision bands, with the Campbell-Fiske gap C3 annotated. The one
      genuinely new visual; sourced entirely from v29_verdicts.json.
  chart_29_convergent_scatter.pdf
      v0.25 B2B SaaS — AIAS Presence (v1.5 composite, 0-100) x Google Trends, the
      convergent monotrait-heteromethod cell (rho = 0.741). Per-point from the
      real merged CSV. The discriminant cell (rho = -0.0002, n = 88) is annotated
      as the inherited contrast, not re-plotted.

Sources:
  osf/v29/v29_verdicts.json                       (all headline numbers; lock v0.29-prereg-r1)
  osf/v25/data/v25_merged_presence_trends.csv     (v0.25 convergent per-point)
"""

from pathlib import Path
import csv
import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import spearmanr

sys.path.insert(0, str(Path(__file__).resolve().parent))
import chart_style as cs

cs.setup()

AIAS_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = AIAS_ROOT / "reports" / "figs" / "v29"
OUT_DIR.mkdir(parents=True, exist_ok=True)

PHASE = "v0.29"

VERDICTS = AIAS_ROOT / "osf" / "v29" / "v29_verdicts.json"
V25_CSV = AIAS_ROOT / "osf" / "v25" / "data" / "v25_merged_presence_trends.csv"

OUT_MTMM = OUT_DIR / "chart_29_mtmm_gap.pdf"
OUT_CONVERGENT = OUT_DIR / "chart_29_convergent_scatter.pdf"

# locked decision bands (mirror prereg/v0_29_cv_baseline_content.py)
C2_CEILING = 0.20          # |rho_disc| must be below this
CONVERGENT_FLOOR = 0.50    # convergent should clear this to be a real monotrait cell


def load_verdicts() -> dict:
    with open(VERDICTS) as f:
        return json.load(f)


# -----------------------------------------------------------------------------
# Figure 1 — MTMM gap: |rho| against bands, C3 annotated
# -----------------------------------------------------------------------------

def build_mtmm_gap():
    v = load_verdicts()
    r = v["result"]
    rho_conv = r["C1_convergent"]["rho"]
    rho_disc = r["C2_discriminant"]["rho"]
    c3 = r["C3_campbell_fiske_gap"]["value"]
    verdict = r["verdict"]

    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero_short"])

    rows = [
        ("Convergent\nPresence x Trends (v0.25)", abs(rho_conv), cs.INDIGO, rho_conv,
         r["C1_convergent"]["p"], v["provenance"]["convergent"]["n"]),
        ("Discriminant\nPresence x BSR (v0.26)", abs(rho_disc), cs.WARM, rho_disc,
         r["C2_discriminant"]["p"], v["provenance"]["discriminant"]["n"]),
    ]
    y = np.arange(len(rows))[::-1]   # convergent on top

    # shaded band regions (discriminant ceiling / convergent floor)
    ax.axvspan(0.0, C2_CEILING, color=cs.PALETTE["teal_t3"], alpha=0.35, zorder=0)
    ax.axvline(C2_CEILING, color=cs.GRAY, lw=0.8, ls="--", zorder=1)
    ax.axvline(CONVERGENT_FLOOR, color=cs.GRAY, lw=0.8, ls=":", zorder=1)

    for yi, (label, arho, color, srho, p, n) in zip(y, rows):
        ax.barh(yi, arho, color=color, alpha=0.88, height=0.46, edgecolor="none", zorder=2)
        ax.text(arho + 0.015, yi,
                rf"$\rho = {srho:+.3f}$   $p = {p:.3g}$   $n = {n}$",
                va="center", ha="left",
                fontsize=cs.FONT_SIZES["annotation"], color=cs.BLACK, zorder=3)

    ax.set_yticks(y)
    ax.set_yticklabels([row[0] for row in rows], fontsize=cs.FONT_SIZES["data_label"])
    ax.set_xlim(0, 1.0)
    ax.set_xlabel(r"$|\rho|$  (absolute Spearman coefficient)",
                  fontsize=cs.FONT_SIZES["axis_label"])
    ax.tick_params(axis="both", labelsize=cs.FONT_SIZES["axis_tick"])
    ax.set_axisbelow(True)

    # band labels
    ax.text(C2_CEILING / 2, max(y) + 0.55, "discriminant\nceiling (0.20)",
            ha="center", va="bottom", fontsize=cs.FONT_SIZES["annotation"],
            color=cs.PALETTE["teal_sec"])
    ax.text(CONVERGENT_FLOOR + 0.02, max(y) + 0.55, "convergent floor (0.50)",
            ha="left", va="bottom", fontsize=cs.FONT_SIZES["annotation"], color=cs.GRAY)

    # C3 gap annotation
    ax.text(0.5, min(y) - 0.62,
            rf"Campbell-Fiske gap  $C_3 = |\rho_{{conv}}| - |\rho_{{disc}}| = {c3:.4f}$",
            ha="center", va="top", fontsize=cs.FONT_SIZES["data_label"],
            color=cs.INDIGO, fontweight="bold")

    ax.set_ylim(min(y) - 0.9, max(y) + 1.0)

    cs.add_header(
        fig,
        "Presence clears the construct-validity baseline",
        "The 2x2 MTMM read as a gap: strong convergent, near-zero discriminant",
        "Inherited Spearman coefficients; the gap between them is the Campbell-Fiske evidence.",
    )
    cs.add_footer(
        fig,
        verdict=rf"$\mathrm{{H_{{CV\_Baseline}}}}$ {verdict} — $C_3 = {c3:.4f} > 0$, significance asymmetry intact.",
        phase=PHASE,
    )

    plt.subplots_adjust(top=0.80, bottom=0.20, left=0.22, right=0.97)
    fig.savefig(OUT_MTMM, **cs.SAVEFIG_PARAMS)
    plt.close(fig)
    print(f"✓ Wrote {OUT_MTMM.relative_to(AIAS_ROOT)}  ({OUT_MTMM.stat().st_size} bytes)")


# -----------------------------------------------------------------------------
# Figure 2 — convergent scatter (v0.25), discriminant as inherited annotation
# -----------------------------------------------------------------------------

def load_v25_points():
    pts = []
    with open(V25_CSV) as f:
        for row in csv.DictReader(f):
            try:
                pts.append((row["brand"],
                            float(row["presence_composite"]),
                            float(row["trends_normalized"])))
            except (ValueError, KeyError):
                continue
    return pts


def build_convergent_scatter():
    v = load_verdicts()
    r = v["result"]
    rho_disc = r["C2_discriminant"]["rho"]
    p_disc = r["C2_discriminant"]["p"]
    n_disc = v["provenance"]["discriminant"]["n"]

    pts = load_v25_points()
    presence = np.array([d[1] for d in pts], dtype=float)
    trends = np.array([d[2] for d in pts], dtype=float)
    rho, p = spearmanr(presence, trends)

    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])

    ax.scatter(presence, trends, s=26, color=cs.INDIGO, alpha=0.80, edgecolors="none")
    ax.set_xlim(0, 100)
    ax.set_xlabel("AIAS Presence (v1.5 composite, 0–100)", fontsize=cs.FONT_SIZES["axis_label"])
    ax.set_ylabel("Google Trends search interest", fontsize=cs.FONT_SIZES["axis_label"])
    ax.tick_params(axis="both", labelsize=cs.FONT_SIZES["axis_tick"])
    ax.grid(True, which="major", linestyle=":", linewidth=0.5,
            color=cs.PALETTE["gray_light"], alpha=0.7)
    ax.set_axisbelow(True)

    # convergent stat box
    ax.text(0.05, 0.97,
            rf"Convergent (v0.25)" "\n"
            rf"$\rho = {rho:+.3f}$" "\n" rf"$p = {p:.2g}$" "\n" rf"$n = {len(presence)}$",
            transform=ax.transAxes, ha="left", va="top",
            fontsize=cs.FONT_SIZES["annotation"], color=cs.BLACK,
            bbox=dict(facecolor="white", edgecolor=cs.PALETTE["gray_light"],
                      boxstyle="round,pad=0.35", linewidth=0.5))

    # discriminant inherited-contrast box (NOT re-plotted; the synthesis asserts it)
    ax.text(0.97, 0.05,
            rf"Discriminant contrast (v0.26, inherited)" "\n"
            rf"Presence x Amazon BSR:  $\rho = {rho_disc:+.4f}$" "\n"
            rf"$p = {p_disc:.3g}$,  $n = {n_disc}$  — near-zero, n.s.",
            transform=ax.transAxes, ha="right", va="bottom",
            fontsize=cs.FONT_SIZES["annotation"], color=cs.WARM_SEC if hasattr(cs, "WARM_SEC") else cs.PALETTE["warm_sec"],
            bbox=dict(facecolor=cs.PALETTE["paper"], edgecolor=cs.PALETTE["warm_t2"],
                      boxstyle="round,pad=0.35", linewidth=0.6))

    cs.add_header(
        fig,
        "The convergent cell: Presence tracks search interest",
        "v0.25 B2B SaaS — AIAS Presence x Google Trends",
        "Per-point convergent data (left box). The discriminant cell is the inherited v0.26 contrast (lower right), asserted not re-plotted.",
    )
    cs.add_footer(
        fig,
        verdict="The two cells together are the Campbell-Fiske evidence: high convergent, near-zero discriminant.",
        phase=PHASE,
    )

    # bottom=0.18 (not 0.12): leaves clearance between the x-axis label and the
    # footer verdict line, which collided at 0.12.
    plt.subplots_adjust(top=0.82, bottom=0.18, left=0.10, right=0.96)
    fig.savefig(OUT_CONVERGENT, **cs.SAVEFIG_PARAMS)
    plt.close(fig)
    print(f"✓ Wrote {OUT_CONVERGENT.relative_to(AIAS_ROOT)}  ({OUT_CONVERGENT.stat().st_size} bytes)")


if __name__ == "__main__":
    build_mtmm_gap()
    build_convergent_scatter()
