#!/usr/bin/env python3
"""
make_scenarios_v1_11.py -- SYNTHETIC scorer outputs for the v1.11 Sentiment Paper A pipeline. SYNTHETIC DATA ONLY.

Base ("scored"): the locked scorer's own Stage J and Stage C outputs from its end-to-end dry run on synthetic replicas
(osf/methodology/v1_11/dryrun/: build_dryrun_v1_11.py replicas, a fake judge and a fake batch service, then
`score_v1_11.py --stage J --dry-run` and `--stage C --dry-run`, 2026-11-10; no real answer, judge call, P, C* or
Ranking value). Those four files are committed as tests/fixtures/SYNTHETIC_base_* (the SHA-256 of each source is in
BASE_SHA256 below). Every other scenario copies the base and gives some statistics other values; every verdict word
is then recomputed with the locked scorer's own functions (scripts/score_v1_11.py, imported read-only:
judge_agreement_verdict, separability_verdict / wave_abs_rho, stability_verdict, band_verdict, self_pref_verdict,
verdict_row, apply_noise_guard), and the sensitivity "verdict_changes" are recomputed the way run_stage_c does.

Files written per scenario, with the scorer's names and schemas, each marked "dry_run": true and "synthetic_fixture":
  OUT/<scenario>/v1_11_verdicts.json  stage_j_v1_11.json  judge_outputs_frozen_v1_11.json  plan_v1_11.json

  python3 papers/v1_11/tests/make_scenarios_v1_11.py OUT [scenario ...]

Scenarios (pre-registration section 5 branches):
  scored        the dry run's own result (H1 MARGINAL: every verdict carries the flag; H2-H9 CONFIRMED)
  confirmed     every hypothesis CONFIRMED
  h1_falsified  H1 FALSIFIED -> noise guard (H2, H3, H5, H7, H8 UNDETERMINED); H9 FALSIFIED (S without J1-provider
                answers reported)
  unstable      H4 FALSIFIED by its rho -> noise guard; H1 CONFIRMED
  marginal      MARGINAL rows (H1, H2, H4, H5, H7, H9), FALSIFIED rows without the guard (H3 at one wave, H6 by p,
                H8); a sensitivity (SD) changes H2
  mixed         MARGINAL rows without a falsified separability test (H2, H3, H4, H6, H8), H7 FALSIFIED; H1 CONFIRMED
  presence      H2 and H5 FALSIFIED at one wave (no guard); H6 FALSIFIED by its rho
  undetermined  every row UNDETERMINED by its floor (fewer than 2 determined waves, too few units); H5 PENDING
  inactive      as scored, H5 INACTIVE (tag v1.10-prereg-r2 not found by the scorer)
Refuses any OUT under osf/.
"""
import copy
import hashlib
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import score_v1_11 as S  # noqa: E402  (read-only: verdict functions and constants)

FIX = HERE / "fixtures"
NAMES = {"verdicts": "v1_11_verdicts.json", "stage_j": "stage_j_v1_11.json",
         "frozen": "judge_outputs_frozen_v1_11.json", "plan": "plan_v1_11.json"}
BASE_SHA256 = {  # the dry run's outputs (v1.11 worktree, osf/methodology/v1_11/dryrun/outputs/, 2026-11-10)
    "verdicts": "2fda34d9e91b6a1e3e7e564cf7d6dc3c2fb211d655584500097e5cca4e6baa32",
    "stage_j": "da4cbfca5148ea26753d2e030e01d056c5e4deddab76179688d53f34140d24fe",
    "frozen": "524e16bbb755d63ccad658a266ba95ce9f84db503ee02369f05c23ddf86e0df9",
    "plan": "1500aec390d59f799136bec2ed9aabcb1cf89a1f3c174c42206fb3b9b92d4050"}
SCENARIOS = ["scored", "confirmed", "h1_falsified", "unstable", "marginal", "mixed", "presence", "undetermined",
             "inactive"]
MARK = "SYNTHETIC TEST DATA - NOT RESULTS (papers/v1_11/tests/make_scenarios_v1_11.py, scenario {s})"
PRIM = ["H1_Judge_Agreement", "H2_Sep_Presence", "H3_Sep_Consistency", "H4_Stability_Short", "H6_Stability_Long",
        "H7_Naming_Frequency", "H8_Recognition_Sep", "H5_Sep_Ranking", "H5_secondary_early"]


def base_path(k):
    return FIX / f"SYNTHETIC_base_{NAMES[k]}"


def load_base():
    out = {}
    for k in NAMES:
        p = base_path(k)
        if hashlib.sha256(p.read_bytes()).hexdigest() != BASE_SHA256[k]:
            raise SystemExit(f"base fixture {p.name} differs from the dry run's output")
        out[k] = json.loads(p.read_text(encoding="utf-8"))
    return out


# --------------------------------------------------------------------------- statistics -> verdict words (scorer)
def _ci(r, half=0.22):
    return [max(-1.0, r - half), min(1.0, r + half)]


def set_wave(leg, w, rho=None, det=None, n=None):
    pw = leg["per_wave"][w]
    if rho is not None:
        pw["rho"], pw["ci95"] = rho, _ci(rho)
    if det is not None:
        pw["determinable"] = det
    if n is not None:
        pw["n"] = n


def set_pooled(leg, rho=None, det=None, n=None, p=None):
    if rho is not None:
        leg["rho"], leg["ci95"] = rho, _ci(rho, 0.18)
    if det is not None:
        leg["determinable"] = det
    if n is not None:
        leg["n"] = n
    if p is not None:
        leg["p_perm"] = p


def _nan(x):
    return float("nan") if x is None else float(x)


def reverdict(res):
    """Verdict words of one gate set (primary or a sensitivity) from its statistics, with the scorer's functions."""
    h1 = res.get("H1_Judge_Agreement")
    if h1 is not None:
        br = h1["brand_rho"]
        det = bool(br.get("determinable")) and h1["units_judged_by_both"] >= S.MIN_UNITS_POOLED
        h1["verdict"] = S.judge_agreement_verdict(_nan(h1["alpha_ordinal"]), _nan(br.get("rho")), det)
    for h in ("H2_Sep_Presence", "H3_Sep_Consistency", "H5_Sep_Ranking", "H8_Recognition_Sep"):
        if h in res:
            pw = res[h]["per_wave"]
            res[h]["verdict"] = S.separability_verdict(
                [S.wave_abs_rho({**pw[w], "rho": _nan(pw[w].get("rho"))}) for w in S.WAVES])
    for h in ("H4_Stability_Short", "H6_Stability_Long"):
        r = res[h]
        r["verdict"] = S.stability_verdict(_nan(r.get("rho")), _nan(r.get("p_perm")), bool(r.get("determinable")))
    for h in ("H7_Naming_Frequency", "H5_secondary_early"):
        if h in res:
            r = res[h]
            r["verdict"] = S.band_verdict(abs(_nan(r.get("rho")))) if r.get("determinable") else "UNDETERMINED"


def reverdict_h9(h9):
    h9["verdict"] = S.self_pref_verdict(_nan(h9.get("delta_points")), h9["n_own_provider"], h9["n_other"])


def finalize(src, scen):
    V, J = src["verdicts"], src["stage_j"]
    state = V["ranking"].get("status", "ACTIVE")
    reverdict(V)
    J["H1_Judge_Agreement"] = copy.deepcopy(V["H1_Judge_Agreement"])        # run_stage_c: H1 as written at Stage J
    reverdict_h9(V["H9_Self_Preference"])
    raw = S.verdict_row(V, V["H9_Self_Preference"], state)
    final, on = S.apply_noise_guard(raw)
    V["verdicts_before_noise_guard"], V["VERDICTS"], V["noise_guard_applied"] = raw, final, on
    V["H1_marginal_flag_on_all_verdicts"] = final["H1"] == "MARGINAL"
    sens = V["sensitivities"]
    changes = []
    for name in ("SU_uncentred_ranks", "SD_without_Denon_v0_19"):
        reverdict(sens[name])
        h9 = sens[name].get("H9_Self_Preference", V["H9_Self_Preference"])
        if "H9_Self_Preference" in sens[name]:
            reverdict_h9(h9)
        for h, val in S.verdict_row(sens[name], h9, state).items():
            if val != raw.get(h):
                changes.append({"sensitivity": name, "hypothesis": h, "primary": raw.get(h), "under_sensitivity": val})
    for name in ("S_NV_in_place_of_S", "S_model_balanced", "S_J2_scored", "S_without_J1_provider_answers"):
        for h in (sens.get(name) or {}).values():
            pw = h["per_wave"]
            h["verdict"] = S.separability_verdict(
                [S.wave_abs_rho({**pw[w], "rho": _nan(pw[w].get("rho"))}) for w in S.WAVES])
    if V["H9_Self_Preference"]["verdict"] == "FALSIFIED":
        sens.setdefault("S_without_J1_provider_answers", copy.deepcopy(sens["S_J2_scored"]))
    else:
        sens.pop("S_without_J1_provider_answers", None)
    sens["verdict_changes"] = changes
    for sc in (V["self_consistency"], J["self_consistency"]):
        for role in sc.values():
            for blk in role.values():
                blk["flag_below_0.90"] = blk["exact_valence_agreement"] < S.SELFCON_MIN_EXACT
    for k in src:
        if "dry_run" in src[k]:                    # the plan file has no dry_run field in the scorer's schema
            src[k]["dry_run"] = True
        src[k]["synthetic_fixture"] = MARK.format(s=scen)
    return src


def drop_h5(V, status, reason):
    for d in (V, V["sensitivities"]["SU_uncentred_ranks"], V["sensitivities"]["SD_without_Denon_v0_19"]):
        d.pop("H5_Sep_Ranking", None)
        d.pop("H5_secondary_early", None)
    V["ranking"] = {"status": status, "reason": reason}


# --------------------------------------------------------------------------- scenarios
def apply(src, scen):
    V = src["verdicts"]
    SU = V["sensitivities"]["SU_uncentred_ranks"]
    SD = V["sensitivities"]["SD_without_Denon_v0_19"]
    every = (V, SU, SD)
    if scen == "scored":
        pass
    elif scen == "confirmed":
        for d in every:
            d["H1_Judge_Agreement"]["alpha_ordinal"] = 0.742
            set_pooled(d["H1_Judge_Agreement"]["brand_rho"], rho=0.884)
    elif scen == "h1_falsified":
        for d in every:
            d["H1_Judge_Agreement"]["alpha_ordinal"] = 0.452
            set_wave(d["H2_Sep_Presence"], "t1", rho=0.41)
        for h9 in (V["H9_Self_Preference"], SD["H9_Self_Preference"]):
            h9["mean_diff_own"] = h9["mean_diff_other"] + 11.6
            h9["delta_points"] = 11.6
    elif scen == "unstable":
        for d in every:
            d["H1_Judge_Agreement"]["alpha_ordinal"] = 0.701
            set_pooled(d["H4_Stability_Short"], rho=0.21, p=0.094)
    elif scen == "marginal":
        for d in every:
            d["H1_Judge_Agreement"]["alpha_ordinal"] = 0.621
            set_pooled(d["H1_Judge_Agreement"]["brand_rho"], rho=0.752)
            set_wave(d["H2_Sep_Presence"], "t2", rho=0.38)
            set_wave(d["H3_Sep_Consistency"], "t3", rho=-0.56)
            set_pooled(d["H4_Stability_Short"], rho=0.42, p=0.0031)
            set_wave(d["H5_Sep_Ranking"], "t1", rho=-0.35)
            set_pooled(d["H6_Stability_Long"], rho=0.61, p=0.081)
            set_pooled(d["H7_Naming_Frequency"], rho=0.36)
            set_wave(d["H8_Recognition_Sep"], "t1", rho=0.52)
        set_wave(SD["H2_Sep_Presence"], "t2", rho=0.27)               # SD changes H2 (MARGINAL -> CONFIRMED)
        for h9 in (V["H9_Self_Preference"], SD["H9_Self_Preference"]):
            h9["mean_diff_own"] = h9["mean_diff_other"] - 7.3
            h9["delta_points"] = -7.3
    elif scen == "mixed":
        for d in every:
            d["H1_Judge_Agreement"]["alpha_ordinal"] = 0.703
            set_wave(d["H2_Sep_Presence"], "t1", rho=0.33)
            set_wave(d["H3_Sep_Consistency"], "t2", rho=-0.34)
            set_pooled(d["H4_Stability_Short"], rho=0.44, p=0.0102)
            set_pooled(d["H6_Stability_Long"], rho=0.45, p=0.0213)
            set_pooled(d["H7_Naming_Frequency"], rho=-0.55)
            set_wave(d["H8_Recognition_Sep"], "t2", rho=-0.36)
    elif scen == "presence":
        for d in every:
            set_wave(d["H2_Sep_Presence"], "t3", rho=0.58)
            set_wave(d["H5_Sep_Ranking"], "t2", rho=0.53)
            set_pooled(d["H6_Stability_Long"], rho=0.22, p=0.152)
    elif scen == "undetermined":
        for d in every:
            set_pooled(d["H1_Judge_Agreement"]["brand_rho"], det=False, n=14)
            for w in ("t2", "t3"):
                set_wave(d["H2_Sep_Presence"], w, det=False, n=11)
                set_wave(d["H8_Recognition_Sep"], w, det=False, n=17)
            for w in ("t1", "t3"):
                set_wave(d["H3_Sep_Consistency"], w, det=False, n=12)
            set_pooled(d["H4_Stability_Short"], det=False, n=16)
            set_pooled(d["H6_Stability_Long"], det=False, n=13)
            set_pooled(d["H7_Naming_Frequency"], det=False, n=18)
        for h9 in (V["H9_Self_Preference"], SD["H9_Self_Preference"]):
            h9["n_own_provider"] = 12
        drop_h5(V, "PENDING", "v1.10 Stage C verdicts not yet on branch v1.10; H5 is computed when they are")
    elif scen == "inactive":
        drop_h5(V, "INACTIVE", "tag v1.10-prereg-r2 not found")
    else:
        raise SystemExit(f"unknown scenario {scen}")
    return finalize(src, scen)


def write(src, out):
    out.mkdir(parents=True, exist_ok=True)
    jp = out / NAMES["stage_j"]
    jp.write_text(json.dumps(S.V._clean(src["stage_j"]), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    src["verdicts"]["stage_j_sha256"] = hashlib.sha256(jp.read_bytes()).hexdigest()
    for k in ("verdicts", "frozen", "plan"):
        (out / NAMES[k]).write_text(json.dumps(S.V._clean(src[k]), indent=2, ensure_ascii=False) + "\n",
                                    encoding="utf-8")


def make(out_root, scenarios=None):
    out_root = Path(out_root).resolve()
    if str(out_root).startswith(str((ROOT / "osf").resolve())):
        raise SystemExit(f"REFUSED: {out_root} is under osf/ (synthetic outputs never go next to real ones)")
    done = {}
    for s in scenarios or SCENARIOS:
        src = apply(load_base(), s)
        write(src, out_root / s)
        done[s] = src["verdicts"]["VERDICTS"]
    return done


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for s, v in make(sys.argv[1], sys.argv[2:] or None).items():
        print(f"{s:13s} {' '.join(f'{h}={w}' for h, w in v.items())}")
