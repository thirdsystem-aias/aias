#!/usr/bin/env python3
"""
v1.13 Grounding Paper A -- figure builder (paper register only: Paper A is not a milestone, so no brand-format report).
House style of build_charts_v112.py (scripts/chart_style.py: bold title top-left, gray subtitle, thin Indigo rule,
italic gray source line citing the pre-registration tag). Every number from the scorers' outputs.

One chart per pre-registered finding (PRE_REGISTRATION_v1_13.md sections 3, 4 and 6):
  chart_01_search_use          RQ1 / MQ2: how often each model's search returned sources (baseline)
  chart_02_source_mix          RQ2: the source-type mix per category and model (baseline)
  chart_03_gstar_by_category   RQ2: the distribution of G* (baseline)
  chart_04_presence_legs       H1_Sep_Presence, primary and every sensitivity (S1-S11, S8 per category)
  chart_05_consistency_legs    H2_Sep_Consistency, the same
  chart_06_run_pairs           H3_Run_Reliability
  chart_07_legs_bands          the gate: every computed leg (H1-H4, H6, H7) against its bands
  chart_08_sdri_gstar          H7_Struct_Gap (only when Part II was collected)

Inputs: --verdicts (osf/methodology/v1_13/v1_13_verdicts.json, score_v1_13.py --stage C1 then C2) and, for chart 8,
--sdri (osf/methodology/v1_13/audit/v1_13_sdri.csv, audit_v1_13.py --sdri). Nothing is re-scored: points are the
files' values; every statistic printed on a chart is a leaf formatted by papers/v1_13/v113_values.py. Chart titles
describe what is plotted and never repeat a finding's or a section's title (CLAUDE.md). --watermark TEXT stamps every
chart (synthetic runs only; required for them).

Usage (real run):  python3 scripts/build_charts_v113.py
Synthetic test:    python3 scripts/build_charts_v113.py --verdicts F.json [--sdri F.csv] --out /tmp/x/figs \
                       --watermark "SYNTHETIC TEST — NOT RESULTS"
"""
import argparse
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "papers/v1_13"))
import chart_style as cs  # noqa: E402
import v113_values as VV  # noqa: E402
import v118_section as V118  # noqa: E402
cs.setup()

SUBCOL = {"v19": cs.PALETTE["indigo"], "v20": cs.PALETTE["warm"], "v21": cs.PALETTE["teal_t2"],
          "v22": cs.PALETTE["blue"], "v23": cs.PALETTE["magenta"]}
MODCOL = {VV.S.FABLE: cs.PALETTE["indigo"], VV.S.GPT6: cs.PALETTE["teal_t2"], VV.S.GEM4: cs.PALETTE["warm"]}
CLASSCOL = {"brand_owned": cs.PALETTE["indigo"], "reference": cs.PALETTE["indigo_t2"],
            "review_editorial": cs.PALETTE["teal_t2"], "retailer": cs.PALETTE["blue_t2"], "news": cs.PALETTE["warm_t2"],
            "forum_ugc": cs.PALETTE["magenta"], "other": cs.PALETTE["gray_light"], "unresolved": cs.PALETTE["gray"]}
SOURCE = ("Source: AIAS™ Methodology v1.13, Grounding Paper A | pre-registration {tag} | answers: v0.42 (t₄, search "
          "on) | Third System™")
TAG = VV.PREREG_TAG
WATERMARK = None
TITLES = {
    1: "Share of category answers whose search returned at least one source",
    2: "Source types in the search records, per category and model",
    3: "G* per rated brand, by category",
    4: "Rank correlation of G* with Presence under each analysis",
    5: "Rank correlation of G* with Consistency under each analysis",
    6: "Per-run G* compared between pairs of runs",
    7: "Every computed leg against its pre-registered bands",
    8: "Structured-data richness and G* per brand",
    9: "Program share of cited domains under four definitions, with 90% intervals",
}
NAMES = {1: "chart_01_search_use", 2: "chart_02_source_mix", 3: "chart_03_gstar_by_category",
         4: "chart_04_presence_legs", 5: "chart_05_consistency_legs", 6: "chart_06_run_pairs",
         7: "chart_07_legs_bands", 8: "chart_08_sdri_gstar", 9: "chart_09_v118_definitions"}
SOURCE_V118 = ("Source: AIAS™ Methodology v1.18 (exploratory) | pre-registration v1.18-prereg-r1 | answers: v0.42 (t₄, "
               "search on) | Third System™")
SENS_LABEL = dict(VV.SENS)


def _header(fig, key, subtitle, desc=""):
    cs.add_header(fig, TITLES[key], subtitle, desc)
    y = 1.0 - (0.74 / fig.get_figheight())
    fig.add_artist(Line2D([cs.LEFT_X, 0.985], [y, y], transform=fig.transFigure, color=cs.INDIGO, lw=0.6))


def _save(fig, key, verdict, out, source=None):
    _, _, _, vy, sy = cs._compute_positions(fig)
    if verdict:
        fig.text(cs.LEFT_X, vy, verdict, fontsize=cs.FONT_SIZES["verdict"], color=cs.INDIGO, fontstyle="italic",
                 ha="left", va="bottom")
    fig.text(cs.LEFT_X, sy, source or SOURCE.format(tag=TAG), fontsize=cs.FONT_SIZES["source"], color=cs.GRAY,
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


def _models(V):
    return [m for m in VV.MODELS if any(k.endswith("|" + m) for k in V["baseline"]["per_substrate_model"])]


def chart_01(V, out):
    psm = V["baseline"]["per_substrate_model"]
    models = _models(V)
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    w = 0.8 / max(1, len(models))
    for j, m in enumerate(models):
        xs, ys = [], []
        for i, s in enumerate(VV.SUBS):
            r = psm.get(f"{s}|{m}")
            if r:
                xs.append(i + (j - (len(models) - 1) / 2) * w)
                ys.append(100 * r["share_with_source"])
        ax.bar(xs, ys, width=w * 0.92, color=MODCOL[m], label=VV.MODEL_NAME[m], zorder=3)
    ax.axhline(25, color=cs.WARM, lw=0.8, ls=":", zorder=2)
    ax.axhline(10, color=cs.WARM, lw=0.8, ls="--", zorder=2)
    ax.set_xticks(range(len(VV.SUBS)))
    ax.set_xticklabels([VV.CAT_SHORT[s] for s in VV.SUBS], fontsize=8.5)
    ax.set_ylim(0, 105)
    ax.set_ylabel("answers with at least one source (%)", fontsize=9)
    ax.tick_params(labelsize=8.5)
    ax.legend(loc="center left", bbox_to_anchor=(1.01, 0.5), fontsize=7.4, frameon=False)
    fig.subplots_adjust(top=0.80, bottom=0.17, left=0.10, right=0.80)
    _header(fig, 1, "Search-on category answers of the three N3 models (baseline, pre-registration §6).",
            "Dotted: 25%, below which MQ2 flags a model; dashed: 10%, below which it leaves the primary score.")
    q = V["MQ"]["MQ2"]
    _save(fig, 1, "MQ2 per model: " + "; ".join(f"{VV.MODEL_NAME[m]} {VV.pct1(q[m]['share'])}" for m in VV.MODELS
                                              if q.get(m) and q[m].get("share") is not None), out)


def chart_02(V, out):
    psm = V["baseline"]["per_substrate_model"]
    models = _models(V)
    labels, rows = [], []
    for s in VV.SUBS:
        for m in models:
            r = psm.get(f"{s}|{m}")
            if r:
                labels.append(f"{VV.CAT_SHORT[s]} · {VV.MODEL_NAME[m]}")
                rows.append(r["mix"])
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero_tall"])
    ys = list(range(len(rows)))[::-1]
    left = [0.0] * len(rows)
    for c in VV.CLASSES:
        vals = [100 * (r.get(c) or 0.0) for r in rows]
        ax.barh(ys, vals, left=left, color=CLASSCOL[c], height=0.72, label=VV.CLASS_NAME[c], zorder=3,
                edgecolor="white", linewidth=0.3)
        left = [a + b for a, b in zip(left, vals)]
    ax.set_yticks(ys)
    ax.set_yticklabels(labels, fontsize=7.2)
    ax.set_xlim(0, 100)
    ax.set_xlabel("mean share of an answer's distinct resolved domains (%)", fontsize=9)
    ax.tick_params(axis="x", labelsize=8.5)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.09), ncol=4, fontsize=7.2, frameon=False)
    fig.subplots_adjust(top=0.86, bottom=0.17, left=0.30, right=0.97)
    _header(fig, 2, "Each answer weighs one; classes by the frozen rule of source_classes_v1_13.md (§2.3).",
            "Baseline descriptive (§6); no verdict rests on the mix.")
    mq3 = V["MQ"]["MQ3"]
    _save(fig, 2, f"MQ3: {VV.pct1(mq3['share'])} of (answer, domain) pairs other or unresolved"
          + (" — low coverage" if mq3.get("low_coverage") else ""), out)


def chart_03(V, out):
    units = V["units"]
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    data = []
    for i, s in enumerate(VV.SUBS):
        v = sorted(u["G_star"] for k, u in units.items() if k.split("|")[0] == s and u["rated"])
        data.append(v)
        ax.scatter([i + 1 + 0.16 * ((j % 5) - 2) / 2 for j in range(len(v))], v, s=16, color=SUBCOL[s], alpha=0.8,
                   edgecolor="white", linewidth=0.3, zorder=3)
    ax.boxplot([d if d else [float("nan")] for d in data], widths=0.5, showfliers=False,
               medianprops=dict(color=cs.INDIGO), boxprops=dict(color=cs.GRAY), whiskerprops=dict(color=cs.GRAY),
               capprops=dict(color=cs.GRAY))
    ax.set_xticks(range(1, 6))
    ax.set_xticklabels([f"{VV.CAT_SHORT[s]}\n(rated {len(d)})" for s, d in zip(VV.SUBS, data)], fontsize=8)
    ax.set_ylim(-3, 103)
    ax.set_ylabel("G* (0–100)", fontsize=9)
    ax.tick_params(labelsize=8.5)
    fig.subplots_adjust(top=0.80, bottom=0.17, left=0.10, right=0.97)
    _header(fig, 3, "Primary panel; rated brands (at least six grounded answers and an own domain).",
            "G* = 100 × answers whose sources include the brand's own domain / grounded answers naming it (§2.4).")
    _save(fig, 3, f"MQ5: {VV.pct0(V['MQ']['MQ5']['zero_share'])} of rated brands at 0 "
          f"({'failed' if V['MQ']['MQ5']['failed'] else 'passed'})", out)


def _sens_rows(V, h):
    """[(label, rho_S1, rho_S0, ci_S1, ci_S0, kind)] for the primary analysis and every sensitivity."""
    legs = V["legs"][h]
    ci = [(l.get("ci90") or {}) for l in legs]
    rows = [("Primary", legs[0].get("rho_w"), legs[1].get("rho_w"), ci[0], ci[1], "primary")]
    SN = V.get("sensitivities") or {}
    for key, label in VV.SENS:
        if key in SN and h in SN[key].get("rho", {}):
            r = SN[key]["rho"][h]
            rows.append((label, r[0], r[1], None, None, "sens"))          # $...$ rendered by mathtext
    lo = SN.get("S8_leave_one_substrate_out") or {}
    for s in VV.SUBS:
        if s in lo:
            r = lo[s]["rho"][h]
            rows.append((f"S8 without {VV.CAT_SHORT[s].lower()}", r[0], r[1], None, None, "s8"))
    return rows


def chart_sep(V, key, h, comp, out):
    rows = _sens_rows(V, h)
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero_tall"])
    ax.axvspan(-0.30, 0.30, color=cs.PALETTE["indigo_t3"], alpha=0.35, zorder=0)
    for x in (-0.5, 0.5):
        ax.axvline(x, color=cs.WARM, lw=0.8, ls=":", zorder=1)
    ax.axvline(0, color=cs.PALETTE["gray_light"], lw=0.8, zorder=1)
    n = len(rows)
    for i, (lab, r1, r0, c1, c0, kind) in enumerate(rows):
        y = n - i
        for r, c, dy, col, mk in ((r1, c1, 0.15, cs.INDIGO, "o"), (r0, c0, -0.15, cs.WARM, "s")):
            if r is None:
                continue
            if c and c.get("lo") is not None:
                ax.plot([c["lo"], c["hi"]], [y + dy, y + dy], color=col, lw=1.4, zorder=2)
            ax.scatter([r], [y + dy], s=30 if kind == "primary" else 18, color=col, marker=mk, zorder=3)
    ax.set_yticks([n - i for i in range(n)])
    ax.set_yticklabels([r[0] for r in rows], fontsize=7.6)
    ax.set_ylim(0.3, n + 0.7)
    ax.set_xlim(-1, 1)
    ax.set_xlabel(f"pooled within-category ρ_w of G* with {comp}", fontsize=9)
    ax.tick_params(axis="x", labelsize=8.5)
    ax.legend(handles=[Line2D([], [], color=cs.INDIGO, marker="o", ls="", label=f"{comp}, search on (S1)"),
                       Line2D([], [], color=cs.WARM, marker="s", ls="", label=f"{comp}, search off (S0)")],
              loc="upper center", bbox_to_anchor=(0.5, -0.07), ncol=2, fontsize=7.4, frameon=False)
    fig.subplots_adjust(top=0.86, bottom=0.14, left=0.27, right=0.97)
    _header(fig, key, "Primary with its 90% bootstrap interval; sensitivities (§7) and leave-one-category-out (S8) "
                      "as points.", "Shaded: |ρ_w| at most 0.30 (separable). Dotted: |ρ_w| = 0.50.")
    _save(fig, key, f"{h}: {V['verdicts'][h]}", out)


def chart_06(V, out):
    h3 = V["H3"]
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    labs, vals, cols = [], [], []
    for pr in h3["pairs"]:
        labs.append(f"runs {pr['pair'][0]} and {pr['pair'][1]}\n(n = {pr['n']})")
        vals.append(pr["rho_w"] if pr["rho_w"] is not None else 0.0)
        cols.append(cs.INDIGO if pr["qualifies"] else cs.PALETTE["gray_light"])
    ax.bar(range(len(vals)), vals, color=cols, width=0.55, zorder=3)
    ax.axhline(0.25, color=cs.WARM, lw=0.8, ls=":", zorder=2)
    ax.axhline(0.125, color=cs.WARM, lw=0.8, ls="--", zorder=2)
    ax.axhline(0, color=cs.PALETTE["gray_light"], lw=0.8, zorder=1)
    ax.set_xticks(range(len(vals)))
    ax.set_xticklabels(labs, fontsize=8.5)
    ax.set_ylim(min(-0.1, min(vals) - 0.05), 1.0)
    ax.set_ylabel("ρ_w of per-run G* (rated in both runs)", fontsize=9)
    ax.tick_params(labelsize=8.5)
    txt = f"qualifying pairs: {h3['n_qualifying_pairs']} of 3"
    if h3.get("rel1") is not None:
        txt += f"\nrel1 = {VV.r3(h3['rel1'])}   rel3 = {VV.r3(h3['rel3'])}"
    if h3.get("p") is not None:
        txt += f"\none-sided p = {VV.p4(h3['p'])}"
    _box(ax, txt, x=0.97, ha="right")
    fig.subplots_adjust(top=0.80, bottom=0.19, left=0.10, right=0.97)
    _header(fig, 6, "Per-run G* (floor: three grounded answers per run); gray: pair below 30 units.",
            "Dotted: rel1 = 0.25 (rel3 = 0.50); dashed: rel1 = 0.125 (rel3 = 0.30).")
    _save(fig, 6, f"H3_Run_Reliability: {V['verdicts']['H3_Run_Reliability']}", out)


def chart_07(V, out):
    st4, st6 = VV.cond_state(V, "H4_Sep_Ranking"), VV.cond_state(V, "H6_Sep_Coverage")
    s7 = VV.h7_state(V)
    rows = []                                    # (label, value, ci, kind, verdict, decides)
    for h, lab in (("H1_Sep_Presence", "H1 Presence"), ("H2_Sep_Consistency", "H2 Consistency")):
        for i, c in enumerate(("S1", "S0")):
            l = V["legs"][h][i]
            rows.append((f"{lab}, {c}", l.get("rho_w"), l.get("ci90"), "sep", V["verdicts"][h], True))
    rows.append(("H3 runs (rel3)", V["H3"].get("rel3"), None, "rel", V["verdicts"]["H3_Run_Reliability"], True))
    for h, st, lab in (("H4_Sep_Ranking", st4, "H4 Ranking R*_S1"), ("H6_Sep_Coverage", st6, "H6 Coverage Cov*")):
        if st["case"] == "COMPUTED":
            l = VV.jget(V, st["leg_path"])
            rows.append((lab, l.get("rho_w"), l.get("ci90"), "sep", st["word"], st["gating"]))
        else:
            rows.append((lab, None, None, "sep", f"{st['word']} ({st['case'].lower()})", False))
    if "leg" in s7:
        rows.append(("H7 SDRI (one-sided)", s7["leg"].get("rho_w"), s7["leg"].get("ci90"), "h7", s7["word"], False))
    else:
        rows.append(("H7 SDRI (one-sided)", None, None, "h7", f"{s7['word'] or 'pending'}", False))
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    n = len(rows)
    for i, (lab, v, ci, kind, verdict, decides) in enumerate(rows):
        y = n - i
        if kind == "sep":
            ax.add_patch(Rectangle((-0.30, y - 0.38), 0.60, 0.76, color=cs.PALETTE["indigo_t3"], alpha=0.35, lw=0))
            for x in (-0.5, 0.5):
                ax.plot([x, x], [y - 0.38, y + 0.38], color=cs.WARM, lw=0.8, ls=":")
        elif kind == "rel":
            ax.add_patch(Rectangle((0.50, y - 0.38), 0.50, 0.76, color=cs.PALETTE["indigo_t3"], alpha=0.35, lw=0))
            ax.plot([0.30, 0.30], [y - 0.38, y + 0.38], color=cs.WARM, lw=0.8, ls=":")
        else:
            ax.add_patch(Rectangle((0.30, y - 0.38), 0.70, 0.76, color=cs.PALETTE["indigo_t3"], alpha=0.35, lw=0))
            ax.plot([0.10, 0.10], [y - 0.38, y + 0.38], color=cs.WARM, lw=0.8, ls=":")
        col = cs.INDIGO if decides else cs.GRAY
        if v is not None and abs(v) <= 1:
            if ci and ci.get("lo") is not None:
                ax.plot([ci["lo"], ci["hi"]], [y, y], color=col, lw=1.5, zorder=3)
            ax.scatter([v], [y], s=34, color=col, zorder=4)
        ax.text(1.03, y, verdict, fontsize=7.2, va="center", ha="left", color=col,
                transform=ax.get_yaxis_transform())
    ax.axvline(0, color=cs.PALETTE["gray_light"], lw=0.8, zorder=1)
    ax.set_yticks([n - i for i in range(n)])
    ax.set_yticklabels([r[0] for r in rows], fontsize=7.8)
    ax.set_ylim(0.4, n + 0.6)
    ax.set_xlim(-1, 1)
    ax.set_xlabel("ρ_w (H3: rel3), with 90% bootstrap interval where computed", fontsize=9)
    ax.tick_params(axis="x", labelsize=8.5)
    fig.subplots_adjust(top=0.80, bottom=0.15, left=0.24, right=0.76)
    _header(fig, 7, "Shaded: the CONFIRMED region of each leg; dotted: its FALSIFIED threshold (§3).",
            "Indigo: legs that decide or can downgrade the gate; gray: reported only, or not computed.")
    fg = VV.final_gate(V)
    _save(fig, 7, f"Gate: {fg['final']}" + (f" (Stage C1: {fg['c1']})" if fg["c1"] != fg["final"] else "")
          + (" — Stage C1 only" if V.get("stage_C2") is None else ""), out)


def chart_08(V, rows_s, out):
    s7 = VV.h7_state(V)
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    gs = {k: u["G_star"] for k, u in V["units"].items() if u["rated"]}
    for s in VV.SUBS:
        x, y = [], []
        for r in rows_s:
            k = f"{r['substrate']}|{r['brand_id']}"
            if r["substrate"] == s and str(r.get("phantom")) != "1" and r.get("SDRI") not in ("", None) and k in gs:
                x.append(float(r["SDRI"]))
                y.append(gs[k])
        ax.scatter(x, y, s=28, color=SUBCOL[s], alpha=0.85, edgecolor="white", linewidth=0.4, zorder=3,
                   label=f"{VV.CAT[s]} (n = {len(x)})")
    ax.set_xlim(-3, 103)
    ax.set_ylim(-3, 103)
    ax.set_xlabel("SDRI (0–100; eight binary indicators, protocol §5)", fontsize=9)
    ax.set_ylabel("G* (0–100)", fontsize=9)
    ax.tick_params(labelsize=8.5)
    ax.legend(loc="center left", bbox_to_anchor=(1.01, 0.5), fontsize=7.2, frameon=False)
    leg = s7.get("leg") or {}
    if leg.get("rho_w") is not None:
        txt = f"ρ_w = {VV.r3(leg['rho_w'])} (one-sided p = {VV.p4(leg['p'])})\nn = {leg['n']} brands"
        _box(ax, txt)
    fig.subplots_adjust(top=0.80, bottom=0.17, left=0.10, right=0.74)
    _header(fig, 8, "Brands with an SDRI (home page fetched) and a rated G*; defunct brands excluded.",
            "SDRI from Part II's first pass; G* from Part I.")
    _save(fig, 8, f"H7_Struct_Gap: {s7['word']}", out)


def chart_09(R, out):
    """v1.18 (exploratory, §3.8): program value per definition as a point, its 90% interval as a whisker."""
    prog, ci = R["primary"]["program"]["pair_weighted"], R["primary_ci"]["program_pair_weighted"]
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    n = len(V118.DEFS)
    for i, (d, s, label) in enumerate(V118.DEFS):
        y = n - i
        lo, hi = ci[d][0], ci[d][1]
        ax.errorbar([prog[d]], [y], xerr=[[prog[d] - lo], [hi - prog[d]]], fmt="o", color=cs.INDIGO, ms=5.5,
                    elinewidth=1.4, capsize=4, capthick=1.2, zorder=3)
        ax.annotate(f"{VV.r2(prog[d])}  ({VV.r2(lo)}–{VV.r2(hi)})", (hi, y), xytext=(8, 0),
                    textcoords="offset points", ha="left", va="center", fontsize=7.6, color=cs.INDIGO)
    ax.set_yticks([n - i for i in range(n)])
    ax.set_yticklabels([f"{s}: {label}" for _, s, label in V118.DEFS], fontsize=8.5)
    ax.set_ylim(0.4, n + 0.6)
    ax.set_xlim(0, 115)
    ax.set_xticks(range(0, 101, 20))
    ax.set_xlabel("pair-weighted share of cited domains (%)", fontsize=9)
    ax.tick_params(axis="x", labelsize=8.5)
    ax.grid(axis="x", color=cs.PALETTE["gray_light"], lw=0.5, zorder=0)
    fig.subplots_adjust(top=0.80, bottom=0.17, left=0.22, right=0.97)
    _header(fig, 9, f"All answer–brand pairs (n = {R['primary']['program']['n_pairs']}); point = program value, "
                    f"whisker = 90% cluster-bootstrap interval ({R['primary_ci']['n_boot']:,} draws).",
            "Exploratory; gates nothing. M = 100 − K by construction.")
    _save(fig, 9, "", out, SOURCE_V118)


def main(argv=None):
    global WATERMARK
    ap = argparse.ArgumentParser(description="v1.13 Grounding Paper A figures")
    ap.add_argument("--verdicts", type=Path, default=VV.VERDICTS_JSON)
    ap.add_argument("--sdri", type=Path, default=None)
    ap.add_argument("--out", type=Path, default=ROOT / "reports/figs/v113")
    ap.add_argument("--watermark", default=None)
    a = ap.parse_args(argv)
    sdri = a.sdri if a.sdri else (VV.SDRI_CSV if VV.SDRI_CSV.exists() else None)
    src = VV.load_sources(a.verdicts, sdri)
    V = src["verdicts"]
    if VV.is_synthetic(V) and not a.watermark:
        sys.exit("[v1.13 charts] REFUSED: synthetic verdicts need --watermark")
    if not VV.is_synthetic(V) and a.watermark:
        sys.exit("[v1.13 charts] REFUSED: --watermark is for synthetic runs only")
    try:
        VV.check_consistency(src)
    except VV.Inconsistent as e:
        sys.exit(f"[v1.13 charts] REFUSED: inconsistent verdict file: {e}")
    WATERMARK = a.watermark
    print(f"building v1.13 figures -> {a.out}")
    chart_01(V, a.out)
    chart_02(V, a.out)
    chart_03(V, a.out)
    chart_sep(V, 4, "H1_Sep_Presence", "Presence P", a.out)
    chart_sep(V, 5, "H2_Sep_Consistency", "Consistency C*", a.out)
    chart_06(V, a.out)
    chart_07(V, a.out)
    if "leg" in (V.get("stage_C2") or {}):
        chart_08(V, src["sdri"]["rows"], a.out)
    try:
        chart_09(V118.load()["v118"], a.out)
    except V118.InputError as e:
        sys.exit(f"[v1.13 charts] REFUSED: v1.18 inputs: {e}")
    print("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
