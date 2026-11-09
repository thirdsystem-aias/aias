#!/usr/bin/env python3
"""
aias_2_0_synthesis_data.py — AIAS(TM) 2.0 synthesis data builder.

The single source for the synthesis paper's section 4 and every figure. Transcribes
papers/aias_2_0/aias_2_0_synthesis_outline.md (r1, tag aias-2-0-outline-locked); THE OUTLINE
GOVERNS where this script and it disagree (a disagreement is a bug to fix toward the outline).

Reads locked records only; every input is hashed into the output.
  lineage   the CPC-era verdict files (v0.30-v0.35, v0.36 frozen copy), v1.7, the frozen
            v1.8 record, v0.37, v0.29, and the v1.9 Stage 1 calibration.
  profiles  per-brand P and C* (C_phi rated at >= 6 total mentions) for each available wave,
            computed with the LOCKED v1.9 scorer functions (score_v1_9.unit_table on
            score_v41.wave_metrics). Before anything is written, t1/t2 must reproduce the
            locked Stage 1 values in v1_9_calibration.json exactly (PARITY A1-A5).
  stage2    osf/v41/v41_verdicts.json and osf/methodology/v1_9/v1_9_verdicts.json are read
            only when both exist AND both prereg tags are on origin (git ls-remote against
            the remote URL, not the local tag). The outline's section-5 class is then
            computed mechanically (classify()).

Outputs (osf/aias_2_0/): aias_2_0_synthesis_data.json, aias_2_0_profiles.csv.
status = "pre-t3" until the Stage 2 section is complete; the data lock tag
(aias-2-0-data-locked) is cut only on status = "complete".

Usage:  AIAS_ROOT=<tree> python3 scripts/aias_2_0_synthesis_data.py [--check-only]
        Test-only overrides: --t3 DIR --v41 FILE --v19 FILE --skip-origin --out DIR
Exit:   0 ok · 2 parity failure (nothing written) · 3 bad arguments
"""
import os
import sys
from pathlib import Path

_ROOT0 = Path(os.environ.get("AIAS_ROOT") or Path(__file__).resolve().parents[1]).resolve()
os.environ["AIAS_ROOT"] = str(_ROOT0)
sys.path.insert(0, str(_ROOT0 / "osf/methodology/v1_9/scripts"))
import score_v1_9 as V19   # noqa: E402  (imports score_v41, which may re-execute this script with a HOME shim)

import argparse            # noqa: E402
import csv                 # noqa: E402
import hashlib             # noqa: E402
import json                # noqa: E402
import math                # noqa: E402
import subprocess          # noqa: E402
from datetime import datetime, timezone  # noqa: E402

S = V19.S
ROOT = V19.ROOT
OSF = ROOT / "osf"
OUTDIR = OSF / "aias_2_0"
OUTLINE_TAG = "aias-2-0-outline-locked"
ORIGIN_URL = "https://github.com/thirdsystem-aias/aias.git"
STAGE2_TAGS = ["v0.41-prereg-r1", "v1.9-prereg-r1"]
V41_VERDICTS = OSF / "v41" / "v41_verdicts.json"
V19_VERDICTS = OSF / "methodology" / "v1_9" / "v1_9_verdicts.json"
CALIBRATION = OSF / "methodology" / "v1_9" / "v1_9_calibration.json"
SPEC = V19.SELECTED_SPEC            # ("C_phi", "FLOOR", "ADD"): C* + the descriptive ADD composite
K2_LINE = V19.K2_MAX                 # 0.95
PARITY_TOL = 1e-12

# Outline section 3.2-3.3: locked records consumed (path relative to ROOT)
LINEAGE = {
    "v0.29": "osf/v29/data/v29_verdicts.json",
    "v0.30": "osf/v30/v30_cpc_verdicts.json",
    "v0.31": "osf/v31/v31_cpc_verdicts.json",
    "v0.32": "osf/v32/v32_verdicts.json",
    "v0.33": "osf/v33/v33_provider_asymmetry_verdicts.json",
    "v0.34": "osf/v34/v34_verdicts.json",
    "v0.35": "osf/v35/v35_verdicts.json",
    "v0.36": "osf/aias_2_0/inputs/v36_verdicts.json",
    "v1.7": "osf/methodology/v1_7/v1_7_cpc_verdicts.json",
    "v1.8": "osf/v41/registries/v1_8_verdicts.json",
    "v0.37": "osf/v37/v37_verdicts.json",
    "v1.9-stage1": "osf/methodology/v1_9/v1_9_calibration.json",
}
# SSRN status per the kickoff registry (master copy, Nov 9, 2026). Declined/withdrawn papers
# are cited by title with the OSF or thirdsystem.ai copy, never an ssrn.com link.
SSRN = {
    "v0.29": ("6870778", "posted"), "v0.30": ("6875319", "declined"), "v0.31": ("6880959", "withdrawn"),
    "v0.32": ("6898581", "posted"), "v0.33": ("6909019", "posted"), "v0.34": ("6915458", "posted"),
    "v0.35": ("6921758", "declined"), "v0.36": ("6927958", "declined"), "v1.7": ("6878818", "posted"),
    "v1.8": ("6963359", "posted"), "v0.37": (None, "not yet submitted"), "v1.9-stage1": (None, "no paper yet"),
}
ERA = {k: "CV-CPC era (lineage; instrument not adopted per v1.7)" for k in
       ("v0.30", "v0.31", "v0.32", "v0.33", "v0.34", "v0.35", "v0.36")}
ERA.update({"v0.29": "Presence (carried by citation)", "v1.7": "CV-CPC falsified (turning point)",
            "v1.8": "phi instrument (AIAS 2.0 evidence)", "v0.37": "phi (AIAS 2.0 evidence)",
            "v1.9-stage1": "scoring rule (AIAS 2.0 evidence; calibration, not a test)"})


class ParityFailure(RuntimeError):
    pass


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _finite(x):
    return x is not None and isinstance(x, (int, float)) and math.isfinite(x)


# ===========================================================================
# lineage (outline 3.2-3.3)
# ===========================================================================
def _verdicts_of(rec):
    """Every '<...>verdict' string in a record, keyed by its dotted path (for the lineage table)."""
    out = {}

    def walk(x, p):
        if isinstance(x, dict):
            for k, v in x.items():
                q = f"{p}.{k}" if p else k
                if k == "verdict" and isinstance(v, str):
                    out[p] = v
                else:
                    walk(v, q)
    walk(rec, "")
    return out


def lineage():
    rows, inputs = {}, {}
    for phase, rel in LINEAGE.items():
        path = ROOT / rel
        rec = json.load(open(path))
        inputs[rel] = sha256(path)
        ssrn_id, ssrn_status = SSRN[phase]
        rows[phase] = {"source": rel, "era": ERA[phase], "ssrn": ssrn_id, "ssrn_status": ssrn_status,
                       "verdicts": _verdicts_of(rec), "record": rec}
    return rows, inputs


# ===========================================================================
# profiles (outline 3.3, 8: per-brand P and C*, declared descriptive summaries)
# ===========================================================================
def wave_rows(wm):
    return V19.unit_table(wm, SPEC)


def summarize(rows):
    per = {}
    for s in S.OMNI:
        r = [x for x in rows if x["s"] == s]
        rated = [x for x in r if x["C"] is not None]
        per[s] = {"n_units": len(r), "n_rated": len(rated),
                  "share_rated": len(rated) / len(r) if r else None,
                  "mean_P": sum(x["P"] for x in r) / len(r) if r else None,
                  "mean_C_rated": sum(x["C"] for x in rated) / len(rated) if rated else None}
    k1, n1 = V19._rho(rows, "C", "P")
    a, na = V19._rho(rows, "A", "P")
    return {"per_substrate": per, "n_units": len(rows),
            "n_rated": sum(1 for x in rows if x["C"] is not None),
            "share_not_rated": sum(1 for x in rows if x["C"] is None) / len(rows),
            "rho_Cstar_P": k1, "rho_Cstar_P_n": n1,
            "rho_A_P_descriptive": a, "rho_A_P_n": na}


def parity_t1_t2(sum1, sum2, rows1, rows2, cal):
    """PARITY A1-A5: the builder's t1/t2 profile reproduces the locked Stage 1 values exactly."""
    row = next(c for c in cal["candidates"] if c["spec"] == "+".join(SPEC))
    relC, nC = V19.retest(rows1, rows2, "C")
    relP, nP = V19.retest(rows1, rows2, "P")
    checks = {
        "A1_K1_t1": (sum1["rho_Cstar_P"], row["t1"]["K1"]["rho"], sum1["rho_Cstar_P_n"], row["t1"]["K1"]["n"]),
        "A2_K1_t2": (sum2["rho_Cstar_P"], row["t2"]["K1"]["rho"], sum2["rho_Cstar_P_n"], row["t2"]["K1"]["n"]),
        "A3_not_rated": (sum1["share_not_rated"], row["t1"]["share_C_not_rated"],
                         sum2["share_not_rated"], row["t2"]["share_C_not_rated"]),
        "A4_retest_C": (relC, row["retest_C"], nC, row["retest_C_n"]),
        "A5_retest_P": (relP, cal["presence_retest_t1_t2"], nP, cal["presence_retest_n"]),
    }
    res = {}
    for k, (a, b, c, d) in checks.items():
        ok = abs(a - b) <= PARITY_TOL and (abs(c - d) <= PARITY_TOL)
        res[k] = {"builder": [a, c], "locked": [b, d], "passed": bool(ok)}
    failed = [k for k, v in res.items() if not v["passed"]]
    if failed:
        raise ParityFailure("parity failed: " + ", ".join(failed) + "\n" + json.dumps(res, indent=2))
    return res


# ===========================================================================
# stage 2 gate (outline 8) and the section-5 class
# ===========================================================================
def origin_tags(tags, url=ORIGIN_URL, runner=subprocess.run):
    """Tag name -> object id on the remote, read with git ls-remote against the URL."""
    try:
        r = runner(["git", "ls-remote", url] + [f"refs/tags/{t}" for t in tags],
                   capture_output=True, text=True, timeout=90)
    except Exception as e:                       # network or git missing: treat as not anchored
        return {}, f"{type(e).__name__}: {e}"
    if r.returncode != 0:
        return {}, (r.stderr or "").strip()[:300]
    found = {}
    for line in r.stdout.splitlines():
        sha, ref = line.split("\t")
        name = ref[len("refs/tags/"):] if ref.startswith("refs/tags/") else ref
        if name.endswith("^{}"):
            found.setdefault(name[:-3] + " (peeled)", sha)
        else:
            found[name] = sha
    return found, None


def stage2_gate(v41_path, v19_path, skip_origin=False, runner=subprocess.run):
    reasons = []
    for p in (v41_path, v19_path):
        if not Path(p).exists():
            reasons.append(f"missing {Path(p).relative_to(ROOT) if str(p).startswith(str(ROOT)) else p}")
    origin = {}
    if skip_origin:
        origin = {"skipped": "test mode (--skip-origin)"}
    else:
        found, err = origin_tags(STAGE2_TAGS, runner=runner)
        origin = {"found": found, "error": err}
        for t in STAGE2_TAGS:
            if t not in found:
                reasons.append(f"tag {t} not on origin")
    return (not reasons), reasons, origin


def _v(d, *path):
    for k in path:
        if not isinstance(d, dict) or k not in d:
            return None
        d = d[k]
    return d


def classify(v19, v41=None):
    """Outline section 5. Governing: v1.9 H_Dissociation_t3 and H_Consistency_Reliability.
    Returns {"class": A|B|C|D|U, "flags": [...], "why": str}. A governing statistic that is
    missing or not finite gives U whatever the verdict string says (the v1.9 module's
    UNDETERMINED rule; guards against a NaN being scored MARGINAL)."""
    if not v19 or "verdicts" not in v19:
        return {"class": "U", "flags": [], "why": "v1.9 Stage 2 verdicts absent"}
    V = v19["verdicts"]
    dis, crs = V.get("H_Dissociation_t3", {}), V.get("H_Consistency_Reliability", {})
    dv, cv = dis.get("verdict"), crs.get("verdict")
    if dv is None or cv is None or "UNDETERMINED" in (dv, cv):
        return {"class": "U", "flags": [], "why": f"governing verdict undetermined ({dv}, {cv})"}
    if not _finite(dis.get("rho")) or not _finite(crs.get("rho")):
        return {"class": "U", "flags": ["governing statistic not finite"],
                "why": f"rho(C*,P)={dis.get('rho')}, rho(C*_t2,C*_t3)={crs.get('rho')}"}
    flags = []
    if dv == "FALSIFIED":
        cls, why = "D", "H_Dissociation_t3 FALSIFIED: drafting pauses; options memo to Pablo"
    elif dv in ("CONFIRMED", "MARGINAL"):
        cls = {"CONFIRMED": "A", "MARGINAL": "B", "FALSIFIED": "C"}.get(cv)
        if cls is None:
            return {"class": "U", "flags": [], "why": f"unrecognized H_Consistency_Reliability verdict {cv!r}"}
        why = f"H_Dissociation_t3 {dv}, H_Consistency_Reliability {cv}"
        if dv == "MARGINAL":
            flags.append("separable with moderate coupling at t3 (print the coupling value)")
    else:
        return {"class": "U", "flags": [], "why": f"unrecognized H_Dissociation_t3 verdict {dv!r}"}
    prs = _v(V, "H_Presence_Score_Reliability", "verdict")
    if prs != "CONFIRMED":
        flags.append(f"R1: H_Presence_Score_Reliability {prs} qualifies the Presence stability sentence only")
    nocomp = _v(V, "H_NoComposite_t3", "rho_A_P")
    if _finite(nocomp) and abs(nocomp) < K2_LINE:
        flags.append(f"R6: rho(A,P) at t3 = {nocomp:.3f} < {K2_LINE}: reported; no composite is revived")
    if v41:
        W = v41.get("verdicts", {})
        phi = _v(W, "H_Phi_LongHorizon", "verdict")
        if phi is not None and phi != cv:
            flags.append(f"R2: H_Phi_LongHorizon {phi} vs H_Consistency_Reliability {cv}: report both; headline follows C*")
        drd = _v(W, "H_Drift_Dissociation", "verdict")
        if drd == "FALSIFIED" and dv in ("CONFIRMED", "MARGINAL"):
            flags.append("R3: levels separate, changes move together (H_Drift_Dissociation FALSIFIED)")
        snap = _v(v41, "manipulation_checks", "MC_Snapshot", "status")
        if snap not in (None, "PASS"):
            flags.append(f"R5: MC_Snapshot {snap}: print the locked sensitivity beside the primary")
    return {"class": cls, "flags": flags, "why": why}


# ===========================================================================
# build
# ===========================================================================
def build(args):
    t_start = datetime.now(timezone.utc).isoformat(timespec="seconds")
    cal = json.load(open(CALIBRATION))
    gates, t1, t2 = S.run_gates()                         # v0.41 P1-P4 (halt on failure)
    full = list(range(S.M))
    w1, w2 = S.wave_metrics(t1, full), S.wave_metrics(t2, full)
    rows1, rows2 = wave_rows(w1), wave_rows(w2)
    sum1, sum2 = summarize(rows1), summarize(rows2)
    parity = parity_t1_t2(sum1, sum2, rows1, rows2, cal)  # raises ParityFailure

    lin, inputs = lineage()
    v41_path = Path(args.v41) if args.v41 else V41_VERDICTS
    v19_path = Path(args.v19) if args.v19 else V19_VERDICTS
    ok, reasons, origin = stage2_gate(v41_path, v19_path, skip_origin=args.skip_origin)
    profiles = {"t1": rows1, "t2": rows2}
    summaries = {"t1": sum1, "t2": sum2}
    stage2 = {"status": "pending", "reasons": reasons, "origin": origin}
    if ok:
        v41 = json.load(open(v41_path))
        v19 = json.load(open(v19_path))
        inputs[str(v41_path)] = sha256(v41_path)
        inputs[str(v19_path)] = sha256(v19_path)
        import score_v0_31 as S31
        used = v19.get("panel_used") or S31.PANEL           # the panel v1.9 Stage 2 scored on
        keep = [i for i, m in enumerate(S31.PANEL) if m in used]
        d3 = Path(args.t3).resolve() if args.t3 else S.DATA3
        t3 = S.load_wave(S._layout(d3, d3 / "v23"))
        w2k, w3k = S.wave_metrics(t2, keep), S.wave_metrics(t3, keep)
        rows2k, rows3 = wave_rows(w2k), wave_rows(w3k)
        profiles["t2_panel_t3"] = rows2k if len(keep) < S.M else None
        profiles["t3"] = rows3
        summaries["t3"] = summarize(rows3)
        relC, nC = V19.retest(rows2k, rows3, "C")
        relP, nP = V19.retest(rows2k, rows3, "P")
        stage2 = {"status": "complete", "reasons": [], "origin": origin,
                  "panel_used": v19.get("panel_used"),
                  "v19_verdicts": v19.get("verdicts"), "v41_verdicts": v41.get("verdicts"),
                  "v41_manipulation_checks": v41.get("manipulation_checks"),
                  "descriptive_retest_t2_t3": {"C_star": [relC, nC], "P": [relP, nP]},
                  "consistency_check": {
                      "rho_Cstar_P_t3_matches_v19": (abs(summaries["t3"]["rho_Cstar_P"] -
                                                         (_v(v19, "verdicts", "H_Dissociation_t3", "rho") or float("nan")))
                                                     <= PARITY_TOL)},
                  "class": classify(v19, v41)}
    else:
        stage2["class"] = {"class": None, "flags": [], "why": "Stage 2 not available yet (see reasons)"}

    out = {
        "phase": "AIAS 2.0 synthesis", "outline_tag": OUTLINE_TAG, "built_at_utc": t_start,
        "status": "complete" if stage2["status"] == "complete" else "pre-t3",
        "spec": {"consistency_score": "C_phi rated at >= 6 total mentions (v1.9 SELECTED_CONSISTENCY)",
                 "presence_score": "P = 100*(C_P/6 + 2*pi_hat)/3 (v0.25 presence_composite)",
                 "composite": "none (v1.9 Stage 1); A = (P + C*)/2 kept only for the descriptive K2 check"},
        "parity_gates_v0_41": {g: gates[g]["passed"] for g in ("P1", "P2", "P3", "P4")},
        "parity_builder_vs_stage1": parity,
        "summaries": summaries,
        "lineage": lin,
        "stage2": stage2,
        "inputs_sha256": inputs,
    }
    return out, profiles


def write(out, profiles, outdir):
    outdir.mkdir(parents=True, exist_ok=True)
    json.dump(S._clean(out), open(outdir / "aias_2_0_synthesis_data.json", "w"), indent=2, allow_nan=False)
    with open(outdir / "aias_2_0_profiles.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["wave", "substrate", "brand", "P", "C_star", "rated", "n_mentions", "A_descriptive"])
        for wave, rows in profiles.items():
            if not rows:
                continue
            for x in sorted(rows, key=lambda r: (r["s"], r["b"])):
                w.writerow([wave, x["s"], x["b"], f"{x['P']:.6f}",
                            "" if x["C"] is None else f"{x['C']:.6f}",
                            int(x["C"] is not None), x["n"], f"{x['A']:.6f}"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-only", action="store_true", help="run parity and the stage-2 gate; write nothing")
    ap.add_argument("--t3", metavar="DIR"); ap.add_argument("--v41", metavar="FILE"); ap.add_argument("--v19", metavar="FILE")
    ap.add_argument("--skip-origin", action="store_true", help="tests only: skip the ls-remote anchor check")
    ap.add_argument("--out", metavar="DIR")
    a = ap.parse_args()
    if a.skip_origin and not a.out:
        print("--skip-origin is for tests and needs --out outside osf/aias_2_0/", file=sys.stderr)
        return 3
    try:
        out, profiles = build(a)
    except ParityFailure as e:
        print("[aias-2.0] PARITY FAILURE (nothing written)\n" + str(e), file=sys.stderr)
        return 2
    except S.GateFailure as e:
        print("[aias-2.0] v0.41 PARITY GATE FAILURE (nothing written)\n" + str(e), file=sys.stderr)
        return 2
    s1, s2 = out["summaries"]["t1"], out["summaries"]["t2"]
    print(f"status: {out['status']}  parity A1-A5: all passed  v0.41 gates: {out['parity_gates_v0_41']}")
    print(f"t1: rho(C*,P) {s1['rho_Cstar_P']:.3f} (n {s1['rho_Cstar_P_n']}), not rated {s1['share_not_rated']:.3f}")
    print(f"t2: rho(C*,P) {s2['rho_Cstar_P']:.3f} (n {s2['rho_Cstar_P_n']}), not rated {s2['share_not_rated']:.3f}")
    print(f"stage 2: {out['stage2']['status']}  class: {out['stage2']['class']['class']}  "
          f"({out['stage2']['class']['why']})  reasons: {out['stage2'].get('reasons')}")
    if a.check_only:
        return 0
    outdir = Path(a.out).resolve() if a.out else OUTDIR
    write(out, profiles, outdir)
    print(f"wrote {outdir}/aias_2_0_synthesis_data.json and aias_2_0_profiles.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
