#!/usr/bin/env python3
"""
build_charts_v38.py — v0.38 Home Coffee Roasters (Aillio-focal) report-register figures.
Third System chart standard (chart_style.py). Reads scored outputs only:
  <root>/v38_verdicts.json, <root>/data/v38_tables.json, <root>/data/v38_coded.csv
Writes PDFs to reports/figs/v38/report/ (or --out).

  report_fig_01_tier.pdf    Aillio presence by prompt tier (pooled bar + one dot per model)
  report_fig_02_map.pdf     category map: presence, beginner vs enthusiast/prosumer framing
  report_fig_03_legacy.pdf  which Bullet the models name when they recommend Aillio
  report_fig_04_lineup.pdf  what each model says when asked directly about Aillio's lineup
  report_fig_05_grounding.pdf  right specs, wrong machine: audited spec accuracy vs generation named
"""
import argparse
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import chart_style as CS  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

ROOT = Path("/Users/pablou/aias")
P = CS.PALETTE
SLOTS = ["M1", "M2", "M3", "M4", "M5", "M6"]
POST = ["M1", "M2", "M5", "M6"]
PRE = ["M3", "M4"]
MODEL = {"M1": "Claude Opus 4.5", "M2": "Claude Sonnet 4.5", "M3": "GPT-4o", "M4": "GPT-4o-mini",
         "M5": "Gemini 2.5 Flash", "M6": "Gemini 2.5 Flash-Lite"}
TIER = {"B": "Beginner\nprompts", "E": "Enthusiast\nprompts", "P": "Prosumer /\nmicro-roastery prompts"}
PHASE, PROTOCOL = "v0.38", "v1.2"

# Report-register chart text. Edited with the content module once verdicts are in.
TEXT = {
    "tier": {"title": "The Bullet is an expert's answer",
             "subtitle": "Share of AI recommendation answers that name the Aillio Bullet, by how the question is framed",
             "description": "Bars: six models pooled (6 prompts x 6 models per tier). Dots: each model on its own."},
    "map": {"title": "Two categories, depending on who is asking",
            "subtitle": "Share of answers naming each brand: beginner questions vs enthusiast and prosumer questions",
            "description": "Brands named in at least 10% of answers in either frame, ordered by presence under enthusiast/prosumer framing."},
    "legacy": {"title": "Every Bullet the models recommend is the R1",
               "subtitle": "Recommendation answers that name the Aillio Bullet, by the generation they name",
               "description": "18 recommendation prompts per model. No answer from any model names the R2 or R2 Pro."},
    "lineup": {"title": "Asked directly, every model describes the old lineup",
               "subtitle": "Each model's answer to four direct questions about Aillio",
               "description": "Quoted names are the models' own wording. Dashed line: models above it were trained after the R2 launch (July 2024)."},
    "grounding": {"title": "Accurate on specs, a generation behind",
                  "subtitle": "What the models say about the Bullet when they recommend it, checked against the machine",
                  "description": "Analyst-audited statements in the 62 recommendation answers that name the Bullet. Fact sheet: 1 kg maximum batch; induction heating."},
}
FOOTER = {"tier": "", "map": "", "legacy": "", "lineup": "", "grounding": ""}


def load(root):
    v = json.loads((root / "v38_verdicts.json").read_text(encoding="utf-8"))
    t = json.loads((root / "data" / "v38_tables.json").read_text(encoding="utf-8"))
    with open(root / "data" / "v38_coded.csv", encoding="utf-8") as f:
        coded = list(csv.DictReader(f))
    reg = json.loads((ROOT / "osf/v38/registries/brands_home_roasters_v0.38.json").read_text(encoding="utf-8"))
    names = {b["id"]: b["brand"] for b in reg["brands"]}
    return v, t, coded, names


def pct(x):
    return f"{round(100 * x):d}%"


def save(fig, out, name):
    out.mkdir(parents=True, exist_ok=True)
    p = out / name
    fig.savefig(p, **CS.SAVEFIG_PARAMS)
    plt.close(fig)
    print("  wrote", p)


def fig_tier(v, t, out):
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    fig.subplots_adjust(top=0.78, bottom=0.24, left=0.09, right=0.97)
    pooled = [v["H_Tier"][f"presence_{k}"] for k in ("B", "E", "P")]
    colors = [P["indigo_t3"], P["indigo"], P["indigo"]]
    xs = [0, 1, 2]
    ax.bar(xs, pooled, width=0.56, color=colors, zorder=2)
    for x, y in zip(xs, pooled):
        ax.text(x, 0.035, pct(y), ha="center", va="bottom", fontsize=13, fontweight="bold",
                color="white" if x else P["indigo"], zorder=4)
    offs = [-0.2, -0.12, -0.04, 0.04, 0.12, 0.2]
    abm = t["aillio_by_model_tier"]
    for i, m in enumerate(SLOTS):
        for x, k in zip(xs, ("B", "E", "P")):
            c = abm[m][k]
            if c["n"]:
                ax.scatter(x + offs[i], c["k"] / c["n"], s=22, zorder=3,
                           color=P["warm"] if m in PRE else P["black"], edgecolor="white", linewidth=0.6)
    ax.set_xticks(xs)
    ax.set_xticklabels([TIER[k] for k in ("B", "E", "P")], fontsize=CS.FONT_SIZES["axis_tick"])
    ax.set_ylim(0, 1.05)
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(["0%", "25%", "50%", "75%", "100%"], fontsize=CS.FONT_SIZES["axis_tick"])
    ax.grid(axis="y", color=P["gray_light"], linewidth=0.5, zorder=0)
    ax.spines["left"].set_visible(False)
    handles = [Line2D([0], [0], marker="o", color="w", markerfacecolor=P["black"], markersize=6, label="Model trained after the R2 launch"),
               Line2D([0], [0], marker="o", color="w", markerfacecolor=P["warm"], markersize=6, label="Model trained before the R2 existed")]
    fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.53, 0.045), ncol=2,
               fontsize=CS.FONT_SIZES["legend"], frameon=False)
    CS.add_header(fig, **TEXT["tier"])
    CS.add_footer(fig, verdict=FOOTER["tier"], phase=PHASE, protocol=PROTOCOL)
    save(fig, out, "report_fig_01_tier.pdf")


def fig_map(v, t, names, out):
    pres = t["presence_pooled"]
    b, ep = pres["B"]["presence"], pres["EP"]["presence"]
    ids = [i for i in names if max(b.get(i) or 0, ep.get(i) or 0) >= 0.10]
    ids.sort(key=lambda i: (ep.get(i) or 0, b.get(i) or 0))
    h = max(3.8, 1.9 + 0.25 * len(ids))
    fig, ax = plt.subplots(figsize=(7.5, h))
    fig.subplots_adjust(top=1 - 1.15 / h, bottom=0.62 / h, left=0.25, right=0.96)
    for y, i in enumerate(ids):
        x0, x1 = b.get(i) or 0, ep.get(i) or 0
        focal = i == "R01"
        ax.plot([x0, x1], [y, y], color=P["indigo"] if focal else P["gray_light"], linewidth=2.2 if focal else 1.4, zorder=1)
        ax.scatter([x0], [y], s=34, color=P["warm"], zorder=2, edgecolor="white", linewidth=0.6)
        ax.scatter([x1], [y], s=34, color=P["indigo"], zorder=3, edgecolor="white", linewidth=0.6)
        if focal:
            ax.text(max(x0, x1) + 0.025, y, f"{pct(x0)} → {pct(x1)}", va="center", fontsize=8.5,
                    fontweight="bold", color=P["indigo"])
    ax.set_yticks(range(len(ids)))
    ax.set_yticklabels([names[i] + (" (discontinued)" if i in ("R29", "R30") else "") for i in ids], fontsize=8.2)
    for lab, i in zip(ax.get_yticklabels(), ids):
        if i == "R01":
            lab.set_fontweight("bold")
            lab.set_color(P["indigo"])
    ax.set_xlim(-0.02, 1.08)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"], fontsize=CS.FONT_SIZES["axis_tick"])
    ax.grid(axis="x", color=P["gray_light"], linewidth=0.5, zorder=0)
    ax.spines["left"].set_visible(False)
    handles = [Line2D([0], [0], marker="o", color="w", markerfacecolor=P["warm"], markersize=7, label="Beginner questions"),
               Line2D([0], [0], marker="o", color="w", markerfacecolor=P["indigo"], markersize=7, label="Enthusiast and prosumer questions")]
    ax.legend(handles=handles, loc="lower right", fontsize=CS.FONT_SIZES["legend"], frameon=True)
    CS.add_header(fig, **TEXT["map"])
    CS.add_footer(fig, verdict=FOOTER["map"], phase=PHASE, protocol=PROTOCOL)
    save(fig, out, "report_fig_02_map.pdf")


def _model_rows():
    return POST + PRE  # top-to-bottom order after inversion handled below


def fig_legacy(v, t, out):
    per = v["H_LegacySlot"]["per_model"]
    gen = t["gen_codes_recommendation_by_model"]
    aware = t["r2_aware"]
    order = _model_rows()
    ys = {m: (len(order) - 1 - k) + (0.6 if m in POST else 0) for k, m in enumerate(order)}
    fig, ax = plt.subplots(figsize=(7.5, 4.9))
    fig.subplots_adjust(top=0.76, bottom=0.2, left=0.2, right=0.95)
    cats = [("R1-only", "Names only the R1", P["warm"]), ("Both", "Names R1 and R2", P["warm_t3"]),
            ("R2-only", "Names only the R2 / R2 Pro", P["indigo"]), ("Unspecified", "Names no generation", P["gray_light"])]
    maxn = max(sum(gen[m].get(c, 0) for c, _, _ in cats) for m in SLOTS) or 1
    for m in order:
        left = 0
        for c, _, col in cats:
            n = gen[m].get(c, 0)
            if n:
                ax.barh(ys[m], n, left=left, color=col, height=0.62, edgecolor="white", linewidth=0.8)
                ax.text(left + n / 2, ys[m], str(n), ha="center", va="center", fontsize=8,
                        color="white" if c in ("R1-only", "R2-only") else P["black"])
                left += n
        if left == 0:
            ax.text(0.2, ys[m], "never names Aillio in a recommendation", va="center", fontsize=7.8,
                    color=P["gray"], fontstyle="italic")
        else:
            ax.text(left + 0.25, ys[m], f"{left} of 18", va="center", fontsize=7.8, color=P["gray"])
    ax.set_yticks([ys[m] for m in order])
    ax.set_yticklabels([MODEL[m] for m in order], fontsize=8.4)
    ax.set_xlim(0, 18)
    ax.set_xlabel("Recommendation answers that name Aillio (of 18 prompts per model)", fontsize=CS.FONT_SIZES["axis_label"])
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="x", labelsize=CS.FONT_SIZES["axis_tick"])
    ytop_post = max(ys[m] for m in POST) + 0.55
    ytop_pre = max(ys[m] for m in PRE) + 0.55
    ax.text(0, ytop_post, "Trained after the R2 launch (July 2024)", fontsize=8, color=P["gray"], va="bottom")
    ax.text(0, ytop_pre, "Trained before the R2 existed", fontsize=8, color=P["gray"], va="bottom")
    ax.set_ylim(-0.6, ytop_post + 0.6)
    handles = [Patch(color=col, label=lab) for _, lab, col in cats]
    fig.legend(handles=handles, loc="lower left", bbox_to_anchor=(0.2, 0.065), ncol=4, fontsize=7.6, frameon=False)
    CS.add_header(fig, **TEXT["legacy"])
    CS.add_footer(fig, verdict=FOOTER["legacy"], phase=PHASE, protocol=PROTOCOL)
    save(fig, out, "report_fig_03_legacy.pdf")


def fig_lineup(root, out):
    audit = json.loads((root / "data" / "v38_coder_audit.json").read_text(encoding="utf-8"))
    lab = audit["probe_labels"]
    cols = [("K1_newest_model", "What is the newest\nAillio Bullet?"), ("K2_current_lineup", "Which models does\nAillio sell now?"),
            ("K3_which_to_buy", "I've chosen a Bullet.\nWhich model?"), ("K4_R1_still_made", "Is the Bullet R1\nstill in production?")]
    order = POST + PRE
    fig, ax = plt.subplots(figsize=(7.5, 4.9))
    fig.subplots_adjust(top=0.74, bottom=0.12, left=0.2, right=0.985)
    nr, nc = len(order), len(cols)
    for ci, (key, head) in enumerate(cols):
        ax.text(ci + 0.5, nr + 0.12, head, ha="center", va="bottom", fontsize=8, fontweight="bold", color=P["black"])
        for ri, m in enumerate(order):
            y = nr - 1 - ri
            ax.add_patch(plt.Rectangle((ci + 0.03, y + 0.06), 0.94, 0.88, color=P["warm_t3"], ec="none", alpha=0.55))
            txt = lab[key][m]
            txt = txt.replace(" (says revisions 'don't warrant ... an \"R2\"')", "\n(says revisions \u201cdon\u2019t\nwarrant\u201d an R2)")
            txt = txt.replace(", or an 'upcoming R1 V3'", "\nor an \u2018upcoming R1 V3\u2019")
            txt = txt.replace(" and ", " +\n").replace(" / ", " /\n").replace(" or ", " or\n") if len(txt) > 16 and "\n" not in txt else txt
            ax.text(ci + 0.5, y + 0.5, txt, ha="center", va="center", fontsize=7.6, color=P["warm_sec"], linespacing=1.15)
    ax.set_xlim(0, nc)
    ax.set_ylim(-0.05, nr + 0.95)
    ax.set_yticks([nr - 1 - ri + 0.5 for ri in range(nr)])
    ax.set_yticklabels([MODEL[m] for m in order], fontsize=8.4)
    ax.set_xticks([])
    for sp in ("left", "bottom", "top", "right"):
        ax.spines[sp].set_visible(False)
    ax.axhline(len(PRE), color=P["gray"], linewidth=0.6, linestyle=(0, (2, 2)))
    CS.add_header(fig, **TEXT["lineup"])
    CS.add_footer(fig, verdict=FOOTER["lineup"], phase=PHASE, protocol=PROTOCOL)
    save(fig, out, "report_fig_04_lineup.pdf")


def fig_grounding(root, v, out):
    """Right specs, wrong machine: analyst-audited spec accuracy vs the generation named."""
    audit = json.loads((root / "data" / "v38_coder_audit.json").read_text(encoding="utf-8"))
    bat, heat = audit["D4_batch"], audit["D4_heating"]
    per = v["H_LegacySlot"]["per_model"]
    n_rec = sum(m["n_specified"] for m in per.values())
    k_r2 = sum(m["n_r2_only"] + m["n_both"] for m in per.values())
    rows = [
        ("Batch capacity stated correctly", "1 kg maximum", bat["correct"], bat["correct"] + bat["incorrect"],
         "statements", P["indigo"]),
        ("Heating method stated correctly", "induction", heat["correct"], heat["correct"] + heat["incorrect"],
         "statements", P["indigo"]),
        ("Current generation named", "R2 or R2 Pro", k_r2, n_rec, "recommendations", P["warm"]),
    ]
    h = 3.5
    fig, ax = plt.subplots(figsize=(7.5, h))
    fig.subplots_adjust(top=1 - 1.08 / h, bottom=0.62 / h, left=0.30, right=0.78)
    ys = [2, 1, 0]
    for y, (lab, sub, k, n, unit, col) in zip(ys, rows):
        share = k / n if n else 0.0
        ax.barh(y, 1.0, height=0.46, color=P["gray_light"], alpha=0.5, zorder=1)
        if share > 0:
            ax.barh(y, share, height=0.46, color=col, zorder=2)
        else:
            ax.plot([0, 0], [y - 0.23, y + 0.23], color=col, linewidth=2.4, zorder=3, solid_capstyle="butt")
        ax.text(1.03, y + 0.08, pct(share), va="center", ha="left", fontsize=13, fontweight="bold", color=col)
        ax.text(1.03, y - 0.24, f"{k} of {n} {unit}", va="center", ha="left", fontsize=7.8, color=P["gray"])
    ax.set_yticks(ys)
    ax.set_yticklabels([f"{lab}\n({sub})" for lab, sub, *_ in rows], fontsize=8.6)
    ax.set_xlim(0, 1.0)
    ax.set_ylim(-0.6, 2.6)
    ax.set_xticks([])
    for sp in ("left", "bottom", "top", "right"):
        ax.spines[sp].set_visible(False)
    ax.tick_params(axis="y", length=0, pad=8)
    CS.add_header(fig, **TEXT["grounding"])
    CS.add_footer(fig, verdict=FOOTER["grounding"], phase=PHASE, protocol=PROTOCOL)
    save(fig, out, "report_fig_05_grounding.pdf")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(ROOT / "osf/v38"))
    ap.add_argument("--out", default=str(ROOT / "reports/figs/v38/report"))
    a = ap.parse_args()
    CS.setup()
    v, t, coded, names = load(Path(a.root))
    out = Path(a.out)
    fig_tier(v, t, out)
    fig_map(v, t, names, out)
    fig_legacy(v, t, out)
    fig_lineup(Path(a.root), out)
    fig_grounding(Path(a.root), v, out)


if __name__ == "__main__":
    main()
