#!/usr/bin/env python3
"""
sources_aias3.py -- every number or locked word that the AIAS 3.0 drafts print TODAY, with the locked file and the
commit it is copied from. Nothing here is typed by hand: a {{L:KEY}} token in the paper template, the report
content or the site page is resolved by reading the cited file at the cited commit (`git show COMMIT:PATH`) and
formatting the value found there. A "json" source names a JSON path; a "text" source names a regular expression
that must match the locked text exactly once (its first group is the value).

Inputs that do not exist yet are NOT here: they are {{P:KEY}} placeholders, mapped in tokens_aias3.py.

  python3 papers/aias_3_0/sources_aias3.py            # prints every key, its value and its source
"""
import json
import re
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

# Commits (full SHA) of the locked or published records the drafts copy from.
C = {
    "v112_scored": "949be61e01dfad9773e43b0855dc33e9de3cc852",   # v1.12 scoring (once): Paper A PASS
    "v112_paper": "86b929aab60a6a7faaf9e6d24005e59507e1cde3",    # v1.12 paper, Cheil revision (published, 20 pp)
    "v112_prereg": "49efc473a63f415b9ae3eaa86811ca62fd81b91a",   # tag v1.12-prereg-r1
    "v119_scored": "6e8f1570de0967749a7ab2e8e0a4e968c9a18c06",   # v1.19 confirmatory run (once)
    "v119_paper": "b9e0d20a9e61a336a20e0e140f7df742ef6b7752",    # v1.19 paper (published, 16 pp)
    "aias2_paper": "a425191a10ad1dbf08d877e497abc12e7368752e",   # tag aias-2-0-paper-locked-r3
    "aias2_outline": "f97db70116ee3fe3aa63428e542344fe8e28b846", # tag aias-2-0-outline-locked
    "v042_scored": "31c64c64656b7b0393eca49e5d10384744475dd9",   # v0.42 scoring (once)
    "v042_erratum": "b3eb52686dc8e6254d71d1ac3421c4acc258e20e",  # v0.42 erratum 2026-11-25
    "v045_prereg": "f827d9d7eff6f756c3a10bfae886d9d624d2f958",   # tag v0.45-prereg-r1
    "v045_sq": "47f174810946401862b02de3ebe8f6f1f7c8d3e6",       # v0.45 DEVIATIONS Entry 2 + S-Q sensitivity
    "v043_prereg": "8c96d9cf8ead60105589269db69df398a2b8c329",   # tag v0.43-prereg-r1
    "v043_stage1": "3ed9e1dd8441e656867ec2f06e0142ef2a7131fe",   # v0.43 Stage 1 scoring run (once)
}
V112 = "osf/methodology/v1_12/v112_verdicts.json"
V119 = "osf/methodology/v1_19/outputs/v119_verdicts.json"
A2 = "osf/aias_2_0/aias_2_0_synthesis_data.json"
V42 = "osf/v42/v42_verdicts.json"
V42SQ = "osf/v45/sensitivity/t4_SQ/v42_verdicts_SQ.json"
V43 = "osf/v43/v43_stage1_verdicts.json"
P112 = "papers/v1_12/v1_12_ssrn_paper_draft.md"
P119 = "papers/v1_19/v1_19_ssrn_paper_draft.md"
PR45 = "osf/v45/prereg/PRE_REGISTRATION_v0_45.md"
PR43 = "osf/v43/prereg/PRE_REGISTRATION_v0_43.md"
ERR42 = "osf/v42/ERRATUM_2026-11-25.md"


def _j(commit, path, jpath, fmt):
    return {"kind": "json", "commit": C[commit], "path": path, "jpath": jpath, "fmt": fmt}


def _t(commit, path, regex, fmt="word"):
    return {"kind": "text", "commit": C[commit], "path": path, "regex": regex, "fmt": fmt}


L = "legs"
LOCKED = {
    # ---- Coverage Paper A (v1.12): verdict file at the scored commit
    "a.verdict": _j("v112_scored", V112, ["paper_A_verdict", "verdict"], "word"),
    "a.answered": _j("v112_scored", V112, ["MC", "MC_Complete", "answered"], "i0"),
    "a.expected": _j("v112_scored", V112, ["MC", "MC_Complete", "expected"], "i0"),
    "a.msit": _j("v112_scored", V112, ["MC", "MC_Situation", "pooled_mean_J_within_minus_J_between"], "r3"),
    "a.h1.rho": _j("v112_scored", V112, [L, "H1_Sep_Presence", "rho_w"], "r3m"),
    "a.h1.n": _j("v112_scored", V112, [L, "H1_Sep_Presence", "n"], "i0"),
    "a.h1.v": _j("v112_scored", V112, [L, "H1_Sep_Presence", "verdict"], "word"),
    "a.h2.rho": _j("v112_scored", V112, [L, "H2_Sep_Consistency", "rho_w"], "r3m"),
    "a.h2.n": _j("v112_scored", V112, [L, "H2_Sep_Consistency", "n"], "i0"),
    "a.h2.v": _j("v112_scored", V112, [L, "H2_Sep_Consistency", "verdict"], "word"),
    "a.h3.rho": _j("v112_scored", V112, [L, "H3_Sep_NamingRate", "rho_w"], "r3m"),
    "a.h3.v": _j("v112_scored", V112, [L, "H3_Sep_NamingRate", "verdict"], "word"),
    "a.h3.n": _j("v112_scored", V112, [L, "H3_Sep_NamingRate", "n"], "i0"),
    "a.h8.n": _j("v112_scored", V112, [L, "H8_Panel_Replication", "n"], "i0"),
    "a.h4.rel": _j("v112_scored", V112, [L, "H4_Reliability", "transformed"], "r3"),
    "a.h4.n": _j("v112_scored", V112, [L, "H4_Reliability", "n"], "i0"),
    "a.h4.v": _j("v112_scored", V112, [L, "H4_Reliability", "verdict"], "word"),
    "a.h5.rho": _j("v112_scored", V112, [L, "H5_Sep_Ranking", "rho_w"], "r3m"),
    "a.h7.rho": _j("v112_scored", V112, [L, "H7_Sep_Presence_Legacy", "rho_w"], "r3m"),
    "a.h8.rho": _j("v112_scored", V112, [L, "H8_Panel_Replication", "rho_w"], "r3"),
    "a.h8.v": _j("v112_scored", V112, [L, "H8_Panel_Replication", "verdict"], "word"),
    # bands and floor as printed in the published paper (its Method)
    "a.band.conf": _t("v112_paper", P112, r"CONFIRMED if \$\|\\rho_w\| \\leq (0\.30)\$", "word"),
    "a.band.fals": _t("v112_paper", P112, r"FALSIFIED if \$\|\\rho_w\| \\geq (0\.50)\$ and MARGINAL", "word"),
    "a.floor": _t("v112_paper", P112, r"Cov\* is rated only when the panel's mentions of \$b\$ total at least "
                                      r"(14) and", "word"),
    "a.rated": _t("v112_paper", P112, r"; (51) brands met its rating floor", "word"),
    "a.units": _t("v112_paper", P112, r"over five categories and (112) brands;", "word"),
    "a.cep_per_cat": _t("v112_paper", P112, r"one per category entry point \((14) per category", "word"),
    "a.spend": _t("v112_paper", P112, r"Recorded spend on all billed requests was \\\$(17\.08)\.", "word"),
    "a.median_lo": _t("v112_paper", P112, r"Median Cov\* ranged from (15\.2) to", "word"),
    "a.median_hi": _t("v112_paper", P112, r"Median Cov\* ranged from 15\.2 to (26\.6) across", "word"),
    # the Declarations' conflict-of-interest paragraph, verbatim from the published v1.12 revision (Cheil sentence
    # included); CLAUDE.md: conform COI language to the source phase's locked record, never from memory
    "coi.v112": _t("v112_paper", P112, r"(?s)## Conflict of interest \{-\}\n\n(.+?)\n\n## Funding", "word"),
    # ---- Coverage Paper B (v1.19): verdict file at the scored commit
    "b.rated": _j("v119_scored", V119, ["rated_units"], "i0"),
    "b.h32.rel": _j("v119_scored", V119, ["H32_SetSampling", "rel_median"], "r3"),
    "b.h32.p10": _j("v119_scored", V119, ["H32_SetSampling", "rel_p10"], "r3"),
    "b.h32.splits": _j("v119_scored", V119, ["H32_SetSampling", "splits"], "i0"),
    "b.h32.pct": _j("v119_scored", V119, ["H32_SetSampling", "paper_A_split_percentile"], "r2"),
    "b.h32.v": _j("v119_scored", V119, ["H32_SetSampling", "verdict"], "word"),
    "b.cue.count": _j("v119_scored", V119, ["H32_CueType", "count"], "i0"),
    "b.cue.v": _j("v119_scored", V119, ["H32_CueType", "verdict"], "word"),
    "b.floor.delta": _j("v119_scored", V119, ["H34_Floor", "primary", "cliffs_delta"], "r3m"),
    "b.floor.v": _j("v119_scored", V119, ["H34_Floor", "primary", "verdict"], "word"),
    "b.floor.resid": _j("v119_scored", V119, ["H34_Floor", "beyond_presence", "cliffs_delta_resid"], "r3m"),
    "b.defunct.answers": _j("v119_scored", V119, ["H34_Defunct_Occupancy", "answers"], "i0"),
    "b.defunct.naming": _j("v119_scored", V119, ["H34_Defunct_Occupancy", "answers_naming_defunct"], "i0"),
    "b.il.n": _j("v119_scored", V119, ["H35", "n"], "i0"),
    "b.il.floor": _t("v119_paper", P119, r"The pre-registered floor is (45) units", "word"),
    "b.il.v": _j("v119_scored", V119, ["verdict_summary", "H35_IL_Coverage"], "word"),
    "b.prof.R": _j("v119_scored", V119, ["H36_Profile_Replication", "mean_rho_w_over_W"], "r3m"),
    "b.prof.n": _j("v119_scored", V119, ["H36_Profile_Replication", "n"], "i0"),
    "b.prof.v": _j("v119_scored", V119, ["H36_Profile_Replication", "verdict"], "word"),
    "b.typology": _j("v119_scored", V119, ["H36_Structure", "cell"], "word"),
    "b.broad_of": _t("v119_paper", P119, r"No rated brand had Cov\* above 50, the value of situation-blind naming: "
                                         r"of the (51) brands", "word"),
    # ---- AIAS 2.0 (published synthesis; data file at the paper-locked-r3 commit)
    "z.class": _j("aias2_paper", A2, ["stage2", "class", "class"], "word"),
    "z.dis.rho": _j("aias2_paper", A2, ["stage2", "v19_verdicts", "H_Dissociation_t3", "rho"], "r3"),
    "z.dis.n": _j("aias2_paper", A2, ["stage2", "v19_verdicts", "H_Dissociation_t3", "n"], "i0"),
    "z.crel.rho": _j("aias2_paper", A2, ["stage2", "v19_verdicts", "H_Consistency_Reliability", "rho"], "r3"),
    "z.crel.n": _j("aias2_paper", A2, ["stage2", "v19_verdicts", "H_Consistency_Reliability", "n"], "i0"),
    "z.prel.rho": _j("aias2_paper", A2, ["stage2", "v19_verdicts", "H_Presence_Score_Reliability", "rho"], "r3"),
    "z.prel.n": _j("aias2_paper", A2, ["stage2", "v19_verdicts", "H_Presence_Score_Reliability", "n"], "i0"),
    "z.nocomp.rho": _j("aias2_paper", A2, ["stage2", "v19_verdicts", "H_NoComposite_t3", "rho_A_P"], "r3"),
    "z.nocomp.k2": _j("aias2_paper", A2, ["stage2", "v19_verdicts", "H_NoComposite_t3", "k2_line"], "r2"),
    # ---- the bridge from the AIAS 2.0 panel to the newest models (v0.42, t4): published and corrected values
    "g.p.rho": _j("v042_scored", V42, ["verdicts", "H_Gen_Presence", "rho"], "r3"),
    "g.p.rho_corr": _j("v045_sq", V42SQ, ["verdicts", "H_Gen_Presence", "rho"], "r3"),
    "g.p.n": _j("v042_scored", V42, ["verdicts", "H_Gen_Presence", "n"], "i0"),
    "g.p.v": _j("v042_scored", V42, ["verdicts", "H_Gen_Presence", "verdict"], "word"),
    "g.phi.rho": _j("v042_scored", V42, ["verdicts", "H_Gen_Phi", "rho"], "r3"),
    "g.phi.rho_corr": _j("v045_sq", V42SQ, ["verdicts", "H_Gen_Phi", "rho"], "r3"),
    "g.phi.n": _j("v042_scored", V42, ["verdicts", "H_Gen_Phi", "n"], "i0"),
    "g.phi.v": _j("v042_scored", V42, ["verdicts", "H_Gen_Phi", "verdict"], "word"),
    "g.err.cells": _t("v042_erratum", ERR42, r"\*\*Size\.\*\* (46) of 12,096 brand-answer cells", "word"),
    # ---- predictive validity (v0.43): Stage 1 verdicts; the Stage 2 amendment rule and its first outcome pull
    "pv.s1.presence": _j("v043_stage1", V43, ["tests", "H_Pred_Presence", "verdict"], "word"),
    "pv.s1.consistency": _j("v043_stage1", V43, ["tests", "H_Pred_Consistency", "verdict"], "word"),
    "pv.s2.first_pull": _t("v043_prereg", PR43, r"the first no earlier than Wednesday (2027-03-10)", "word"),
    "pv.s2.window_end": _t("v043_prereg", PR43, r"Y = the change from W\(2026-11-07\) to W\((2027-03-06)\)",
                           "word"),
    # ---- t5 (v0.45): what it carries for Coverage, and t6's target date as v0.45 quotes v0.42
    "t5.window": _t("v045_prereg", PR45, r"first call not before Thu (2026-12-03) 06:00 UTC", "word"),
    "t5.no_cov": _t("v045_prereg", PR45, r"It adds (no Coverage block) \(the Coverage re-ask does not fit", "word"),
    "t6.target": _t("v045_prereg", PR45, r"t₆ \(target (2027-02-12)\)", "word"),
}

FMT = {
    "word": lambda x: str(x),
    "i0": lambda x: f"{int(x):,}",
    "r2": lambda x: f"{float(x):.2f}",
    "r3": lambda x: f"{float(x):.3f}",
    "r3m": lambda x: f"{float(x):.3f}".replace("-", "−"),
}


class SourceError(KeyError):
    pass


@lru_cache(maxsize=None)
def blob(commit, path):
    r = subprocess.run(["git", "-C", str(ROOT), "show", f"{commit}:{path}"], capture_output=True, text=True)
    if r.returncode != 0:
        raise SourceError(f"{commit[:7]}:{path} not readable: {r.stderr.strip()}")
    return r.stdout


@lru_cache(maxsize=None)
def blob_id(commit, path):
    r = subprocess.run(["git", "-C", str(ROOT), "rev-parse", f"{commit}:{path}"], capture_output=True, text=True,
                       check=True)
    return r.stdout.strip()


def raw(key):
    if key not in LOCKED:
        raise SourceError(f"unmapped locked token {{{{L:{key}}}}}")
    s = LOCKED[key]
    text = blob(s["commit"], s["path"])
    if s["kind"] == "json":
        o = json.loads(text)
        for p in s["jpath"]:
            o = o[p]
        if o is None:
            raise SourceError(f"{key}: null at {s['path']} {s['jpath']}")
        return o
    hits = re.findall(s["regex"], text)
    if len(hits) != 1:
        raise SourceError(f"{key}: regex matched {len(hits)} times in {s['commit'][:7]}:{s['path']}")
    return hits[0]


def resolve(key):
    r = raw(key)                  # raises SourceError for an unmapped key
    return FMT[LOCKED[key]["fmt"]](r)


def provenance(key):
    value = resolve(key)          # raises SourceError for an unmapped key
    s = LOCKED[key]
    where = s["jpath"] if s["kind"] == "json" else s["regex"]
    return {"key": key, "value": value, "commit": s["commit"], "path": s["path"],
            "blob": blob_id(s["commit"], s["path"]), "where": where}


if __name__ == "__main__":
    for k in LOCKED:
        p = provenance(k)
        print(f"{k}\t{p['value']}\t{p['commit'][:7]}:{p['path']}")
    sys.exit(0)
