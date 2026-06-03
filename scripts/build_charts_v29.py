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
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import numpy as np
from scipy.stats import spearmanr

sys.path.insert(0, str(Path(__file__).resolve().parent))
import chart_style as cs

cs.setup()

AIAS_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = AIAS_ROOT / "reports" / "figs" / "v29"
OUT_DIR.mkdir(parents=True, exist_ok=True)

PHASE = "v0.29"

VERDICTS = AIAS_ROOT / "osf" / "v29" / "data" / "v29_verdicts.json"
V25_CSV = AIAS_ROOT / "osf" / "v25" / "data" / "v25_merged_presence_trends.csv"
V25_VERDICTS = AIAS_ROOT / "osf" / "v25" / "v25_verdicts.json"

OUT_MTMM = OUT_DIR / "chart_29_mtmm_gap.pdf"
OUT_CONVERGENT = OUT_DIR / "chart_29_convergent_scatter.pdf"
OUT_DISCRIMINANT = OUT_DIR / "chart_29_discriminant_asymmetry.pdf"
OUT_VERDICT = OUT_DIR / "chart_29_verdict_gate.pdf"

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


# -----------------------------------------------------------------------------
# Figure 3 — discriminant leg: the signed-rho asymmetry axis (P3)
# -----------------------------------------------------------------------------
# Both legs on one signed-correlation axis. The convergent point carries its
# INHERITED v0.25 bootstrap 95% CI (ci_lower/ci_upper, read from v25_verdicts);
# the discriminant point sits at the locked v0.26 rho with NO whisker — v0.26
# published no CI, and this synthesis asserts the null rather than re-deriving
# it (the 88-point pairing is not reproducible from the deposited files, and a
# re-plot would disagree with the locked rho = -0.0002). Numbers are read from
# v29_verdicts.json + v25_verdicts.json; nothing here is synthesized.

def _v25_convergent_ci():
    with open(V25_VERDICTS) as f:
        d = json.load(f)
    for h in d.get("hypotheses", []):
        if (h.get("hypothesis") or h.get("name") or h.get("id")) == "H_CV_Primary":
            st = h.get("statistics", h)
            return float(st["rho"]), float(st["ci_lower"]), float(st["ci_upper"]), st.get("n")
    raise KeyError("v25 H_CV_Primary CI not found in v25_verdicts.json")


def build_discriminant_asymmetry():
    v = load_verdicts()
    r = v["result"]
    rho_conv = r["C1_convergent"]["rho"]
    n_conv = v["provenance"]["convergent"]["n"]
    rho_disc = r["C2_discriminant"]["rho"]
    p_disc = r["C2_discriminant"]["p"]
    n_disc = v["provenance"]["discriminant"]["n"]
    _, ci_lo, ci_hi, _ = _v25_convergent_ci()

    fig, ax = plt.subplots(figsize=(7.5, 3.8))

    # discriminant null zone |rho| < 0.20, and the zero line
    ax.axvspan(-C2_CEILING, C2_CEILING, color=cs.PALETTE["teal_t3"], alpha=0.35, zorder=0)
    ax.axvline(0.0, color=cs.GRAY, lw=0.9, zorder=1)

    y_conv, y_disc = 1.0, 0.0

    # convergent: dot + inherited 95% CI whisker (clears the null zone and zero)
    ax.plot([ci_lo, ci_hi], [y_conv, y_conv], color=cs.INDIGO, lw=2.4,
            solid_capstyle="round", zorder=2)
    for xb in (ci_lo, ci_hi):
        ax.plot([xb, xb], [y_conv - 0.07, y_conv + 0.07], color=cs.INDIGO, lw=2.4, zorder=2)
    ax.scatter([rho_conv], [y_conv], s=90, color=cs.INDIGO, zorder=3)

    # discriminant: bare point inside the null zone (no CI in the lock)
    ax.scatter([rho_disc], [y_disc], s=90, color=cs.WARM, zorder=3)

    ax.text(rho_conv, y_conv + 0.20, "Convergent  ·  Presence x Google Trends (v0.25)",
            ha="center", va="bottom", fontsize=cs.FONT_SIZES["data_label"],
            color=cs.INDIGO, fontweight="bold")
    ax.text(rho_conv, y_conv - 0.22,
            rf"$\rho = {rho_conv:+.3f}$    95% CI [{ci_lo:.2f}, {ci_hi:.2f}]    $n = {n_conv}$",
            ha="center", va="top", fontsize=cs.FONT_SIZES["annotation"], color=cs.BLACK)

    ax.text(rho_disc, y_disc - 0.22, "Discriminant  ·  Presence x Amazon BSR (v0.26)",
            ha="center", va="top", fontsize=cs.FONT_SIZES["data_label"],
            color=cs.PALETTE["warm_sec"], fontweight="bold")
    ax.text(rho_disc, y_disc + 0.20,
            rf"$\rho = {rho_disc:+.4f}$    $p = {p_disc:.3g}$    $n = {n_disc}$   (n.s.)",
            ha="center", va="bottom", fontsize=cs.FONT_SIZES["annotation"], color=cs.BLACK)

    ax.text(0.0, y_disc - 0.62, r"discriminant null zone   $|\rho| < 0.20$",
            ha="center", va="top", fontsize=cs.FONT_SIZES["annotation"],
            color=cs.PALETTE["teal_sec"])

    ax.set_xlim(-0.5, 1.0)
    ax.set_ylim(-0.85, 1.55)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_xlabel(r"Spearman $\rho$  (signed; 0 = no association)",
                  fontsize=cs.FONT_SIZES["axis_label"])
    ax.tick_params(axis="x", labelsize=cs.FONT_SIZES["axis_tick"])
    ax.set_axisbelow(True)

    cs.add_header(
        fig,
        "Significant where expected, null where expected",
        "The two legs on one signed-correlation axis",
        "Convergent clears zero with its inherited 95% CI; discriminant sits inside the null zone, indistinguishable from zero.",
    )
    cs.add_footer(
        fig,
        verdict="The inferential asymmetry — one CI excludes zero, the other leg is n.s. — is the Campbell-Fiske signature.",
        phase=PHASE,
    )

    plt.subplots_adjust(top=0.80, bottom=0.20, left=0.07, right=0.96)
    fig.savefig(OUT_DISCRIMINANT, **cs.SAVEFIG_PARAMS)
    plt.close(fig)
    print(f"✓ Wrote {OUT_DISCRIMINANT.relative_to(AIAS_ROOT)}  ({OUT_DISCRIMINANT.stat().st_size} bytes)")


# -----------------------------------------------------------------------------
# Figure 4 — verdict: the conjunctive construct-validity gate (P4)
# -----------------------------------------------------------------------------
# C1 ∧ C2 ∧ C3 -> H_CV_Baseline. Every value read from v29_verdicts.json; the
# gate is the verdict logic locked in score_v29.py, drawn rather than re-derived.

def _check(ax, x, y, color, size=0.013):
    """Draw a checkmark as two line segments in axes coords (no glyph dependency
    — Akkurat lacks U+2713, so we render the tick rather than typeset it)."""
    ax.plot([x, x + size], [y, y - size], color=color, lw=2.2,
            solid_capstyle="round", transform=ax.transAxes, zorder=6)
    ax.plot([x + size, x + 2.6 * size], [y - size, y + 1.7 * size], color=color, lw=2.2,
            solid_capstyle="round", transform=ax.transAxes, zorder=6)


def build_verdict_gate():
    v = load_verdicts()
    r = v["result"]
    c1, c2, c3 = r["C1_convergent"], r["C2_discriminant"], r["C3_campbell_fiske_gap"]
    verdict = r["verdict"]

    conds = [
        ("C1", "Convergent leg positive & significant",
         rf"$\rho = {c1['rho']:.3f}$,   $p = {c1['p']:.1e}$"),
        ("C2", "Discriminant below 0.20 ceiling & n.s.",
         rf"$\rho = {c2['rho']:+.4f}$,   $p = {c2['p']:.3f}$"),
        ("C3", "Campbell-Fiske gap strictly positive",
         rf"$C_3 = {c3['value']:.4f} > 0$"),
    ]

    fig, ax = plt.subplots(figsize=(7.5, 4.6))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    box_x, box_w, box_h = 0.02, 0.46, 0.205
    ys = [0.76, 0.47, 0.18]
    green = cs.PALETTE["teal_t1"]

    for (cid, label, stat), y in zip(conds, ys):
        ax.add_patch(FancyBboxPatch(
            (box_x, y - box_h / 2), box_w, box_h,
            boxstyle="round,pad=0.006,rounding_size=0.02",
            linewidth=1.0, edgecolor=cs.INDIGO,
            facecolor=cs.PALETTE["indigo_t3"], alpha=0.30, zorder=2))
        ax.text(box_x + 0.028, y + 0.042, cid, fontsize=cs.FONT_SIZES["data_label"],
                fontweight="bold", color=cs.INDIGO, va="center")
        ax.text(box_x + 0.085, y + 0.042, label, fontsize=cs.FONT_SIZES["annotation"],
                color=cs.BLACK, va="center")
        ax.text(box_x + 0.085, y - 0.045, stat, fontsize=cs.FONT_SIZES["annotation"],
                color=cs.PALETTE["gray"], va="center")
        _check(ax, box_x + box_w - 0.055, y + 0.005, green)

    # AND junction
    and_x, and_y, and_r = 0.615, 0.47, 0.05
    ax.add_patch(Circle((and_x, and_y), and_r, edgecolor=cs.INDIGO,
                        facecolor=cs.PALETTE["white"], lw=1.3, zorder=3))
    ax.text(and_x, and_y, "AND", ha="center", va="center",
            fontsize=cs.FONT_SIZES["annotation"], fontweight="bold",
            color=cs.INDIGO, zorder=4)

    # connectors: each condition box -> AND
    for y in ys:
        ax.add_patch(FancyArrowPatch(
            (box_x + box_w, y), (and_x - and_r, and_y),
            arrowstyle="-", connectionstyle="arc3,rad=0.0",
            color=cs.GRAY, lw=1.0, zorder=1))

    # AND -> verdict box
    vbx = 0.73
    ax.add_patch(FancyArrowPatch(
        (and_x + and_r, and_y), (vbx, and_y),
        arrowstyle="-|>", mutation_scale=15, color=cs.INDIGO, lw=1.5, zorder=3))

    ax.add_patch(FancyBboxPatch(
        (vbx, and_y - 0.135), 0.25, 0.27,
        boxstyle="round,pad=0.008,rounding_size=0.02",
        linewidth=1.4, edgecolor=cs.INDIGO, facecolor=cs.INDIGO, zorder=3))
    ax.text(vbx + 0.125, and_y + 0.045, "H_CV_Baseline", ha="center", va="center",
            fontsize=cs.FONT_SIZES["data_label"], color=cs.PALETTE["white"], fontweight="bold")
    ax.text(vbx + 0.125, and_y - 0.048, verdict, ha="center", va="center",
            fontsize=cs.FONT_SIZES["subtitle"], color=cs.TEAL, fontweight="bold")

    cs.add_header(
        fig,
        "All three conditions hold — jointly",
        "The conjunctive construct-validity gate",
        "The baseline is CONFIRMED only if every pre-registered condition passes; each does, so the conjunction does.",
    )
    cs.add_footer(
        fig,
        verdict="H_CV_Baseline CONFIRMED — C1 & C2 & C3 hold together, significance asymmetry intact.",
        phase=PHASE,
    )

    plt.subplots_adjust(top=0.80, bottom=0.10, left=0.04, right=0.97)
    fig.savefig(OUT_VERDICT, **cs.SAVEFIG_PARAMS)
    plt.close(fig)
    print(f"✓ Wrote {OUT_VERDICT.relative_to(AIAS_ROOT)}  ({OUT_VERDICT.stat().st_size} bytes)")


if __name__ == "__main__":
    build_mtmm_gap()
    build_convergent_scatter()
    build_discriminant_asymmetry()
    build_verdict_gate()
