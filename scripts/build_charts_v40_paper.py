#!/usr/bin/env python3
"""v0.40 paper figures (academic register): one figure per pre-registered hypothesis.

Every plotted value and every label number is read from osf/v40/v40_values.json (values_v0_40.py), by key;
nothing is typed. Labels use the values file's display strings. Figure titles say what is plotted and never
repeat the finding's heading (CLAUDE.md, chart rule of Nov 9, 2026).

Run from the repo or worktree root:  ~/aias/venv/bin/python scripts/build_charts_v40_paper.py
Outputs: reports/figs/v40/paper/fig_0N_<name>.pdf
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import chart_style as CS  # noqa: E402

VALUES = json.loads((ROOT / "osf/v40/v40_values.json").read_text(encoding="utf-8"))["values"]
OUT = ROOT / "reports/figs/v40/paper"

INDIGO = "#37237B"
GREY = "#6E6E6E"
LIGHT = "#CCCCCC"
FAILZ = "#E4E4E4"
INK = "#1A1A1A"
SOURCE = ("Source: AIAS™ v0.40, osf/v40/v40_values.json; pre-registration v0.40-prereg-r1 (OSF ec6wh/v40); "
          "Protocol v1.2 (SSRN 6761698). Third System™")


def v(key):
    return VALUES[key]["value"]


def d(key):
    return VALUES[key]["display"]


def header(fig, title, subtitle):
    fig.text(0.02, 0.985, title, fontsize=12, fontweight="bold", color=INK, ha="left", va="top")
    fig.text(0.02, 0.935, subtitle, fontsize=9, color=GREY, ha="left", va="top")
    fig.add_artist(plt.Line2D([0.02, 0.98], [0.895, 0.895], color=INDIGO, linewidth=0.8))
    fig.text(0.02, 0.012, SOURCE, fontsize=6.5, color=GREY, fontstyle="italic", ha="left", va="bottom")


def save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / f"{name}.pdf"
    fig.savefig(p)
    plt.close(fig)
    print("wrote", p.relative_to(ROOT))


def dotplot(ax, rows, xlim, refs, xlabel):
    """rows: list of (label, x, passed, annotation) or a group header (label, None, None, None)."""
    n = len(rows)
    for i, (lab, x, ok, ann) in enumerate(rows):
        y = n - 1 - i
        if x is None:
            ax.text(-0.03, y, lab, fontsize=8.5, fontweight="bold", color=INK, ha="right", va="center",
                    transform=ax.get_yaxis_transform())
            continue
        ax.plot([xlim[0], xlim[1]], [y, y], color="#EFEFEF", linewidth=0.6, zorder=0)
        ax.scatter([x], [y], s=46, zorder=3, color=INDIGO if ok else "white", edgecolor=INDIGO if ok else GREY,
                   linewidth=1.2)
        ax.text(x, y + 0.33, ann, fontsize=7, color=INK if ok else GREY, ha="center", va="bottom")
    for xr, lab in refs:
        ax.axvline(xr, color=GREY, linewidth=0.8, linestyle=(0, (3, 2)), zorder=1)
        ax.text(xr, n + 0.05, lab, fontsize=7, color=GREY, ha="center", va="bottom")
    ax.set_yticks([n - 1 - i for i, r in enumerate(rows) if r[1] is not None])
    ax.set_yticklabels([r[0] for r in rows if r[1] is not None], fontsize=8)
    ax.set_xlim(*xlim)
    ax.set_ylim(-0.7, n + 0.6)
    ax.set_xlabel(xlabel, fontsize=8.5, color=INK)
    ax.tick_params(axis="x", labelsize=8)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)


def rho_row(label, base):
    ok = v(f"{base}.pass") if f"{base}.pass" in VALUES else None
    return (label, v(f"{base}.rho"), bool(ok), f"ρ {d(base + '.rho')}, p {d(base + '.p_perm')}")


def fig1_reinforce():
    rows = [("Airlines", None, None, None),
            rho_row("All nine models", "H_Reinforce.airline"),
            rho_row("Legacy six", "sensitivity.S-Arm.legacy.H_Reinforce.airline"),
            rho_row("Current three", "sensitivity.S-Arm.current.H_Reinforce.airline"),
            rho_row("Ambiguous names in (S-Ambig)", "sensitivity.S-Ambig.H_Reinforce.airline"),
            rho_row("Operating share (S-Operating)", "sensitivity.S-Operating.H_Reinforce_airline"),
            rho_row("Sun Country in Allegiant (S-SunCountry)", "sensitivity.S-SunCountry.H_Reinforce_airline"),
            ("Banks", None, None, None),
            rho_row("All nine models", "H_Reinforce.bank"),
            rho_row("Legacy six", "sensitivity.S-Arm.legacy.H_Reinforce.bank"),
            rho_row("Current three", "sensitivity.S-Arm.current.H_Reinforce.bank"),
            rho_row("Ambiguous names in (S-Ambig)", "sensitivity.S-Ambig.H_Reinforce.bank")]
    s = ("Without brokerage holders (S-D4)", v("sensitivity.S-D4.rho"),
         v("sensitivity.S-D4.p_perm") < 0.05 and v("sensitivity.S-D4.rho") >= v("thresholds.reinforce_rho"),
         f"ρ {d('sensitivity.S-D4.rho')}, p {d('sensitivity.S-D4.p_perm')}")
    rows.append(s)
    fig, ax = plt.subplots(figsize=(7.5, 5.6))
    fig.subplots_adjust(left=0.36, right=0.97, top=0.83, bottom=0.12)
    header(fig, "Spearman rank correlation of market share with AI share, by panel and specification",
           "Filled: rule met ($\\rho \\geq$ " + d("thresholds.reinforce_rho") + " and one-sided permutation p < 0.05). Open: rule not met.")
    dotplot(ax, rows, (0.0, 1.0), [(v("thresholds.reinforce_rho"), "registered " + d("thresholds.reinforce_rho"))], "Spearman ρ")
    save(fig, "fig_01_reinforce")


def ratio_row(label, base):
    amp = v(f"{base}.amplified")
    return (label, v(f"{base}.ratio"), bool(amp), f"{d(base + '.ratio')} ({d(base + '.k')} of {d(base + '.n')})")


def fig2_amplify():
    # each row: (label, verdict-file key base, ceiling key base); the ceiling is the post-scoring check of
    # DEVIATIONS Entry 2 (osf/v40/v40_postscore.json via the values file), not a pre-registered statistic
    spec = [("Airlines: American (Delta in S-Operating)", None, None),
            ("All nine models", "H_Amplify.airline", "ceiling.specs.all_nine.airline"),
            ("Legacy six", "sensitivity.S-Arm.legacy.H_Amplify.airline", "ceiling.specs.legacy.airline"),
            ("Current three", "sensitivity.S-Arm.current.H_Amplify.airline", "ceiling.specs.current.airline"),
            ("Ambiguous names in (S-Ambig)", "sensitivity.S-Ambig.H_Amplify.airline", "ceiling.specs.S-Ambig.airline"),
            ("Operating share, Delta (S-Operating)", "sensitivity.S-Operating.H_Amplify_airline",
             "ceiling.specs.S-Operating.airline"),
            ("Sun Country in Allegiant (S-SunCountry)", "sensitivity.S-SunCountry.H_Amplify_airline",
             "ceiling.specs.S-SunCountry.airline"),
            ("Banks: JPMorgan Chase holder", None, None),
            ("All nine models", "H_Amplify.bank", "ceiling.specs.all_nine.bank"),
            ("Legacy six", "sensitivity.S-Arm.legacy.H_Amplify.bank", "ceiling.specs.legacy.bank"),
            ("Current three", "sensitivity.S-Arm.current.H_Amplify.bank", "ceiling.specs.current.bank")]
    for _, base, cb in spec:            # the ceiling rows must describe the same ratio as the verdict-file rows
        if base:
            assert v(f"{base}.k") == v(f"{cb}.k") and v(f"{base}.n") == v(f"{cb}.n"), (base, cb)
    rows = [(lab, None, None, None) if base is None else ratio_row(lab, base) for lab, base, _ in spec]
    fig, ax = plt.subplots(figsize=(7.5, 5.4))
    fig.subplots_adjust(left=0.36, right=0.97, top=0.80, bottom=0.13)
    header(fig, "Leader's share of AI naming divided by its market share, with the most the ratio could reach",
           "Dots: ratio (k of n); none reached the registered threshold. Grey ticks: largest ratio at the observed "
           "breadth (DEVIATIONS Entry 2).")
    dotplot(ax, rows, (0.0, 1.6), [(1.0, "parity 1.0"), (v("thresholds.amplify_ratio"), "registered " + d("thresholds.amplify_ratio"))],
            "Ratio (k/n) / p₀")
    n = len(rows)
    for i, (_, base, cb) in enumerate(spec):
        if base is None:
            continue
        y = n - 1 - i
        c = v(f"{cb}.ceiling_ratio")
        ax.plot([v(f"{base}.ratio"), c], [y, y], color=LIGHT, linewidth=1.6, zorder=1, solid_capstyle="butt")
        ax.plot([c, c], [y - 0.26, y + 0.26], color=GREY, linewidth=1.8, zorder=2)
        ax.text(c + 0.015, y - 0.05, d(f"{cb}.ceiling_ratio"), fontsize=6.5, color=GREY, ha="left", va="center",
                bbox=dict(facecolor="white", edgecolor="none", pad=0.4), zorder=4)
    save(fig, "fig_02_amplify")


def fig3_afterlife():
    specs = [("All nine models", "H_Afterlife"), ("Legacy six", "sensitivity.S-Arm.legacy.H_Afterlife"),
             ("Current three", "sensitivity.S-Arm.current.H_Afterlife"),
             ("Ambiguous names in (S-Ambig)", "sensitivity.S-Ambig.H_Afterlife"),
             ("Legal-date gaps (S-Legal)", "sensitivity.S-Legal.H_Afterlife")]
    fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.9), sharey=True)
    fig.subplots_adjust(left=0.27, right=0.98, top=0.78, bottom=0.17, wspace=0.08)
    header(fig, "Share of ghost × model pairs named without a gone-flag in recommendation answers",
           "Bars: afterlife rate (afterlife pairs of pre-cutoff pairs). Dashed: registered null 5% and pass line 20%.")
    for ax, cat, ttl in ((axes[0], "airline", "Airlines (7 ghosts)"), (axes[1], "bank", "Banks (17 ghosts)")):
        ys = list(range(len(specs)))[::-1]
        for y, (lab, base) in zip(ys, specs):
            k = f"{base}.{cat}"
            r = v(k + ".rate")
            ax.barh(y, r, height=0.55, color=LIGHT if not v(k + ".pass") else INDIGO)
            ax.text(r + 0.006, y, f"{d(k + '.rate')} ({d(k + '.afterlife_pairs')} of {d(k + '.pairs')})",
                    fontsize=7, color=INK, va="center")
        for xr in (v("thresholds.afterlife_null"), v("thresholds.afterlife_rate")):
            ax.axvline(xr, color=GREY, linewidth=0.8, linestyle=(0, (3, 2)))
        ax.set_xlim(0, 0.30)
        ax.set_xticks([0, 0.05, 0.10, 0.20, 0.30])
        ax.set_xticklabels(["0%", "5%", "10%", "20%", "30%"], fontsize=7.5)
        ax.set_title(ttl, fontsize=9, loc="left", color=INK)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
    axes[0].set_yticks(list(range(len(specs)))[::-1])
    axes[0].set_yticklabels([s[0] for s in specs], fontsize=8)
    save(fig, "fig_03_afterlife")


def fig4_decay():
    specs = [("All nine models", "H_Decay"), ("Legacy six", "sensitivity.S-Arm.legacy.H_Decay"),
             ("Current three", "sensitivity.S-Arm.current.H_Decay"),
             ("Ambiguous names in (S-Ambig)", "sensitivity.S-Ambig.H_Decay"),
             ("Legal-date gaps (S-Legal)", "sensitivity.S-Legal.H_Decay"),
             ("Without length-flagged answers (S-Length)", "sensitivity.S-Length.H_Decay")]
    rows = []
    for lab, b in specs:
        ok = v(b + ".verdict") == "CONFIRMED"
        rows.append((lab, v(b + ".rho"), ok, f"ρ {d(b + '.rho')}, p {d(b + '.p_perm')}; "
                     f"{d(b + '.pairs_present')} of {d(b + '.pairs')} pairs named"))
    fig, ax = plt.subplots(figsize=(7.5, 3.9))
    fig.subplots_adjust(left=0.36, right=0.97, top=0.78, bottom=0.16)
    header(fig, "Spearman correlation of exit-to-cutoff gap with ghost Presence, by panel and specification",
           "Filled: $\\rho \\leq$ " + d("thresholds.decay_rho") + " and p < 0.05 (registered CONFIRMED band). Evaluable only with " + d("thresholds.decay_min_present") + " or more "
           "pairs named.")
    dotplot(ax, rows, (-0.6, 0.1), [(v("thresholds.decay_rho"), "registered " + d("thresholds.decay_rho")), (0.0, "0")],
            "Spearman ρ (gap in months, ghost Presence)")
    save(fig, "fig_04_decay")


def fig5_flag():
    specs = [("All nine models", "H_Flag"), ("Legacy six", "sensitivity.S-Arm.legacy.H_Flag"),
             ("Current three", "sensitivity.S-Arm.current.H_Flag"),
             ("Without Discover (S-Discover)", "sensitivity.S-Discover")]
    fig, ax = plt.subplots(figsize=(7.5, 4.0))
    fig.subplots_adjust(left=0.30, right=0.97, top=0.78, bottom=0.15)
    header(fig, "Share of status answers that say the brand is gone: ghosts against living brands",
           "Search off, all runs. Dark: ghost answers (pre-cutoff exits). Light: control answers "
           "(living-brand controls and incumbents).")
    n = len(specs)
    for i, (lab, b) in enumerate(specs):
        y = (n - 1 - i) * 1.0
        g, c = v(b + ".ghost_rate"), v(b + ".control_rate")
        ax.barh(y + 0.18, g, height=0.34, color=INDIGO)
        ax.barh(y - 0.18, c, height=0.34, color=LIGHT)
        ax.text(g + 0.01, y + 0.18, f"{d(b + '.ghost_rate')} ({d(b + '.ghost_flagged')} of {d(b + '.ghost_answers')})",
                fontsize=7, va="center", color=INK)
        ax.text(c + 0.01, y - 0.18,
                f"{d(b + '.control_rate')} ({d(b + '.control_flagged')} of {d(b + '.control_answers')})",
                fontsize=7, va="center", color=INK)
    ax.axvline(v("thresholds.flag_rate"), color=GREY, linewidth=0.8, linestyle=(0, (3, 2)))
    ax.text(v("thresholds.flag_rate"), n - 0.45, "registered 80%", fontsize=7, color=GREY, ha="center")
    ax.set_yticks([(n - 1 - i) for i in range(n)])
    ax.set_yticklabels([s[0] for s in specs], fontsize=8)
    ax.set_xlim(0, 1.18)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"], fontsize=7.5)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    save(fig, "fig_05_flag")


def fig6_search():
    fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.6), gridspec_kw={"width_ratios": [1.25, 1]})
    fig.subplots_adjust(left=0.20, right=0.97, top=0.76, bottom=0.17, wspace=0.75)
    header(fig, "Ghost status cells of the current models, search off against search on",
           "Left: discordant (ghost, model) cells; the McNemar part needs 10 or more. "
           "Right: post-cutoff exits flagged with search on.")
    ax = axes[0]
    labs = ["Flagged with search on only", "Flagged with search off only"]
    vals = [v("H_Search.s1_only_flagged"), v("H_Search.s0_only_flagged")]
    disp = [d("H_Search.s1_only_flagged"), d("H_Search.s0_only_flagged")]
    ax.barh([1, 0], vals, height=0.5, color=[LIGHT, LIGHT])
    for y, x, t in zip([1, 0], vals, disp):
        ax.text(x + 0.15, y, t, fontsize=7.5, va="center", color=INK)
    ax.axvline(v("thresholds.search_min_discordant"), color=GREY, linewidth=0.8, linestyle=(0, (3, 2)))
    ax.text(v("thresholds.search_min_discordant"), 1.45, "10 discordant", fontsize=7, color=GREY, ha="center")
    ax.set_yticks([1, 0])
    ax.set_yticklabels(labs, fontsize=8)
    ax.set_xlim(0, 11)
    ax.set_ylim(-0.6, 1.8)
    ax.set_xlabel(f"Cells, of {d('H_Search.paired_cells')} paired (McNemar p {d('H_Search.p_mcnemar_exact')})",
                  fontsize=8)
    ax = axes[1]
    r = v("H_Search.post_cutoff_s1_rate")
    ax.bar([0], [r], width=0.5, color=INDIGO)
    ax.text(0, r + 0.03, f"{d('H_Search.post_cutoff_s1_rate')} ({d('H_Search.post_cutoff_s1_flagged')} of "
            f"{d('H_Search.post_cutoff_cells')})", fontsize=7.5, ha="center", color=INK)
    ax.axhline(v("thresholds.search_post_rate"), color=GREY, linewidth=0.8, linestyle=(0, (3, 2)))
    ax.text(0.32, v("thresholds.search_post_rate") + 0.02, "registered 80%", fontsize=7, color=GREY, ha="left")
    ax.set_xticks([0])
    ax.set_xticklabels(["Post-cutoff cells"], fontsize=8)
    ax.set_xlim(-0.5, 1.0)
    ax.set_ylim(0, 1.18)
    ax.set_yticks([0, 0.5, 1.0])
    ax.set_yticklabels(["0%", "50%", "100%"], fontsize=7.5)
    for a in axes:
        for s in ("top", "right"):
            a.spines[s].set_visible(False)
    save(fig, "fig_06_search")


def main():
    CS.setup()
    plt.rcParams["axes.unicode_minus"] = False
    for f in (fig1_reinforce, fig2_amplify, fig3_afterlife, fig4_decay, fig5_flag, fig6_search):
        f()


if __name__ == "__main__":
    main()
