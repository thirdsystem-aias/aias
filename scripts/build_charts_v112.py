#!/usr/bin/env python3
"""
v1.12 Coverage Paper A -- figure builder (paper register only: Paper A has no Third System report).
House style of build_charts_v42.py (scripts/chart_style.py: bold title top-left, gray subtitle, thin Indigo rule,
italic gray source line citing the pre-registration tag). Every number from the scorer's outputs.

One chart per pre-registered finding (PRE_REGISTRATION_v1_12.md sections 3-5):
  chart_01_situation_overlap     MC_Situation (instrument gate)
  chart_02_legs_bands            the gate legs and secondary tests against their bands (Paper A verdict)
  chart_03_cov_presence          H1_Sep_Presence
  chart_04_cov_consistency       H2_Sep_Consistency
  chart_05_naming_rate           H3_Sep_NamingRate (with raw Cov, MC_Positive)
  chart_06_halves                H4_Reliability
  chart_07_panel_replication     H8_Panel_Replication
  chart_08_baseline              cross-category baseline (section 5, descriptive)

Inputs: --verdicts (osf/methodology/v1_12/v112_verdicts.json) and --table (v112_unit_table.csv), both written by
score_v1_12.py. Nothing is re-scored: points are the unit table's values, every statistic printed on a chart is a
verdicts-JSON leaf formatted by papers/v1_12/v112_values.py. Chart titles describe what is plotted and never repeat
a finding's headline (CLAUDE.md). --watermark TEXT stamps every chart (synthetic runs only; required for them).

Usage (real run):  python3 scripts/build_charts_v112.py
Synthetic test:    python3 scripts/build_charts_v112.py --verdicts F.json --table F.csv --out /tmp/x/figs \
                       --watermark "SYNTHETIC TEST — NOT RESULTS"
"""
import argparse
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "papers/v1_12"))
import chart_style as cs  # noqa: E402
import v112_values as VV  # noqa: E402
cs.setup()

SUBCOL = {"v0.19": cs.PALETTE["indigo"], "v0.20": cs.PALETTE["warm"], "v0.21": cs.PALETTE["teal_t2"],
          "v0.22": cs.PALETTE["blue"], "v0.23": cs.PALETTE["magenta"]}
SOURCE = ("Source: AIAS™ Methodology v1.12, Coverage Paper A | pre-registration {tag} | comparators: v0.42 (t₄) | "
          "Third System™")
WATERMARK = None
PLAIN = {"H1_Sep_Presence": "Presence P_N3", "H2_Sep_Consistency": "Consistency C*_N3",
         "H3_Sep_NamingRate": "naming rate π_cov", "H4_Reliability": "half A vs half B",
         "H5_Sep_Ranking": "Ranking R*_S0", "H6_Sep_Sentiment": "Sentiment S",
         "H7_Sep_Presence_Legacy": "published Presence, t₃", "H8_Panel_Replication": "panel N3 vs C3"}
TITLES = {
    1: "Brand-set overlap between runs of one situation and between situations",
    2: "Rank correlations of Cov* with each comparator, with 95% intervals",
    3: "Cov* and Presence per brand",
    4: "Cov* and Consistency C* per brand",
    5: "Cov* and raw coverage against the naming rate in the situation answers",
    6: "Cov* on the two halves of the situation set",
    7: "Cov* on two panels that differ in one model",
    8: "Cov* per brand by category",
}
NAMES = {1: "chart_01_situation_overlap", 2: "chart_02_legs_bands", 3: "chart_03_cov_presence",
         4: "chart_04_cov_consistency", 5: "chart_05_naming_rate", 6: "chart_06_halves",
         7: "chart_07_panel_replication", 8: "chart_08_baseline"}


def _header(fig, key, subtitle, desc=""):
    cs.add_header(fig, TITLES[key], subtitle, desc)
    y = 1.0 - (0.74 / fig.get_figheight())
    fig.add_artist(Line2D([cs.LEFT_X, 0.985], [y, y], transform=fig.transFigure, color=cs.INDIGO, lw=0.6))


def _save(fig, key, verdict, tag, out):
    _, _, _, vy, sy = cs._compute_positions(fig)
    if verdict:
        fig.text(cs.LEFT_X, vy, verdict, fontsize=cs.FONT_SIZES["verdict"], color=cs.INDIGO, fontstyle="italic",
                 ha="left", va="bottom")
    fig.text(cs.LEFT_X, sy, SOURCE.format(tag=tag), fontsize=cs.FONT_SIZES["source"], color=cs.GRAY,
             fontstyle="italic", ha="left", va="bottom")
    if WATERMARK:
        fig.text(0.5, 0.5, WATERMARK, rotation=28, fontsize=30, color=cs.WARM, alpha=0.22, ha="center",
                 va="center", fontweight="bold", zorder=100)
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / f"{NAMES[key]}.pdf", **cs.SAVEFIG_PARAMS)
    fig.savefig(out / f"{NAMES[key]}_preview.png", dpi=110, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    print(f"  wrote {out / (NAMES[key] + '.pdf')}")


def _box(ax, text, x=0.03, y=0.97, ha="left", va="top", fs=7.6):
    ax.text(x, y, text, transform=ax.transAxes, ha=ha, va=va, fontsize=fs, color=cs.INDIGO,
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=cs.INDIGO, lw=0.6), zorder=5)


def _pts(rows, xcol, ycol, rated_only=True):
    out = {s: ([], []) for s in VV.SUBS}
    for r in rows:
        if rated_only and str(r.get("rated")) != "1":
            continue
        x, y = VV.fnum(r.get(xcol)), VV.fnum(r.get(ycol))
        if x is not None and y is not None and math.isfinite(x) and math.isfinite(y):
            out[r["substrate"]][0].append(x)
            out[r["substrate"]][1].append(y)
    return out


def _leg_text(V, h):
    leg = V["legs"][h]
    if leg.get("rho_w") is None:
        return f"{VV.LEG_SHORT[h]}: {leg['verdict']}", f"{VV.LEG_SHORT[h]} {leg['verdict']}"
    ci = leg.get("ci95_rho_w")
    txt = f"ρ_w = {VV.r3(leg['rho_w'])}"
    if ci:
        txt += f"   95% interval [{VV.r3(ci[0])}, {VV.r3(ci[1])}]"
    txt += f"\nn = {leg.get('n')} brands in {leg.get('n_categories')} categories"
    if leg.get("p_perm") is not None:
        txt += f"   p_perm = {VV.p4(leg['p_perm'])}"
    return txt, f"{h}: {leg['verdict']} — ρ_w = {VV.r3(leg['rho_w'])} (n = {leg.get('n')})"


def scatter(V, rows, key, h, xcol, ycol, xlabel, ylabel, subtitle, out, xlim=None, ylim=None, rated_only=True,
            diag=False):
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    pts = _pts(rows, xcol, ycol, rated_only)
    if diag:
        ax.plot([0, 100], [0, 100], color=cs.PALETTE["gray_light"], lw=0.8, ls="--", zorder=1)
    for s in VV.SUBS:
        x, y = pts[s]
        ax.scatter(x, y, s=28, color=SUBCOL[s], alpha=0.85, edgecolor="white", linewidth=0.4, zorder=3,
                   label=f"{VV.CAT[s]} (n = {len(x)})")
    if ycol.startswith("cov_star") or ycol == "cov_star":
        ax.axhline(50, color=cs.PALETTE["gray_light"], lw=0.8, ls=":", zorder=1)
    if xlim:
        ax.set_xlim(*xlim)
    if ylim:
        ax.set_ylim(*ylim)
    ax.set_xlabel(xlabel, fontsize=9)
    ax.set_ylabel(ylabel, fontsize=9)
    ax.tick_params(labelsize=8.5)
    ax.legend(loc="center left", bbox_to_anchor=(1.01, 0.5), fontsize=7.2, frameon=False)
    txt, verdict = _leg_text(V, h)
    _box(ax, txt)
    fig.subplots_adjust(top=0.80, bottom=0.17, left=0.10, right=0.74)
    _header(fig, key, subtitle, "ρ_w: Spearman on within-category ranks centred per category (pre-registration §2.5). "
                                "Dotted: Cov* = 50, situation-blind naming.")
    _save(fig, key, verdict, V["prereg_tag"], out)


def chart_01(V, rows, out):
    ms = V["MC"]["MC_Situation"]
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    for s in VV.SUBS:
        c = [x for x in ms.get("cells") or [] if x["substrate"] == s and x["J_between"] is not None
             and x["J_within"] is not None]
        ax.scatter([x["J_between"] for x in c], [x["J_within"] for x in c], s=28, color=SUBCOL[s], alpha=0.85,
                   edgecolor="white", linewidth=0.4, zorder=3, label=f"{VV.CAT[s]} ({len(c)} cells)")
    ax.plot([0, 1], [0, 1], color=cs.PALETTE["gray_light"], lw=0.8, ls="--", zorder=1)
    ax.plot([0, 0.9], [0.1, 1.0], color=cs.WARM, lw=0.8, ls=":", zorder=1)
    ax.axvline(0.60, color=cs.WARM, lw=0.8, ls=":", zorder=1)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_xlabel("J_between: mean Jaccard of brand sets, different situations (same model and run)", fontsize=9)
    ax.set_ylabel("J_within: mean Jaccard, same situation, other runs", fontsize=9)
    ax.tick_params(labelsize=8.5)
    ax.legend(loc="center left", bbox_to_anchor=(1.01, 0.5), fontsize=7.2, frameon=False)
    _box(ax, f"pooled J_within − J_between = {VV.r3(ms['pooled_mean_J_within_minus_J_between'])} (minimum 0.10)\n"
             f"pooled J_between = {VV.r3(ms['pooled_mean_J_between'])} (maximum 0.60)\n"
             f"cells: {ms['cells_used']}")
    fig.subplots_adjust(top=0.80, bottom=0.17, left=0.10, right=0.74)
    _header(fig, 1, f"One point per model × run × category of panel {V['primary_panel']}; registry brands only.",
            "Dashed: equal overlap. Dotted: the pre-registered limits (difference 0.10; J_between 0.60).")
    _save(fig, 1, f"MC_Situation: {'passed' if ms['passed'] else 'failed'} — difference "
                  f"{VV.r3(ms['pooled_mean_J_within_minus_J_between'])}", V["prereg_tag"], out)


def chart_02(V, rows, out):
    legs = [h for h in VV.ALL_LEGS if V["legs"][h].get("rho_w") is not None]
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    ax.axvspan(-0.30, 0.30, color=cs.PALETTE["indigo_t3"], alpha=0.35, zorder=0)
    for x in (-0.5, 0.5):
        ax.axvline(x, color=cs.WARM, lw=0.8, ls=":", zorder=1)
    ax.axvline(0, color=cs.PALETTE["gray_light"], lw=0.8, zorder=1)
    for i, h in enumerate(legs):
        leg = V["legs"][h]
        y = len(legs) - i
        ci = leg.get("ci95_rho_w")
        col = cs.INDIGO if h in V["paper_A_verdict"]["legs"] else cs.GRAY
        if ci:
            ax.plot(ci, [y, y], color=col, lw=1.6, zorder=2)
        ax.scatter([leg["rho_w"]], [y], s=40, color=col, zorder=3)
        if h == "H4_Reliability":
            ax.scatter([leg["transformed"]], [y], s=40, marker="D", facecolor="white", edgecolor=col, zorder=3)
        ax.text(1.03, y, leg["verdict"], fontsize=7.6, va="center", ha="left", color=col,
                transform=ax.get_yaxis_transform())
    ax.set_yticks([len(legs) - i for i in range(len(legs))])
    ax.set_yticklabels([f"{VV.LEG_SHORT[h]}: {PLAIN[h]}" for h in legs], fontsize=8)
    ax.set_xlim(-1, 1)
    ax.set_xlabel("pooled within-category ρ_w (H4: r of the halves; diamond = rel = 2r/(1 + r))", fontsize=9)
    ax.tick_params(labelsize=8.5)
    fig.subplots_adjust(top=0.80, bottom=0.17, left=0.30, right=0.86)
    _header(fig, 2, f"Panel {V['primary_panel']}, search off; Indigo: legs in the gate; gray: secondary or not gating.",
            "Shaded: |ρ_w| ≤ 0.30 (separable). Dotted: |ρ_w| = 0.50. H4 and H8 have their own bars (§2.7).")
    _save(fig, 2, f"Paper A: {V['paper_A_verdict']['label']}", V["prereg_tag"], out)


def chart_05(V, rows, out):
    fig, (a1, a2) = plt.subplots(1, 2, figsize=cs.FIGSIZE["hero"], sharex=True)
    for ax, ycol, rated, lab in ((a1, "cov_star", True, "Cov* (rated brands)"),
                                 (a2, "raw_cov_k2", False, "raw Cov, k = 2 (all brands, %)")):
        pts = _pts(rows, "pi_cov", ycol, rated)
        for s in VV.SUBS:
            x, y = pts[s]
            ax.scatter(x, y, s=20, color=SUBCOL[s], alpha=0.85, edgecolor="white", linewidth=0.3, zorder=3,
                       label=VV.CAT_SHORT[s])
        ax.set_ylim(-2, 102)
        ax.set_ylabel(lab, fontsize=9)
        ax.set_xlabel("naming rate π_cov in the situation answers", fontsize=9)
        ax.tick_params(labelsize=8)
    a1.axhline(50, color=cs.PALETTE["gray_light"], lw=0.8, ls=":", zorder=1)
    a2.legend(loc="upper right", fontsize=7, frameon=False)
    leg = V["legs"]["H3_Sep_NamingRate"]
    _box(a1, _leg_text(V, "H3_Sep_NamingRate")[0], fs=7)
    _box(a2, f"ρ_w = {VV.r3(V['MC']['MC_Positive']['rho_w_raw_cov_pi_cov'])}\n(MC_Positive: |ρ_w| ≥ 0.50 expected)",
         fs=7)
    fig.subplots_adjust(top=0.80, bottom=0.17, left=0.09, right=0.98, wspace=0.28)
    _header(fig, 5, f"Panel {V['primary_panel']}; left: the component score; right: the raw share of situations covered.",
            "Raw coverage is expected to follow the naming rate (Double Jeopardy); Cov* adjusts for it.")
    _save(fig, 5, f"H3_Sep_NamingRate: {leg['verdict']}", V["prereg_tag"], out)


def chart_08(V, rows, out):
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    data = []
    for i, s in enumerate(VV.SUBS):
        v = [VV.fnum(r["cov_star"]) for r in rows if r["substrate"] == s and str(r.get("rated")) == "1"]
        v = [x for x in v if x is not None]
        data.append(v)
        ax.scatter([i + 1 + 0.18 * ((j % 5) - 2) / 2 for j in range(len(v))], v, s=16, color=SUBCOL[s], alpha=0.8,
                   edgecolor="white", linewidth=0.3, zorder=3)
    ax.boxplot([d if d else [float("nan")] for d in data], widths=0.5, showfliers=False,
               medianprops=dict(color=cs.INDIGO), boxprops=dict(color=cs.GRAY), whiskerprops=dict(color=cs.GRAY),
               capprops=dict(color=cs.GRAY))
    ax.axhline(50, color=cs.PALETTE["gray_light"], lw=0.8, ls=":", zorder=1)
    ax.set_xticks(range(1, 6))
    ax.set_xticklabels([f"{VV.CAT_SHORT[s]}\n(rated {len(d)})" for s, d in zip(VV.SUBS, data)], fontsize=8)
    ax.set_ylim(-2, 102)
    ax.set_ylabel("Cov* (0–100; 50 = situation-blind)", fontsize=9)
    ax.tick_params(labelsize=8.5)
    fig.subplots_adjust(top=0.80, bottom=0.17, left=0.10, right=0.97)
    _header(fig, 8, f"Panel {V['primary_panel']}, search off; rated brands (at least 14 mentions, named by at least "
                    f"two models).", "Box: median and interquartile range. Descriptive (pre-registration §5).")
    _save(fig, 8, "Cross-category baseline: descriptive, no verdict", V["prereg_tag"], out)


def main(argv=None):
    global WATERMARK
    ap = argparse.ArgumentParser(description="v1.12 Coverage Paper A figures")
    ap.add_argument("--verdicts", type=Path, default=ROOT / "osf/methodology/v1_12/v112_verdicts.json")
    ap.add_argument("--table", type=Path, default=ROOT / "osf/methodology/v1_12/v112_unit_table.csv")
    ap.add_argument("--out", type=Path, default=ROOT / "reports/figs/v112")
    ap.add_argument("--watermark", default=None)
    a = ap.parse_args(argv)
    src = VV.load_sources(a.verdicts, a.table)
    V, rows = src["verdicts"], src["table"]["rows"]
    if VV.is_synthetic(V) and not a.watermark:
        sys.exit("[v1.12 charts] REFUSED: synthetic verdicts need --watermark")
    if not VV.is_synthetic(V) and a.watermark:
        sys.exit("[v1.12 charts] REFUSED: --watermark is for synthetic runs only")
    WATERMARK = a.watermark
    pm = V["primary_panel"]
    print(f"building v1.12 figures -> {a.out}")
    chart_01(V, rows, a.out)
    chart_02(V, rows, a.out)
    scatter(V, rows, 3, "H1_Sep_Presence", "P_comparator", "cov_star", "Presence P_N3 (v0.42, t₄, search off; 0–100)",
            f"Cov* (panel {pm}; 0–100)", "Rated brands; Presence from the same models' t₄ answers (§2.5).", a.out,
            (-2, 102), (-2, 102))
    scatter(V, rows, 4, "H2_Sep_Consistency", "C_star_comparator", "cov_star",
            "Consistency C*_N3 (v0.42, t₄, search off; 0–100)", f"Cov* (panel {pm}; 0–100)",
            "Brands rated on both scores (C*: at least six t₄ recall mentions).", a.out, (-2, 102), (-2, 102))
    chart_05(V, rows, a.out)
    scatter(V, rows, 6, "H4_Reliability", "cov_star_A", "cov_star_B", "Cov* on half A (7 situations, one per cue type)",
            "Cov* on half B (the other 7)", "Each half refits its own situation effects; floor 7 mentions per half.",
            a.out, (-2, 102), (-2, 102), rated_only=False, diag=True)
    scatter(V, rows, 7, "H8_Panel_Replication", "cov_star_N3", "cov_star_C3",
            "Cov* on N3 (Claude Fable 5.2, GPT-6 Astra, Gemini 4 Argon)", "Cov* on C3 (Claude Opus 5.5 in place of Fable)",
            "Brands rated on both panels.", a.out, (-2, 102), (-2, 102), rated_only=False, diag=True)
    chart_08(V, rows, a.out)
    print("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
