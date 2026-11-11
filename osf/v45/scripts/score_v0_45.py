#!/usr/bin/env python3
"""
score_v0_45.py -- AIAS(TM) v0.45: t4 -> t5 short-term stability (pre-registration r1, section 2 and section 5;
section 2 as fixed in r0, unchanged in r1).

Reuses v0.42's scorer functions unchanged (osf/v42/scripts/score_v0_42.py: Data, pi_hat, phi_panel, rho_pw on CENTRED
within-substrate ranks, perm_p_within, bootstrap, presence_test, rel1_of, manipulation_checks, served_ok), so t4 and
t5 are measured by the same code. Both waves are coded by v0.42's coder (code_t5_v0_45.py checks its blob).

Tests (section 2):
  H_Stab_Presence        PRIMARY    rho_pw(pi_t4, pi_t5), N3 S0, 112 brands; perm p (seed 450041), bootstrap.
                                    CONFIRMED rho >= 0.70 and p < 0.05; FALSIFIED rho < 0.50; PARTIAL otherwise.
  H_Stab_Consistency     SECONDARY  rho_pw(phi_t4, phi_t5), N3 S0, phi defined at both waves; seed 450043.
                                    UNDETERMINED n < 40; CONFIRMED rho >= 0.50 and p < 0.05; FALSIFIED rho < 0.30.
  H_Stab_Drift           SECONDARY  per model, within-wave vs cross-wave run-pair rho_pw of k/n (S0); exact
                                    permutation over the 20 x 20 x 20 ways to split each model's six runs 3 + 3.
                                    CONFIRMED (no drift beyond run-to-run noise) p_exact >= 0.05 and SR >= 0.90;
                                    FALSIFIED p_exact < 0.05 and SR < 0.75; PARTIAL otherwise; UNDETERMINED if the
                                    mean within-wave rho < 0.30, a run pair is incomputable, or < 2 common models.
  H_Stab_Search_Presence SECONDARY  as H_Stab_Presence on S1 (seed 450044).
  Component legs                    Ranking: v1.14 Stage 2's H3 verdict, carried (not re-tested). Grounding,
                                    Coverage, Sentiment: the component's locked score at both waves (CSV), if it
                                    exists; ACTIVE iff that component's gate is PASS or MARGINAL; rho_pw, perm p
                                    (seed 450046), CONFIRMED rho >= 0.50 and p < 0.05, FALSIFIED rho < 0.30,
                                    PARTIAL otherwise, UNDETERMINED n < 30; else NOT MEASURED / descriptive.
Modes: --synthetic T4DIR T5DIR (each holds t?_raw.jsonl and coded/; output T5DIR/_score) | --run (refuses unless
tags v0.45-prereg-r1 and v0.45-acquisition-locked are on origin)
"""
import argparse
import collections
import csv
import hashlib
import itertools
import json
import statistics
import subprocess
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import code_t5_v0_45 as K   # noqa: E402  (imports v0.42's coder and bootstraps ROOT)

C = K.C
ROOT = K.ROOT
import numpy as np            # noqa: E402
import score_v0_42 as S       # noqa: E402  (v0.42 scorer, unchanged)
import budget_v0_45 as BG     # noqa: E402

PHASE_ID = "v0.45"
PREREG_TAG = "v0.45-prereg-r1"
ACQ_TAG = "v0.45-acquisition-locked"
MODELS = list(S.MODELS)
SEEDS = {"H_Stab_Presence": 450041, "H_Stab_Consistency": 450043, "H_Stab_Search_Presence": 450044,
         "descriptives": 450045, "components": 450046}
STAB_CONF, STAB_FALS, ALPHA = 0.70, 0.50, 0.05
PHI_CONF, PHI_FALS, PHI_N = 0.50, 0.30, 40
SR_CONF, SR_FALS, NOISE_FLOOR = 0.90, 0.75, 0.30
COMP_CONF, COMP_FALS, COMP_N = 0.50, 0.30, 30
GAP_DAYS = (14, 35)
NAN = float("nan")
SPLITS = list(itertools.combinations(range(6), 3))   # the 20 ways to call three of a model's six runs "wave A"


class Halt(RuntimeError):
    pass


# =========================================================================== waves
class Wave:
    def __init__(self, raw, A, B, brands, name):
        self.name, self.raw = name, raw
        self.calls = C.dedupe_calls(raw)
        self.mcs, self.served_excl = S.manipulation_checks(self.calls)
        self.excl = S.excluded_set(self.mcs["MC_Complete"])
        self.D = S.Data(brands, A, B, excluded=self.served_excl)
        self.A = [r for r in A if r["call_id"] not in self.served_excl]
        self.B = [r for r in B if r["call_id"] not in self.served_excl]


def brands_list():
    return list(S.load_t3_table())     # the 112 units, in the locked order of v0.41's table


def common_models(w4, w5, cond):
    return [m for m in MODELS if (m, cond) not in w4.excl and (m, cond) not in w5.excl]


# =========================================================================== verdict rules
def verdict_stab(rho, p):
    if not np.isfinite(rho) or p is None or not np.isfinite(p):
        return "UNDETERMINED"
    if rho >= STAB_CONF and p < ALPHA:
        return "CONFIRMED"
    if rho < STAB_FALS:
        return "FALSIFIED"
    return "PARTIAL"


def verdict_phi(n, rho, p):
    if n < PHI_N or not np.isfinite(rho) or p is None or not np.isfinite(p):
        return "UNDETERMINED"
    if rho >= PHI_CONF and p < ALPHA:
        return "CONFIRMED"
    if rho < PHI_FALS:
        return "FALSIFIED"
    return "PARTIAL"


def verdict_drift(p, sr, within):
    if not (np.isfinite(p) and np.isfinite(sr) and np.isfinite(within)) or within < NOISE_FLOOR:
        return "UNDETERMINED"
    if p >= ALPHA and sr >= SR_CONF:
        return "CONFIRMED"
    if p < ALPHA and sr < SR_FALS:
        return "FALSIFIED"
    return "PARTIAL"


def verdict_component(n, rho, p):
    if n < COMP_N or not np.isfinite(rho) or p is None or not np.isfinite(p):
        return "UNDETERMINED"
    if rho >= COMP_CONF and p < ALPHA:
        return "CONFIRMED"
    if rho < COMP_FALS:
        return "FALSIFIED"
    return "PARTIAL"


# =========================================================================== hypotheses
def h_stab_presence(w4, w5, cfg, cond="S0", name="H_Stab_Presence", tier="PRIMARY"):
    seed = SEEDS[name]
    models = common_models(w4, w5, cond)
    out = {"tier": tier, "condition": cond, "seed": seed, "models": models}
    if len(models) < 2:
        return {**out, "verdict": "UNDETERMINED", "reason": "fewer than 2 N3 models retained at both waves (section 5.4)"}
    out["panel"] = "N3" if len(models) == 3 else "reduced panel"
    x, y = S.pi_hat(w4.D, models, cond), S.pi_hat(w5.D, models, cond)
    res = S.presence_test(x, y, seed, cfg)
    out.update(res)
    out["verdict"] = verdict_stab(res.get("rho", NAN), res.get("p_perm"))
    per_model = {}
    for m in models:
        keys, a, b, g = S.pair_arrays(S.pi_hat(w4.D, [m], cond), S.pi_hat(w5.D, [m], cond))
        per_model[m] = {"rho": S.rho_pw(a, b, g), "n": len(keys)}
    out["per_model"] = per_model
    return out


def h_stab_consistency(w4, w5, cfg):
    seed = SEEDS["H_Stab_Consistency"]
    models = common_models(w4, w5, "S0")
    out = {"tier": "SECONDARY", "condition": "S0", "seed": seed}
    if len(models) < 3:
        return {**out, "verdict": "UNDETERMINED", "reason": "phi needs all three N3 models at both waves (section 5.4)"}
    p4, p5 = S.phi_panel(w4.D, models, "S0"), S.phi_panel(w5.D, models, "S0")
    x = {k: v[0] for k, v in p4.items() if v[1] == "defined"}
    y = {k: v[0] for k, v in p5.items() if v[1] == "defined"}
    res = S.presence_test(x, y, seed, cfg)
    out.update(res)
    out["verdict"] = verdict_phi(res["n"], res.get("rho", NAN), res.get("p_perm"))
    out["partitions"] = {w: dict(collections.Counter(v[1] for v in p.values())) for w, p in (("t4", p4), ("t5", p5))}
    cx = {k: (100 * (1 - v[0] / 9) if v[1] == "defined" else (100.0 if v[1] == "saturated" else None)) for k, v in p4.items()}
    cy = {k: (100 * (1 - v[0] / 9) if v[1] == "defined" else (100.0 if v[1] == "saturated" else None)) for k, v in p5.items()}
    keys, a, b, g = S.pair_arrays(cx, cy)
    out["C_star_alongside"] = {"n": len(keys), "rho": S.rho_pw(a, b, g) if len(keys) >= 3 else NAN,
                               "note": "C* = 100(1 - phi/9), saturated = 100; rating floor not applied here (descriptive)"}
    return out


def _rates(D, model, cond, keys):
    Kk, Nn = S.model_arrays(D, model, cond, keys)
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where(Nn > 0, Kk / np.where(Nn > 0, Nn, 1), np.nan)


def pair_matrix(R, g):
    M = np.full((R.shape[0], R.shape[0]), np.nan)
    for a, b in itertools.combinations(range(R.shape[0]), 2):
        m = np.isfinite(R[a]) & np.isfinite(R[b])
        if m.sum() >= 3:
            M[a, b] = M[b, a] = S.rho_pw(R[a][m], R[b][m], g[m])
    return M


def split_stats(M, A):
    B = [i for i in range(6) if i not in A]
    within = [M[a, b] for grp in (A, B) for a, b in itertools.combinations(grp, 2)]
    cross = [M[a, b] for a in A for b in B]
    w, c = float(np.mean(within)), float(np.mean(cross))
    return w - c, w, c


def exact_drift_p(dists, d_obs):
    """dists: per-model arrays of D over the 20 splits; exact p of the mean over models, all 20^M splits."""
    tot = np.zeros(1)
    for d in dists:
        tot = (tot[:, None] + np.asarray(d)[None, :]).ravel()
    tot = tot / len(dists)
    return float(np.mean(tot >= d_obs - 1e-12)), int(tot.size)


def h_stab_drift(w4, w5, cond="S0"):
    models = common_models(w4, w5, cond)
    out = {"tier": "SECONDARY", "condition": cond, "models": models,
           "statistic": "D = mean within-wave run-pair rho_pw - mean cross-wave run-pair rho_pw (rates k/n), per model, "
                        "averaged over models; SR = mean cross / mean within"}
    if len(models) < 2:
        return {**out, "verdict": "UNDETERMINED", "reason": "fewer than 2 N3 models retained at both waves"}
    keys = list(w4.D.brands)
    g = np.array([k[0] for k in keys])
    per, dists = {}, []
    for m in models:
        R = np.vstack([_rates(w4.D, m, cond, keys), _rates(w5.D, m, cond, keys)])
        M = pair_matrix(R, g)
        if not np.all(np.isfinite(M[np.triu_indices(6, 1)])):
            return {**out, "verdict": "UNDETERMINED", "reason": f"{m}: a run pair has no computable rho_pw"}
        d, w, c = split_stats(M, (0, 1, 2))
        per[m] = {"D": d, "within": w, "cross": c, "SR": c / w if w else NAN,
                  "pair_matrix": [[None if not np.isfinite(v) else float(v) for v in row] for row in M]}
        dists.append([split_stats(M, A)[0] for A in SPLITS])
    d_obs = float(np.mean([v["D"] for v in per.values()]))
    within = float(np.mean([v["within"] for v in per.values()]))
    cross = float(np.mean([v["cross"] for v in per.values()]))
    p, n_splits = exact_drift_p(dists, d_obs)
    sr = cross / within if within else NAN
    out.update({"D": d_obs, "within": within, "cross": cross, "SR": sr, "p_exact": p, "n_splits": n_splits,
                "per_model": per, "panel": "N3" if len(models) == 3 else "reduced panel"})
    out["verdict"] = verdict_drift(p, sr, within)
    return out


# =========================================================================== component legs
def read_component(path):
    out = {}
    for r in csv.DictReader(open(path, newline="", encoding="utf-8")):
        v = (r.get("value") or "").strip()
        out[(r["substrate"], r["brand"])] = float(v) if v not in ("", "NA", "NOT RATED") else None
    return out


def component_leg(name, f4, f5, gate, cfg, brands):
    if not f4 or not f5:
        return {"verdict": "NOT MEASURED", "reason": "no locked score at both waves (section 2.6)"}
    x, y = read_component(f4), read_component(f5)
    keys = [k for k in brands if x.get(k) is not None and y.get(k) is not None]
    out = {"gate": gate, "inputs_sha256": {w: hashlib.sha256(Path(f).read_bytes()).hexdigest() for w, f in (("t4", f4), ("t5", f5))}}
    xv, yv = np.array([x[k] for k in keys]), np.array([y[k] for k in keys])
    g = np.array([k[0] for k in keys])
    n = len(keys)
    rho = S.rho_pw(xv, yv, g) if n >= 3 else NAN
    p = S.perm_p_within(xv, yv, g, rho, SEEDS["components"], cfg.n_perm) if n >= 3 else NAN
    out.update({"n": n, "rho": rho, "p_perm": p})
    if n >= 3:
        b = S.bootstrap(g, SEEDS["components"], cfg.n_boot, lambda i: {"rho": S.rho_pw(xv[i], yv[i], g[i])})
        out["ci95_rho"] = b["rho"]["ci95"]
    if gate not in ("PASS", "MARGINAL"):
        out["verdict"] = "DESCRIPTIVE"
        out["reason"] = f"{name} gate is {gate}: computed and reported, no verdict (section 2.6)"
    else:
        out["verdict"] = verdict_component(n, rho, p)
    return out


def carried_ranking(path):
    if not path:
        return {"verdict": "PENDING", "reason": "v1.14 Stage 2 output not supplied; v1.14 owns the test (section 2.5)"}
    d = json.load(open(path, encoding="utf-8"))
    h = (d.get("verdicts") or {}).get("H3_Retest_Reliability") or d.get("H3_Retest_Reliability") or {}
    return {"verdict": h.get("verdict", "UNREADABLE"), "carried_from": str(path),
            "sha256": hashlib.sha256(Path(path).read_bytes()).hexdigest(),
            **{k: h.get(k) for k in ("rho", "n", "p_perm", "p_shuffle", "panel") if k in h}}


# =========================================================================== Presence score P (alongside)
def recognition_share(w, models, v23_override=None):
    """{(sub, brand): share of models whose S0 run-1 Phase A answer is coded recognized} (None if no coded answer).
    v23_override: {call_id: r_level} (the successor judge's codes; judge held constant across waves)."""
    codes = collections.defaultdict(dict)
    for r in w.A:
        if r["condition"] != "S0" or r["model"] not in models:
            continue
        rec = r.get("recognized")
        if r["substrate"] == "v0.23" and v23_override is not None:
            rec = C.r_level_to_binary(v23_override.get(r["call_id"], "R_ERR"))
        if rec is None or rec == "":
            continue
        codes[(r["substrate"], r["brand"])][r["model"]] = int(rec)
    return {k: (sum(v.values()) / len(v) if v else None) for k, v in codes.items()}


def presence_P(w, models, v23_override=None):
    pi = S.pi_hat(w.D, models, "S0")
    cp = recognition_share(w, models, v23_override)
    return {k: (100 * (cp[k] + 2 * pi[k]) / 3 if cp.get(k) is not None and np.isfinite(pi[k]) else None) for k in pi}


# =========================================================================== checks and descriptives
def _median_time(calls, cond):
    ts = sorted(datetime.fromisoformat(r["started_utc"]) for r in calls
                if r.get("condition") == cond and r.get("started_utc") and C.is_answered(r))
    return ts[len(ts) // 2] if ts else None


def mc_gap(w4, w5):
    a, b = _median_time(w4.calls, "S0"), _median_time(w5.calls, "S0")
    if not a or not b:
        return {"days": None, "pass": False}
    d = (b - a).total_seconds() / 86400
    return {"t4_median_utc": a.isoformat(), "t5_median_utc": b.isoformat(), "days": d,
            "pass": GAP_DAYS[0] <= d <= GAP_DAYS[1], "rule": f"{GAP_DAYS[0]}-{GAP_DAYS[1]} days, else flagged"}


def served_change(w4, w5):
    """MC_Served (addition): per model, the served IDs seen at each wave; flagged if t5's differ from t4's."""
    out = {}
    for m in MODELS:
        s4 = sorted({str(r.get("served_model")) for r in w4.calls if r["model_requested"] == m and C.is_answered(r)})
        s5 = sorted({str(r.get("served_model")) for r in w5.calls if r["model_requested"] == m and C.is_answered(r)})
        out[m] = {"t4": s4, "t5": s5, "flag_changed": s4 != s5}
    return out


def mc_probe_parity(w5, probes_path=K.PROBES_PATH):
    """t5 prompts equal the t4 probe file byte for byte (v1.14 section 6); halts otherwise."""
    t4 = C.load_probe_map(ROOT / "osf/v42/prereg/probes_v0_42.jsonl")
    t5 = C.load_probe_map(probes_path)
    same_file = ({k: v.get("prompt") for k, v in t4.items()} == {k: v.get("prompt") for k, v in t5.items()})
    bad = [r["call_id"] for r in w5.calls
           if r.get("prompt") is not None and t4.get((r["substrate"], r["phase"], r["probe_id"]), {}).get("prompt") != r["prompt"]]
    return {"probe_files_equal": same_file, "calls_with_other_prompt": len(bad), "examples": bad[:10],
            "pass": same_file and not bad}


def t4_parity(w4, brand_table):
    """Gate G3 (section 5.3): pi and phi (with partition) recomputed here from v0.42's coded t4 tables equal v0.42's
    scored brand table exactly (N3, S0 and S1), so the t4 side of every test is v0.42's own t4."""
    if brand_table is None:
        return {"pass": None, "note": "v0.42 brand table not supplied (synthetic run)"}
    rows = {(r["substrate"], r["brand"]): r for r in csv.DictReader(open(brand_table, newline="", encoding="utf-8"))}
    bad = []
    for c in ("S0", "S1"):
        ms = [m for m in MODELS if (m, c) not in w4.excl]
        if len(ms) < 3:
            continue
        pi, ph = S.pi_hat(w4.D, ms, c), S.phi_panel(w4.D, ms, c)
        for k in w4.D.brands:
            r = rows.get(k, {})
            want_pi = r.get(f"pi_N3_{c}", "")
            got_pi = "" if not np.isfinite(pi[k]) else pi[k]
            if (want_pi == "" and got_pi != "") or (want_pi != "" and (got_pi == "" or float(want_pi) != got_pi)):
                bad.append(f"{k} pi_{c}")
            want_phi, want_part = r.get(f"phi_N3_{c}", ""), r.get(f"phi_partition_N3_{c}", "")
            got_phi, got_part = ph[k][0], ph[k][1]
            if want_part != got_part or (want_phi == "") != (got_phi is None) or \
                    (got_phi is not None and float(want_phi) != got_phi):
                bad.append(f"{k} phi_{c}")
    return {"pass": not bad, "mismatches": len(bad), "examples": bad[:10],
            "sha256": hashlib.sha256(Path(brand_table).read_bytes()).hexdigest()}


def descriptives(w4, w5):
    keys = list(w4.D.brands)
    g = np.array([k[0] for k in keys])
    rel = {}
    for wn, w in (("t4", w4), ("t5", w5)):
        for m in MODELS:
            for c in ("S0", "S1"):
                Kk, Nn = S.model_arrays(w.D, m, c, keys)
                r1 = S.rel1_of(Kk, Nn, g)
                rel[f"{wn}|{m}|{c}"] = {"rel1": r1, "rel3": S.rel3_of(r1)}
    floor = {}
    for c in ("S0",):
        ms = common_models(w4, w5, c)
        if ms:
            p4, p5 = S.pi_hat(w4.D, ms, c), S.pi_hat(w5.D, ms, c)
            below4 = {k for k, v in p4.items() if np.isfinite(v) and v * S.F < 1}
            below5 = {k for k, v in p5.items() if np.isfinite(v) and v * S.F < 1}
            floor[c] = {"below_t4": len(below4), "still_below_t5": len(below4 & below5),
                        "share_still_below": len(below4 & below5) / len(below4) if below4 else None,
                        "above_t4_below_t5": len((set(p4) - below4) & below5)}
    search = {}
    for wn, w in (("t4", w4), ("t5", w5)):
        for m in MODELS:
            rs = [r for r in w.calls if r["model_requested"] == m and r["condition"] == "S1" and C.is_answered(r)]
            if rs:
                search[f"{wn}|{m}"] = {"calls": len(rs), "searches_per_call": statistics.mean(S._search_n(r) for r in rs),
                                       "sources_per_call": statistics.mean(len((r.get("search") or {}).get("sources") or []) for r in rs),
                                       "citations_per_call": statistics.mean(len((r.get("search") or {}).get("citations") or []) for r in rs),
                                       "share_with_citation": statistics.mean(int(bool((r.get("search") or {}).get("citations"))) for r in rs)}
    cost = {wn: round(sum(BG.record_cost(r) for r in w.raw), 4) for wn, w in (("t4", w4), ("t5", w5))}
    by_block = collections.defaultdict(float)
    for wn, w in (("t4", w4), ("t5", w5)):
        for r in w.raw:
            by_block[f"{wn}|{r.get('model_requested')}|{r.get('phase')}-{r.get('condition')} run {r.get('run')}"] += BG.record_cost(r)
    recog = {}
    for wn, w in (("t4", w4), ("t5", w5)):
        for m in MODELS:
            codes = [int(r["recognized"]) for r in w.A if r["model"] == m and r["condition"] == "S0"
                     and r.get("recognized") not in (None, "")]
            recog[f"{wn}|{m}"] = {"coded": len(codes), "share_recognized": (sum(codes) / len(codes)) if codes else None}
    return {"run_to_run_reliability": rel, "floor_persistence": floor, "search": search, "cost_usd_recorded": cost,
            "cost_usd_by_model_block": {k: round(v, 4) for k, v in sorted(by_block.items())},
            "recognition_share_by_model": recog,
            "answer_form": answer_form(w4, w5), "cited_domains": cited_domain_overlap(w4, w5)}


REFUSAL_REASONS = ("refusal", "safety", "content_filter")


def answer_form(w4, w5):
    """Descriptive 4: words per answer, registry brands named per Phase B answer, finish reasons, refusals and
    Phase A non-answers (v0.19-v0.22 answers the yes/no parser cannot code), per wave x model x condition x phase."""
    out = {}
    for wn, w in (("t4", w4), ("t5", w5)):
        named = collections.Counter()
        for r in w.B:
            named[r["call_id"]] += int(r["mentioned"])
        labels = {r["call_id"]: r.get("label") for r in w.A}
        for m in MODELS:
            for c in ("S0", "S1"):
                for ph in ("A", "B"):
                    rs = [r for r in w.calls if r["model_requested"] == m and r["condition"] == c and r["phase"] == ph
                          and C.is_answered(r) and r["call_id"] not in w.served_excl]
                    if not rs:
                        continue
                    fr = collections.Counter(str(r.get("finish_reason")) for r in rs)
                    d = {"answers": len(rs), "words_per_answer": statistics.mean(len((r.get("text") or "").split()) for r in rs),
                         "finish_reasons": dict(fr),
                         "refusals": sum(n for k, n in fr.items() if any(x in k.lower() for x in REFUSAL_REASONS))}
                    if ph == "B":
                        d["registry_brands_named_per_answer"] = statistics.mean(named.get(r["call_id"], 0) for r in rs)
                    else:
                        yn = [labels.get(r["call_id"]) for r in rs if r["substrate"] != "v23"]
                        d["phase_a_non_answers"] = sum(1 for x in yn if x not in ("yes", "no"))
                    out[f"{wn}|{m}|{c}|{ph}"] = d
    return out


def cited_domain_overlap(w4, w5, top=20):
    """Descriptive 5: Jaccard overlap of the `top` most-cited domains (S1 citations) per model, t4 vs t5."""
    tops = {}
    for wn, w in (("t4", w4), ("t5", w5)):
        for m in MODELS:
            cnt = collections.Counter()
            for r in w.calls:
                if r["model_requested"] == m and r["condition"] == "S1" and C.is_answered(r):
                    for cit in ((r.get("search") or {}).get("citations") or []):
                        d = S._domain(cit.get("url") or "")
                        if d:
                            cnt[d] += 1
            tops[(wn, m)] = [d for d, _ in cnt.most_common(top)]
    out = {}
    for m in MODELS:
        a, b = set(tops[("t4", m)]), set(tops[("t5", m)])
        out[m] = {"t4_top": tops[("t4", m)], "t5_top": tops[("t5", m)],
                  "jaccard": (len(a & b) / len(a | b)) if (a | b) else None}
    return out


def disattenuated(h_presence, desc):
    """Descriptive 1 (second half): rho*_m = rho_m / sqrt(rel3_t4 * rel3_t5), S0, per model."""
    out = {}
    for m, v in (h_presence.get("per_model") or {}).items():
        r4 = desc["run_to_run_reliability"].get(f"t4|{m}|S0", {}).get("rel3", NAN)
        r5 = desc["run_to_run_reliability"].get(f"t5|{m}|S0", {}).get("rel3", NAN)
        ok = np.isfinite(r4) and np.isfinite(r5) and r4 > 0 and r5 > 0
        out[m] = {"rho": v["rho"], "rel3_t4": r4, "rel3_t5": r5,
                  "rho_star": v["rho"] / float(np.sqrt(r4 * r5)) if ok else NAN}
    return out


# =========================================================================== orchestration
def score(t4, t5, cfg, extras=None, enforce=True):
    """t4, t5: (raw, A, B). extras: ranking_stage2, components {name: (f4, f5, gate)}, v23_t4_successor, j1."""
    extras = extras or {}
    brands = brands_list()
    w4, w5 = Wave(*t4, brands, "t4"), Wave(*t5, brands, "t5")
    parity = mc_probe_parity(w5)
    if enforce and not parity["pass"]:
        raise Halt(f"t5 prompts differ from t4's: {parity}")
    g3 = t4_parity(w4, extras.get("t4_brand_table"))
    if enforce and g3["pass"] is False:
        raise Halt(f"gate G3: t4 values recomputed here differ from v0.42's brand table: {g3}")
    hyps = {"H_Stab_Presence": h_stab_presence(w4, w5, cfg),
            "H_Stab_Consistency": h_stab_consistency(w4, w5, cfg),
            "H_Stab_Drift": h_stab_drift(w4, w5),
            "H_Stab_Search_Presence": h_stab_presence(w4, w5, cfg, "S1", "H_Stab_Search_Presence", "SECONDARY")}
    parts = {"Presence": {"verdict_from": "H_Stab_Presence"}, "Consistency": {"verdict_from": "H_Stab_Consistency"},
             "Ranking": carried_ranking(extras.get("ranking_stage2"))}
    for name in ("Grounding", "Coverage", "Sentiment"):
        f4, f5, gate = (extras.get("components") or {}).get(name, (None, None, None))
        parts[name] = component_leg(name, f4, f5, gate, cfg, brands)
    ms = common_models(w4, w5, "S0")
    j1 = extras.get("j1")
    v23 = extras.get("v23_t4_successor")
    P4, P5 = presence_P(w4, ms, v23), presence_P(w5, ms)
    keys, a, b, g = S.pair_arrays({k: (NAN if v is None else v) for k, v in P4.items()},
                                  {k: (NAN if v is None else v) for k, v in P5.items()})
    hyps["H_Stab_Presence"]["P_alongside"] = {
        "n": len(keys), "rho": S.rho_pw(a, b, g) if len(keys) >= 3 else NAN,
        "v23_t4_codes": "successor judge (held constant)" if v23 is not None else "v0.42 Sonnet 4.5 codes (mixed judges; flagged)"}
    mcs = dict(w5.mcs)
    mcs.update({"MC_Probe_Parity": parity, "G3_t4_parity": g3, "MC_Gap": mc_gap(w4, w5),
                "MC_Judge_J1": (j1 or {}).get("verdict", {"pass": None, "note": "J1 record not supplied"}),
                "MC_Budget": {"t5_calls_usd": round(sum(BG.record_cost(r) for r in w5.raw), 4),
                              "judge_reserve_usd": BG.JUDGE_RESERVE_USD, "cap_usd": BG.BUDGET_CAP_USD}})
    out = {"phase": PHASE_ID, "prereg": "osf/v45/prereg/PRE_REGISTRATION_v0_45.md", "prereg_tag": PREREG_TAG,
           "seeds": SEEDS, "draws": {"permutation": cfg.n_perm, "bootstrap": cfg.n_boot},
           "models_excluded": {"t4": sorted(f"{m}|{c}" for m, c in w4.excl), "t5": sorted(f"{m}|{c}" for m, c in w5.excl)},
           "manipulation_checks_t5": mcs, "verdicts": hyps, "parts": parts, "descriptives": descriptives(w4, w5)}
    out["descriptives"]["disattenuated_rho_S0"] = disattenuated(hyps["H_Stab_Presence"], out["descriptives"])
    out["manipulation_checks_t5"]["MC_Served_change"] = served_change(w4, w5)
    rows = []
    pis = {f"pi_{w.name}_{c}": S.pi_hat(w.D, common_models(w4, w5, c) or MODELS, c) for w in (w4, w5) for c in ("S0", "S1")}
    phis = {f"phi_{w.name}_S0": S.phi_panel(w.D, MODELS, "S0") for w in (w4, w5)}
    for k in brands:
        r = {"substrate": k[0], "brand": k[1], **{n: v[k] for n, v in pis.items()}}
        for n, v in phis.items():
            r[n], r[n.replace("phi_", "phi_partition_")] = v[k][0], v[k][1]
        r["P_t4_S0"], r["P_t5_S0"] = P4.get(k), P5.get(k)
        rows.append(r)
    return out, rows


def write_outputs(out, rows, dest):
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    S.write_outputs(out, rows, dest / "v45_verdicts.json", dest / "v45_unit_table.csv")


def load_dir(d, raw_name):
    d = Path(d)
    raw = C.read_raw(d / raw_name)
    A, B = C.read_tables(d / "coded")
    return raw, A, B


def main():
    ap = argparse.ArgumentParser(description="AIAS v0.45 scorer (t4 -> t5 stability)")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--synthetic", nargs=2, metavar=("T4DIR", "T5DIR"))
    g.add_argument("--run", action="store_true")
    ap.add_argument("--draws", type=int, default=None, help="tests only")
    ap.add_argument("--t4-dir", help="--run: t4_raw.jsonl (from tag v0.42-acquisition-locked) + coded/ (v0.42's scored commit)")
    ap.add_argument("--t4-brand-table", help="--run: v0.42's v42_brand_table.csv (gate G3)")
    ap.add_argument("--j1", help="--run: osf/v45/data/judge_parity_J1_v0_45.json (successor judge record, with t4_codes)")
    ap.add_argument("--ranking-stage2", help="v1.14 Stage 2 output (carried Ranking verdict)")
    ap.add_argument("--component", action="append", default=[], metavar="NAME=T4CSV,T5CSV,GATE",
                    help="Grounding / Coverage / Sentiment locked scores at both waves and that component's gate state")
    a = ap.parse_args()
    cfg = S.Cfg(*(a.draws,) * 2) if a.draws else S.Cfg()
    comps = {}
    for spec in a.component:
        name, rest = spec.split("=", 1)
        f4, f5, gate = rest.split(",")
        comps[name] = (f4, f5, gate)
    if a.run:
        if a.draws:
            ap.error("--draws is for tests only")
        r = subprocess.run(["git", "-C", str(ROOT), "ls-remote", "--tags", "origin", PREREG_TAG, ACQ_TAG],
                           capture_output=True, text=True, timeout=60)
        if f"refs/tags/{PREREG_TAG}" not in r.stdout or f"refs/tags/{ACQ_TAG}" not in r.stdout:
            print(f"[v45] REFUSED: {PREREG_TAG} and {ACQ_TAG} must be on origin", file=sys.stderr)
            return 3
        if not (a.t4_dir and a.t4_brand_table and a.j1):
            ap.error("--run needs --t4-dir, --t4-brand-table and --j1")
        dest = ROOT / "osf/v45"
        if (dest / "v45_verdicts.json").exists():
            print("[v45] REFUSED: scored once already (osf/v45/v45_verdicts.json exists)", file=sys.stderr)
            return 3
        j1 = json.load(open(a.j1, encoding="utf-8"))
        extras = {"t4_brand_table": a.t4_brand_table, "j1": j1, "ranking_stage2": a.ranking_stage2,
                  "components": comps, "v23_t4_successor": j1.get("t4_codes") if j1.get("verdict", {}).get("pass") else None}
        t4 = load_dir(a.t4_dir, "t4_raw.jsonl")
        raw5 = C.read_raw(K.REAL_RAW)
        A5, B5 = C.read_tables(K.DEFAULT_OUT)
        try:
            out, rows = score(t4, (raw5, A5, B5), cfg, extras)
        except Halt as e:
            print(f"[v45] HALT: {e}", file=sys.stderr)
            return 4
        write_outputs(out, rows, dest)
        print(f"wrote {dest}/v45_verdicts.json")
        return 0
    d4, d5 = Path(a.synthetic[0]).resolve(), Path(a.synthetic[1]).resolve()
    try:
        out, rows = score(load_dir(d4, "t4_raw.jsonl"), load_dir(d5, "t5_raw.jsonl"), cfg,
                          {"ranking_stage2": a.ranking_stage2, "components": comps})
    except Halt as e:
        print(f"[v45] HALT: {e}", file=sys.stderr)
        return 4
    write_outputs(out, rows, d5 / "_score")
    for k, v in out["verdicts"].items():
        print(f"  {k}: {v['verdict']}")
    for k, v in out["parts"].items():
        print(f"  part {k}: {v.get('verdict', v.get('verdict_from'))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
