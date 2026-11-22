#!/usr/bin/env python3
"""
brief_v1_12_values.py -- every number printed in the Coverage Paper A brief (TS-BR-v1.12-r1) and its chart.

Numbers are read by code, never typed:
  * result values from the study's verdict file osf/methodology/v1_12/v112_verdicts.json, through
    papers/v1_12/v112_values.py (the paper's own loader and Values class: each printed value records source file,
    JSON path, raw value and format);
  * decision lines (the 0.30 / 0.50 bands, the 0.50 reliability and 0.70 replication bars, the 0.10 / 0.60
    situation-check lines, the rating floor) from the locked scorer's constants
    (osf/methodology/v1_12/scripts/score_v1_12.py, read with ast, not imported), recorded as kind "rule".

The source files are checked out unchanged from branch v1.12-paper-cheil-r (86b929a): the verdict file and scorer
of the v1.12 scoring commit 949be61, the paper draft with its Declarations as revised for Cheil Worldwide / Iris.
write_provenance() writes reports/briefs/v1_12/brief_v1_12_provenance.json (number -> source key).
ROOT is the worktree (AIAS_ROOT, or this file's parent's parent), never the main tree.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(os.environ.get("AIAS_ROOT") or Path(__file__).resolve().parents[1]).resolve()
sys.path.insert(0, str(ROOT / "papers/v1_12"))
import v112_values as VV  # noqa: E402

DESIGN = ROOT / "osf/methodology/v1_12"
VERDICTS = DESIGN / "v112_verdicts.json"
N1 = DESIGN / "prereg/calibration_N1_v1_12.json"
SCORER = DESIGN / "scripts/score_v1_12.py"
PAPER_MD = ROOT / "papers/v1_12/v1_12_ssrn_paper_draft.md"
PROV_OUT = ROOT / "reports/briefs/v1_12/brief_v1_12_provenance.json"
SOURCE_COMMIT = "86b929a (branch v1.12-paper-cheil-r; verdicts and scorer as scored at 949be61)"
SEP_LEGS = ["H1_Sep_Presence", "H2_Sep_Consistency", "H3_Sep_NamingRate"]


# ------------------------------------------------------------------ formats used by the brief
def r3(x):
    return VV.r3(x)


def m3(x):
    """three decimals with a true minus sign"""
    return VV.r3(x).replace("-", "−")


def r2(x):
    return VV.r2(x)


def i0(x):
    return VV.i0(x)


def usd(x):
    return f"US${float(x):,.2f}"


def d_mul(a, b):
    return float(a) * float(b)


def scorer_constants(path=SCORER):
    """Module-level constants of the locked scorer, including tuple assignments (A, B = 1, 2); read with ast,
    the file is not executed."""
    tree = ast.parse(Path(path).read_text(encoding="utf-8"))
    out = {}
    for node in tree.body:
        if not (isinstance(node, ast.Assign) and len(node.targets) == 1):
            continue
        tg = node.targets[0]
        try:
            val = ast.literal_eval(node.value)
        except Exception:
            continue
        if isinstance(tg, ast.Name):
            out[tg.id] = val
        elif isinstance(tg, ast.Tuple) and isinstance(val, tuple) and len(tg.elts) == len(val):
            for e, x in zip(tg.elts, val):
                if isinstance(e, ast.Name):
                    out[e.id] = x
    return out


class BriefValues(VV.Values):
    def rule(self, name, const, fmt, consts, index=None):
        raw = consts[const] if index is None else consts[const][index]
        s = fmt(raw)
        self.vals[name] = s
        self.prov[name] = {"kind": "rule", "source": str(SCORER.relative_to(ROOT)), "constant": const,
                           "index": index, "raw": raw, "fmt": fmt.__name__, "formatted": s}
        return s


def _declarations(md_path=PAPER_MD):
    return Path(md_path).read_text(encoding="utf-8")


def cheil_sentence(md_path=PAPER_MD):
    """The Cheil Worldwide / Iris sentence of the paper's Declarations, read from the paper, with the group named as
    the employer's group: the brief does not name the employer (named only in the paper's Declarations)."""
    txt = _declarations(md_path)
    m = re.search(r"Cheil Worldwide, [^\n]*?\(conflict-of-interest screen of v0\.62, DEVIATIONS Entry 0, Part F\)\.", txt)
    if not m:
        raise SystemExit("Cheil sentence not found in the paper's Declarations")
    s = m.group(0)
    old = "a marketing company of the Samsung group in which Samsung Electronics holds 28.43%,"
    if old not in s:
        raise SystemExit("Cheil sentence differs from the expected wording")
    s = s.replace(old, "a marketing company of the employer's group,")
    s = s.replace(" (conflict-of-interest screen of v0.62, DEVIATIONS Entry 0, Part F).", ".")
    if "Samsung" in s:
        raise SystemExit("Cheil sentence still names the employer")
    return s


def ai_use_statement(md_path=PAPER_MD):
    """The paper's 'Use of AI tools' statement, verbatim."""
    txt = _declarations(md_path)
    m = re.search(r"## Use of AI tools \{-\}\n\n(.+?)\n", txt)
    if not m:
        raise SystemExit("AI-use statement not found in the paper's Declarations")
    return m.group(1).strip()


def load():
    src = VV.load_sources(VERDICTS, None, N1)
    V = src["verdicts"]
    if VV.is_synthetic(V):
        raise SystemExit("refusing synthetic / dry-run outputs")
    if V.get("phase") != "v1.12" or V.get("prereg_tag") != "v1.12-prereg-r1":
        raise SystemExit("v112_verdicts.json is not the v1.12 result")
    k = scorer_constants()
    v = BriefValues(src)
    L = lambda h, *p: ["legs", h, *p]  # noqa: E731
    MS = ["MC", "MC_Situation"]

    # -- instrument check: do situations change the brands named?
    v.put("MSIT_DIFF", "verdicts", MS + ["pooled_mean_J_within_minus_J_between"], r3)
    v.put("MSIT_WITHIN", "verdicts", MS + ["pooled_mean_J_within"], r3)
    v.put("MSIT_BETWEEN", "verdicts", MS + ["pooled_mean_J_between"], r3)
    v.put("MSIT_CELLS", "verdicts", MS + ["cells_used"], i0)
    # -- separability legs (Coverage score Cov*, primary panel)
    for key, h in (("H1", "H1_Sep_Presence"), ("H2", "H2_Sep_Consistency"), ("H3", "H3_Sep_NamingRate"),
                   ("H5", "H5_Sep_Ranking"), ("H8", "H8_Panel_Replication")):
        v.put(key, "verdicts", L(h, "rho_w"), m3)
        v.put(f"{key}_N", "verdicts", L(h, "n"), i0)
    # -- reliability
    v.put("H4_R", "verdicts", L("H4_Reliability", "rho_w"), r3)
    v.put("H4_REL", "verdicts", L("H4_Reliability", "transformed"), r3)
    v.put("H4_N", "verdicts", L("H4_Reliability", "n"), i0)
    # -- the raw count of situations (sensitivity S1, raw Cov at k = 2)
    v.put("RAW_H1", "verdicts", ["sensitivities", "S1_raw_Cov_k2", "rho_w", "H1_Sep_Presence"], m3)
    v.put("RAW_H3", "verdicts", ["sensitivities", "S1_raw_Cov_k2", "rho_w", "H3_Sep_NamingRate"], m3)
    # -- the run
    v.put("CALLS", "verdicts", ["MC", "MC_Complete", "answered"], i0)
    v.put("CALLS_EXP", "verdicts", ["MC", "MC_Complete", "expected"], i0)
    v.put("BRANDS", "verdicts", ["parity_gates", "P2", "units"], i0)
    v.put("CEP_PER_CAT", "verdicts", MS + ["cells", 0, "n_ceps"], i0)
    v.derive("CEPS", d_mul, [("verdicts", MS + ["cells", 0, "n_ceps"]), ("verdicts", L("H1_Sep_Presence", "n_categories"))],
             i0)
    v.put("SPEND", "verdicts", ["descriptives", "tokens_and_spend", "total_usd"], usd)
    # -- the sensitivity with a higher rating floor: too few brands to decide
    v.derive("S2HI_NMAX", VV.d_max, [("verdicts", ["sensitivities", "S2_floor_28", "n", h]) for h in SEP_LEGS], i0)
    # -- decision lines of the locked scorer
    v.rule("BAND_LO", "SEP_CONF", r2, k)
    v.rule("BAND_HI", "SEP_FALS", r2, k)
    v.rule("REL_MIN", "REL_CONF", r2, k)
    v.rule("REP_MIN", "REP_CONF", r2, k)
    v.rule("MSIT_DIFF_MIN", "MCS_DIFF_MIN", r2, k)
    v.rule("MSIT_JB_MAX", "MCS_JB_MAX", r2, k)
    v.rule("FLOOR", "FLOOR_FULL", i0, k)
    v.rule("MINMOD", "MIN_MODELS_NAMED", i0, k)
    v.rule("FLOOR_HI", "FLOOR_SENS", i0, k, index=1)
    v.rule("NUNITS_MIN", "N_FLOOR_UNITS", i0, k)

    # -- the brief's words assume these verdicts (stop on any mismatch)
    words = V["verdicts"]
    expect = {"H1_Sep_Presence": "CONFIRMED", "H2_Sep_Consistency": "CONFIRMED", "H3_Sep_NamingRate": "CONFIRMED",
              "H4_Reliability": "CONFIRMED", "H5_Sep_Ranking": "CONFIRMED", "H6_Sep_Sentiment": "INACTIVE",
              "H7_Sep_Presence_Legacy": "CONFIRMED", "H8_Panel_Replication": "CONFIRMED"}
    bad = {h: words[h] for h, w in expect.items() if words[h] != w}
    if bad:
        raise SystemExit(f"the brief's wording assumes other verdicts: {bad}")
    if V["paper_A_verdict"]["verdict"] != "PASS" or V["MC"]["MC_Situation"]["passed"] is not True:
        raise SystemExit("Paper A is not PASS with MC_Situation passed; the brief's wording does not apply")
    if VV.case_h5(V) != "REPORTED":
        raise SystemExit("H5 is not 'reported, not gating'; the Ranking sentence does not apply")
    src_h5 = V.get("H5_ranking_source") or {}
    if src_h5.get("stage1_verdict") != "MARGINAL":
        raise SystemExit("v1.14 Stage 1 interim verdict is not MARGINAL; the Ranking sentence does not apply")
    ch = V["verdict_changes_under_sensitivities"]
    if set(ch) != {"S1_raw_Cov_k2", "S2_floor_28", "S4_room_to_vary"}:
        raise SystemExit(f"sensitivities with changed verdicts differ from the brief's sentence: {sorted(ch)}")
    if {h: list(x) for h, x in ch["S4_room_to_vary"].items()} != {"H4_Reliability": ["CONFIRMED", "MARGINAL"]}:
        raise SystemExit("S4 change is not H4 CONFIRMED -> MARGINAL")
    if any(x[1] != "UNDETERMINED" for x in ch["S2_floor_28"].values()):
        raise SystemExit("S2 floor 28 changes are not all UNDETERMINED")
    if max(V["sensitivities"]["S2_floor_28"]["n"][h] for h in SEP_LEGS) >= k["N_FLOOR_UNITS"]:
        raise SystemExit("S2 floor 28 kept enough brands; the 'too few to decide' sentence does not apply")
    if any(abs(float(V["legs"][h]["rho_w"])) > k["SEP_CONF"] for h in SEP_LEGS):
        raise SystemExit("a separability leg is outside the band; the wording does not apply")
    sd = V["sensitivities"]["S10_without_Denon"]
    if sd["verdict_changes"] or any(sd["verdicts"][h] != words[h] for h in sd["verdicts"]):
        raise SystemExit("a verdict changes without Denon; the disclosure sentence does not apply")
    v.word("SD_SAME", "the same verdicts", "sensitivities.S10_without_Denon.verdicts == verdicts (no verdict_changes)")
    v.word("CHEIL", cheil_sentence(), "papers/v1_12/v1_12_ssrn_paper_draft.md Declarations, Cheil sentence, "
           "employer's name replaced by 'the employer's group'")
    v.word("AI_USE", ai_use_statement(), "papers/v1_12/v1_12_ssrn_paper_draft.md Declarations, Use of AI tools, verbatim")
    return v, src


def chart_data(src):
    """Rows of the chart: the Coverage score (Cov*) with its 95% interval and the raw count (S1, raw Cov k = 2)
    against Presence, Consistency and naming rate."""
    V = src["verdicts"]
    S1 = V["sensitivities"]["S1_raw_Cov_k2"]
    rows = []
    for h, label in zip(SEP_LEGS, ("Presence", "Consistency", "Naming rate")):
        leg = V["legs"][h]
        rows.append({"leg": h, "label": label, "rho": leg["rho_w"], "lo": leg["ci95_rho_w"][0],
                     "hi": leg["ci95_rho_w"][1], "n": leg["n"], "raw": S1["rho_w"][h], "raw_n": S1["n"][h],
                     "paths": [["verdicts", "legs", h, "rho_w"], ["verdicts", "legs", h, "ci95_rho_w"],
                               ["verdicts", "legs", h, "n"], ["verdicts", "sensitivities", "S1_raw_Cov_k2", "rho_w", h],
                               ["verdicts", "sensitivities", "S1_raw_Cov_k2", "n", h]]})
    return rows


def _sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def write_provenance(v, extra=None):
    PROV_OUT.parent.mkdir(parents=True, exist_ok=True)
    out = {"_note": "Every number printed in TS-BR-v1.12-r1 and its chart: name -> source file, JSON path (or locked "
                    "scorer constant), raw value, format. Source: osf/methodology/v1_12/v112_verdicts.json; decision "
                    "lines: osf/methodology/v1_12/scripts/score_v1_12.py; disclosure wording: "
                    "papers/v1_12/v1_12_ssrn_paper_draft.md. Files checked out unchanged from " + SOURCE_COMMIT + ".",
           "sources_sha256": {str(p.relative_to(ROOT)): _sha(p) for p in (VERDICTS, SCORER, PAPER_MD, N1)},
           "values": v.prov}
    if extra:
        out.update(extra)
    PROV_OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    return PROV_OUT


if __name__ == "__main__":
    v, src = load()
    for n, s in v.vals.items():
        print(f"{n:<14} {s if len(s) < 90 else s[:90] + '...'}")
