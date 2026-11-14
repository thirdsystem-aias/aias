#!/usr/bin/env python3
"""
AIAS v1.19 (Coverage Paper B) -- fills papers/v1_19/v1_19_ssrn_paper_template.md from recorded files only.

Reads (nothing else):
  osf/methodology/v1_19/outputs/v119_verdicts.json   the scorer's one run (SHA-256 must equal EXPECTED_SHA)
  osf/methodology/v1_19/anchor/osf_anchor_v1_19.json  tag, tag object, lock commit, Paper A's window
  osf/methodology/v1_19/anchor/DEVIATIONS.md          dated entries (counted)
  osf/methodology/v1_19/prereg/phantom_roster_v1_19.csv  recall-floor flags (frozen)
  Paper A's unit table, read in memory from the pinned commit 949be61 (git cat-file; never written to the tree),
      its SHA-256 checked against the verdicts' inputs.paper_A_unit_table_sha256
  git commit times of the lock, anchor, run and Paper A's data and scoring commits
Writes papers/v1_19/v1_19_ssrn_paper_draft.md and v1_19_ssrn_paper_draft_provenance.json (source, JSON path or
derivation, raw value, format and text of every value filled in).

Refuses (exit 2, nothing written) if prereg_tag != v1.19-prereg-r1, if the tag or the anchor does not match its
commit, if the verdicts' SHA-256 differs, or if a fixed sentence of the template (a comparison with a band, a count)
does not hold on the record.

Cheil Worldwide / Iris: ON by default. v1.19's own locked pre-registration (section 14, Declarations) carries the
agency-work paragraph, and its section 8 sensitivity S-COI drops the five brands it names; CLAUDE.md's COI rule is to
conform a paper's COI language to the source phase's locked record. The paper therefore quotes that paragraph verbatim
(from "Cheil Worldwide, a marketing company" through "(sensitivity S-COI)."), read at fill time from the locked
PRE_REGISTRATION_v1_19.md, whose SHA-256 must equal the anchor's record. --no-coi-cheil leaves it out (a parity switch
only, as the v0.43 pipeline's --coi-cheil was).
Usage: python3 papers/v1_19/fill_paper_v1_19.py [--no-coi-cheil] [--verdicts PATH] [--out PATH]
"""
import argparse
import csv
import hashlib
import io
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OSF = ROOT / "osf/methodology/v1_19"
TEMPLATE = HERE / "v1_19_ssrn_paper_template.md"
OUT = HERE / "v1_19_ssrn_paper_draft.md"
VERDICTS = OSF / "outputs/v119_verdicts.json"
ANCHOR = OSF / "anchor/osf_anchor_v1_19.json"
DEVIATIONS = OSF / "anchor/DEVIATIONS.md"
ROSTER = OSF / "prereg/phantom_roster_v1_19.csv"
PREREG = OSF / "prereg/PRE_REGISTRATION_v1_19.md"
EXPECTED_TAG = "v1.19-prereg-r1"
EXPECTED_SHA = "bf363060e4e90aed81c918544f561b43f387b5e41ef20d08d4844dc2d2176776"
PAPER_A_REF = "949be61e01dfad9773e43b0855dc33e9de3cc852"
PAPER_A_TABLE = "osf/methodology/v1_12/v112_unit_table.csv"
COMMITS = {"ANCHOR": "5974fcc", "RUN": "6e8f157", "A_DATA": "b89ff1f", "A_SCORE": "949be61"}
MODEL = {"claude-fable-5-2": "Claude Fable 5.2", "gpt-6-astra": "GPT-6 Astra", "gemini-4-argon": "Gemini 4 Argon",
         "claude-opus-5-5": "Claude Opus 5.5"}
CAT = {"v0.19": ("headphone", "headphones"), "v0.20": ("skincare", "skincare"), "v0.21": ("cosmetics", "cosmetics"),
       "v0.22": ("automotive", "automotive"), "v0.23": ("spirits", "spirits")}
W_ORDER = ["why", "when", "where", "while", "with whom", "with what", "how feeling"]
WORDS = {0: "none", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight",
         9: "nine", 10: "ten"}
SENS_ORDER = ["S-COI", "S-Floor6", "S-C3", "S-Equal", "S-LOCO-v0.19", "S-LOCO-v0.20", "S-LOCO-v0.21",
              "S-LOCO-v0.22", "S-LOCO-v0.23", "S-IL-t1", "S-F-noD", "S-Mid"]
SENS_LABEL = {"S-COI": "S-COI (six brands out)", "S-Floor6": "S-Floor6 (floor 6)", "S-C3": "S-C3 (panel C3)",
              "S-Equal": "S-Equal (equal-weight null)", "S-IL-t1": "S-IL-t1 ($t_1$ identity load)",
              "S-F-noD": "S-F-noD (flags without defunct)", "S-Mid": "S-Mid (mid-$p$ $\\beta$)"}
V_ORDER = ["H32_SetSampling", "H32_CueType", "H34_Floor_Signature", "H34_Floor_BeyondPresence",
           "H34_Defunct_Occupancy", "H35_IL_Coverage", "H35_IL_Robust_cell", "H35_IL_CueType",
           "H36_Profile_Replication", "H36_Typology_cell"]


class Refused(Exception):
    pass


def git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, check=True).stdout


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def jget(obj, path):
    """Path parts are separated by '|' without spaces (the D36 quadrant keys contain ' | ' and stay whole)."""
    cur = obj
    for part in re.split(r"(?<! )\|(?! )", path):
        cur = cur[part]
    return cur


# ---- formats (the provenance names each) ----
def r3(x): return f"{x:.3f}"
def p4(x): return f"{x:.4f}"
def i0(x): return str(int(x))
def thou(x): return f"{int(x):,}"
def gnum(x): return f"{x:g}"
def word(x): return WORDS[int(x)]
def s(x): return str(x)
FMT = {"r3": r3, "p4": p4, "i0": i0, "thou": thou, "gnum": gnum, "word": word, "str": s}


def when(iso):
    """git ISO time -> 'on 13 November 2026 at 10:17 CT (16:17 UTC)'."""
    d = datetime.fromisoformat(iso)
    u = d.astimezone(timezone.utc)
    return f"on {d.day} {d:%B %Y} at {d:%H:%M} CT ({u:%H:%M} UTC" + \
        (f", {u.day} {u:%B})" if u.date() != d.date() else ")")


def verify(V, sha, anchor, tag_commit, tag_object):
    """The refusals (pre-registration discipline): returns a list of problems, empty when the record is sound."""
    p = []
    if sha != EXPECTED_SHA:
        p.append(f"verdicts SHA-256 {sha} != {EXPECTED_SHA}")
    if V.get("prereg_tag") != EXPECTED_TAG:
        p.append(f"prereg_tag {V.get('prereg_tag')!r} != {EXPECTED_TAG}")
    if anchor.get("tag") != EXPECTED_TAG:
        p.append(f"anchor tag {anchor.get('tag')!r} != {EXPECTED_TAG}")
    if tag_commit != anchor.get("commit"):
        p.append(f"tag {EXPECTED_TAG} -> {tag_commit}, anchor names {anchor.get('commit')}")
    if tag_object != anchor.get("tag_object"):
        p.append(f"tag object {tag_object} != anchor tag_object {anchor.get('tag_object')}")
    if V.get("status") != "RUN" or (V.get("paper_A") or {}).get("a_verdict") != "PASS":
        p.append("the verdict file is not a RUN on Paper A's PASS")
    return p


class Vals:
    def __init__(self, V):
        self.V, self.v, self.prov = V, {}, {}

    def j(self, key, path, fmt):
        raw = jget(self.V, path)
        self.put(key, raw, fmt, {"source": "outputs/v119_verdicts.json", "path": path})
        return raw

    def put(self, key, raw, fmt, src):
        text = FMT[fmt](raw) if fmt in FMT else fmt(raw)
        self.v[key] = text
        self.prov[key] = {**src, "raw": raw, "format": fmt if isinstance(fmt, str) else "custom", "text": text}
        return text


def compute(V, anchor, dev_text, table_rows, roster, tag_commit, coi_cheil):
    X = Vals(V)
    A = []   # (fixed sentence of the template, holds on the record)
    git_src = lambda c: {"source": "git", "path": f"git log -1 --format=%cI {c}"}
    X.put("TAG", V["prereg_tag"], "str", {"source": "outputs/v119_verdicts.json", "path": "prereg_tag"})
    X.put("LOCK_COMMIT10", anchor["commit"][:10], "str", {"source": "anchor/osf_anchor_v1_19.json", "path": "commit"})
    X.put("LOCK_FILES", anchor["lock_manifest"]["files_listed"], "i0",
          {"source": "anchor/osf_anchor_v1_19.json", "path": "lock_manifest|files_listed"})
    X.put("T_LOCK", git("log", "-1", "--format=%cI", anchor["commit"]).decode().strip(), when, git_src(anchor["commit"]))
    for k, c in COMMITS.items():
        full = git("rev-parse", c).decode().strip()
        X.put(f"{k}_COMMIT7", full[:7], "str", {"source": "git", "path": f"git rev-parse {c}"})
        X.put(f"T_{k.replace('_', '')}", git("log", "-1", "--format=%cI", full).decode().strip(), when, git_src(full))
    win = anchor["paper_A_answers"]["collection_window_opens_utc"]
    wd = datetime.fromisoformat(win)
    X.put("T_WINDOW", win, lambda x: f"on {wd.day} {wd:%B %Y} at {wd:%H:%M} UTC",
          {"source": "anchor/osf_anchor_v1_19.json", "path": "paper_A_answers|collection_window_opens_utc"})
    t_lock = datetime.fromisoformat(git("log", "-1", "--format=%cI", anchor["commit"]).decode().strip())
    t_ascore = datetime.fromisoformat(git("log", "-1", "--format=%cI", COMMITS["A_SCORE"]).decode().strip())
    t_adata = datetime.fromisoformat(git("log", "-1", "--format=%cI", COMMITS["A_DATA"]).decode().strip())
    A.append(("lock before Paper A's window, data and scoring (confirmatory)", t_lock < wd < t_adata < t_ascore
              and anchor["paper_A_answers"]["tag_before_window_opens"] is True))
    n_dev = len(re.findall(r"Entry \d+ — ex ante", dev_text))
    X.put("DEV_N", n_dev, "i0", {"source": "anchor/DEVIATIONS.md", "path": "count of 'Entry N — ex ante'"})
    A.append(("both dated entries ex ante", n_dev == 2))
    X.j("A_VERDICT", "paper_A|a_verdict", "str")
    X.j("RATED", "rated_units", "i0")
    X.j("NPERM", "draws|permutation", "thou")
    X.j("NGAP", "draws|gap_reference", "i0")
    X.put("PANEL", V["panel"], lambda p: ", ".join(MODEL[m] for m in p),
          {"source": "outputs/v119_verdicts.json", "path": "panel"})
    X.j("PRIMARY_PANEL", "inputs|primary_panel", "str")
    X.put("BP0", V["parity"]["B-P0"]["passed"], lambda b: "passed" if b else "FAILED",
          {"source": "outputs/v119_verdicts.json", "path": "parity|B-P0|passed"})
    X.put("BP1", V["parity"]["B-P1"]["passed"], lambda b: "passed" if b else "FAILED",
          {"source": "outputs/v119_verdicts.json", "path": "parity|B-P1|passed"})
    X.j("BP1_UNITS", "parity|B-P1|units", "i0")
    X.j("A_VERDICTS_SHA8", "inputs|paper_A_verdicts_sha256", lambda x: x[:8])
    X.j("A_TABLE_SHA8", "inputs|paper_A_unit_table_sha256", lambda x: x[:8])
    X.j("IL_T1_SHA8", "inputs|il_t1_sha256", lambda x: x[:8])
    vs = V["verdict_summary"]

    # #32
    S = V["H32_SetSampling"]
    X.j("S_SPLITS", "H32_SetSampling|splits", "i0")
    X.j("S_SPLITS_FLOOR", "H32_SetSampling|splits_meeting_n_floor", "i0")
    X.j("S_MEDR", "H32_SetSampling|median_r", "r3")
    rel = X.j("S_REL", "H32_SetSampling|rel_median", "r3")
    p10 = X.j("S_P10", "H32_SetSampling|rel_p10", "r3")
    sp = X.j("S_P", "H32_SetSampling|p_perm_one_sided", "p4")
    X.j("S_PCTL", "H32_SetSampling|paper_A_split_percentile", "gnum")
    X.j("S_SPLIT0_REL", "H32_SetSampling|per_split|0|rel", "r3")
    X.j("S_SPLIT0_N", "H32_SetSampling|per_split|0|n", "i0")
    ps = S["per_split"].values()
    der = lambda op, path: {"source": "derived", "op": op, "path": path}
    X.put("S_R_MIN", min(x["r"] for x in ps), "r3", der("min", "H32_SetSampling|per_split|*|r"))
    X.put("S_R_MAX", max(x["r"] for x in ps), "r3", der("max", "H32_SetSampling|per_split|*|r"))
    X.put("S_N_MIN", min(x["n"] for x in ps), "i0", der("min", "H32_SetSampling|per_split|*|n"))
    X.put("S_N_MAX", max(x["n"] for x in ps), "i0", der("max", "H32_SetSampling|per_split|*|n"))
    X.j("V_H32S", "verdict_summary|H32_SetSampling", "str")
    A.append(("H32_SetSampling: 0.30 <= rel < 0.50, p < .05, P10 < 0.30, MARGINAL",
              0.30 <= rel < 0.50 and sp < 0.05 and p10 < 0.30 and vs["H32_SetSampling"] == "MARGINAL"
              and S["splits_meeting_n_floor"] == S["splits"]))
    C = V["H32_CueType"]
    X.j("C_REF_N", "H32_CueType|reference_pairs", "i0")
    p5 = X.j("C_P5", "H32_CueType|reference_p5", "r3")
    X.j("C_MED", "H32_CueType|reference_median", "r3")
    cnt = X.j("C_COUNT", "H32_CueType|count", "i0")
    X.j("C_COUNT_WORD", "H32_CueType|count", "word")
    X.put("C_BELOW", C["W_below_p5"], lambda w: ", ".join(w), {"source": "outputs/v119_verdicts.json",
                                                                 "path": "H32_CueType|W_below_p5"})
    X.put("C_RHO_BELOW", C["per_W"][C["W_below_p5"][0]]["rho_w_full_vs_minus_W"], "r3",
          {"source": "outputs/v119_verdicts.json", "path": f"H32_CueType|per_W|{C['W_below_p5'][0]}|rho_w_full_vs_minus_W"})
    X.put("C_RHO_MIN", min(x["rho_w_full_vs_minus_W"] for x in C["per_W"].values()), "r3",
          der("min", "H32_CueType|per_W|*|rho_w_full_vs_minus_W"))
    X.put("C_RHO_MAX", max(x["rho_w_full_vs_minus_W"] for x in C["per_W"].values()), "r3",
          der("max", "H32_CueType|per_W|*|rho_w_full_vs_minus_W"))
    X.j("V_H32C", "verdict_summary|H32_CueType", "str")
    A.append(("H32_CueType: exactly one W below p5, CONFIRMED", cnt == 1 and len(C["W_below_p5"]) == 1
              and vs["H32_CueType"] == "CONFIRMED" and all((x["rho_w_full_vs_minus_W"] < p5) == (w in C["W_below_p5"])
                                                           for w, x in C["per_W"].items())))
    # #34
    F = V["H34_Floor"]
    nf = X.j("F_NF", "H34_Floor|n_flagged_rated", "i0")
    X.j("F_NF_WORD", "H34_Floor|n_flagged_rated", "word")
    X.j("F_NU", "H34_Floor|n_unflagged_rated", "i0")
    X.put("F_CATS", F["categories_with_pairs"], lambda c: ", ".join(c[:-1]) + " and " + c[-1],
          {"source": "outputs/v119_verdicts.json", "path": "H34_Floor|categories_with_pairs"})
    X.put("F_NCATS", len(F["categories_with_pairs"]), "word", der("len", "H34_Floor|categories_with_pairs"))
    d1 = X.j("F_D", "H34_Floor|primary|cliffs_delta", "r3")
    X.j("F_P", "H34_Floor|primary|p_perm_two_sided", "p4")
    d2 = X.j("F_DR", "H34_Floor|beyond_presence|cliffs_delta_resid", "r3")
    X.j("F_PR", "H34_Floor|beyond_presence|p_perm_two_sided", "p4")
    X.j("F_NR", "H34_Floor|beyond_presence|n", "i0")
    X.j("V_F1", "verdict_summary|H34_Floor_Signature", "str")
    X.j("V_F2", "verdict_summary|H34_Floor_BeyondPresence", "str")
    A.append(("H34 floor: |delta| < 0.15 both arms, both FALSIFIED (same band)", abs(d1) < 0.15 and abs(d2) < 0.15
              and vs["H34_Floor_Signature"] == vs["H34_Floor_BeyondPresence"] == "FALSIFIED"))
    flag = {(r["substrate"], r["brand"]): r["recall_floor_flag_F"] == "1" for r in roster}
    rated = [(r["substrate"], r["brand"]) for r in table_rows if str(r["rated"]) == "1"]
    fl = [u for u in rated if flag[u]]
    bycat = {c: sum(1 for u in fl if u[0] == c) for c in CAT}
    tsrc = {"source": f"git cat-file blob {PAPER_A_REF[:7]}:{PAPER_A_TABLE} x prereg/phantom_roster_v1_19.csv"}
    X.put("F_BYCAT", bycat, lambda b: _join([f"{n} {CAT[c][0]} brand{'s' if n != 1 else ''}" for c, n in b.items()
                                             if n]), {**tsrc, "op": "rated and flagged, per category"})
    A.append(("unit table x roster reproduces the flagged and other rated counts; automotive holds none",
              len(fl) == nf and len(rated) - len(fl) == F["n_unflagged_rated"] and bycat["v0.22"] == 0
              and len(rated) == V["rated_units"]))
    coi_ex = [tuple(x) for x in V["sensitivities"]["S-COI"]["opts"]["exclude"]]
    coi_fl = [u for u in fl if u in coi_ex]
    X.put("COI_FLAGGED", coi_fl, lambda L: _join([b for _, b in L]), {**tsrc, "op": "rated, flagged and in S-COI's exclude"})
    A.append(("S-COI removes exactly one rated flagged brand, named (not a v0.23 code)",
              len(coi_fl) == 1 and not re.fullmatch(r"S\d\d", coi_fl[0][1])))
    broad = sum(1 for r in table_rows if str(r["rated"]) == "1" and float(r["cov_star"]) > 50)
    X.put("N_BROAD", broad, "i0", {**tsrc, "op": "rated units with cov_star > 50"})
    Dq = V["H36_Structure"]["dj_quadrants"]
    A.append(("no broad unit (unit table and D36 quadrants agree)", broad == 0 and
              all("situation-bound" in k for k in Dq) and sum(Dq.values()) == V["rated_units"]))
    X.put("DJ_HIGH", Dq["high P | situation-bound"], "i0", {"source": "outputs/v119_verdicts.json",
                                                             "path": "H36_Structure|dj_quadrants|high P | situation-bound"})
    X.put("DJ_LOW", Dq["low P | situation-bound"], "i0", {"source": "outputs/v119_verdicts.json",
                                                           "path": "H36_Structure|dj_quadrants|low P | situation-bound"})
    D = V["H34_Defunct_Occupancy"]
    X.j("D_ANS", "H34_Defunct_Occupancy|answers", "i0")
    dn = X.j("D_NAMING", "H34_Defunct_Occupancy|answers_naming_defunct", "i0")
    X.j("D_FISKER", "H34_Defunct_Occupancy|D34|Fisker_beside_D|answers_naming_any", "i0")
    X.j("D_REASON", "H34_Defunct_Occupancy|reason", "str")
    X.j("V_D", "verdict_summary|H34_Defunct_Occupancy", "str")
    d34 = sum(v for grp in D["D34"].values() for kind in grp["mentions_by_W"].values() for v in kind.values())
    X.put("D34_SUM", d34, "i0", der("sum", "H34_Defunct_Occupancy|D34|*|mentions_by_W|*|*"))
    A.append(("defunct: no answer names a defunct brand ('None of'), UNDETERMINED, D34 counts all zero", dn == 0 and d34 == 0
              and vs["H34_Defunct_Occupancy"] == "UNDETERMINED"))
    # #35
    H = V["H35"]
    iln = X.j("IL_N", "H35|n", "i0")
    X.put("IL_BYCAT", H["per_category"], lambda b: _join([f"{n} {CAT[c][1]}" for c, n in b.items()]),
          {"source": "outputs/v119_verdicts.json", "path": "H35|per_category"})
    X.j("IL_REASON", "H35|primary|reason", "str")
    X.j("V_IL1", "verdict_summary|H35_IL_Coverage", "str")
    X.j("V_IL2", "verdict_summary|H35_IL_Robust_cell", "str")
    X.j("V_IL3", "verdict_summary|H35_IL_CueType", "str")
    t1 = V["sensitivities"]["S-IL-t1"]["verdicts"]
    X.put("V_IL_T1", sorted(set(t1.values())), lambda x: ", ".join(x),
          {"source": "outputs/v119_verdicts.json", "path": "sensitivities|S-IL-t1|verdicts|*"})
    A.append(("identity load: n < 45, all three UNDETERMINED, also under S-IL-t1", iln < 45 and
              sum(H["per_category"].values()) == iln and
              {vs["H35_IL_Coverage"], vs["H35_IL_Robust_cell"], vs["H35_IL_CueType"]} == {"UNDETERMINED"}
              and set(t1.values()) == {"UNDETERMINED"}))
    # #36
    R = V["H36_Profile_Replication"]
    rm = X.j("R_MEAN", "H36_Profile_Replication|mean_rho_w_over_W", "r3")
    X.j("R_P", "H36_Profile_Replication|p_perm_one_sided", "p4")
    X.j("R_N", "H36_Profile_Replication|n", "i0")
    X.j("R_NCAT", "H36_Profile_Replication|n_categories", "i0")
    X.put("R_W_MIN", min(R["per_W"].values()), "r3", der("min", "H36_Profile_Replication|per_W|*"))
    X.put("R_W_MAX", max(R["per_W"].values()), "r3", der("max", "H36_Profile_Replication|per_W|*"))
    X.j("V_R", "verdict_summary|H36_Profile_Replication", "str")
    A.append(("H36 replication: R < 0.10, FALSIFIED", rm < 0.10 and vs["H36_Profile_Replication"] == "FALSIFIED"))
    T = V["H36_Structure"]
    X.j("ST_N", "H36_Structure|n", "i0")
    k = X.j("ST_K", "H36_Structure|full|k", "i0")
    rk = X.j("ST_RK", "H36_Structure|residual|k", "i0")
    X.j("ST_ARI", "H36_Structure|ari_vs_presence_tiers", "r3")
    X.j("ST_PARI", "H36_Structure|p_ari", "r3")
    X.j("ST_CELL", "H36_Structure|cell", "str")
    X.put("V_ST_SHORT", T["cell"], lambda c: c.split(" (")[0], {"source": "outputs/v119_verdicts.json",
                                                                  "path": "H36_Structure|cell", "op": "before ' ('"})
    A.append(("structure: k = 1 on both arms, no silhouette, NO TYPOLOGY", k == 1 and rk == 1 and
              T["full"]["silhouette"] is None and T["cell"].startswith("NO TYPOLOGY")
              and vs["H36_Typology_cell"] == T["cell"]))
    prof = V["H36_Structure"]["D36_profiles"]["category_mean_profiles"]
    allx = [x for c in prof.values() for x in c["mean_excess"].values()]
    X.put("D36_MIN", min(allx), "r3", der("min", "H36_Structure|D36_profiles|category_mean_profiles|*|mean_excess|*"))
    X.put("D36_MAX", max(allx), "r3", der("max", "H36_Structure|D36_profiles|category_mean_profiles|*|mean_excess|*"))
    # tables
    X.v["CUE_TABLE"] = cue_table(X, V)
    X.v["SENS_TABLE"], nochange = sens_table(X, V)
    X.v["SENS_NOCHANGE"] = _join(nochange)[0].upper() + _join(nochange)[1:]
    ch = V["verdict_changes_under_sensitivities"]
    floor_vars = sorted(k for k, v in ch.items() if "H34_Floor_Signature" in v and v["H34_Floor_Signature"][1] == "UNDETERMINED")
    A.append(("sensitivity prose: the floor tests turn UNDETERMINED exactly under S-COI and S-LOCO of the four "
              "categories holding flagged brands; S-Floor6 MARGINAL; S-Mid FALSIFIED; S-LOCO-v0.23 UNDETERMINED "
              "for set sampling; nothing else changes",
              floor_vars == sorted(["S-COI"] + [f"S-LOCO-{c}" for c in CAT if bycat[c]])
              and all(ch[k]["H34_Floor_BeyondPresence"][1] == "UNDETERMINED" for k in floor_vars)
              and ch["S-Floor6"] == {"H34_Floor_Signature": ["FALSIFIED", "MARGINAL"]}
              and ch["S-Mid"] == {"H32_SetSampling": ["MARGINAL", "FALSIFIED"]}
              and ch["S-LOCO-v0.23"]["H32_SetSampling"] == ["MARGINAL", "UNDETERMINED"]
              and set(ch) == set(floor_vars) | {"S-Floor6", "S-Mid"}
              and all(set(v) == {"H34_Floor_Signature", "H34_Floor_BeyondPresence"}
                      for kk, v in ch.items() if kk in floor_vars and kk != "S-LOCO-v0.23")))
    X.put("N_LOCO_FLOOR_WORD", len([k for k in floor_vars if k.startswith("S-LOCO")]), "word",
          der("count of S-LOCO variants turning H34_Floor_Signature UNDETERMINED", "verdict_changes_under_sensitivities"))
    pre = PREREG.read_bytes()
    cheil = re.findall(r"Cheil Worldwide, a marketing company.*?\(sensitivity S-COI\)\.", pre.decode("utf-8"), re.DOTALL)
    A.append(("the locked pre-registration (SHA-256 as the anchor records) holds exactly one agency-work paragraph",
              sha256_bytes(pre) == anchor["locked_files"]["osf/methodology/v1_19/prereg/PRE_REGISTRATION_v1_19.md"]["sha256"]
              and len(cheil) == 1 and "\n" not in cheil[0]))
    X.put("COI_CHEIL_TEXT", cheil[0] if cheil else "", "str",
          {"source": "osf/methodology/v1_19/prereg/PRE_REGISTRATION_v1_19.md", "sha256": sha256_bytes(pre),
           "path": "section 14 Declarations: from 'Cheil Worldwide, a marketing company' through '(sensitivity S-COI).'"})
    flags = {"COI_CHEIL": bool(coi_cheil), "NO_CHEIL": not coi_cheil, "NO_BROAD": broad == 0}
    return X, A, flags


def _join(L):
    L = list(L)
    return L[0] if len(L) == 1 else ", ".join(L[:-1]) + " and " + L[-1]


def cue_table(X, V):
    C, R = V["H32_CueType"]["per_W"], V["H36_Profile_Replication"]["per_W"]
    below = V["H32_CueType"]["W_below_p5"]
    rows = ["Table: Per cue type: rank correlation of Cov* with Cov* after dropping the cue type's two situations "
            f"(H32_CueType; reference 5th percentile {X.v['C_P5']}), and the half-A to half-B correlation of the "
            "excess profile (H36_Profile_Replication).", "",
            "| Cue type | $\\rho_w(\\text{Cov}^*, \\text{Cov}^*_{-W})$ | $n$ | Below reference | Profile replication $\\rho_w$ |",
            "|:--------------|-----------:|----:|:----------|-----------:|"]
    for w in W_ORDER:
        a = X.put(f"CUE|{w}|rho", C[w]["rho_w_full_vs_minus_W"], "r3",
                  {"source": "outputs/v119_verdicts.json", "path": f"H32_CueType|per_W|{w}|rho_w_full_vs_minus_W"})
        n = X.put(f"CUE|{w}|n", C[w]["n"], "i0", {"source": "outputs/v119_verdicts.json",
                                                  "path": f"H32_CueType|per_W|{w}|n"})
        r = X.put(f"CUE|{w}|rep", R[w], "r3", {"source": "outputs/v119_verdicts.json",
                                              "path": f"H36_Profile_Replication|per_W|{w}"})
        rows.append(f"| {w} | {a} | {n} | {'yes' if w in below else 'no'} | {r} |")
    return "\n".join(rows)


def sens_table(X, V):
    S = V["sensitivities"]
    rows = ["Table: Pre-registered sensitivity analyses (§2.4): the studies each re-ran and every verdict that differs "
            "from the primary one (primary $\\rightarrow$ sensitivity). Sensitivities never change a verdict.", "",
            "| Sensitivity | Studies | Verdicts that differ from the primary |",
            "|:----------------------------|:--------------|:--------------------------------------------------|"]
    nochange = []
    for k in SENS_ORDER:
        lab = SENS_LABEL.get(k) or f"S-LOCO without {CAT[k.split('-')[-1]][1]}"
        st = X.put(f"SENS|{k}|studies", S[k]["studies"], lambda L: ", ".join("#" + x for x in L),
                   {"source": "outputs/v119_verdicts.json", "path": f"sensitivities|{k}|studies"})
        chg = S[k]["verdict_changes"]
        txt = X.put(f"SENS|{k}|changes", chg, lambda c: "; ".join(f"{h}: {a} → {b}" for h, (a, b) in c.items()) or
                    "none", {"source": "outputs/v119_verdicts.json", "path": f"sensitivities|{k}|verdict_changes"})
        if not chg:
            nochange.append(lab.split(" (")[0] if k.startswith("S-LOCO") is False else lab)
        rows.append(f"| {lab} | {st} | {txt} |")
    return "\n".join(rows), nochange


def fill(verdicts=VERDICTS, out=OUT, coi_cheil=True, template=TEMPLATE, anchor_path=ANCHOR):
    raw = Path(verdicts).read_bytes()
    V = json.loads(raw)
    anchor = json.loads(Path(anchor_path).read_text())
    tag_commit = git("rev-parse", f"{EXPECTED_TAG}^{{commit}}").decode().strip()
    tag_object = git("rev-parse", EXPECTED_TAG).decode().strip()
    problems = verify(V, sha256_bytes(raw), anchor, tag_commit, tag_object)
    if problems:
        raise Refused("; ".join(problems))
    tb = git("cat-file", "blob", f"{PAPER_A_REF}:{PAPER_A_TABLE}")
    if sha256_bytes(tb) != V["inputs"]["paper_A_unit_table_sha256"]:
        raise Refused("Paper A's unit table at the pinned commit does not match the verdicts' recorded SHA-256")
    table_rows = list(csv.DictReader(io.StringIO(tb.decode("utf-8"))))
    roster = list(csv.DictReader(io.StringIO(ROSTER.read_text(encoding="utf-8"))))
    X, asserts, flags = compute(V, anchor, DEVIATIONS.read_text(encoding="utf-8"), table_rows, roster, tag_commit,
                                coi_cheil)
    bad = [d for d, ok in asserts if not ok]
    if bad:
        raise Refused("a fixed sentence of the template does not hold on the record: " + " | ".join(bad))
    text = Path(template).read_text(encoding="utf-8")
    for f, on in flags.items():
        text = re.sub(r"\{% if " + f + r" %\}(.*?)\{% endif %\}", (lambda m: m.group(1)) if on else "", text,
                      flags=re.DOTALL)
    if not flags["NO_BROAD"]:
        raise Refused("the abstract's sentence on broad brands needs NO_BROAD")
    missing = sorted(set(re.findall(r"\{\{(\w+)\}\}", text)) - set(X.v))
    if missing:
        raise Refused(f"template keys without a value: {missing}")
    text = re.sub(r"\{\{(\w+)\}\}", lambda m: X.v[m.group(1)], text)
    if "{{" in text or "{%" in text:
        raise Refused("template syntax left after filling")
    out = Path(out)
    out.write_text(text, encoding="utf-8")
    prov = {"phase": "v1.19", "synthetic": False, "prereg_tag": V["prereg_tag"], "verdicts": str(VERDICTS.relative_to(ROOT)),
            "verdicts_sha256": sha256_bytes(raw), "tag_commit": tag_commit, "tag_object": tag_object,
            "paper_A_unit_table": {"ref": PAPER_A_REF, "path": PAPER_A_TABLE,
                                   "blob": git("rev-parse", f"{PAPER_A_REF}:{PAPER_A_TABLE}").decode().strip(),
                                   "sha256": sha256_bytes(tb), "read": "in memory by git cat-file; never in the tree"},
            "coi_cheil": bool(coi_cheil), "flags": flags, "asserts": [{"sentence": d, "holds": ok} for d, ok in asserts],
            "values": X.prov}
    Path(str(out).replace(".md", "_provenance.json")).write_text(json.dumps(prov, indent=1, ensure_ascii=False) + "\n",
                                                               encoding="utf-8")
    return text, prov


def main(argv=None):
    ap = argparse.ArgumentParser(description="Fill the v1.19 paper from the recorded outputs")
    ap.add_argument("--verdicts", type=Path, default=VERDICTS)
    ap.add_argument("--out", type=Path, default=OUT)
    ap.add_argument("--no-coi-cheil", action="store_true",
                    help="leave out the pre-registration's agency-work paragraph (Cheil Worldwide / Iris); it is ON by "
                         "default because v1.19's locked pre-registration carries it (parity switch only)")
    a = ap.parse_args(argv)
    try:
        text, prov = fill(a.verdicts, a.out, not a.no_coi_cheil)
    except Refused as e:
        print(f"[v1.19 fill] REFUSED: {e}", file=sys.stderr)
        return 2
    print(f"[v1.19 fill] wrote {a.out} ({len(prov['values'])} values; {len(prov['asserts'])} fixed sentences hold; "
          f"coi_cheil={prov['coi_cheil']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
