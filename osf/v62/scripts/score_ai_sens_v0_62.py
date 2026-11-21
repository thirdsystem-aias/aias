#!/usr/bin/env python3
"""
score_ai_sens_v0_62.py -- AIAS(TM) v0.62: the sensitivities S-Trans and S-AliasAI of DEVIATIONS Entry 2 (b)-(d),
as parameters of the scorer, WITHOUT changing any confirmatory statistic, threshold or unit set.

Why a separate module: score_v0_62.py is one of the 73 files of prereg/LOCK_MANIFEST_v0_62.sha256 (tag
v0.62-prereg-r1) and Entry 2 states that the locked files are not modified. This module imports score_v0_62 UNCHANGED
and adds keyword parameters to its score(): score(..., s_trans=None, en_B=None, s_alias_ai=None). With the new
parameters left at None it returns score_v0_62.score()'s result object itself (byte-identical JSON; tested), and with
them it only ADDS the key "sensitivities_ai_check"; "tests", "sensitivities", "joint_reading" and every other key are
those of score_v0_62.score() (tested).

S-Trans (Entry 2 (b); per language; reported beside every confirmatory test, never changing a verdict):
  every statistic of score_v0_62.score() recomputed without the Phase B questions FLAGGED in that language (a second
  line without the STRICTLY FLAGGED ones only), with the English t4 comparator recomputed on the same reduced question
  set from t4's coded English Phase B rows (en_B). Questions are identified by (substrate, probe_id): the row's
  `probe_id` field, else the 4th field of a v0.62 call_id 'lang|substrate|B|probe_id|model|cond|run'. With q of the
  six questions of a category removed, the kernels run with F = 6 - q for that category (pi_hat over the answered
  calls left; phi per run on F questions; a model-run counts as complete when it has F answered calls); a category
  with all six removed has no unit in the test. The kernels are transcriptions of score_v0_62.phi_m / unit_values with
  F a parameter, identical to them at F = 6 (tested). H_Lang_Rank under S-Trans needs v1.14's R* on the reduced set
  (rank_trans); without it the test reads NOT TESTED. If an H_Lang_Presence verdict differs from the primary one, the
  line carries presence_differs = True (the paper then reports both in its abstract, as for S-Denon / S-Headphones /
  S-COI). Input: results/s_trans_flags_v0_62.json of ai_check_v0_62.py --analyze.
S-AliasAI (Entry 2 (c); Korean, Chinese): H_Lang_Presence on the coded Phase B rows of a coding re-run with the aliases
  C4 coded "not used for this brand" switched off (alias_ai_aliaser() builds that coder input from code_v0_62's
  alias table, unchanged otherwise; code_v0_62.prepare_raw(..., aliaser=...) then v0.42's coder, as for the primary
  coding). English comparator, units, seeds and thresholds as the primary test. Input: s_alias_ai_off_v0_62.json.
"""
import collections
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import score_v0_62 as S  # noqa: E402  (locked; imported unchanged)

LINES = ("flagged", "strictly_flagged")


def sub_key(s):
    """'v0.19' / 'v19' -> 'v19'."""
    s = str(s)
    return "v" + s[3:] if s.startswith("v0.") else s


def question_of(row):
    q = row.get("probe_id")
    if q:
        return (sub_key(row["substrate"]), q)
    parts = str(row.get("call_id", "")).split("|")
    if len(parts) == 7 and parts[2] == "B":
        return (sub_key(parts[1]), parts[3])
    raise ValueError(f"row without probe_id and without a v0.62 call_id: {row.get('call_id')!r}")


def removed_set(keys):
    """['v20|q1', ...] (ai_check_v0_62 Phase B keys) or [(sub, probe_id)] -> {(sub, probe_id)}."""
    out = set()
    for k in keys or []:
        if isinstance(k, str):
            s, q = k.split("|", 1)
        else:
            s, q = k
        out.add((sub_key(s), q))
    return out


def drop_questions(rows, removed):
    return [r for r in rows if question_of(r) not in removed] if removed else list(rows)


def f_by_sub(removed, f=S.F):
    c = collections.Counter(s for s, _q in removed)
    return {s: f - c[s] for s in ("v19", "v20", "v21", "v22", "v23")}


# ------------------------------------------------------------------ kernels with F a parameter (identical at F = 6)
def phi_m_f(k, F):
    """score_v0_62.phi_m with F a parameter."""
    k = np.asarray(k, float)
    m = len(k)
    pi = float(k.sum() / (m * F))
    if pi <= 0.0:
        return None, pi, "zero"
    if pi >= 1.0:
        return None, pi, "saturated"
    return float(((k - F * pi) ** 2).sum() / (F * pi * (1.0 - pi)) / (m - 1)), pi, "defined"


def unit_values_f(units, B, fsub, models=S.MODELS):
    """score_v0_62.unit_values with F per category (fsub: {'v19': F, ...}); F = 0 -> the unit has no value."""
    k, ans = S.aggregate(B)
    out = {}
    for (s, b) in units:
        F = fsub[sub_key(s)]
        num = sum(k[(m, r, s, b)] for m in models for r in S.RUNS)
        den = sum(len(ans[(m, r, s)]) for m in models for r in S.RUNS)
        runs = []
        for r in S.RUNS:
            if F <= 0 or any(len(ans[(m, r, s)]) != F for m in models):
                runs.append((None, "missing"))
                continue
            phi, _pi, part = phi_m_f([k[(m, r, s, b)] for m in models], F)
            runs.append((phi, part))
        vals = [p for p, part in runs if part == "defined"]
        parts = [part for _, part in runs]
        if len(vals) >= 2:
            phi, part = float(np.mean(vals)), "defined"
        elif parts and all(p == "zero" for p in parts):
            phi, part = None, "zero"
        elif parts and all(p == "saturated" for p in parts):
            phi, part = None, "saturated"
        else:
            phi, part = None, "undefined"
        out[(s, b)] = {"pi": num / den if den and F > 0 else S.NAN, "phi": phi, "partition": part}
    return out


# ------------------------------------------------------------------ one language, values given (mirrors S.score)
def score_language(lg, units, en, V, B, n_b_per_run, rank=None, rank_status="NOT RESOLVED", option=None,
                   n_perm=S.N_PERM, n_boot=S.N_BOOT):
    """The body of score_v0_62.score() for one language, with the language's unit values V given (so that the
    kernels may run on a reduced question set). Identical to score_v0_62.score() when V = S.unit_values(units, B)
    and n_b_per_run = 30 (tested)."""
    option = option or S.P.HEADPHONES_OPTION
    keys = S.unit_set(units, option)
    tests, sens = {}, {}
    drop = S.dropped_models(B, n_b_per_run)
    und = f"models below 90% of Phase B calls in {lg}: {drop}" if drop else None
    xpi, ypi = {u: en[u]["pi"] for u in en}, {u: V[u]["pi"] for u in V}
    t = S.rank_test(xpi, ypi, keys, S.SEEDS[("H_Lang_Presence", lg)], n_perm, n_boot)
    t["verdict"] = "UNDETERMINED" if und else S.verdict_presence(t["rho_c"], t["p_perm"])
    _k, x, y, g = S._pairs(xpi, ypi, keys)
    t["delta_L"] = float(np.mean(y - x)) if len(x) else S.NAN
    t["delta_L_ci95"] = S.bootstrap_ci(g, S.SEEDS["bootstrap"], n_boot, lambda i: float(np.mean(y[i] - x[i]))) \
        if len(x) else [S.NAN, S.NAN]
    if und:
        t["reason"] = und
    tests[f"H_Lang_Presence_{lg}"] = t
    xph = {u: en[u]["phi"] for u in en if en[u].get("phi") is not None}
    yph = {u: V[u]["phi"] for u in V if V[u]["phi"] is not None}
    tp = S.rank_test(xph, yph, keys, S.SEEDS[("H_Lang_Phi", lg)], n_perm, n_boot)
    tp["verdict"] = "UNDETERMINED" if und else S.verdict_phi(tp["n"], tp["rho_c"], tp["p_perm"])
    tp["partitions"] = dict(collections.Counter(V[u]["partition"] for u in keys))
    tests[f"H_Lang_Phi_{lg}"] = tp
    if rank_status != "PASS" or not rank:
        tests[f"H_Lang_Rank_{lg}"] = {"verdict": "NOT TESTED", "reason": f"v1.14 status: {rank_status}"}
    else:
        tr = S.rank_test(rank["en"], rank[lg], keys, S.SEEDS[("H_Lang_Rank", lg)], n_perm, n_boot, min_cat=5)
        vals = [rank[lg][k] for k in keys if k in rank[lg] and k in rank["en"]]
        deg = bool(vals) and collections.Counter(vals).most_common(1)[0][1] > 0.8 * len(vals)
        tr["verdict"] = "UNDETERMINED" if und else S.verdict_rank(tr["n"], tr["rho_c"], tr["p_perm"], deg)
        tests[f"H_Lang_Rank_{lg}"] = tr
    for s_ in ("S-Denon", "S-Headphones", "S-COI"):
        if s_ != "S-COI" and (option == "C" or (option == "B" and s_ == "S-Denon")):
            sens[f"{s_}_{lg}"] = {"void": f"headphones option {option}"}
            continue
        ks = S.unit_set(units, option, s_)
        s = S.rank_test(xpi, ypi, ks, S.SEEDS[("H_Lang_Presence", lg)], n_perm, n_boot)
        s["verdict"] = "UNDETERMINED" if und else S.verdict_presence(s["rho_c"], s["p_perm"])
        sens[f"{s_}_{lg}"] = s
    return tests, sens


# ------------------------------------------------------------------ the sensitivities
def s_trans_block(units, en_B, lang_B, s_trans, primary, n_b_per_run=30, rank_trans=None, option=None,
                  n_perm=S.N_PERM, n_boot=S.N_BOOT):
    out = {}
    for line in LINES:
        res = {"tests": {}, "sensitivities": {}, "removed": {}, "presence_differs": {}}
        for lg in S.LANGS:
            rem = removed_set((s_trans.get(lg) or {}).get(line))
            fs = f_by_sub(rem)
            B = drop_questions(lang_B[lg], rem)
            E = drop_questions(en_B, rem)
            V = unit_values_f(units, B, fs)
            EV = unit_values_f(units, E, fs)
            en = {u: {"pi": EV[u]["pi"], "phi": EV[u]["phi"]} for u in EV}
            rk = (rank_trans or {}).get(line, {}).get(lg)
            rstat = "PASS" if rk else "S-Trans: R* on the reduced question set not supplied"
            t, s = score_language(lg, units, en, V, B, n_b_per_run - len(rem), rk, rstat, option, n_perm, n_boot)
            res["tests"].update(t)
            res["sensitivities"].update(s)
            res["removed"][lg] = sorted(f"{a}|{b}" for a, b in rem)
            pv = primary["tests"][f"H_Lang_Presence_{lg}"]["verdict"]
            res["presence_differs"][lg] = t[f"H_Lang_Presence_{lg}"]["verdict"] != pv
        res["joint_reading"] = S.joint_reading(*(res["tests"][f"H_Lang_Presence_{lg}"]["verdict"] for lg in S.LANGS))
        out[line] = res
    return out


def s_alias_ai_block(units, en, lang_B_alias_ai, primary, n_b_per_run=30, option=None, n_perm=S.N_PERM,
                     n_boot=S.N_BOOT):
    option = option or S.P.HEADPHONES_OPTION
    keys = S.unit_set(units, option)
    out = {}
    for lg, B in lang_B_alias_ai.items():
        if lg not in ("ko", "zh"):
            raise ValueError(f"S-AliasAI is defined for Korean and Chinese only, not {lg!r}")
        V = S.unit_values(units, B)
        drop = S.dropped_models(B, n_b_per_run)
        xpi, ypi = {u: en[u]["pi"] for u in en}, {u: V[u]["pi"] for u in V}
        t = S.rank_test(xpi, ypi, keys, S.SEEDS[("H_Lang_Presence", lg)], n_perm, n_boot)
        t["verdict"] = "UNDETERMINED" if drop else S.verdict_presence(t["rho_c"], t["p_perm"])
        if drop:
            t["reason"] = f"models below 90% of Phase B calls in {lg}: {drop}"
        t["presence_differs"] = t["verdict"] != primary["tests"][f"H_Lang_Presence_{lg}"]["verdict"]
        out[f"S-AliasAI_{lg}"] = t
    return out


def score(units, en, lang_B, n_b_per_run=30, rank=None, rank_status="NOT RESOLVED", option=None,
          n_perm=S.N_PERM, n_boot=S.N_BOOT, *, s_trans=None, en_B=None, rank_trans=None, s_alias_ai=None):
    """score_v0_62.score() with two optional sensitivities (Entry 2 (b), (c)).
    s_trans: {'es': {'flagged': [...], 'strictly_flagged': [...]}, 'ko': ..., 'zh': ...} with en_B (t4's coded English
    Phase B rows); s_alias_ai: {'ko': coded Phase B rows with the C4-'not used' aliases off, 'zh': ...}.
    Both None -> exactly score_v0_62.score()'s result."""
    out = S.score(units, en, lang_B, n_b_per_run, rank, rank_status, option, n_perm, n_boot)
    if s_trans is None and s_alias_ai is None:
        return out
    extra = {}
    if s_trans is not None:
        if en_B is None:
            raise ValueError("S-Trans needs en_B, t4's coded English Phase B rows")
        extra["S-Trans"] = s_trans_block(units, en_B, lang_B, s_trans, out, n_b_per_run, rank_trans, option,
                                         n_perm, n_boot)
    if s_alias_ai is not None:
        extra["S-AliasAI"] = s_alias_ai_block(units, en, s_alias_ai, out, n_b_per_run, option, n_perm, n_boot)
    out["sensitivities_ai_check"] = extra
    return out


# ------------------------------------------------------------------ S-AliasAI coder input
def alias_ai_aliaser(off, path=None):
    """code_v0_62.Aliaser on the locked alias table minus the aliases in `off` ([[substrate, brand, alias]], from
    s_alias_ai_off_v0_62.json). Raises if an entry is not in the table. -> (aliaser, n removed)."""
    import code_v0_62 as C
    rows = C.load_aliases(path)
    off = {(sub_key(s), b, a) for s, b, a in off}
    present = {(sub_key(r[0]), r[1], r[2]) for r in rows}
    unknown = off - present
    if unknown:
        raise ValueError(f"aliases not in the table: {sorted(unknown)}")
    keep = [r for r in rows if (sub_key(r[0]), r[1], r[2]) not in off]
    return C.Aliaser(keep), len(rows) - len(keep)
