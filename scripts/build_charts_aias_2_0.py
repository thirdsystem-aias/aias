#!/usr/bin/env python3
"""
build_charts_aias_2_0.py — AIAS(TM) 2.0 synthesis paper figures (academic register).
House style via scripts/chart_style.py; forked from scripts/build_charts_v1_9.py.

  chart_01_component_roadmap      two of six components measured (outline §9, Fig 1)
  chart_02_coupling_by_instrument CV-CPC vs phi vs C*: coupling with Presence (Fig 2)
  chart_03_presence_by_consistency P x C* per category, June and November (Fig 3)
  chart_04_reliability_ladder     ~3 weeks vs ~5 months, against the frame null (Fig 4)
  chart_05_no_composite           the eight Stage 1 candidates, K1 and K2, + November (Fig 5)
  chart_06_rating_floor           share of brands rated for Consistency, by category and wave (Fig 6)

Single source: osf/aias_2_0/aias_2_0_synthesis_data.json and aias_2_0_profiles.csv
(tag aias-2-0-data-locked); the only other input is the v1.9 pre-registration text, for the
pre-look windfall figures quoted in chart 06. Nothing is computed here that the data
lock does not already hold, except shares and positions for drawing.
Deviation from the outline's Fig 2 list: the rejected C_phiJ + FLOOR rows are left to the
text (§4.5), so the chart compares only the instruments the program used or adopted.

Output: reports/figs/aias_2_0/chart_0N_<topic>.pdf
Run on the Mac (Akkurat Pro): AIAS_ROOT=<tree> ~/aias/venv/bin/python scripts/build_charts_aias_2_0.py
"""
import csv
import json
import os
import re
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(os.environ.get("AIAS_ROOT", str(Path.home() / "aias")))
sys.path.insert(0, str(ROOT / "scripts"))
import chart_style as cs  # noqa: E402
cs.setup()

OUT = ROOT / "reports/figs/aias_2_0"
OUT.mkdir(parents=True, exist_ok=True)
A2 = ROOT / "osf/aias_2_0"
D = json.load(open(A2 / "aias_2_0_synthesis_data.json"))
assert D["status"] == "complete" and D["stage2"]["class"]["class"] == "A", "build figures only from the data lock"
PROF = list(csv.DictReader(open(A2 / "aias_2_0_profiles.csv", newline="")))
LIN = D["lineage"]
CAL = LIN["v1.9-stage1"]["record"]
V19 = D["stage2"]["v19_verdicts"]
V41 = D["stage2"]["v41_verdicts"]
SUM = D["summaries"]

PHASE = "2.0 synthesis (data lock aias-2-0-data-locked)"
PROTOCOL = "Presence v1.6 · Consistency v1.8, v1.9"
INDIGO, GRAY, WARM = cs.PALETTE["indigo"], cs.PALETTE["gray"], cs.PALETTE["warm"]
LIGHT = cs.PALETTE["indigo_t2"]
OMNI = ["v0.19", "v0.20", "v0.21", "v0.22", "v0.23"]
NAME = {"v0.19": "Audiophile headphones", "v0.20": "Skincare", "v0.21": "Cosmetics",
        "v0.22": "Automotive", "v0.23": "Premium spirits"}
WAVE = {"t1": "May", "t2": "June", "t3": "November"}


def _save(fig, name, verdict):
    cs.add_footer(fig, verdict=verdict, phase=PHASE, protocol=PROTOCOL)
    fig.savefig(OUT / f"{name}.pdf", **cs.SAVEFIG_PARAMS)
    plt.close(fig)
    print(f"  wrote {name}.pdf")


def _clean_axes(ax, left=True):
    for s in ("top", "right") + (() if left else ("left",)):
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=8)


# ============================================================ 01
def chart_01():
    comps = [("Presence", "AIAS 1.0", True, "Locks v1.2–v1.6\nSSRN 6817841"),
             ("Consistency", "AIAS 2.0", True, "Locks v1.7–v1.9\nthis synthesis"),
             ("Ranking", "AIAS 3.0", False, "next"),
             ("Sentiment", "AIAS 4.0", False, ""),
             ("Coverage", "AIAS 5.0", False, ""),
             ("Grounding", "AIAS 6.0", False, "")]
    fig, ax = plt.subplots(figsize=(7.5, 2.9))
    ax.set_xlim(0, 6); ax.set_ylim(0, 1); ax.axis("off")
    for i, (name, ver, measured, note) in enumerate(comps):
        x0 = i + 0.06
        box = FancyBboxPatch((x0, 0.40), 0.88, 0.42, boxstyle="round,pad=0.0,rounding_size=0.05",
                             fc=INDIGO if measured else "white", ec=INDIGO if measured else cs.PALETTE["gray_light"],
                             lw=1.0, transform=ax.transData)
        ax.add_patch(box)
        col = "white" if measured else GRAY
        ax.text(x0 + 0.44, 0.66, name, ha="center", va="center", fontsize=9.6, fontweight="bold", color=col)
        ax.text(x0 + 0.44, 0.52, ver, ha="center", va="center", fontsize=8, color=col)
        if note:
            ax.text(x0 + 0.44, 0.33, note, ha="center", va="top", fontsize=7.2,
                    color=INDIGO if measured else GRAY, linespacing=1.3)
    ax.annotate("", xy=(1.97, 0.88), xytext=(0.03, 0.88),
                arrowprops=dict(arrowstyle="-", color=INDIGO, lw=1.2))
    ax.text(1.0, 0.92, "measured, reported side by side", ha="center", va="bottom", fontsize=7.6, color=INDIGO)
    fig.subplots_adjust(top=0.70, bottom=0.14, left=0.04, right=0.98)
    cs.add_header(fig, "Two of the six AIAS components are now measured",
                  "Presence (AIAS 1.0) and Consistency (AIAS 2.0); the other four are planned, in roadmap order.",
                  "AIAS 2.0 reports the two measured components as two scores; it does not combine them.")
    _save(fig, "chart_01_component_roadmap",
          "Measured: Presence (AIAS 1.0) and Consistency (AIAS 2.0); no composite (v1.9 Stage 1: no candidate passed K1–K3).")


# ============================================================ 02
def chart_02():
    v17 = LIN["v1.7"]["record"]["H_CPC_Dissociates"]["pooled"]["composite"]
    v18 = LIN["v1.8"]["record"]["verdicts"]
    cvr = v18["H_CV_Reproduces"]["stat"]; mi = v18["H_MeanIndependent"]["stat"]["pooled"]
    dis = V19["H_Dissociation_t3"]
    rows = [  # label, |rho|, n, colour, bold
        ("CV-CPC with the Presence composite (v1.7)", v17["abs_rho"], v17["n"], WARM, False),
        ("CV-CPC with mean recall (v1.8 reproduction)", cvr["abs_rho"], cvr["n"], WARM, False),
        ("φ with mean recall (v1.8)", mi["abs_rho"], mi["n"], INDIGO, False),
        ("C* with P, May (v1.9 Stage 1)", abs(SUM["t1"]["rho_Cstar_P"]), SUM["t1"]["rho_Cstar_P_n"], INDIGO, False),
        ("C* with P, June (v1.9 Stage 1)", abs(SUM["t2"]["rho_Cstar_P"]), SUM["t2"]["rho_Cstar_P_n"], INDIGO, False),
        ("C* with P, November (v1.9 Stage 2, confirmatory)", abs(dis["rho"]), dis["n"], INDIGO, True),
    ]
    fig, ax = plt.subplots(figsize=(7.5, 4.0))
    ys = np.arange(len(rows))[::-1]
    for y, (lab, v, n, col, bold) in zip(ys, rows):
        ax.plot([0, v], [y, y], color=col, lw=1.4, alpha=0.55, zorder=1)
        ax.scatter([v], [y], s=64 if bold else 44, color=col, zorder=3, edgecolor="white", lw=0.6)
        ax.text(v + 0.018, y, f"{v:.3f}  (n = {n})", va="center", ha="left", fontsize=7.8, color=col,
                fontweight="bold" if bold else "normal", zorder=4,
                bbox=dict(boxstyle="square,pad=0.15", fc="white", ec="none"))
    ax.axvline(0.50, color=WARM, lw=1.0, ls="--", zorder=0)
    ax.text(0.505, ys[0] + 0.62, "0.50: independence ceiling (v1.7, v1.8, K1)", fontsize=7.2, color=cs.PALETTE["warm_t1"],
            ha="left", va="bottom")
    ax.axvline(0.30, color=INDIGO, lw=0.9, ls=":", zorder=0)
    ax.text(0.295, ys[0] + 0.62, "0.30: H_Dissociation_t3 line", fontsize=7.2, color=INDIGO, ha="right", va="bottom")
    ax.set_yticks(ys); ax.set_yticklabels([r[0] for r in rows], fontsize=8)
    ax.set_xlim(0, 1.0); ax.set_ylim(-0.6, len(rows) - 0.1)
    ax.set_xlabel("absolute rank correlation with Presence or mean recall", fontsize=8.5)
    _clean_axes(ax); ax.tick_params(axis="y", length=0)
    fig.subplots_adjust(top=0.76, bottom=0.21, left=0.37, right=0.97)
    cs.add_header(fig, "Consistency had to be rebuilt to stand apart from Presence",
                  "Coupling of each Consistency measure with how often brands are named.",
                  "CV-CPC moved with recall and was not adopted; the φ-based score stays near zero, in November as well.")
    _save(fig, "chart_02_coupling_by_instrument",
          f"H_Dissociation_t3 CONFIRMED: |ρ(C*, P)| = {abs(dis['rho']):.3f} in November (at or below 0.30); "
          f"v1.7 H_CPC_Dissociates FALSIFIED ({v17['abs_rho']:.3f}, above 0.50).")


# ============================================================ 03
def chart_03():
    fig, axes = plt.subplots(2, 3, figsize=(7.5, 5.6), sharex=True, sharey=True)
    flat = axes.ravel()
    for ax, s in zip(flat, OMNI):
        jun = [r for r in PROF if r["wave"] == "t2" and r["substrate"] == s and r["rated"] == "1"]
        nov = [r for r in PROF if r["wave"] == "t3" and r["substrate"] == s]
        rated = [r for r in nov if r["rated"] == "1"]; unr = [r for r in nov if r["rated"] != "1"]
        ax.scatter([float(r["P"]) for r in jun], [float(r["C_star"]) for r in jun], s=22, facecolor="none",
                   edgecolor=LIGHT, lw=0.9, zorder=2)
        ax.scatter([float(r["P"]) for r in rated], [float(r["C_star"]) for r in rated], s=24, color=INDIGO,
                   edgecolor="white", lw=0.4, zorder=3)
        ax.scatter([float(r["P"]) for r in unr], [-9] * len(unr), s=16, marker="|", color=GRAY, zorder=3)
        ax.axhline(-4, color=cs.PALETTE["gray_light"], lw=0.6)
        ax.set_title(f"{NAME[s]}\n{len(rated)} of {len(nov)} rated in November", fontsize=8, loc="left",
                     color=cs.PALETTE["black"], fontweight="normal")
        ax.set_xlim(0, 100); ax.set_ylim(-14, 105); ax.set_yticks([0, 50, 100]); ax.set_xticks([0, 50, 100])
        _clean_axes(ax)
    flat[2].tick_params(labelbottom=True)          # its column has no panel below it
    key = flat[5]; key.axis("off")
    key.scatter([0.08], [0.78], s=24, color=INDIGO, transform=key.transAxes, clip_on=False)
    key.text(0.16, 0.78, "rated brand, November", transform=key.transAxes, va="center", fontsize=7.8)
    key.scatter([0.08], [0.62], s=22, facecolor="none", edgecolor=LIGHT, lw=0.9, transform=key.transAxes, clip_on=False)
    key.text(0.16, 0.62, "rated brand, June", transform=key.transAxes, va="center", fontsize=7.8)
    key.scatter([0.08], [0.46], s=16, marker="|", color=GRAY, transform=key.transAxes, clip_on=False)
    key.text(0.16, 0.46, "not rated in November\n(under 6 mentions), at its P", transform=key.transAxes,
             va="center", fontsize=7.8, linespacing=1.25)
    r2, r3 = SUM["t2"]["rho_Cstar_P"], V19["H_Dissociation_t3"]["rho"]
    key.text(0.02, 0.18, f"Rank correlation of C* with P\nwithin categories: {r2:.2f} (June),\n{r3:.2f} (November)",
             transform=key.transAxes, va="center", fontsize=7.8, color=INDIGO, linespacing=1.3)
    for ax in axes[1, :2]:
        ax.set_xlabel("Presence P (0 to 100)", fontsize=8)
    axes[1, 2].set_xlabel("")
    for ax in axes[:, 0]:
        ax.set_ylabel("Consistency C* (0 to 100)", fontsize=8)
    fig.subplots_adjust(top=0.80, bottom=0.15, left=0.09, right=0.98, hspace=0.42, wspace=0.12)
    cs.add_header(fig, "Being named often and being named consistently are different",
                  "Each dot is a brand rated on both scores, per category, in June and November.",
                  "A brand's Presence says little about how evenly the six models name it.")
    _save(fig, "chart_03_presence_by_consistency",
          f"H_Dissociation_t3 CONFIRMED: ρ(C*, P) = {r3:.2f}, n = {V19['H_Dissociation_t3']['n']} (within-category ranks).")


# ============================================================ 04
def chart_04():
    selected = next(c for c in CAL["candidates"] if c["spec"] == "C_phi+FLOOR+ADD")
    phi_tw = LIN["v1.8"]["record"]["two_wave_reproducibility"]["phi_t1_t2_rank_agreement"]
    prs, crs, phl = V19["H_Presence_Score_Reliability"], V19["H_Consistency_Reliability"], V41["H_Phi_LongHorizon"]
    rows = [  # label, short (value, n), long (value, n), pass mark, frame null (mean, p95) or None
        ("Presence score P", "within-category ranks", (CAL["presence_retest_t1_t2"], CAL["presence_retest_n"]),
         (prs["rho"], prs["n"]), 0.80, None),
        ("Consistency score C*", "within-category ranks", (selected["retest_C"], selected["retest_C_n"]),
         (crs["rho"], crs["n"]), 0.50, (crs["frame_structure_null"]["null_mean"], crs["frame_structure_null"]["null_p95"])),
        ("Raw φ", "pooled ranks", (phi_tw["rho"], phi_tw["n"]), (phl["rho"], phl["n"]), 0.50,
         (phl["frame_structure_null"]["null_mean"], phl["frame_structure_null"]["null_p95"])),
    ]
    fig, ax = plt.subplots(figsize=(7.5, 4.0))
    ys = [2, 1, 0]
    for y, (lab, stat, sh, lo, mark, null) in zip(ys, rows):
        ax.plot([0, 1], [y, y], color=cs.PALETTE["gray_light"], lw=0.7, zorder=0)
        if null:
            ax.plot([null[0], null[1]], [y, y], color=cs.PALETTE["indigo_t3"], lw=8, solid_capstyle="butt", zorder=1)
            ax.text((null[0] + null[1]) / 2, y - 0.2, f"frames alone: {null[0]:.2f}–{null[1]:.2f}", ha="center",
                    va="top", fontsize=7, color=GRAY)
        ax.plot([mark, mark], [y - 0.15, y + 0.15], color=WARM, lw=1.4, zorder=2)
        ax.text(mark, y + 0.19, f"pass {mark:.2f}", ha="center", va="bottom", fontsize=7, color=cs.PALETTE["warm_t1"])
        ax.scatter([sh[0]], [y], s=56, facecolor="white", edgecolor=INDIGO, lw=1.3, zorder=3)
        ax.scatter([lo[0]], [y], s=56, color=INDIGO, zorder=4)
    labels = [f"{lab} ({stat})\n3 weeks {sh[0]:.2f} (n {sh[1]})  →  5 months {lo[0]:.2f} (n {lo[1]})"
              for lab, stat, sh, lo, _, _ in rows]
    ax.scatter([], [], s=56, facecolor="white", edgecolor=INDIGO, lw=1.3, label="May to June (about 3 weeks)")
    ax.scatter([], [], s=56, color=INDIGO, label="June to November (about 5 months)")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2, fontsize=7.8, frameon=False)
    ax.set_yticks(ys); ax.set_yticklabels(labels, fontsize=7.8, linespacing=1.5)
    ax.set_xlim(0, 1); ax.set_ylim(-0.6, 2.6)
    ax.set_xlabel("rank correlation between waves", fontsize=8.5)
    _clean_axes(ax, left=False); ax.tick_params(axis="y", length=0)
    fig.subplots_adjust(top=0.76, bottom=0.27, left=0.40, right=0.97)
    cs.add_header(fig, "Both scores keep their brand order over five months",
                  "Agreement between waves for each score, short and long horizon.",
                  "Shaded: what the question frames alone produce when models are shuffled (mean to 95th percentile, November).")
    dec = V41["H_Horizon_Decay"]
    _save(fig, "chart_04_reliability_ladder",
          f"H_Presence_Score_Reliability, H_Consistency_Reliability (p_frame = {crs['frame_structure_null']['p_frame']:.3f}) "
          f"and H_Phi_LongHorizon CONFIRMED; H_Horizon_Decay {dec['phi']['verdict']} (no detectable decay).")


# ============================================================ 05
def chart_05():
    lab = {"C_phi": "φ", "C_phiJ": "φ + J", "FLOOR": "floor", "SHRINK": "shrink", "ADD": "average", "MOD": "multiply"}
    cands = CAL["candidates"]
    names = [f"{lab[c['consistency']]} · {lab[c['low_count']]} · {lab[c['form']]}" for c in cands]
    y = np.arange(len(cands))[::-1]
    sel = [i for i, c in enumerate(cands) if c["spec"] == "C_phi+FLOOR+ADD"][0]
    nov = {"K1": abs(V19["H_Dissociation_t3"]["rho"]), "K2": V19["H_NoComposite_t3"]["rho_A_P"]}
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.5, 4.6), sharey=True)
    for ax, k, lim, xl, title in ((a1, "K1", CAL["constants"]["K1"], (0.0, 0.85), "K1: Consistency with Presence\n(pass at or below 0.50)"),
                                  (a2, "K2", CAL["constants"]["K2"], (0.92, 1.0), "K2: composite with Presence\n(pass at or below 0.95)")):
        for i, c in enumerate(cands):
            v1, v2 = abs(c["t1"][k]["rho"]), abs(c["t2"][k]["rho"])
            ax.plot([v1, v2], [y[i], y[i]], color=cs.PALETTE["gray_light"], lw=1.2, zorder=1)
            ax.scatter([v1], [y[i]], s=30, color=LIGHT, zorder=3, label="May" if i == 0 else None)
            ax.scatter([v2], [y[i]], s=30, color=INDIGO, zorder=3, label="June" if i == 0 else None)
        ax.scatter([nov[k]], [y[sel]], s=46, marker="D", facecolor="white", edgecolor=WARM, lw=1.3, zorder=4,
                   label="November, locked score")
        ax.axvline(lim, color=WARM, lw=1.0, ls="--", zorder=2)
        ax.axvspan(lim, xl[1], color=cs.PALETTE["warm_t3"], alpha=0.25, zorder=0, lw=0)
        ax.set_xlim(*xl)
        ax.set_title(title, fontsize=8.4, color=cs.PALETTE["black"], loc="left", fontweight="normal")
        ax.set_xlabel("absolute rank correlation", fontsize=8.2)
        _clean_axes(ax)
    a1.set_yticks(y); a1.set_yticklabels(names, fontsize=7.8)
    a1.tick_params(axis="y", length=0)
    a1.legend(loc="upper center", bbox_to_anchor=(1.0, -0.17), ncol=3, fontsize=7.6, frameon=False)
    a2.text(0.98, 0.985, "shaded = fails", transform=a2.transAxes, ha="right", va="top", fontsize=7.2,
            color=GRAY, fontstyle="italic")
    fig.subplots_adjust(top=0.72, bottom=0.27, left=0.24, right=0.97, wspace=0.08)
    cs.add_header(fig, "No single score passes: the composite follows Presence",
                  "The eight pre-specified composites, May and June (v1.9 Stage 1), with November for the locked score.",
                  "Row: Consistency score · rule for brands with few mentions · how the two are combined.")
    _save(fig, "chart_05_no_composite",
          f"v1.9 Stage 1: no candidate passed K1–K3 at both waves; November ρ(A, P) = {nov['K2']:.2f} "
          f"(H_NoComposite_t3, descriptive).")


# ============================================================ 06
def chart_06():
    mod = (ROOT / "osf/methodology/v1_9/prereg/v1_9_two_component_composite_content.py").read_text(encoding="utf-8")
    m = re.search(r"brands named once score ([\d.]+) on average\s+\(n (\d+)\) against ([\d.]+) for brands never named \(n (\d+)\)", mod)
    assert m, "pre-look windfall sentence not found in the v1.9 module"
    once, n_once, never, n_never = m.group(1), m.group(2), m.group(3), m.group(4)
    groups = OMNI + ["all"]
    fig, ax = plt.subplots(figsize=(7.5, 3.9))
    w = 0.26
    cols = {"t1": cs.PALETTE["indigo_t3"], "t2": LIGHT, "t3": INDIGO}
    for j, wave in enumerate(("t1", "t2", "t3")):
        ps = SUM[wave]["per_substrate"]
        vals = [ps[s]["n_rated"] / ps[s]["n_units"] for s in OMNI] + [SUM[wave]["n_rated"] / SUM[wave]["n_units"]]
        xs = np.arange(len(groups)) + (j - 1) * w
        ax.bar(xs, vals, width=w * 0.92, color=cols[wave], label=WAVE[wave], zorder=2)
        for x, v in zip(xs, vals):
            ax.text(x, v + 0.015, f"{v * 100:.0f}", ha="center", va="bottom", fontsize=6.6, color=cs.PALETTE["black"])
    ax.set_xticks(np.arange(len(groups)))
    ax.set_xticklabels([NAME[s].replace(" ", "\n", 1) if s != "all" else "All five\n(112 brands)" for s in groups],
                       fontsize=7.8)
    ax.set_ylim(0, 0.85); ax.set_yticks([0, 0.25, 0.5, 0.75]); ax.set_yticklabels(["0%", "25%", "50%", "75%"])
    ax.set_ylabel("share of brands rated for C*", fontsize=8.5)
    ax.legend(loc="upper left", ncol=3, fontsize=7.6, frameon=False)
    _clean_axes(ax)
    ax.text(0.99, 0.97, f"Why a floor: a plain average of P and the unfloored score\nwould give brands named once {once} on average (n {n_once})\n"
                        f"against {never} for brands never named (n {n_never}).",
            transform=ax.transAxes, ha="right", va="top", fontsize=7.4, color=GRAY, linespacing=1.3,
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=cs.PALETTE["gray_light"], lw=0.6))
    fig.subplots_adjust(top=0.76, bottom=0.22, left=0.09, right=0.98)
    cs.add_header(fig, "About half the brands are named too rarely to rate for Consistency",
                  "Share of brands with six or more mentions across the six models (out of 36), by category and wave.",
                  "Below six mentions the score reflects chance, not agreement, so those brands carry Presence only.")
    _save(fig, "chart_06_rating_floor",
          "C* rated only at 6 or more total mentions (v1.9 FLOOR, locked); share rated "
          + ", ".join(f"{WAVE[w]} {SUM[w]['n_rated'] / SUM[w]['n_units'] * 100:.0f}%" for w in ("t1", "t2", "t3")) + ".")


if __name__ == "__main__":
    print("building AIAS 2.0 paper figures -> reports/figs/aias_2_0/")
    chart_01(); chart_02(); chart_03(); chart_04(); chart_05(); chart_06()
    print("done")
