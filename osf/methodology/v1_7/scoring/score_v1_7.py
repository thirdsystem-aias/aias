#!/usr/bin/env python3
"""
v1.7 — CPC Consistency Methodology Lock · retrospective scorer.

Locked against v1.7-prereg-r2 (anchored set narrowed to the canonical two-channel
trio v0.20 / v0.21 / v0.22; DEVIATIONS Entry 0). No new acquisition.

Single-source discipline: ALL methodology constants are read from the locked
pre-reg module prereg/v1_7_cpc_consistency_content.py (COMPUTATION + THRESHOLDS).
Mention detection REUSES each phase's own v1.4 canonical matcher
(scripts/score_v{20,21,22}.py :: detect_mention).

Computation (per brand b, across the fixed six-model panel; content.py:46-52):
    r_{b,k} = R_cat hits + R_cult hits for model k         (0..6 here: 3+3 frames)
    CPC_raw = sd_pop(r_{b,·}) / mean(r_{b,·})              (CV; ddof=0, whole panel)
    CPC     = 1 / (1 + CPC_raw)                            (0,1]
    floor   : mean(r_{b,·}) < mu_floor(1.0) -> CPC = N/A

Presence (for the dissociation test) = the canonical AIAS presence_composite
(osf/v25/scripts/score_v0_25.py): mean of [C_P/6, R_cat_total/18, R_cult_total/18].
It blends Phase A recognition breadth and both Phase B recall channels, so it
retains spread even where recognition C_P saturates. We also record a
recognition-only (C_P) and a recall-level (mean r) variant for robustness.

Outputs:
    osf/methodology/v1_7/data/v1_7_cpc.csv          per-brand CPC + presence components
    osf/methodology/v1_7/v1_7_cpc_verdicts.json     three-finding verdicts + per-substrate rho
    osf/methodology/v1_7/v1_7_run_log.md            certified input hashes + console summary
"""
import sys, json, csv, hashlib, warnings
from pathlib import Path
import numpy as np
from scipy import stats

ROOT = Path.home() / "aias"
sys.path.insert(0, str(ROOT / "prereg"))
sys.path.insert(0, str(ROOT / "scripts"))

# --- single-source constants from the locked pre-reg module ------------------
import v1_7_cpc_consistency_content as PREREG
PANEL_N   = PREREG.COMPUTATION["panel_n"]            # 6
DDOF      = PREREG.COMPUTATION["dispersion_ddof"]    # 0 (population sd)
MU_FLOOR  = PREREG.THRESHOLDS["mu_floor"]            # 1.0  (mean combined recall count)
DISS_CEIL = PREREG.THRESHOLDS["dissociation_ceiling"]  # 0.50
N_BOOT    = 10000
SEED      = 280400
SIG_ALPHA = 0.05

import score_v20, score_v21, score_v22

SUBSTRATES = [
    {"key": "v0.20", "name": "skincare",   "mod": score_v20,
     "reg": ("json",   ROOT / "prereg" / "v0_20_registry.json"),
     "pa": ROOT / "osf/v20/phase_a_results.csv", "pb": ROOT / "osf/v20/phase_b_results.csv"},
    {"key": "v0.21", "name": "cosmetics",  "mod": score_v21,
     "reg": ("json",   ROOT / "prereg" / "v0_21_registry.json"),
     "pa": ROOT / "osf/v21/phase_a_results.csv", "pb": ROOT / "osf/v21/phase_b_results.csv"},
    {"key": "v0.22", "name": "automotive", "mod": score_v22,
     "reg": ("module", ROOT / "prereg" / "v0_22_automotive_content.py"),
     "pa": ROOT / "osf/v22/phase_a_results.csv", "pb": ROOT / "osf/v22/phase_b_results.csv"},
]
PHANTOM_LABEL = "Defunct"   # Cell D label that marks pure-phantom brands


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()


def load_cells(sub):
    """Return [(brand, cell_key, cell_label, is_phantom), ...] for a substrate."""
    kind, path = sub["reg"]
    reg = sub["mod"].load_registry(path) if kind == "json" else sub["mod"].load_prereg_module(path)
    rows = []
    for ck, cv in reg["cells"].items():
        bs = cv.get("brands", []) if isinstance(cv, dict) else cv
        label = cv.get("label", "") if isinstance(cv, dict) else ""
        is_phantom = PHANTOM_LABEL.lower() in label.lower()
        for b in bs:
            name = b.get("name") if isinstance(b, dict) else b
            rows.append((name, ck, label, is_phantom))
    return rows


def read_csv(p):
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def score_substrate(sub):
    cells = load_cells(sub)
    pa = read_csv(sub["pa"])
    pb = read_csv(sub["pb"])
    detect = sub["mod"].detect_mention

    # Phase A: per-(brand,model) recognized bool -> C_P = count over panel
    recog = {}
    for r in pa:
        b, m = r["brand"], r["model"]
        recog.setdefault(b, {})
        recog[b][m] = (r["recognized"].strip().lower() == "yes")

    # Phase B rows grouped by model, split by channel
    models = sorted({r["model"] for r in pb})
    rows_by_model_chan = {m: {"R_cat": [], "R_cult": []} for m in models}
    for r in pb:
        m, ch = r["model"], r["channel"]
        if m in rows_by_model_chan and ch in ("R_cat", "R_cult"):
            rows_by_model_chan[m][ch].append(r["response_text"])
    assert len(models) == PANEL_N, f"{sub['key']}: expected {PANEL_N} models, got {len(models)}"

    records = {}
    for brand, ck, label, is_phantom in cells:
        r_vec = []          # combined recall count per model (0..6)
        rcat_total = rcult_total = 0
        for m in models:
            cat_hits  = sum(1 for txt in rows_by_model_chan[m]["R_cat"]  if detect(txt, brand))
            cult_hits = sum(1 for txt in rows_by_model_chan[m]["R_cult"] if detect(txt, brand))
            r_vec.append(cat_hits + cult_hits)
            rcat_total  += cat_hits
            rcult_total += cult_hits
        r = np.asarray(r_vec, float)
        mu = float(r.mean())
        sd = float(np.std(r, ddof=DDOF))
        defined = mu >= MU_FLOOR
        cpc_raw   = (sd / mu) if (defined and mu > 0) else None
        cpc_score = (1.0 / (1.0 + cpc_raw)) if cpc_raw is not None else None
        cpc_status = "defined" if defined else "N/A"

        c_p = int(sum(1 for v in recog.get(brand, {}).values() if v))
        # canonical AIAS presence_composite (v0.25): components scaled to 0..100
        presence_composite = float(np.mean([
            (c_p / PANEL_N) * 100,
            (rcat_total / 18) * 100,    # 6 models x 3 R_cat frames
            (rcult_total / 18) * 100,   # 6 models x 3 R_cult frames
        ]))
        records[brand] = {
            "brand": brand, "substrate": sub["key"], "cell": ck, "cell_label": label,
            "in_market": not is_phantom, "is_phantom": is_phantom,
            "r_per_model": r_vec, "mean_r": mu, "sd_pop": sd,
            "cpc_raw": cpc_raw, "cpc_score": cpc_score,
            "cpc_status": cpc_status, "cpc_panel_n": len(models),
            "C_P": c_p, "R_cat_total": rcat_total, "R_cult_total": rcult_total,
            "presence_composite": presence_composite,    # primary Presence
            "presence_recognition": c_p,                 # robustness variant
            "presence_recall_level": mu,                 # robustness variant
        }
    return {"key": sub["key"], "name": sub["name"], "records": records}


def spearman_ci(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    res = stats.spearmanr(x, y)
    rho, p = float(res.statistic), float(res.pvalue)
    ci_lo = ci_hi = float("nan")
    if len(x) >= 6 and len(set(x.tolist())) > 1 and len(set(y.tolist())) > 1:
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                bs = stats.bootstrap((x, y),
                    lambda a, b: stats.spearmanr(a, b).statistic,
                    paired=True, vectorized=False, n_resamples=N_BOOT,
                    method="BCa", random_state=SEED)
            ci_lo, ci_hi = float(bs.confidence_interval.low), float(bs.confidence_interval.high)
        except Exception:
            pass
    return {"rho": rho, "abs_rho": abs(rho), "p": p, "ci_low": ci_lo, "ci_high": ci_hi, "n": int(len(x))}


def quadrants(brands, cpc, pres):
    """Median-split CPC and Presence; return off-diagonal brand membership."""
    cpc = np.asarray(cpc, float); pres = np.asarray(pres, float)
    cpc_med, pres_med = float(np.median(cpc)), float(np.median(pres))
    hiP_loC, loP_hiC = [], []
    for b, c, p in zip(brands, cpc, pres):
        if p >= pres_med and c < cpc_med:  hiP_loC.append(b)
        if p < pres_med and c >= cpc_med:  loP_hiC.append(b)
    return {"cpc_median": cpc_med, "presence_median": pres_med,
            "high_presence_low_cpc": hiP_loC, "low_presence_high_cpc": loP_hiC,
            "off_diagonal_n": len(hiP_loC) + len(loP_hiC)}


def main():
    subs = [score_substrate(s) for s in SUBSTRATES]
    all_recs = {s["key"]: s["records"] for s in subs}

    # ---- F1  H_CPC_Defined: defined-rate among in-market brands ----
    f1_per = {}
    pooled_in, pooled_def = 0, 0
    for s in subs:
        inm = [r for r in s["records"].values() if r["in_market"]]
        deff = [r for r in inm if r["cpc_status"] == "defined"]
        na = [r["brand"] for r in inm if r["cpc_status"] == "N/A"]
        f1_per[s["key"]] = {"in_market_n": len(inm), "defined_n": len(deff),
                            "defined_rate": (len(deff) / len(inm) if inm else None),
                            "na_brands": na}
        pooled_in += len(inm); pooled_def += len(deff)
    pooled_rate = pooled_def / pooled_in if pooled_in else None
    # falsified if a material fraction of in-market brands return N/A
    F1 = "CONFIRM" if pooled_rate == 1.0 else ("REVIEW" if (pooled_rate or 0) >= 0.90 else "FALSIFIED")

    # ---- F2  H_CPC_Dissociates: rho(CPC, Presence) ----
    def gather(records):
        bs, cpc, pres, presR, presL = [], [], [], [], []
        for r in records:
            if r["in_market"] and r["cpc_score"] is not None:
                bs.append(r["brand"]); cpc.append(r["cpc_score"])
                pres.append(r["presence_composite"])
                presR.append(r["presence_recognition"]); presL.append(r["presence_recall_level"])
        return bs, cpc, pres, presR, presL

    per_sub_rho = {}
    for s in subs:
        bs, cpc, pres, presR, presL = gather(s["records"].values())
        per_sub_rho[s["key"]] = {
            "composite":   spearman_ci(cpc, pres),
            "recognition": spearman_ci(cpc, presR),
            "recall_level": spearman_ci(cpc, presL),
            "quadrants": quadrants(bs, cpc, pres) if len(bs) >= 2 else None,
            "n_defined_in_market": len(bs),
        }
    # pooled across the trio
    pbs, pcpc, ppres, ppresR, ppresL = [], [], [], [], []
    for s in subs:
        bs, cpc, pres, presR, presL = gather(s["records"].values())
        pbs += [f"{s['key']}:{b}" for b in bs]; pcpc += cpc; ppres += pres
        ppresR += presR; ppresL += presL
    pooled_rho   = spearman_ci(pcpc, ppres)
    pooled_rhoR  = spearman_ci(pcpc, ppresR)
    pooled_rhoL  = spearman_ci(pcpc, ppresL)
    pooled_quad  = quadrants(pbs, pcpc, ppres)
    any_offdiag = pooled_quad["off_diagonal_n"] > 0 or any(
        (v["quadrants"] and v["quadrants"]["off_diagonal_n"] > 0) for v in per_sub_rho.values())
    F2 = "CONFIRM" if (pooled_rho["abs_rho"] < DISS_CEIL and any_offdiag) else "FALSIFIED"

    # ---- F3  H_CPC_PhantomNull: every Cell D phantom returns N/A ----
    phantoms = [r for s in subs for r in s["records"].values() if r["is_phantom"]]
    offenders = [{"brand": r["brand"], "substrate": r["substrate"], "mean_r": r["mean_r"],
                  "cpc_status": r["cpc_status"]} for r in phantoms if r["cpc_status"] != "N/A"]
    F3 = ("CONFIRM" if phantoms and not offenders else
          ("FALSIFIED" if offenders else "UNDETERMINED"))  # UNDETERMINED only if no phantom cell exists

    # ---- write per-brand CSV ----
    out_dir = ROOT / "osf/methodology/v1_7/data"; out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "v1_7_cpc.csv"
    cols = ["brand", "substrate", "cell", "cell_label", "in_market", "is_phantom",
            "r_per_model", "mean_r", "sd_pop", "cpc_raw", "cpc_score", "cpc_status",
            "cpc_panel_n", "C_P", "R_cat_total", "R_cult_total",
            "presence_composite", "presence_recognition", "presence_recall_level"]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
        for s in subs:
            for r in s["records"].values():
                row = dict(r); row["r_per_model"] = json.dumps(row["r_per_model"])
                w.writerow({c: row[c] for c in cols})

    # ---- reconciliation vs v0.30 cpc_raw (same underlying recall) ----
    recon = {"checked": 0, "max_abs_diff": 0.0, "mismatches": []}
    v30_csv = ROOT / "osf/v30/data/v30_cpc.csv"
    if v30_csv.exists():
        v30 = {(r["substrate"], r["brand"]): r for r in read_csv(v30_csv)}
        for s in subs:
            for b, r in s["records"].items():
                key = (s["key"], b)
                if r["cpc_raw"] is None or key not in v30:
                    continue
                v = v30[key].get("cpc_raw", "")
                if v in ("", "None", None):
                    continue
                diff = abs(r["cpc_raw"] - float(v))
                recon["checked"] += 1
                recon["max_abs_diff"] = max(recon["max_abs_diff"], diff)
                if diff > 1e-9:
                    recon["mismatches"].append({"brand": b, "substrate": s["key"],
                                                "v1_7": r["cpc_raw"], "v0_30": float(v), "diff": diff})

    certified = {s["key"]: {"phase_a": sha256(s["pa"]), "phase_b": sha256(s["pb"])} for s in SUBSTRATES}
    verdicts = {
        "phase": "v1.7", "component": "CPC", "lock": "v1.7-prereg-r2",
        "no_new_llm_calls": True,
        "constants_source": "prereg/v1_7_cpc_consistency_content.py",
        "anchored_set": [{"key": s["key"], "name": s["name"]} for s in subs],
        "thresholds": {"mu_floor": MU_FLOOR, "dissociation_ceiling": DISS_CEIL,
                       "dispersion_ddof": DDOF, "panel_n": PANEL_N},
        "r_range_note": ("r=R_cat+R_cult is 0..6 (3+3 frames/channel), not the spec's "
                         "annotated 0..12; CV is scale-invariant so CPC is unaffected."),
        "presence_note": ("Primary Presence = canonical presence_composite "
                          "(mean of C_P/6, R_cat/18, R_cult/18); recognition-only and "
                          "recall-level variants reported for robustness."),
        "H_CPC_Defined":   {"verdict": F1, "pooled_defined_rate": pooled_rate, "per_substrate": f1_per},
        "H_CPC_Dissociates": {
            "verdict": F2, "ceiling": DISS_CEIL,
            "pooled": {"composite": pooled_rho, "recognition": pooled_rhoR, "recall_level": pooled_rhoL,
                       "quadrants": pooled_quad},
            "per_substrate": per_sub_rho,
            "any_off_diagonal": bool(any_offdiag),
        },
        "H_CPC_PhantomNull": {"verdict": F3, "n_phantoms": len(phantoms),
                              "phantom_cell_substrates": ["v0.22"], "offenders": offenders,
                              "phantoms": [{"brand": r["brand"], "substrate": r["substrate"],
                                            "mean_r": r["mean_r"], "cpc_status": r["cpc_status"]}
                                           for r in phantoms]},
        "reconciliation_vs_v0_30": recon,
        "certified_inputs_sha256": certified,
        "bootstrap": {"resamples": N_BOOT, "seed": SEED, "method": "BCa", "ci": "95%"},
    }
    vpath = ROOT / "osf/methodology/v1_7/v1_7_cpc_verdicts.json"
    with open(vpath, "w") as f:
        json.dump(verdicts, f, indent=2)

    # ---- run log + console summary ----
    lines = []
    def out(s=""):
        print(s); lines.append(s)
    out("=" * 78)
    out("v1.7 (CPC) verdicts — lock v1.7-prereg-r2  |  trio: skincare / cosmetics / automotive")
    out("=" * 78)
    out(f"  H_CPC_Defined      : {F1}   (pooled defined-rate {pooled_rate*100:.0f}% of {pooled_in} in-market)")
    for k, v in f1_per.items():
        na = f"  N/A: {v['na_brands']}" if v["na_brands"] else ""
        out(f"      {k}: {v['defined_n']}/{v['in_market_n']} defined ({v['defined_rate']*100:.0f}%){na}")
    out(f"  H_CPC_Dissociates  : {F2}   [load-bearing]")
    out(f"      pooled |rho(CPC, Presence_composite)| = {pooled_rho['abs_rho']:.3f}  "
        f"(rho={pooled_rho['rho']:.3f}, p={pooled_rho['p']:.3g}, "
        f"95% BCa [{pooled_rho['ci_low']:.3f}, {pooled_rho['ci_high']:.3f}], n={pooled_rho['n']}) vs ceiling {DISS_CEIL}")
    out(f"      pooled |rho| recognition-only={pooled_rhoR['abs_rho']:.3f}  recall-level={pooled_rhoL['abs_rho']:.3f}")
    for k, v in per_sub_rho.items():
        c = v["composite"]; q = v["quadrants"]
        od = q["off_diagonal_n"] if q else 0
        out(f"      {k}: rho={c['rho']:+.3f} |rho|={c['abs_rho']:.3f} (n={c['n']}) off-diag brands={od}")
    out(f"      off-diagonal occupancy (pooled): hiP/loC={pooled_quad['high_presence_low_cpc']}")
    out(f"                                       loP/hiC={pooled_quad['low_presence_high_cpc']}")
    out(f"  H_CPC_PhantomNull  : {F3}   ({len(phantoms)} Cell-D phantoms; offenders={[o['brand'] for o in offenders]})")
    out("")
    out(f"  reconciliation vs v0.30 cpc_raw: checked {recon['checked']} brands, "
        f"max|Δ|={recon['max_abs_diff']:.2e}  -> {'OK' if recon['max_abs_diff'] < 1e-9 else 'MISMATCH'}")
    out(f"  wrote: {csv_path}")
    out(f"  wrote: {vpath}")

    log_path = ROOT / "osf/methodology/v1_7/v1_7_run_log.md"
    with open(log_path, "w") as f:
        f.write("# v1.7 CPC scoring run log\n\n```\n" + "\n".join(lines) + "\n```\n\n")
        f.write("## Certified input hashes (SHA256)\n\n")
        for k, v in certified.items():
            f.write(f"- {k}: phase_a `{v['phase_a']}`  phase_b `{v['phase_b']}`\n")
    print(f"  wrote: {log_path}")
    return verdicts


if __name__ == "__main__":
    main()
