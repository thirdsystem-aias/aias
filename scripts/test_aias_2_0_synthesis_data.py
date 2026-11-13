#!/usr/bin/env python3
"""
test_aias_2_0_synthesis_data.py — tests for scripts/aias_2_0_synthesis_data.py (no API calls;
no writes inside the repo).

  A. unit: classify() over every outline section-5 class and rule flag, including the
     non-finite-statistic guard; origin_tags() parsing; stage2_gate() on missing files,
     a missing origin tag, and both tags present.
  B. parity: the builder's t1/t2 profiles reproduce the locked v1.9 Stage 1 values exactly.
  C. end-to-end (--e2e SCRATCH): synthetic t3 = t1 copy (make_synthetic_t3.py copy_t1),
     the real v0.41 and v1.9 Stage 2 scorers in synthetic mode, then the builder with
     --skip-origin into SCRATCH; known answer: the t3 profile equals the t1 profile.

Usage: AIAS_ROOT=<tree> python3 scripts/test_aias_2_0_synthesis_data.py [--e2e SCRATCH]
"""
import os
import sys
from pathlib import Path

_ROOT0 = Path(os.environ.get("AIAS_ROOT") or Path(__file__).resolve().parents[1]).resolve()
os.environ["AIAS_ROOT"] = str(_ROOT0)
sys.path.insert(0, str(_ROOT0 / "scripts"))
import aias_2_0_synthesis_data as B   # noqa: E402  (may re-execute this script with the HOME shim)

import json        # noqa: E402
import subprocess  # noqa: E402
import tempfile    # noqa: E402
import types       # noqa: E402

RESULTS = []


def check(name, cond, detail=""):
    RESULTS.append((name, bool(cond), detail))
    print(f"{'PASS' if cond else 'FAIL'}  {name}" + (f"  [{detail}]" if detail and not cond else ""))


def v19(dv, cv, prs="CONFIRMED", drho=0.1, crho=0.7, nocomp=0.97):
    return {"verdicts": {"H_Dissociation_t3": {"verdict": dv, "rho": drho},
                         "H_Consistency_Reliability": {"verdict": cv, "rho": crho},
                         "H_Presence_Score_Reliability": {"verdict": prs},
                         "H_NoComposite_t3": {"rho_A_P": nocomp}}}


def unit():
    c = B.classify
    check("U when v1.9 Stage 2 absent", c(None)["class"] == "U")
    check("A: CONFIRMED/CONFIRMED", c(v19("CONFIRMED", "CONFIRMED"))["class"] == "A")
    r = c(v19("MARGINAL", "CONFIRMED"))
    check("A with moderate-coupling flag: MARGINAL/CONFIRMED", r["class"] == "A" and any("moderate" in f for f in r["flags"]))
    check("B: CONFIRMED/MARGINAL", c(v19("CONFIRMED", "MARGINAL"))["class"] == "B")
    check("C: CONFIRMED/FALSIFIED", c(v19("CONFIRMED", "FALSIFIED"))["class"] == "C")
    check("C: MARGINAL/FALSIFIED", c(v19("MARGINAL", "FALSIFIED"))["class"] == "C")
    for cv in ("CONFIRMED", "MARGINAL", "FALSIFIED"):
        check(f"D: FALSIFIED/{cv}", c(v19("FALSIFIED", cv))["class"] == "D")
    check("U: UNDETERMINED governing verdict", c(v19("UNDETERMINED", "CONFIRMED"))["class"] == "U")
    check("U guard: non-finite rho(C*,P) scored MARGINAL", c(v19("MARGINAL", "CONFIRMED", drho=None))["class"] == "U")
    check("U guard: NaN retest scored MARGINAL", c(v19("CONFIRMED", "MARGINAL", crho=float("nan")))["class"] == "U")
    check("R1 flag when Presence score reliability is not CONFIRMED",
          any(f.startswith("R1") for f in c(v19("CONFIRMED", "CONFIRMED", prs="MARGINAL"))["flags"]))
    check("no R1 flag when it is CONFIRMED", not any(f.startswith("R1") for f in c(v19("CONFIRMED", "CONFIRMED"))["flags"]))
    check("R6 flag when rho(A,P) < 0.95 at t3", any(f.startswith("R6") for f in c(v19("CONFIRMED", "CONFIRMED", nocomp=0.90))["flags"]))
    check("R6 class unchanged (no composite revival)", c(v19("CONFIRMED", "CONFIRMED", nocomp=0.90))["class"] == "A")
    v41 = {"verdicts": {"H_Phi_LongHorizon": {"verdict": "FALSIFIED"}, "H_Drift_Dissociation": {"verdict": "FALSIFIED"}},
           "manipulation_checks": {"MC_Snapshot": {"status": "MISMATCH"}}}
    r = c(v19("CONFIRMED", "CONFIRMED"), v41)
    fl = " ".join(r["flags"])
    check("R2/R3/R5 flags from v0.41; class still set by v1.9", r["class"] == "A" and "R2" in fl and "R3" in fl and "R5" in fl, fl)
    v41ok = {"verdicts": {"H_Phi_LongHorizon": {"verdict": "CONFIRMED"}, "H_Drift_Dissociation": {"verdict": "CONFIRMED"}},
             "manipulation_checks": {"MC_Snapshot": {"status": "PASS"}}}
    check("no R2/R3/R5 when v0.41 agrees", not [f for f in c(v19("CONFIRMED", "CONFIRMED"), v41ok)["flags"] if f[:2] in ("R2", "R3", "R5")])

    def fake(stdout, rc=0):
        return lambda *a, **k: types.SimpleNamespace(returncode=rc, stdout=stdout, stderr="boom" if rc else "")
    both = ("a" * 40 + "\trefs/tags/v0.41-prereg-r1\n" + "b" * 40 + "\trefs/tags/v0.41-prereg-r1^{}\n"
            + "c" * 40 + "\trefs/tags/v1.9-prereg-r1\n")
    found, err = B.origin_tags(B.STAGE2_TAGS, runner=fake(both))
    check("origin_tags parses names and peeled refs", err is None and found.get("v0.41-prereg-r1") == "a" * 40
          and found.get("v1.9-prereg-r1") == "c" * 40 and "v0.41-prereg-r1 (peeled)" in found)
    found, err = B.origin_tags(B.STAGE2_TAGS, runner=fake("", rc=128))
    check("origin_tags reports a git failure as not anchored", found == {} and err)

    every = lambda tags: {t: (True, "fake") for t in tags}            # noqa: E731
    with tempfile.TemporaryDirectory() as td:
        a, b = Path(td) / "v41.json", Path(td) / "v19.json"
        ok, reasons, _ = B.stage2_gate(a, b, anchors=every)
        check("gate closed when verdict files are missing", not ok and len([r for r in reasons if r.startswith("missing")]) == 2)
        a.write_text("{}"); b.write_text("{}")
        half = lambda tags: {t: (t == "v0.41-prereg-r1", "fake") for t in tags}  # noqa: E731
        ok, reasons, _ = B.stage2_gate(a, b, anchors=half)
        check("gate closed when one lock is not anchored", not ok and reasons == ["v1.9-prereg-r1 not externally anchored: fake"], reasons)
        ok, reasons, _ = B.stage2_gate(a, b, anchors=every)
        check("gate open with both files and both locks anchored", ok and not reasons, reasons)

        # OSF public-API walk (with pagination) returns the stored SHA-256
        def folder(name, href):
            return {"attributes": {"name": name, "kind": "folder"}, "relationships": {"files": {"links": {"related": {"href": href}}}}}
        pages = {
            B.OSF_API_ROOT: {"data": [folder("v40", "x")], "links": {"next": "root2"}},
            "root2": {"data": [folder("methodology", "m")], "links": {"next": None}},
            "m": {"data": [folder("v1_9", "m19")], "links": {}},
            "m19": {"data": [folder("anchor", "anc")], "links": {}},
            "anc": {"data": [{"attributes": {"name": "git_anchor_v1_9.json", "kind": "file",
                                             "extra": {"hashes": {"sha256": "f" * 64}}}}], "links": {}},
        }
        check("osf_sha256 walks folders and pages", B.osf_sha256(B.OSF_ANCHORS["v1.9-prereg-r1"][1], pages.get) == "f" * 64)
        check("osf_sha256 returns None for an absent file", B.osf_sha256(["methodology", "v1_9", "anchor", "nope.json"], pages.get) is None)

        # osf_anchor_ok: OSF bytes match AND the anchor names the local tag object
        anc = Path(td) / "git_anchor_v1_9.json"
        anc.write_text(json.dumps({"tag": "v1.9-prereg-r1", "tag_object": "1" * 40}))
        sha = B.sha256(anc)
        saved = dict(B.OSF_ANCHORS)
        B.OSF_ANCHORS["v1.9-prereg-r1"] = (str(anc), saved["v1.9-prereg-r1"][1])   # ROOT / absolute path = that path
        pages["anc"]["data"][0]["attributes"]["extra"]["hashes"]["sha256"] = sha
        try:
            ok, how = B.osf_anchor_ok("v1.9-prereg-r1", getter=pages.get, runner=fake("1" * 40 + "\n"))
            check("OSF anchor accepted when bytes and tag object match", ok, how)
            ok, how = B.osf_anchor_ok("v1.9-prereg-r1", getter=pages.get, runner=fake("2" * 40 + "\n"))
            check("OSF anchor refused when the local tag moved", not ok and "tag object" in how, how)
            pages["anc"]["data"][0]["attributes"]["extra"]["hashes"]["sha256"] = "0" * 64
            ok, how = B.osf_anchor_ok("v1.9-prereg-r1", getter=pages.get, runner=fake("1" * 40 + "\n"))
            check("OSF anchor refused when the OSF bytes differ", not ok and "different" in how, how)
        finally:
            B.OSF_ANCHORS.clear(); B.OSF_ANCHORS.update(saved)

    # anchor_status: origin first; a tag absent on origin falls back to the OSF anchor
    st = B.anchor_status(B.STAGE2_TAGS, runner=fake("a" * 40 + "\trefs/tags/v0.41-prereg-r1\n"),
                         getter=lambda url: {"data": [], "links": {}})
    check("anchor_status: origin hit for v0.41", st["v0.41-prereg-r1"][0] and st["v0.41-prereg-r1"][1].startswith("origin"))
    check("anchor_status: v1.9 falls back to OSF and is refused here", not st["v1.9-prereg-r1"][0], st["v1.9-prereg-r1"][1])


def parity():
    cal = json.load(open(B.CALIBRATION))
    gates, t1, t2 = B.S.run_gates()
    check("v0.41 parity gates P1-P4", all(gates[g]["passed"] for g in ("P1", "P2", "P3", "P4")))
    full = list(range(B.S.M))
    r1, r2 = B.wave_rows(B.S.wave_metrics(t1, full)), B.wave_rows(B.S.wave_metrics(t2, full))
    s1, s2 = B.summarize(r1), B.summarize(r2)
    try:
        res = B.parity_t1_t2(s1, s2, r1, r2, cal)
        check("builder reproduces Stage 1 (A1-A5)", all(v["passed"] for v in res.values()))
    except B.ParityFailure as e:
        check("builder reproduces Stage 1 (A1-A5)", False, str(e)[:300])
    check("112 units per wave", s1["n_units"] == 112 and s2["n_units"] == 112)
    check("per-substrate units 16/24/24/24/24",
          [s1["per_substrate"][s]["n_units"] for s in B.S.OMNI] == [16, 24, 24, 24, 24])
    # a perturbed calibration must fail parity
    bad = json.loads(json.dumps(cal))
    row = next(c for c in bad["candidates"] if c["spec"] == "C_phi+FLOOR+ADD")
    row["retest_C"] += 1e-6
    try:
        B.parity_t1_t2(s1, s2, r1, r2, bad)
        check("parity fails on a perturbed locked value", False)
    except B.ParityFailure:
        check("parity fails on a perturbed locked value", True)


def e2e(scratch):
    scratch = Path(scratch).resolve()
    syn = scratch / "syn_copy_t1"
    env = dict(os.environ)
    py = sys.executable
    root = B.ROOT
    steps = [
        [py, str(root / "osf/v41/scripts/tests/make_synthetic_t3.py"), "copy_t1", str(syn)],
        [py, str(root / "osf/v41/scripts/score_v41.py"), "--synthetic", str(syn)],
        [py, str(root / "osf/methodology/v1_9/scripts/score_v1_9.py"), "--stage2-synthetic", str(syn)],
    ]
    for cmd in steps:
        r = subprocess.run(cmd, capture_output=True, text=True, env=env)
        check("e2e step: " + Path(cmd[1]).name + " " + cmd[2], r.returncode == 0, (r.stderr or r.stdout)[-400:])
        if r.returncode:
            return
    v41f, v19f = syn / "_score" / "v41_verdicts.json", syn / "_score_v1_9" / "v1_9_verdicts.json"
    out = scratch / "_aias20"
    r = subprocess.run([py, str(root / "scripts/aias_2_0_synthesis_data.py"), "--t3", str(syn), "--v41", str(v41f),
                        "--v19", str(v19f), "--skip-origin", "--out", str(out)], capture_output=True, text=True, env=env)
    check("e2e: builder exits 0", r.returncode == 0, (r.stderr or r.stdout)[-400:])
    if r.returncode:
        return
    d = json.load(open(out / "aias_2_0_synthesis_data.json"))
    s1, s3 = d["summaries"]["t1"], d["summaries"]["t3"]
    check("e2e: status complete", d["status"] == "complete")
    check("e2e: t3 (= t1 copy) reproduces the t1 rho(C*,P) and rated share",
          abs(s3["rho_Cstar_P"] - s1["rho_Cstar_P"]) < 1e-12 and s3["share_not_rated"] == s1["share_not_rated"])
    check("e2e: builder's t3 rho(C*,P) equals the v1.9 Stage 2 statistic",
          d["stage2"]["consistency_check"]["rho_Cstar_P_t3_matches_v19"])
    v = d["stage2"]["v19_verdicts"]
    expect = B.classify({"verdicts": v}, {"verdicts": d["stage2"]["v41_verdicts"],
                                         "manipulation_checks": d["stage2"]["v41_manipulation_checks"]})
    check("e2e: class recorded = classify(recorded verdicts)", d["stage2"]["class"]["class"] == expect["class"],
          f"{d['stage2']['class']} vs {expect}")
    print(f"      synthetic copy_t1: DIS {v['H_Dissociation_t3']['verdict']} ({v['H_Dissociation_t3']['rho']:.3f}), "
          f"CRS {v['H_Consistency_Reliability']['verdict']} ({v['H_Consistency_Reliability']['rho']:.3f}), "
          f"PRS {v['H_Presence_Score_Reliability']['verdict']} -> class {d['stage2']['class']['class']}")


if __name__ == "__main__":
    unit()
    parity()
    if "--e2e" in sys.argv:
        e2e(sys.argv[sys.argv.index("--e2e") + 1])
    n_fail = sum(1 for _, ok, _ in RESULTS if not ok)
    print(f"{len(RESULTS) - n_fail}/{len(RESULTS)} passed")
    sys.exit(1 if n_fail else 0)
