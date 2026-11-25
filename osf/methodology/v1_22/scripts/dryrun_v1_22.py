#!/usr/bin/env python3
"""v1.22 keyless dry run (pre-registration section 11; draft r1, 2026-11-25).

Synthetic worlds only, on t4's real design (the 112 v1.13 units with their D_b status, v1.19's frozen F / D flags,
v0.42's 30 Phase B questions with their channel labels, N3 x 3 runs x 2 waves). The few parameters taken from data
are Paper A's PUBLISHED aggregates (v1_13_verdicts.json: MQ2 search-use share per model, the baseline class mix and
domains per answer per model) and the list of units that carry an SDRI (values are synthetic). No answer text, no
source record and no statistic of t4 or t5 is read. No network, no key, no model call.

Worlds (seeds 122490-122494): null, effects, paperA_like, thin_s1, c5 (+ t6 for Stage 2 in the effects world).
Also: the not-run paths of section 1, the refusal guards, B-P1 on a synthetic Paper A output written by v1.13's
own functions, the exhaustive GB table, and a calibration batch for the #47 / #48 bands (C9).
"""
import argparse
import collections
import itertools
import json
import math
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import score_v1_22 as S  # noqa: E402

A = S.A
TYPE_TILT = np.array([[1.0, 0.0, 0.0, 1.0, 0.0, 0.0],       # type 0: reference + news
                      [0.0, 0.0, 0.0, 0.0, 1.0, 1.0],       # type 1: review/editorial + retailer
                      [0.0, 0.0, 1.0, 0.0, 0.0, 0.0]])      # type 2: forum / UGC
BASE = dict(rho_gp=0.0, retest=0.0, beta_F=0.0, beta_sdri=0.0, ch_pts=0.0, beta_il=0.0, type_tilt=0.0,
            pi_shift=0.0, gem_search=None, drop_t5=None, c5=False, t6=False, brand_src=1)
WORLDS = {
    "null": (122490, {}),
    "effects": (122491, dict(rho_gp=0.1, retest=0.95, beta_F=1.0, beta_sdri=1.0, ch_pts=8.0, beta_il=-0.6,
                             type_tilt=3.0, brand_src=3, t6=True)),
    "paperA_like": (122492, dict(rho_gp=0.35, retest=0.6, pi_shift=-0.9)),
    "thin_s1": (122493, dict(rho_gp=0.2, retest=0.7, gem_search=0.18, drop_t5="gpt-6-astra")),
    "c5": (122494, dict(rho_gp=0.1, retest=0.9, c5=True)),
}


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def published_params():
    d = json.loads(S.V113_VERDICTS.read_text(encoding="utf-8"))
    base = d["baseline"]["per_substrate_model"]
    mix, dom = {}, {}
    for m in S.N3:
        rows = [v for k, v in base.items() if k.endswith("|" + m)]
        mix[m] = {c: float(np.mean([r["mix"].get(c) or 0.0 for r in rows])) for c in A.CLASS_ORDER}
        g = sum(r["grounded"] for r in rows)
        dom[m] = sum(r["domains_per_answer"] * r["answers"] for r in rows) / g if g else 5.0
    return {"search_share": {m: v["share"] for m, v in d["MQ"]["MQ2"].items()}, "class_mix": mix,
            "domains_per_grounded_answer": dom,
            "source": "osf/methodology/v1_13/v1_13_verdicts.json (published aggregates only)"}


class Design:
    def __init__(self):
        self.units = A.load_brand_domains()
        self.keys = sorted(self.units)
        self.flags = S.roster_flags(self.units)
        self.channels, self.labels = S.load_channels()
        self.questions = sorted(self.channels)
        self.params = published_params()
        self.sdri_keys = sorted(k for k, v in A.read_sdri(S.V113_SDRI, self.units).items() if S._f(v))


def make_world(design, seed, **kw):
    cfg = dict(BASE, **kw)
    rng = np.random.default_rng(seed)
    units, keys = design.units, design.keys
    idx = {k: i for i, k in enumerate(keys)}
    n = len(keys)
    Fv = np.array([design.flags[k]["F"] for k in keys], float)
    trio = np.array([k[0] in S.TRIO for k in keys], float)
    zP = rng.normal(size=n) - 0.8 * Fv
    zS, zIL, zC = rng.normal(size=n), rng.normal(size=n), rng.normal(size=n)
    types = rng.integers(0, 3, n)
    structural = cfg["rho_gp"] * zP + cfg["beta_F"] * Fv + cfg["beta_sdri"] * zS + cfg["beta_il"] * zIL * trio
    r = cfg["retest"]
    u = {"t4": rng.normal(size=n)}
    u["t5"] = r * u["t4"] + math.sqrt(1 - r * r) * rng.normal(size=n)
    u["t6"] = r * u["t5"] + math.sqrt(1 - r * r) * rng.normal(size=n)
    pi = sigmoid(-1.0 + cfg["pi_shift"] + 1.1 * zP)
    mix6 = {m: np.array([design.params["class_mix"][m][c] for c in S.PROFILE_CLASSES]) + 1e-3 for m in S.N3}
    gen_cls = [c for c in A.CLASS_ORDER if c != "brand_owned"]
    gen_p = {m: np.array([design.params["class_mix"][m][c] for c in gen_cls]) + 1e-3 for m in S.N3}
    waves = {}
    for w in (("t4", "t5", "t6") if cfg["t6"] else ("t4", "t5")):
        zG = structural + u[w]
        q = sigmoid(-1.2 + 0.9 * zG)
        answers, answered = [], collections.Counter()
        for m in S.N3:
            share = cfg["gem_search"] if (m == A.GEM4 and cfg["gem_search"] is not None) else \
                design.params["search_share"][m]
            for run in (1, 2, 3):
                for (sub, pid) in design.questions:
                    if w == "t5" and cfg["drop_t5"] == m and rng.random() < 0.25:
                        continue
                    answered[m] += 1
                    ch = design.channels[(sub, pid)]
                    sub_keys = [k for k in keys if k[0] == sub]
                    named = {k for k in sub_keys if rng.random() < pi[idx[k]]}
                    srcs = []
                    if rng.random() < share:
                        p = gen_p[m] / gen_p[m].sum()
                        for _ in range(max(1, rng.poisson(min(design.params["domains_per_grounded_answer"][m], 12)
                                                         * 0.5))):
                            c = gen_cls[rng.choice(len(gen_cls), p=p)]
                            dom = None if c == "unresolved" else f"{c}{int(rng.integers(0, 80))}.example"
                            srcs.append(
                                {"key": ("unresolved", f"u{len(srcs)}") if dom is None else (dom, "/"),
                                 "domain": dom, "cls": c, "redirect": False, "via_title": False})
                        for k in sorted(named):
                            i = idx[k]
                            qq = q[i] + (cfg["ch_pts"] / 200.0) * (1 if ch == "cat" else -1)
                            if units[k]["status"] == "RESOLVED" and rng.random() < min(max(qq, 0.0), 1.0):
                                d = sorted(units[k]["domains"])[0]
                                srcs.append({"key": (d, "/"), "domain": d, "cls": "brand_owned", "redirect": False,
                                             "via_title": False})
                            wt = mix6[m] * np.exp(cfg["type_tilt"] * TYPE_TILT[types[i]])
                            for _j in range(cfg["brand_src"]):
                                c = S.PROFILE_CLASSES[rng.choice(6, p=wt / wt.sum())]
                                if c != "brand_owned":
                                    d = f"{c}-b{i}-{int(rng.integers(0, 6))}.example"
                                    srcs.append({"key": (d, "/"), "domain": d, "cls": c, "redirect": False,
                                                 "via_title": False})
                    seen, uniq = set(), []
                    for s in srcs:
                        if s["key"] not in seen:
                            seen.add(s["key"])
                            uniq.append(s)
                    src = "C5" if (cfg["c5"] and w == "t5" and run in (2, 3)) else "wave"
                    answers.append({"call_id": f"{w}|{sub}|{pid}|{m}|S1|{run}", "substrate": sub, "model": m,
                                    "provider": None, "run": run, "named": named, "sources": uniq, "channel": ch,
                                    "wave": w, "source": src})
        dropped = [m for m in S.N3 if answered[m] < S.ANSWERED_MIN * S.S1_CALLS_PER_MODEL]
        mq2 = A.mq2_search_use(answers, S.N3)
        dropped += [m for m in S.N3 if mq2[m]["dropped_from_g_star"] and m not in dropped]
        models = [m for m in S.N3 if m not in dropped]

        def pmap(off):
            v = 100 * sigmoid(0.3 + 1.1 * zP + 0.25 * rng.normal(size=n) + off)
            return {k: float(v[idx[k]]) for k in keys}

        def cmap():
            v = np.clip(50 + 15 * zC + 5 * rng.normal(size=n), 0, 100)
            return {k: float(v[idx[k]]) for k in keys}
        waves[w] = {"label": w, "answers": [a for a in answers if a["model"] in models], "models": models,
                    "dropped": dropped, "answered_by_model": dict(answered), "answers_cited": None,
                    "P": {"S0": pmap(0.0), "S1": pmap(0.2)}, "C": {"S0": cmap(), "S1": cmap()}}
    sdri = {k: float(np.clip(40 + 20 * zS[idx[k]], 0, 100)) for k in design.sdri_keys}
    il = {k: {"il": float(0.3 * zIL[idx[k]]), "pi_hat": float(min(max(pi[idx[k]], 0.02), 0.98))}
          for k in keys if k[0] in S.TRIO}
    inp = {"units": units, "flags": design.flags, "il": il, "sdri": sdri, "waves": {w: waves[w] for w in ("t4", "t5")},
           "paper_a_verdict": "MARGINAL",
           "decision": {"go": True, "date": "2026-11-25", "text": "synthetic dry-run decision record"}}
    return inp, waves.get("t6"), cfg


# =========================================================================== checks around the worlds
def synthetic_paper_a(inp):
    """A Paper-A verdict document written by v1.13's own gate_statistics on the synthetic t4 (B-P1's synthetic arm)."""
    w4 = inp["waves"]["t4"]
    r = A.gate_statistics(w4["answers"], inp["units"], w4["P"], w4["C"], n_perm=0, n_boot=0)
    return {"panel_models": w4["models"], "units": {f"{k[0]}|{k[1]}": v for k, v in r["stats"].items()},
            "legs": r["legs"]}


def not_run_paths(inp):
    out = {}
    for name, dec, verdict in (("no decision", None, "MARGINAL"),
                               ("undated decision", {"go": True, "text": "ok"}, "MARGINAL"),
                               ("declined", {"go": False, "date": "2026-11-25", "text": "no"}, "MARGINAL")):
        doc = S.stage1(dict(inp, decision=dec, paper_a_verdict=verdict), n_perm=10, n_boot=0, gap_b=5,
                       with_sensitivities=False)
        out[name] = {"status": doc["status"], "statistics": doc["statistics"]}
    try:
        S.stage1(dict(inp, paper_a_verdict="PASS"), n_perm=10, with_sensitivities=False)
        out["Paper A PASS"] = "NOT REFUSED (error)"
    except S.Refused as e:
        out["Paper A PASS"] = f"refused: {e}"
    return out


def guards():
    """Offline: the origin lookup is replaced by the LOCAL tag list (no network in the dry run); before the lock
    neither has tag v1.22-prereg-r1, so the guard must refuse."""
    out = {}
    orig = S.tag_commit_on_origin

    def local_only(tag):
        c = S.git("rev-parse", "--verify", "--quiet", f"refs/tags/{tag}^{{commit}}")
        return c.decode().strip() if c else None
    S.tag_commit_on_origin = local_only
    try:
        S.guard_stage(1, "0" * 40)
        out["guard_stage_1"] = "PASSED (unexpected before the lock)"
    except S.Refused as e:
        out["guard_stage_1"] = f"refused: {e}"
    finally:
        S.tag_commit_on_origin = orig
    S._GUARD["passed"] = None
    try:
        S.load_wave_real("t5", "/nonexistent/t5_raw.jsonl", "/nonexistent", "/nonexistent", {}, {}, {})
        out["load_t5_without_guard"] = "READ (error)"
    except S.Refused as e:
        out["load_t5_without_guard"] = f"refused: {e}"
    return out


def gb_table():
    V = (S.C, S.M, S.F, S.U)
    cnt = collections.Counter(S.gate_completion(*c) for c in itertools.product(V, repeat=4))
    return {"combinations": 4 ** 4, "by_outcome": dict(cnt)}


def summarise(doc):
    r = doc["results"]
    pick = {}
    for h in ("HB1", "HB4"):
        if h in r:
            pick[h] = {"rho_w_S1": r[h]["legs"][0]["rho_w"], "rho_w_S0": r[h]["legs"][1]["rho_w"],
                       "n": [r[h]["legs"][0]["n"], r[h]["legs"][1]["n"]]}
    if "HB2" in r:
        pick["HB2"] = {k: r["HB2"].get(k) for k in ("rho_pw", "p_perm_one_sided", "n", "ci95", "v045_verdict")}
    if "HB3" in r:
        pick["HB3"] = {"pairs_n": [p["n"] for p in r["HB3"]["pairs"]], "rel3": r["HB3"]["rel3"], "p": r["HB3"]["p"]}
    for h, ks in (("HB44", ("rho_w", "p", "n")), ("HB44b", ("rho_w", "p", "n")),
                  ("HB46", ("delta", "p", "n_F", "n_nonF")), ("HB46b", ("delta", "p", "n_F", "n_nonF")),
                  ("HB47", ("dbar", "p", "n", "min_category_units")), ("HB47b", ("rho_w", "p", "n")),
                  ("HB48", ("R", "p", "n"))):
        pick[h] = {k: r[h].get(k) for k in ks}
    t = r.get("HB48b", {})
    pick["HB48b"] = {k: t.get(k) for k in ("cell", "n")}
    if "full" in t:
        pick["HB48b"].update(k=t["full"]["k"], silhouette=t["full"]["silhouette"], ari=t["ari_vs_presence_tiers"])
    return {"verdicts": doc["verdicts"], "rated": r["rated"], "panel_t5": r["panel_t5"],
            "reduced_panel": r["reduced_panel"], "statistics": pick,
            "verdict_changes_in_sensitivities": doc.get("verdict_changes"),
            "sensitivities_not_available": (doc.get("sensitivities") or {}).get("_not_available")}


# =========================================================================== calibration of the #47 / #48 bands (C9)
def calibration(design, n_worlds, n_perm, log=print):
    out = {"n_worlds_per_cell": n_worlds, "n_perm": n_perm, "HB47_by_channel_points": {}, "HB48_by_type_tilt": {}}
    base_seed = 1224900
    for pts in (0.0, 2.0, 5.0, 8.0):
        cnt, dbars = collections.Counter(), []
        for i in range(n_worlds):
            inp, _, _ = make_world(design, base_seed + i, rho_gp=0.1, retest=0.9, ch_pts=pts)
            ap = inp["waves"]["t4"]["answers"] + inp["waves"]["t5"]["answers"]
            r = S.hb47(ap, inp["units"], S.SEEDS["HB47"], n_perm)
            cnt[r["verdict"]] += 1
            dbars.append(r["dbar"])
        out["HB47_by_channel_points"][str(pts)] = {"verdicts": dict(cnt), "mean_dbar": float(np.mean(dbars)),
                                                   "sd_dbar": float(np.std(dbars, ddof=1))}
        log(f"  calibration HB47 {pts} pts: {dict(cnt)}")
    for tilt in (0.0, 1.0, 2.0, 3.0):
        cnt, Rs = collections.Counter(), []
        for i in range(n_worlds):
            inp, _, _ = make_world(design, base_seed + 1000 + i, rho_gp=0.1, retest=0.9, type_tilt=tilt,
                                   brand_src=3)
            w4, w5 = inp["waves"]["t4"], inp["waves"]["t5"]
            g4, _ = S.gstar(w4["answers"], inp["units"])
            g5, _ = S.gstar(w5["answers"], inp["units"])
            r = S.hb48(S.profiles(w4["answers"], inp["units"]), S.profiles(w5["answers"], inp["units"]), g4, g5,
                       S.SEEDS["HB48"], n_perm)
            cnt[r["verdict"]] += 1
            Rs.append(r["R"])
        out["HB48_by_type_tilt"][str(tilt)] = {"verdicts": dict(cnt), "mean_R": float(np.mean([x for x in Rs if x is not None]))}
        log(f"  calibration HB48 tilt {tilt}: {dict(cnt)}")
    out["HB46_by_phantom_shift_sd"] = {}           # #46 keeps v1.19's bands (not C9); measured for the record
    for shift in (0.0, 0.5, 1.0, 1.5):
        cnt, ds = collections.Counter(), []
        for i in range(n_worlds):
            inp, _, _ = make_world(design, base_seed + 2000 + i, rho_gp=0.1, retest=0.9, beta_F=shift)
            ap = inp["waves"]["t4"]["answers"] + inp["waves"]["t5"]["answers"]
            gp, _ = S.gstar(ap, inp["units"])
            r = S.hb46(gp, inp["flags"], S.SEEDS["HB46"], n_perm)
            cnt[r["verdict"]] += 1
            ds.append(r["delta"])
        out["HB46_by_phantom_shift_sd"][str(shift)] = {"verdicts": dict(cnt),
                                                      "mean_delta": float(np.mean([x for x in ds if x is not None]))}
        log(f"  calibration HB46 shift {shift}: {dict(cnt)}")
    return out


# =========================================================================== driver
def pass_conditions(res):
    w = {k: v["summary"]["verdicts"] for k, v in res["worlds"].items()}
    eff = w["effects"]
    built = {"HB2": eff["HB2"] == S.C, "HB44": eff["HB44"] == S.C, "HB46": eff["HB46"] == S.C,
             "HB47": eff["HB47"] == S.C, "HB48": eff["HB48"] == S.C,
             "HB48b typology": not str(eff.get("HB48b", "")).startswith("NO TYPOLOGY"),
             "HB45 (Stage 2)": all(v == S.C for v in res["worlds"]["effects"]["stage2"]["verdicts"].values())}
    null = w["null"]
    return {"effects_world_returns_each_built_effect": built,
            "null_world_no_CONFIRMED_on_structure_tests": {h: null[h] != S.C for h in ("HB44", "HB46", "HB47",
                                                                                         "HB48")},
            "null_world_GB_MARGINAL_or_FAIL": null["GB"] in ("MARGINAL", "FAIL"),
            "paperA_like_HB3_UNDETERMINED": w["paperA_like"]["HB3"] == S.U,
            "thin_world_reduced_panel": res["worlds"]["thin_s1"]["summary"]["reduced_panel"],
            "c5_world_S-C5_computed": "S-C5" not in (res["worlds"]["c5"]["summary"]["sensitivities_not_available"]
                                                     or []),
            "not_run_paths_write_no_statistic": all(isinstance(v, str) or v["statistics"] is None
                                                    for v in res["not_run_paths"].values()),
            "B-P1_synthetic": res["worlds"]["paperA_like"]["B-P1_synthetic"]["passed"],
            "guards_refuse_before_lock": all(v.startswith("refused") for v in res["guards"].values())}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--draws", type=int, default=S.N_PERM)
    ap.add_argument("--gap-b", type=int, default=S.GAP_B)
    ap.add_argument("--worlds", nargs="*", default=list(WORLDS))
    ap.add_argument("--calib-worlds", type=int, default=40)
    ap.add_argument("--calib-draws", type=int, default=1000)
    ap.add_argument("--no-sensitivities", action="store_true")
    ap.add_argument("--name", default="dry_run_v1_22_r1.json")
    a = ap.parse_args(argv)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    design = Design()
    res = {"phase": S.PHASE_ID, "kind": "keyless synthetic dry run (section 11)", "started_utc":
           datetime.now(timezone.utc).isoformat(), "scorer_sha256": S.sha256_file(S.__file__),
           "dryrun_sha256": S.sha256_file(__file__), "draws": {"permutation": a.draws, "gap_references": a.gap_b},
           "published_parameters": design.params, "design": {
               "units": len(design.units), "F_flags": sum(v["F"] for v in design.flags.values()),
               "D_flags": sum(v["D"] for v in design.flags.values()), "questions": len(design.questions),
               "channel_labels": dict(collections.Counter(design.labels.values())),
               "units_with_sdri": len(design.sdri_keys)}, "worlds": {}}
    for name in a.worlds:
        seed, kw = WORLDS[name]
        t1 = time.time()
        inp, t6, cfg = make_world(design, seed, **kw)
        doc = S.stage1(inp, a.draws, S.N_BOOT, a.gap_b, not a.no_sensitivities,
                       out_dir=out / f"_hb2_{name}")
        rec = {"seed": seed, "config": cfg, "summary": summarise(doc), "seconds": round(time.time() - t1, 1)}
        if t6 is not None:
            gs = {w: S.gstar(x["answers"], inp["units"])[0] for w, x in (("t4", inp["waves"]["t4"]),
                                                                       ("t5", inp["waves"]["t5"]), ("t6", t6))}
            st2 = S.stage2(gs["t4"], gs["t5"], gs["t6"], inp["units"], a.draws, 1000)
            rec["stage2"] = {"verdicts": st2["verdicts"],
                             "rho": {h: st2[h]["rho_pw"] for h in ("HB45_t5t6", "HB45_t4t6")},
                             "n": {h: st2[h]["n"] for h in ("HB45_t5t6", "HB45_t4t6")}}
        if name == "paperA_like":
            rec["B-P1_synthetic"] = S.b_p1(inp["waves"]["t4"], inp["units"], synthetic_paper_a(inp))
            res["not_run_paths"] = not_run_paths(inp)
        write_full = out / f"world_{name}_v1_22_r1.json"
        S.write_json(write_full, doc)
        rec["full_output"] = write_full.name
        rec["full_output_sha256"] = S.sha256_file(write_full)
        res["worlds"][name] = rec
        print(f"{name}: {rec['summary']['verdicts']} ({rec['seconds']} s)", flush=True)
    res["guards"] = guards()
    res["gb_table"] = gb_table()
    if a.calib_worlds:
        res["calibration_C9"] = calibration(design, a.calib_worlds, a.calib_draws)
    if set(WORLDS) <= set(res["worlds"]):
        res["pass_conditions"] = pass_conditions(res)
    res["seconds_total"] = round(time.time() - t0, 1)
    S.write_json(out / a.name, res)
    print(json.dumps(S._jsonable(res.get("pass_conditions")), indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
