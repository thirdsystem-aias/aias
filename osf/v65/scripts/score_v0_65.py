#!/usr/bin/env python3
"""
score_v0_65.py -- AIAS(TM) v0.65 scorer SKELETON (study #55, cross-cultural identity load), pre-registration
DRAFT r0. Re-analysis of v0.62's Spanish, Korean and Chinese category answers against t4's English answers
(v0.42). No model call, no network, no spend. THE PRE-REGISTRATION PROSE IS AUTHORITATIVE: a constant here that
disagrees with the prose is a bug to fix toward the prose.

Identity load (IL-Direct), exactly as the programme defines it (v0.37, osf/v37/prereg/
v0_37_cpc_identity_load_moderator_content.py, MODERATOR_DEFINITION; construct anchor v1.6 Increment 2,
H_IdentityLoad_Direct): IL-Direct(b) = R_cult(b) - R_cat(b), the per-brand two-channel recall asymmetry; higher =
more cultural-channel-led surfacing = higher identity load; construct-valid scope = the canonical two-channel trio
v0.20 / v0.21 / v0.22 (72 units). Here R_cult and R_cat are counted per language on N3 (three models), S0, three
runs, and divided by the answered calls of the channel (rate form, section 2.1 of the pre-registration; with complete
data it is the count form divided by 27, so the within-category ranks are identical; sensitivity S-Count uses the
count form). Channel of each question: the `channel` field of osf/v62/inputs/probes_v0_42.jsonl (byte copy of t4's
probes): R_cat / R_cult for the trio.

Modes: --dry-run (synthetic v0.62-shaped data only; writes prereg/dry_run_v0_65_r0.txt), --power (synthetic;
writes prereg/power_v0_65_r0.json), --lock-manifest,
--verify-lock, --run (refuses: see guard_run). Without a mode nothing is computed.
"""
import argparse
import collections
import csv
import hashlib
import io
import json
import math
import os
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = Path(os.environ.get("AIAS_ROOT", str(HERE.parents[2]))).resolve()
V62S = ROOT / "osf/v62/scripts"
sys.path.insert(0, str(V62S))
import params_v0_62 as P62  # noqa: E402  (locked v0.62 parameters, imported unchanged)
import score_v0_62 as S62   # noqa: E402  (locked v0.62 statistics, imported unchanged)

V65 = ROOT / "osf/v65"
PREREG_TAG = "v0.65-prereg-r1"
V62_TAG = "v0.62-prereg-r1"
VERDICTS = V65 / "outputs/v65_verdicts.json"
V62_VERDICTS = ROOT / "osf/v62/v62_verdicts.json"
PROBES = ROOT / "osf/v62/inputs/probes_v0_42.jsonl"
TRANSLATIONS = ROOT / "osf/v62/translations/translations_v0_62_r2.json"
V62_CODED = ROOT / "osf/v62/data/coded"
V17_CPC = ROOT / "osf/methodology/v1_7/data/v1_7_cpc.csv"
MANIFEST = V65 / "prereg/LOCK_MANIFEST_v0_65.sha256"

# English comparator: t4's coded Phase B tables, read from git at v0.42's scoring tag, each blob pinned (section 4.1).
EN_TAG = "v0.42-scoring-locked"
EN_BLOBS = {
    "v19": "7fb571b51eac6e408eb4e48440b07bd9aa4b3ad7",
    "v20": "5f765d9853c94bc0456531615a1bf384a3a65cdf",
    "v21": "feb9d5f6297f98d6cff35b2f2237660b53dfc733",
    "v22": "8dc39b9d39645658bf4786ff96258dd040a84126",
    "v23": "7f379235ecdc851f62acf14f15d0b63b68389bbb",
}

MODELS, RUNS = list(S62.MODELS), tuple(S62.RUNS)
LANGS = ("es", "ko", "zh")
TRIO = ("v0.20", "v0.21", "v0.22")          # confirmatory scope (v0.37 MODERATOR_DEFINITION)
EXPLORATORY = ("v0.19", "v0.23")            # exploratory E1 only (out of construct in v0.37)
CAT_LABELS = {"R_cat", "category_anchored", "editorial-authority"}
CULT_LABELS = {"R_cult", "cultural_footprint", "cultural-cult"}

SEEDS = {("H1", "es"): 650101, ("H1", "ko"): 650102, ("H1", "zh"): 650103,
         ("H2", "es"): 650111, ("H2", "ko"): 650112, ("H2", "zh"): 650113,
         ("H3", "es"): 650121, ("H3", "ko"): 650122, ("H3", "zh"): 650123,
         "bootstrap_rho": 650131, "descriptives": 650141,
         "dry_run": (650151, 650152, 650153, 650154, 650155), "power": 650161}
N_PERM = N_BOOT = 10_000
ALPHA = 0.05
N_FLOOR = 45                                  # v0.37 ELIGIBILITY_ATTRITION power floor
H1_BARS = (0.50, 0.30)                        # CONFIRMED rho_c >= 0.50 and p < .05; FALSIFIED rho_c < 0.30
H2_BARS = (0.30, 0.15)                        # v0.37 bands: CONFIRMED rho <= -0.30 and p < .05; FALSIFIED rho > -0.15
# H3 equivalence bound: 2/27 (two mentions in the 27 answered calls of a channel, per unit on average). r0 first
# drafted 1/27; the synthetic dry run showed the 95% interval of the mean shift is about +/-0.04 wide at n ~ 72, so
# 1/27 (0.037) could almost never return FALSIFIED (DEVIATIONS Entry 0, item 6; decision Q5 for the pre-registrant).
H3_SESOI = 2.0 / 27.0
NAN = float("nan")


# =========================================================================== design inputs
def canon_sub(s):
    """'v20' / 'v0.20' -> 'v0.20'."""
    s = str(s)
    return s if s.startswith("v0.") else "v0." + s[1:]


def channel_map(path=PROBES):
    """{(substrate, frame_id): 'cat' | 'cult'} for every Phase B question of t4 (30)."""
    out = {}
    for line in open(path, encoding="utf-8"):
        r = json.loads(line)
        if r.get("phase") != "B":
            continue
        ch = r.get("channel")
        if ch in CAT_LABELS:
            out[(canon_sub(r["substrate"]), r["frame_id"])] = "cat"
        elif ch in CULT_LABELS:
            out[(canon_sub(r["substrate"]), r["frame_id"])] = "cult"
        else:
            raise ValueError(f"unknown channel label {ch!r} for {r['probe_id']}")
    return out


def drift_map(path=TRANSLATIONS, probes=PROBES):
    """{(lang, substrate, frame_id): 'equivalent' | 'minor drift' | 'meaning change'} from v0.62's r2 translations."""
    pid2frame = {}
    for line in open(probes, encoding="utf-8"):
        r = json.loads(line)
        if r.get("phase") == "B":
            pid2frame[(canon_sub(r["substrate"]), r["probe_id"])] = r["frame_id"]
    out = {}
    for it in json.load(open(path, encoding="utf-8"))["phase_b"]:
        sub = canon_sub(it["substrate"])
        fr = pid2frame[(sub, it["probe_id"])]
        for lg in LANGS:
            out[(lg, sub, fr)] = it[f"{lg}_drift"]
    return out


# =========================================================================== identity load per language
def il_values(rows, units, cmap, frames_keep=None, excluded_calls=frozenset(), models=None):
    """Coded Phase B rows (v0.62 / v0.42 shape: call_id, substrate, brand, model, condition, run, frame_id, mentioned)
    -> {unit: {'il', 'il_count', 'pi', 'c_cat', 'c_cult', 'n_cat', 'n_cult'}}.
    n_ch = answered calls of the unit's category in channel ch (N3, S0, runs 1-3); c_ch = calls of that set whose
    answer mentions the unit. il = c_cult/n_cult - c_cat/n_cat (rate form); il_count = c_cult - c_cat (v0.37 form);
    pi = (c_cat + c_cult) / (n_cat + n_cult) (= v0.62's recall Presence over the six questions).
    frames_keep: optional set of (substrate, frame_id) to use (S-Drift)."""
    models = MODELS if models is None else models
    calls = collections.defaultdict(set)
    ment = collections.defaultdict(int)
    for r in rows:
        if r.get("condition", "S0") != "S0" or r["model"] not in models or int(r["run"]) not in RUNS:
            continue
        if r["call_id"] in excluded_calls:
            continue
        sub = canon_sub(r["substrate"])
        key = (sub, r["frame_id"])
        if key not in cmap or (frames_keep is not None and key not in frames_keep):
            continue
        ch = cmap[key]
        calls[(sub, ch)].add(r["call_id"])
        if int(r["mentioned"]):
            ment[(sub, r["brand"], ch)] += 1
    out = {}
    for (s, b) in units:
        n_cat, n_cult = len(calls[(s, "cat")]), len(calls[(s, "cult")])
        c_cat, c_cult = ment[(s, b, "cat")], ment[(s, b, "cult")]
        ok = n_cat > 0 and n_cult > 0
        out[(s, b)] = {"il": (c_cult / n_cult - c_cat / n_cat) if ok else NAN,
                       "il_count": float(c_cult - c_cat) if ok else NAN,
                       "pi": (c_cat + c_cult) / (n_cat + n_cult) if (n_cat + n_cult) else NAN,
                       "c_cat": c_cat, "c_cult": c_cult, "n_cat": n_cat, "n_cult": n_cult}
    return out


def eligible(v):
    """Section 2.2: a unit enters H1/H3 in language L iff 0 < pi < 1 in English AND in L (v0.37's true-zero floor and
    saturation ceiling, applied to pi over the six questions) and IL is defined in both."""
    return v is not None and np.isfinite(v["il"]) and np.isfinite(v["pi"]) and 0.0 < v["pi"] < 1.0


# =========================================================================== statistics
def partial_rho_c(x, y, z, g):
    """Partial correlation of the centred within-category ranks of x and y given those of z (section 2.1)."""
    rx, ry, rz = (S62.centred_ranks(v, g) for v in (x, y, z))
    rxy, rxz, ryz = S62._pearson(rx, ry), S62._pearson(rx, rz), S62._pearson(ry, rz)
    if not all(np.isfinite(v) for v in (rxy, rxz, ryz)):
        return NAN
    d = math.sqrt(max(0.0, (1 - rxz * rxz) * (1 - ryz * ryz)))
    return (rxy - rxz * ryz) / d if d > 0 else NAN


def perm_two_tails(stat, x, g, seed, n_draws):
    """x permuted within category; returns (p_lower, p_upper) = (1 + #{T_perm <= T}) / (N + 1), (1 + #{T_perm >= T})."""
    obs = stat(np.asarray(x, float))
    if not np.isfinite(obs):
        return NAN, NAN
    rng = np.random.default_rng(seed)
    x = np.asarray(x, float)
    lo = hi = 0
    for _ in range(n_draws):
        xp = x.copy()
        for gi in S62._gidx(g):
            xp[gi] = x[rng.permutation(gi)]
        t = stat(xp)
        lo += bool(t <= obs + 1e-12)
        hi += bool(t >= obs - 1e-12)
    return (1 + lo) / (n_draws + 1), (1 + hi) / (n_draws + 1)


def verdict_h1(n, rho, p):
    if n < N_FLOOR or not np.isfinite(rho) or not np.isfinite(p):
        return "UNDETERMINED"
    if rho >= H1_BARS[0] and p < ALPHA:
        return "CONFIRMED"
    return "FALSIFIED" if rho < H1_BARS[1] else "MARGINAL"


def verdict_h2(n, rho, p_lower, p_upper):
    """Predicted sign negative. Returns (verdict, label)."""
    if n < N_FLOOR or not np.isfinite(rho) or not np.isfinite(p_lower):
        return "UNDETERMINED", None
    if rho <= -H2_BARS[0] and p_lower < ALPHA:
        return "CONFIRMED", None
    if rho > -H2_BARS[1]:
        rev = "REVERSED" if (rho >= H2_BARS[0] and p_upper < ALPHA) else None
        return "FALSIFIED", rev
    return "MARGINAL", None


def verdict_h3(n, delta, ci, sesoi=H3_SESOI):
    """Two-sided level shift of IL. Returns (verdict, direction)."""
    if n < N_FLOOR or not np.isfinite(delta) or not all(np.isfinite(ci)):
        return "UNDETERMINED", None
    if -sesoi < ci[0] and ci[1] < sesoi:
        return "FALSIFIED", "equivalent within the bound"
    if (ci[0] > 0 or ci[1] < 0) and abs(delta) >= sesoi:
        return "CONFIRMED", "toward cultural" if delta > 0 else "toward category"
    return "MARGINAL", None


def joint_reading(h1):
    """Section 2.6 on the H1 verdicts {lang: verdict}."""
    if all(h1[l] == "CONFIRMED" for l in LANGS):
        return "IL-portable"
    bad = [l.upper() for l in LANGS if h1[l] == "FALSIFIED"]
    if bad:
        return "IL-language-bound (" + ", ".join(bad) + ")"
    return "Partly portable"


# =========================================================================== tests (section 2)
def dropped_models(rows, n_questions=30):
    """v0.62 section 7.4 drop rule: a model with < 90% of its expected Phase B calls (3 runs x n_questions) answered."""
    calls = collections.defaultdict(set)
    for r in rows:
        if r.get("condition", "S0") == "S0":
            calls[r["model"]].add(r["call_id"])
    return [m for m in MODELS if len(calls[m]) < S62.DROP_SHARE * len(RUNS) * n_questions]


def _arrays(keys, xd, yd, field_x="il", field_y="il"):
    x = np.array([xd[k][field_x] for k in keys], float)
    y = np.array([yd[k][field_y] for k in keys], float)
    g = np.array([k[0] for k in keys])
    return x, y, g


def h1_test(en, lv, units, seed, n_perm, n_boot, field="il"):
    keys = [u for u in units if eligible(en.get(u)) and eligible(lv.get(u))]
    x, y, g = _arrays(keys, en, lv, field, field)
    rho = S62.rho_c(x, y, g) if len(keys) >= 3 else NAN
    t = {"n": len(keys), "rho_c": rho,
         "rho_uncentred": S62.rho_uncentred(x, y, g) if len(keys) >= 3 else NAN,
         "p_perm_one_sided": S62.perm_p(x, y, g, rho, seed, n_perm) if np.isfinite(rho) else NAN}
    t["ci95_rho_c"] = (S62.bootstrap_ci(g, SEEDS["bootstrap_rho"], n_boot, lambda i: S62.rho_c(x[i], y[i], g[i]))
                       if np.isfinite(rho) else [NAN, NAN])
    t["per_category_rho_c"] = {c: (S62.rho_c(x[g == c], y[g == c], g[g == c]) if (g == c).sum() >= 3 else NAN)
                               for c in dict.fromkeys(g)}
    t["verdict"] = verdict_h1(t["n"], rho, t["p_perm_one_sided"])
    return t, keys


def h2_test(en, lv, units, seed, n_perm):
    keys = [u for u in units if eligible(en.get(u)) and lv.get(u) is not None and np.isfinite(lv[u]["pi"])]
    x = np.array([en[k]["il"] for k in keys], float)
    y = np.array([lv[k]["pi"] for k in keys], float)
    z = np.array([en[k]["pi"] for k in keys], float)
    g = np.array([k[0] for k in keys])
    stat = (lambda xx: partial_rho_c(xx, y, z, g))
    rho = stat(x) if len(keys) >= 4 else NAN
    plo, phi_ = perm_two_tails(stat, x, g, seed, n_perm) if np.isfinite(rho) else (NAN, NAN)
    v, label = verdict_h2(len(keys), rho, plo, phi_)
    simple = S62.rho_c(x, y - z, g) if len(keys) >= 3 else NAN
    return {"n": len(keys), "rho_partial": rho, "p_lower": plo, "p_upper": phi_, "verdict": v, "label": label,
            "reported_alongside_rho_c_IL_EN_vs_delta_pi": simple}


def h3_test(en, lv, keys, seed, n_boot, sesoi=H3_SESOI):
    if not keys:
        return {"n": 0, "delta_IL": NAN, "ci95": [NAN, NAN], "verdict": "UNDETERMINED", "direction": None}
    x, y, g = _arrays(keys, en, lv)
    d = float(np.mean(y - x))
    ci = S62.bootstrap_ci(g, seed, n_boot, lambda i: float(np.mean(y[i] - x[i])))
    v, direction = verdict_h3(len(keys), d, ci, sesoi)
    by_ch = {}
    for ch in ("cat", "cult"):
        a = np.array([en[k][f"c_{ch}"] / en[k][f"n_{ch}"] for k in keys])
        b = np.array([lv[k][f"c_{ch}"] / lv[k][f"n_{ch}"] for k in keys])
        by_ch[ch] = {"mean_rate_en": float(a.mean()), "mean_rate_l": float(b.mean())}
    return {"n": len(keys), "delta_IL": d, "ci95": ci, "sesoi": sesoi, "verdict": v, "direction": direction,
            "channel_rates": by_ch}


def coi_trio(units):
    """S-COI: v0.62's COI_FLAGGED units that fall in the trio (imported unchanged from params_v0_62)."""
    return [u for u in units if u not in set(P62.COI_FLAGGED)]


def equivalent_frames(dmap, lg):
    return {(s, f) for (l, s, f), code in dmap.items() if l == lg and code == "equivalent"}


def score(units, en_rows, lang_rows, cmap, dmap, n_perm=N_PERM, n_boot=N_BOOT, excluded=None, alias_rows=None,
          t1_il=None, n_questions=30):
    """units: all registry units [(substrate, brand)]; en_rows: t4 coded Phase B rows; lang_rows: {lang: rows};
    excluded: {'S-Language': {lang: call_ids}, 'S-Script': {'zh': call_ids}} from v0.62's manipulation checks;
    alias_rows: {lang: rows coded with collision-prone aliases off} (S-Alias); t1_il: {unit: IL-Direct at t1}."""
    trio = [u for u in units if u[0] in TRIO]
    expl = [u for u in units if u[0] in EXPLORATORY]
    out = {"phase": "v0.65", "prereg_tag": PREREG_TAG, "n_trio_units": len(trio), "tests": {}, "sensitivities": {},
           "descriptives": {}, "exploratory": {}}
    en = il_values(en_rows, units, cmap)
    en_drop = dropped_models(en_rows, n_questions)
    out["en_dropped_models"] = en_drop
    h1v, lv_all, keys_all = {}, {}, {}
    for lg in LANGS:
        rows = lang_rows.get(lg, [])
        drop = dropped_models(rows, n_questions)
        und = (f"English comparator incomplete: {en_drop}" if en_drop else None) or \
              (f"models below 90% of Phase B calls in {lg}: {drop}" if drop else None)
        lv = il_values(rows, units, cmap)
        lv_all[lg] = lv
        t1, keys = h1_test(en, lv, trio, SEEDS[("H1", lg)], n_perm, n_boot)
        t2 = h2_test(en, lv, trio, SEEDS[("H2", lg)], n_perm)
        t3 = h3_test(en, lv, keys, SEEDS[("H3", lg)], n_boot)
        keys_all[lg] = keys
        if und:
            for t in (t1, t2, t3):
                t["verdict"], t["reason"] = "UNDETERMINED", und
        out["tests"][f"H1_IL_Order_{lg}"] = t1
        out["tests"][f"H2_IL_Moderates_Language_{lg}"] = t2
        out["tests"][f"H3_IL_Shift_{lg}"] = t3
        h1v[lg] = t1["verdict"]
        # ---------------------------------------------------------------- sensitivities (section 7.5; no verdict changes)
        sens = {}
        ks = coi_trio(trio)
        s1, kk = h1_test(en, lv, ks, SEEDS[("H1", lg)], n_perm, n_boot)
        sens["S-COI"] = {"H1": s1, "H2": h2_test(en, lv, ks, SEEDS[("H2", lg)], n_perm),
                         "H3": h3_test(en, lv, kk, SEEDS[("H3", lg)], n_boot), "n_units": len(ks)}
        fk = equivalent_frames(dmap, lg)
        en_d, lv_d = il_values(en_rows, units, cmap, fk), il_values(rows, units, cmap, fk)
        s1, kk = h1_test(en_d, lv_d, trio, SEEDS[("H1", lg)], n_perm, n_boot)
        sens["S-Drift"] = {"H1": s1, "H3": h3_test(en_d, lv_d, kk, SEEDS[("H3", lg)], n_boot),
                           "frames_kept": sorted(f"{s}/{f}" for s, f in fk if s in TRIO)}
        sens["S-Count"] = {"H1": h1_test(en, lv, trio, SEEDS[("H1", lg)], n_perm, n_boot, field="il_count")[0]}
        for name in ("S-Language", "S-Script"):
            calls = (excluded or {}).get(name, {}).get(lg)
            if calls is None:
                sens[name] = {"status": "NOT AVAILABLE" if not (name == "S-Script" and lg != "zh") else "not applicable"}
                continue
            lx = il_values(rows, units, cmap, excluded_calls=set(calls))
            s1, kk = h1_test(en, lx, trio, SEEDS[("H1", lg)], n_perm, n_boot)
            sens[name] = {"H1": s1, "H3": h3_test(en, lx, kk, SEEDS[("H3", lg)], n_boot), "excluded_calls": len(calls)}
        if alias_rows and lg in alias_rows and lg != "es":
            la = il_values(alias_rows[lg], units, cmap)
            s1, kk = h1_test(en, la, trio, SEEDS[("H1", lg)], n_perm, n_boot)
            sens["S-Alias"] = {"H1": s1, "H3": h3_test(en, la, kk, SEEDS[("H3", lg)], n_boot)}
        else:
            sens["S-Alias"] = {"status": "not applicable" if lg == "es" else "NOT AVAILABLE"}
        for name, s in sens.items():
            if und:                                   # the drop rule applies to every sensitivity in L as well
                for h in ("H1", "H2", "H3"):
                    if h in s:
                        s[h]["verdict"], s[h]["reason"] = "UNDETERMINED", und
            if "H1" in s:
                s["H1_differs_from_primary"] = s["H1"]["verdict"] != t1["verdict"]
        out["sensitivities"][lg] = sens
        # ---------------------------------------------------------------- exploratory E1 (v0.19 + v0.23; no verdict)
        e1, _ = h1_test(en, lv, expl, SEEDS["descriptives"], n_perm, n_boot)
        e1.pop("verdict")
        out["exploratory"][f"E1_{lg}"] = e1
    out["joint_reading"] = joint_reading(h1v)
    # -------------------------------------------------------------------- descriptives (section 2.5; no verdicts)
    pairs = {}
    for a, b in (("es", "ko"), ("es", "zh"), ("ko", "zh")):
        keys = [u for u in trio if eligible(lv_all[a].get(u)) and eligible(lv_all[b].get(u))]
        x, y, g = _arrays(keys, lv_all[a], lv_all[b])
        pairs[f"{a}-{b}"] = {"n": len(keys), "rho_c": S62.rho_c(x, y, g) if len(keys) >= 3 else NAN}
    out["descriptives"]["D2_pairwise_language_rho_c"] = pairs
    if t1_il:
        keys = [u for u in trio if u in t1_il and eligible(en.get(u))]
        x = np.array([t1_il[k] for k in keys], float)
        y = np.array([en[k]["il"] for k in keys], float)
        g = np.array([k[0] for k in keys])
        out["descriptives"]["D3_benchmark_t1_vs_t4_EN"] = {"n": len(keys), "rho_c": S62.rho_c(x, y, g)}
    else:
        out["descriptives"]["D3_benchmark_t1_vs_t4_EN"] = {"status": "NOT AVAILABLE"}
    counts = {}
    for lg in LANGS:
        c = collections.Counter()
        for u in trio:
            e, l = en.get(u), lv_all[lg].get(u)
            c[f"eligible_{u[0]}"] += int(eligible(e) and eligible(l))
            for tag, v in (("en", e), (lg, l)):
                if v is not None and np.isfinite(v["pi"]):
                    c[f"floor_{tag}"] += int(v["pi"] == 0.0)
                    c[f"ceiling_{tag}"] += int(v["pi"] == 1.0)
        mc = {f"{s}/{ch}": lv_all[lg][next(u for u in trio if u[0] == s)][f"n_{ch}"]
              for s in TRIO for ch in ("cat", "cult") if any(u[0] == s for u in trio)}
        counts[lg] = {"counts": dict(c), "MC_Channel_answered_calls": mc}
    out["descriptives"]["D5_counts"] = counts
    out["descriptives"]["D4_home_language"] = {"status": "uses v0.62's country column (v0.62 section 2.9 item 5) "
                                                         "when it exists; NOT AVAILABLE in this skeleton"}
    return out


# =========================================================================== synthetic v0.62-shaped data (dry run, tests)
COI_NAMES = {"v0.19": ["Denon"], "v0.20": ["Eucerin"], "v0.22": ["BMW", "Bentley", "Chevrolet"],
             "v0.23": ["Jack Daniel's"]}
SIZES = {"v0.19": 16, "v0.20": 24, "v0.21": 24, "v0.22": 24, "v0.23": 24}


def synthetic_units():
    units = []
    for s, n in SIZES.items():
        names = list(COI_NAMES.get(s, []))
        names += [f"{s}-B{i:02d}" for i in range(1, n - len(names) + 1)]
        units += [(s, b) for b in names]
    return units


def _sig(z):
    return 1.0 / (1.0 + np.exp(-z))


def synthetic_world(seed, units, cmap, spec, drop=None):
    """spec: {lang: {'r': latent IL correlation with EN, 'kappa': presence change per unit of latent IL,
    'shift': logit added to cultural-channel questions}}; drop: {lang: (model, share of calls removed)}.
    Returns (en_rows, {lang: rows}) in v0.62's coded Phase B shape. Synthetic only; no archive is read."""
    rng = np.random.default_rng(seed)
    a = {u: rng.normal(-1.2, 1.0) for u in units}
    d = {u: rng.normal(0.0, 1.0) for u in units}

    def rows_for(tag, a_, d_, shift, drop_spec):
        rows = []
        for m in MODELS:
            for run in RUNS:
                for (s, fr), ch in sorted(cmap.items()):
                    cid = f"{tag}|{m}|{run}|{s}|{fr}"
                    if drop_spec and drop_spec[0] == m and rng.random() < drop_spec[1]:
                        continue
                    for (us, b) in units:
                        if us != s:
                            continue
                        z = a_[(us, b)] + (0.8 if ch == "cult" else -0.8) * d_[(us, b)] + (shift if ch == "cult" else 0)
                        rows.append({"call_id": cid, "substrate": s, "brand": b, "model": m, "condition": "S0",
                                     "run": str(run), "probe_id": fr, "frame_id": fr,
                                     "mentioned": str(int(rng.random() < _sig(z)))})
        return rows

    en_rows = rows_for("en", a, d, 0.0, None)
    lang_rows = {}
    for lg in LANGS:
        sp = spec.get(lg, {})
        r = sp.get("r", 0.95)
        dl = {u: r * d[u] + math.sqrt(max(0.0, 1 - r * r)) * rng.normal() for u in units}
        al = {u: a[u] + sp.get("kappa", 0.0) * d[u] for u in units}
        lang_rows[lg] = rows_for(lg, al, dl, sp.get("shift", 0.0), (drop or {}).get(lg))
    return en_rows, lang_rows


DRY_SCENARIOS = [
    ("A portable", {}, None),
    ("B language-bound in KO", {"ko": {"r": 0.0}}, None),
    ("C cultural shift in ZH", {"zh": {"shift": 1.0}}, None),
    ("D moderation in ES", {"es": {"kappa": -1.0}}, None),
    ("E drop rule in ES", {}, {"es": ("gemini-4-argon", 0.20)}),
]


def dry_run(n_perm=2000, n_boot=2000, path=None):
    cmap, dmap = channel_map(), drift_map()
    units = synthetic_units()
    lines = [f"v0.65 dry run (synthetic v0.62-shaped data only; no archive answer read); n_perm = {n_perm}, "
             f"n_boot = {n_boot} (the real run uses {N_PERM:,} each)"]
    results = {}
    for (name, spec, drop), seed in zip(DRY_SCENARIOS, SEEDS["dry_run"]):
        en_rows, lang_rows = synthetic_world(seed, units, cmap, spec, drop)
        res = score(units, en_rows, lang_rows, cmap, dmap, n_perm=n_perm, n_boot=n_boot)
        results[name] = res
        lines.append(f"\n[{name}] seed {seed}; joint reading: {res['joint_reading']}")
        for lg in LANGS:
            t1 = res["tests"][f"H1_IL_Order_{lg}"]
            t2 = res["tests"][f"H2_IL_Moderates_Language_{lg}"]
            t3 = res["tests"][f"H3_IL_Shift_{lg}"]
            coi = res["sensitivities"][lg]["S-COI"]["H1"]
            lines.append(f"  {lg}: H1 n={t1['n']} rho_c={t1['rho_c']:.3f} p={t1['p_perm_one_sided']:.4f} -> {t1['verdict']}"
                         f" | H2 n={t2['n']} rho_partial={t2['rho_partial']:.3f} -> {t2['verdict']}"
                         f"{' (' + t2['label'] + ')' if t2['label'] else ''}"
                         f" | H3 delta={t3['delta_IL']:+.4f} CI=[{t3['ci95'][0]:+.4f}, {t3['ci95'][1]:+.4f}] -> {t3['verdict']}"
                         f" | S-COI H1 n={coi['n']} {coi['verdict']}")
    text = "\n".join(lines) + "\n"
    if path:
        Path(path).write_text(text, encoding="utf-8")
    return results, text


def power(n_worlds=500, path=None, seed=None):
    """Operating characteristics over many synthetic worlds (invented generative model; not a prediction for v0.62).
    H1: P(CONFIRMED), P(FALSIFIED) by latent IL correlation r. With n ~ 70 and rho_c >= 0.50 the permutation p is
    far below .05, so H1 is read from rho_c and n (p not computed here). H3: P(verdict) by cultural shift (logit) at
    r = 0.9, bootstrap 1,000. Language ES only; the other two languages are generated and ignored."""
    cmap = channel_map()
    units = synthetic_units()
    trio = [u for u in units if u[0] in TRIO]
    seed = SEEDS["power"] if seed is None else seed
    rng = np.random.default_rng(seed)
    out = {"n_worlds": n_worlds, "seed": seed, "H1_by_r": {}, "H3_by_shift_at_r_0.9": {}}
    for r in (0.3, 0.5, 0.7, 0.8, 0.9, 0.95):
        c = collections.Counter()
        for _ in range(n_worlds):
            en_rows, lr = synthetic_world(int(rng.integers(1 << 31)), units, cmap, {"es": {"r": r}})
            en, lv = il_values(en_rows, units, cmap), il_values(lr["es"], units, cmap)
            keys = [u for u in trio if eligible(en[u]) and eligible(lv[u])]
            x, y, g = _arrays(keys, en, lv)
            rho = S62.rho_c(x, y, g)
            c["CONFIRMED" if (len(keys) >= N_FLOOR and rho >= H1_BARS[0]) else
              "UNDETERMINED" if len(keys) < N_FLOOR else "FALSIFIED" if rho < H1_BARS[1] else "MARGINAL"] += 1
            c["rho_c_sum"] += rho
        out["H1_by_r"][str(r)] = {k: (v / n_worlds) for k, v in c.items()}
    for shift in (0.0, 0.25, 0.5, 1.0):
        c = collections.Counter()
        for _ in range(n_worlds):
            en_rows, lr = synthetic_world(int(rng.integers(1 << 31)), units, cmap, {"es": {"r": 0.9, "shift": shift}})
            en, lv = il_values(en_rows, units, cmap), il_values(lr["es"], units, cmap)
            keys = [u for u in trio if eligible(en[u]) and eligible(lv[u])]
            c[h3_test(en, lv, keys, int(rng.integers(1 << 31)), 1000)["verdict"]] += 1
        out["H3_by_shift_at_r_0.9"][str(shift)] = {k: v / n_worlds for k, v in c.items()}
    for v in out["H1_by_r"].values():
        v["mean_rho_c"] = v.pop("rho_c_sum")
    if path:
        Path(path).write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    return out


# =========================================================================== real inputs (read only by --run)
def _git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True, check=True).stdout


def en_blob_ids():
    """Blob ids of t4's coded Phase B tables at EN_TAG (metadata only; no content read)."""
    return {raw: _git("rev-parse", f"{EN_TAG}:osf/v42/data/coded/{raw}_phase_b.csv").strip() for raw in EN_BLOBS}


def read_en_rows():
    got = en_blob_ids()
    if got != EN_BLOBS:
        raise SystemExit(f"HALT: t4 coded tables differ from the pinned blobs: {got}")
    rows = []
    for raw in EN_BLOBS:
        rows += list(csv.DictReader(io.StringIO(_git("show", f"{EN_TAG}:osf/v42/data/coded/{raw}_phase_b.csv"))))
    return rows


def read_lang_rows():
    return {lg: S62.read_coded_b(V62_CODED / lg) for lg in LANGS}


def read_t1_il(path=V17_CPC):
    """IL-Direct at t1 for the trio, exactly as score_v0_37.load_il_direct (R_cult_total - R_cat_total); also returns
    v0.37's hash of the consumed columns so it can be compared with osf/v37/.v37_il_direct_baseline.sha256."""
    out, hrows = {}, []
    with open(path, encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    for r in rows:
        if r["substrate"] in TRIO:
            out[(r["substrate"], r["brand"])] = float(r["R_cult_total"]) - float(r["R_cat_total"])
            hrows.append(f"{r['substrate']}|{r['brand']}|{r['R_cat_total']}|{r['R_cult_total']}")
    return out, hashlib.sha256("\n".join(sorted(hrows)).encode()).hexdigest()


def tag_on_origin(tag=PREREG_TAG):
    try:
        return bool(_git("ls-remote", "--tags", "origin", tag).strip())
    except Exception:
        return False


def guard_run(tag_ok=None, v62_scored=None, outputs_exist=None, manifest_ok=None):
    """--run refuses unless: the tag is on origin; v0.62 has been scored (its own single run comes first);
    the lock manifest verifies; no v0.65 output exists yet (one run only). Returns the list of refusals."""
    tag_ok = tag_on_origin() if tag_ok is None else tag_ok
    v62_scored = V62_VERDICTS.exists() if v62_scored is None else v62_scored
    outputs_exist = VERDICTS.exists() if outputs_exist is None else outputs_exist
    manifest_ok = (verify_manifest(MANIFEST) == []) if manifest_ok is None else manifest_ok
    no = []
    if not tag_ok:
        no.append(f"tag {PREREG_TAG} not on origin")
    if not v62_scored:
        no.append("v0.62 not yet scored (osf/v62/v62_verdicts.json missing)")
    if outputs_exist:
        no.append("v0.65 outputs already exist (the scoring runs once)")
    if not manifest_ok:
        no.append("lock manifest does not verify")
    return no


# =========================================================================== lock manifest
MANIFEST_FILES = [
    "osf/v65/prereg/PRE_REGISTRATION_v0_65_DRAFT_r0.md",
    "osf/v65/anchor/DEVIATIONS.md",
    "osf/v65/README.md",
    "osf/v65/scripts/score_v0_65.py",
    "osf/v65/scripts/test_score_v0_65.py",
    "osf/v65/prereg/dry_run_v0_65_r0.txt",
    "osf/v65/prereg/power_v0_65_r0.json",
    # read or imported unchanged from v0.62's lock (same blobs as at e449b6c)
    "osf/v62/scripts/score_v0_62.py",
    "osf/v62/scripts/params_v0_62.py",
    "osf/v62/inputs/probes_v0_42.jsonl",
    "osf/v62/translations/translations_v0_62_r2.json",
    "osf/v62/prereg/PRE_REGISTRATION_v0_62.md",
    # t1 identity load (descriptive D3)
    "osf/methodology/v1_7/data/v1_7_cpc.csv",
    "osf/v37/.v37_il_direct_baseline.sha256",
]


def _sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def write_manifest(path, files=None, root=None):
    root = Path(root) if root else ROOT
    files = MANIFEST_FILES if files is None else files
    lines = [f"{_sha(root / f)}  {f}" for f in files]
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return lines


def verify_manifest(path, root=None):
    """Returns the list of problems ([] = OK)."""
    root = Path(root) if root else ROOT
    if not Path(path).exists():
        return [f"missing manifest {path}"]
    bad = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        h, f = line.split("  ", 1)
        if not (root / f).exists():
            bad.append(f"missing {f}")
        elif _sha(root / f) != h:
            bad.append(f"changed {f}")
    return bad


def _clean(o):
    if isinstance(o, dict):
        return {str(k) if not isinstance(k, tuple) else "/".join(k): _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    if isinstance(o, float) and not math.isfinite(o):
        return None
    if isinstance(o, np.generic):
        return _clean(o.item())
    return o


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--lock-manifest", metavar="PATH")
    ap.add_argument("--verify-lock", metavar="PATH")
    ap.add_argument("--power", action="store_true")
    ap.add_argument("--run", action="store_true")
    a = ap.parse_args(argv)
    if a.dry_run:
        _res, text = dry_run(path=V65 / "prereg/dry_run_v0_65_r0.txt")
        print(text)
    elif a.power:
        print(json.dumps(power(path=V65 / "prereg/power_v0_65_r0.json"), indent=2))
    elif a.lock_manifest:
        print("\n".join(write_manifest(a.lock_manifest)))
    elif a.verify_lock:
        bad = verify_manifest(a.verify_lock)
        print("lock manifest OK" if not bad else "\n".join(bad))
        return 1 if bad else 0
    elif a.run:
        no = guard_run()
        if no:
            print("REFUSED: " + "; ".join(no))
            return 2
        en_rows = read_en_rows()
        units = sorted({(canon_sub(r["substrate"]), r["brand"]) for r in en_rows})
        assert len(units) == 112, f"expected 112 registry units, found {len(units)}"
        t1_il, t1_hash = read_t1_il()
        base = ROOT / "osf/v37/.v37_il_direct_baseline.sha256"
        if t1_hash != base.read_text().strip():
            raise SystemExit("HALT: t1 IL-Direct source differs from v0.37's baseline hash")
        res = score(units, en_rows, read_lang_rows(), channel_map(), drift_map(), t1_il=t1_il)
        res["t1_il_hash"] = t1_hash
        VERDICTS.parent.mkdir(parents=True, exist_ok=True)
        VERDICTS.write_text(json.dumps(_clean(res), indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {VERDICTS}")
    else:
        ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
