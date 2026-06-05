#!/usr/bin/env python3
"""
v0.32 CPC Version-Snapshot Stability — figure builder (one per finding).

Reads osf/v32/v32_verdicts.json. Each figure carries its qualification visually:
  fig_01 PRIMARY   — CPC_A x CPC_B scatter, y=x, rho + LOO-triplet inset.
  fig_02 SECONDARY — signed dCPC per brand (diverging), 0.5*SD tolerance band.
  fig_03 TERTIARY  — top: flip table honest zero; bottom: EXPLORATORY emerging
                     recall A vs B with the floor line (rise that didn't cross),
                     visually demarcated so it can't read as confirmatory.

Outputs reports/figs/v32/chart_0{1,2,3}.pdf (canonical) + .png (pre-flight view).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

sys.path.insert(0, str(Path(__file__).parent))
from chart_style import (setup, add_header, add_footer, PALETTE, FIGSIZE,
                         SAVEFIG_PARAMS, cell_colors, INDIGO, WARM, GRAY, BLACK)

ROOT = Path.home() / "aias"
V = json.load(open(ROOT / "osf" / "v32" / "v32_verdicts.json"))
OUTD = ROOT / "reports" / "figs" / "v32"
OUTD.mkdir(parents=True, exist_ok=True)
CELLC = cell_colors()
CELL_LABEL = {"A": "Heritage", "B": "Disruptor", "C": "Mass-Legacy", "D": "Defunct"}
PHASE = "v0.32"


def save(fig, n):
    pdf, png = OUTD / f"chart_0{n}.pdf", OUTD / f"chart_0{n}.png"
    fig.savefig(pdf, **SAVEFIG_PARAMS)
    fig.savefig(png, **SAVEFIG_PARAMS)
    plt.close(fig)
    print(f"  wrote {pdf.name} + {png.name}")


def pairwise():
    out = []
    for b, d in V["per_brand_cpc"].items():
        if d["cpc_A"] is not None and d["cpc_B"] is not None:
            out.append((b, d["cell"], d["cpc_A"], d["cpc_B"]))
    return out


# --- fig_01: PRIMARY rho scatter + LOO inset -------------------------------
def fig01():
    pw = pairwise()
    p = V["PRIMARY_H_ScoreRankStable"]
    fig, ax = plt.subplots(figsize=FIGSIZE["hero"])
    plt.subplots_adjust(top=0.80, bottom=0.16, left=0.11, right=0.96)
    lo, hi = 0.45, 1.0
    ax.plot([lo, hi], [lo, hi], ls="--", lw=0.9, color=GRAY, zorder=1)
    ax.text(hi - 0.005, hi - 0.02, "y = x", color=GRAY, fontsize=7.5,
            ha="right", va="top", fontstyle="italic")
    seen = set()
    for b, c, a, bb in pw:
        ax.scatter(a, bb, s=46, color=CELLC[c], edgecolor="white", linewidth=0.6,
                   zorder=3, label=(CELL_LABEL[c] if c not in seen else None))
        seen.add(c)
        ax.annotate(b, (a, bb), fontsize=6.2, color=BLACK, xytext=(3, 3),
                    textcoords="offset points")
    ax.set_xlim(lo, hi); ax.set_ylim(lo, hi)
    ax.set_xlabel("CPC — Arm A (older vintage)")
    ax.set_ylabel("CPC — Arm B (current vintage)")
    ax.set_aspect("equal")
    ax.legend(loc="upper left", bbox_to_anchor=(0.02, 0.80), fontsize=7.5, framealpha=0.9)
    # rho annotation
    ax.text(0.03, 0.97, f"Spearman ρ = {p['rho']:.3f}   (n = {p['n_pairwise_complete']} pairwise-complete)\n"
            f"verdict: {p['verdict']} — band: {p['interpretive_band']}",
            transform=ax.transAxes, ha="left", va="top", fontsize=8.5,
            color=INDIGO, bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=INDIGO, lw=0.7))
    # LOO inset — provider dependence
    loo = V["SENSITIVITY_leave_one_provider_out"]
    order = [("drop_openai", "drop OpenAI\n(4o→5.x jump)"), ("drop_anthropic", "drop Anthropic"),
             ("drop_google", "drop Google")]
    iax = fig.add_axes([0.60, 0.205, 0.30, 0.22])
    vals = [loo[k]["rho"] for k, _ in order]
    labs = [lab for _, lab in order]
    cols = [PALETTE["teal"] if v >= 0.70 else WARM for v in vals]
    iax.barh(range(len(vals)), vals, color=cols, height=0.62)
    iax.axvline(0.70, color=BLACK, lw=0.8, ls=":")
    iax.axvline(p["rho"], color=INDIGO, lw=1.0)
    for i, v in enumerate(vals):
        iax.text(v + 0.01, i, f"{v:.2f}", va="center", fontsize=6.5)
    iax.set_yticks(range(len(labs))); iax.set_yticklabels(labs, fontsize=6.2)
    iax.set_xlim(0, 1.0); iax.set_xticks([0, 0.5, 0.7, 1.0]); iax.tick_params(labelsize=6)
    iax.set_title("leave-one-provider-out ρ  (dotted = 0.70)", fontsize=6.5, loc="left")
    add_header(fig, "Rank-order stability across a two-generation model jump",
               "PRIMARY · H_ScoreRankStable — CPC per brand, Arm A vs Arm B",
               "ρ clears 0.70 but the inset shows it is provider-dependent: dropping the OpenAI 4o→5.x jump raises it to 0.82.")
    add_footer(fig, verdict="PRIMARY CONFIRMED at ρ=0.708 — borderline; provider-dependent per leave-one-out.",
               phase=PHASE, protocol="v1.7")
    save(fig, 1)


# --- fig_02: SECONDARY signed dCPC diverging + tolerance band ---------------
def fig02():
    pw = pairwise()
    s = V["SECONDARY_H_ScoreMagnitudeStable"]
    thr = s["threshold_0.5xSD"]
    rows = sorted([(b, c, bb - a) for b, c, a, bb in pw], key=lambda r: r[2])
    fig, ax = plt.subplots(figsize=FIGSIZE["hero_tall"])
    plt.subplots_adjust(top=0.82, bottom=0.14, left=0.20, right=0.96)
    y = range(len(rows))
    ax.axvspan(-thr, thr, color=PALETTE["indigo_t3"], alpha=0.45, zorder=0,
               label=f"tolerance ±0.5·SD = ±{thr:.3f}")
    for i, (b, c, d) in enumerate(rows):
        ax.barh(i, d, color=CELLC[c], height=0.66,
                edgecolor=(WARM if abs(d) > thr else "white"),
                linewidth=(1.1 if abs(d) > thr else 0.5), zorder=2)
    ax.axvline(0, color=BLACK, lw=0.8)
    ax.set_yticks(list(y)); ax.set_yticklabels([b for b, _, _ in rows], fontsize=7.5)
    ax.set_xlabel("signed ΔCPC  (Arm B − Arm A)")
    ax.set_xlim(-0.22, 0.24)
    ax.legend(loc="upper left", fontsize=7.5)
    ax.text(0.98, 0.04,
            f"mean |ΔCPC| = {s['mean_abs_dCPC']:.3f}  >  0.5·SD = {thr:.3f}   → {s['verdict']}\n"
            f"signed mean ΔCPC = {s['mean_signed_dCPC']:+.3f}  (spread exceeds tolerance,\nbut ~centered — no net drift)",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=8.2, color=INDIGO,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=INDIGO, lw=0.7))
    add_header(fig, "Magnitude shift exceeds the instrument's own tolerance",
               "SECONDARY · H_ScoreMagnitudeStable — per-brand signed ΔCPC (sorted)",
               "Bars outside the shaded band exceed half the Arm-A between-brand SD; outlined bars are the over-tolerance brands.")
    add_footer(fig, verdict="SECONDARY FALSIFIED — mean|ΔCPC|=0.077 > 0.069; scattered, near-zero net drift.",
               phase=PHASE, protocol="v1.7")
    save(fig, 2)


# --- fig_03: TERTIARY flip-zero (top) + EXPLORATORY emerging recall (bottom) -
def fig03():
    t = V["TERTIARY_H_EmergingInstability"]
    fig = plt.figure(figsize=FIGSIZE["hero_tall"])
    plt.subplots_adjust(top=0.80, bottom=0.12, left=0.12, right=0.95, hspace=0.55)
    # top — confirmatory: flip rate by cell (all zero)
    axt = fig.add_subplot(2, 1, 1)
    cells = ["A", "B", "C", "D"]
    rates = [t["cell_flip_rate"][c]["flip_rate"] or 0.0 for c in cells]
    nin = [t["cell_flip_rate"][c]["na_in_A"] for c in cells]
    axt.bar(range(4), rates, color=[CELLC[c] for c in cells], width=0.6)
    axt.set_ylim(0, 1.0)
    axt.set_xticks(range(4))
    axt.set_xticklabels([f"{CELL_LABEL[c]}\n(N/A in A: {n})" for c, n in zip(cells, nin)], fontsize=7.5)
    axt.set_ylabel("N/A→defined flip rate")
    for i, r in enumerate(rates):
        axt.text(i, 0.03, "0", ha="center", fontsize=9, color=BLACK, fontweight="bold")
    axt.set_title("Confirmatory test — flip rate by cell: zero everywhere",
                  fontsize=9, loc="left", color=BLACK)
    axt.text(0.99, 0.92, "TERTIARY FALSIFIED — no N/A→defined flips;\nidentical 10-brand N/A set in both arms",
             transform=axt.transAxes, ha="right", va="top", fontsize=7.5, color=WARM)
    # bottom — EXPLORATORY: emerging-brand mean recall A vs B, floor line
    axb = fig.add_subplot(2, 1, 2)
    axb.set_facecolor("#FBF1EC")  # tint to demarcate exploratory
    emerging = ["Rivian", "Lucid", "Polestar", "Fisker"]  # sub-floor Cell-B
    mA, mB = [], []
    for b in emerging:
        d = V["per_brand_cpc"][b]
        mA.append(float(np.mean(d["counts_A"]))); mB.append(float(np.mean(d["counts_B"])))
    x = np.arange(len(emerging)); w = 0.38
    axb.bar(x - w / 2, mA, w, color=PALETTE["gray_light"], label="Arm A (older)")
    axb.bar(x + w / 2, mB, w, color=WARM, label="Arm B (current)")
    axb.axhline(1.0, color=BLACK, lw=1.0, ls="--")
    axb.text(len(emerging) - 0.5, 1.02, "floor (mean = 1.0) → below = CPC N/A",
             ha="right", va="bottom", fontsize=7, color=BLACK)
    axb.set_xticks(x); axb.set_xticklabels(emerging, fontsize=7.5)
    axb.set_ylabel("mean recall (0–6) across panel")
    axb.set_ylim(0, 1.4)
    axb.legend(loc="center right", fontsize=7.5)
    # demarcation border + label
    axb.add_patch(Rectangle((0, 0), 1, 1, transform=axb.transAxes, fill=False,
                            edgecolor=WARM, lw=1.4, ls=(0, (4, 3)), zorder=10, clip_on=False))
    axb.text(0.01, 0.98, "EXPLORATORY — not a confirmatory test", transform=axb.transAxes,
             ha="left", va="top", fontsize=8, color=WARM, fontweight="bold")
    axb.set_title("Exploratory — emerging-brand recall rose under Arm B but did not cross the floor",
                  fontsize=9, loc="left", color=WARM)
    add_header(fig, "Emerging-brand instability: predicted, but sub-floor",
               "TERTIARY · H_EmergingInstability — Cell-B disruptors",
               "Top: the locked flip test is zero. Bottom (exploratory): newer models recall Rivian/Lucid more, but below the v1.7 floor.")
    add_footer(fig, verdict="TERTIARY FALSIFIED — zero floor-crossing flips; sub-floor rise is exploratory only.",
               phase=PHASE, protocol="v1.7")
    save(fig, 3)


if __name__ == "__main__":
    setup()
    print("building v0.32 figures (one per finding):")
    fig01(); fig02(); fig03()
    print("done.")
