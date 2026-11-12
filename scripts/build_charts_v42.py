#!/usr/bin/env python3
"""
v0.42 t4 cross-generation wave -- figure builder (paper and report registers).
Forked from build_charts_v41.py; house style via scripts/chart_style.py; every number from the scorer's outputs.

One chart per pre-registered finding (PRE_REGISTRATION_v0_42.md r2, sections 2.2-2.7):
  chart_01_presence_t3_t4   H_Gen_Presence    (PRIMARY)    report_fig_01 (P1)
  chart_02_phi_t3_t4        H_Gen_Phi         (SECONDARY)  report_fig_02 (P2)
  chart_03_search_s0_s1     H_Search_Presence (SECONDARY)  report_fig_03 (P3)
  chart_04_run_reliability  descriptive 1     (noise floor for t5)     report_fig_04 (P4)
  chart_05_floor            descriptive 3     (floor persistence)      report_fig_05 (P5)

Inputs: --verdicts (osf/v42/v42_verdicts.json) and --table (osf/v42/v42_brand_table.csv), both written by
score_v0_42.py. Nothing is re-scored or re-estimated here: points are the table's per-brand values, every statistic
printed on a chart is a verdicts-JSON leaf (formatted by papers/v0_42/v42_values.py). Chart titles describe what is
plotted and never repeat a finding's headline (CLAUDE.md, Report build).

Outputs: <out>/chart_0N_<topic>.pdf (+ _preview.png) and <report-out>/report_fig_0N.pdf.
--watermark TEXT stamps every chart (synthetic test runs only).

Usage (real run, after `score_v0_42.py --run`):
  python3 scripts/build_charts_v42.py
Synthetic test:
  python3 scripts/build_charts_v42.py --verdicts DIR/_score/v42_verdicts.json --table DIR/_score/v42_brand_table.csv \
      --out /tmp/t4_pipeline_test/figs --report-out /tmp/t4_pipeline_test/figs/report \
      --watermark "SYNTHETIC TEST — NOT RESULTS"
"""
import argparse
import math
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]          # the worktree / repository this script lives in
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "papers/v0_42"))
import chart_style as cs  # noqa: E402
import v42_values as VV  # noqa: E402
cs.setup()

SUBCOL = {"v0.19": cs.PALETTE["indigo"], "v0.20": cs.PALETTE["warm"], "v0.21": cs.PALETTE["teal_t2"],
          "v0.22": cs.PALETTE["blue"], "v0.23": cs.PALETTE["magenta"]}
MODECOL = {"S0": cs.INDIGO, "S1": cs.WARM}
SOURCE = ("Source: AIAS™ v0.42, t₄ wave | pre-registration {tag} | t₃: v0.41 (SSRN 7685100) | "
          "φ: Methodology v1.8 (SSRN 6963359) | Third System™")
MODE = "paper"
WATERMARK = None

META = {
    1: ("chart_01_presence_t3_t4", "report_fig_01"),
    2: ("chart_02_phi_t3_t4", "report_fig_02"),
    3: ("chart_03_search_s0_s1", "report_fig_03"),
    4: ("chart_04_run_reliability", "report_fig_04"),
    5: ("chart_05_floor", "report_fig_05"),
}

# Paper titles (academic) and report titles (managerial); both describe the plot, never a finding's headline.
TITLES = {
    1: ("Recall Presence per brand: retiring panel (t₃) and newest models (t₄, search off)",
        "Presence on the retiring models and on the newest models"),
    2: ("Consistency φ per brand: retiring panel (t₃) and newest models (t₄, search off)",
        "Consistency score on the retiring models and on the newest models"),
    3: ("Recall Presence per brand on the newest models, search off and search on (t₄)",
        "Presence with web search off and on"),
    4: ("Run-to-run reliability of recall, by model and condition (t₄)",
        "Agreement between repeated runs, by model"),
    5: ("Brands below the recall floor at t₃ and at t₄",
        "Brands below the recall floor, before and after the switch of models"),
}


def _tag(V):
    return V.get("prereg_tag", VV.EXPECTED_PREREG_TAG)


def _header(fig, key, subtitle, desc=""):
    title = TITLES[key][0 if MODE == "paper" else 1]
    cs.add_header(fig, title, subtitle, desc)
    h = fig.get_figheight()
    y = 1.0 - (0.74 / h)
    fig.add_artist(Line2D([cs.LEFT_X, 0.985], [y, y], transform=fig.transFigure, color=cs.INDIGO, lw=0.6))


def _footer(fig, verdict, tag):
    _, _, _, vy, sy = cs._compute_positions(fig)
    if verdict:
        fig.text(cs.LEFT_X, vy, verdict, fontsize=cs.FONT_SIZES["verdict"], color=cs.INDIGO,
                 fontstyle="italic", ha="left", va="bottom")
    fig.text(cs.LEFT_X, sy, SOURCE.format(tag=tag), fontsize=cs.FONT_SIZES["source"], color=cs.GRAY,
             fontstyle="italic", ha="left", va="bottom")
    if WATERMARK:
        fig.text(0.5, 0.5, WATERMARK, rotation=28, fontsize=30, color=cs.WARM, alpha=0.22, ha="center",
                 va="center", fontweight="bold", zorder=100)


def _save(fig, key, verdict, tag, out_dirs):
    if MODE == "paper" and key in (1, 2, 3):
        verdict = None   # a paper chart never repeats a finding's headline; the verdict is in the text (Nov 11)
    _footer(fig, verdict, tag)
    name = META[key][0 if MODE == "paper" else 1]
    d = out_dirs[MODE]
    d.mkdir(parents=True, exist_ok=True)
    fig.savefig(d / f"{name}.pdf", **cs.SAVEFIG_PARAMS)
    if MODE == "paper":
        fig.savefig(d / f"{name}_preview.png", dpi=110, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    print(f"  [{MODE}] wrote {d / (name + '.pdf')}")


def _box(ax, text, x=0.03, y=0.97, ha="left", va="top", fs=7.8):
    ax.text(x, y, text, transform=ax.transAxes, ha=ha, va=va, fontsize=fs, color=cs.INDIGO,
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=cs.INDIGO, lw=0.6), zorder=5)


def _rows(rows, xcol, ycol):
    out = {s: ([], []) for s in VV.SUBS}
    for r in rows:
        x, y = VV.fnum(r.get(xcol)), VV.fnum(r.get(ycol))
        if x is not None and y is not None and math.isfinite(x) and math.isfinite(y):
            out[r["substrate"]][0].append(x)
            out[r["substrate"]][1].append(y)
    return out


def _status(case, register):
    return (VV.PAPER_STATUS if register == "paper" else VV.REPORT_STATUS)[case]


# ============================================================ 1. H_Gen_Presence
def chart_01(V, rows, out_dirs):
    h = V["verdicts"]["H_Gen_Presence"]
    case = VV.case_gen(V)
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    pts = _rows(rows, "t3_pi_hat", "pi_N3_S0")
    ax.plot([0, 1], [0, 1], color=cs.PALETTE["gray_light"], lw=0.8, ls="--", zorder=1)
    for s in VV.SUBS:
        x, y = pts[s]
        ax.scatter(x, y, s=30, color=SUBCOL[s], alpha=0.85, edgecolor="white", linewidth=0.4, zorder=3,
                   label=f"{s} {VV.CAT[s]} (n = {len(x)})")
    ax.set_xlim(-0.02, 1.02); ax.set_ylim(-0.02, 1.02)
    ax.set_xlabel("recall Presence π̂ at t₃, six retiring models (9 Nov 2026)", fontsize=9)
    ax.set_ylabel("recall Presence π̂ at t₄, newest models, search off", fontsize=9)
    ax.tick_params(labelsize=8.5)
    ax.legend(loc="lower right", fontsize=7.4, frameon=False)
    if case in ("CONFIRMED", "MARGINAL", "FALSIFIED"):
        txt = (f"ρ_pw = {VV.r3(h['rho'])}   95% interval [{VV.r3(h['ci95_rho'][0])}, {VV.r3(h['ci95_rho'][1])}]\n"
               f"p_perm = {VV.p4(h['p_perm'])}   n = {h['n']}\n"
               f"level shift (t₄ minus t₃) = {VV.sr3(h['delta'])}  [{VV.sr3(h['ci95_delta'][0])}, {VV.sr3(h['ci95_delta'][1])}]\n"
               "pre-registered bars: confirm at least 0.70 with p < .05; falsify below 0.50")
        verdict = (f"H_Gen_Presence: {case} — ρ_pw = {VV.r3(h['rho'])} (n = {h['n']}), p_perm = {VV.p4(h['p_perm'])}"
                   if MODE == "paper" else f"P1 {_status(case, 'report')} — rank correlation {VV.r2(h['rho'])} across {h['n']} brands")
    else:
        why = (f"{VV.names(VV.excluded_models(V, 'S0'))} below 90% of calls answered (drop rule)"
               if case == "UNDETERMINED_EXCLUDED" else "statistic undefined (degenerate data)")
        txt = f"UNDETERMINED: {why}"
        verdict = (f"H_Gen_Presence: UNDETERMINED — {why}" if MODE == "paper"
                   else f"P1 {_status(case, 'report')} — {why}")
    if MODE == "report" and case in ("CONFIRMED", "MARGINAL", "FALSIFIED"):
        txt = (f"rank correlation {VV.r2(h['rho'])} across {h['n']} brands\n"
               f"plausible range {VV.r2(h['ci95_rho'][0])} to {VV.r2(h['ci95_rho'][1])}\n"
               "registered bar: 0.70 to call the order the same; below 0.50, different")
    _box(ax, txt)
    fig.subplots_adjust(top=0.80, bottom=0.17, left=0.10, right=0.97)
    if MODE == "paper":
        _header(fig, 1, "Per-brand share of category answers that name the brand; 112 brands, five categories; "
                        "t₄ = mean of three runs.",
                "ρ_pw: Spearman on within-category ranks centred per category (decision statistic, C25). "
                "Dashed: equal values.")
    else:
        _header(fig, 1, "Share of category answers naming each brand: six retiring models (9 Nov) vs the newest "
                        "model of each provider.", "Each dot is one brand. On the dashed line, its share is the same.")
    _save(fig, 1, verdict, _tag(V), out_dirs)


# ============================================================ 2. H_Gen_Phi
def chart_02(V, rows, out_dirs):
    h = V["verdicts"]["H_Gen_Phi"]
    case = VV.case_phi(V)
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    pts = _rows(rows, "t3_phi", "phi_N3_S0")
    allv = [v for s in VV.SUBS for v in pts[s][0] + pts[s][1]]
    lim = max(1.0, math.ceil(2 * max(allv) * 1.04) / 2) if allv else 1.0
    ax.plot([0, lim], [0, lim], color=cs.PALETTE["gray_light"], lw=0.8, ls="--", zorder=1)
    for s in VV.SUBS:
        x, y = pts[s]
        ax.scatter(x, y, s=30, color=SUBCOL[s], alpha=0.85, edgecolor="white", linewidth=0.4, zorder=3,
                   label=f"{s} {VV.CAT[s]} (n = {len(x)})")
    ax.set_xlim(0, lim); ax.set_ylim(0, lim)
    ax.set_xlabel("φ at t₃, six retiring models   (lower = models agree more)", fontsize=9)
    ax.set_ylabel("φ at t₄, newest models, search off (mean of runs)", fontsize=9)
    ax.tick_params(labelsize=8.5)
    ax.legend(loc="upper right", fontsize=7.4, frameon=False)
    pc = (h.get("reported_alongside") or {}).get("partition_counts", {}).get("N3_S0", {}).get("brand_level")
    pc_txt = (f"\nt₄ brands: {pc['defined']} defined, {pc['zero']} zero, {pc['saturated']} saturated, "
              f"{pc['undefined']} undefined" if pc else "")
    if case in ("CONFIRMED", "MARGINAL", "FALSIFIED"):
        txt = (f"ρ_pw = {VV.r3(h['rho'])}   95% interval [{VV.r3(h['ci95_rho'][0])}, {VV.r3(h['ci95_rho'][1])}]\n"
               f"p_perm = {VV.p4(h['p_perm'])}   n = {h['n']} (φ defined in both waves)\n"
               "pre-registered bars: confirm at least 0.50 with p < .05; falsify below 0.30; n at least 40" + pc_txt)
        verdict = (f"H_Gen_Phi: {case} — ρ_pw = {VV.r3(h['rho'])} (n = {h['n']}), p_perm = {VV.p4(h['p_perm'])}"
                   if MODE == "paper" else f"P2 {_status(case, 'report')} — rank correlation {VV.r2(h['rho'])} across {h['n']} brands")
    else:
        if case == "UNDETERMINED_FLOOR":
            why = f"n = {h['n']} brands with φ defined in both waves, below the floor of 40"
        elif case == "UNDETERMINED_EXCLUDED":
            why = f"{VV.names(VV.excluded_models(V, 'S0'))} below 90% of calls answered (drop rule)"
        else:
            why = "statistic undefined (degenerate data)"
        txt = f"UNDETERMINED: {why}" + pc_txt
        verdict = (f"H_Gen_Phi: UNDETERMINED — {why}" if MODE == "paper"
                   else f"P2 {_status(case, 'report')} — {why}")
    if MODE == "report" and case in ("CONFIRMED", "MARGINAL", "FALSIFIED"):
        txt = (f"rank correlation {VV.r2(h['rho'])} across {h['n']} brands scored on both\n"
               f"plausible range {VV.r2(h['ci95_rho'][0])} to {VV.r2(h['ci95_rho'][1])}\n"
               "registered bar: 0.50; below 0.30 counts as a change")
    _box(ax, txt)
    fig.subplots_adjust(top=0.80, bottom=0.17, left=0.10, right=0.97)
    if MODE == "paper":
        _header(fig, 2, "Per-brand φ (v1.8 between-model dispersion; higher = less consistent), brands with "
                        "φ defined at t₃ and t₄.",
                "t₄ φ: mean over runs with a defined partition (at least 2 of 3). Dashed: equal values.")
    else:
        _header(fig, 2, "How much the models disagree about each brand: retiring models vs newest models "
                        "(lower = more agreement).", "Brands scored on both panels. On the dashed line, the score is the same.")
    _save(fig, 2, verdict, _tag(V), out_dirs)


# ============================================================ 3. H_Search_Presence
def chart_03(V, rows, out_dirs):
    h = V["verdicts"]["H_Search_Presence"]
    case = VV.case_search(V)
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(7.5, 4.6), gridspec_kw={"width_ratios": [1.0, 1.15]})
    pts = _rows(rows, "pi_N3_S0", "pi_N3_S1")
    ax.plot([0, 1], [0, 1], color=cs.PALETTE["gray_light"], lw=0.8, ls="--", zorder=1)
    for s in VV.SUBS:
        x, y = pts[s]
        ax.scatter(x, y, s=20, color=SUBCOL[s], alpha=0.85, edgecolor="white", linewidth=0.4, zorder=3,
                   label=VV.CAT_SHORT[s])
    ax.set_xlim(-0.02, 1.02); ax.set_ylim(-0.02, 1.02)
    ax.set_xlabel("π̂, search off (S0)" if MODE == "paper" else "Presence, search off", fontsize=8.5)
    ax.set_ylabel("π̂, search on (S1)" if MODE == "paper" else "Presence, search on", fontsize=8.5)
    ax.tick_params(labelsize=7.5)
    ax.legend(loc="upper left", fontsize=6.8, frameon=False, handletextpad=0.2)
    labels, vals, cis, cols = [], [], [], []
    if case != "NOT_COMPUTED" and VV.has(h, ["rho"]):
        labels.append("all models (ρ_S)" if MODE == "paper" else "all models"); vals.append(h["rho"])
        cis.append(h.get("ci95_rho")); cols.append(cs.INDIGO)
        for m, d in (h.get("per_model") or {}).items():
            if VV.has(d, ["rho"]):
                labels.append(VV.MODEL_NAME.get(m, m)); vals.append(d["rho"]); cis.append(None); cols.append(cs.PALETTE["indigo_t1"])
        for s in VV.SUBS:
            d = (h.get("per_substrate") or {}).get(s)
            if d and VV.has(d, ["rho"]):
                labels.append(VV.CAT_SHORT[s]); vals.append(d["rho"]); cis.append(None); cols.append(SUBCOL[s])
    ys = np.arange(len(labels))[::-1]
    lo_x = min([0.0] + [v - 0.05 for v in vals] + [c[0] - 0.05 for c in cis if c])
    bx.axvspan(0.80, 1.05, color=cs.PALETTE["indigo_t3"], alpha=0.35, zorder=0)
    bx.axvspan(lo_x, 0.50, color=cs.PALETTE["warm_t3"], alpha=0.35, zorder=0)
    for y, v, c, col in zip(ys, vals, cis, cols):
        if c:
            bx.plot(c, [y, y], color=col, lw=2.2, zorder=2, solid_capstyle="butt")
        bx.plot([v], [y], "o", color=col, ms=5.5, zorder=3)
        # paper: three decimals, as Table 5 and section 3.4 print them
        bx.text(1.06, y, (VV.r3 if MODE == "paper" else VV.r2)(v), va="center", ha="left", fontsize=7, color=col,
                clip_on=False)
    bx.set_yticks(ys); bx.set_yticklabels(labels, fontsize=7.4)
    bx.set_xlim(lo_x, 1.05); bx.set_ylim(-0.6, max(len(labels), 1) + 0.9)
    bx.set_xlabel("rank correlation, search off vs on", fontsize=8.5); bx.tick_params(axis="x", labelsize=7.5)
    bx.text(0.81, len(labels) - 0.35, "robust zone:\nlower bound\nat least 0.80", fontsize=6.4, color=cs.INDIGO, va="bottom")
    bx.text(lo_x + 0.01, len(labels) - 0.35, "dominated zone:\nupper bound < 0.50", fontsize=6.4, color=cs.PALETTE["warm_sec"], va="bottom")
    if case in ("ROBUST", "SENSITIVE", "DOMINATED"):
        lab = h["label"]
        verdict = (f"H_Search_Presence: {lab} — ρ_S = {VV.r3(h['rho'])}, 95% interval "
                   f"[{VV.r3(h['ci95_rho'][0])}, {VV.r3(h['ci95_rho'][1])}], level shift = {VV.sr3(h['delta'])}"
                   + ("; reduced panel" if h.get("reduced_panel") else "")
                   if MODE == "paper" else
                   f"P3 {_status(case, 'report')} — rank correlation {VV.r2(h['rho'])} between search off and on")
    else:
        why = "no model retained in both conditions" if case == "NOT_COMPUTED" else "no interval (degenerate data)"
        bx.text(0.5, 0.5, f"not computed: {why}", transform=bx.transAxes, ha="center", fontsize=8, color=cs.GRAY)
        verdict = (f"H_Search_Presence: {case.replace('_', ' ')} — {why}" if MODE == "paper"
                   else f"P3 {_status(case, 'report')} — {why}")
    fig.subplots_adjust(top=0.78, bottom=0.19, left=0.08, right=0.93, wspace=0.42)
    if MODE == "paper":
        _header(fig, 3, "Left: per-brand π̂ (mean of three runs). Right: ρ_S with its 95% bootstrap "
                        "interval; per model and per category (points).",
                "Pre-declared reading: robust if the interval's lower bound is at least 0.80; dominated if its upper "
                "bound < 0.50; sensitive otherwise.")
    else:
        _header(fig, 3, "Each brand's Presence on the newest models without and with their own web search.",
                "Right: how closely the two brand orders agree, overall (with its range) and per model and category.")
    _save(fig, 3, verdict, _tag(V), out_dirs)


# ============================================================ 4. descriptive 1 (run-to-run reliability)
def chart_04(V, rows, out_dirs):
    rel = V["descriptives"]["1_run_reliability"]
    fig, ax = plt.subplots(figsize=(7.5, 3.9))
    ys = np.arange(len(VV.N3))[::-1]
    for y, m in zip(ys, VV.N3):
        for j, c in enumerate(("S0", "S1")):
            d = rel.get(f"{m}|{c}") or {}
            off = 0.14 if c == "S0" else -0.14
            if VV.has(d, ["rel1"]):
                ax.plot([d["rel1"]], [y + off], "o", color=MODECOL[c], ms=6.5, zorder=3)
                ax.text(d["rel1"], y + off + (0.09 if c == "S0" else -0.09),
                        (VV.r3 if MODE == "paper" else VV.r2)(d["rel1"]), fontsize=6.6,       # paper: as Table 6
                        color=MODECOL[c], ha="center", va="bottom" if c == "S0" else "top")
            if VV.has(d, ["rel3"]):
                ax.plot([d["rel3"]], [y + off], "o", mfc="white", mec=MODECOL[c], ms=6.5, zorder=3)
            if VV.has(d, ["rel1"]) and VV.has(d, ["rel3"]):
                ax.plot([d["rel1"], d["rel3"]], [y + off, y + off], color=MODECOL[c], lw=0.8, zorder=2)
    ax.set_yticks(ys); ax.set_yticklabels([VV.MODEL_NAME[m] for m in VV.N3], fontsize=8.5)
    vals = [d.get(k) for d in rel.values() for k in ("rel1", "rel3") if VV.has(d, [k])]
    lo = min([0.0] + [v - 0.05 for v in vals])
    ax.set_xlim(lo, 1.04); ax.set_ylim(-0.6, len(VV.N3) - 0.4)
    ax.set_xlabel("rank correlation of recall between runs (ρ_pw)" if MODE == "paper"
                  else "agreement between repeated runs (1 = identical brand order)", fontsize=8.5)
    ax.tick_params(axis="x", labelsize=8)
    handles = [Line2D([], [], marker="o", ls="", color=MODECOL["S0"], label="search off: one run (rel1)" if MODE == "paper" else "search off, one run"),
               Line2D([], [], marker="o", ls="", color=MODECOL["S1"], label="search on: one run (rel1)" if MODE == "paper" else "search on, one run"),
               Line2D([], [], marker="o", ls="", mfc="white", mec=cs.GRAY, label="mean of three runs (rel3)" if MODE == "paper" else "average of three runs")]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.42, -0.24), ncol=3, fontsize=7.2, frameon=False)
    fig.subplots_adjust(top=0.74, bottom=0.30, left=0.17, right=0.97)
    if MODE == "paper":
        _header(fig, 4, "rel1 = mean ρ_pw over the three run pairs of k/6; rel3 = 3·rel1/(1 + 2·rel1). "
                        "Descriptive; no verdict.", "The noise floor against which the t₅ and t₆ waves will be read.")
        verdict = "Descriptive 1 (pre-registered, section 2.7): run-to-run reliability of recall per model × condition"
    else:
        _header(fig, 4, "How alike the brand order is when the same model answers the same questions again.",
                "Filled dots: one run against another. Open dots: the average of three runs, which the scores use.")
        verdict = f"P4 {VV.REPORT_STATUS['DESCRIPTIVE']} — descriptive; no pass mark was set"
    _save(fig, 4, verdict, _tag(V), out_dirs)


# ============================================================ 5. descriptive 3 (floor persistence)
def chart_05(V, rows, out_dirs):
    d = V["descriptives"]["3_floor_persistence"]
    fig, ax = plt.subplots(figsize=(7.5, 3.7))
    if d.get("status") == "NOT_COMPUTED":
        ax.axis("off")
        ax.text(0.5, 0.5, "not computed: a model was excluded in search off (drop rule)", ha="center",
                transform=ax.transAxes, fontsize=9, color=cs.GRAY)
    else:
        b3, b4, both = d["below_floor_t3"], d["below_floor_t4"], d["below_both"]
        lab3 = "below at t₃" if MODE == "paper" else "below on the retiring models"
        lab4 = "below at t₄" if MODE == "paper" else "below on the newest models"
        ax.barh(1, both, color=cs.INDIGO, height=0.5, zorder=2)
        ax.barh(1, b3 - both, left=both, color=cs.PALETTE["indigo_t3"], height=0.5, zorder=2)
        ax.barh(0, both, color=cs.INDIGO, height=0.5, zorder=2)
        ax.barh(0, b4 - both, left=both, color=cs.WARM, height=0.5, zorder=2)
        ax.text(b3 + 0.6, 1, f"{both} of {b3} still below at t₄" if MODE == "paper" else f"{both} of {b3} still below",
                va="center", fontsize=8, color=cs.INDIGO)
        ax.text(b4 + 0.6, 0, f"{b4 - both} of {b4} were above at t₃" if MODE == "paper" else f"{b4 - both} of {b4} were above before",
                va="center", fontsize=8, color=cs.INDIGO)
        ax.set_yticks([1, 0]); ax.set_yticklabels([lab3, lab4], fontsize=8.5)
        ax.set_xlim(0, max(b3, b4) * 1.45 + 1); ax.set_ylim(-0.6, 1.6)
        ax.set_xlabel("brands (of 112)", fontsize=8.5); ax.tick_params(axis="x", labelsize=8)
        ax.legend(handles=[Patch(color=cs.INDIGO, label="below the floor on both panels"),
                           Patch(color=cs.PALETTE["indigo_t3"], label="below at t₃ only" if MODE == "paper" else "below on the retiring models only"),
                           Patch(color=cs.WARM, label="below at t₄ only" if MODE == "paper" else "below on the newest models only")],
                  loc="upper center", bbox_to_anchor=(0.45, -0.3), ncol=3, fontsize=7.2, frameon=False)
    fig.subplots_adjust(top=0.74, bottom=0.33, left=0.20, right=0.97)
    if MODE == "paper":
        _header(fig, 5, "Floor: t₃, mean k per model < 1 (v0.41's rule); t₄, mean k per model-run < 1 "
                        "(newest models, search off).", "Descriptive 3 (section 2.7, clarification C2); no verdict.")
        verdict = "Descriptive 3 (pre-registered, section 2.7): floor persistence from t₃ to t₄"
    else:
        _header(fig, 5, "Brands named less than once per model on average, on the retiring models and on the newest "
                        "models.", "Descriptive: no pass mark was set.")
        verdict = f"P5 {VV.REPORT_STATUS['DESCRIPTIVE']} — descriptive; no pass mark was set"
    _save(fig, 5, verdict, _tag(V), out_dirs)


def main(argv=None):
    global MODE, WATERMARK
    ap = argparse.ArgumentParser(description="v0.42 figures (paper and report registers)")
    ap.add_argument("--verdicts", type=Path, default=ROOT / "osf/v42/v42_verdicts.json")
    ap.add_argument("--table", type=Path, default=ROOT / "osf/v42/v42_brand_table.csv")
    ap.add_argument("--out", type=Path, default=ROOT / "reports/figs/v42")
    ap.add_argument("--report-out", type=Path, default=ROOT / "reports/figs/v42/report")
    ap.add_argument("--watermark", default=None)
    a = ap.parse_args(argv)
    src = VV.load_sources(a.verdicts, a.table)
    V, rows = src["verdicts"], src["table"]["rows"]
    if VV.is_synthetic(V) and not a.watermark:
        sys.exit("[v42 charts] REFUSED: synthetic verdicts (MC_Parity SKIPPED_SYNTHETIC) need --watermark")
    WATERMARK = a.watermark
    dirs = {"paper": a.out, "report": a.report_out}
    print(f"building v0.42 figures -> {a.out} and {a.report_out}")
    for m in ("paper", "report"):
        MODE = m
        for fn in (chart_01, chart_02, chart_03, chart_04, chart_05):
            fn(V, rows, dirs)
    print("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
