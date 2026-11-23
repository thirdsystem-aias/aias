#!/usr/bin/env python3
"""
brief_v0_27_values.py -- every number printed in the brief of the combined v0.27 + v0.28 validity paper
(TS-BR-v0.27-r1; v0.28 named in the title block) and its chart.

Numbers are read by code, never typed:
  * Study 1 (v0.27, CV.03) results from its verdict file osf/v27/v0.27_verdicts.json and Study 2 (v0.28, CV.04)
    results from osf/v28/v28_verdicts.json (each written by its study's single scoring run), through the Values
    class of papers/v1_12/v112_values.py (each printed value records source, JSON path, raw value and format);
  * decision lines from the locked scorers, read as text (not imported or executed): scripts/score_v27.py writes
    the convergent lines as literals in its H_CV3_Primary call (0.60 confirms with p < 0.05, 0.74 strong, under
    0.30 falsified); scripts/score_v28.py holds the discriminant bands as constants (CONFIRMED_CEIL 0.50,
    CONVERGENT_BENCHMARK 0.74) and the dissociation lines as literals (|z difference| > 1.0, at least 4 cases).
    Each rule records the exact source line it was taken from.

The verdict files and both scorers are byte-identical to branch v0.27-28-combined (c22617f), the paper's branch,
from which the paper (Declarations) and its PDF are checked out unchanged. write_provenance() writes
reports/briefs/v0_27/brief_v0_27_provenance.json. ROOT is the worktree (AIAS_ROOT), never the main tree.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

ROOT = Path(os.environ.get("AIAS_ROOT") or Path(__file__).resolve().parents[1]).resolve()
sys.path.insert(0, str(ROOT / "papers/v1_12"))
sys.path.insert(0, str(ROOT / "reports"))
import v112_values as VV  # noqa: E402
from brief_v1_12_values import scorer_constants as _consts  # noqa: E402  (ast reader)

V27 = ROOT / "osf/v27/v0.27_verdicts.json"
V28 = ROOT / "osf/v28/v28_verdicts.json"
SCORER27 = ROOT / "scripts/score_v27.py"
SCORER28 = ROOT / "scripts/score_v28.py"
PAPER_MD = ROOT / "papers/v0_27_28/v0_27_28_combined_validity_paper.md"
PROV_OUT = ROOT / "reports/briefs/v0_27/brief_v0_27_provenance.json"
SOURCE_COMMIT = ("c22617f (branch v0.27-28-combined); v0.27_verdicts.json as written by the v0.27 scoring run "
                 "(85cab7b), v28_verdicts.json as written by the single v0.28 scoring run (65bb5ab)")

# (name, scorer, regex with one group = the literal; the source line must match exactly once)
RULE_LINES = {
    "CONF": (SCORER27, r'"status": v_convergent\(bx1, (0\.60), 0\.74, 0\.30, padj\[0\]\),'),
    "STRONG": (SCORER27, r'"status": v_convergent\(bx1, 0\.60, (0\.74), 0\.30, padj\[0\]\),'),
    "FALS": (SCORER27, r'"status": v_convergent\(bx1, 0\.60, 0\.74, (0\.30), padj\[0\]\),'),
    "ALPHA": (SCORER27, r"sig = \(p is not None and p < (0\.05)\)"),
    "Z": (SCORER28, r"if d > (1\.0):"),
    "Z_NEG": (SCORER28, r"elif d < (-1\.0):"),
    "CASES": (SCORER28, r"if cases >= (\d+) and amplified and suppressed:"),
}


def r3(x):
    return VV.r3(x)


def m3(x):
    """Signed three decimals, rounded half up on the stored decimal (as the paper prints it), true minus sign."""
    d = Decimal(repr(float(x))).quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)
    s = f"{d:.3f}"
    return "0.000" if s == "-0.000" else s.replace("-", "−")


def r2(x):
    return VV.r2(x)


def i0(x):
    return VV.i0(x)


def d_len(xs):
    return len(xs)


def scorer_rules():
    out = {}
    for name, (path, pat) in RULE_LINES.items():
        hits = re.findall(pat, path.read_text(encoding="utf-8"))
        if len(hits) != 1:
            raise SystemExit(f"rule {name}: {len(hits)} matches in {path.name}")
        out[name] = (float(hits[0]), pat, path)
    k = _consts(SCORER28)
    out["CEIL"] = (k["CONFIRMED_CEIL"], "CONFIRMED_CEIL = 0.50", SCORER28)
    out["BENCH"] = (k["CONVERGENT_BENCHMARK"], "CONVERGENT_BENCHMARK = 0.74", SCORER28)
    if out["Z_NEG"][0] != -out["Z"][0] or out["Z"][0] != int(out["Z"][0]):
        raise SystemExit("the dissociation lines are not +/- one whole standard deviation")
    if out["STRONG"][0] != out["BENCH"][0]:
        raise SystemExit("the two studies' 0.74 lines differ; the text names one benchmark")
    return out


class BriefValues(VV.Values):
    def rule(self, name, rules, fmt):
        raw, line, path = rules[name]
        s = fmt(raw)
        self.vals[name] = s
        self.prov[name] = {"kind": "rule", "source": str(path.relative_to(ROOT)), "source_line": line, "raw": raw,
                           "fmt": fmt.__name__, "formatted": s}
        return s


def _md():
    return PAPER_MD.read_text(encoding="utf-8")


# The paper's conflict-of-interest paragraph, with the employer and its companies named only as the employer's
# group (decision 4). Each replacement must occur exactly once in the paper's text.
COI_REPLACE = [
    ("The author is employed by Samsung Electronics America. Samsung had no role in the design, conduct, analysis "
     "or reporting of either study.",
     "The author is employed by a consumer-electronics company; it and its affiliates are named in the paper's "
     "Declarations. The employer had no role in the design, conduct, analysis or reporting of either study."),
    ("Neither panel contains a Samsung-group brand:", "Neither panel contains a brand of the employer's group:"),
    ("Harman International, a Samsung subsidiary,", "Harman International, a company of the employer's group,"),
    ("brands that compete with Samsung in some product categories",
     "brands that compete with the employer in some product categories"),
    ("one brand in which a Samsung subsidiary holds a significant minority equity stake (Corning, in which Samsung "
     "Display is a shareholder)",
     "one brand in which a company of the employer's group holds a significant minority equity stake (Corning)"),
    ("relationships with Samsung group companies", "relationships with companies of the employer's group"),
    ("Cheil Worldwide, a Samsung affiliate,", "Cheil Worldwide, a marketing company of the employer's group,"),
]


def coi_paragraph():
    m = re.search(r"## Conflict of interest \{-\}\n\n(.+?)\n", _md())
    if not m:
        raise SystemExit("conflict-of-interest paragraph not found in the paper's Declarations")
    s = m.group(1).strip()
    for a, b in COI_REPLACE:
        if s.count(a) != 1:
            raise SystemExit(f"COI wording differs from the expected text: {a[:60]}")
        s = s.replace(a, b)
    if "Samsung" in s:
        raise SystemExit("COI paragraph still names the employer")
    if "Harman International" not in s or "Cheil Worldwide" not in s:
        raise SystemExit("COI paragraph must name Harman and Cheil as the employer's group")
    return s


def ai_use_statement():
    m = re.search(r"## Use of AI tools \{-\}\n\n(.+?)\n", _md())
    if not m:
        raise SystemExit("AI-use statement not found in the paper's Declarations")
    return m.group(1).strip()


def load():
    A = json.loads(V27.read_text(encoding="utf-8"))
    B = json.loads(V28.read_text(encoding="utf-8"))
    if A["_meta"].get("prereg") != "v0.27-prereg-r5" or A["_meta"]["instruments_present"] != \
            {"I1": True, "I2": False, "I3": False}:
        raise SystemExit("v0.27_verdicts.json is not the v0.27 run on I1 alone")
    if not B["_meta"].get("study", "").startswith("v0.28") or B["_meta"].get("lock_module") != "matched" \
            or B["_meta"]["presence_n_joined"] != B["_meta"]["panel_n"]:
        raise SystemExit("v28_verdicts.json is not the v0.28 run with every panel brand joined")
    rules = scorer_rules()
    if B["_meta"]["convergent_benchmark"] != rules["BENCH"][0]:
        raise SystemExit("v0.28 benchmark in the verdict file differs from the scorer")
    v = BriefValues({"v27": A, "v28": B})
    S1 = ["verdicts", "H_CV3_Primary"]
    v.put("P_RHO", "v27", S1 + ["block", "rho"], r3)
    v.put("P_N", "v27", S1 + ["block", "n"], i0)
    v.put("P_PADJ", "v27", S1 + ["p_adj"], r3)
    v.put("P_LO", "v27", S1 + ["block", "ci", 0], m3)
    v.put("P_HI", "v27", S1 + ["block", "ci", 1], r3)
    T2 = ["verdicts", "_sensitivity_type2_construct_gap"]
    v.put("T2_RHO", "v27", T2 + ["H_CV3_Primary", "rho"], r3)
    v.put("T2_NEX", "v27", T2 + ["n_excluded"], i0)
    v.put("ST_RHO", "v27", ["verdicts", "_sensitivity_stride_confound", "H_CV3_Primary", "rho"], r3)
    M = ["verdicts", "H_CV3_Component", "matrix", "recall_channel_som"]
    for key, dim in (("PQ", "I1_presence_quality"), ("BRR", "I1_brand_recognition"), ("SENT", "I1_sentiment"),
                     ("MKT", "I1_market_competition")):
        v.put(key, "v27", M + [dim], r3)
    F, R = ["verdicts", "H_Disc_Familiarity"], ["verdicts", "H_Disc_Recognition"]
    v.put("F_RHO", "v28", F + ["spearman_rho"], r3)
    v.put("F_N", "v28", F + ["n"], i0)
    v.put("F_LO", "v28", F + ["bca_ci_95", 0], r3)
    v.put("F_HI", "v28", F + ["bca_ci_95", 1], r3)
    v.put("R_RHO", "v28", R + ["spearman_rho"], r3)
    v.put("R_LO", "v28", R + ["bca_ci_95", 0], m3)
    v.put("R_HI", "v28", R + ["bca_ci_95", 1], m3)
    D = ["verdicts", "H_Dissociation"]
    v.put("DISS", "v28", D + ["n_cases"], i0)
    v.derive("AMP", d_len, [("v28", D + ["amplified"])], i0)
    v.derive("SUP", d_len, [("v28", D + ["suppressed"])], i0)
    for name in ("CONF", "STRONG", "FALS", "CEIL", "BENCH"):
        v.rule(name, rules, r2)
    v.rule("ALPHA", rules, r2)
    v.rule("Z", rules, i0)
    v.rule("CASES", rules, i0)

    # -- the brief's words assume these verdicts (stop on any mismatch)
    VA = A["verdicts"]
    want27 = {"H_CV3_Primary": "FALSIFIED", "H_CV3_Profound": "NOT_RUN", "H_CV3_SOM": "NOT_RUN",
              "H_CV3_Discriminant": "NOT_RUN", "H_CV3_Recognition_Null": "CONFIRMED",
              "H_CV3_Component": "EXPLORATORY"}
    got = {h: VA[h]["status"] for h in want27}
    if got != want27:
        raise SystemExit(f"the brief's wording assumes other v0.27 verdicts: {got}")
    if VA["H_CV3_Recognition_Null"]["C_P_sd"] != 0 or VA["H_CV3_Recognition_Null"]["C_P_mean"] != 6:
        raise SystemExit("the text says every brand was recognised by all six models")
    p, t2, st = (VA["H_CV3_Primary"]["block"]["rho"], VA["_sensitivity_type2_construct_gap"]["H_CV3_Primary"]["rho"],
                 VA["_sensitivity_stride_confound"]["H_CV3_Primary"]["rho"])
    if not (st < p < t2 < rules["CONF"][0]) or p >= rules["FALS"][0] or VA["H_CV3_Primary"]["p_adj"] < 0.05:
        raise SystemExit("the text says: primary under the falsification line and not significant; dropping the "
                         "type-2 brands raises it, dropping Stride lowers it, neither reaches the confirmation line")
    m = VA["H_CV3_Component"]["matrix"]["recall_channel_som"]
    if not (min(m["I1_presence_quality"], m["I1_brand_recognition"]) >= rules["BENCH"][0] >
            max(m["I1_sov"], m["I1_sentiment"], m["I1_market_competition"])):
        raise SystemExit("the text says presence quality and brand recognition, and only they, pass 0.74")
    VB = B["verdicts"]
    f, r = VB["H_Disc_Familiarity"], VB["H_Disc_Recognition"]
    if (f["status"], f["point_verdict"], f["flags"].get("undetermined_reason")) != \
            ("UNDETERMINED", "PARTIAL", "BCa CI spans all three |rho| bands"):
        raise SystemExit("the text says familiarity: point PARTIAL, interval spans all bands, UNDETERMINED")
    if (r["status"], r["point_verdict"], r["flags"]["ci_excludes_reducibility"], r["flags"]["provisional"]) != \
            ("CONFIRMED", "CONFIRMED", True, False):
        raise SystemExit("the text says recognition: CONFIRMED, interval excludes reducibility, not provisional")
    if r["bca_ci_95"][1] >= rules["BENCH"][0] or r["bca_ci_95"][0] >= 0 or r["spearman_rho"] < 0 \
            or f["spearman_rho"] < 0:
        raise SystemExit("interval or sign differs from the text")
    d = VB["H_Dissociation"]
    if d["status"] != "FULL" or d["n_cases"] != len(d["amplified"]) + len(d["suppressed"]) \
            or d["n_cases"] < rules["CASES"][0] or not d["amplified"] or not d["suppressed"]:
        raise SystemExit("the text says the dissociation count is FULL, in both directions")
    v.word("COI", coi_paragraph(), "papers/v0_27_28/v0_27_28_combined_validity_paper.md Declarations, Conflict "
           "of interest, with the employer and its companies named as the employer's group (COI_REPLACE)")
    v.word("AI_USE", ai_use_statement(), "papers/v0_27_28/v0_27_28_combined_validity_paper.md Declarations, Use "
           "of AI tools, verbatim")
    return v, {"v27": A, "v28": B}


def chart_data(src):
    """The three gating correlations with their 95% intervals: Study 1 primary (percentile bootstrap) and Study 2
    familiarity and recognition (BCa)."""
    A, B = src["v27"]["verdicts"], src["v28"]["verdicts"]
    return [{"key": "P", "study": 1, "rho": A["H_CV3_Primary"]["block"]["rho"], "ci": A["H_CV3_Primary"]["block"]["ci"],
             "verdict": A["H_CV3_Primary"]["status"]},
            {"key": "R", "study": 2, "rho": B["H_Disc_Recognition"]["spearman_rho"],
             "ci": B["H_Disc_Recognition"]["bca_ci_95"], "verdict": B["H_Disc_Recognition"]["status"]},
            {"key": "F", "study": 2, "rho": B["H_Disc_Familiarity"]["spearman_rho"],
             "ci": B["H_Disc_Familiarity"]["bca_ci_95"], "verdict": B["H_Disc_Familiarity"]["status"]}]


def _sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def write_provenance(v, extra=None):
    PROV_OUT.parent.mkdir(parents=True, exist_ok=True)
    out = {"_note": "Every number printed in TS-BR-v0.27-r1 (brief of the combined v0.27 + v0.28 paper) and its "
                    "chart: name -> source file, JSON path (or the locked scorer's source line), raw value, format. "
                    "Sources: v27 = osf/v27/v0.27_verdicts.json, v28 = osf/v28/v28_verdicts.json; decision lines: "
                    "scripts/score_v27.py, scripts/score_v28.py; disclosure wording: "
                    "papers/v0_27_28/v0_27_28_combined_validity_paper.md. Files identical to " + SOURCE_COMMIT + ".",
           "sources_sha256": {str(p.relative_to(ROOT)): _sha(p) for p in (V27, V28, SCORER27, SCORER28, PAPER_MD)},
           "values": v.prov}
    if extra:
        out.update(extra)
    PROV_OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    return PROV_OUT


if __name__ == "__main__":
    v, src = load()
    for n, s in v.vals.items():
        print(f"{n:<10} {s if len(s) < 90 else s[:90] + '...'}")
