"""check_paper_numbers.py - AIAS 2.0 paper draft: quoted statistics against the data lock.

Every check derives the value from osf/aias_2_0/aias_2_0_synthesis_data.json (the data lock;
lineage records are embedded in it) or from the locked v0.41 / v1.9 verdict files, formats it
as the paper prints it, and requires that string in the draft.
Run from a checkout of branch aias-2.0:  python3 papers/aias_2_0/check_paper_numbers.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEXT = (ROOT / "papers/aias_2_0/aias_2_0_synthesis_paper_draft.md").read_text(encoding="utf-8")
D = json.load(open(ROOT / "osf/aias_2_0/aias_2_0_synthesis_data.json"))
V41 = json.load(open(ROOT / "osf/v41/v41_verdicts.json"))
L = D["lineage"]; S = D["summaries"]; V = D["stage2"]["v19_verdicts"]; W = D["stage2"]["v41_verdicts"]
CAL = L["v1.9-stage1"]["record"]; C = {c["spec"]: c for c in CAL["candidates"]}
checks = []


def need(label, s, truth=True):
    checks.append((label, s, bool(truth)))


f3 = lambda x: f"{x:.3f}"  # noqa: E731
need("status complete, class A", "class A", D["status"] == "complete" and D["stage2"]["class"]["class"] == "A")
v17 = L["v1.7"]["record"]["H_CPC_Dissociates"]["pooled"]["composite"]
need("v1.7 coupling", f"pooled ρ = {f3(v17['abs_rho'])}, n = {v17['n']}")
need("v1.7 abstract", f"(pooled ρ = {f3(v17['abs_rho'])})")
need("v1.7 defined rate", f"{L['v1.7']['record']['H_CPC_Defined']['pooled_defined_rate'] * 100:.1f}% of in-market brands")
v18 = L["v1.8"]["record"]["verdicts"]
need("v1.8 CV reproduces", f"|ρ(CV-CPC, μ)| = {f3(v18['H_CV_Reproduces']['stat']['abs_rho'])}, n = {v18['H_CV_Reproduces']['stat']['n']}")
mi = v18["H_MeanIndependent"]["stat"]["pooled"]
need("v1.8 mean-independent", f"pooled |ρ(φ, μ)| = {f3(mi['abs_rho'])}, n = {mi['n']}")
lr = v18["H_LowRecallDefined"]["stat"]
need("v1.8 defined", f"({lr['phi_defined']} of {lr['n_nonzero_surfacing']}, against {lr['cv_raw_defined']} for CV-CPC)")
pdis = v18["H_PositionalDissociation"]["stat"]
need("v1.8 phi-J", f"ρ(φ, J) = {pdis['rho']:.3f}, n = {pdis['n']}".replace("-", "−"))
need("K1 t1", f"{f3(S['t1']['rho_Cstar_P'])} in May (n = {S['t1']['rho_Cstar_P_n']})")
need("K1 t2", f"{f3(S['t2']['rho_Cstar_P'])} in June (n = {S['t2']['rho_Cstar_P_n']})")
dis = V["H_Dissociation_t3"]
need("DIS", f"{f3(abs(dis['rho']))} in November (n = {dis['n']})", dis["verdict"] == "CONFIRMED")
need("abstract three waves", f"(|ρ| = {f3(S['t1']['rho_Cstar_P'])}, {f3(S['t2']['rho_Cstar_P'])} and {f3(abs(dis['rho']))})")
dr = W["H_Drift_Dissociation"]
need("drift", f"ρ = {f3(dr['rho'])}, n = {dr['n']}; H_Drift_Dissociation CONFIRMED", dr["verdict"] == "CONFIRMED")
need("drift baseline", f"June coupling of {f3(dr['baseline_coupling_t2_rho'])}")
v37 = L["v0.37"]["record"]["verdicts"]["H_IL_Consistency"]["stat"]
need("v0.37", f"ρ = {v37['rho']:.3f}, p_perm = {f3(v37['p_perm'])}, n = {v37['n']}".replace("-", "−"))
need("rated counts", f"{S['t1']['n_rated']} of 112 brands were rated in May, {S['t2']['n_rated']} in June and {S['t3']['n_rated']} in November")
need("rated shares", "(" + ", ".join(f"{S[w]['n_rated'] / S[w]['n_units'] * 100:.0f}%" for w in ("t1", "t2")) +
     f" and {S['t3']['n_rated'] / S['t3']['n_units'] * 100:.0f}%)")
shares = [ps["n_rated"] / ps["n_units"] for w in ("t1", "t2", "t3") for ps in S[w]["per_substrate"].values()]
need("share range", f"ranges from {min(shares) * 100:.0f}% to {max(shares) * 100:.0f}%")
prs, crs = V["H_Presence_Score_Reliability"], V["H_Consistency_Reliability"]
need("P 3 weeks / 5 months", f"ρ = {CAL['presence_retest_t1_t2']:.3f} over three weeks and {f3(prs['rho'])} over five months (n = {prs['n']}",
     prs["verdict"] == "CONFIRMED")
pl = W["H_Presence_LongHorizon"]["per_substrate"]
need("PLH range", f"(ρ {min(v['rho'] for v in pl.values()):.3f}–{max(v['rho'] for v in pl.values()):.3f}, five of five above 0.70)",
     W["H_Presence_LongHorizon"]["verdict"] == "CONFIRMED" and W["H_Presence_LongHorizon"]["n_ge_070"] == 5)
sel = C["C_phi+FLOOR+ADD"]
need("C* 3 weeks", f"{f3(sel['retest_C'])} across three weeks (n = {sel['retest_C_n']})")
need("C* 5 months", f"{f3(crs['rho'])} across five months (n = {crs['n']})", crs["verdict"] == "CONFIRMED")
fn = crs["frame_structure_null"]
need("C* null", f"still averages {f3(fn['null_mean'])} (95th percentile {f3(fn['null_p95'])})")
need("C* p_frame", f"$p_{{\\text{{frame}}}}$ = {f3(fn['p_frame'])}), so H_Consistency_Reliability is CONFIRMED")
tw = L["v1.8"]["record"]["two_wave_reproducibility"]["phi_t1_t2_rank_agreement"]
phl = W["H_Phi_LongHorizon"]
need("phi", f"{f3(tw['rho'])} over three weeks (n = {tw['n']}) and {f3(phl['rho'])} over five months (n = {phl['n']})",
     phl["verdict"] == "CONFIRMED")
pfn = phl["frame_structure_null"]
need("phi null", f"null averaging {f3(pfn['null_mean'])} (95th percentile {f3(pfn['null_p95'])}; $p_{{\\text{{frame}}}}$ = {pfn['p_frame']:.4f})")
dec = V41["verdicts"]["H_Horizon_Decay"]
need("decay phi", f"(difference {f3(dec['phi']['D'])}, 95% CI {dec['phi']['ci95'][0]:.3f} to {f3(dec['phi']['ci95'][1])})".replace("-", "−"),
     dec["phi"]["verdict"] == "MARGINAL")
need("decay pi", f"({f3(dec['pi_hat']['D'])}, CI {dec['pi_hat']['ci95'][0]:.3f} to {f3(dec['pi_hat']['ci95'][1])})".replace("-", "−"),
     dec["pi_hat"]["verdict"] == "MARGINAL")
ph = V41["verdicts"]["H_Phantom_LongPersistence"]["pooled"]
need("phantom", f"Of the {ph['t2_phantom']} brands below the six-mention line in June (v0.34's recall floor), {ph['retained_t3']} were still")
need("phantom = unrated set (June)", "", ph["t2_phantom"] == S["t2"]["n_units"] - S["t2"]["n_rated"])
k2 = [c[w]["K2"]["rho"] for k, c in C.items() if "FLOOR" in k for w in ("t1", "t2")]
need("K2 range", f"ρ(A, P) = {min(k2):.3f}–{max(k2):.3f}")
sh = C["C_phi+SHRINK+ADD"]
need("SHRINK K1", f"ρ = {f3(sh['t1']['K1']['rho'])} and {f3(sh['t2']['K1']['rho'])} for φ")
dA = [c["t1"]["K3"]["dA"] for k, c in C.items() if "SHRINK" in k]
need("K3", f"{min(dA):.1f}–{max(dA):.1f} points in May against an allowance of {sel['t1']['K3']['dP'] + CAL['constants']['K3_slack']:.1f}")
j = C["C_phiJ+FLOOR+ADD"]
need("phiJ", f"({f3(j['retest_C'])}) but put Consistency on the K1 line ({f3(j['t1']['K1']['rho'])}, {f3(j['t2']['K1']['rho'])})")
need("Nov composite", f"(ρ = {f3(V['H_NoComposite_t3']['rho_A_P'])})")
need("abstract C* reliability", f"(ρ = {f3(crs['rho'])}, n = {crs['n']}, frame-structure p = {f3(fn['p_frame'])})")
need("abstract P reliability", f"(ρ = {f3(prs['rho'])}, n = {prs['n']})")
need("days t2->t3", "152 days", all(d["days_t2_t3"] == 152 for d in V41["delta_t"]))
d12 = [d["days_t1_t2"] for d in V41["delta_t"]]
need("days t1->t2", f"{min(d12)}–{max(d12)} days later")
mc = V41["manipulation_checks"]
need("852/852", "returned all 852 responses", mc["MC_Completeness"]["ok_total"] == 852 == mc["MC_Completeness"]["expected_total"])
need("snapshots", "served the same snapshots", mc["MC_Snapshot"]["status"] == "PASS")
v31 = L["v0.31"]["record"]["H_CPC_CrossCategory"]
need("v0.31", f"H = {v31['kruskal_H']:.2f}, p = {v31['kruskal_p']:.5f}")
v32 = L["v0.32"]["record"]; lo = v32["SENSITIVITY_leave_one_provider_out"]
need("v0.32", f"(ρ = {f3(v32['PRIMARY_H_ScoreRankStable']['rho'])})")
need("v0.32 LOPO", f"ρ {min(x['rho'] for x in lo.values()):.2f}–{max(x['rho'] for x in lo.values()):.2f}")
v33 = L["v0.33"]["record"]["H_Provider_Asymmetry"]
need("v0.33", f"= {f3(v33['mean_eta2_observed'])}, MC p = {v33['mc_p_onesided']:.4f}")
v34 = L["v0.34"]["record"]["verdicts"]["H_CPC_Temporal_Stability"]["per_substrate_rho"]
need("v0.34", f"ρ {min(v for k, v in v34.items() if k != 'v0.19'):.2f}–{max(v34.values()):.2f} in four of five categories; headphones {v34['v0.19']:.2f}")

fails = [(l, s) for l, s, t in checks if not t or (s and s not in TEXT)]
for l, s in fails:
    print(f"FAIL {l}: {s!r}")
print(f"{len(checks) - len(fails)}/{len(checks)} checks pass")
sys.exit(1 if fails else 0)
