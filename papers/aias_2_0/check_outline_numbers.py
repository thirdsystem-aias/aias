"""check_outline_numbers.py - AIAS 2.0 outline: every quoted statistic against its locked source.

Each check computes the value from a locked file (read from git, not the working tree),
formats it the way the outline prints it, and requires that exact string in the outline.
Run from the repo or a worktree:  python3 papers/aias_2_0/check_outline_numbers.py
Exit 0 = all checks pass; 1 = at least one failure (all failures are printed).
"""
import json, re, subprocess, sys
from pathlib import Path

REF = "70e19ac"          # v1.9-prereg-r1 (contains v29-v37, v1.7, the frozen v1.8 record, v1.9, v0.41)
REF_V36 = "v0.36"        # osf/v36 lives on branch v0.36 only
OUTLINE = Path(__file__).with_name("aias_2_0_synthesis_outline.md")


def git_text(ref, path):
    r = subprocess.run(["git", "show", f"{ref}:{path}"], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"cannot read {ref}:{path}: {r.stderr.strip()}")
    return r.stdout


def js(ref, path):
    return json.loads(git_text(ref, path))


def f(x, nd):
    return f"{x:.{nd}f}"


text = OUTLINE.read_text(encoding="utf-8")
checks = []   # (label, expected string in outline, source-derived truth)


def need(label, s, truth=True):
    checks.append((label, s, truth))


# v0.29
v29 = js(REF, "osf/v29/data/v29_verdicts.json")["result"]
need("v0.29 verdict", "H_CV_Baseline CONFIRMED", v29["verdict"] == "CONFIRMED")
need("v0.29 rho_conv", f"convergent ρ = {f(v29['C1_convergent']['rho'], 4)}")
need("v0.29 p_conv", f"p = {v29['C1_convergent']['p']:.1e}".replace("e-05", "e-05"))
need("v0.29 rho_disc", f"discriminant ρ = {v29['C2_discriminant']['rho']:.4f}".replace("-", "−"))
need("v0.29 p_disc", f"p = {f(v29['C2_discriminant']['p'], 3)}")
need("v0.29 C3", f"gap {f(v29['C3_campbell_fiske_gap']['value'], 4)}")

# v0.30
v30 = js(REF, "osf/v30/v30_cpc_verdicts.json")
need("v0.30 verdicts", "F1 Computable CONFIRM; F2 LevelConfound and F3 LevelCorrected UNDETERMINED; F4 SubstrateVariation CONFIRM",
     [v30[k]["verdict"] for k in ("F1_H_CPC_Computable", "F2_H_CPC_LevelConfound", "F3_H_CPC_LevelCorrected", "F4_H_CPC_SubstrateVariation")]
     == ["CONFIRM", "UNDETERMINED", "UNDETERMINED", "CONFIRM"])

# v0.31
v31 = js(REF, "osf/v31/v31_cpc_verdicts.json")
need("v0.31 verdicts", "Computable CONFIRM; CrossCategory CONFIRM",
     v31["H_CPC_Computable"]["verdict"] == "CONFIRM" and v31["H_CPC_CrossCategory"]["verdict"] == "CONFIRM")
need("v0.31 H", f"H = {f(v31['H_CPC_CrossCategory']['kruskal_H'], 2)}")
need("v0.31 p", f"p = {f(v31['H_CPC_CrossCategory']['kruskal_p'], 5)}")

# v0.32
v32 = js(REF, "osf/v32/v32_verdicts.json")
lopo = v32["SENSITIVITY_leave_one_provider_out"]
need("v0.32 primary", f"PRIMARY CONFIRMED (ρ = {f(v32['PRIMARY_H_ScoreRankStable']['rho'], 3)})",
     v32["PRIMARY_H_ScoreRankStable"]["verdict"] == "CONFIRMED")
need("v0.32 sec/ter", "SECONDARY and TERTIARY FALSIFIED",
     v32["SECONDARY_H_ScoreMagnitudeStable"]["verdict"] == "FALSIFIED" and v32["TERTIARY_H_EmergingInstability"]["verdict"] == "FALSIFIED")
need("v0.32 LOPO", f"ρ {f(lopo['drop_anthropic']['rho'], 3)} / {f(lopo['drop_openai']['rho'], 3)} / {f(lopo['drop_google']['rho'], 3)} (drop Anthropic / OpenAI / Google)")

# v0.33
v33 = js(REF, "osf/v33/v33_provider_asymmetry_verdicts.json")
need("v0.33 asym", f"H_Provider_Asymmetry CONFIRMED (mean η² = {f(v33['H_Provider_Asymmetry']['mean_eta2_observed'], 3)}, MC p = {f(v33['H_Provider_Asymmetry']['mc_p_onesided'], 4)})",
     v33["H_Provider_Asymmetry"]["verdict"] == "CONFIRMED")
need("v0.33 beyond", f"(δη² = {f(v33['H_Provider_Beyond_Presence']['delta_eta2_observed'], 3)}, MC p = {f(v33['H_Provider_Beyond_Presence']['mc_p_onesided'], 4)})")
need("v0.33 ordinal", "H_Provider_Ordinal UNINFORMATIVE", v33["H_Provider_Ordinal"]["verdict"].startswith("UNINFORMATIVE"))

# v0.34
v34 = js(REF, "osf/v34/v34_verdicts.json")["verdicts"]
r = v34["H_CPC_Temporal_Stability"]["per_substrate_rho"]
need("v0.34 temporal", f"H_CPC_Temporal_Stability CONFIRMED (ρ {f(r['v0.20'],2)} / {f(r['v0.21'],2)} / {f(r['v0.22'],2)} / {f(r['v0.23'],2)} for v0.20–v0.23; v0.19 {f(r['v0.19'],2)})",
     v34["H_CPC_Temporal_Stability"]["verdict"] == "CONFIRMED")
need("v0.34 drift", "H_CPC_Drift_Beyond_Presence MARGINAL", v34["H_CPC_Drift_Beyond_Presence"]["verdict"] == "MARGINAL")
need("v0.34 drift saturation 4/5", "recognition saturated in 4/5",
     sum(v34["H_CPC_Drift_Beyond_Presence"]["saturation_flagged"].values()) == 4)
need("v0.34 presence", "H_Presence_Temporal_Stability MARGINAL", v34["H_Presence_Temporal_Stability"]["verdict"] == "MARGINAL")

# v0.35
v35 = js(REF, "osf/v35/v35_verdicts.json")["verdicts"]
need("v0.35 verdicts", "H_Phantom_CPC_Signature CONFIRMED; H_Phantom_Beyond_Presence UNDETERMINED (control flip); H_Phantom_Cross_Substrate UNINFORMATIVE",
     v35["H_Phantom_CPC_Signature"]["verdict"] == "CONFIRMED"
     and v35["H_Phantom_Beyond_Presence"]["verdict"].startswith("UNDETERMINED (control flip)")
     and v35["H_Phantom_Cross_Substrate"]["verdict"].startswith("UNINFORMATIVE"))

# v0.36
v36 = js(REF_V36, "osf/v36/v36_verdicts.json")
hyp = v36["hypotheses"]
need("v0.36 cell", "Cell D (unstructured); all four structure hypotheses NOT SUPPORTED",
     v36["verdict_matrix_cell"] == "Cell D" and v36["verdict_matrix_cell_verdict"] == "unstructured"
     and len(hyp) == 4 and all(h["verdict"] == "NOT SUPPORTED" for h in hyp.values()))

# v1.7
v17 = js(REF, "osf/methodology/v1_7/v1_7_cpc_verdicts.json")
c = v17["H_CPC_Dissociates"]["pooled"]["composite"]
need("v1.7 dissociates", f"H_CPC_Dissociates FALSIFIED (pooled composite ρ = {f(c['rho'],3)}, n = {c['n']})",
     v17["H_CPC_Dissociates"]["verdict"] == "FALSIFIED")
need("v1.7 defined", f"H_CPC_Defined FALSIFIED (defined rate {f(v17['H_CPC_Defined']['pooled_defined_rate'],3)})",
     v17["H_CPC_Defined"]["verdict"] == "FALSIFIED")
need("v1.7 in figure list", f"CV-CPC (v1.7 {f(c['rho'],3)}")

# v1.8 (frozen copy)
v18 = js(REF, "osf/v41/registries/v1_8_verdicts.json")
V = v18["verdicts"]
need("v1.8 CV reproduces", f"|ρ(CV-CPC, μ)| = {f(V['H_CV_Reproduces']['stat']['abs_rho'],3)}, n = {V['H_CV_Reproduces']['stat']['n']}",
     V["H_CV_Reproduces"]["verdict"].startswith("CONFIRMED"))
pooled = V["H_MeanIndependent"]["stat"]["pooled"]
need("v1.8 mean-independent", f"pooled |ρ(φ, μ)| = {f(pooled['abs_rho'],3)}, n = {pooled['n']}",
     V["H_MeanIndependent"]["verdict"].startswith("CONFIRMED"))
s = V["H_LowRecallDefined"]["stat"]
need("v1.8 low recall", f"φ defined for {s['phi_defined']}/{s['n_nonzero_surfacing']} surfacing brands, against {s['cv_raw_defined']} for CV-CPC",
     V["H_LowRecallDefined"]["verdict"].startswith("CONFIRMED"))
pd = V["H_PositionalDissociation"]["stat"]
need("v1.8 positional", f"ρ(φ, J) = {f(pd['rho'],3)}, n = {pd['n']}".replace("-", "−"),
     V["H_PositionalDissociation"]["verdict"].startswith("CONFIRMED"))
need("v1.8 graded", "H_GradedRecognition FORWARD-SPEC", V["H_GradedRecognition"]["verdict"].startswith("FORWARD-SPEC"))
need("v1.8 phantom", "H_PhantomSignature NULL", V["H_PhantomSignature"]["verdict"] == "NULL")
tw = v18["two_wave_reproducibility"]["phi_t1_t2_rank_agreement"]
need("v1.8 two-wave", f"ρ(φ_t₁, φ_t₂) = {f(tw['rho'],3)} (n = {tw['n']})")
need("v1.8 in claim 3", f"H_MeanIndependent ({f(pooled['abs_rho'],3)})")

# v0.37
v37 = js(REF, "osf/v37/v37_verdicts.json")["verdicts"]["H_IL_Consistency"]
need("v0.37", f"ρ = {f(v37['stat']['rho'],3)}, p_perm = {f(v37['stat']['p_perm'],3)}, n = {v37['stat']['n']}".replace("-", "−"),
     v37["verdict"] == "FALSIFIED" and v37["headline_cell"] == "CLEAN-NULL")

# v1.9 Stage 1
cal = js(REF, "osf/methodology/v1_9/v1_9_calibration.json")
C = {x["spec"]: x for x in cal["candidates"]}
a = C["C_phi+FLOOR+ADD"]
need("v1.9 K1", f"ρ(C\\*, P) = {f(a['t1']['K1']['rho'],3)} (t₁, n = {a['t1']['K1']['n']}) and {f(a['t2']['K1']['rho'],3)} (t₂, n = {a['t2']['K1']['n']})")
need("v1.9 retest C*", f"Retest t₁→t₂ {f(a['retest_C'],3)} (n = {a['retest_C_n']})")
need("v1.9 not rated", f"{f(a['t1']['share_C_not_rated'],3)} (t₁) and {f(a['t2']['share_C_not_rated'],3)} (t₂)")
floor = [x for k, x in C.items() if "FLOOR" in k]
k2 = [x[w]["K2"]["rho"] for x in floor for w in ("t1", "t2")]
need("v1.9 FLOOR K2 range", f"ρ(A, P) {f(min(k2),3)}–{f(max(k2),3)}", all(v > cal["constants"]["K2"] for v in k2))
sh = C["C_phi+SHRINK+ADD"]
need("v1.9 SHRINK K1", f"ρ(C\\*, P) {f(sh['t1']['K1']['rho'],3)} / {f(sh['t2']['K1']['rho'],3)}")
shr = [x for k, x in C.items() if "SHRINK" in k]
d1 = [x["t1"]["K3"]["dA"] for x in shr]; d2 = [x["t2"]["K3"]["dA"] for x in shr]
need("v1.9 SHRINK dA", f"ΔA {f(min(d1),1)}–{f(max(d1),1)} at t₁ and {f(min(d2),1)}–{f(max(d2),1)} at t₂ against ΔP + 5 = "
     f"{f(a['t1']['K3']['dP'] + cal['constants']['K3_slack'],1)} / {f(a['t2']['K3']['dP'] + cal['constants']['K3_slack'],1)}",
     not any(x[w]["K3"]["pass"] for x in shr for w in ("t1", "t2")))
j = C["C_phiJ+FLOOR+ADD"]
need("v1.9 phiJ", f"C_phiJ + FLOOR retests higher ({f(j['retest_C'],3)}) but sits on the K1 line ({f(j['t1']['K1']['rho'],3)} / {f(j['t2']['K1']['rho'],3)})")
need("v1.9 P retest", f"Presence retest t₁→t₂: {f(cal['presence_retest_t1_t2'],3)} (n = {cal['presence_retest_n']})")
need("v1.9 no composite", "no candidate", cal["selected"] is None and not any(x["passes_all"] for x in cal["candidates"]))
need("v1.9 floor n", "≥ 6 total mentions", cal["constants"]["floor_n"] == 6)

# v1.9 pre-registration text (pre-look and scale)
mod = git_text(REF, "osf/methodology/v1_9/prereg/v1_9_two_component_composite_content.py")
for lit, label in [("phi_max = F*M/(M-1) = 7.2", "phi_max 7.2"), ("C_phi 0.533 (n 83)", "pre-look C_phi retest"),
                   ("brands named once score 58.0 on average\n  (n 9) against 30.4 for brands never named (n 28)", "windfall"),
                   ("at mean 0.39 (95th pct 0.55)", "frame-shuffle null"), ("(12:15 am CT)", "Pablo confirmation time"),
                   ("brand-level n per substrate 16-24", "16-24 brands"), ('"confirmed_iff": "rho >= 0.80 AND p_perm < .05"', "PRS rule"),
                   ('"falsified_iff": "rho < 0.60 OR p_perm >= .05"', "PRS falsified"), ('"confirmed_iff": "|rho| <= 0.30"', "DIS rule"),
                   ('"falsified_iff": "|rho| >= 0.50"', "DIS falsified"), ('"confirmed_iff": "rho >= 0.50 AND p_frame < .05"', "CRS rule"),
                   ('"falsified_iff": "rho < 0.30 OR p_frame >= .05"', "CRS falsified")]:
    need("v1.9 module: " + label, "", lit in mod)
need("outline phi_max", "φ_max = 7.2 for M = F = 6")
need("outline pre-look 0.533", "against 0.533 for unfloored C_phi")
need("outline windfall", "58.0 on average (n = 9) against 30.4 for brands never named (n = 28)")
need("outline shuffle", "at mean 0.39 (95th percentile 0.55)")

# v0.41 pre-registration text
m41 = git_text("f515fb6", "osf/v41/prereg/v0_41_longitudinal_t3_omnibus_content.py")
for lit, label in [('"confirmed_iff": "rho >= 0.50 AND p_perm < 0.05 AND p_frame < 0.05 (SCORER_NOTES S2)"', "PHI rule"),
                   ('"falsified_iff": "rho < 0.30 OR p_perm >= 0.05"', "PHI falsified"),
                   ('"confirmed_iff": "rho >= 0.70 in >= 4/5 substrates"', "PLH rule"),
                   ('"falsified_iff": "rho < 0.50 in >= 3/5 substrates"', "PLH falsified"),
                   ('"confirmed_iff": "|rho| <= 0.30"', "DRD rule"),
                   ('"falsified_iff": "|rho| >= 0.50 with p_perm < 0.05"', "DRD falsified")]:
    need("v0.41 module: " + label, "", lit in m41)
fs = js("f515fb6", "osf/v41/prereg/frame_structure_floor_v0_41.json")
vals = [v for v in json.dumps(fs).replace(",", " ").split() if re.match(r"^0\.\d+", v)]
need("v0.41 frame floor file has 0.39/0.55", "", any(v.startswith("0.39") or v.startswith("0.38") for v in vals) and any(v.startswith("0.55") or v.startswith("0.54") for v in vals))
man = git_text("f515fb6", "osf/v41/prereg/acquisition_manifest_v41.md")
need("v0.41 t3 date", "locked date Nov 9, 2026", "| v0.19 | 2026-05-20 | 2026-06-10 | 2026-11-09 | 152 |" in man)

fails = 0
for label, s, truth in checks:
    ok = bool(truth) and (s == "" or s in text)
    if not ok:
        fails += 1
        why = "source" if not truth else "not in outline"
        print(f"FAIL [{why}] {label}: {s!r}")
print(f"{len(checks) - fails}/{len(checks)} checks pass")
sys.exit(1 if fails else 0)
