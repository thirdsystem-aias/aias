#!/usr/bin/env python3
"""
brief_v1_14_values.py -- every number printed in the Ranking closing brief (TS-BR-v1.14-r1, the brief of the combined
v1.14 + v1.16 paper) and its chart.

Numbers are read by code, never typed:
  * v1.16 results from osf/methodology/v1_16/outputs/results_v1_16.json (the scorer's single run, branch v1.16
    commit b6f5749) and v1.14 Stage 1 results from osf/methodology/v1_14/outputs/stage1/stage1_v1_14.json (branch
    v1.14), through the Values class of papers/v1_12/v112_values.py (each printed value records source, JSON path,
    raw value and format);
  * decision lines (separability 0.30 / 0.50, retest 0.50, rating floor 6) from the locked v1.10 scorer's constants
    (scripts/score_v1_10.py, read with ast, not imported), which scripts/score_v1_16.py takes over unchanged (checked
    in its text), kind "rule".

Source files are checked out unchanged from branch ranking-close (8018665); the two output files and both scorers
are byte-identical to branches v1.16 and v1.14. write_provenance() writes
reports/briefs/v1_14/brief_v1_14_provenance.json. ROOT is the worktree (AIAS_ROOT), never the main tree.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(os.environ.get("AIAS_ROOT") or Path(__file__).resolve().parents[1]).resolve()
sys.path.insert(0, str(ROOT / "papers/v1_12"))
sys.path.insert(0, str(ROOT / "reports"))
import v112_values as VV  # noqa: E402
from brief_v1_12_values import scorer_constants as _consts  # noqa: E402  (ast reader with tuple assignments)

R16 = ROOT / "osf/methodology/v1_16/outputs/results_v1_16.json"
S14 = ROOT / "osf/methodology/v1_14/outputs/stage1/stage1_v1_14.json"
SCORER10 = ROOT / "scripts/score_v1_10.py"
SCORER16 = ROOT / "scripts/score_v1_16.py"
SCORER14 = ROOT / "scripts/score_v1_14.py"
PAPER_MD = ROOT / "papers/v1_14_16/v1_14_16_ranking_close_paper_draft.md"
PROV_OUT = ROOT / "reports/briefs/v1_14/brief_v1_14_provenance.json"
SOURCE_COMMIT = ("8018665 (branch ranking-close); results_v1_16.json as written by the single run (branch v1.16, "
                 "b6f5749), stage1_v1_14.json as written by Stage 1 (branch v1.14)")
WAVES = ["t1", "t2", "t3", "t4"]


def r3(x):
    return VV.r3(x)


def m3(x):
    return VV.r3(x).replace("-", "−")


def r2(x):
    return VV.r2(x)


def i0(x):
    return VV.i0(x)


def f4(x):
    return f"{float(x):.4f}"


def scorer_constants(path=SCORER10):
    return _consts(path)


class BriefValues(VV.Values):
    def rule(self, name, const, fmt, consts):
        raw = consts[const]
        s = fmt(raw)
        self.vals[name] = s
        self.prov[name] = {"kind": "rule", "source": str(SCORER10.relative_to(ROOT)), "constant": const, "raw": raw,
                           "fmt": fmt.__name__, "formatted": s}
        return s


def _md():
    return PAPER_MD.read_text(encoding="utf-8")


def cheil_sentence():
    """The paper's Cheil Worldwide / Iris sentence, with the group named as the employer's group."""
    m = re.search(r"Cheil Worldwide, [^\n]*?from 2024\)\.", _md())
    if not m:
        raise SystemExit("Cheil sentence not found in the paper's Declarations")
    s = m.group(0)
    old = "a marketing company of the Samsung group in which Samsung Electronics holds 28.43%,"
    if old not in s:
        raise SystemExit("Cheil sentence differs from the expected wording")
    s = s.replace(old, "a marketing company of the employer's group,")
    if "Samsung" in s:
        raise SystemExit("Cheil sentence still names the employer")
    return s


def ai_use_statement():
    m = re.search(r"## Use of AI tools \{-\}\n\n(.+?)\n", _md())
    if not m:
        raise SystemExit("AI-use statement not found in the paper's Declarations")
    return m.group(1).strip()


def _check_scorers():
    """v1.14 and v1.16 take the v1.10 decision lines over unchanged (text check, files not executed)."""
    for p in (SCORER16, SCORER14):
        s = p.read_text(encoding="utf-8")
        for line in ("SEP_CONF, SEP_FALS = R.SEP_CONF, R.SEP_FALS", "STAB_CONF, STAB_FALS = R.STAB_CONF, R.STAB_FALS",
                     "RATING_FLOOR = R.RATING_FLOOR"):
            if line not in s:
                raise SystemExit(f"{p.name} does not take '{line}' from score_v1_10.py")


def load():
    A = json.loads(R16.read_text(encoding="utf-8"))
    B = json.loads(S14.read_text(encoding="utf-8"))
    if A.get("phase") != "v1.16" or A.get("prereg_tag") != "v1.16-prereg-r1" or A.get("statistic") != "PREC":
        raise SystemExit("results_v1_16.json is not the v1.16 run")
    if B.get("phase") != "v1.14" or B.get("prereg_tag") != "v1.14-prereg-r2" or B.get("dry_run"):
        raise SystemExit("stage1_v1_14.json is not the v1.14 Stage 1 run")
    _check_scorers()
    k = scorer_constants()
    v = BriefValues({"v116": A, "v114": B})
    # -- v1.16: precedence (PREC)
    for i, w in enumerate(WAVES, 1):
        v.put(f"P{i}", "v116", ["H1_Sep_Presence", "per_wave", w, "rho"], r3)
    v.derive("P_MAX", VV.d_max, [("v116", ["H1_Sep_Presence", "per_wave", w, "rho"]) for w in WAVES], r3)
    v.derive("C_MAX", VV.d_max, [("v116", ["H2_Sep_Consistency", "per_wave", w, "rho"]) for w in WAVES], r3)
    v.put("H3", "v116", ["H3_Retest_t1_t2", "rho"], r3)
    v.put("H3_N", "v116", ["H3_Retest_t1_t2", "n"], i0)
    v.put("H3_P", "v116", ["H3_Retest_t1_t2", "p_shuffle"], f4)
    v.put("SHUF", "v116", ["MQ7_negative_control", "shuffled_mean_rho_H3"], f4)
    v.put("H5", "v116", ["H5_Retest_t2_t3", "rho"], r3)
    v.put("H4", "v116", ["H4_Sep_Presence_t4_S1", "rho"], r3)
    us = [("v116", ["D1_descriptives", w, "units_rated"]) for w in WAVES]
    v.derive("U_MIN", VV.d_min, us, i0)
    v.derive("U_MAX", VV.d_max, us, i0)
    S = ["sensitivities"]
    v.put("F10_1", "v116", S + ["S2_floor_10", "H1", "per_wave", "t1", "rho"], r3)
    v.put("F10_2", "v116", S + ["S2_floor_10", "H1", "per_wave", "t2", "rho"], r3)
    v.put("NOSP_2", "v116", S + ["S4_leave_out_v0.23", "H1", "per_wave", "t2", "rho"], r3)
    v.put("NOSP_3", "v116", S + ["S4_leave_out_v0.23", "H1", "per_wave", "t3", "rho"], r3)
    v.derive("NOCAR_MAX", VV.d_max, [("v116", S + ["S4_leave_out_v0.22", "H1", "per_wave", w, "rho"])
                                     for w in WAVES], r3)
    v.put("UNC_1", "v116", S + ["S9_uncentred", "H2", "per_wave", "t1", "rho"], r3)
    # -- v1.14: the modal position (MODE), Stage 1 on the fourth wave
    v.put("M_H1", "v114", ["H1_Sep_Presence", "rho"], r3)
    v.put("M_H2", "v114", ["H2_Sep_Consistency", "rho"], r3)
    v.put("M_S1", "v114", ["H4_Sep_Presence_S1", "rho"], r3)
    v.put("M_F10", "v114", ["sensitivities", "S2_floor_10", "H1", "rho"], r3)
    v.put("M_TOP1", "v114", ["sensitivities", "S3_candidate_TOP1", "H1", "rho"], r3)
    v.derive("ANSWERS", VV.d_sum, [("v114", ["analysis_set", "counts", c]) for c in B["analysis_set"]["counts"]], i0)
    v.put("BRANDS", "v114", ["unit_join", "matched"], i0)
    # -- decision lines of the locked v1.10 scorer (taken over by v1.14 and v1.16)
    v.rule("SEP_CONF", "SEP_CONF", r2, k)
    v.rule("SEP_FALS", "SEP_FALS", r2, k)
    v.rule("STAB_CONF", "STAB_CONF", r2, k)
    v.rule("FLOOR", "RATING_FLOOR", i0, k)
    v.rule("ALPHA", "P_ALPHA", r2, k)

    # -- the brief's words assume these verdicts (stop on any mismatch)
    want16 = {"H1_Sep_Presence": "MARGINAL", "H2_Sep_Consistency": "CONFIRMED", "H3_Retest_t1_t2": "CONFIRMED",
              "H4_Sep_Presence_t4_S1": "MARGINAL", "H5_Retest_t2_t3": "CONFIRMED"}
    bad = {h: A[h]["verdict"] for h, w in want16.items() if A[h]["verdict"] != w}
    if bad or A["GATE"] != "MARGINAL":
        raise SystemExit(f"the brief's wording assumes other v1.16 verdicts: {bad}, gate {A['GATE']}")
    if not A["CONSEQUENCE"].startswith("NOT PASS: Ranking is reported as part of Presence and not as a separate "
                                       "AIAS component. There is no further Ranking redesign."):
        raise SystemExit("the printed consequence differs from the brief's decision line")
    rd = [A["H1_Sep_Presence"]["per_wave"][w]["single_wave_reading"] for w in WAVES]
    if rd != ["CONFIRMED", "MARGINAL", "MARGINAL", "CONFIRMED"]:
        raise SystemExit(f"per-wave Presence readings differ from 'inside at two, between at two': {rd}")
    if any(A["H2_Sep_Consistency"]["per_wave"][w]["single_wave_reading"] != "CONFIRMED" for w in WAVES):
        raise SystemExit("Consistency is not inside the band at every wave")
    if A["MQ7_negative_control"]["flag"] or A["MQ9_identification"].get("flag"):
        raise SystemExit("a control is flagged")
    ch = {(c["sensitivity"], c["hypothesis"], c["under_sensitivity"]) for c in A["verdict_changes_under_sensitivities"]}
    if ch != {("S2_floor_10", "H1", "FALSIFIED"), ("S9_uncentred", "H2", "MARGINAL"),
              ("S4_leave_out_v0.22", "H1", "CONFIRMED"), ("S4_leave_out_v0.23", "H1", "FALSIFIED")}:
        raise SystemExit(f"v1.16 sensitivity changes differ from the brief's sentence: {ch}")
    for s in ("S7_without_Denon", "S_COI_without_Denon_and_Cheil_Iris"):
        if A["sensitivities"][s]["H1"]["verdict"] != "MARGINAL" or A["sensitivities"][s]["H2"]["verdict"] != "CONFIRMED":
            raise SystemExit(f"{s} changes a verdict")
    want14 = {"H1_Sep_Presence": "MARGINAL", "H2_Sep_Consistency": "CONFIRMED", "H4_Sep_Presence_S1": "MARGINAL"}
    bad = {h: B[h]["verdict"] for h, w in want14.items() if B[h]["verdict"] != w}
    if bad or B["STAGE1_VERDICT"] != "MARGINAL" or set(B["component_legs"].values()) != {"INACTIVE"}:
        raise SystemExit(f"the brief's wording assumes other v1.14 verdicts: {bad}")
    ch = {(c["sensitivity"], c["hypothesis"], c["under_sensitivity"]) for c in B["verdict_changes_under_sensitivities"]}
    if ch != {("S2_floor_10", "H1", "CONFIRMED"), ("S3_candidate_TOP1", "H1", "CONFIRMED")}:
        raise SystemExit(f"v1.14 sensitivity changes differ from the brief's sentence: {ch}")
    if B["sensitivities"]["S7_without_Denon"]["H1"]["rho"] != B["H1_Sep_Presence"]["rho"]:
        raise SystemExit("v1.14 without Denon differs from the primary")
    v.word("CHEIL", cheil_sentence(), "papers/v1_14_16/v1_14_16_ranking_close_paper_draft.md Declarations, Cheil "
           "sentence, employer's name replaced by 'the employer's group'")
    v.word("AI_USE", ai_use_statement(), "papers/v1_14_16/v1_14_16_ranking_close_paper_draft.md Declarations, Use of "
           "AI tools, verbatim")
    return v, {"v116": A, "v114": B}


def chart_data(src):
    """Per wave: PREC's within-category correlation with Presence and with Consistency (search off), and at the
    fourth wave PREC with search on and the modal position (v1.14) with search off and on."""
    A, B = src["v116"], src["v114"]
    rows = []
    for w in WAVES:
        rows.append({"wave": w, "presence": A["H1_Sep_Presence"]["per_wave"][w]["rho"],
                     "consistency": A["H2_Sep_Consistency"]["per_wave"][w]["rho"]})
    extra = {"prec_s1": A["H4_Sep_Presence_t4_S1"]["rho"], "mode_s0": B["H1_Sep_Presence"]["rho"],
             "mode_s1": B["H4_Sep_Presence_S1"]["rho"]}
    return rows, extra


def _sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def write_provenance(v, extra=None):
    PROV_OUT.parent.mkdir(parents=True, exist_ok=True)
    out = {"_note": "Every number printed in TS-BR-v1.14-r1 and its chart: name -> source file, JSON path (or locked "
                    "scorer constant), raw value, format. Sources: v116 = osf/methodology/v1_16/outputs/"
                    "results_v1_16.json, v114 = osf/methodology/v1_14/outputs/stage1/stage1_v1_14.json; decision "
                    "lines: scripts/score_v1_10.py (taken over by score_v1_14.py and score_v1_16.py); disclosure "
                    "wording: papers/v1_14_16/v1_14_16_ranking_close_paper_draft.md. Files checked out unchanged "
                    "from " + SOURCE_COMMIT + ".",
           "sources_sha256": {str(p.relative_to(ROOT)): _sha(p)
                              for p in (R16, S14, SCORER10, SCORER14, SCORER16, PAPER_MD)},
           "values": v.prov}
    if extra:
        out.update(extra)
    PROV_OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    return PROV_OUT


if __name__ == "__main__":
    v, src = load()
    for n, s in v.vals.items():
        print(f"{n:<10} {s if len(s) < 90 else s[:90] + '...'}")
