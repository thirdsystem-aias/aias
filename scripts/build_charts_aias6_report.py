#!/usr/bin/env python3
"""
AIAS 6.0 Preview (provisional) -- report figures (managerial register, report design system v2, data-viz rules v2).

One chart per finding (reports/aias6_preview_report_content.py, CHARTS and FINDINGS). Title and subtitle are the
content module's (tested: a chart title never repeats or paraphrases its finding's title); the one insight is stated
on the chart in Indigo and is built only from {{v:KEY}} values (papers/aias_6_0_preview/tokens_aias6.py), so it
reports a value and never an outcome claim of its own; everything else is in neutrals. Every plotted number is a
leaf of the scorer's outputs (results JSON, profile CSV); nothing is re-scored or typed.

  report_fig_01_pairs                  S-tests of the included parts with 90% intervals and the pre-set bars; parts
                                       under review below a rule, descriptive (STRUCT)
  report_fig_02_presence_consistency   Presence rank against Consistency rank, centred within category (STRUCT)
  report_fig_03_part_states            each part in the column of its state at the data lock
  report_fig_04_parts_per_brand        brands by number of included parts rated, per category (D9; STRUCT)
  report_fig_05_average_vs_presence    rank correlation of the parts' equal-weight average with Presence, against
                                       the pre-set limit, beside each included part's own (STRUCT)

SYNTHETIC outputs: --watermark is required, every file name starts with SYNTHETIC_, every chart carries the
diagonal watermark and a SYNTHETIC source line, and the output folder must be outside the repository. Real
outputs: --watermark is refused.

  python3 scripts/build_charts_aias6_report.py --outputs DIR [--out DIR] [--watermark TEXT]
"""
import argparse
import csv
import importlib.util
import sys
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "papers/aias_6_0_preview"))
import chart_style as cs  # noqa: E402
import aias6_values as VV  # noqa: E402
import tokens_aias6 as T  # noqa: E402
cs.setup()

_spec = importlib.util.spec_from_file_location("aias6_rc", ROOT / "reports" / "aias6_preview_report_content.py")
RC = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(RC)

INDIGO = "#37237B"
IRIS = "#908EC5"
LAVENDER = "#BBB9DD"
GREY = "#6E6E6E"
LIGHT = "#CCCCCC"
FAILZ = "#E4E4E4"
INK = "#1A1A1A"
WARMBG = "#EFEFEF"
W = 7.5
SOURCE = ("Source: Third System™, AIAS™ 6.0 Preview (provisional), pre-registration {tag} (osf.io/ec6wh, "
          "aias_6_0_preview); values read from the locked scorer's outputs.")
SYN_SOURCE = "SYNTHETIC TEST DATA — NOT RESULTS. Invented brands and scores, made to exercise the pipeline."
CHART_KEYS = ["report_fig_01_pairs", "report_fig_02_presence_consistency", "report_fig_03_part_states",
              "report_fig_04_parts_per_brand", "report_fig_05_average_vs_presence"]


class Ctx:
    def __init__(self, outputs, synthetic, watermark):
        self.outputs = Path(outputs)
        self.tok = T.context(outputs, synthetic=synthetic)
        self.res = self.tok["src"]["results"]
        self.synthetic = synthetic
        self.watermark = watermark
        # the charts of the findings this outcome keeps (a chart is built only for a finding that prints it)
        kept = {f["chart"] for f in T.fill_content(RC.FINDINGS, self.tok)}
        self.charts = {k: v for k, v in T.fill_content(RC.CHARTS, self.tok).items() if v is not None and k in kept}

    def v(self, key):
        return T.resolve(key, self.tok)

    def profile(self):
        with open(self.outputs / VV.NAMES["profile"], encoding="utf-8", newline="") as fh:
            return list(csv.DictReader(fh))


def file_name(key, synthetic):
    return ("SYNTHETIC_" if synthetic else "") + key + ".pdf"


def frame(X, key, insight, h):
    spec = X.charts[key + ".pdf"]
    fig = plt.figure(figsize=(W, h))
    fig.text(0.0, 1 - 0.07 / h, spec["title"], fontsize=10.5, fontweight="bold", color=INK, ha="left", va="top")
    fig.text(0.0, 1 - 0.30 / h, spec["subtitle"], fontsize=7.8, color=GREY, ha="left", va="top")
    fig.text(0.0, 1 - 0.52 / h, insight, fontsize=9, color=INDIGO, ha="left", va="top")
    fig.text(0.0, 0.0, SOURCE.format(tag=X.v("pv.prereg_tag")), fontsize=6.5, color=GREY, ha="left", va="bottom")
    if X.synthetic:
        fig.text(0.0, 0.14 / h, SYN_SOURCE, fontsize=6.8, color="#B5441A", fontweight="bold", ha="left",
                 va="bottom")
    return fig


def save(X, fig, key, out):
    if X.watermark:
        fig.text(0.5, 0.5, X.watermark, rotation=22, fontsize=26, color="#F36C35", alpha=0.25, ha="center",
                 va="center", fontweight="bold", zorder=100)
    out.mkdir(parents=True, exist_ok=True)
    p = out / file_name(key, X.synthetic)
    fig.savefig(p)
    plt.close(fig)
    print(f"  wrote {p}")
    return p


def clean(ax, left=False):
    for s in ("top", "right") + (() if left else ("left",)):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis="both", labelsize=7.5, length=0)


def num(x, nd=2):
    s = (VV.r2 if nd == 2 else VV.r3)(x)
    return s.replace("-", "−")


def cap(s):
    return s[:1].upper() + s[1:]


def fig_01(X, out):
    st = X.res["structure"]
    rows = [(t, False) for t in (st.get("S_tests") or {}).values()]
    rows += [(t, True) for t in (st.get("descriptive_marginal_pairs") or {}).values()]
    n = len(rows)
    h = 1.95 + (0.27 if n <= 9 else 0.19) * n          # six parts: 15 pairs; the page keeps room for the body
    fig = frame(X, "report_fig_01_pairs",
                f"{cap(X.v('pv.structure.d'))} of {X.v('pv.structure.k')} included parts separate or partly "
                f"separate; structure test {X.v('pv.structure.verdict')}", h)
    ax = fig.add_axes([0.30, 0.55 / h + 0.12, 0.56, 1 - (0.55 / h + 0.12) - 0.85 / h])
    conf, fals = float(X.tok["scorer"].SEP_CONF), float(X.tok["scorer"].SEP_FALS)
    ax.axvspan(-conf, conf, color=WARMBG, zorder=0, lw=0)
    for x0 in (-fals, fals):
        ax.axvline(x0, color=GREY, lw=0.7, ls=(0, (3, 2)), zorder=1)
    ax.axvline(0, color=LIGHT, lw=0.6, zorder=1)
    labels = []
    nk = sum(1 for _, d in rows if not d)
    GAP = 0.8 if nk < n else 0.0                    # space between the included pairs and the parts under review
    ys = [n - 1 - i + (GAP if i < nk else 0.0) for i in range(n)]
    for i, (t, desc) in enumerate(rows):
        y = ys[i]
        a, b = t["pair"]
        labels.append(f"{VV.NAME[a]} and {VV.NAME[b]}")
        if t.get("rho") is None:
            ax.text(0, y, "not computed", fontsize=7, color=GREY, ha="center", va="center")
            continue
        ci = t.get("ci90") or [None, None]
        if not desc and ci[0] is not None and ci[1] is not None:
            ax.plot(ci, [y, y], color=LAVENDER, lw=2.4, solid_capstyle="round", zorder=2)
        ax.scatter([t["rho"]], [y], s=34, color=GREY if desc else INDIGO, marker="D" if desc else "o", zorder=3,
                   edgecolor="white", linewidth=0.4)
        ax.text(1.04, y, "descriptive" if desc else t["verdict"], fontsize=6.8, color=GREY if desc else INK,
                va="center", ha="left", transform=ax.get_yaxis_transform())
        ax.text(t["rho"], y + 0.32, num(t["rho"]), fontsize=6.6, color=INK, ha="center", va="bottom")
    if nk < n:
        ymid = n - nk - 0.5 + GAP / 2
        ax.axhline(ymid, color=GREY, lw=0.5)
        ax.text(-0.98, ymid - 0.12, "Parts under review (no verdict)", fontsize=6.6, color=GREY, va="top",
                ha="left")
    top = n - 1 + GAP
    ax.set_yticks(ys, labels, fontsize=7.6)
    ax.set_xlim(-1, 1)
    ax.set_ylim(-0.7, top + 0.8)
    ax.text(conf, top + 0.55, f"±{num(conf)}", fontsize=6.6, color=GREY, ha="center", va="bottom")
    ax.text(fals, top + 0.55, f"±{num(fals)}", fontsize=6.6, color=GREY, ha="center", va="bottom")
    ax.set_xlabel("Rank correlation within category (dot) and its 90% interval (bar); shaded: separate", fontsize=7.4)
    clean(ax)
    return save(X, fig, "report_fig_01_pairs", out)


def _centred_ranks(vals):
    order = sorted(range(len(vals)), key=lambda i: vals[i])
    ranks = [0.0] * len(vals)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and vals[order[j + 1]] == vals[order[i]]:
            j += 1
        for k in range(i, j + 1):
            ranks[order[k]] = (i + j) / 2 + 1
        i = j + 1
    m = len(vals)
    return [(r - (m + 1) / 2) / m for r in ranks]


def fig_02(X, out):
    by = defaultdict(list)
    for row in X.profile():
        if row.get("P_rated") == "1" and row.get("C_rated") == "1" and row["P"] and row["C"]:
            by[row["substrate"]].append((float(row["P"]), float(row["C"])))
    cats = [c for c in VV.SUBS if c in by]
    h = 3.1
    fig = frame(X, "report_fig_02_presence_consistency",
                f"Rank correlation within categories {X.v('pv.pc.rho')} (90% interval {X.v('pv.pc.lo')} to "
                f"{X.v('pv.pc.hi')}); pre-set bar {X.v('pv.band.confirm')}", h)
    gap, x0, wtot = 0.018, 0.06, 0.92
    pw = (wtot - gap * (len(cats) - 1)) / max(1, len(cats))
    for i, c in enumerate(cats):
        ax = fig.add_axes([x0 + i * (pw + gap), 0.62 / h + 0.07, pw, 1 - (0.62 / h + 0.07) - 1.0 / h])
        p = _centred_ranks([a for a, _ in by[c]])
        q = _centred_ranks([b for _, b in by[c]])
        ax.axhline(0, color=LIGHT, lw=0.5, zorder=0)
        ax.axvline(0, color=LIGHT, lw=0.5, zorder=0)
        ax.scatter(p, q, s=14, color=INDIGO, alpha=0.85, edgecolor="white", linewidth=0.3, zorder=2)
        ax.set_xlim(-0.6, 0.6)
        ax.set_ylim(-0.6, 0.6)
        ax.set_xticks([-0.5, 0, 0.5], ["low", "", "high"])
        ax.set_yticks([-0.5, 0, 0.5], ["low", "", "high"] if i == 0 else ["", "", ""])
        ax.set_title(f"{VV.CAT[c]} ({len(p)})", fontsize=7.6, color=INK, pad=3)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        ax.tick_params(axis="both", labelsize=6.6, length=0)
        if i == 0:
            ax.set_ylabel("Consistency rank", fontsize=7.2)
    fig.text(0.5, 0.40 / h + 0.035, "Presence rank within category (brands rated on both)", fontsize=7.2,
             color=INK, ha="center", va="bottom")
    return save(X, fig, "report_fig_02_presence_consistency", out)


STATE_COLUMNS = [("Published", ()), ("Passed its first test", ("PASS", "PASS_RETEST_PENDING", "PASS_AI_JUDGED")),
                 ("Under review", ("MARGINAL",)), ("Pending", ("NOT_RUN",)),
                 ("Not passed or not determined", ("FAIL", "UNDETERMINED"))]


def fig_03(X, out):
    states = X.res["gate_states"]
    K = set(X.res["K"])
    h = 3.0
    fig = frame(X, "report_fig_03_part_states", f"In the structure test: {X.v('pv.K.names')}", h)
    ax = fig.add_axes([0.13, 0.55 / h + 0.04, 0.85, 1 - (0.55 / h + 0.04) - 1.05 / h])
    n = len(VV.ORDER)
    for j in range(len(STATE_COLUMNS)):
        ax.axvspan(j - 0.46, j + 0.46, color=WARMBG if j % 2 == 0 else "white", lw=0, zorder=0)
    for i, part in enumerate(VV.ORDER):
        y = n - 1 - i
        if part in ("P", "C"):
            col, word = 0, X.res["labels"][part]["label"]
        else:
            st = states[part]
            col = next(j for j, (_, ws) in enumerate(STATE_COLUMNS) if st in ws)
            word = VV.STATE_WORD[st]
        inK = part in K
        ax.scatter([col - 0.36], [y], s=48, marker="o", zorder=3, color=INDIGO if inK else "white",
                   edgecolor=INDIGO if inK else GREY, linewidth=1.0)
        ax.text(col - 0.29, y, word, fontsize=6.9, color=INK if inK else GREY, va="center", ha="left")
    ax.set_yticks(range(n - 1, -1, -1), [VV.NAME[p] for p in VV.ORDER], fontsize=7.8)
    ax.set_xticks(range(len(STATE_COLUMNS)), [c for c, _ in STATE_COLUMNS], fontsize=7.2)
    ax.xaxis.tick_top()
    ax.set_xlim(-0.5, len(STATE_COLUMNS) - 0.5)
    ax.set_ylim(-0.6, n - 0.4)
    clean(ax)
    ax.spines["bottom"].set_visible(False)
    fig.text(0.13, 0.30 / h + 0.02, "Filled: in the structure test. Open: shown with its state, in no result.",
             fontsize=6.8, color=GREY, ha="left", va="bottom")
    return save(X, fig, "report_fig_03_part_states", out)


def fig_04(X, out):
    rpu = X.res["descriptives"]["D9_coverage"]["rated_parts_per_unit"]["K"]
    k = len(X.res["K"])
    cats = [c for c in VV.SUBS if c in rpu]
    h = 3.0
    fig = frame(X, "report_fig_04_parts_per_brand",
                f"{X.v('pv.uk.n')} of {X.v('pv.units')} brands rated on every included part", h)
    ax = fig.add_axes([0.14, 0.62 / h + 0.04, 0.70, 1 - (0.62 / h + 0.04) - 1.0 / h])
    shades = {0: FAILZ}
    mids = [LAVENDER, IRIS, "#6B5FA8", "#4E3F92"]
    for j in range(1, k):
        shades[j] = mids[min(j - 1, len(mids) - 1)]
    shades[k] = INDIGO
    left = [0.0] * len(cats)
    for j in range(k + 1):
        vals = [float(rpu[c].get(str(j), 0)) for c in cats]
        ax.barh(range(len(cats)), vals, left=left, color=shades[j], height=0.62, edgecolor="white", linewidth=0.6,
                label="all " + str(k) if j == k else f"{j} of {k}")
        for y, (l0, v) in enumerate(zip(left, vals)):
            if v >= 2:
                ax.text(l0 + v / 2, y, f"{int(v)}", fontsize=6.6, ha="center", va="center",
                        color="white" if j >= 2 else INK)
        left = [a + b for a, b in zip(left, vals)]
    ax.set_yticks(range(len(cats)), [VV.CAT[c] for c in cats], fontsize=7.6)
    ax.invert_yaxis()
    ax.set_xlabel("Brands (number of included parts on which each is rated)", fontsize=7.4)
    ax.legend(loc="center left", bbox_to_anchor=(1.01, 0.5), fontsize=6.8, frameon=False, title="parts rated",
              title_fontsize=6.8)
    clean(ax, left=True)
    return save(X, fig, "report_fig_04_parts_per_brand", out)


def fig_05(X, out):
    st = X.res["structure"]
    comp = st["composite_check"]
    k2 = float(X.tok["scorer"].K2_MAX)
    rows = [("Average of the included parts", comp["rho_A_P"], True)]
    for t in (st.get("S_tests") or {}).values():
        if t["pair"][0] == "P" and t.get("rho") is not None:
            rows.append((f"{VV.NAME[t['pair'][1]]} alone", t["rho"], False))
    n = len(rows)
    h = 1.95 + 0.30 * n
    fig = frame(X, "report_fig_05_average_vs_presence",
                f"Average against Presence: {X.v('pv.comp.rho_AP')}; pre-set limit {X.v('pv.k2_max')}", h)
    ax = fig.add_axes([0.30, 0.55 / h + 0.08, 0.62, 1 - (0.55 / h + 0.08) - 0.95 / h])
    ax.axvline(k2, color=GREY, lw=0.8, ls=(0, (3, 2)), zorder=1)
    ax.text(k2 - 0.015, n - 0.35, f"pre-set limit {num(k2)}", fontsize=6.6, color=GREY, ha="right", va="bottom")
    ax.axvline(0, color=LIGHT, lw=0.6, zorder=1)
    for i, (lab, rho, main) in enumerate(rows):
        y = n - 1 - i
        ax.plot([0, rho], [y, y], color=INDIGO if main else LIGHT, lw=1.6 if main else 1.0, zorder=2)
        ax.scatter([rho], [y], s=42 if main else 26, color=INDIGO if main else GREY, zorder=3,
                   marker="o" if main else "s", edgecolor="white", linewidth=0.4)
        ax.text(rho + (0.03 if rho >= 0 else -0.03), y + 0.22, num(rho, 3 if main else 2), fontsize=6.8,
                color=INDIGO if main else INK, ha="left" if rho >= 0 else "right", va="bottom")
    ax.set_yticks(range(n - 1, -1, -1), [r[0] for r in rows], fontsize=7.6)
    ax.set_xlim(-0.5, 1.0)
    ax.set_ylim(-0.6, n - 0.1)
    ax.set_xlabel("Rank correlation with Presence within category (descriptive; nothing adopted)", fontsize=7.4)
    clean(ax)
    return save(X, fig, "report_fig_05_average_vs_presence", out)


BUILDERS = {"report_fig_01_pairs": fig_01, "report_fig_02_presence_consistency": fig_02,
            "report_fig_03_part_states": fig_03, "report_fig_04_parts_per_brand": fig_04,
            "report_fig_05_average_vs_presence": fig_05}


def build(outputs, out, watermark=None):
    """Build the charts the content keeps for this outcome; returns {content file name: written path}."""
    src = VV.load_sources(outputs)
    synthetic = VV.is_synthetic(src)
    if synthetic and not watermark:
        raise SystemExit("[aias6 report charts] REFUSED: synthetic outputs need --watermark")
    if not synthetic and watermark:
        raise SystemExit("[aias6 report charts] REFUSED: --watermark is for synthetic runs only")
    out = Path(out).resolve()
    if synthetic and str(out).startswith(str(ROOT.resolve())):
        raise SystemExit(f"[aias6 report charts] REFUSED: synthetic charts must be written outside the repository "
                         f"({out})")
    X = Ctx(outputs, synthetic, watermark)
    made = {}
    for key in CHART_KEYS:
        if key + ".pdf" in X.charts:
            made[key + ".pdf"] = BUILDERS[key](X, out)
    return made


def main(argv=None):
    ap = argparse.ArgumentParser(description="AIAS 6.0 Preview report figures")
    ap.add_argument("--outputs", type=Path, default=VV.OUTDIR)
    ap.add_argument("--out", type=Path, default=ROOT / "reports/figs/aias6/report")
    ap.add_argument("--watermark", default=None)
    a = ap.parse_args(argv)
    print(f"building AIAS 6.0 Preview report figures -> {a.out}")
    made = build(a.outputs, a.out, a.watermark)
    print(f"done: {len(made)} charts")
    return 0


if __name__ == "__main__":
    sys.exit(main())
