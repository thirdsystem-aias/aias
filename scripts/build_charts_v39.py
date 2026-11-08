#!/usr/bin/env python3
"""
build_charts_v39.py — v0.39 Commercial Coffee Roasters (Bellwether-focal) report-register figures.
Forked from build_charts_v38.py (fork-don't-rebuild). Third System chart standard (chart_style.py).
Reads scored and audited outputs only:
  <root>/v39_verdicts.json, <root>/data/v39_tables.json, <root>/data/v39_coded.csv, <root>/data/v39_coder_audit.json
Writes PDFs to reports/figs/v39/report/ (or --out).

  report_fig_01_frame.pdf       how "should my café roast?" answers treat venting (audited), by arm
  report_fig_02_constraint.pdf  Bellwether presence: generic vs constraint café questions, by arm (+ per model)
  report_fig_03_ranking.pdf     who wins the constraint answer: older models vs current assistants
  report_fig_04_search.pdf      what web search changes: presence per model, and currency
  report_fig_05_lineup.pdf      what each model says when asked directly about Bellwether (audited labels)
  report_fig_06_showfloor.pdf   the six Coffee Fest Dallas-Fort Worth exhibitors on the AI shelf
"""
import argparse
import csv
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import chart_style as CS  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

ROOT = Path(os.environ.get("AIAS_ROOT", "/Users/pablou/aias"))
P = CS.PALETTE
LEGACY = ["M1", "M2", "M3", "M4", "M5", "M6"]
CURRENT = ["C1", "C2", "C3"]
MODEL = {"M1": "Claude Opus 4.5", "M2": "Claude Sonnet 4.5", "M3": "GPT-4o", "M4": "GPT-4o-mini",
         "M5": "Gemini 2.5 Flash", "M6": "Gemini 2.5 Flash-Lite",
         "C1": "Claude Opus 5.5", "C2": "GPT-6 Astra", "C3": "Gemini 4 Argon"}
CELLS = [("L", "S0"), ("C", "S0"), ("C", "S1")]
CELL_LABEL = {("L", "S0"): "2024–25 models\n(fixed panel)", ("C", "S0"): "Current assistants,\nno search",
              ("C", "S1"): "Current assistants,\nwith web search"}
CELL_SHORT = {("L", "S0"): "2024–25 models", ("C", "S0"): "Current, no search", ("C", "S1"): "Current, with search"}
CELL_COLOR = {("L", "S0"): P["warm"], ("C", "S0"): P["indigo"], ("C", "S1"): P["indigo_t2"]}
FOCAL = "B01"
PHASE, PROTOCOL = "v0.39", "v1.2"

TEXT = {
    "frame": {"title": "Before any brand is named, the older models tell cafés to vent",
              "subtitle": "How answers to “should my café roast in-house?” questions treat venting",
              "description": "Analyst-audited classification of every answer: 6 questions x 6 models (2024–25) or x 3 models (current)."},
    "constraint": {"title": "Bellwether appears when the café names the barrier",
                   "subtitle": "Share of café roaster recommendations that name Bellwether, generic vs constraint questions",
                   "description": "Constraint questions state no gas line, no venting, smoke or air-quality rules. Bars pool models; dots show each model."},
    "ranking": {"title": "Older models answer the constraint with drums; current ones with Bellwether",
                "subtitle": "Share of constraint-framed café answers naming each brand (top eight in each panel)",
                "description": "Six questions per model: no gas line, no ductwork, can't vent, least smoke, air-quality rules, best electric roaster."},
    "search": {"title": "Search adds currency, not presence",
               "subtitle": "What changes when the current assistants can search the web",
               "description": "Left: café recommendations (generic and constraint, 12 per model). Right: direct questions about Bellwether."},
    "lineup": {"title": "Asked directly, older models guess; current ones know the Shop Roaster",
               "subtitle": "Each model's answer to four direct questions about Bellwether, as read by the analyst",
               "description": "Indigo: matches the current Shop Roaster or lineup. Gray: no answer, a range, or an older machine. Orange: wrong or invented."},
    "showfloor": {"title": "Six roaster makers on the show floor, five on the AI shelf",
                  "subtitle": "Share of café and roastery recommendation answers naming each Coffee Fest Dallas-Fort Worth exhibitor",
                  "description": "Recommendation answers: 18 questions per model (generic café, constraint and production roastery)."},
}


def load(root):
    v = json.loads((root / "v39_verdicts.json").read_text(encoding="utf-8"))
    t = json.loads((root / "data" / "v39_tables.json").read_text(encoding="utf-8"))
    a = json.loads((root / "data" / "v39_coder_audit.json").read_text(encoding="utf-8"))
    with open(root / "data" / "v39_coded.csv", encoding="utf-8") as f:
        coded = list(csv.DictReader(f))
    reg = json.loads((root / "registries" / "brands_commercial_roasters_v0.39.json").read_text(encoding="utf-8"))
    names = {b["id"]: b["brand"] for b in reg["brands"]}
    strata = {b["id"]: b["stratum"] for b in reg["brands"]}
    return v, t, a, coded, names, strata


def pct(x):
    return f"{round(100 * x):d}%"


def save(fig, out, name):
    out.mkdir(parents=True, exist_ok=True)
    p = out / name
    fig.savefig(p, **CS.SAVEFIG_PARAMS)
    plt.close(fig)
    print("  wrote", p)


def fig_frame(a, out):
    summ = a["frame_classification"]["summary"]
    cls = a["frame_classification"]["classes"]
    segs = [(cls[0], "Venting presented as required", P["warm"], "white"),
            (cls[1], "Ventless option raised, no brand", P["indigo_t3"], P["black"]),
            (cls[2], "Ventless option named, with a brand", P["indigo"], "white"),
            (cls[3], "Venting not discussed", P["gray_light"], P["black"])]
    h = 4.0
    fig, ax = plt.subplots(figsize=(7.5, h))
    fig.subplots_adjust(top=1 - 1.25 / h, bottom=0.95 / h, left=0.25, right=0.96)
    ys = [2, 1, 0]
    for y, cell in zip(ys, CELLS):
        s = summ[f"{cell[0]}|{cell[1]}"]
        n, left = s["n"], 0.0
        for key, _, col, tc in segs:
            k = s["counts"].get(key, 0)
            if not k:
                continue
            w = k / n
            ax.barh(y, w, left=left, height=0.58, color=col, edgecolor="white", linewidth=0.8)
            if w >= 0.08:
                ax.text(left + w / 2, y, pct(w), ha="center", va="center", fontsize=8.6, color=tc, fontweight="bold")
            left += w
        ax.text(1.01, y, f"n = {n}", va="center", ha="left", fontsize=7.8, color=P["gray"])
    ax.set_yticks(ys)
    ax.set_yticklabels([CELL_LABEL[c] for c in CELLS], fontsize=8.4)
    ax.set_xlim(0, 1)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"], fontsize=CS.FONT_SIZES["axis_tick"])
    for sp in ("left", "top", "right"):
        ax.spines[sp].set_visible(False)
    ax.tick_params(axis="y", length=0)
    handles = [Patch(color=col, label=lab) for _, lab, col, _ in segs]
    fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.55, 0.035), ncol=2, fontsize=7.6, frameon=False)
    CS.add_header(fig, **TEXT["frame"])
    CS.add_footer(fig, verdict="", phase=PHASE, protocol=PROTOCOL)
    save(fig, out, "report_fig_01_frame.pdf")


def fig_constraint(t, out):
    pres, bm = t["presence"], t["bellwether_by_model_tier"]
    fig, ax = plt.subplots(figsize=(7.5, 4.9))
    fig.subplots_adjust(top=0.775, bottom=0.235, left=0.09, right=0.97)
    groups = [0, 1.25, 2.5]
    off = 0.21
    for gx, cell in zip(groups, CELLS):
        arm, cond = cell
        slots = LEGACY if arm == "L" else CURRENT
        for j, (tier, col) in enumerate((("G", P["indigo_t3"]), ("C", P["indigo"]))):
            x = gx + (j - 0.5) * 2 * off
            y = pres[f"{arm}|{cond}|{tier}"]["presence"][FOCAL] or 0
            ax.bar(x, y, width=0.38, color=col, zorder=2)
            if y >= 0.12:  # label inside the bar foot, clear of the per-model dots
                ax.text(x, 0.03, pct(y), ha="center", va="bottom", fontsize=11.5, fontweight="bold",
                        color="white" if tier == "C" else P["indigo"], zorder=4)
            else:
                ax.text(x, y + 0.04, pct(y), ha="center", va="bottom", fontsize=11.5, fontweight="bold",
                        color=P["indigo"], zorder=4)
            k = len(slots)
            for i, m in enumerate(slots):
                c = bm[f"{arm}|{cond}|{m}|{tier}"]
                if c["n"]:
                    dx = (i - (k - 1) / 2) * (0.28 / max(k - 1, 1))
                    ax.scatter(x + dx, c["k"] / c["n"], s=16, zorder=3, color=P["black"], edgecolor="white", linewidth=0.5)
    ax.set_xticks([g + d for g in groups for d in (-off, off)])
    ax.set_xticklabels(["Generic", "Constraint"] * 3, fontsize=8.2)
    for gx, cell in zip(groups, CELLS):
        ax.text(gx, -0.2, CELL_LABEL[cell], ha="center", va="top", fontsize=8.4, fontweight="bold",
                color=P["black"], transform=ax.get_xaxis_transform())
    ax.set_ylim(0, 1.12)
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(["0%", "25%", "50%", "75%", "100%"], fontsize=CS.FONT_SIZES["axis_tick"])
    ax.grid(axis="y", color=P["gray_light"], linewidth=0.5, zorder=0)
    ax.spines["left"].set_visible(False)
    ax.axvline(0.625, color=P["gray_light"], linewidth=0.8, linestyle=(0, (2, 2)))
    CS.add_header(fig, **TEXT["constraint"])
    CS.add_footer(fig, verdict="", phase=PHASE, protocol=PROTOCOL)
    save(fig, out, "report_fig_02_constraint.pdf")


def fig_ranking(t, names, out):
    pres = t["presence"]
    panels = [(("L", "S0"), "2024–25 models (36 answers)"), (("C", "S0"), "Current assistants, no search (18 answers)")]
    h = 4.6
    fig, axes = plt.subplots(1, 2, figsize=(7.5, h))
    fig.subplots_adjust(top=1 - 1.3 / h, bottom=0.55 / h, left=0.17, right=0.975, wspace=0.62)
    for ax, (cell, head) in zip(axes, panels):
        pr = pres[f"{cell[0]}|{cell[1]}|C"]["presence"]
        top = sorted(((v or 0, b) for b, v in pr.items()), key=lambda x: (-x[0], names[x[1]]))[:8]
        if FOCAL not in [b for _, b in top]:
            top = top[:7] + [(pr[FOCAL] or 0, FOCAL)]
        ys = list(range(len(top)))[::-1]
        for y, (val, b) in zip(ys, top):
            focal = b == FOCAL
            ax.barh(y, val, height=0.62, color=P["indigo"] if focal else P["gray_light"], zorder=2)
            ax.text(val + 0.02, y, pct(val), va="center", fontsize=8, color=P["indigo"] if focal else P["gray"],
                    fontweight="bold" if focal else "normal")
        ax.set_yticks(ys)
        ax.set_yticklabels([names[b] for _, b in top], fontsize=8.2)
        for lab, (_, b) in zip(ax.get_yticklabels(), top):
            if b == FOCAL:
                lab.set_fontweight("bold")
                lab.set_color(P["indigo"])
        ax.set_xlim(0, 1.05)
        ax.set_xticks([0, 0.5, 1.0])
        ax.set_xticklabels(["0%", "50%", "100%"], fontsize=CS.FONT_SIZES["axis_tick"])
        for sp in ("left", "top", "right"):
            ax.spines[sp].set_visible(False)
        ax.tick_params(axis="y", length=0)
        ax.set_title(head, fontsize=8.6, loc="left", color=P["black"], fontweight="bold", pad=6)
    CS.add_header(fig, **TEXT["ranking"])
    CS.add_footer(fig, verdict="", phase=PHASE, protocol=PROTOCOL)
    save(fig, out, "report_fig_03_ranking.pdf")


def fig_search(coded, a, t, out):
    agg = defaultdict(lambda: [0, 0])
    for r in coded:
        if r["arm"] == "C" and r["tier"] in ("G", "C") and r["status"] == "ok":
            c = agg[(r["model_slot"], r["condition"])]
            c[0] += int(r["bellwether"])
            c[1] += 1
    h = 4.4
    fig = plt.figure(figsize=(7.5, h))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.15], left=0.15, right=0.975, top=1 - 1.3 / h, bottom=0.95 / h, wspace=0.55)
    ax = fig.add_subplot(gs[0, 0])
    ys = [2, 1, 0]
    for y, m in zip(ys, CURRENT):
        s0 = agg[(m, "S0")][0] / agg[(m, "S0")][1]
        s1 = agg[(m, "S1")][0] / agg[(m, "S1")][1]
        ax.plot([s0, s1], [y, y], color=P["gray_light"], linewidth=2, zorder=1)
        ax.scatter([s0], [y], s=46, color=P["indigo"], zorder=3, edgecolor="white", linewidth=0.6)
        ax.scatter([s1], [y], s=46, color=P["indigo_t2"], zorder=3, edgecolor="white", linewidth=0.6, marker="D")
        lo, hi = min(s0, s1), max(s0, s1)
        if abs(s1 - s0) < 0.005:
            ax.text(s0, y + 0.3, pct(s0) + " (both)", ha="right", fontsize=7.8, color=P["indigo"])
        else:
            ax.text(s0, y + 0.3, pct(s0), ha="center", fontsize=7.8, color=P["indigo"])
            ax.text(s1, y - 0.42, pct(s1), ha="center", fontsize=7.8, color=P["indigo_t1"])
    ax.set_yticks(ys)
    ax.set_yticklabels([MODEL[m] for m in CURRENT], fontsize=8.2)
    ax.set_xlim(0, 1.05)
    ax.set_ylim(-0.8, 2.7)
    ax.set_xticks([0, 0.5, 1.0])
    ax.set_xticklabels(["0%", "50%", "100%"], fontsize=CS.FONT_SIZES["axis_tick"])
    for sp in ("left", "top", "right"):
        ax.spines[sp].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.set_title("Café answers naming Bellwether", fontsize=8.6, loc="left", fontweight="bold", pad=6)
    handles = [Line2D([0], [0], marker="o", color="w", markerfacecolor=P["indigo"], markersize=7, label="No search"),
               Line2D([0], [0], marker="D", color="w", markerfacecolor=P["indigo_t2"], markersize=6, label="With search")]
    fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, 0.07), ncol=2, fontsize=7.6, frameon=False)

    ax2 = fig.add_subplot(gs[0, 1])
    lab = a["k_probe_labels"]
    mk = t["descriptives"]["D7_retrieval"]["markers_2026_in_K1_K2"]
    n26 = {c: sum(1 for k in mk if k.endswith("|" + c) and k.split("|")[1] in CURRENT) for c in ("S0", "S1")}
    k5 = {c: sum(1 for m in CURRENT if "(correct)" in lab["K5_batch"][f"{m}|{c}"]) for c in ("S0", "S1")}
    d3 = a["D3_claim_reproduction"]
    uniq_s1 = len(d3["reproduced_as_fact"]) + len(d3["reproduced_with_attribution"])
    rows = [("Lineup answers naming the\nOct 2026 Shop Roaster", n26["S0"], n26["S1"], 6),
            ("Batch size stated correctly\n(1.5 kg)", k5["S0"], k5["S1"], 3),
            ("Answers repeating “the only\nventless roaster”", 0, uniq_s1, None)]
    ys2 = [2, 1, 0]
    for y, (txt, a0, a1, n) in zip(ys2, rows):
        den = n if n else max(a1, 1)
        for j, (val, col) in enumerate(((a0, P["indigo"]), (a1, P["indigo_t2"]))):
            yy = y + (0.17 if j == 0 else -0.17)
            ax2.barh(yy, val / den if den else 0, height=0.3, color=col, zorder=2)
            lbl = f"{val} of {n}" if n else f"{val} answers"
            ax2.text((val / den if den else 0) + 0.03, yy, lbl, va="center", fontsize=7.6, color=P["gray"])
    ax2.set_yticks(ys2)
    ax2.set_yticklabels([r[0] for r in rows], fontsize=7.8)
    ax2.set_xlim(0, 1.45)
    ax2.set_xticks([])
    for sp in ("left", "top", "right", "bottom"):
        ax2.spines[sp].set_visible(False)
    ax2.tick_params(axis="y", length=0)
    ax2.set_title("Direct questions about Bellwether", fontsize=8.6, loc="left", fontweight="bold", pad=6)
    CS.add_header(fig, **TEXT["search"])
    CS.add_footer(fig, verdict="", phase=PHASE, protocol=PROTOCOL)
    save(fig, out, "report_fig_04_search.pdf")


# Tone of each audited label (v39_coder_audit.json k_probe_labels). Indigo: matches the current Shop Roaster or
# lineup on the fact sheet. Gray: no answer, a range, or an older Bellwether machine. Orange: wrong or invented.
TONE = {
    "Doesn't know": "none", "Unsure": "none", "Unsure; mentions Shop Roaster": "none",
    "\u201cSeries 3\u201d": "bad", "Shop Roaster (2024)": "good", "New Shop Roaster (Oct 2026)": "good",
    "Reads it as a coffee seller": "bad", "Series 1 and 2": "none", "Shop Roaster + Series 2": "good", "Shop Roaster only": "good",
    "No (correct)": "good", "Yes: a 6-inch duct (wrong)": "bad", "Yes (wrong)": "bad", "Yes: burns gas (wrong)": "bad",
    "0.5\u20131.4 kg (wrong)": "bad", "4.5\u20137 kg (wrong)": "bad", "2.7 kg (Series 2 figure)": "none", "5\u201312 lb (wrong)": "bad",
    "3 kg (wrong)": "bad", "1 kg (wrong)": "bad", "1\u20133 kg (range)": "none", "Series 2 2.7 kg; Shop 1.6 kg": "good",
    "1.5 kg (correct)": "good",
}


def _tone(txt):
    return TONE[txt]  # KeyError on any unmapped label: fail loudly rather than guess


def fig_lineup(a, out):
    lab = a["k_probe_labels"]
    cols = [("K1_newest", "Newest roaster?"), ("K2_lineup", "What does it sell now?"),
            ("K3_venting", "Does it need venting?"), ("K5_batch", "Batch size?")]
    order = [(m, MODEL[m]) for m in LEGACY] + [(f"{m}|S0", MODEL[m]) for m in CURRENT] + [(f"{m}|S1", MODEL[m]) for m in CURRENT]
    h = 5.75
    fig, ax = plt.subplots(figsize=(7.5, h))
    fig.subplots_adjust(top=1 - 1.4 / h, bottom=0.42 / h, left=0.2, right=0.985)
    tone_col = {"good": P["indigo_t3"], "bad": P["warm_t3"], "none": "#E6E6E6"}
    txt_col = {"good": P["indigo"], "bad": P["warm_sec"], "none": P["gray"]}
    nr, nc = len(order), len(cols)
    gaps = {6: 0.35, 9: 0.35}
    ypos, y = {}, 0.0
    for ri in range(nr):
        if ri in gaps:
            y += gaps[ri]
        ypos[ri] = y
        y += 1.0
    total = y
    for ci, (key, head) in enumerate(cols):
        ax.text(ci + 0.5, total + 0.15, head, ha="center", va="bottom", fontsize=8.2, fontweight="bold", color=P["black"])
        for ri, (k, _) in enumerate(order):
            yy = total - ypos[ri] - 1
            txt = lab[key][k]
            tone = _tone(txt)
            ax.add_patch(plt.Rectangle((ci + 0.03, yy + 0.07), 0.94, 0.86, color=tone_col[tone], ec="none"))
            ax.text(ci + 0.5, yy + 0.5, txt.replace("; ", ";\n") if len(txt) > 24 else txt, ha="center", va="center",
                    fontsize=6.9, color=txt_col[tone], linespacing=1.1)
    ax.set_xlim(0, nc)
    ax.set_ylim(-0.1, total + 1.0)
    ax.set_yticks([total - ypos[ri] - 0.5 for ri in range(nr)])
    ax.set_yticklabels([lbl for _, lbl in order], fontsize=7.8)
    ax.set_xticks([])
    for sp in ("left", "bottom", "top", "right"):
        ax.spines[sp].set_visible(False)
    ax.tick_params(axis="y", length=0)
    for ri, head in ((0, "2024–25 models"), (6, "Current assistants, no search"), (9, "Current assistants, with search")):
        ax.text(-0.02, total - ypos[ri] + 0.06, head, ha="right", va="bottom", fontsize=7.4, color=P["gray"],
                fontstyle="italic", transform=ax.transData)
    CS.add_header(fig, **TEXT["lineup"])
    CS.add_footer(fig, verdict="", phase=PHASE, protocol=PROTOCOL)
    save(fig, out, "report_fig_05_lineup.pdf")


def fig_showfloor(t, names, strata, out):
    d5 = t["descriptives"]["D5_show_floor_vs_ai_shelf"]
    sf = [b for b in names if strata[b] == "S"]
    order = sorted(sf, key=lambda b: -(d5["C|S0"]["show_floor_presence"][names[b]] or 0))
    h = 4.7
    fig, ax = plt.subplots(figsize=(7.5, h))
    fig.subplots_adjust(top=1 - 1.25 / h, bottom=0.95 / h, left=0.24, right=0.95)
    bh = 0.24
    for i, b in enumerate(order):
        y = len(order) - 1 - i
        for j, cell in enumerate(CELLS):
            val = d5[f"{cell[0]}|{cell[1]}"]["show_floor_presence"][names[b]] or 0
            yy = y + (1 - j) * bh
            ax.barh(yy, val, height=bh * 0.92, color=CELL_COLOR[cell], zorder=2)
            ax.text(val + 0.012, yy, pct(val), va="center", fontsize=7.2, color=P["gray"])
    ax.set_yticks(range(len(order))[::-1])
    ax.set_yticklabels([names[b] for b in order], fontsize=8.4)
    for lab in ax.get_yticklabels():
        if lab.get_text() == names[FOCAL]:
            lab.set_fontweight("bold")
            lab.set_color(P["indigo"])
    ax.set_xlim(0, 1.0)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"], fontsize=CS.FONT_SIZES["axis_tick"])
    ax.grid(axis="x", color=P["gray_light"], linewidth=0.5, zorder=0)
    for sp in ("left", "top", "right"):
        ax.spines[sp].set_visible(False)
    ax.tick_params(axis="y", length=0)
    handles = [Patch(color=CELL_COLOR[c], label=CELL_SHORT[c] + f" ({d5[f'{c[0]}|{c[1]}']['n']} answers)") for c in CELLS]
    fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.55, 0.065), ncol=3, fontsize=7.4, frameon=False)
    CS.add_header(fig, **TEXT["showfloor"])
    CS.add_footer(fig, verdict="", phase=PHASE, protocol=PROTOCOL)
    save(fig, out, "report_fig_06_showfloor.pdf")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(ROOT / "osf/v39"))
    ap.add_argument("--out", default=str(ROOT / "reports/figs/v39/report"))
    args = ap.parse_args()
    CS.setup()
    v, t, a, coded, names, strata = load(Path(args.root))
    out = Path(args.out)
    fig_frame(a, out)
    fig_constraint(t, out)
    fig_ranking(t, names, out)
    fig_search(coded, a, t, out)
    fig_lineup(a, out)
    fig_showfloor(t, names, strata, out)


if __name__ == "__main__":
    main()
