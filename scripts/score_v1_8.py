#!/usr/bin/env python3
"""
score_v1_8.py — AIAS(TM) v1.8 CPC instrument scorer (DRAFT for review).

Scores the LOCKED v1.8 pre-registration (tag v1.8-prereg-r3) against the frozen
v0.19-v0.23 omnibus, in its three framings (v0.34 two-wave / v0.35 phantom
roster / v0.36 low-recall stratum). Produces:
    osf/methodology/v1_8/v1_8_verdicts.json          (per-hypothesis verdicts)
    osf/methodology/v1_8/v1_8_instrument_table.csv   (supplementary per-brand)

ONE-WAY BOUNDARY (program discipline):
    Running this script with --run is the first scoring call — the irreversible
    crossing past the externally-anchored pre-registration. Without --run the
    script computes NOTHING (it prints this notice and exits). Do not author any
    prose finding anywhere before v1_8_verdicts.json exists.

SPEC THIS IMPLEMENTS (forks A-D, locked):
  A  phi computed on pi_hat in (0,1); BOTH the true-zero floor (pi_hat=0) and the
     saturation ceiling (pi_hat=1) are partitioned out as pre-specified exclusions,
     counts reported separately.
  B  v1.7's certified CV-CPC function reused UNMODIFIED as the H_CV_Reproduces
     baseline; phi coverage reported against BOTH CPC_raw and CPC_corr;
     H_LowRecallDefined verdict follows the actual pi_hat distribution
     (UNDETERMINED is an honest outcome if the ceiling breaks strict containment).
  C  Stage 0 verifies v0.23 frame granularity; J spans only the frame-resolved
     substrates; phi spans all five regardless; coverage reported.
  D  within-framing ranks pooled for the blocking-factor rho; per-framing rho
     reported alongside.

DESIGN INVARIANTS (read, never hardcode):
  - M, F (channel-agnostic primary), F_chan (secondary), THRESHOLDS, HYPOTHESES,
    VERDICT_KEYS all come from the locked content module.
  - Surfacing extraction reuses the CERTIFIED lineage unmodified and consumes
    score_v33's RECONCILED per-model counts (its reconciliation gate), not raw
    per-substrate counts. CV-CPC reuses score_v1_7 (CPC_raw) + score_v30 (CPC_corr).
  - phi / J are NEW v1.8 instruments implemented directly from the locked formula.

RUN PREREQUISITES (must be materialized into the working tree before --run; they
live on other phase branches, not v1.8):
  modules : scripts/score_v33.py, scripts/score_v0_31.py  (+ score_v20/21/22.py,
            score_v30.py, osf/methodology/v1_7/scoring/score_v1_7.py — present)
  data    : t1 wave osf/{v19..v23}/...                     (present)
            t2 wave osf/v34/data/{v19..v23}/...             (v0.34 branch)
            osf/v33/data/v33_eta2.csv                       (v0.33 branch)
            osf/v35/data/v35_phantom_roster.csv             (v0.35 branch)
            osf/v36/... low-recall stratum definition       (v0.36 branch)
            osf/methodology/v1_7/data/v1_7_cpc.csv          (reconciliation ref; present)
  Missing inputs raise loudly (assert / FileNotFoundError); nothing is silently skipped.

Items flagged RUNTIME-VERIFY are integration seams to confirm at the review/run
boundary (v0.23 frame granularity; v0.35 roster membership column; v0.36 stratum
definition). Each is guarded so a wrong assumption fails loudly rather than
producing a quiet wrong number.
"""

import sys, os, json, csv, argparse, itertools
from pathlib import Path

import numpy as np
from scipy import stats

ROOT = Path.home() / "aias"

# --- import paths for the locked module + the certified lineage --------------
sys.path.insert(0, str(ROOT / "prereg"))                       # locked v1.8 module
sys.path.insert(0, str(ROOT / "scripts"))                      # score_v33, score_v0_31, score_v20/21/22, score_v30
sys.path.insert(0, str(ROOT / "osf/methodology/v1_7/scoring")) # score_v1_7 (CPC_raw certified)

import v1_8_consistency_instrument_content as PREREG           # the locked record (r3)

# ---------------------------------------------------------------------------
# Locked constants — read from the module, never hardcoded.
# ---------------------------------------------------------------------------
M        = PREREG.COMPUTATION["panel_n"]                 # 6 models
F        = PREREG.COMPUTATION["frames_per_model"]         # 6  (channel-agnostic primary)
F_CHAN   = PREREG.COMPUTATION["frames_per_channel"]       # 3  (per-channel secondary)
MF       = M * F                                          # 36 (primary denominator)
TH       = PREREG.THRESHOLDS
VK       = PREREG.VERDICT_KEYS
HYPS     = {h["id"]: h for h in PREREG.HYPOTHESES}
SEC      = PREREG.COMPUTATION["per_channel_secondary"]    # scope/excludes for the secondary diagnostic

CEIL_MI   = TH["mean_independence_ceiling"]        # 0.50 (make-or-break)
FLOOR_CV  = TH["cv_reproduces_floor"]              # 0.50
CEIL_PD   = TH["positional_dissociation_ceiling"]  # 0.70
TRIG_J    = TH["J_small_set_trigger"]              # 0.50
TARGET_LR = TH["low_recall_defined_target"]        # 1.00

OMNI = ["v0.19", "v0.20", "v0.21", "v0.22", "v0.23"]   # full channel-agnostic omnibus (phi spans all)
SEC_SUBS = ["v0.20", "v0.21", "v0.22"]                  # per-channel secondary scope (canonical 2-channel)

# r4 RULING (locked module + DEVIATIONS Entry 3): the reachable "low-recall gain HOLDS, but
# the by-design pi_hat=1 ceiling breaks strict containment" outcome routes to the structural
# cell [3] PARTIAL-STRUCTURAL. Cell [1] is now PARTIAL-IMPLEMENTATION — a residual undefined
# for a NON-ceiling reason, structurally unreachable (phi is total on (0,1)) and retained as a
# fail-loud guard; verdicts() asserts every residual-undefined >=1-surfacing brand is saturated.
LOWRECALL_CEILING_ROUTE = VK["H_LowRecallDefined"][3]   # PARTIAL-STRUCTURAL


# ===========================================================================
# STAGE 0 — surfacing (certified extraction; consume score_v33 reconciled output)
# ===========================================================================
def stage0_primary_counts():
    """
    Channel-agnostic per-model counts k(b,m) in 0..F via the CERTIFIED lineage,
    CONSUMING score_v33.recall_counts() + reconciliation_gate() (not raw counts).
    Returns: counts {sub: {brand: [M counts in PANEL order]}}, cells {sub:{brand:cell}},
             recon (the gate result), PANEL (model order).
    """
    import score_v33 as V33                  # certified orchestrator (pulls S31, score_v20/21/22)
    PANEL = V33.PANEL
    assert len(PANEL) == M, f"PANEL has {len(PANEL)} models, locked M={M}"

    rc = V33.recall_counts()                 # {sub: ({brand:[6]}, {brand:cell})}
    counts = {k: v[0] for k, v in rc.items()}
    cells  = {k: v[1] for k, v in rc.items()}

    recon = V33.reconciliation_gate(rc)      # bit-for-bit vs v1.7 r_per_model (v0.20/21/22)
    assert recon["passed"], f"reconciliation gate FAILED: {recon['mismatches'][:3]}"

    # geometry guard: every per-model count must lie in 0..F (channel-agnostic 0..6)
    for sub in OMNI:
        for b, vec in counts[sub].items():
            assert len(vec) == M, f"{sub}/{b}: {len(vec)} models != M={M}"
            assert all(0 <= int(x) <= F for x in vec), f"{sub}/{b}: count outside 0..{F}: {vec}"
    return counts, cells, recon, PANEL


def stage0_frame_surfacing(panel):
    """
    Frame-level surfacing S(b,m) = {frames where b surfaced under model m}, for J.
    Frame-resolved substrates only (Fork C). Reuses the certified matchers:
      v0.19      : pre-scored 'mentioned' per (brand, panel_model, frame)
      v0.20-0.22 : score_v{20,21,22}.detect_mention(response_text, brand) per (model, frame_id)
      v0.23      : RUNTIME-VERIFY frame granularity; include only if frame-resolved
    Returns: frames {sub: {brand: {model: set(frame_ids)}}}, frame_resolved {sub: bool}.
    Each substrate's frame-summed surfacing is asserted to equal the Stage-0 per-model
    count (consistency of the frame view with the reconciled aggregate).
    """
    import score_v0_31 as S31
    import score_v20, score_v21, score_v22
    V = ROOT / "osf"
    frames, resolved = {}, {}

    # --- v0.19: single-channel, pre-scored 'mentioned' per frame -------------
    f19 = {}
    rows = S31.read_csv(V / "v19/phase_b_results.csv")
    for r in rows:
        b, m, fr = r["brand"], r["panel_model"], r["frame"]
        if m not in panel:
            continue
        f19.setdefault(b, {}).setdefault(m, set())
        if str(r["mentioned"]).strip() == "1":
            f19[b][m].add(fr)
    frames["v0.19"], resolved["v0.19"] = f19, True

    # --- v0.20/21/22: certified detect_mention per (model, frame_id) ---------
    detect = {"v0.20": score_v20.detect_mention, "v0.21": score_v21.detect_mention,
              "v0.22": score_v22.detect_mention}
    reg = {"v0.20": ROOT / "prereg/v0_20_registry.json", "v0.21": ROOT / "prereg/v0_21_registry.json",
           "v0.22": ROOT / "prereg/v0_22_automotive_content.py"}
    for sub in ("v0.20", "v0.21", "v0.22"):
        brands = _registry_brands(sub, reg[sub], S31)
        det = detect[sub]
        pb = S31.read_csv(V / f"{sub.replace('v0.', 'v')}/phase_b_results.csv")
        fmap = {}
        for r in pb:
            m, fr, txt = r["model"], r["frame_id"], r["response_text"]
            if m not in panel:
                continue
            for b in brands:
                if det(txt, b):
                    fmap.setdefault(b, {}).setdefault(m, set()).add(fr)
        # brands with no surfacing still need empty entries for J's domain test
        for b in brands:
            fmap.setdefault(b, {})
        frames[sub], resolved[sub] = fmap, True

    # --- v0.23: RUNTIME-VERIFY frame granularity (Fork C) --------------------
    # v0.23 phase_b is JSON with probe_id + channel + brand_mentions. J needs >=2
    # distinct frames per model. We treat it as frame-resolved IFF probe_id yields
    # >=2 frames per model; otherwise J excludes v0.23 (phi still includes it).
    f23, ok23 = _v23_frame_surfacing(V / "v23/data/v23_phase_b_scored.json", panel)
    frames["v0.23"], resolved["v0.23"] = f23, ok23

    return frames, resolved


def _registry_brands(sub, reg_path, S31):
    """Brand list for a raw-text substrate, via the same registry the certified
    matcher was certified against. RUNTIME-VERIFY: mirror score_v33.RECON_CFG kinds."""
    import score_v33 as V33
    rk, rp, mod, pb = V33.RECON_CFG[sub]
    counts, _ = S31.counts_raw_text(rk, rp, mod, pb)   # certified extraction
    return sorted(counts.keys())


def _v23_frame_surfacing(path, panel):
    """v0.23 frame-level surfacing if resolvable. VERIFIED schema: frame key = probe_id
    (CC-1..3 / EA-1..3 -> 6/model); brand_mentions is a CODED DICT {brand_id: 0/1}
    keyed S01.. (mirrors score_v0_31.counts_v23 brand keys, so J matches the count path).
    Returns ({brand_id:{model:set(probe_ids)}}, frame_resolved)."""
    data = json.load(open(path))
    fkey = "probe_id"
    assert all(fkey in r for r in data), "v23: probe_id missing — frame granularity unverified"
    per_model_frames = {}
    for r in data:
        m = r.get("model_id")
        if m in panel:
            per_model_frames.setdefault(m, set()).add(r.get(fkey))
    ok = bool(per_model_frames) and min(len(v) for v in per_model_frames.values()) >= 2
    if not ok:
        return {}, False
    fmap = {}
    for r in data:
        m = r.get("model_id")
        if m not in panel:
            continue
        for b, v in (r.get("brand_mentions") or {}).items():   # coded dict {S01: 0/1}
            fmap.setdefault(b, {}).setdefault(m, set())
            if v:
                fmap[b][m].add(r.get(fkey))
    return fmap, True


def assert_frame_count_consistency(frames, counts, panel):
    """Stage-0 cross-check (fail loud): the frame-level surfacing summed per model MUST
    equal the reconciled per-model count. A mismatch means the J frame-path and the phi
    count-path disagree -> a silent extraction bug. (v23 keys are S01.. brand-ids on both
    sides; v19/v20-22 keys are brand names on both sides.) Brand SETS must align: a brand in
    only one path fails loud (a count-only brand is allowed iff it never surfaced)."""
    for sub, fmap in frames.items():
        cnt = counts[sub]
        fb, cb = set(fmap), set(cnt)
        extra = fb - cb
        assert not extra, f"{sub}: brands in frame-path but absent from count-path: {sorted(extra)[:5]}"
        for b in (cb - fb):     # count-only brands allowed ONLY if they never surfaced
            assert sum(int(x) for x in cnt[b]) == 0, \
                f"{sub}: {b} has reconciled counts but no frame-path entry (extraction gap)"
        for b, mm in fmap.items():
            vec = cnt[b]
            for i, m in enumerate(panel):
                got = len(mm.get(m, ()))
                assert got == int(vec[i]), \
                    f"frame/count mismatch {sub}/{b}/{m}: frames={got} reconciled_count={vec[i]}"


# ===========================================================================
# STAGE 1 — instruments (phi / J primary; CV-CPC baseline; per-channel secondary)
# ===========================================================================
def phi_of(counts_vec):
    """
    phi_b = [1/(M-1)] * sum_m (k - F*pi_hat)^2 / [F*pi_hat*(1-pi_hat)]   (locked formula).
    Channel-agnostic: k in 0..F, pi_hat = sum_k/(M*F). Fork A partition:
      pi_hat == 0  -> 'zero'       (true-zero floor; excluded)
      pi_hat == 1  -> 'saturated'  (ceiling; excluded)
      else         -> 'defined'    -> finite phi.
    Returns (phi or None, pi_hat, partition_label).
    """
    k = np.asarray(counts_vec, float)
    pi = float(k.sum() / MF)
    if pi <= 0.0:
        return None, pi, "zero"
    if pi >= 1.0:
        return None, pi, "saturated"
    denom = F * pi * (1.0 - pi)
    phi = float(((k - F * pi) ** 2).sum() / denom / (M - 1))
    return phi, pi, "defined"


def jaccard_of(model_to_frames):
    """J_b = mean over model pairs of |S_m ∩ S_m'| / |S_m ∪ S_m'|. Defined for >=1
    surfacing across >=2 models. Returns (J or None, n_models_surfacing)."""
    sets = [frozenset(s) for s in model_to_frames.values() if s]
    if len(sets) < 2:
        return None, len(sets)
    vals = []
    for a, b in itertools.combinations(sets, 2):
        union = a | b
        vals.append(len(a & b) / len(union) if union else 0.0)
    return (float(np.mean(vals)) if vals else None), len(sets)


def cvcpc_of(counts_vec):
    """
    CERTIFIED CV-CPC baseline, reused unmodified:
      CPC_raw  (v1.7)  : sd/mu on the per-model COUNT vector, defined iff mu>=MU_FLOOR and mu>0
      CPC_corr (v30)   : sd/sqrt(pi(1-pi)) on the RATE pi=mu/F, defined iff 0<pi<1
    sd is the population sd (DDOF read from the v1.7 prereg). Returns dict of values + defined flags.
    """
    import score_v1_7 as V17                 # certified CPC_raw constants/logic
    DDOF     = V17.DDOF                       # 0
    MU_FLOOR = V17.MU_FLOOR                   # 1.0
    k = np.asarray(counts_vec, float)
    mu = float(k.mean())
    sd = float(np.std(k, ddof=DDOF))
    raw_def = (mu >= MU_FLOOR and mu > 0.0)
    cpc_raw = (sd / mu) if raw_def else None             # v1.7 certified
    pi = mu / F
    corr_def = (0.0 < pi < 1.0)
    cpc_corr = (sd / np.sqrt(pi * (1.0 - pi))) if corr_def else None   # v30 Bhatia-Davis certified
    return {"mu_count": mu, "sd_pop": sd, "cpc_raw": cpc_raw, "cpc_raw_defined": raw_def,
            "cpc_corr": cpc_corr, "cpc_corr_defined": corr_def}


def _mu_floor():
    """v1.7's certified MU_FLOOR (count threshold gating CPC_raw / the gain-set boundary)."""
    import score_v1_7 as V17
    return V17.MU_FLOOR


def _cv_parity_check():
    """Belt-and-suspenders parity on the reproduced CV-CPC vs hand-verified values.
    Vector [0,0,0,0,0,6]: mu_count=1.0, sd_pop=sqrt(5); cpc_raw=sd/mu=sqrt(5);
    pi=1/6 -> cpc_corr = sqrt(5)/sqrt((1/6)(5/6)) = 6.0 exactly."""
    r = cvcpc_of([0, 0, 0, 0, 0, 6])
    assert abs(r["mu_count"] - 1.0) < 1e-12, r["mu_count"]
    assert abs(r["sd_pop"]  - 5 ** 0.5) < 1e-9, r["sd_pop"]
    assert abs(r["cpc_raw"] - 5 ** 0.5) < 1e-9, r["cpc_raw"]
    assert abs(r["cpc_corr"] - 6.0) < 1e-9, r["cpc_corr"]


def build_instrument_table(counts, cells, frames, resolved):
    """Per-(substrate, brand) primary instruments + CV-CPC baseline + partition labels."""
    table = []
    for sub in OMNI:
        for b, vec in counts[sub].items():
            phi, pi, part = phi_of(vec)
            cv = cvcpc_of(vec)
            if resolved.get(sub) and b in frames.get(sub, {}):
                J, nJ = jaccard_of(frames[sub][b])
            else:
                J, nJ = None, 0
            row = {
                "substrate": sub, "brand": b, "cell": cells[sub].get(b, ""),
                "k_per_model": list(int(x) for x in vec),
                "pi_hat": pi, "mu": pi,                 # mu == pi_hat (the level, for rho(phi,mu))
                "phi": phi, "phi_partition": part, "phi_defined": part == "defined",
                "J": J, "J_n_models": nJ, "J_defined": J is not None,
                "J_frame_resolved_substrate": bool(resolved.get(sub)),
                **cv,
            }
            table.append(row)
    return table


def per_channel_secondary(panel):
    """
    SECONDARY, NON-GATING diagnostic: per-channel phi / J (R_cat, R_cult) on v0.20-0.22.
    Reuses detect_mention per (model, frame_id, channel). F=F_CHAN per channel.
    RUNTIME-VERIFY: v0.19 (single-channel) and v0.23 (non-canonical) are excluded by spec.
    Returns {sub: {channel: {brand: {phi, pi_hat, J}}}}.
    """
    import score_v0_31 as S31
    import score_v20, score_v21, score_v22
    V = ROOT / "osf"
    det = {"v0.20": score_v20.detect_mention, "v0.21": score_v21.detect_mention,
           "v0.22": score_v22.detect_mention}
    reg = {"v0.20": ROOT / "prereg/v0_20_registry.json", "v0.21": ROOT / "prereg/v0_21_registry.json",
           "v0.22": ROOT / "prereg/v0_22_automotive_content.py"}
    out = {}
    for sub in SEC_SUBS:
        brands = _registry_brands(sub, reg[sub], S31)
        pb = S31.read_csv(V / f"{sub.replace('v0.', 'v')}/phase_b_results.csv")
        chans = sorted({r["channel"] for r in pb})
        assert set(chans) == {"R_cat", "R_cult"}, f"{sub}: non-canonical channels {chans}"
        out[sub] = {}
        for ch in chans:
            # per-model count k(b,m) over this channel's F_CHAN frames; frame sets for J
            kc = {b: {m: 0 for m in panel} for b in brands}
            fc = {b: {m: set() for m in panel} for b in brands}
            for r in pb:
                if r["channel"] != ch or r["model"] not in panel:
                    continue
                for b in brands:
                    if det[sub](r["response_text"], b):
                        kc[b][r["model"]] += 1
                        fc[b][r["model"]].add(r["frame_id"])
            res = {}
            for b in brands:
                vec = [kc[b][m] for m in panel]
                phi, pi, part = _phi_chan(vec)
                J, _ = jaccard_of(fc[b])
                res[b] = {"phi": phi, "pi_hat": pi, "phi_partition": part, "J": J}
            out[sub][ch] = res
    return out


def _phi_chan(counts_vec):
    """phi on a single channel: F = F_CHAN, M*F = M*F_CHAN (=18). Same partition rule."""
    mf = M * F_CHAN
    k = np.asarray(counts_vec, float)
    pi = float(k.sum() / mf)
    if pi <= 0.0:
        return None, pi, "zero"
    if pi >= 1.0:
        return None, pi, "saturated"
    denom = F_CHAN * pi * (1.0 - pi)
    return float(((k - F_CHAN * pi) ** 2).sum() / denom / (M - 1)), pi, "defined"


# ===========================================================================
# STAGE 2 — rho per framing, then pooled with framing as a blocking factor (Fork D)
# ===========================================================================
def framing_membership(table):
    """
    The three framings are brand-subset / two-wave views of the one omnibus.
      v0.34 : two-wave reproducibility — handled separately (phi at t1 vs t2).
              Its rho(phi,mu) here uses the canonical (t1) omnibus.
      v0.35 : phantom roster subset (RUNTIME-VERIFY membership column in v35_phantom_roster.csv)
      v0.36 : low-recall stratum subset (RUNTIME-VERIFY stratum definition; the CV-undefined cohort)
    Returns ({framing: set((substrate, brand))}, v35_phantom_subset).
    """
    import score_v0_31 as S31
    omni_keys = {(r["substrate"], r["brand"]) for r in table}
    members = {"v0.34": set(omni_keys)}   # full omnibus at t1

    # v0.35 — VERIFIED roster schema: group in {non_phantom(55), phantom_analyzable(29),
    #         phantom_excluded(28)}. The "84-unit baseline" = non_phantom + phantom_analyzable
    #         (excludes the 28 pi_hat=0 true-zeros). The phantom SUBSET tested by
    #         H_PhantomSignature is phantom_analyzable (the >=1-surfacing near-phantoms).
    roster = ROOT / "osf/v35/data/v35_phantom_roster.csv"
    baseline_84, phantom = set(), set()
    for r in S31.read_csv(roster):
        key = (r["substrate"], r["brand"])
        g = str(r.get("group", "")).strip()
        if g in ("non_phantom", "phantom_analyzable"):
            baseline_84.add(key)
        if g == "phantom_analyzable":
            phantom.add(key)
    members["v0.35"] = baseline_84 & omni_keys
    v35_phantom = phantom & omni_keys

    # v0.36 — low-recall stratum = phi-defined AND CV-CPC_raw-UNDEFINED == the gain set
    #         {0 < pi_hat < MU_FLOOR/F} (cpc_raw_defined carries v1.7's MU_FLOOR). Derivation
    #         governs; cross-checked against any v0.36 cohort record at run time, not read from one.
    members["v0.36"] = {(r["substrate"], r["brand"]) for r in table
                        if r["phi_defined"] and not r["cpc_raw_defined"]}
    return members, v35_phantom


def rho_phi_mu(table, members):
    """Spearman rho(phi, mu) per framing (Fork D), then pooled via within-framing ranks."""
    by_key = {(r["substrate"], r["brand"]): r for r in table}
    per = {}
    pooled_rp, pooled_rm = [], []
    for fr, keys in members.items():
        rows = [by_key[k] for k in keys if k in by_key and by_key[k]["phi_defined"]]
        phis = np.array([r["phi"] for r in rows], float)
        mus  = np.array([r["mu"] for r in rows], float)
        per[fr] = _spearman(phis, mus)
        if len(rows) >= 3:
            pooled_rp.append(stats.rankdata(phis))   # rank WITHIN framing
            pooled_rm.append(stats.rankdata(mus))
    pr = np.concatenate(pooled_rp) if pooled_rp else np.array([])
    pm = np.concatenate(pooled_rm) if pooled_rm else np.array([])
    pooled = _spearman(pr, pm, already_ranked=True)
    return {"per_framing": per, "pooled": pooled}


def rho_generic(table, xkey, ykey, defined_pred):
    """Spearman over the omnibus for an (x,y) pair on rows satisfying defined_pred."""
    rows = [r for r in table if defined_pred(r)]
    x = np.array([r[xkey] for r in rows], float)
    y = np.array([r[ykey] for r in rows], float)
    return _spearman(x, y), len(rows)


def _spearman(x, y, already_ranked=False):
    if len(x) < 3 or len(y) < 3:
        return {"rho": None, "p": None, "n": int(min(len(x), len(y))), "note": "n<3"}
    if already_ranked:
        rho, p = stats.pearsonr(x, y)
    else:
        rho, p = stats.spearmanr(x, y)
    return {"rho": float(rho), "abs_rho": abs(float(rho)), "p": float(p), "n": int(len(x))}


# ===========================================================================
# STAGE 3 — verdicts against the locked matrix (VERDICT_KEYS)
# ===========================================================================
def _pick(hyp_id, predicate_to_key):
    """Choose the matrix cell whose predicate is True; assert it is a locked VERDICT_KEYS entry."""
    chosen = next((k for pred, k in predicate_to_key if pred), None)
    assert chosen is not None, f"{hyp_id}: no verdict cell matched (matrix non-exhaustive?)"
    assert chosen in VK[hyp_id], f"{hyp_id}: '{chosen}' not in locked VERDICT_KEYS"
    return chosen


def verdicts(table, members, v35_phantom, recon, frame_resolved):
    out = {}

    # --- H_CV_Reproduces: |rho(CV-CPC_raw, mu)| >= floor ---------------------
    cv = rho_generic(table, "cpc_raw", "mu",
                     lambda r: r["cpc_raw_defined"] and r["phi_partition"] != "zero")
    cvr, n = cv
    a = cvr["abs_rho"]
    out["H_CV_Reproduces"] = {
        "verdict": _pick("H_CV_Reproduces", [
            (a is not None and a >= FLOOR_CV, VK["H_CV_Reproduces"][0]),
            (True,                            VK["H_CV_Reproduces"][1]),
        ]),
        "stat": cvr, "threshold": f"|rho(CV-CPC_raw, mu)| >= {FLOOR_CV}",
    }

    # --- H_MeanIndependent (MAKE-OR-BREAK): |rho(phi, mu)| <= ceiling, POOLED -
    rpm = rho_phi_mu(table, members)
    pooled_abs = rpm["pooled"].get("abs_rho")
    mi_verdict = _pick("H_MeanIndependent", [
        (pooled_abs is not None and pooled_abs <= CEIL_MI, VK["H_MeanIndependent"][0]),
        (True,                                             VK["H_MeanIndependent"][1]),
    ])
    mi_falsified = (mi_verdict == VK["H_MeanIndependent"][1])
    out["H_MeanIndependent"] = {
        "verdict": mi_verdict,
        "stat": rpm, "threshold": f"|rho(phi, mu)| <= {CEIL_MI} (pooled, make-or-break)",
        "make_or_break": True,
        "escalation_triggered": mi_falsified,                # False on pass -> ICC never entered
        "escalation_status": (
            "TRIGGERED — beta-binomial ICC / overdispersion rho required; flagged, NOT auto-run"
            if mi_falsified else
            "N/A (pass) — H_MeanIndependent CONFIRMED; beta-binomial ICC NOT entered"),
        "escalation_path_if_falsified": TH["escalation_path"],
    }

    # --- H_LowRecallDefined (gated on CPC_raw per ruling A; CPC_corr reported alongside) -
    #     gain set = phi-defined AND CV-CPC_raw-UNDEFINED = {0 < pi_hat < MU_FLOOR/F}.
    #     CONFIRMED iff the gain set is NON-EMPTY on real data AND no pi_hat=1 ceiling brand
    #     breaks strict containment. FALSIFIED iff no gain. The mixed outcome (gain holds,
    #     ceiling breaks) routes via LOWRECALL_CEILING_ROUTE (UNRULED -> fail loud).
    nonzero = [r for r in table if r["phi_partition"] != "zero"]   # >=1-surfacing
    phi_def = {(r["substrate"], r["brand"]) for r in nonzero if r["phi_defined"]}
    cvr_def = {(r["substrate"], r["brand"]) for r in nonzero if r["cpc_raw_defined"]}
    sat     = [r for r in nonzero if r["phi_partition"] == "saturated"]
    gain    = [r for r in nonzero if r["phi_defined"] and not r["cpc_raw_defined"]]   # the gain set
    cov_full      = (len(phi_def) == len(nonzero))     # 100% of >=1-surfacing phi-defined (<=> no saturation)
    contains      = cvr_def.issubset(phi_def)          # strict containment of the CV_raw-defined set
    gain_nonempty = len(gain) > 0
    ceiling_breaks = any(r["cpc_raw_defined"] for r in sat)   # CV_raw defines a brand phi excludes
    lr = VK["H_LowRecallDefined"]   # [CONFIRMED, PARTIAL, FALSIFIED]

    if gain_nonempty and cov_full and contains:
        lr_verdict = lr[0]                                  # CONFIRMED
    elif not gain_nonempty:
        lr_verdict = lr[2]                                  # FALSIFIED (no gain — vacuous extension)
    else:
        # gain holds but coverage/containment broken. By phi's totality on (0,1) the ONLY by-design
        # cause is the pi_hat=1 ceiling: assert every residual-undefined >=1-surfacing brand is
        # saturated -> PARTIAL-STRUCTURAL [3]. A non-ceiling residual is impossible-by-construction
        # = an extraction/phi defect -> fail loud as PARTIAL-IMPLEMENTATION [1].
        residual_undef = [r for r in nonzero if not r["phi_defined"]]
        non_ceiling = [r for r in residual_undef if r["phi_partition"] != "saturated"]
        assert not non_ceiling, (
            "H_LowRecallDefined -> " + lr[1] + ": a residual >=1-surfacing brand is undefined for a "
            "NON-ceiling reason (structurally impossible given phi totality on (0,1)) = extraction/phi "
            "bug: " + str([(r["substrate"], r["brand"], r["phi_partition"]) for r in non_ceiling][:5]))
        lr_verdict = LOWRECALL_CEILING_ROUTE                # PARTIAL-STRUCTURAL [3]
    assert lr_verdict in lr, f"H_LowRecallDefined: '{lr_verdict}' not in the locked 4-cell matrix"

    out["H_LowRecallDefined"] = {
        "verdict": lr_verdict,
        "stat": {
            "n_nonzero_surfacing": len(nonzero), "phi_defined": len(phi_def),
            "cv_raw_defined": len(cvr_def), "gain_set_size": len(gain), "gain_nonempty": gain_nonempty,
            "gain_brands": [{"substrate": r["substrate"], "brand": r["brand"], "pi_hat": r["pi_hat"],
                             "mu_count": r["mu_count"], "cpc_corr": r["cpc_corr"]} for r in gain],
            "coverage_full": cov_full, "phi_contains_cv_raw": contains,
            "n_saturated_ceiling": len(sat), "saturation_breaks_containment": ceiling_breaks,
            "mu_floor": _mu_floor(), "target": TARGET_LR,
            "note": ("CONFIRMED needs non-empty gain AND no ceiling break; gain_brands list confirms "
                     "they are genuinely low-recall (pi_hat) and gives the CPC_corr same-domain contrast"),
        },
        "threshold": "phi-defined strictly-contains CV-CPC_raw-defined with a NON-EMPTY low-recall gain set",
    }

    # --- H_GradedRecognition: FORWARD-SPEC (locked; not computed) -------------
    out["H_GradedRecognition"] = {
        "verdict": next(k for k in VK["H_GradedRecognition"] if k.startswith("FORWARD-SPEC")),
        "stat": {"status": "FORWARD-SPEC", "reason": "frozen recognition binary by probe design (DEVIATIONS Entry 0)"},
        "threshold": "n/a (forward-spec)",
    }

    # --- H_PositionalDissociation: |rho(phi, J)| <= ceiling AND >=1 discordant brand
    #     discordance computed WITHIN each framing (percentile rule); union across framings.
    pj, npj = rho_generic(table, "phi", "J", lambda r: r["phi_defined"] and r["J_defined"])
    a_pj = pj["abs_rho"]
    by_key = {(r["substrate"], r["brand"]): r for r in table}
    disc_by_framing, disc_union = {}, set()
    for fr, keys in members.items():
        ds = discordant_set([by_key[k] for k in keys if k in by_key])
        disc_by_framing[fr] = len(ds)
        disc_union |= {(r["substrate"], r["brand"]) for r in ds}
    pd_keys = VK["H_PositionalDissociation"]   # [CONFIRMED, PARTIAL, FALSIFIED]
    out["H_PositionalDissociation"] = {
        "verdict": _pick("H_PositionalDissociation", [
            (a_pj is not None and a_pj <= CEIL_PD and len(disc_union) >= 1, pd_keys[0]),
            (a_pj is not None and a_pj <= CEIL_PD and len(disc_union) == 0, pd_keys[1]),
            (True,                                                          pd_keys[2]),
        ]),
        "stat": {**pj, "n_discordant_union": len(disc_union), "discordant_per_framing": disc_by_framing,
                 "rule": "|cons_pct(phi) - cons_pct(J)| >= 0.50 within framing",
                 "j_substrates": [s for s in OMNI if frame_resolved.get(s)]},
        "threshold": f"|rho(phi, J)| <= {CEIL_PD} AND >=1 discordant brand (percentile rule)",
    }

    # --- H_PhantomSignature: exploratory — phantom_analyzable near-phantoms vs the 84-unit baseline
    #     also report the cleaner DISJOINT contrast (29 phantom_analyzable vs 55 non_phantom).
    base84 = members["v0.35"]
    non_phantom = base84 - v35_phantom
    ph  = [r for r in table if (r["substrate"], r["brand"]) in v35_phantom and r["phi_defined"]]
    npn = [r for r in table if (r["substrate"], r["brand"]) in non_phantom and r["phi_defined"]]
    ps_keys = VK["H_PhantomSignature"]   # [SIGNATURE-PRESENT, NULL, UNDETERMINED]
    out["H_PhantomSignature"] = {
        "verdict": _pick("H_PhantomSignature", [
            (len(ph) < 3, ps_keys[2]),          # UNDETERMINED (insufficient non-zero phantoms)
            (True,        ps_keys[1]),           # NULL by default; exploratory, no directional commitment
        ]),
        "stat": {"n_phantom_defined": len(ph), "n_84_baseline": len(base84),
                 "disjoint_contrast": {"phantom_analyzable": len(ph), "non_phantom": len(npn)},
                 "note": "exploratory; no directional commitment; disjoint 29-vs-55 contrast reported descriptively"},
        "threshold": "exploratory",
    }
    return out


def discordant_set(rows):
    """Pre-specified facet-divergence rule for H_PositionalDissociation's '>=1 discordant'.
    Within a brand set, consistency-orient BOTH facets to [0,1] percentile ranks:
        phi (inconsistency-oriented): cons_phi = 1 - pctrank(phi)
        J   (consistency-oriented):   cons_J   =     pctrank(J)
    pctrank = (avg_rank - 1)/(n - 1). A brand is DISCORDANT iff
        |cons_phi - cons_J| >= 0.50   (the facets place it >= half the distribution apart).
    Returns the list of discordant rows."""
    elig = [r for r in rows if r["phi_defined"] and r["J_defined"]]
    n = len(elig)
    if n < 2:
        return []
    def pct(vals):
        rk = stats.rankdata(np.asarray(vals, float), method="average")
        return (rk - 1.0) / (n - 1.0)
    cons_phi = 1.0 - pct([r["phi"] for r in elig])
    cons_J   =       pct([r["J"]   for r in elig])
    return [r for i, r in enumerate(elig) if abs(cons_phi[i] - cons_J[i]) >= 0.50]


# ===========================================================================
# STAGE 4 — outputs (verdicts JSON gate, then supplementary CSV)
# ===========================================================================
def write_outputs(table, verds, recon, two_wave, secondary, frame_resolved):
    outdir = ROOT / "osf/methodology/v1_8"
    outdir.mkdir(parents=True, exist_ok=True)

    payload = {
        "prereg_tag": PREREG.METADATA["prereg_tag"],
        "revision": PREREG.METADATA["revision"],
        "instrument": "phi (channel-agnostic primary), J, CV-CPC baseline; per-channel secondary",
        "constants": {"M": M, "F_primary": F, "MF_primary": MF, "F_per_channel": F_CHAN},
        "reconciliation_gate": recon,
        "frame_resolved_substrates": {s: bool(frame_resolved.get(s)) for s in OMNI},
        "two_wave_reproducibility": two_wave,      # v0.34 t1<->t2 (phi agreement)
        "secondary_per_channel": _summarize_secondary(secondary),
        "verdicts": verds,
    }
    (outdir / "v1_8_verdicts.json").write_text(json.dumps(payload, indent=2))

    cols = ["substrate", "brand", "cell", "k_per_model", "pi_hat", "mu", "phi",
            "phi_partition", "phi_defined", "J", "J_n_models", "J_defined",
            "J_frame_resolved_substrate", "mu_count", "sd_pop",
            "cpc_raw", "cpc_raw_defined", "cpc_corr", "cpc_corr_defined"]
    with open(outdir / "v1_8_instrument_table.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in table:
            row = dict(r)
            row["k_per_model"] = json.dumps(row["k_per_model"])
            w.writerow(row)
    return outdir


def two_wave_reproducibility(panel):
    """v0.34: phi at t1 (osf/{v}/phase_b) vs t2 (osf/v34/data/{v}/phase_b); rank agreement.
    Reuses the certified S31 extractors on each wave's paths."""
    import score_v0_31 as S31
    import score_v33 as V33
    V = ROOT / "osf"

    def counts_for(base, v23_rel):
        out = {}
        for sub in ("v0.20", "v0.21", "v0.22"):
            rk, rp, mod, _ = V33.RECON_CFG[sub]
            pb = base / f"{sub.replace('v0.', 'v')}/phase_b_results.csv"
            out[sub], _ = S31.counts_raw_text(rk, rp, mod, pb)
        out["v0.19"], _ = S31.counts_v19(base / "v19/phase_b_results.csv")
        out["v0.23"], _ = S31.counts_v23(base / v23_rel)   # v23 layout differs by wave (explicit, no fallback)
        return out

    # t1 = original deposits (v23 under v23/data/); t2 = re-acquisition (v23 under v34/data/v23/)
    t1 = counts_for(V,             "v23/data/v23_phase_b_scored.json")
    t2 = counts_for(V / "v34/data", "v23/v23_phase_b_scored.json")
    pairs = []
    for sub in OMNI:
        for b in (set(t1.get(sub, {})) & set(t2.get(sub, {}))):
            p1, _, s1 = phi_of(t1[sub][b])
            p2, _, s2 = phi_of(t2[sub][b])
            if s1 == "defined" and s2 == "defined":
                pairs.append((p1, p2))
    if len(pairs) >= 3:
        x, y = zip(*pairs)
        rep = _spearman(np.array(x, float), np.array(y, float))
    else:
        rep = {"rho": None, "n": len(pairs), "note": "insufficient defined pairs"}
    return {"phi_t1_t2_rank_agreement": rep, "n_pairs": len(pairs)}


def _summarize_secondary(sec):
    summ = {"scope": SEC["scope"], "excludes": SEC["excludes"], "status": SEC["status"], "per_substrate": {}}
    for sub, chans in sec.items():
        summ["per_substrate"][sub] = {ch: sum(1 for v in res.values() if v["phi"] is not None)
                                      for ch, res in chans.items()}
    return summ


# ===========================================================================
# main — guarded by --run (the one-way boundary)
# ===========================================================================
def main(do_run):
    if not do_run:
        print(__doc__.split("SPEC THIS IMPLEMENTS")[0].strip())
        print("\n*** BOUNDARY: re-invoke with --run to perform the first scoring call. "
              "Nothing computed. ***")
        return 0

    print("[stage 0] certified surfacing extraction + reconciliation gate ...")
    counts, cells, recon, panel = stage0_primary_counts()
    frames, resolved = stage0_frame_surfacing(panel)
    assert_frame_count_consistency(frames, counts, panel)   # frame-sum == reconciled count (fail loud)
    print(f"           reconciliation: checked={recon['checked']} passed={recon['passed']}")
    print(f"           frame/count consistency: OK")
    print(f"           frame-resolved (J-eligible): {[s for s in OMNI if resolved.get(s)]}")

    print("[stage 1] phi / J primary, CV-CPC baseline, per-channel secondary ...")
    _cv_parity_check()                                      # one-case parity on reproduced CV-CPC
    table = build_instrument_table(counts, cells, frames, resolved)
    secondary = per_channel_secondary(panel)

    print("[stage 2] rho per framing + pooled (within-framing ranks) ...")
    members, v35_phantom = framing_membership(table)
    two_wave = two_wave_reproducibility(panel)

    print("[stage 3] verdicts vs locked matrix ...")
    verds = verdicts(table, members, v35_phantom, recon, resolved)

    print("[stage 4] writing verdicts JSON (the gate) + instrument table ...")
    outdir = write_outputs(table, verds, recon, two_wave, secondary, resolved)
    for hid, v in verds.items():
        print(f"           {hid:26s} -> {v['verdict']}")
    print(f"\nWrote {outdir/'v1_8_verdicts.json'} and {outdir/'v1_8_instrument_table.csv'}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="AIAS v1.8 CPC scorer (one-way boundary; --run required).")
    ap.add_argument("--run", action="store_true",
                    help="perform the first scoring call (crosses the pre-registration boundary)")
    sys.exit(main(ap.parse_args().run))
