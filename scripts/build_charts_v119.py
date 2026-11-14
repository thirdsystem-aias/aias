#!/usr/bin/env python3
"""
v1.19 Coverage Paper B -- figure builder (paper register). House style of build_charts_v112.py (scripts/chart_style.py:
bold title top-left, gray subtitle, thin Indigo rule, italic gray source line citing the pre-registration tag).
Every statistic printed on a chart is a leaf of osf/methodology/v1_19/outputs/v119_verdicts.json; chart 3's points are
Paper A's unit table read in memory from the pinned commit 949be61 (git cat-file, SHA-256 checked against the
verdicts' inputs.paper_A_unit_table_sha256; never written to the tree) and the frozen roster. Nothing is re-scored.
Titles describe what is plotted and never repeat a finding (CLAUDE.md, chart conventions).

One chart per finding with data (UNDETERMINED tests without a statistic get none: H34_Defunct_Occupancy, H35):
  chart_01_split_reliability     H32_SetSampling
  chart_02_cue_type_drop         H32_CueType
  chart_03_floor_flag            H34_Floor_Signature and H34_Floor_BeyondPresence
  chart_04_profile_replication   H36_Profile_Replication
  chart_05_category_profiles     H36_Structure / D36 (descriptive)
Usage: python3 scripts/build_charts_v119.py
"""
import csv
import hashlib
import io
import json
import subprocess
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import chart_style as cs  # noqa: E402
cs.setup()

VERDICTS = ROOT / "osf/methodology/v1_19/outputs/v119_verdicts.json"
ROSTER = ROOT / "osf/methodology/v1_19/prereg/phantom_roster_v1_19.csv"
EXPECTED_SHA = "bf363060e4e90aed81c918544f561b43f387b5e41ef20d08d4844dc2d2176776"
PAPER_A_REF = "949be61e01dfad9773e43b0855dc33e9de3cc852"
PAPER_A_TABLE = "osf/methodology/v1_12/v112_unit_table.csv"
OUT = ROOT / "reports/figs/v119"
SUBS = ["v0.19", "v0.20", "v0.21", "v0.22", "v0.23"]
CAT = {"v0.19": "Headphones", "v0.20": "Skincare", "v0.21": "Cosmetics", "v0.22": "Automotive", "v0.23": "Spirits"}
W_ORDER = ["why", "when", "where", "while", "with whom", "with what", "how feeling"]
SOURCE = "Source: AIAS™ Methodology v1.19, Coverage Paper B | pre-registration {tag} | answers: Coverage Paper A (v1.12) | Third System™"
TITLES = {
    1: "Split-half reliability of Cov* over the 64 balanced splits of the situation set",
    2: "Correlation of Cov* with Cov* after each cue type's two situations are dropped",
    3: "Cov* of brands with and without the recall-floor flag",
    4: "Half-to-half correlation of brands' excess situation profiles, by cue type",
    5: "Mean excess situation profile by category and cue type",
}
NAMES = {1: "chart_01_split_reliability", 2: "chart_02_cue_type_drop", 3: "chart_03_floor_flag",
         4: "chart_04_profile_replication", 5: "chart_05_category_profiles"}
r3 = lambda x: f"{x:.3f}"
p4 = lambda x: f"{x:.4f}"


def _header(fig, key, subtitle, desc=""):
    cs.add_header(fig, TITLES[key], subtitle, desc)
    y = 1.0 - (0.74 / fig.get_figheight())
    fig.add_artist(Line2D([cs.LEFT_X, 0.985], [y, y], transform=fig.transFigure, color=cs.INDIGO, lw=0.6))


def _save(fig, key, verdict, tag):
    _, _, _, vy, sy = cs._compute_positions(fig)
    fig.text(cs.LEFT_X, vy, verdict, fontsize=cs.FONT_SIZES["verdict"], color=cs.INDIGO, fontstyle="italic",
             ha="left", va="bottom")
    fig.text(cs.LEFT_X, sy, SOURCE.format(tag=tag), fontsize=cs.FONT_SIZES["source"], color=cs.GRAY,
             fontstyle="italic", ha="left", va="bottom")
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"{NAMES[key]}.pdf", **cs.SAVEFIG_PARAMS)
    fig.savefig(OUT / f"{NAMES[key]}_preview.png", dpi=110, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    print(f"  wrote {OUT / (NAMES[key] + '.pdf')}")


def _box(ax, text, x=0.03, y=0.97, ha="left", va="top", fs=7.6):
    ax.text(x, y, text, transform=ax.transAxes, ha=ha, va=va, fontsize=fs, color=cs.INDIGO,
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=cs.INDIGO, lw=0.6), zorder=5)


def chart_01(V):
    S = V["H32_SetSampling"]
    items = sorted(S["per_split"].items(), key=lambda kv: kv[1]["rel"])
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    ax.axhspan(-0.2, 0.30, color=cs.PALETTE["warm_t3"], alpha=0.25, zorder=0)
    ax.axhspan(0.50, 1.0, color=cs.PALETTE["indigo_t3"], alpha=0.30, zorder=0)
    xs = list(range(1, len(items) + 1))
    ax.scatter(xs, [v["rel"] for _, v in items], s=18, color=cs.GRAY, zorder=3)
    for i, (code, v) in enumerate(items):
        if code == str(S["paper_A_H4_split_code"]):
            ax.scatter([i + 1], [v["rel"]], s=60, color=cs.INDIGO, zorder=4)
            ax.annotate(f"split 0 (Paper A's halves): {r3(v['rel'])}", (i + 1, v["rel"]), xytext=(-150, 14),
                        textcoords="offset points", fontsize=7.6, color=cs.INDIGO,
                        arrowprops=dict(arrowstyle="-", color=cs.INDIGO, lw=0.6))
    ax.axhline(S["rel_median"], color=cs.INDIGO, lw=0.9, ls="--", zorder=2)
    ax.axhline(S["rel_p10"], color=cs.PALETTE["warm_t1"], lw=0.9, ls=":", zorder=2)
    ax.text(1, S["rel_median"] + 0.015, f"median-based rel = {r3(S['rel_median'])}", fontsize=7.4, color=cs.INDIGO)
    ax.text(1, S["rel_p10"] + 0.015, f"P10 = {r3(S['rel_p10'])}", fontsize=7.4, color=cs.PALETTE["warm_t1"])
    ax.set_xlim(0, len(items) + 1)
    ax.set_ylim(-0.2, 0.8)
    ax.set_xlabel(f"the {S['splits']} balanced splits, sorted by reliability", fontsize=9)
    ax.set_ylabel("split-half reliability rel = 2r/(1 + r)", fontsize=9)
    ax.tick_params(labelsize=8.5)
    _box(ax, f"median r = {r3(S['median_r'])}, rel = {r3(S['rel_median'])}\nP10 of rel = {r3(S['rel_p10'])}\n"
             f"one-sided p_perm = {p4(S['p_perm_one_sided'])}\nsplit 0 at the {S['paper_A_split_percentile']:g}th "
             f"percentile", x=0.97, y=0.03, ha="right", va="bottom")
    fig.subplots_adjust(top=0.80, bottom=0.17, left=0.10, right=0.97)
    _header(fig, 1, "Each split puts one situation of each cue type in each half; Cov* on panel N3 per half.",
            "Shaded: rel at least 0.50 (Indigo) and below 0.30 (warm), the pre-registered bands (§3.1).")
    _save(fig, 1, f"H32_SetSampling: {V['verdict_summary']['H32_SetSampling']} — rel = {r3(S['rel_median'])}, "
                  f"P10 = {r3(S['rel_p10'])}", V["prereg_tag"])


def chart_02(V):
    C = V["H32_CueType"]
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero_short"])
    ax.axvline(C["reference_p5"], color=cs.WARM, lw=0.9, ls=":", zorder=1)
    ax.axvline(C["reference_median"], color=cs.PALETTE["gray_light"], lw=0.9, ls="--", zorder=1)
    for i, w in enumerate(W_ORDER):
        y = len(W_ORDER) - i
        v = C["per_W"][w]["rho_w_full_vs_minus_W"]
        col = cs.INDIGO if w in C["W_below_p5"] else cs.GRAY
        ax.scatter([v], [y], s=42, color=col, zorder=3)
        ax.text(v + 0.006, y + 0.22, r3(v), fontsize=7.4, color=col)
    ax.set_yticks([len(W_ORDER) - i for i in range(len(W_ORDER))])
    ax.set_yticklabels([f"without {w} (n = {C['per_W'][w]['n']})" for w in W_ORDER], fontsize=8)
    ax.set_xlim(0.70, 1.0)
    ax.set_ylim(0.3, len(W_ORDER) + 1.3)
    ax.set_xlabel("ρ_w(Cov* on 14 situations, Cov* on the 12 left)", fontsize=9)
    ax.tick_params(labelsize=8.5)
    ax.text(C["reference_p5"] - 0.003, len(W_ORDER) + 0.85, f"reference 5th percentile {r3(C['reference_p5'])}",
            fontsize=7.2, color=cs.WARM, ha="right")
    ax.text(C["reference_median"] + 0.003, len(W_ORDER) + 0.85, f"reference median {r3(C['reference_median'])}",
            fontsize=7.2, color=cs.GRAY, ha="left")
    fig.subplots_adjust(top=0.72, bottom=0.24, left=0.26, right=0.97)
    _header(fig, 2, f"Reference: {C['reference_pairs']} drops of two situations of different cue types; panel N3.",
            "Indigo: below the reference 5th percentile.")
    _save(fig, 2, f"H32_CueType: {V['verdict_summary']['H32_CueType']} — {C['count']} of 7 below the reference",
          V["prereg_tag"])


def _unit_table(V):
    b = subprocess.run(["git", "-C", str(ROOT), "cat-file", "blob", f"{PAPER_A_REF}:{PAPER_A_TABLE}"],
                       capture_output=True, check=True).stdout
    if hashlib.sha256(b).hexdigest() != V["inputs"]["paper_A_unit_table_sha256"]:
        sys.exit("[v1.19 charts] REFUSED: Paper A's unit table does not match the recorded SHA-256")
    return list(csv.DictReader(io.StringIO(b.decode("utf-8"))))


def chart_03(V):
    rows = _unit_table(V)
    flag = {(r["substrate"], r["brand"]): r["recall_floor_flag_F"] == "1"
            for r in csv.DictReader(io.StringIO(ROSTER.read_text(encoding="utf-8")))}
    rated = [r for r in rows if str(r["rated"]) == "1"]
    F = V["H34_Floor"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=cs.FIGSIZE["hero"], gridspec_kw={"width_ratios": [1.15, 1]})
    for i, s in enumerate(SUBS):
        for j, r in enumerate([r for r in rated if r["substrate"] == s]):
            f = flag[(s, r["brand"])]
            x = i + 1 + (0.16 if f else -0.16) + 0.05 * ((j % 3) - 1)
            a1.scatter([x], [float(r["cov_star"])], s=22, zorder=3, color=cs.INDIGO if f else "white",
                       edgecolor=cs.INDIGO if f else cs.GRAY, linewidth=0.8)
    a1.set_xticks(range(1, 6))
    nper = {s: (sum(1 for r in rated if r["substrate"] == s and flag[(s, r["brand"])]),
                sum(1 for r in rated if r["substrate"] == s and not flag[(s, r["brand"])])) for s in SUBS}
    a1.set_xticklabels([f"{CAT[s]}\n{nper[s][0]} / {nper[s][1]}" for s in SUBS], fontsize=7.4)
    a1.set_ylabel("Cov* (panel N3; 50 = situation-blind)", fontsize=9)
    a1.set_ylim(0, 52)
    a1.axhline(50, color=cs.PALETTE["gray_light"], lw=0.8, ls=":")
    a1.tick_params(labelsize=8)
    for r in rated:
        f = flag[(r["substrate"], r["brand"])]
        a2.scatter([float(r["P_comparator"])], [float(r["cov_star"])], s=22, zorder=3,
                   color=cs.INDIGO if f else "white", edgecolor=cs.INDIGO if f else cs.GRAY, linewidth=0.8)
    a2.set_xlabel("Presence P (v0.42, t₄, same models; 0–100)", fontsize=9)
    a2.set_ylim(0, 52)
    a2.set_xlim(-2, 102)
    a2.axhline(50, color=cs.PALETTE["gray_light"], lw=0.8, ls=":")
    a2.tick_params(labelsize=8)
    _box(a1, f"Cliff's δ = {r3(F['primary']['cliffs_delta'])}\np_perm = {p4(F['primary']['p_perm_two_sided'])}",
         fs=7.2)
    _box(a2, f"on residuals given P:\nδ = {r3(F['beyond_presence']['cliffs_delta_resid'])}, "
             f"p_perm = {p4(F['beyond_presence']['p_perm_two_sided'])}", fs=7.2)
    a2.legend(handles=[Line2D([], [], marker="o", ls="", color=cs.INDIGO, label=f"flagged ({F['n_flagged_rated']})"),
                       Line2D([], [], marker="o", ls="", markerfacecolor="white", markeredgecolor=cs.GRAY,
                              label=f"not flagged ({F['n_unflagged_rated']})")],
              loc="lower left", fontsize=7.2, frameon=False)   # lower left: no brand there (P >= 30)
    fig.subplots_adjust(top=0.80, bottom=0.19, left=0.09, right=0.98, wspace=0.18)
    _header(fig, 3, "Rated brands; flag: mean t₁ recall below 1.0 on the legacy panel (frozen roster). "
                    "Under each category: flagged / not.", "Points: Paper A's unit table (commit 949be61).")
    vs = V["verdict_summary"]
    _save(fig, 3, f"H34_Floor_Signature: {vs['H34_Floor_Signature']}; H34_Floor_BeyondPresence: "
                  f"{vs['H34_Floor_BeyondPresence']}", V["prereg_tag"])


def chart_04(V):
    R = V["H36_Profile_Replication"]
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero_short"])
    ax.axvspan(0.20, 0.5, color=cs.PALETTE["indigo_t3"], alpha=0.30, zorder=0)
    ax.axvspan(-0.5, 0.10, color=cs.PALETTE["warm_t3"], alpha=0.22, zorder=0)
    ax.axvline(0, color=cs.PALETTE["gray_light"], lw=0.8, zorder=1)
    ax.axvline(R["mean_rho_w_over_W"], color=cs.INDIGO, lw=0.9, ls="--", zorder=2)
    for i, w in enumerate(W_ORDER):
        y = len(W_ORDER) - i
        v = R["per_W"][w]
        ax.scatter([v], [y], s=40, color=cs.GRAY, zorder=3)
        ax.text(v + 0.014, y + 0.28, r3(v), fontsize=7.4, color=cs.GRAY)
    ax.text(R["mean_rho_w_over_W"] - 0.01, 0.55, f"mean R = {r3(R['mean_rho_w_over_W'])}", fontsize=7.4,
            color=cs.INDIGO, ha="right")
    ax.set_yticks([len(W_ORDER) - i for i in range(len(W_ORDER))])
    ax.set_yticklabels(W_ORDER, fontsize=8)
    ax.set_xlim(-0.4, 0.4)
    ax.set_ylim(0.3, len(W_ORDER) + 0.7)
    ax.set_xlabel("ρ_w(excess on the cue type's half-A situation, excess on its half-B situation)", fontsize=9)
    ax.tick_params(labelsize=8.5)
    _box(ax, f"R = {r3(R['mean_rho_w_over_W'])}\none-sided p_perm = {p4(R['p_perm_one_sided'])}\n"
             f"n = {R['n']} brands, {R['n_categories']} categories", x=0.97, y=0.97, ha="right")
    fig.subplots_adjust(top=0.72, bottom=0.24, left=0.14, right=0.97)
    _header(fig, 4, "Excess: mentions in the situation minus the situation-blind expectation, per brand mention; N3.",
            "Shaded: R at least 0.20 (Indigo) and below 0.10 (warm), the pre-registered bands (§7.2).")
    _save(fig, 4, f"H36_Profile_Replication: {V['verdict_summary']['H36_Profile_Replication']} — R = "
                  f"{r3(R['mean_rho_w_over_W'])}", V["prereg_tag"])


def chart_05(V):
    P = V["H36_Structure"]["D36_profiles"]["category_mean_profiles"]
    M = [[P[s]["mean_excess"][w] for w in W_ORDER] for s in SUBS]
    lim = max(abs(x) for row in M for x in row)
    cmap = LinearSegmentedColormap.from_list("ts_div", [cs.WARM, "#FFFFFF", cs.INDIGO])
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero_short"])
    im = ax.imshow(M, cmap=cmap, vmin=-lim, vmax=lim, aspect="auto")
    for i, row in enumerate(M):
        for j, x in enumerate(row):
            ax.text(j, i, f"{x:+.3f}", ha="center", va="center", fontsize=7.4,
                    color="white" if abs(x) > 0.6 * lim else cs.PALETTE["black"])
    ax.set_xticks(range(len(W_ORDER)))
    ax.set_xticklabels(W_ORDER, fontsize=8)
    ax.set_yticks(range(len(SUBS)))
    ax.set_yticklabels([f"{CAT[s]} (n = {P[s]['n']})" for s in SUBS], fontsize=8)
    ax.tick_params(length=0)
    cb = fig.colorbar(im, ax=ax, fraction=0.035, pad=0.02)
    cb.ax.tick_params(labelsize=7)
    fig.subplots_adjust(top=0.72, bottom=0.27, left=0.17, right=0.97)
    T = V["H36_Structure"]
    _header(fig, 5, f"Rated brands ({T['n']}); share of a brand's mentions, observed minus situation-blind expected.",
            "Each row sums to zero. Descriptive (pre-registration §7.4).")
    _save(fig, 5, f"H36_Structure: {T['cell']}", V["prereg_tag"])


def main():
    raw = VERDICTS.read_bytes()
    if hashlib.sha256(raw).hexdigest() != EXPECTED_SHA:
        sys.exit("[v1.19 charts] REFUSED: verdicts SHA-256 differs")
    V = json.loads(raw)
    print(f"building v1.19 figures -> {OUT}")
    for f in (chart_01, chart_02, chart_03, chart_04, chart_05):
        f(V)
    print("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
