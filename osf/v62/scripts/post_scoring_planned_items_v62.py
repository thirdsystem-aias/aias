#!/usr/bin/env python3
"""
post_scoring_planned_items_v62.py -- AIAS v0.62, the pre-registered items that the locked scorer did not compute
(DEVIATIONS Entry 7; written Wed 2026-11-25, after the one scoring run of commit 262464d; approved by the
pre-registrant Wed 11/25, 1:15 pm CT). Descriptive and secondary results only: no verdict is changed and
osf/v62/v62_verdicts.json is not written. No model or API is called; only archived files are read.

Locked modules are imported UNCHANGED (score_v0_62, code_v0_62, params_v0_62, budget_v0_62); this script only calls
their functions. The Entry 4 helper v23_ids() (sens_coi106_en_corrected_v0_62.py) names v0.23's units S01-S24.

Items (pre-registration section numbers; readings where the text is open are recorded in DEVIATIONS Entry 7):
  2.2  per-model rho_c (reading (i): x = model m's English t4 pi_hat, y = model m's pi_hat in L; reading (ii):
       x = the N3 English pi_hat, y = model m's pi_hat in L); point values, as the locked per-category rho_c.
  2.3  |rho_c(phi_L, pi_L)| per language, flagged if >= 0.50 (units with phi_L defined; also on the H_Lang_Phi units).
  2.5  per category x language: rho_c, Delta_L with a 95% bootstrap interval (seed 620131, 10,000 within-category
       resamples, as the locked Delta_L), share of units with |pi_L - pi_EN| > 1/6, the label; rho_c between each pair
       of languages (point value; 95% bootstrap interval and permutation p with the descriptives seed 620141);
       the 10 units with the largest |pi_L - pi_EN| per language.
  2.7  benchmark for time: not available (t5 not scored).
  2.8  MC_Complete, MC_Served, MC_Language, MC_Script, MC_Alias (counts of the exported audit), MC_Truncation,
       MC_Window, MC_Budget (recomputed from the archived files).
  7.5  S-Language, S-Script, S-Alias on H_Lang_Presence (as the locked score() computes S-COI: rank_test with the
       primary seed per language, 10,000 permutations and bootstrap draws, verdict_presence, the 90% drop rule).
  2.9  1 rel1 / rel3 per model x language beside t4 English; 2 recognition (88 yes/no questions) per model x language
       beside t4 English on the same 88 units; 3 answer form (tokens per call and the measured language factor,
       characters per answer, registry brands named per Phase B answer, finish reasons, refusals); 4 script of brand
       mentions in KO and ZH; 5 home-language descriptive: NOT COMPUTED (no country column was built before the
       lock); 6 cost per model x language.

Modes:
  --prepare WORK    write the coded tables that S-Alias and descriptive 4 need: code_v0_62.prepare_raw() on
                    data/v62_raw.jsonl (a) with the collision-prone aliases off (S-Alias) and (b) with no alias at all
                    (Latin-script matches only), then v0.42's coder unchanged (judge off) on KO and ZH, exactly as
                    data/gates/run_v62_score.sh -> data/s_alias_off/{ko,zh}, data/latin_only/{ko,zh}.
  --compute         compute every item -> data/v62_planned_items_v0_62.json (full),
                    data/v62_planned_items_summary_v0_62.json (values for the paper), and three CSV tables.
Both modes refuse to overwrite.
"""
import argparse
import collections
import csv
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import budget_v0_62 as BG  # noqa: E402  (locked; unchanged)
import code_v0_62 as C  # noqa: E402  (locked; unchanged)
import params_v0_62 as P  # noqa: E402  (locked; unchanged)
import score_v0_62 as S  # noqa: E402  (locked; unchanged)

RANK_STATUS = "MARGINAL (v1.14 Stage 1, commit 3129674; not PASS)"   # as in data/gates/run_v62_score.sh
LOCKED_EN_SHA = "792e14addb7ad1ef03a147ee16cee56e82cfecd58030d2e8e3cf3e3ea255af7f"
DATA = S.V62 / "data"
OUT_FULL = DATA / "v62_planned_items_v0_62.json"
OUT_SUMMARY = DATA / "v62_planned_items_summary_v0_62.json"
CSV_CAT = DATA / "v62_planned_category_labels_v0_62.csv"
CSV_TOP = DATA / "v62_planned_top10_shift_v0_62.csv"
CSV_MC = DATA / "v62_planned_checks_v0_62.csv"
ALIAS_OFF_DIR = DATA / "s_alias_off"
LATIN_DIR = DATA / "latin_only"
SUB_RAW = {"v0.19": "v19", "v0.20": "v20", "v0.21": "v21", "v0.22": "v22", "v0.23": "v23"}
RAW_SUB = {v: k for k, v in SUB_RAW.items()}
YN_SUBS = ("v0.19", "v0.20", "v0.21", "v0.22")
EXPECTED = {"B": 90, "A": 88}                       # per model x language (blocks 1-3; block 4)
SHIFT = 1.0 / 6.0
EPS = 1e-12
LABEL_RHO = (0.70, 0.50)
PHI_PI_FLAG = 0.50
LANG_FLAG, SCRIPT_FLAG, TRUNC_FLAG = 0.95, 0.05, 0.05
SEED_DESC, SEED_BOOT = S.SEEDS["descriptives"], S.SEEDS["bootstrap"]
REFUSAL_WORDS = ("refusal", "content_filter", "safety", "prohibited", "blocklist")       # v0.42 N10
SNAPSHOT_RE = re.compile(r"^-(\d{4}-\d{2}-\d{2}|\d{8})$")                               # v0.42 N11


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


# =========================================================================== raw records
def final_records(lines):
    """v0.42 N5: one record per call_id: the last answered attempt (status ok, non-empty text), else the last."""
    out = {}
    for r in lines:
        cid = r["call_id"]
        ok = r.get("status") == "ok" and (r.get("text") or "").strip()
        if cid not in out or ok or not (out[cid].get("status") == "ok" and (out[cid].get("text") or "").strip()):
            out[cid] = r
    return out


def answered(r):
    return r.get("status") == "ok" and bool((r.get("text") or "").strip()) and not r.get("error")


def read_jsonl(path):
    return [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]


# =========================================================================== section 2.2: per-model rho_c
def per_model_rho(units, keys, en, en_B, lang_B):
    """Point values of rho_c (and the uncentred value) per model and language. (i) model m in EN vs model m in L;
    (ii) N3 English pi_hat vs model m in L. pi_hat of one model = score_v0_62.unit_values(..., models=[m])."""
    out = {}
    with np.errstate(invalid="ignore", divide="ignore"):   # phi on one model is undefined (m - 1 = 0); only pi is used
        en_m = {m: S.unit_values(units, en_B, models=[m]) for m in S.MODELS}
        V_m = {(lg, m): S.unit_values(units, lang_B[lg], models=[m]) for lg in S.LANGS for m in S.MODELS}
    for lg in S.LANGS:
        for m in S.MODELS:
            V = V_m[(lg, m)]
            y = {u: V[u]["pi"] for u in V}
            row = {}
            for reading, xd in (("i_same_model_english", {u: en_m[m][u]["pi"] for u in en_m[m]}),
                                ("ii_n3_english", {u: en[u]["pi"] for u in en})):
                k, x, yy, g = S._pairs(xd, y, keys)
                row[reading] = {"n": len(k), "rho_c": S.rho_c(x, yy, g), "rho_uncentred": S.rho_uncentred(x, yy, g)}
            out[f"{lg}|{m}"] = row
    return out


# =========================================================================== section 2.3: phi-pi flag
def phi_pi_flag(units, keys, en, lang_B):
    """|rho_c(phi_L, pi_L)| per language, flagged if >= 0.50. Primary: units with phi_L defined; also on the units
    of the H_Lang_Phi test (phi defined in both English and L)."""
    out = {}
    for lg in S.LANGS:
        V = S.unit_values(units, lang_B[lg])
        ph = {u: V[u]["phi"] for u in V if V[u]["phi"] is not None}
        pi = {u: V[u]["pi"] for u in V}
        row = {}
        both = [u for u in keys if en.get(u, {}).get("phi") is not None]
        for name, ks in (("phi_L_defined", keys), ("h_lang_phi_units", both)):
            k, x, y, g = S._pairs(ph, pi, ks)
            r = S.rho_c(x, y, g)
            row[name] = {"n": len(k), "rho_c": r, "abs_rho_c": abs(r) if np.isfinite(r) else S.NAN,
                         "flag_abs_ge_0.50": bool(np.isfinite(r) and abs(r) >= PHI_PI_FLAG)}
        out[lg] = row
    return out


# =========================================================================== section 2.5
def category_label(rho, ci):
    """Section 2.5 labels (fixed in the pre-registration)."""
    if not np.isfinite(rho) or ci is None or not all(np.isfinite(ci)):
        return "undetermined"
    if rho >= LABEL_RHO[0]:
        return "language-stable" if ci[0] <= 0.0 <= ci[1] else "level-shifted"
    if rho < LABEL_RHO[1]:
        return "language-sensitive"
    return "intermediate"


def moved_share(x, y):
    """Share of units whose pi_hat moves by more than 1/6 (strictly; |d| > 1/6 + 1e-12)."""
    d = np.abs(np.asarray(y, float) - np.asarray(x, float))
    return float(np.mean(d > SHIFT + EPS)) if len(d) else S.NAN, int(np.sum(d > SHIFT + EPS))


def per_category(keys, en, V_by_lang, n_boot=S.N_BOOT):
    out = {}
    xpi = {u: en[u]["pi"] for u in en}
    for lg in S.LANGS:
        ypi = {u: V_by_lang[lg][u]["pi"] for u in V_by_lang[lg]}
        k, x, y, g = S._pairs(xpi, ypi, keys)
        for c in dict.fromkeys(g):
            i = g == c
            xc, yc, gc = x[i], y[i], g[i]
            rho = S.rho_c(xc, yc, gc)
            dl = float(np.mean(yc - xc))
            ci = S.bootstrap_ci(gc, SEED_BOOT, n_boot, lambda j: float(np.mean(yc[j] - xc[j])))
            share, n_moved = moved_share(xc, yc)
            out[f"{lg}|{c}"] = {"language": lg, "category": c, "n": int(i.sum()), "rho_c": rho, "delta_L": dl,
                                "delta_L_ci95": ci, "share_moved_gt_1_6": share, "n_moved_gt_1_6": n_moved,
                                "label": category_label(rho, ci)}
    return out


def language_pairs(keys, V_by_lang, n_perm=S.N_PERM, n_boot=S.N_BOOT):
    out = {}
    for a, b in (("es", "ko"), ("es", "zh"), ("ko", "zh")):
        xa = {u: V_by_lang[a][u]["pi"] for u in V_by_lang[a]}
        xb = {u: V_by_lang[b][u]["pi"] for u in V_by_lang[b]}
        t = S.rank_test(xa, xb, keys, SEED_DESC, n_perm, n_boot)
        out[f"{a.upper()}-{b.upper()}"] = {k: t[k] for k in ("n", "rho_c", "rho_uncentred_comparability", "p_perm",
                                                             "ci95_rho_c", "per_category_rho_c")}
    return out


def top_shifts(keys, en, V_by_lang, names, n_top=10):
    """The 10 units with the largest |pi_L - pi_EN| per language (ties broken by category, then registry name);
    units tied with the 10th are counted."""
    out = {}
    for lg in S.LANGS:
        rows = []
        for u in keys:
            x, y = en[u]["pi"], V_by_lang[lg][u]["pi"]
            if np.isfinite(x) and np.isfinite(y):
                rows.append({"substrate": u[0], "unit": u[1], "name": names.get(u, u[1]), "pi_en": x, "pi_l": y,
                             "shift": y - x, "abs_shift": abs(y - x)})
        rows.sort(key=lambda r: (-round(r["abs_shift"], 10), r["substrate"], r["name"]))
        top = rows[:n_top]
        cut = round(top[-1]["abs_shift"], 10) if top else None
        ties = sum(1 for r in rows[n_top:] if round(r["abs_shift"], 10) == cut)
        out[lg] = {"top": top, "units_tied_with_10th_not_listed": ties}
    return out


# =========================================================================== section 2.8: manipulation checks
def served_ok(requested, served):
    """v0.42 N11: served ID equals the requested ID, or a dated snapshot of it; a leading 'models/' is ignored."""
    if served is None:
        return None
    s = served[7:] if served.startswith("models/") else served
    return s == requested or (s.startswith(requested) and bool(SNAPSHOT_RE.match(s[len(requested):])))


def truncated(finish_reason):
    """v0.42 N11: finish reason (lower-case) contains max_tokens / max_output_tokens, or equals 'length'."""
    f = (finish_reason or "").lower()
    return "max_tokens" in f or "max_output_tokens" in f or f == "length"


def refused(finish_reason):
    f = (finish_reason or "").lower()
    return any(w in f for w in REFUSAL_WORDS)


def _ml(r):
    return f"{r['language']}|{r['model_requested']}"


def manipulation_checks(lines, final, prepared, budget_state, audit_rows, window):
    mc = {}
    # MC_Complete (recomputed; the acquisition-lock commit 37ac08b records it)
    per = {}
    for lg in S.LANGS:
        for m in S.MODELS:
            for ph in ("B", "A"):
                recs = [r for r in final.values() if r["language"] == lg and r["model_requested"] == m and r["phase"] == ph]
                n_ans = sum(answered(r) for r in recs)
                per[f"{lg}|{m}|{ph}"] = {"calls": len(recs), "answered": n_ans, "expected": EXPECTED[ph],
                                         "share_of_expected": n_ans / EXPECTED[ph],
                                         "below_90pct": n_ans / EXPECTED[ph] < S.DROP_SHARE}
    n_sent, n_ans = len(final), sum(answered(r) for r in final.values())
    mc["MC_Complete"] = {"calls_sent": n_sent, "attempt_lines": len(lines), "answered": n_ans,
                         "share": n_ans / n_sent, "pass_ge_98pct": n_ans / n_sent >= 0.98,
                         "per_model_language_phase": per, "below_90pct": [k for k, v in per.items() if v["below_90pct"]]}
    # MC_Served
    mism, no_id = [], []
    for r in final.values():
        ok = served_ok(r["model_requested"], r.get("served_model"))
        if ok is None and answered(r):
            no_id.append(r["call_id"])
        elif ok is False:
            mism.append([r["call_id"], r["model_requested"], r.get("served_model")])
    mc["MC_Served"] = {"answered_calls_checked": n_ans, "n_mismatched": len(mism), "mismatched": mism,
                       "answered_without_served_id": no_id, "pass": not mism and not no_id,
                       "note": "the one failed attempt line (ConnectTimeout, no served ID) is not a final record"}
    # MC_Language and MC_Script (code_v0_62.in_language / zh_traditional, as stored by the locked pre-step)
    lang, script = {}, {}
    for lg in S.LANGS:
        for m in S.MODELS:
            for scope in ("all", "B", "A"):
                recs = [prepared[c] for c, r in final.items() if r["language"] == lg and r["model_requested"] == m
                        and answered(r) and (scope == "all" or r["phase"] == scope)]
                n_in = sum(bool(p["in_language"]) for p in recs)
                share = n_in / len(recs) if recs else S.NAN
                lang[f"{lg}|{m}|{scope}"] = {"answers": len(recs), "in_language": n_in, "share": share,
                                             "flag_below_95pct": bool(recs) and share < LANG_FLAG,
                                             "off_language_call_ids": [p["call_id"] for p in recs if not p["in_language"]]
                                             if scope == "B" else None}
                if lg == "zh":
                    n_tr = sum(bool(p["zh_traditional"]) for p in recs)
                    script[f"zh|{m}|{scope}"] = {"answers": len(recs), "with_traditional_only_characters": n_tr,
                                                 "share": n_tr / len(recs) if recs else S.NAN,
                                                 "flag_above_5pct": bool(recs) and n_tr / len(recs) > SCRIPT_FLAG}
    mc["MC_Language"] = {"rule": "code_v0_62.in_language (section 2.8); flagged below 95% per model x language",
                         "per_model_language": lang,
                         "flagged_all_answers": [k for k, v in lang.items() if k.endswith("|all") and v["flag_below_95pct"]],
                         "flagged_phase_B": [k for k, v in lang.items() if k.endswith("|B") and v["flag_below_95pct"]]}
    mc["MC_Script"] = {"rule": "code_v0_62.zh_traditional (24 characters, ZH_TRAD); flagged above 5% per model",
                       "per_model": script,
                       "flagged_all_answers": [k for k, v in script.items() if k.endswith("|all") and v["flag_above_5pct"]]}
    # MC_Alias: counts of the exported audit (data/coded/v62_alias_audit.csv); the audit itself is a reading
    cnt = collections.Counter((a["call_id"][:2], a["alias"], a["brand"]) for a in audit_rows)
    mc["MC_Alias"] = {"matches_exported": len(audit_rows),
                      "by_language_alias_unit": [{"language": k[0], "alias": k[1], "unit": k[2], "matches": v}
                                                 for k, v in sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))],
                      "calls_with_a_match": len({a["call_id"] for a in audit_rows}),
                      "note": "counts only; the reading of each match (brand or common word) is not done by this script"}
    # MC_Truncation
    tr = {}
    for lg in S.LANGS:
        for m in S.MODELS:
            recs = [r for r in final.values() if r["language"] == lg and r["model_requested"] == m and answered(r)]
            n_cap = sum(truncated(r.get("finish_reason")) for r in recs)
            share = n_cap / len(recs) if recs else S.NAN
            tr[f"{lg}|{m}"] = {"calls": len(recs), "at_cap": n_cap, "share": share,
                               "flag_above_5pct": bool(recs) and share > TRUNC_FLAG}
    mc["MC_Truncation"] = {"rule": "v0.42 N11", "per_model_language": tr,
                           "finish_reasons": dict(collections.Counter(str(r.get("finish_reason")) for r in final.values())),
                           "flagged": [k for k, v in tr.items() if v["flag_above_5pct"]]}
    # MC_Window
    starts = [r["started_utc"] for r in lines if r.get("started_utc")]
    ends = [r["finished_utc"] for r in lines if r.get("finished_utc")]
    t0, t1 = min(starts), max(ends)
    span = (datetime.fromisoformat(t1) - datetime.fromisoformat(t0)).total_seconds() / 3600
    mc["MC_Window"] = {"first_call_started_utc": t0, "last_call_finished_utc": t1, "span_hours": span,
                       "window": window, "pass_within_72h": span <= 72.0}
    # MC_Budget
    costs = [BG.record_cost(r) for r in lines]
    mc["MC_Budget"] = {"spend_from_recorded_usage_usd": sum(costs), "spend_rounded_4dp": round(sum(costs), 4),
                       "cap_usd": 100.0, "pause_usd": 80.0, "pass": sum(costs) <= 100.0,
                       "approvals_recorded": budget_state.get("approvals", {}),
                       "calls_not_sent": len(S.LANGS) * len(S.MODELS) * sum(EXPECTED.values()) - n_sent,
                       "pauses_or_stops": "none in the main pass (collect_v0_62.log); the re-run pass of one call ran "
                                          "under the recorded projection approval (collect_v0_62_rerun.log)"}
    mc["MC_Parity"] = {"recorded_in": "commit 262464d (data/gates/gate_P1real_P3_v0_62.json, gate_P2_v0_62.json)",
                       "computed_here": False}
    return mc


# =========================================================================== section 7.5: S-Language, S-Script, S-Alias
def presence_on(units, keys, en, B, lg, n_perm=S.N_PERM, n_boot=S.N_BOOT):
    """H_Lang_Presence in language lg on coded rows B, exactly as score_v0_62.score() computes S-COI (rank_test with
    the primary seed, verdict_presence, the 90% drop rule on the rows given)."""
    V = S.unit_values(units, B)
    drop = S.dropped_models(B, 30)
    xpi, ypi = {u: en[u]["pi"] for u in en}, {u: V[u]["pi"] for u in V}
    t = S.rank_test(xpi, ypi, keys, S.SEEDS[("H_Lang_Presence", lg)], n_perm, n_boot)
    t["verdict"] = "UNDETERMINED" if drop else S.verdict_presence(t["rho_c"], t["p_perm"])
    if drop:
        t["reason"] = f"models below 90% of Phase B calls in {lg}: {drop}"
    return t


def exclude_calls(B, call_ids):
    ids = set(call_ids)
    return [r for r in B if r["call_id"] not in ids]


def no_collision_aliaser():
    """S-Alias: the alias table without its collision-prone rows (= Aliaser.canonicalise(collision=False))."""
    rows = C.load_aliases()
    keep = [r for r in rows if not r[4]]
    return C.Aliaser(keep), len(rows) - len(keep)


# =========================================================================== section 2.9 descriptives
def rel1(B, units, model, rho=S.rho_c):
    """v0.42 rel1_of (score_v0_42.py, N8), transcribed: mean centred pooled-within rho over the three run pairs of the
    per-run rates k/n of one model (pairs with >= 3 units having both rates)."""
    k, ans = S.aggregate(B)
    K = np.array([[k[(model, r, s, b)] for (s, b) in units] for r in S.RUNS], float)
    N = np.array([[len(ans[(model, r, s)]) for (s, b) in units] for r in S.RUNS], float)
    g = np.array([u[0] for u in units])
    with np.errstate(invalid="ignore", divide="ignore"):
        rates = np.where(N > 0, K / np.where(N > 0, N, 1), np.nan)
    vals = []
    for a, b in ((0, 1), (0, 2), (1, 2)):
        m = np.isfinite(rates[a]) & np.isfinite(rates[b])
        if m.sum() >= 3:
            vals.append(rho(rates[a][m], rates[b][m], g[m]))
    vals = [v for v in vals if np.isfinite(v)]
    return float(np.mean(vals)) if vals else S.NAN


def rel3(r):
    """v0.42 rel3_of: Spearman-Brown for three runs."""
    return 3 * r / (1 + 2 * r) if np.isfinite(r) else S.NAN


def recognition(A_rows, models=S.MODELS, subs=YN_SUBS):
    out = {}
    for m in models:
        v = [r for r in A_rows if r["model"] == m and r.get("condition", "S0") == "S0" and r["substrate"] in subs]
        rec = sum(int(r["recognized"]) for r in v if r["recognized"] not in ("", None))
        coded = sum(1 for r in v if r["recognized"] not in ("", None))
        out[m] = {"recognized": rec, "coded_answers": coded, "rows": len(v),
                  "labels": dict(collections.Counter(r["label"] for r in v)),
                  "share": rec / coded if coded else S.NAN}
    return out


def read_coded_a(coded_dir):
    rows = []
    for raw in ("v19", "v20", "v21", "v22", "v23"):
        p = Path(coded_dir) / f"{raw}_phase_a.csv"
        if p.exists():
            rows += list(csv.DictReader(open(p, encoding="utf-8")))
    return rows


def _mean(xs):
    xs = [x for x in xs if x is not None]
    return float(np.mean(xs)) if xs else None


def form_block(recs, B_rows=None):
    """Answer form of a set of answered final records (one model x language-or-English x phase)."""
    d = {"calls": len(recs),
         "input_tokens_mean": _mean([r.get("input_tokens") for r in recs]),
         "output_tokens_mean": _mean([r.get("output_tokens") for r in recs]),
         "thinking_tokens_mean": _mean([r.get("thinking_tokens") for r in recs]),
         "thinking_tokens_reported": sum(r.get("thinking_tokens") is not None for r in recs),
         "characters_per_answer_mean": _mean([len(r.get("text") or "") for r in recs]),
         "cost_per_call_usd_mean": _mean([BG.record_cost(r) for r in recs]),
         "finish_reasons": dict(collections.Counter(str(r.get("finish_reason")) for r in recs)),
         "refusals_by_finish_reason": sum(refused(r.get("finish_reason")) for r in recs)}
    if B_rows is not None:
        ids = {r["call_id"] for r in recs}
        per = collections.Counter()
        for r in B_rows:
            if r["call_id"] in ids:
                per[r["call_id"]] += int(r["mentioned"])
        d["registry_brands_named_per_phase_B_answer"] = float(np.mean([per[c] for c in ids])) if ids else None
    return d


def answer_form(final_l, lang_B, final_en, en_B):
    """Section 2.9 item 3 (per model x language x phase, beside t4 English S0 on the same question types) and the
    measured language factor: mean cost per answered call in L / the same in English (per model x question type;
    pooled = sum over models of the means in L / the same in English)."""
    out, fac = {}, {}
    en_ids_b = {r["call_id"] for r in en_B if r.get("condition") == "S0"}
    for m in S.MODELS:
        for ph in ("B", "A"):
            en_recs = [r for r in final_en.values() if r["model_requested"] == m and r["phase"] == ph and answered(r)
                       and r.get("condition") == "S0" and (ph == "B" or RAW_SUB.get(r["substrate"]) in YN_SUBS)]
            out[f"en|{m}|{ph}"] = form_block(en_recs, [r for r in en_B if r["call_id"] in en_ids_b] if ph == "B" else None)
            for lg in S.LANGS:
                recs = [r for r in final_l.values() if r["language"] == lg and r["model_requested"] == m
                        and r["phase"] == ph and answered(r)]
                out[f"{lg}|{m}|{ph}"] = form_block(recs, lang_B[lg] if ph == "B" else None)
    for lg in S.LANGS:
        for ph in ("B", "A"):
            num = den = 0.0
            for m in S.MODELS:
                a, e = out[f"{lg}|{m}|{ph}"], out[f"en|{m}|{ph}"]
                f = {"cost_factor": a["cost_per_call_usd_mean"] / e["cost_per_call_usd_mean"],
                     "output_tokens_factor": a["output_tokens_mean"] / e["output_tokens_mean"],
                     "input_tokens_factor": a["input_tokens_mean"] / e["input_tokens_mean"]}
                fac[f"{lg}|{m}|{ph}"] = f
                num += a["cost_per_call_usd_mean"]
                den += e["cost_per_call_usd_mean"]
            fac[f"{lg}|pooled|{ph}"] = {"cost_factor": num / den}
    return out, fac


def cost_per_model_language(lines):
    out = {}
    for lg in S.LANGS:
        for m in S.MODELS:
            recs = [r for r in lines if r["language"] == lg and r["model_requested"] == m]
            parts = [p for r in recs for p in (r.get("usage_parts") or [])]
            out[f"{lg}|{m}"] = {"records": len(recs), "billed_parts": len(parts),
                                "worst_case_parts": sum(bool(p.get("worst_case")) for p in parts),
                                "input_tokens": sum(p.get("input_tokens") or 0 for p in parts),
                                "output_tokens": sum(p.get("output_tokens") or 0 for p in parts),
                                "thinking_tokens": sum(p.get("thinking_tokens") or 0 for p in parts),
                                "usd": sum(BG.record_cost(r) for r in recs)}
    out["total_usd"] = sum(v["usd"] for v in out.values())
    return out


def alias_regexes(lg, v23_name_to_id):
    """{(substrate 'v0.xx', unit key): [compiled alias regexes of language lg]} from the locked alias table."""
    out = collections.defaultdict(list)
    for sub, brand, alias, kind, _cp in C.load_aliases():
        if kind != lg:
            continue
        s = RAW_SUB.get(sub, sub)
        key = v23_name_to_id.get(brand, brand) if s == "v0.23" else brand
        out[(s, key)].append(C.alias_regex(alias, kind))
    return out


def mention_scripts(primary_rows, latin_rows, texts, rx):
    """Section 2.9 item 4, per mentioned cell (answer x unit coded 1 in the primary coding): 'latin_only' (the unit
    is also coded with every alias switched off and no alias of the unit occurs in the answer), 'native_only' (not
    coded without aliases: the mention is a Hangul / Han alias), 'both' (coded without aliases and an alias of the
    unit also occurs). texts: {call_id: answer after normalise() and strip_urls()}."""
    lat = {(r["call_id"], r["substrate"], r["brand"]): int(r["mentioned"]) for r in latin_rows}
    res = collections.defaultdict(collections.Counter)
    for r in primary_rows:
        key = (r["call_id"], r["substrate"], r["brand"])
        l_on = lat.get(key, 0) == 1
        if not int(r["mentioned"]):
            if l_on:
                res[r["model"]]["latin_coded_but_not_primary"] += 1
            continue
        native = any(x.search(texts.get(r["call_id"], "")) for x in rx.get((r["substrate"], r["brand"]), []))
        cls = "both" if (l_on and native) else ("latin_only" if l_on else "native_only")
        res[r["model"]][cls] += 1
    out = {}
    tot = collections.Counter()
    for m in S.MODELS:
        c = res[m]
        tot.update(c)
        out[m] = _script_shares(c)
    out["all_models"] = _script_shares(tot)
    return out


def _script_shares(c):
    n = c["latin_only"] + c["native_only"] + c["both"]
    return {"mentions": n, "latin_only": c["latin_only"], "native_only": c["native_only"], "both": c["both"],
            "share_latin_only": c["latin_only"] / n if n else None,
            "share_native_only": c["native_only"] / n if n else None,
            "share_both": c["both"] / n if n else None,
            "share_with_latin_form": (c["latin_only"] + c["both"]) / n if n else None,
            "share_with_native_form": (c["native_only"] + c["both"]) / n if n else None,
            "latin_coded_but_not_primary": c["latin_coded_but_not_primary"]}


# =========================================================================== --prepare
def prepare(work, v42):
    work = Path(work)
    for d in (ALIAS_OFF_DIR, LATIN_DIR):
        for lg in ("ko", "zh"):
            if (d / lg).exists():
                raise SystemExit(f"REFUSED: {d / lg} exists (new files only)")
    al_off, n_off = no_collision_aliaser()
    variants = (("s_alias_off", al_off, ALIAS_OFF_DIR), ("latin_only", C.Aliaser([]), LATIN_DIR))
    print(f"S-Alias: {n_off} collision-prone alias rows switched off")
    for name, aliaser, out in variants:
        n, h = C.prepare_raw(C.REAL_RAW, work / name, aliaser=aliaser)
        print(f"{name}: prepared {n}; {h} collision-prone alias matches")
        for lg in ("ko", "zh"):
            r = subprocess.run([sys.executable, str(Path(v42) / "scripts/code_t4_v0_42.py"), "--raw",
                                str(work / name / f"v62_prepared_{lg}.jsonl"), "--out", str(out / lg)])
            if r.returncode != 0:
                raise SystemExit(f"coder failed on {name} {lg}")
    return 0


# =========================================================================== --compute
def compute(v42, n_perm=S.N_PERM, n_boot=S.N_BOOT, reproduce=True):
    from sens_coi106_en_corrected_v0_62 import v23_ids        # Entry 4 helper (v0.23 registry ids)
    for p in (OUT_FULL, OUT_SUMMARY, CSV_CAT, CSV_TOP, CSV_MC):
        if p.exists():
            raise SystemExit(f"REFUSED: {p} exists (new files only)")
    v42 = Path(v42)
    en_p = v42 / "v42_brand_table.csv"
    if sha256(en_p) != LOCKED_EN_SHA:
        raise SystemExit("v42_brand_table.csv does not have the locked SHA-256")
    en = S.read_english(en_p)
    units = sorted(en)
    option = P.HEADPHONES_OPTION
    keys = S.unit_set(units, option)
    lang_B = {lg: S.read_coded_b(DATA / "coded" / lg) for lg in S.LANGS}
    en_B = S.read_coded_b(v42 / "data/coded")
    ids = v23_ids()
    names = {("v0.23", i): b for b, i in ids.items()}
    locked = json.loads(S.VERDICTS.read_text(encoding="utf-8"))

    repro = None
    if reproduce:   # step 0, as Entry 4: the locked scoring reproduces byte for byte
        v_l = S.score(units, en, lang_B, rank_status=RANK_STATUS)
        repro = json.dumps(S._clean(v_l), indent=1, ensure_ascii=False) == S.VERDICTS.read_text(encoding="utf-8")
        print("reproduces v62_verdicts.json byte for byte:", repro, flush=True)
        if not repro:
            raise SystemExit("STOP: the locked scoring does not reproduce; nothing written")

    lines = read_jsonl(C.REAL_RAW)
    final = final_records(lines)
    prepared = {}
    for lg in S.LANGS:
        prepared.update(final_records(read_jsonl(DATA / "coded" / f"v62_prepared_{lg}.jsonl")))
    audit = list(csv.DictReader(open(DATA / "coded/v62_alias_audit.csv", encoding="utf-8")))
    budget_state = json.loads((DATA / "v62_budget_state.json").read_text(encoding="utf-8"))
    V = {lg: S.unit_values(units, lang_B[lg]) for lg in S.LANGS}
    res = {"phase": "v0.62", "deviation_entry": 7, "no_model_called": True, "locked_verdicts_stand": True,
           "headphones_option": option, "n_units": len(keys), "rank_status": RANK_STATUS,
           "reproduced_locked_verdicts_byte_for_byte": repro}

    # 2.2 per-model rho_c
    res["2.2_per_model_rho_c"] = per_model_rho(units, keys, en, en_B, lang_B)
    print("2.2 done", flush=True)
    # 2.3 phi-pi flag
    res["2.3_phi_pi_flag"] = phi_pi_flag(units, keys, en, lang_B)
    # 2.5
    cat = per_category(keys, en, V, n_boot)
    for lg in S.LANGS:   # the locked per-category rho_c must be reproduced
        for c, r in locked["tests"][f"H_Lang_Presence_{lg}"]["per_category_rho_c"].items():
            if abs(cat[f"{lg}|{c}"]["rho_c"] - r) > 1e-12:
                raise SystemExit(f"per-category rho_c differs from the locked value: {lg} {c}")
    res["2.5_per_category"] = cat
    res["2.5_language_pairs"] = language_pairs(keys, V, n_perm, n_boot)
    res["2.5_top10_shift"] = top_shifts(keys, en, V, names)
    print("2.5 done", flush=True)
    res["2.7_benchmark_for_time"] = {"status": "not available",
                                     "reason": "t5 (English, target 2026-12-03) has not been scored before v0.62"}

    # 2.8 manipulation checks
    window = budget_state.get("window")
    mc = manipulation_checks(lines, final, prepared, budget_state, audit, window)
    res["2.8_manipulation_checks"] = mc

    # 7.5 sensitivities on H_Lang_Presence
    sens = {}
    off_lang = {lg: [c for c, p in prepared.items() if p["language"] == lg and p["phase"] == "B"
                     and answered(final[c]) and not p["in_language"]] for lg in S.LANGS}
    trad = [c for c, p in prepared.items() if p["language"] == "zh" and p["phase"] == "B" and answered(final[c])
            and p["zh_traditional"]]
    for lg in S.LANGS:
        s = presence_on(units, keys, en, exclude_calls(lang_B[lg], off_lang[lg]), lg, n_perm, n_boot)
        s["excluded_calls"] = off_lang[lg]
        sens[f"S-Language_{lg}"] = s
    s = presence_on(units, keys, en, exclude_calls(lang_B["zh"], trad), "zh", n_perm, n_boot)
    s["excluded_calls"] = trad
    sens["S-Script_zh"] = s
    _al, n_off = no_collision_aliaser()
    for lg in S.LANGS:
        B = lang_B[lg] if lg == "es" else S.read_coded_b(ALIAS_OFF_DIR / lg)
        s = presence_on(units, keys, en, B, lg, n_perm, n_boot)
        s["note"] = ("no ES alias exists (section 4.2): the primary ES coded tables" if lg == "es" else
                     f"coded tables data/s_alias_off/{lg} ({n_off} collision-prone alias rows off)")
        if lg != "es":
            prim = {(r["call_id"], r["brand"]): r["mentioned"] for r in lang_B[lg]}
            s["cells_differing_from_primary"] = sum(1 for r in B if prim.get((r["call_id"], r["brand"])) != r["mentioned"])
        sens[f"S-Alias_{lg}"] = s
    for k, s in sens.items():
        lg = k.rsplit("_", 1)[1]
        s["primary_verdict"] = locked["tests"][f"H_Lang_Presence_{lg}"]["verdict"]
        s["verdict_differs_from_primary"] = s["verdict"] != s["primary_verdict"]
    res["7.5_sensitivities"] = sens
    print("7.5 done", flush=True)

    # 2.9 descriptives
    v42v = json.loads((v42 / "v42_verdicts.json").read_text(encoding="utf-8"))
    d = {}
    rel = {}
    for m in S.MODELS:
        e1 = rel1(en_B, units, m)
        e_locked = v42v["descriptives"]["1_run_reliability"][f"{m}|S0"]["rel1"]
        rel[f"en|{m}"] = {"rel1": e1, "rel3": rel3(e1), "rel1_t4_locked": e_locked,
                          "transcription_equals_t4_locked": abs(e1 - e_locked) < 1e-12}
        for lg in S.LANGS:
            r1 = rel1(lang_B[lg], units, m)
            rel[f"{lg}|{m}"] = {"rel1": r1, "rel3": rel3(r1), "rel1_uncentred": rel1(lang_B[lg], units, m, S.rho_uncentred)}
    d["1_run_reliability"] = rel
    A_en = read_coded_a(v42 / "data/coded")
    recog = {"en_t4_same_88_units": recognition(A_en)}
    for lg in S.LANGS:
        recog[lg] = recognition(read_coded_a(DATA / "coded" / lg))
    recog["en_t4_locked_112_units"] = v42v["descriptives"]["2_recognition"]["t4"]
    d["2_recognition"] = recog
    final_en = final_records(read_jsonl(v42 / "data/t4_raw.jsonl"))
    form, fac = answer_form(final, lang_B, final_en, en_B)
    d["3_answer_form"] = form
    d["3_measured_language_factor"] = fac
    d["3_planning_language_factors_section_6_2"] = {"central": {"es": 1.25, "ko": 1.75, "zh": 1.50},
                                                    "conservative_high": {"es": 1.50, "ko": 2.50, "zh": 2.25}}
    scripts_ = {}
    for lg in ("ko", "zh"):
        texts = {c: C.strip_urls(C.normalise(p.get("text_original") or "")) for c, p in prepared.items()
                 if p["language"] == lg and p["phase"] == "B"}
        scripts_[lg] = mention_scripts(lang_B[lg], S.read_coded_b(LATIN_DIR / lg), texts, alias_regexes(lg, ids))
    d["4_script_of_mentions"] = scripts_
    d["5_home_language"] = {"status": "not computed",
                            "reason": "the country column (section 2.9 item 5) was to be built from cited sources before "
                                      "the lock; no such column was built (it is not among the 73 files of "
                                      "prereg/LOCK_MANIFEST_v0_62.sha256 and no v0.62 file holds it); building it after "
                                      "scoring would not meet the pre-registered condition"}
    d["6_cost"] = cost_per_model_language(lines)
    res["2.9_descriptives"] = d
    res["inputs_sha256"] = {"v62_verdicts.json": sha256(S.VERDICTS), "v62_raw.jsonl": sha256(C.REAL_RAW),
                            "v42_brand_table.csv": sha256(en_p), "v42_verdicts.json": sha256(v42 / "v42_verdicts.json"),
                            "t4_raw.jsonl": sha256(v42 / "data/t4_raw.jsonl"),
                            "score_v0_62.py": sha256(S.__file__), "code_v0_62.py": sha256(C.__file__),
                            "params_v0_62.py": sha256(P.__file__), "budget_v0_62.py": sha256(BG.__file__)}
    return res, names


def summarise(res):
    """Compact values for the paper (rounded only in presentation by the reader; full precision kept)."""
    sm = {"deviation_entry": 7, "no_model_called": True, "locked_verdicts_stand": True,
          "verdicts_unchanged": {"H_Lang_Presence": "CONFIRMED ES, KO, ZH", "H_Lang_Phi": "ES CONFIRMED, KO/ZH MARGINAL",
                                 "H_Lang_Rank": "NOT TESTED"}}
    sm["per_model_rho_c"] = {k: {r: v[r]["rho_c"] for r in v} for k, v in res["2.2_per_model_rho_c"].items()}
    sm["phi_pi_flag"] = {lg: {k: {"rho_c": v["rho_c"], "flag": v["flag_abs_ge_0.50"], "n": v["n"]} for k, v in row.items()}
                         for lg, row in res["2.3_phi_pi_flag"].items()}
    sm["category_labels"] = {k: {x: v[x] for x in ("n", "rho_c", "delta_L", "delta_L_ci95", "share_moved_gt_1_6",
                                                   "n_moved_gt_1_6", "label")} for k, v in res["2.5_per_category"].items()}
    sm["language_pairs"] = {k: {x: v[x] for x in ("n", "rho_c", "ci95_rho_c", "p_perm")}
                            for k, v in res["2.5_language_pairs"].items()}
    sm["top10_shift"] = {lg: [[r["substrate"], r["name"], r["pi_en"], r["pi_l"], r["shift"]] for r in v["top"]]
                         for lg, v in res["2.5_top10_shift"].items()}
    mc = res["2.8_manipulation_checks"]
    sm["checks"] = {
        "MC_Complete": {k: mc["MC_Complete"][k] for k in ("calls_sent", "answered", "share", "pass_ge_98pct", "below_90pct")},
        "MC_Served": {k: mc["MC_Served"][k] for k in ("answered_calls_checked", "n_mismatched", "pass")},
        "MC_Language": {"share_all_answers": {k[:-4]: v["share"] for k, v in mc["MC_Language"]["per_model_language"].items() if k.endswith("|all")},
                        "share_phase_B": {k[:-2]: v["share"] for k, v in mc["MC_Language"]["per_model_language"].items() if k.endswith("|B")},
                        "share_phase_A": {k[:-2]: v["share"] for k, v in mc["MC_Language"]["per_model_language"].items() if k.endswith("|A")},
                        "flagged_all_answers": mc["MC_Language"]["flagged_all_answers"],
                        "flagged_phase_B": mc["MC_Language"]["flagged_phase_B"]},
        "MC_Script": {"share_all_answers": {k[:-4]: v["share"] for k, v in mc["MC_Script"]["per_model"].items() if k.endswith("|all")},
                      "flagged": mc["MC_Script"]["flagged_all_answers"]},
        "MC_Alias": {"matches_exported": mc["MC_Alias"]["matches_exported"],
                     "by_alias": [[r["language"], r["alias"], r["unit"], r["matches"]] for r in mc["MC_Alias"]["by_language_alias_unit"]]},
        "MC_Truncation": {"at_cap_total": sum(v["at_cap"] for v in mc["MC_Truncation"]["per_model_language"].values()),
                          "flagged": mc["MC_Truncation"]["flagged"]},
        "MC_Window": {k: mc["MC_Window"][k] for k in ("first_call_started_utc", "last_call_finished_utc", "span_hours", "pass_within_72h")},
        "MC_Budget": {k: mc["MC_Budget"][k] for k in ("spend_from_recorded_usage_usd", "spend_rounded_4dp", "calls_not_sent", "pass")}}
    sm["sensitivities"] = {k: {x: v.get(x) for x in ("n", "rho_c", "ci95_rho_c", "p_perm", "verdict", "primary_verdict",
                                                    "verdict_differs_from_primary")} | {"n_excluded_calls": len(v.get("excluded_calls", []))}
                           for k, v in res["7.5_sensitivities"].items()}
    d = res["2.9_descriptives"]
    sm["rel1_rel3"] = {k: {"rel1": v["rel1"], "rel3": v["rel3"]} for k, v in d["1_run_reliability"].items()}
    sm["recognition"] = {g: {m: {"recognized": v["recognized"], "coded": v["coded_answers"], "share": v["share"]}
                             for m, v in d["2_recognition"][g].items()} for g in ("en_t4_same_88_units", "es", "ko", "zh")}
    sm["language_factor"] = d["3_measured_language_factor"]
    sm["answer_form"] = {k: {x: v.get(x) for x in ("calls", "input_tokens_mean", "output_tokens_mean", "thinking_tokens_mean",
                                                  "characters_per_answer_mean", "registry_brands_named_per_phase_B_answer",
                                                  "refusals_by_finish_reason")} for k, v in d["3_answer_form"].items()}
    sm["script_of_mentions"] = {lg: v["all_models"] for lg, v in d["4_script_of_mentions"].items()}
    sm["home_language"] = d["5_home_language"]
    sm["cost"] = {k: (v if not isinstance(v, dict) else {x: v[x] for x in ("records", "input_tokens", "output_tokens", "thinking_tokens", "usd")})
                  for k, v in d["6_cost"].items()}
    sm["benchmark_for_time"] = res["2.7_benchmark_for_time"]
    sm["bears_on_a_verdict"] = any(v["verdict_differs_from_primary"] for v in res["7.5_sensitivities"].values())
    return sm


def write_outputs(res, sm):
    def dump(p, obj):
        if p.exists():
            raise SystemExit(f"REFUSED: {p} exists (new files only)")
        p.write_text(json.dumps(S._clean(obj), indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {p} sha256 {sha256(p)}")
    dump(OUT_FULL, res)
    dump(OUT_SUMMARY, sm)
    with open(CSV_CAT, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["language", "category", "n", "rho_c", "delta_L", "delta_L_ci95_lo", "delta_L_ci95_hi",
                    "share_moved_gt_1_6", "n_moved_gt_1_6", "label"])
        for v in res["2.5_per_category"].values():
            w.writerow([v["language"], v["category"], v["n"], f"{v['rho_c']:.10f}", f"{v['delta_L']:.10f}",
                        f"{v['delta_L_ci95'][0]:.10f}", f"{v['delta_L_ci95'][1]:.10f}", f"{v['share_moved_gt_1_6']:.10f}",
                        v["n_moved_gt_1_6"], v["label"]])
    with open(CSV_TOP, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["language", "rank", "substrate", "unit", "name", "pi_en", "pi_l", "shift"])
        for lg, v in res["2.5_top10_shift"].items():
            for i, r in enumerate(v["top"], 1):
                w.writerow([lg, i, r["substrate"], r["unit"], r["name"], f"{r['pi_en']:.10f}", f"{r['pi_l']:.10f}",
                            f"{r['shift']:.10f}"])
    mc = res["2.8_manipulation_checks"]
    with open(CSV_MC, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["check", "cell", "n", "count", "share", "flag"])
        for k, v in mc["MC_Language"]["per_model_language"].items():
            w.writerow(["MC_Language", k, v["answers"], v["in_language"], f"{v['share']:.10f}", v["flag_below_95pct"]])
        for k, v in mc["MC_Script"]["per_model"].items():
            w.writerow(["MC_Script", k, v["answers"], v["with_traditional_only_characters"], f"{v['share']:.10f}", v["flag_above_5pct"]])
        for k, v in mc["MC_Truncation"]["per_model_language"].items():
            w.writerow(["MC_Truncation", k, v["calls"], v["at_cap"], f"{v['share']:.10f}", v["flag_above_5pct"]])
        for k, v in mc["MC_Complete"]["per_model_language_phase"].items():
            w.writerow(["MC_Complete", k, v["expected"], v["answered"], f"{v['share_of_expected']:.10f}", v["below_90pct"]])
    for p in (CSV_CAT, CSV_TOP, CSV_MC):
        print(f"wrote {p} sha256 {sha256(p)}")


def main(argv=None):
    ap = argparse.ArgumentParser(description="v0.62 pre-registered items not computed by the locked scorer (Entry 7)")
    ap.add_argument("--v42", required=True, help="v0.42's osf/v42 folder")
    ap.add_argument("--prepare", metavar="WORK", help="write the S-Alias and Latin-only coded tables")
    ap.add_argument("--compute", action="store_true")
    a = ap.parse_args(argv)
    if a.prepare:
        return prepare(a.prepare, a.v42)
    if a.compute:
        res, _names = compute(a.v42)
        write_outputs(res, summarise(res))
        return 0
    ap.error("--prepare WORK or --compute")


if __name__ == "__main__":
    sys.exit(main())
