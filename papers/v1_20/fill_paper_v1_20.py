#!/usr/bin/env python3
"""
fill_paper_v1_20.py -- fills papers/v1_20/v1_20_paper_template.md: Sentiment Paper A (v1.11's study; v1.11's Stage J
halted, case B; scored under its pre-registered successor rule v1.20, tag v1.20-prereg-r1).

Forked from papers/v1_11/fill_paper_v1_11.py (pre-data pipeline, branch v1.11-paper); the template engine, md_table
and the verdict cases are imported from there unchanged. No number is typed here: every value is a leaf of
  v1_20_verdicts.json, stage_j_v1_20.json, comparison_v1_11_v1_20.json   (score_v1_20.py --stage J / --stage C)
  judge_outputs_frozen_v1_11.json, plan_v1_11.json                         (judge_v1_11.py)
  run_values_v1_20.json                                                    (make_run_values_v1_20.py, metadata only)
  stage_j_run_v1_11.log                                                    (v1.11's own Stage J console record)
or a named function of such leaves (v120_values.DERIVE), formatted by named functions; the provenance of every value
is written beside the paper (v1_20_paper_draft_provenance.json).

Refusals (real mode): a synthetic file; prereg_tag not v1.20-prereg-r1; the verdicts' stage_j_sha256 not the Stage J
file's; Stage J's v1_11_frozen_sha256 not the frozen file's; the run values' raw_sha256 not the frozen raw_sha256;
the frozen plan_sha256 not the plan file's; different unit tables or judges; the tags v1.11-prereg-r1 or
v1.20-prereg-r1 missing, or an anchor record that does not name its tag's commit with an OSF deposit; v1.11's case
not B or the role of the verdicts not Sentiment Paper A's result; the v1.11 halt in v1.11's own console record not the
halt list v1.20 recomputed; verdict words not reproduced by the locked v1.11 scorer's functions (v1.20 runs v1.11's
statistics); and any sentence of the template whose factual premise (a sign, a band, a count) the data do not meet.

Usage (worktree or repository root):  python3 papers/v1_20/fill_paper_v1_20.py
"""
import argparse
import json
import math
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import v120_values as VV  # noqa: E402

ROOT = VV.ROOT
sys.path.insert(0, str(ROOT / "papers/v1_11"))
from fill_paper_v1_11 import FillError, render, md_table, switch_alternatives  # noqa: E402,F401  (engine, unchanged)

TEMPLATE = HERE / "v1_20_paper_template.md"
ANCHORS = {VV.EXPECTED_PREREG_TAG: ROOT / "osf/methodology/v1_20/anchor/git_anchor_v1_20.json",
           VV.V111_TAG: ROOT / "osf/methodology/v1_11/anchor/git_anchor_v1_11.json"}
DEV_FILES = {"v1.11 (before and at the lock)": ROOT / "osf/methodology/v1_11/anchor/DEVIATIONS.md",
             "v1.11 (continued after the lock)": ROOT / "osf/methodology/v1_11/postlock/DEVIATIONS_continued_v1_11.md",
             "v1.20": ROOT / "osf/methodology/v1_20/anchor/DEVIATIONS.md"}
R11, R20, RATT = "v1.11 rule", "v1.20 rule (first counting)", "S-ATT (v1.11 first)"
SENS_NAME = {"SU_uncentred_ranks": "SU", "SD_without_Denon_v0_19": "SD", "S_ATT_v1_11_first": "S-ATT",
             "S_CUT_without_cut_answers": "S-CUT", "S_CUT_M_without_cut_cells": "S-CUT-M"}
SENS_ORDER = ["SU_uncentred_ranks", "SD_without_Denon_v0_19", "S_ATT_v1_11_first", "S_CUT_without_cut_answers",
              "S_CUT_M_without_cut_cells"]
BLOCK = {"R": "Recognition", "F": "Omnibus", "OMNI": "Omnibus", "E": "Early", "EARLY-6": "Early"}
REDUCTION_TEXT = {"e_cap": "the early window cap lowered from 36 to 24",
                  "j2_e_share": "J2's early sample lowered from 10% to 5%",
                  "e_half": "the early block judged on a seeded half of each set's answers",
                  "e_none": "the early block not judged"}
WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
         10: "ten", 11: "eleven", 12: "twelve"}


class Cells:
    """Collects (formatted, source, path, fmt) for every number put in a table."""

    def __init__(self, val):
        self.val, self.cells = val, []

    def f(self, src, path, fmt, missing="--"):
        try:
            raw = self.val.raw(src, path)
        except VV.Missing:
            return missing
        if raw is None or (isinstance(raw, float) and not math.isfinite(raw)):
            return missing
        s = fmt(raw)
        self.cells.append((s, src, path, fmt.__name__))
        return s


def need(cond, why):
    """A template sentence's factual premise: refuse to print it if the data do not meet it."""
    if not cond:
        raise FillError(f"template premise not met: {why}")


# =========================================================================== consistency with the locked scorer
def scorer():
    sys.path.insert(0, str(ROOT / "scripts"))
    import score_v1_11 as S  # noqa: E402  (read-only; v1.20 runs v1.11's statistics and verdict functions)
    return S


def _nan(x):
    return float("nan") if x is None else float(x)


def recompute_words(V):
    S = scorer()
    h1 = V["H1_Judge_Agreement"]
    br = h1["brand_rho"]
    raw = {"H1": S.judge_agreement_verdict(_nan(h1["alpha_ordinal"]), _nan(br.get("rho")),
                                           bool(br.get("determinable")) and h1["units_judged_by_both"] >= S.MIN_UNITS_POOLED)}
    for h in VV.SEP_HYPS:
        if h in V:
            pw = V[h]["per_wave"]
            raw[VV.SHORT[h]] = S.separability_verdict([S.wave_abs_rho({**pw[w], "rho": _nan(pw[w].get("rho"))})
                                                       for w in VV.WAVES])
    if "H5_Sep_Ranking" not in V:
        raw["H5"] = V["ranking"]["status"]
    for h in VV.STAB_HYPS:
        r = V[h]
        raw[VV.SHORT[h]] = S.stability_verdict(_nan(r.get("rho")), _nan(r.get("p_perm")), bool(r.get("determinable")))
    r = V["H7_Naming_Frequency"]
    raw["H7"] = S.band_verdict(abs(_nan(r.get("rho")))) if r.get("determinable") else "UNDETERMINED"
    h9 = V["H9_Self_Preference"]
    raw["H9"] = S.self_pref_verdict(_nan(h9.get("delta_points")), h9["n_own_provider"], h9["n_other"])
    final, on = S.apply_noise_guard(raw)
    return raw, final, on


def check_consistency(src):
    V, J, C, F, P = src["verdicts"], src["stage_j"], src["comparison"], src["frozen"], src["plan"]
    raw, final, on = recompute_words(V)
    if raw != V["verdicts_before_noise_guard"] or final != V["VERDICTS"] or on != V["noise_guard_applied"]:
        raise FillError(f"verdict words not reproduced by the scorer's functions: file {V['VERDICTS']}, "
                        f"recomputed {final}")
    for h in VV.HYPS:
        leg = V.get(h)
        if leg is not None and leg.get("verdict") != raw[VV.SHORT[h]]:
            raise FillError(f"{h}: verdict {leg.get('verdict')} != {raw[VV.SHORT[h]]}")
    if J["H1_Judge_Agreement"]["verdict"] != V["H1_Judge_Agreement"]["verdict"]:
        raise FillError("H1 differs between Stage J and Stage C")
    if not (V["roles"] == J["roles"] == C["roles"] == F["roles"] == P["roles"]):
        raise FillError("the files name different judges")
    if (C.get("verdicts_side_by_side") or {}).get("v1.20") != V["VERDICTS"]:
        raise FillError("the comparison file's v1.20 verdicts differ from v1_20_verdicts.json")
    for k in V["VERDICTS"]:
        if V["VERDICTS"][k] not in VV.VERDICT_WORDS:
            raise FillError(f"{k}: unknown verdict word {V['VERDICTS'][k]!r}")


# =========================================================================== helpers
def put_or(val, name, src, path, fmt, alt="n/a"):
    try:
        return val.put(name, src, path, fmt)
    except VV.Missing:
        return val.word(name, alt, [src] + list(path) + ["(null)"])


def ci_text(val, name, src, path):
    lo = put_or(val, f"{name}_LO", src, path + ["ci95", 0], VV.r3)
    hi = put_or(val, f"{name}_HI", src, path + ["ci95", 1], VV.r3)
    return lo, hi


def wave_cells(cl, src, path):
    leg = VV.jget(cl.val.src[src], path)
    n = cl.f(src, path + ["n"], VV.i0)
    if not leg.get("determinable"):
        return f"n.d. ({n})"
    rho = cl.f(src, path + ["rho"], VV.sr3)
    lo, hi = cl.f(src, path + ["ci95", 0], VV.sr3), cl.f(src, path + ["ci95", 1], VV.sr3)
    return f"{rho} [{lo}, {hi}] ({n})"


def set_label(key):
    """'J1 EARLY-6 v0.9 pm' -> ('Early', 'PM software', '--'); 'J1 OMNI t1 v0.22' -> ('Omnibus', 'Automotive', 't1')."""
    parts = key.split()
    blk = parts[1]
    if blk == "EARLY-6":
        return BLOCK[blk], VV.EARLY_SHORT.get(parts[3], parts[3]), "--"
    return BLOCK[blk], VV.CAT_SHORT.get(parts[3], parts[3]), parts[2]


def set_phrase(key):
    b, c, w = set_label(key)
    return f"the {b.lower()} {c.lower()} set" + ("" if w == "--" else f" at ${w[0]}_{w[1]}$")


def wave_math(w):
    return f"$t_{w[1]}$"


def joinand(xs):
    return VV.joinand(xs)


def utc_hm(iso):
    return datetime.fromisoformat(iso).strftime("%H:%M")


# =========================================================================== values
def compute(src, synthetic, fig_dir, tags, deviations, halt_log):
    V, J, C, F, P, R, L = (src[k] for k in ("verdicts", "stage_j", "comparison", "frozen", "plan", "run", "cutlist"))
    W = V["VERDICTS"]
    val = VV.Values(src)
    cases = {"CASE_H1": VV.case_h1(V), "CASE_OVERALL": VV.case_overall(V), "CASE_H7": VV.case_h7(V),
             "CASE_H9": VV.case_h9(V)}
    for h in VV.SEP_HYPS:
        cases[f"CASE_{VV.SHORT[h]}"] = VV.case_sep(V, h)
    for h in VV.STAB_HYPS:
        cases[f"CASE_{VV.SHORT[h]}"] = VV.case_stab(V, h)
    flags = {"SYNTHETIC": synthetic, "GUARD_ON": bool(V["noise_guard_applied"]),
             "H1_FLAG": bool(V["H1_marginal_flag_on_all_verdicts"]), "JOIN_PASS": bool(V["join"]["passes"])}
    (c20, d20), (c11, d11) = tags[VV.EXPECTED_PREREG_TAG], tags[VV.V111_TAG]
    val.word("PREREG_TAG", V["prereg_tag"], ["verdicts", "prereg_tag"])
    val.word("PREREG_COMMIT", c20[:7], ["git", f"refs/tags/{VV.EXPECTED_PREREG_TAG}"])
    val.word("PREREG_DATE", d20, ["git", "taggerdate", VV.EXPECTED_PREREG_TAG])
    val.word("V111_TAG", V["successor_of_tag"], ["verdicts", "successor_of_tag"])
    val.word("V111_COMMIT", c11[:7], ["git", f"refs/tags/{VV.V111_TAG}"])
    val.word("V111_DATE", d11, ["git", "taggerdate", VV.V111_TAG])
    val.word("PAPER_DATE", "Synthetic test build" if synthetic else
             datetime.fromisoformat(V["created_utc"]).strftime("%B %Y"), ["verdicts", "created_utc"])
    val.word("FIG_DIR", str(fig_dir), ["argument --fig-dir"])
    val.word("FIG_CAPTION", "SYNTHETIC TEST DATA --- NOT RESULTS." if synthetic else "", ["synthetic flag"])
    val.word("DEV_SENTENCE", deviations[0], deviations[1])

    # ---------------- 3.1 the judge run (frozen record, plan, call-record metadata)
    val.put("RECORDS", "frozen", ["records"], VV.i0)
    need(R["records"] == F["records"] and R["raw_sha256"] == F["raw_sha256"], "run values come from the frozen raw file")
    val.put("REC_J1", "run", ["records_by_role", "J1"], VV.i0)
    val.put("REC_J2", "run", ["records_by_role", "J2"], VV.i0)
    att = R["records_by_role_pass_attempt"]
    firsts = [("run", ["records_by_role_pass_attempt", r, k]) for r in att for k in att[r] if k.endswith("attempt 1")]
    retries = [("run", ["records_by_role_pass_attempt", r, k]) for r in att for k in att[r] if not k.endswith("attempt 1")]
    need(all(k.endswith("attempt 1") for k in att.get("J2", {})), "J2 had no retry ('all by J1')")
    val.derive("FIRST_TRIES", VV.d_sum, firsts, VV.i0)
    val.derive("RETRIES", VV.d_sum, retries, VV.i0)
    val.put("ERRORS", "run", ["records_with_error_or_status_not_ok"], VV.i0)
    need(R["records_with_error_or_status_not_ok"] == 0, "no API error ('No call ended in an API error')")
    need(list(F["served_models"]) == [V["roles"]["J1"], V["roles"]["J2"]] or
         set(F["served_models"]) == set(V["roles"].values()), "served models are the requested ones")
    val.put("SERVED_J1", "frozen", ["served_models", V["roles"]["J1"]], VV.i0)
    val.put("SERVED_J2", "frozen", ["served_models", V["roles"]["J2"]], VV.i0)
    fin = R["finish_reason_by_role"]
    need(list(fin["J1"]) == ["end_turn"] and list(fin["J2"]) == ["completed"], "finish reasons: none at the cap")
    val.put("FIN_J1", "run", ["finish_reason_by_role", "J1", "end_turn"], VV.i0)
    val.put("FIN_J2", "run", ["finish_reason_by_role", "J2", "completed"], VV.i0)
    need(list(R["mode"]) == ["batch"], "all calls through batch services")
    val.put("BATCHES_J1", "run", ["batches_by_role", "J1"], VV.i0)
    val.put("BATCHES_J2", "run", ["batches_by_role", "J2"], VV.i0)
    val.word("RUN_FIRST", utc_hm(R["first_utc"]), ["run", "first_utc"])
    val.word("RUN_LAST", utc_hm(R["last_utc"]), ["run", "last_utc"])
    need(R["first_utc"][:10] == R["last_utc"][:10] == "2026-11-22", "run on 22 November 2026")
    val.put("SPEND", "frozen", ["spend_usd"], VV.usd2)
    need(abs(R["usd_total"] - F["spend_usd"]) < 0.005 and F["spend_usd_by_mode"].get("sync", 0) == 0,
         "per-judge spend sums to the frozen spend; no synchronous spend")
    need(F["spend_usd"] < 80, "spend under the US$80 pause")
    val.put("SPEND_J1", "run", ["usd_by_role", "J1"], VV.usd2)
    val.put("SPEND_J2", "run", ["usd_by_role", "J2"], VV.usd2)
    need(R["tokens_by_role"]["J1"]["thinking_reported"] == 0, "J1 records carry no reasoning count")
    val.put("THINK_J2", "run", ["tokens_by_role", "J2", "thinking_tokens"], VV.i0)
    val.put("CAL_J1", "plan", ["calibration", "calls", "J1"], VV.i0)
    val.put("CAL_J2", "plan", ["calibration", "calls", "J2"], VV.i0)
    val.put("OUT_J1", "plan", ["calibration", "output_tokens_per_call", "J1"], VV.i0)
    val.put("OUT_J2", "plan", ["calibration", "output_tokens_per_call", "J2"], VV.i0)
    val.put("PLAN_USD", "plan", ["steps", -1, "usd_with_overhead"], VV.usd2)
    red = P.get("reductions_applied") or []
    val.word("REDUCTION_SENTENCE", "no reduction of the early block applied." if not red else
             "the pre-registered reductions applied in their fixed order: "
             + "; ".join(REDUCTION_TEXT.get(str(r), str(r)) for r in red) + ".", ["plan", "reductions_applied"])
    rep = F.get("replacements") or []
    val.word("REPLACEMENT_SENTENCE", "Neither judge was replaced by the alternate." if not rep else
             "The alternate replaced a judge, as recorded in the frozen outputs.", ["frozen", "replacements"])

    # ---------------- 3.2 v1.11's halt (comparison file; v1.11's own console record)
    jf = C["judge_fail_by_judge_set"]
    j1sets = [k for k in jf if k.startswith("J1 ")]
    j2sets = [k for k in jf if k.startswith("J2 ")]
    halts = C["halts"][R11]
    need(sorted(halts) == sorted(halt_log["sets"]), "v1.11's console halt list equals the recomputed v1.11 halt list")
    need(sorted(halts) == sorted(V["v1_11_stage_j"]["halt"]) and V["v1_11_stage_j"]["case"] == "B",
         "case B recorded in the verdicts")
    need(V["role_of_these_verdicts"].startswith("Sentiment Paper A's result"), "role of the verdicts")
    val.word("V111_STAGEJ_START", halt_log["started"].replace("T", " ").replace("Z", "")[:16],
             ["v111_log", "started_utc"])
    val.word("V111_EXIT", halt_log["exit"], ["v111_log", "EXIT"])
    val.put("V111_FAIL", "comparison", ["outcome_counts", R11, "J1", "JUDGE_FAIL"], VV.i0)
    val.put("UNITS_J1", "stage_j", ["outcome_counts", "J1", "VALID"], VV.i0)
    val.put("UNITS_J2", "stage_j", ["outcome_counts", "J2", "VALID"], VV.i0)
    need(C["outcome_counts"][R11]["J1"]["VALID"] + C["outcome_counts"][R11]["J1"]["JUDGE_FAIL"]
         == J["outcome_counts"]["J1"]["VALID"], "v1.11-rule J1 units equal v1.20 J1 units")
    val.derive("V111_FAIL_SHARE", VV.d_ratio, [("comparison", ["outcome_counts", R11, "J1", "JUDGE_FAIL"]),
                                               ("stage_j", ["outcome_counts", "J1", "VALID"])], VV.pct2)
    val.put("V111_REP_FAIL", "frozen", ["outcomes", "J1 repeat", "JUDGE_FAIL"], VV.i0)
    val.derive("V111_J2_FAIL", VV.d_sum, [("comparison", ["judge_fail_by_judge_set", k, R11, "judge_fail"])
                                          for k in j2sets], VV.i0)
    val.derive("V111_HALT_N", VV.d_len, [("comparison", ["halts", R11])], VV.i0)
    val.derive("J1_SETS", VV.d_count, [("comparison", ["judge_fail_by_judge_set", k, R11, "fail_share"])
                                       for k in j1sets], VV.i0)
    val.derive("V111_FAIL_MAX", VV.d_max, [("comparison", ["judge_fail_by_judge_set", k, R11, "fail_share"])
                                           for k in j1sets], VV.pct2)
    kmax = max(j1sets, key=lambda k: jf[k][R11]["fail_share"])
    val.word("V111_FAIL_MAX_SET", set_phrase(kmax)[4:], ["comparison", "judge_fail_by_judge_set", kmax])
    early_all = [k for k in j1sets if " EARLY-6 " in k]
    early_h = [k for k in halts if " EARLY-6 " in k]
    rest = sorted([k for k in halts if " EARLY-6 " not in k])
    parts = []
    if early_h:
        parts.append(f"all {WORDS.get(len(early_all), len(early_all))} early sets" if len(early_h) == len(early_all)
                     else joinand(set_phrase(k) for k in sorted(early_h)))
    parts += [set_phrase(k) for k in rest]
    val.word("V111_HALT_DESC", joinand(parts), ["comparison", "halts", R11])
    cl = Cells(val)
    rows = []
    order = sorted(j1sets, key=lambda k: ({"R": 0, "OMNI": 1, "EARLY-6": 2}[k.split()[1]], k))
    for k in order:
        b, c, w = set_label(k)
        pk = ["judge_fail_by_judge_set", k]
        need(jf[k][R11]["valid"] + jf[k][R11]["judge_fail"] == jf[k][R20]["valid"] + jf[k][R20]["judge_fail"],
             f"{k}: units sent equal under both rules")
        val.derive(f"_U_{k}", VV.d_add, [("comparison", pk + [R11, "valid"]), ("comparison", pk + [R11, "judge_fail"])],
                   VV.i0)
        cl.cells.append((val.vals[f"_U_{k}"], "comparison", pk + [R11, "valid+judge_fail"], "i0"))
        rows.append([b, c, w, val.vals[f"_U_{k}"], cl.f("comparison", pk + [R11, "judge_fail"], VV.i0),
                     cl.f("comparison", pk + [R11, "fail_share"], VV.pct2), "yes" if k in halts else "no",
                     cl.f("comparison", pk + [R20, "judge_fail"], VV.i0),
                     cl.f("comparison", pk + [RATT, "judge_fail"], VV.i0)])
    val.table("TABLE_HALT", md_table(["Block", "Category", "Wave", "Units", "JUDGE_FAIL v1.11", "Share", "Halt",
                                      "JUDGE_FAIL v1.20", "S-ATT"], rows,
                                     ["l", "l", "l", "r", "r", "r", "l", "r", "r"]), cl.cells)
    need(all(jf[k][r]["judge_fail"] == 0 for k in j2sets for r in (R11, R20, RATT)), "J2 had no JUDGE_FAIL")

    # ---------------- 3.3 the successor rule on the same replies
    val.derive("V120_FAIL", VV.d_sum, [("comparison", ["judge_fail_by_judge_set", k, R20, "judge_fail"])
                                       for k in j1sets], VV.i0)
    val.derive("V120_UNJ", VV.d_sum, [("comparison", ["judge_fail_by_judge_set", k, R20, "unjudged"])
                                      for k in j1sets], VV.i0)
    val.derive("V120_FAIL_MAX", VV.d_max, [("comparison", ["judge_fail_by_judge_set", k, R20, "fail_share"])
                                           for k in j1sets], VV.pct1)
    need(max(jf[k][R20]["fail_share"] for k in j1sets) < 0.005 and not C["halts"][R20], "v1.20 prediction met, no halt")
    tr = C["status_transitions_v1_11_to_v1_20"]
    need(tr.get("J1 main: JUDGE_FAIL -> VALID") == C["outcome_counts"][R11]["J1"]["JUDGE_FAIL"] and
         tr.get("J1 repeat: JUDGE_FAIL -> VALID") == F["outcomes"]["J1 repeat"]["JUDGE_FAIL"] and
         set(tr) == {"J1 main: JUDGE_FAIL -> VALID", "J1 main: VALID -> VALID", "J1 repeat: JUDGE_FAIL -> VALID",
                     "J1 repeat: VALID -> VALID", "J2 main: VALID -> VALID", "J2 repeat: VALID -> VALID"},
         "every v1.11 failure became valid and every valid unit stayed valid")
    val.put("TRANS_VV", "comparison", ["status_transitions_v1_11_to_v1_20", "J1 main: VALID -> VALID"], VV.i0)
    val.put("DIFF_ATTEMPT", "comparison", ["valid_under_both_from_a_different_attempt", "J1 main", "n"], VV.i0)
    val.word("V120_STAGEJ_UTC", J["created_utc"].replace("T", " ")[:16], ["stage_j", "created_utc"])
    val.word("V120_STAGEC_UTC", V["created_utc"].replace("T", " ")[:16], ["verdicts", "created_utc"])
    val.derive("WINDOW_MISMATCH", VV.d_len, [("verdicts", ["F_window_count_vs_n_mentions", "mismatches"])], VV.i0)
    # P/C* cross-check against the v1.9 unit table (v1.20 section 5 item 3): omitted by score_v1_20.run_stage_c,
    # completed post hoc on 2026-11-22 by v1_9_cross_check_v1_20.py with v1.11's own comparison (never a verdict input)
    X = src["xcheck"]
    need(all(i.get("matches_pin") for i in X["inputs"].values()) and len(X["inputs"]) == 2,
         "cross-check inputs match v1.11's input manifest")
    need(X["keys"]["keys_in_both"] == X["P_Cstar_v1_9_cross_check"]["rows_compared"], "cross-check rows all joined")
    xd = X["descriptive_at_v1_9_printed_precision_4dp"]
    need(xd["rows_differing"] == 0, "every row agrees at the v1.9 table's 4 decimals ('all rows agree')")
    val.derive("PC_DIFF", VV.d_len, [("xcheck", ["P_Cstar_v1_9_cross_check", "differences"])], VV.i0)
    val.put("PC_ROWS", "xcheck", ["P_Cstar_v1_9_cross_check", "rows_compared"], VV.i0)
    val.put("PC_MAXDP", "xcheck", ["descriptive_at_v1_9_printed_precision_4dp", "max_abs_diff_P"], VV.sci1)
    val.put("PC_MAXDC", "xcheck", ["descriptive_at_v1_9_printed_precision_4dp", "max_abs_diff_Cstar"], VV.sci1)
    val.put("PC_NC", "xcheck", ["descriptive_at_v1_9_printed_precision_4dp", "rows_with_Cstar_in_both"], VV.i0)
    rk = V["ranking"]
    need(rk.get("status") == "ACTIVE" and all(t.get("matches_v1_10_stage_s") for t in rk["rank_tables"].values()),
         "H5 active, rank tables match v1.10")
    val.derive("RANK_TABLES", VV.d_len, [("verdicts", ["ranking", "rank_tables"])], VV.i0)
    val.word("RANKING_SENTENCE", f"$R^*$ ({rk.get('statistic')}) was computed with v1.10's locked code after v1.10's "
             f"own verdicts existed; all {val.vals['RANK_TABLES']} regenerated rank tables equalled v1.10's Stage S "
             "tables.", ["verdicts", "ranking"])

    # ---------------- 3.4 H1 and self-consistency
    H1 = ["H1_Judge_Agreement"]
    val.word("V_H1", W["H1"], ["verdicts", "VERDICTS", "H1"])
    val.put("H1_PAIRS", "verdicts", H1 + ["units_judged_by_both"], VV.i0)
    put_or(val, "H1_ALPHA", "verdicts", H1 + ["alpha_ordinal"], VV.r3)
    put_or(val, "H1_ALPHA_REF", "verdicts", H1 + ["alpha_refers_true_both"], VV.r3)
    for b in ("R", "F", "E"):
        put_or(val, f"H1_ALPHA_{b}", "verdicts", H1 + ["alpha_by_block", b], VV.r3)
    put_or(val, "H1_KAPPA", "verdicts", H1 + ["kappa_evaluative"], VV.r3)
    put_or(val, "H1_BRHO", "verdicts", H1 + ["brand_rho", "rho"], VV.r3)
    val.put("H1_BRHO_N", "verdicts", H1 + ["brand_rho", "n"], VV.i0)
    ci_text(val, "H1_BRHO", "verdicts", H1 + ["brand_rho"])
    SATT = ["sensitivities", "S_ATT_v1_11_first"]
    val.word("V_H1_SATT", V["sensitivities"]["S_ATT_v1_11_first"]["H1_Judge_Agreement"]["verdict"],
             ["verdicts"] + SATT + ["H1_Judge_Agreement", "verdict"])
    put_or(val, "H1_ALPHA_SATT", "verdicts", SATT + ["H1_Judge_Agreement", "alpha_ordinal"], VV.r3)
    put_or(val, "H1_BRHO_SATT", "verdicts", SATT + ["H1_Judge_Agreement", "brand_rho", "rho"], VV.r3)
    conf = V["H1_Judge_Agreement"]["confusion_J1_rows_J2_cols"]
    cp = H1 + ["confusion_J1_rows_J2_cols"]
    off = [k for k in conf if k.split("|")[0] != k.split("|")[1]]
    one = [k for k in off if abs(int(k.split("|")[0]) - int(k.split("|")[1])) == 1]
    val.derive("CONF_OFF", VV.d_sum, [("verdicts", cp + [k]) for k in off], VV.i0)
    val.derive("CONF_ONE", VV.d_sum, [("verdicts", cp + [k]) for k in one], VV.i0)
    val.derive("CONF_SAME", VV.d_sum, [("verdicts", cp + [k]) for k in conf if k not in off], VV.i0)
    val.word("CONF_SENTENCE", f"they gave the same valence on {val.vals['CONF_SAME']} units and differed on "
             f"{val.vals['CONF_OFF']}, of which {val.vals['CONF_ONE']} were one step apart.", ["verdicts"] + cp)
    SC = ["self_consistency"]
    put_or(val, "SC_J1_ALL", "verdicts", SC + ["J1", "all", "exact_valence_agreement"], VV.r3)
    put_or(val, "SC_J2_ALL", "verdicts", SC + ["J2", "all", "exact_valence_agreement"], VV.r3)
    cl = Cells(val)
    rows, anyflag = [], False
    for r in ("J1", "J2"):
        for b, lab in (("R", "Recognition"), ("F", "Omnibus"), ("E", "Early"), ("all", "All")):
            pk = SC + [r, b]
            if not VV.has(V, pk):
                continue
            anyflag |= bool(VV.jget(V, pk).get("flag_below_0.90"))
            rows.append([f"{r} ({VV.JUDGE_NAME.get(V['roles'][r], V['roles'][r])})" if b == "R" else "", lab,
                         cl.f("verdicts", pk + ["n"], VV.i0), cl.f("verdicts", pk + ["exact_valence_agreement"], VV.r3),
                         cl.f("verdicts", pk + ["alpha_ordinal"], VV.r3), cl.f("verdicts", pk + ["kappa_evaluative"], VV.r3),
                         "yes" if VV.jget(V, pk).get("flag_below_0.90") else "no"])
    flags["SC_ANY_FLAG"] = anyflag
    val.table("TABLE_SELFCON", md_table(["Judge", "Block", "Pairs", "Exact", "$\\alpha$", "$\\kappa$", "Below 0.90"],
                                        rows, ["l", "l", "r", "r", "r", "r", "l"]), cl.cells)

    # ---------------- 3.5 separability
    cl = Cells(val)
    rows = []
    against = {"H2_Sep_Presence": "Presence $P$", "H3_Sep_Consistency": "Consistency $C^*$",
               "H5_Sep_Ranking": "Ranking $R^*$", "H8_Recognition_Sep": "Presence ($S_{\\text{rec}}$)"}
    for h in VV.SEP_HYPS:
        s = VV.SHORT[h]
        val.word(f"V_{s}", W[s], ["verdicts", "VERDICTS", s])
        rows.append([s, against[h]] + [wave_cells(cl, "verdicts", [h, "per_wave", w]) for w in VV.WAVES] + [W[s]])
    val.table("TABLE_SEP", md_table(["", "Against", "$t_1$", "$t_2$", "$t_3$", "Verdict"], rows,
                                    ["l", "l", "r", "r", "r", "l"]), cl.cells)
    put_or(val, "H5E_RHO", "verdicts", ["H5_secondary_early", "rho"], VV.r3)
    val.put("H5E_N", "verdicts", ["H5_secondary_early", "n"], VV.i0)
    val.word("H5E_V", V["H5_secondary_early"]["verdict"], ["verdicts", "H5_secondary_early", "verdict"])
    pw2 = V["H2_Sep_Presence"]["per_wave"]
    for k, w in enumerate(VV.WAVES, 1):
        put_or(val, f"H2_T{k}", "verdicts", ["H2_Sep_Presence", "per_wave", w, "rho"], VV.p4)
        put_or(val, f"H8_T{k}", "verdicts", ["H8_Recognition_Sep", "per_wave", w, "rho"], VV.r3)
    det = [w for w in VV.WAVES if pw2[w].get("determinable")]
    fals = [w for w in det if abs(pw2[w]["rho"]) >= 0.50]
    marg = [w for w in det if 0.30 < abs(pw2[w]["rho"]) < 0.50]
    if W["H2"] == "FALSIFIED":
        need(fals and all(pw2[w]["rho"] > 0 for w in det), "H2 falsified with positive correlations")
        val.word("H2_FALS_TEXT", f"At {joinand(wave_math(w) for w in fals)} $\\lvert\\rho_w\\rvert$ reached 0.50.",
                 ["verdicts", "H2_Sep_Presence", "per_wave"])
        val.word("H2_FALS_SHORT", f"reaching the falsifying 0.50 line at {joinand(wave_math(w) for w in fals)}",
                 ["verdicts", "H2_Sep_Presence", "per_wave"])
        mtxt = (f" At {joinand(wave_math(w) for w in marg)} it was in the marginal band, not below it." if marg else "")
        val.word("H2_DIRECTION", "All determined correlations are positive: within category, brands with higher "
                 "Presence received warmer descriptions, the failure the v1.7 lesson warns of." + mtxt,
                 ["verdicts", "H2_Sep_Presence", "per_wave"])
        val.word("H2_FIRM", f"The H2 verdict rests on {WORDS.get(len(fals), len(fals))} wave at or above the 0.50 line "
                 f"({joinand(val.vals['H2_T' + w[1]] + ' at ' + wave_math(w) for w in fals)}) and "
                 f"{WORDS.get(len(marg), len(marg))} in the marginal band.", ["verdicts", "H2_Sep_Presence", "per_wave"])
    else:
        for n in ("H2_FALS_TEXT", "H2_FALS_SHORT", "H2_DIRECTION", "H2_FIRM"):
            val.word(n, "", ["H2 not FALSIFIED"])

    def over(h):
        pw = V[h]["per_wave"]
        ws = [w for w in VV.WAVES if pw[w].get("determinable") and abs(pw[w]["rho"]) > 0.30]
        nd = sum(1 for w in VV.WAVES if pw[w].get("determinable"))
        return ("all three determined waves" if len(ws) == nd == 3 else
                f"{WORDS.get(len(ws), len(ws))} of the {WORDS.get(nd, nd)} determined waves ({joinand(wave_math(w) for w in ws)})")
    val.word("H5_OVER", over("H5_Sep_Ranking"), ["verdicts", "H5_Sep_Ranking", "per_wave"])
    val.word("H8_OVER", over("H8_Recognition_Sep"), ["verdicts", "H8_Recognition_Sep", "per_wave"])

    # ---------------- 3.6 stability, 3.7 secondary
    for h in VV.STAB_HYPS:
        s = VV.SHORT[h]
        val.word(f"V_{s}", W[s], ["verdicts", "VERDICTS", s])
        put_or(val, f"{s}_RHO", "verdicts", [h, "rho"], VV.r3)
        val.put(f"{s}_N", "verdicts", [h, "n"], VV.i0)
        ci_text(val, s, "verdicts", [h])
        put_or(val, f"{s}_P", "verdicts", [h, "p_perm"], VV.p4)
    nperm = V["draws"]["perm"]
    val.put("N_PERM", "verdicts", ["draws", "perm"], VV.i0)
    flags["P_MIN"] = all(abs(V[h]["p_perm"] - 1.0 / (nperm + 1)) < 1e-12 and V[h]["perm_draws"] == nperm
                         for h in VV.STAB_HYPS)
    for s in ("H7", "H9"):
        val.word(f"V_{s}", W[s], ["verdicts", "VERDICTS", s])
    put_or(val, "H7_RHO", "verdicts", ["H7_Naming_Frequency", "rho"], VV.r3)
    val.put("H7_N", "verdicts", ["H7_Naming_Frequency", "n"], VV.i0)
    ci_text(val, "H7", "verdicts", ["H7_Naming_Frequency"])
    h7 = V["H7_Naming_Frequency"]["rho"]
    val.word("H7_DIRECTION", "The correlation is positive, the same direction as H2." if h7 > 0 and
             V["H2_Sep_Presence"]["per_wave"]["t1"]["rho"] > 0 else "The correlation is negative.",
             ["verdicts", "H7_Naming_Frequency", "rho"])
    H9 = ["H9_Self_Preference"]
    put_or(val, "H9_OWN", "verdicts", H9 + ["mean_diff_own"], VV.sf2)
    put_or(val, "H9_OTHER", "verdicts", H9 + ["mean_diff_other"], VV.sf2)
    put_or(val, "H9_DELTA", "verdicts", H9 + ["delta_points"], VV.sf2)
    val.put("H9_N_OWN", "verdicts", H9 + ["n_own_provider"], VV.i0)
    val.put("H9_N_OTHER", "verdicts", H9 + ["n_other"], VV.i0)
    flags["H9_NEG"] = V["H9_Self_Preference"]["delta_points"] < 0

    # ---------------- 3.8 verdict table: every pre-registered test exactly once
    stat = {"H1_Judge_Agreement": "ordinal $\\alpha$; brand $\\rho_w(S_{J1}, S_{J2})$",
            "H2_Sep_Presence": "$\\lvert\\rho_w(S, P)\\rvert$ per wave", "H3_Sep_Consistency":
            "$\\lvert\\rho_w(S, C^*)\\rvert$ per wave", "H4_Stability_Short": "$\\rho_w(S_{t_1}, S_{t_2})$, permutation",
            "H5_Sep_Ranking": "$\\lvert\\rho_w(S, R^*)\\rvert$ per wave", "H6_Stability_Long":
            "$\\rho_w(S_{t_2}, S_{t_3})$, permutation", "H7_Naming_Frequency":
            "$\\lvert\\rho_w(S, n_{\\text{named}})\\rvert$, early", "H8_Recognition_Sep":
            "$\\lvert\\rho(S_{\\text{rec}}, P)\\rvert$ per wave", "H9_Self_Preference": "$\\Delta$ of $u_{J1} - u_{J2}$, own vs other"}
    key = {"H1_Judge_Agreement": ("alpha_ordinal", VV.r3), "H4_Stability_Short": ("rho", VV.r3),
           "H6_Stability_Long": ("rho", VV.r3), "H7_Naming_Frequency": ("rho", VV.r3),
           "H9_Self_Preference": ("delta_points", VV.sf2)}
    cl = Cells(val)
    rows = []
    for h in VV.HYPS:
        s = VV.SHORT[h]
        if h in key:
            k, fm = key[h]
            v = cl.f("verdicts", [h, k], fm)
            if h == "H1_Judge_Agreement":
                v = f"$\\alpha$ {v}; $\\rho_w$ {cl.f('verdicts', [h, 'brand_rho', 'rho'], VV.r3)}"
        else:
            v = " / ".join(cl.f("verdicts", [h, "per_wave", w, "rho"], VV.r3) for w in VV.WAVES)
        before = V["verdicts_before_noise_guard"][s]
        rows.append([h.replace("_", "\\_"), VV.TIER[s], stat[h], v, W[s] + ("" if before == W[s] else f" ({before})")])
    val.table("TABLE_VERDICTS", md_table(["Test", "Tier", "Statistic", "Value(s)", "Verdict"], rows,
                                         ["l", "l", "l", "r", "l"]), cl.cells)

    # ---------------- 3.9 sensitivities
    sens = V["sensitivities"]
    ch = list(sens.get("verdict_changes") or [])
    # v1.11 5.1: "verdict changes under any sensitivity are listed" -- the scorer lists the full variants; the H2/H3-only
    # variants (NV, model-balanced, J2-scored) are compared here with the primary words, nothing re-decided.
    VAR = [("S_NV_in_place_of_S", "NV in place of S"), ("S_model_balanced", "model-balanced S"),
           ("S_J2_scored", "J2-scored S"), ("S_without_J1_provider_answers", "S without J1-provider answers")]
    ch_var = [{"sensitivity": lab, "hypothesis": hk, "primary": V["verdicts_before_noise_guard"][hk],
               "under_sensitivity": sens[k][hk]["verdict"]}
              for k, lab in VAR if k in sens for hk in ("H2", "H3")
              if sens[k][hk]["verdict"] != V["verdicts_before_noise_guard"][hk]]
    allch = [{**c, "sensitivity": SENS_NAME.get(c["sensitivity"], c["sensitivity"])} for c in ch] + ch_var
    val.word("SENS_SENTENCE", "No verdict changed under any sensitivity analysis." if not allch else
             "Verdicts that differ under a sensitivity analysis (never replacing the primary verdict): " + "; ".join(
                 f"{c['hypothesis']} under {c['sensitivity']}, {c['primary']} $\\rightarrow$ {c['under_sensitivity']}"
                 for c in allch) + ".", ["verdicts", "sensitivities", "verdict_changes", "+ H2/H3 variants"])
    satt = [c for c in ch if c["sensitivity"] == "S_ATT_v1_11_first"]
    val.word("SATT_SENTENCE", "Scoring v1.11's own attempt where v1.11's rule yields a judgement (S-ATT) changes no "
             "verdict." if not satt else "Scoring v1.11's own attempt (S-ATT) changes "
             + joinand(c["hypothesis"] for c in satt) + ".", ["verdicts", "sensitivities", "verdict_changes"])
    rows = []
    for h in VV.HYPS:
        s = VV.SHORT[h]
        row = [s, V["verdicts_before_noise_guard"][s]]
        for name in SENS_ORDER:
            d = sens[name]
            row.append(d[h]["verdict"] if h in d else "--")
        rows.append(row)
    val.table("TABLE_SENS", md_table(["", "Primary", "SU", "SD", "S-ATT", "S-CUT", "S-CUT-M"], rows,
                                     ["l"] * 7), [])
    cl = Cells(val)
    rows = [["Primary", W["H2"]] + [wave_cells(cl, "verdicts", ["H2_Sep_Presence", "per_wave", w]) for w in VV.WAVES]]
    for name in SENS_ORDER:
        pk = ["sensitivities", name, "H2_Sep_Presence"]
        rows.append([SENS_NAME[name], VV.jget(V, pk)["verdict"]] + [wave_cells(cl, "verdicts", pk + ["per_wave", w])
                                                                   for w in VV.WAVES])
    for k, lab in VAR:
        if k in sens:
            pk = ["sensitivities", k, "H2"]
            rows.append([lab[0].upper() + lab[1:], VV.jget(V, pk)["verdict"]] +
                        [wave_cells(cl, "verdicts", pk + ["per_wave", w]) for w in VV.WAVES])
    val.table("TABLE_H2_SENS", md_table(["Analysis", "H2", "$t_1$", "$t_2$", "$t_3$"], rows,
                                        ["l", "l", "r", "r", "r"]), cl.cells)
    # every H2 variant: none confirmed, every determined rho positive (premise of H2_ROBUST)
    h2v = [V["H2_Sep_Presence"]] + [sens[n]["H2_Sep_Presence"] for n in SENS_ORDER] + [sens[k]["H2"] for k, _ in VAR
                                                                                        if k in sens]
    need(all(x["verdict"] != "CONFIRMED" for x in h2v), "no H2 variant CONFIRMED")
    need(all(x["per_wave"][w]["rho"] > 0 for x in h2v for w in VV.WAVES if x["per_wave"][w].get("determinable")),
         "every H2 variant positive at every determined wave")
    nvar = len(h2v) - 1
    marg_var = [r[0] for r in rows[1:] if r[1] == "MARGINAL"]
    val.word("H2_ROBUST", f"No variant put H2 in the confirmed band, and the correlation with Presence was positive at "
             f"every determined wave in the primary analysis and in all {WORDS.get(nvar, nvar)} variants "
             f"(Table 7); {joinand(marg_var)} give MARGINAL, the others FALSIFIED. The falsification is narrow, not a "
             "sign that Sentiment is separable from Presence, and the pre-registered verdict, H2 FALSIFIED, stands.",
             ["verdicts", "sensitivities", "H2"])
    cutd = V["descriptives"]["cut_answers"]
    DC = ["descriptives", "cut_answers"]
    val.derive("CUT_UNITS", VV.d_sum, [("verdicts", DC + ["S_CUT", k, "units"]) for k in cutd["S_CUT"]], VV.i0)
    val.derive("CUTM_UNITS", VV.d_sum, [("verdicts", DC + ["S_CUT_M", k, "units"]) for k in cutd["S_CUT_M"]], VV.i0)
    val.put("CUT_ANSWERS", "verdicts", ["cut_list", "answers_flagged"], VV.i0)
    val.derive("CUT_M_CELLS", VV.d_len, [("verdicts", ["cut_list", "s_cut_m_cells"])], VV.i0)
    need(L["rows"] == V["cut_list"]["answers_flagged"], "cut list rows equal answers_flagged")
    G = ["groups"]
    rt12 = list(L["groups"]["R t1/t2 flagged"])
    need(all("inferred" in k for k in rt12), "R t1/t2 rows are the inferred ones")
    fa, fr = "F cut after naming a brand (unit kept), all evidence", "F cut after naming a brand, recorded evidence only"
    refs = ([("cutlist", G + ["R t1/t2 flagged", k]) for k in rt12] + [("cutlist", G + [fa, w]) for w in L["groups"][fa]]
            + [("cutlist", G + [fr, w]) for w in L["groups"][fr]])
    signs = tuple([1] * len(rt12) + [1] * len(L["groups"][fa]) + [-1] * len(L["groups"][fr]))
    val.derive("CUT_INFERRED", VV.d_signed, refs, VV.i0, consts=(signs,))
    sc, scm = sens["S_CUT_without_cut_answers"]["H2_Sep_Presence"], sens["S_CUT_M_without_cut_cells"]["H2_Sep_Presence"]
    for nm, d in (("SCUT", "S_CUT_without_cut_answers"), ("SCUTM", "S_CUT_M_without_cut_cells")):
        for k, w in enumerate(VV.WAVES, 1):
            val.put(f"{nm}_T{k}", "verdicts", ["sensitivities", d, "H2_Sep_Presence", "per_wave", w, "rho"], VV.p4)
    val.word("CUT_SENTENCE", f"Without the {val.vals['CUT_UNITS']} units whose answer is in the cut-answer list "
             f"(S-CUT), $\\rho_w(S, P)$ was {val.vals['SCUT_T1']}, {val.vals['SCUT_T2']} and {val.vals['SCUT_T3']} "
             f"(H2 {sc['verdict']}); without the {val.vals['CUTM_UNITS']} units of the mostly cut cells (S-CUT-M), "
             f"{val.vals['SCUTM_T1']}, {val.vals['SCUTM_T2']} and {val.vals['SCUTM_T3']} (H2 {scm['verdict']}). "
             "The units are listed in the appendix.", ["verdicts", "sensitivities"])
    if W["H2"] == "FALSIFIED":
        need(sc["verdict"] == scm["verdict"] == "MARGINAL" and max(sc["per_wave"][w]["rho"] for w in VV.WAVES) < 0.5
             and max(scm["per_wave"][w]["rho"] for w in VV.WAVES) < 0.5, "cut sensitivities move H2 below the line")
        val.word("CUT_DISCUSSION", f"Without the answers that ended, or probably ended, at the answering models' output "
                 f"limit, the $t_3$ correlation falls to {val.vals['SCUT_T3']} (S-CUT) or {val.vals['SCUTM_T3']} "
                 "(S-CUT-M), below the line, and H2 is MARGINAL in both.", ["verdicts", "sensitivities"])
    else:
        val.word("CUT_DISCUSSION", "", ["H2 not FALSIFIED"])
    abs_parts = []
    if any(c["hypothesis"] == "H2" and c["sensitivity"] in ("S-CUT", "S-CUT-M") for c in allch):
        abs_parts.append("without the answers that ended at the answering models' output limit (S-CUT, S-CUT-M), H2 "
                         "is MARGINAL")
    other = [c for c in allch if not (c["hypothesis"] == "H2" and c["sensitivity"] in ("S-CUT", "S-CUT-M"))]
    abs_parts += [f"under {c['sensitivity']}, {c['hypothesis']} is {c['under_sensitivity']}" for c in other]
    val.word("ABS_SENS", ("In sensitivity analyses, " + "; ".join(abs_parts) + "; the primary verdicts stand.")
             if abs_parts else "No sensitivity analysis changed a verdict.", ["verdicts", "sensitivities"])
    cl = Cells(val)
    rows = []
    for setname, lab in (("S_CUT", "S-CUT"), ("S_CUT_M", "S-CUT-M")):
        for k in sorted(cutd[setname]):
            b, w, c, m = k.split("|")
            pk = DC + [setname, k]
            rows.append([lab, BLOCK[b], w, VV.CAT_SHORT.get(c, c), f"`{m}`", cl.f("verdicts", pk + ["units"], VV.i0),
                         cl.f("verdicts", pk + ["judged"], VV.i0), cl.f("verdicts", pk + ["j2_sample"], VV.i0),
                         cl.f("verdicts", pk + ["paper_b_sample"], VV.i0)])
    val.table("TABLE_CUT", md_table(["List", "Block", "Wave", "Category", "Model", "Units", "Judged", "J2",
                                     "Paper B"], rows, ["l", "l", "l", "l", "l", "r", "r", "r", "r"]), cl.cells)
    cl = Cells(val)
    rows = []
    for b in ("R", "F", "E"):
        rows.append([f"$\\alpha$, block {b}", "", cl.f("verdicts", H1 + ["alpha_by_block", b], VV.r3), "", "", ""])
    for k, lab in VAR:
        if k not in sens:
            continue
        for hk in ("H2", "H3"):
            pk = ["sensitivities", k, hk]
            rows.append([f"{lab[0].upper() + lab[1:]}, {hk}", VV.jget(V, pk)["verdict"], ""]
                        + [wave_cells(cl, "verdicts", pk + ["per_wave", w]) for w in VV.WAVES])
    val.table("TABLE_SENS_S", md_table(["Variant", "Verdict", "Value", "$t_1$", "$t_2$", "$t_3$"], rows,
                                       ["l", "l", "r", "r", "r", "r"]), cl.cells)
    baseline(val, V)
    return val, cases, flags, allch


def baseline(val, V):
    """3.10 and the appendix (v1.11 section 6), as in fill_paper_v1_11.py."""
    D = ["descriptives"]
    base = V["descriptives"]["baseline"]
    order = sorted(range(len(base)), key=lambda i: ({"R": 0, "F": 1, "E": 2}[base[i]["block"]], base[i]["category"],
                                                    base[i]["wave"]))
    lab = lambda b: (VV.CAT_SHORT.get(b["category"], b["category"]) if b["block"] != "E"   # noqa: E731
                     else VV.EARLY_SHORT.get(b["category"], b["category"]))
    cl = Cells(val)
    rows = []
    for i in order:
        b = base[i]
        pk = D + ["baseline", i]
        rows.append([BLOCK[b["block"]], lab(b), b["wave"],
                     cl.f("verdicts", pk + ["brands"], VV.i0), cl.f("verdicts", pk + ["brands_rated"], VV.i0),
                     cl.f("verdicts", pk + ["S", "median"], VV.f1),
                     f"{cl.f('verdicts', pk + ['S', 'q25'], VV.f1)}--{cl.f('verdicts', pk + ['S', 'q75'], VV.f1)}",
                     cl.f("verdicts", pk + ["E_mean"], VV.r2), cl.f("verdicts", pk + ["share_non_evaluative"], VV.pct0),
                     cl.f("verdicts", pk + ["share_mixed"], VV.pct0), cl.f("verdicts", pk + ["share_refers_false"], VV.pct1)])
    val.table("TABLE_BASE", md_table(["Block", "Category", "Wave", "Brands", "Rated", "S median", "S IQR", "E",
                                      "Non-eval.", "Mixed", "Not brand"], rows,
                                     ["l", "l", "l", "r", "r", "r", "r", "r", "r", "r", "r"]), cl.cells)
    cl = Cells(val)
    rows = []
    miss = V["descriptives"].get("extraction_misses_by_set") or {}
    for i in order:
        b = base[i]
        pk = D + ["baseline", i]
        set_key = (f"OMNI {b['wave']} {b['category']}" if b["block"] == "F"
                   else f"EARLY-6 {b['wave']} {b['category']}" if b["block"] == "E" else None)
        rows.append([BLOCK[b["block"]], lab(b), b["wave"],
                     cl.f("verdicts", pk + ["units"], VV.i0), cl.f("verdicts", pk + ["judge_fail"], VV.i0),
                     cl.f("verdicts", pk + ["unjudged"], VV.i0), cl.f("verdicts", pk + ["bare_share"], VV.pct1),
                     cl.f("verdicts", D + ["extraction_misses_by_set", set_key], VV.i0) if set_key in miss else "--"])
    val.table("TABLE_BASE2", md_table(["Block", "Category", "Wave", "Judged units", "JUDGE_FAIL", "UNJUDGED",
                                       "Bare windows", "Extraction misses"], rows,
                                      ["l", "l", "l", "r", "r", "r", "r", "r"]), cl.cells)
    for blk, nm in (("F", "BASE_F"), ("E", "BASE_E")):
        refs = [("verdicts", D + ["baseline", i, "S", "median"]) for i, b in enumerate(base)
                if b["block"] == blk and VV.has(V, D + ["baseline", i, "S", "median"])]
        val.derive(f"{nm}_MIN", VV.d_min, refs, VV.f1)
        val.derive(f"{nm}_MAX", VV.d_max, refs, VV.f1)
    put_or(val, "PANEL_LEGACY", "verdicts", D + ["mean_u", "by panel", "LEGACY-6", "mean_u"], VV.f1)
    put_or(val, "PANEL_EARLY", "verdicts", D + ["mean_u", "by panel", "EARLY-6", "mean_u"], VV.f1)
    for k, w in enumerate(VV.WAVES, 1):
        put_or(val, f"CONV_T{k}", "verdicts", D + ["convergence_rec_vs_frames", w, "spearman"], VV.r3)
        val.put(f"CONV_N{k}", "verdicts", D + ["convergence_rec_vs_frames", w, "n"], VV.i0)
    cl = Cells(val)
    mu = V["descriptives"]["mean_u"]
    models = sorted({m for g in ("R by model", "F by model", "E by model") for m in (mu.get(g) or {})})
    rows = []
    for m in models:
        rows.append([f"`{m}`"] + [cl.f("verdicts", D + ["mean_u", g, m, "mean_u"], VV.f1) + " (" +
                                  cl.f("verdicts", D + ["mean_u", g, m, "n"], VV.i0) + ")"
                                  if VV.has(V, D + ["mean_u", g, m]) else "--"
                                  for g in ("R by model", "F by model", "E by model")])
    val.table("TABLE_MODEL", md_table(["Answering model", "Recognition", "Omnibus", "Early"], rows), cl.cells)
    cl = Cells(val)
    rows = []
    for g, lb in (("R by frame", "Recognition"), ("F by frame", "Omnibus"), ("E by frame", "Early")):
        for k, fr in enumerate(sorted(mu.get(g) or {})):
            pk = D + ["mean_u", g, fr]
            rows.append([lb if k == 0 else "", f"`{fr}`", cl.f("verdicts", pk + ["mean_u"], VV.f1),
                         cl.f("verdicts", pk + ["n"], VV.i0)])
    val.table("TABLE_FRAME", md_table(["Block", "Frame / prompt", "Mean u", "Units"], rows,
                                      ["l", "l", "r", "r"]), cl.cells)
    lg = V["descriptives"].get("legacy_label_agreement") or {}
    if lg.get("n"):
        n = val.put("LEGACY_N", "verdicts", D + ["legacy_label_agreement", "n"], VV.i0)
        a = val.put("LEGACY_AGREE", "verdicts", D + ["legacy_label_agreement", "agreement"], VV.pct1)
        val.word("LEGACY_SENTENCE", f"Exploratory (v1.11 §6.6): on {n} (answer, brand) pairs of the five v0.9 early "
                 f"sets, the sign of J1's valence agreed with the archived per-brand label in {a} of pairs.",
                 ["verdicts"] + D + ["legacy_label_agreement"])
    else:
        val.word("LEGACY_SENTENCE", "Exploratory (v1.11 §6.6): not computed.", ["verdicts"] + D)


# =========================================================================== checks and main
def deviations_text():
    counts = {}
    for lab, p in DEV_FILES.items():
        if not p.exists():
            raise FillError(f"{p} not found")
        counts[lab] = re.findall(r"(?m)^## Entry (\d+)\b", p.read_text(encoding="utf-8"))
    a, c, v = counts.values()
    ent = lambda xs: joinand(xs)  # noqa: E731
    s = (f"The deviations records (OSF `methodology/`) hold, for v1.11, Entries {ent(a)} (`v1_11/anchor/DEVIATIONS.md`: "
         f"the conflict-of-interest screen, the Denon correction and the pre-lock record; the replacement of two Denon "
         f"units in the Paper B sample) and Entry {ent(c)} in its post-lock continuation "
         f"(`v1_11/postlock/`: the successor rule, recorded ex ante before the first judge call); "
         f"and, for v1.20, Entries {ent(v)} (`v1_20/anchor/DEVIATIONS.md`, both ex ante, before its "
         f"lock). No entry was made after a judge reply existed.")
    return s, [str(p.relative_to(ROOT)) for p in DEV_FILES.values()]


def tag_info(tag):
    commit = VV.git_tag_commit(tag)
    r = subprocess.run(["git", "-C", str(ROOT), "for-each-ref", "--format=%(taggerdate:iso-strict)",
                        f"refs/tags/{tag}"], capture_output=True, text=True)
    d = r.stdout.strip()
    return commit, (datetime.fromisoformat(d).strftime("%-d %B %Y") if d else None)


def read_halt_log():
    import ast
    h = VV.v111_halt_log()
    m = re.search(r"units: (\[.*?\])", h["halt_line"] or "")
    if not m:
        raise FillError("v1.11's Stage J console record carries no halt list")
    return {"sets": ast.literal_eval(m.group(1)), "exit": h["exit"], "started": h["started_utc"]}


def verify_real(src, outputs):
    if VV.is_synthetic(src):
        raise FillError("the outputs are synthetic (dry_run / synthetic_fixture)")
    V, J, C, F, P, R = (src[k] for k in ("verdicts", "stage_j", "comparison", "frozen", "plan", "run"))
    if V.get("prereg_tag") != VV.EXPECTED_PREREG_TAG or V.get("stage") != "C" or J.get("stage") != "J":
        raise FillError("not v1.20-prereg-r1 Stage C and Stage J outputs")
    if V.get("successor_of_tag") != VV.V111_TAG:
        raise FillError("v1.20 is not recorded as the successor of v1.11-prereg-r1")
    if V.get("stage_j_sha256") != VV.sha256(VV.source_path(outputs, "stage_j")):
        raise FillError("the verdicts were not computed from this Stage J file")
    if J.get("v1_11_frozen_sha256") != VV.sha256(VV.source_path(outputs, "frozen")):
        raise FillError("Stage J was not computed from this frozen record")
    if F.get("plan_sha256") != VV.sha256(VV.source_path(outputs, "plan")):
        raise FillError("the plan file is not the one the frozen record names")
    if R.get("raw_sha256") != F.get("raw_sha256"):
        raise FillError("run values not made from the frozen raw file")
    if V.get("cut_list", {}).get("json_sha256") != VV.sha256(VV.source_path(outputs, "cutlist")):
        raise FillError("cut list file differs from the one v1.20's Stage C used")
    if not (F.get("units_sha256") == V.get("units_sha256") == J.get("units_sha256") == C.get("units_sha256")):
        raise FillError("different unit tables")
    if C.get("config_sha256") != V.get("config_sha256") or J.get("switches") != V.get("switches"):
        raise FillError("switches differ between stages")
    tags = {}
    for tag, anchor in ANCHORS.items():
        commit, date = tag_info(tag)
        if not commit:
            raise FillError(f"tag {tag} not found")
        an = json.loads(anchor.read_text(encoding="utf-8"))
        if an.get("commit") != commit or not (an.get("osf_deposit") or "").strip():
            raise FillError(f"anchor {anchor.name} does not name {commit} with an OSF deposit")
        tags[tag] = (commit, date)
    return tags


def fill(outputs, out=None, fig_dir=None, template=TEMPLATE):
    src = VV.load_sources(outputs)
    tags = verify_real(src, outputs)
    check_consistency(src)
    fig_dir = fig_dir or "../../reports/figs/v120"
    val, cases, flags, allch = compute(src, False, fig_dir, tags, deviations_text(), read_halt_log())
    text = render(Path(template).read_text(encoding="utf-8"), val.vals, cases, flags)
    if out:
        out = Path(out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        prov = {"outputs": str(outputs), "synthetic": False, "cases": cases, "flags": flags,
                "verdict_changes_reported": allch, "values": val.prov}
        Path(str(out).replace(".md", "_provenance.json")).write_text(
            json.dumps(prov, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
    return text, val, cases, flags


def main(argv=None):
    ap = argparse.ArgumentParser(description="Fill the Sentiment Paper A (v1.11 / v1.20) template")
    ap.add_argument("--outputs", type=Path, default=VV.OUTDIR)
    ap.add_argument("--fig-dir", default=None)
    ap.add_argument("--out", type=Path, default=HERE / "v1_20_paper_draft.md")
    a = ap.parse_args(argv)
    try:
        text, val, cases, flags = fill(a.outputs, a.out, a.fig_dir)
    except (FillError, VV.Missing) as e:
        print(f"[fill v1.20] REFUSED: {e}", file=sys.stderr)
        return 3
    print(f"[fill v1.20] wrote {a.out} ({len(text.split())} words); cases {cases}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
