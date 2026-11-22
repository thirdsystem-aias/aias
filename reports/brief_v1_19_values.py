#!/usr/bin/env python3
"""
brief_v1_19_values.py -- every number printed in the Coverage Paper B brief (TS-BR-v1.19-r1) and its chart.

Numbers are read by code, never typed:
  * result values from the study's verdict file osf/methodology/v1_19/outputs/v119_verdicts.json (the scorer's single
    run, commit 6e8f157), through the Values class of papers/v1_12/v112_values.py (each printed value records source,
    JSON path, raw value and format);
  * decision lines (reliability 0.50 / 0.30 and the 0.30 tenth-percentile line, the 0.15 / 0.30 Cliff's delta bands,
    the 45-unit identity-load floor, the 0.20 / 0.10 replication bands, the 10-answer defunct floor) from the locked
    scorer's constants (osf/methodology/v1_19/scripts/score_v1_19.py, read with ast, not imported), kind "rule".

Source files are checked out unchanged from branch v1.19-paper (b9e0d20). write_provenance() writes
reports/briefs/v1_19/brief_v1_19_provenance.json. ROOT is the worktree (AIAS_ROOT), never the main tree.
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

DESIGN = ROOT / "osf/methodology/v1_19"
VERDICTS = DESIGN / "outputs/v119_verdicts.json"
SCORER = DESIGN / "scripts/score_v1_19.py"
PAPER_MD = ROOT / "papers/v1_19/v1_19_ssrn_paper_draft.md"
PROV_OUT = ROOT / "reports/briefs/v1_19/brief_v1_19_provenance.json"
PAPER_A_VERDICTS = ROOT / "osf/methodology/v1_12/v112_verdicts.json"  # the file v1.19 read (SHA-256 checked)
SOURCE_COMMIT = "b9e0d20 (branch v1.19-paper; verdict file as written by the single run at 6e8f157)"


def r3(x):
    return VV.r3(x)


def m3(x):
    return VV.r3(x).replace("-", "−")


def r2(x):
    return VV.r2(x)


def i0(x):
    return VV.i0(x)


def pct2(x):
    return f"{float(x):.2f}"


def d_abs(x):
    return abs(float(x))


def scorer_constants(path=SCORER):
    return _consts(path)


def rel_of(r):
    """split-half reliability 2r/(1+r) (Paper A's rule, v1.12 section 2.7), for the chart's per-split points"""
    r = float(r)
    return 2 * r / (1 + r)


class BriefValues(VV.Values):
    def rule(self, name, const, fmt, consts):
        raw = consts[const]
        s = fmt(raw)
        self.vals[name] = s
        self.prov[name] = {"kind": "rule", "source": str(SCORER.relative_to(ROOT)), "constant": const, "raw": raw,
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


def load():
    V = json.loads(VERDICTS.read_text(encoding="utf-8"))
    if V.get("phase") != "v1.19" or V.get("prereg_tag") != "v1.19-prereg-r1" or V.get("status") != "RUN":
        raise SystemExit("v119_verdicts.json is not the v1.19 run")
    src = {"verdicts": V, "paperA": json.loads(PAPER_A_VERDICTS.read_text(encoding="utf-8"))}
    if _sha(PAPER_A_VERDICTS) != V["inputs"]["paper_A_verdicts_sha256"]:
        raise SystemExit("Paper A's verdict file is not the one v1.19 read")
    k = scorer_constants()
    v = BriefValues(src)
    S = ["H32_SetSampling"]
    # -- #32 situation sampling
    v.put("SPLITS", "verdicts", S + ["splits"], i0)
    v.put("REL_MED", "verdicts", S + ["rel_median"], r3)
    v.put("MED_R", "verdicts", S + ["median_r"], r3)
    v.put("P10", "verdicts", S + ["rel_p10"], r3)
    v.put("PCTL_A", "verdicts", S + ["paper_A_split_percentile"], pct2)
    a_code = str(V["H32_SetSampling"]["paper_A_H4_split_code"])
    v.put("REL_A", "verdicts", S + ["per_split", a_code, "rel"], r3)
    ns = [("verdicts", S + ["per_split", s, "n"]) for s in V["H32_SetSampling"]["per_split"]]
    v.derive("SPLIT_NMIN", VV.d_min, ns, i0)
    v.derive("SPLIT_NMAX", VV.d_max, ns, i0)
    C = ["H32_CueType"]
    v.put("CUE_P5", "verdicts", C + ["reference_p5"], r3)
    ws = [("verdicts", C + ["per_W", w, "rho_w_full_vs_minus_W"]) for w in V["H32_CueType"]["per_W"]]
    v.derive("CUE_MIN", VV.d_min, ws, r3)
    v.derive("CUE_MAX", VV.d_max, ws, r3)
    # -- #34 phantom brands
    F = ["H34_Floor"]
    v.put("N_FLAG", "verdicts", F + ["n_flagged_rated"], i0)
    v.put("N_OTHER", "verdicts", F + ["n_unflagged_rated"], i0)
    v.put("DELTA", "verdicts", F + ["primary", "cliffs_delta"], m3)
    v.put("DELTA_RES", "verdicts", F + ["beyond_presence", "cliffs_delta_resid"], m3)
    v.derive("DELTA_ABS", d_abs, [("verdicts", F + ["primary", "cliffs_delta"])], r3)  # the rule tests |delta|
    v.put("DEF_ANS", "verdicts", ["H34_Defunct_Occupancy", "answers"], i0)
    v.put("DEF_NAMED", "verdicts", ["H34_Defunct_Occupancy", "answers_naming_defunct"], i0)
    # -- #35 identity load
    v.put("IL_N", "verdicts", ["H35", "n"], i0)
    # -- #36 profiles
    P = ["H36_Profile_Replication"]
    v.put("REP_R", "verdicts", P + ["mean_rho_w_over_W"], m3)
    v.put("REP_N", "verdicts", P + ["n"], i0)
    pw = [("verdicts", P + ["per_W", w]) for w in V["H36_Profile_Replication"]["per_W"]]
    v.derive("REP_MIN", VV.d_min, pw, m3)
    v.derive("REP_MAX", VV.d_max, pw, m3)
    # -- the run
    v.put("RATED", "verdicts", ["rated_units"], i0)
    v.put("BRANDS", "verdicts", ["parity", "B-P1", "units"], i0)
    v.put("CEP_PER_CAT", "paperA", ["MC", "MC_Situation", "cells", 0, "n_ceps"], i0)
    # -- decision lines of the locked scorer
    v.rule("REL_LINE", "REL_CONF", r2, k)
    v.rule("REL_LOW", "REL_FALS", r2, k)
    v.rule("P10_LINE", "P10_MIN", r2, k)
    v.rule("D_FALS", "DELTA_FALS", r2, k)
    v.rule("D_CONF", "DELTA_CONF", r2, k)
    v.rule("IL_FLOOR", "IL_NFLOOR", i0, k)
    v.rule("REPL_LINE", "REP_CONF", r2, k)
    v.rule("REPL_LOW", "REP_FALS", r2, k)
    v.rule("PH_MIN", "PH_MIN", i0, k)

    # -- the brief's words assume these verdicts (stop on any mismatch)
    vs = V["verdict_summary"]
    expect = {"H32_SetSampling": "MARGINAL", "H32_CueType": "CONFIRMED", "H34_Floor_Signature": "FALSIFIED",
              "H34_Floor_BeyondPresence": "FALSIFIED", "H34_Defunct_Occupancy": "UNDETERMINED",
              "H35_IL_Coverage": "UNDETERMINED", "H35_IL_Robust_cell": "UNDETERMINED", "H35_IL_CueType": "UNDETERMINED",
              "H36_Profile_Replication": "FALSIFIED"}
    bad = {h: vs.get(h) for h, w in expect.items() if vs.get(h) != w}
    if bad or not vs["H36_Typology_cell"].startswith("NO TYPOLOGY"):
        raise SystemExit(f"the brief's wording assumes other verdicts: {bad}")
    if V["H32_CueType"]["W_below_p5"] != ["with what"]:
        raise SystemExit("cue type below the reference is not only 'with what'")
    ch = V["verdict_changes_under_sensitivities"]
    want = {"S-COI": {"H34_Floor_Signature", "H34_Floor_BeyondPresence"},
            "S-Floor6": {"H34_Floor_Signature"}, "S-Mid": {"H32_SetSampling"},
            "S-LOCO-v0.19": {"H34_Floor_Signature", "H34_Floor_BeyondPresence"},
            "S-LOCO-v0.20": {"H34_Floor_Signature", "H34_Floor_BeyondPresence"},
            "S-LOCO-v0.21": {"H34_Floor_Signature", "H34_Floor_BeyondPresence"},
            "S-LOCO-v0.23": {"H32_SetSampling", "H34_Floor_Signature", "H34_Floor_BeyondPresence"}}
    if {s: set(x) for s, x in ch.items()} != want:
        raise SystemExit(f"sensitivity changes differ from the brief's sentence: {ch}")
    if ch["S-Floor6"]["H34_Floor_Signature"][1] != "MARGINAL" or ch["S-Mid"]["H32_SetSampling"][1] != "FALSIFIED" \
            or ch["S-LOCO-v0.23"]["H32_SetSampling"][1] != "UNDETERMINED":
        raise SystemExit("sensitivity verdict words differ from the brief's sentence")
    if any(x[1] != "UNDETERMINED" for s in ("S-COI", "S-LOCO-v0.19", "S-LOCO-v0.20", "S-LOCO-v0.21")
           for x in ch[s].values()):
        raise SystemExit("floor-test sensitivities are not all UNDETERMINED")
    if V["H34_Floor"]["n_flagged_rated"] != k["PH_MIN"]:
        raise SystemExit("the flagged count is not exactly the floor; the 'any one drops out' sentence does not apply")
    if V["H35"]["n"] >= k["IL_NFLOOR"]:
        raise SystemExit("identity load reached its floor")
    v.word("CHEIL", cheil_sentence(), "papers/v1_19/v1_19_ssrn_paper_draft.md Declarations, Cheil sentence, employer's "
           "name replaced by 'the employer's group'")
    v.word("AI_USE", ai_use_statement(), "papers/v1_19/v1_19_ssrn_paper_draft.md Declarations, Use of AI tools, verbatim")
    return v, src


def chart_data(src):
    """Per split: reliability 2r/(1+r) of the split's half correlation (verdict file per_split.r; the file's own 'rel'
    where present), sorted; Paper A's split marked."""
    H = src["verdicts"]["H32_SetSampling"]
    a = str(H["paper_A_H4_split_code"])
    rows = []
    for code, s in H["per_split"].items():
        rel = s.get("rel")
        rows.append({"split": code, "rel": float(rel) if rel is not None else rel_of(s["r"]), "n": s["n"],
                     "paper_A": code == a, "path": ["verdicts", "H32_SetSampling", "per_split", code]})
    rows.sort(key=lambda r: r["rel"])
    return rows


def _sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def write_provenance(v, extra=None):
    PROV_OUT.parent.mkdir(parents=True, exist_ok=True)
    out = {"_note": "Every number printed in TS-BR-v1.19-r1 and its chart: name -> source file, JSON path (or locked "
                    "scorer constant), raw value, format. Source: osf/methodology/v1_19/outputs/v119_verdicts.json; "
                    "decision lines: osf/methodology/v1_19/scripts/score_v1_19.py; disclosure wording: "
                    "papers/v1_19/v1_19_ssrn_paper_draft.md. Files checked out unchanged from " + SOURCE_COMMIT + ".",
           "sources_sha256": {str(p.relative_to(ROOT)): _sha(p) for p in (VERDICTS, SCORER, PAPER_MD, PAPER_A_VERDICTS)},
           "values": v.prov}
    if extra:
        out.update(extra)
    PROV_OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    return PROV_OUT


if __name__ == "__main__":
    v, src = load()
    for n, s in v.vals.items():
        print(f"{n:<14} {s if len(s) < 90 else s[:90] + '...'}")
    rows = chart_data(src)
    print("per-split rel without file value:", sum(1 for s in src["verdicts"]["H32_SetSampling"]["per_split"].values()
                                                   if s.get("rel") is None))
