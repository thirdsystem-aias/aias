#!/usr/bin/env python3
"""
score_v0_37.py — AIAS(TM) v0.37 scorer: Identity-Load (IL-Direct) x phi moderation.

================================ REWORK NOTICE =================================
REWORKED from the v1.8 phi/J template (seeded verbatim from score_v1_8.py) into
v0.37's IL-moderation design, against the locked pre-registration at tag
v0.37-prereg-r2 (commit 87ee3c2; amends r1 2f381f7). The rework is a faithful
TRANSCRIPTION of the locked prose
(prereg/v0_37_cpc_identity_load_moderator_content.py). Per pinned constraint F,
THE PROSE IS AUTHORITATIVE: every constant below carries an inline citation to
the prose section it transcribes; a scorer constant that disagreed with the
prose would be a bug to fix toward the prose, never a silent re-number.

KERNEL KEPT PRISTINE (the reason the scorer was seated): phi_of (the
mean-independent instrument + Fork-A pi_hat in {0,1} exclusions), _spearman,
cvcpc_of (now the SUPPLEMENTARY comparator, not the DV), the certified Stage-0
extraction + reconciliation gate (DECISION-2), and the one-way --run boundary.

VERDICT SHELL REPLACED WHOLESALE (not edited): v1.8's H_* stages, the
framing-membership / two-wave / per-channel machinery, and the J/frame-surfacing
path are REMOVED and rebuilt as v0.37's IL-moderation logic. (J is not a v0.37
verdict instrument; see NOTE-J below.)

DECISION-1: structured constants are TRANSCRIBED into this scorer with prose
citations; prereg/v0_37_*.py stays byte-identical to the r2 tag.
DECISION-2: phi is computed from the certified Stage-0 extraction (reconciled
bit-for-bit to v1.7 r_per_model), NOT recomputed from v1_7_cpc.csv's r_per_model
column — so the reconciliation gate remains a real check, not trivially true.

ROOT FOOTGUN (resolved): ROOT = ~/aias. v0.37 is now checked out in the main
tree (the worktree is gone), so the hardcoded ROOT resolves to v0.37 data. Run
from ~/aias only.

ONE-WAY BOUNDARY: --run is the first scoring call — the irreversible crossing of
the externally-anchored pre-registration. Without --run nothing is computed.
Outputs: osf/v37/v37_verdicts.json, osf/v37/v37_il_phi_analysis_set.csv.
===============================================================================
"""

import sys, os, json, csv, argparse, hashlib
from pathlib import Path

import numpy as np
from scipy import stats

ROOT = Path.home() / "aias"

sys.path.insert(0, str(ROOT / "prereg"))                       # locked v0.37 module (guard)
sys.path.insert(0, str(ROOT / "scripts"))                      # score_v33, score_v0_31, score_v20/21/22, score_v30
sys.path.insert(0, str(ROOT / "osf/methodology/v1_7/scoring")) # score_v1_7 (CPC_raw certified)

# Import the locked record ONLY to bind provenance + run its commit guard
# (it raises if a <<CONFORM-VERBATIM placeholder survives). Constants are NOT
# read from it: the module is prose-only by design (DECISION-1).
import v0_37_cpc_identity_load_moderator_content as PREREG     # noqa: F401  (guard + provenance)

# ===========================================================================
# DECISION-1: TRANSCRIBED CONSTANTS (prose authoritative; citations inline)
# ===========================================================================
PREREG_TAG = "v0.37-prereg-r2"     # amends r1 (2f381f7); see prereg DEVIATIONS Entry 2

# DESIGN / mega-prompt: canonical two-channel trio, n=72 (24x3). v0.19 excluded
# (single-channel, out of construct); v0.23 walled (not in the trio).
TRIO = ["v0.20", "v0.21", "v0.22"]

# COMPUTATION (phi kernel) — from METRIC_DEFINITION (locked formula).
M  = 6     # panel models           (TRANSCRIBED: METRIC_DEFINITION / v1.8 panel)
F  = 6     # frames per model       (channel-agnostic primary)
MF = M * F # = 36 (primary denominator)

# PRIMARY bands — HYPOTHESES / DECISION_RULES (pinned):
#   |rho| >= 0.30 & p < .05 -> CONFIRMED (sign-split); |rho| < 0.15 -> FALSIFIED;
#   else -> MARGINAL.
RHO_CONFIRM = 0.30          # TRANSCRIBED: DECISION_RULES
RHO_FALSIFY = 0.15          # TRANSCRIBED: DECISION_RULES
P_ALPHA     = 0.05          # TRANSCRIBED: DECISION_RULES (two-sided)

# Permutation inference — HYPOTHESES (PRIMARY): >= 10,000 MC, two-sided,
# IL-Direct labels permuted WITHIN substrate only.
MC_DRAWS = 10_000           # TRANSCRIBED: HYPOTHESES (">= 10,000")
# (GAP-C, recorded in DEVIATIONS Entry 2, NOT locked) The seed is an
# implementation-determinism choice pinned HERE, not in the lock. Value chosen
# from the phase id (v0.37 -> 370037); arbitrary but fixed for reproducibility.
PERM_SEED = 370037
# DEVIATIONS Entry 2: every permutation p is reported with its Monte Carlo
# standard error; any |effect| whose p sits within MC_SE_FLAG_K * MC-SE of
# P_ALPHA is flagged seed-sensitive.
MC_SE_FLAG_K = 2.0

# n-floor — ELIGIBILITY_ATTRITION (LOCKED at r1): realized pooled analyzable
# n < 45 -> PRIMARY INDETERMINATE-UNDERPOWERED (band coherence: critical Spearman
# rho at p=.05 crosses 0.30 near n~=44).
N_FLOOR = 45                # TRANSCRIBED: ELIGIBILITY_ATTRITION
# per-substrate fragility flag: < 10 analyzable units -> unstable within-substrate
# ranks; reported as a note on the pooled primary, NOT a gate.
SUBSTRATE_FRAGILE_N = 10     # TRANSCRIBED: ELIGIBILITY_ATTRITION

# SECONDARY partial arm — H_IL_Presence_Robustness (r2 amendment):
#   partial CONFIRMED: |rho_partial| >= 0.30 AND p_perm < .05
#   partial NULL:      |rho_partial| < 0.15
#   partial MIDDLE:    in between (incl. |rho|>=0.30 with p>=.05)
# CONFIRMED-row attenuation cut (separate use): |rho_partial| < 0.15 -> ATTENUATES.
PARTIAL_CONFIRM = 0.30      # TRANSCRIBED: H_IL_Presence_Robustness r2
PARTIAL_NULL    = 0.15      # TRANSCRIBED: H_IL_Presence_Robustness r2 / CONFIRMED-row cut

# Verdict-key strings — transcribed from VERDICT_MATRIX labels (faithful).
VK = {
    "INDETERMINATE_UNDERPOWERED": "INDETERMINATE-UNDERPOWERED",
    "HEADLINE_POSITIVE":          "HEADLINE-POSITIVE",
    "PRESENCE_SCOPED_POSITIVE":   "PRESENCE-SCOPED-POSITIVE",
    "CONFIRMED_REVERSED":         "CONFIRMED_REVERSED",
    "MARGINAL":                   "MARGINAL",
    "FRAGILE_MARGINAL":           "fragile-MARGINAL",
    "CLEAN_NULL":                 "CLEAN-NULL",
    "SUPPRESSION_UNDETERMINED":   "UNDETERMINED-pending-suppression-diagnosis",
}

# Moderator/control source — MODERATOR_DEFINITION + mega-prompt.
V1_7_CPC = ROOT / "osf/methodology/v1_7/data/v1_7_cpc.csv"


# ===========================================================================
# STAGE 0 — KERNEL-KEEP: certified surfacing extraction + reconciliation gate
#           (verbatim from the seeded template; DECISION-2)
# ===========================================================================
def stage0_primary_counts():
    """Channel-agnostic per-model counts k(b,m) in 0..F via the CERTIFIED lineage,
    CONSUMING score_v33.recall_counts() + reconciliation_gate(). Returns
    counts {sub:{brand:[M]}}, cells {sub:{brand:cell}}, recon, PANEL."""
    import score_v33 as V33
    PANEL = V33.PANEL
    assert len(PANEL) == M, f"PANEL has {len(PANEL)} models, locked M={M}"
    rc = V33.recall_counts()
    counts = {k: v[0] for k, v in rc.items()}
    cells  = {k: v[1] for k, v in rc.items()}
    recon = V33.reconciliation_gate(rc)          # bit-for-bit vs v1.7 r_per_model (trio)
    assert recon["passed"], f"reconciliation gate FAILED: {recon['mismatches'][:3]}"
    for sub in TRIO:                              # geometry guard, trio scope
        for b, vec in counts[sub].items():
            assert len(vec) == M, f"{sub}/{b}: {len(vec)} != M={M}"
            assert all(0 <= int(x) <= F for x in vec), f"{sub}/{b}: count outside 0..{F}: {vec}"
    return counts, cells, recon, PANEL


# ===========================================================================
# STAGE 1 — KERNEL-KEEP: phi (the mean-independent DV) + CV-CPC comparator
# ===========================================================================
def phi_of(counts_vec):
    """phi_b = [1/(M-1)] * sum_m (k - F*pi_hat)^2 / [F*pi_hat*(1-pi_hat)] (locked).
    Fork-A: pi_hat==0 -> 'zero'; pi_hat==1 -> 'saturated'; else 'defined' -> phi.
    phi is INCONSISTENCY-oriented (higher phi = lower consistency). Returns
    (phi or None, pi_hat, label)."""
    k = np.asarray(counts_vec, float)
    pi = float(k.sum() / MF)
    if pi <= 0.0:
        return None, pi, "zero"
    if pi >= 1.0:
        return None, pi, "saturated"
    denom = F * pi * (1.0 - pi)
    phi = float(((k - F * pi) ** 2).sum() / denom / (M - 1))
    return phi, pi, "defined"


def cvcpc_of(counts_vec):
    """CERTIFIED CV-CPC (v1.7), reused UNMODIFIED — here a SUPPLEMENTARY comparator
    (SUPPLEMENTARY_CONTRAST), never the DV. CPC_raw = sd/mu, defined iff mu>=MU_FLOOR."""
    import score_v1_7 as V17
    DDOF, MU_FLOOR = V17.DDOF, V17.MU_FLOOR
    k = np.asarray(counts_vec, float)
    mu = float(k.mean()); sd = float(np.std(k, ddof=DDOF))
    raw_def = (mu >= MU_FLOOR and mu > 0.0)
    return {"mu_count": mu, "sd_pop": sd, "cpc_raw": (sd / mu) if raw_def else None,
            "cpc_raw_defined": raw_def}


# J — DESCRIPTIVE non-verdict instrument (RESTORED per ruling a). METRIC_DEFINITION
# lists J "reported per scorer convention where frame-resolved" as a STATED
# DELIVERABLE, so it is REPORTED (never a verdict input). The v0.23 frame-
# granularity seam is GUARDED LOUD: schema corruption fails loud; insufficient
# granularity (or an absent file) is RECORDED frame-unresolved -- not crashed,
# since v0.23 is walled/optional and not in the trio analysis set. "Computed
# where we could, flagged where we couldn't" is the locked behavior.
def jaccard_of(model_to_frames):
    """J_b = mean over model pairs of |S_m ∩ S_m'| / |S_m ∪ S_m'|. Defined for
    >=1 surfacing across >=2 models. KERNEL-KEEP: verbatim from the seeded template."""
    import itertools
    sets = [frozenset(s) for s in model_to_frames.values() if s]
    if len(sets) < 2:
        return None, len(sets)
    vals = []
    for a, b in itertools.combinations(sets, 2):
        union = a | b
        vals.append(len(a & b) / len(union) if union else 0.0)
    return (float(np.mean(vals)) if vals else None), len(sets)


def _registry_brands(sub, reg_path, S31):
    """Brand list via the registry the certified matcher was certified against.
    KERNEL-KEEP: verbatim from the seeded template."""
    import score_v33 as V33
    rk, rp, mod, pb = V33.RECON_CFG[sub]
    counts, _ = S31.counts_raw_text(rk, rp, mod, pb)
    return sorted(counts.keys())


def trio_frame_surfacing(panel):
    """Frame-level surfacing S(b,m) for the TRIO via certified detect_mention,
    feeding the DESCRIPTIVE J column. Each trio substrate is frame-resolved by
    construction (detect_mention per frame_id). TRANSCRIBED: METRIC_DEFINITION."""
    import score_v0_31 as S31
    import score_v20, score_v21, score_v22
    V = ROOT / "osf"
    detect = {"v0.20": score_v20.detect_mention, "v0.21": score_v21.detect_mention,
              "v0.22": score_v22.detect_mention}
    reg = {"v0.20": ROOT / "prereg/v0_20_registry.json", "v0.21": ROOT / "prereg/v0_21_registry.json",
           "v0.22": ROOT / "prereg/v0_22_automotive_content.py"}
    frames = {}
    for sub in TRIO:
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
        for b in brands:
            fmap.setdefault(b, {})
        frames[sub] = fmap
    return frames


def v23_walled_status(panel):
    """OPTIONAL walled v0.23 J extension (DESIGN: 'optional runtime-verify
    extension, walled'). LOUD on schema corruption; RECORDS frame-unresolved if
    granularity is insufficient or the file is absent -- never gates, never crashes
    (v0.23 is not in the trio analysis set). Returns a status dict (+ J counts if resolved)."""
    path = ROOT / "osf/v23/data/v23_phase_b_scored.json"
    if not path.exists():
        return {"frame_resolved": False, "note": "v0.23 phase_b absent; walled extension not run"}
    data = json.load(open(path))
    assert all("probe_id" in r for r in data), \
        "v0.23 LOUD GUARD: probe_id missing -- frame granularity schema unverifiable"
    per_model = {}
    for r in data:
        m = r.get("model_id")
        if m in panel:
            per_model.setdefault(m, set()).add(r.get("probe_id"))
    resolved = bool(per_model) and min(len(v) for v in per_model.values()) >= 2
    if not resolved:
        return {"frame_resolved": False, "note": "v0.23 frame granularity < 2/model -- recorded unresolved (walled)"}
    fmap = {}
    for r in data:
        m = r.get("model_id")
        if m not in panel:
            continue
        for b, v in (r.get("brand_mentions") or {}).items():
            fmap.setdefault(b, {}).setdefault(m, set())
            if v:
                fmap[b][m].add(r.get("probe_id"))
    jvals = {b: jaccard_of(mm)[0] for b, mm in fmap.items()}
    return {"frame_resolved": True, "n_brands": len(jvals),
            "j_defined": sum(1 for v in jvals.values() if v is not None),
            "note": "v0.23 walled descriptive J (non-verdict)"}


# ===========================================================================
# STAGE 1b — NEW: load the IL-Direct moderator + controls (MODERATOR_DEFINITION)
# ===========================================================================
def load_il_direct():
    """Per-brand IL-Direct = R_cult_total - R_cat_total (brand granularity), plus
    controls C_P (v1.6) and recall-mean (= mean_r), from v1_7_cpc.csv. Keyed
    (substrate, brand). TRANSCRIBED: MODERATOR_DEFINITION + mega-prompt.
    recall-mean = mean_r [(implied): rank-identical to pi_hat, so the partial is
    invariant to the count-vs-rate choice]."""
    assert V1_7_CPC.exists(), f"moderator source missing: {V1_7_CPC}"
    out, il_hash_rows = {}, []
    with open(V1_7_CPC) as fh:
        for r in csv.DictReader(fh):
            sub = r["substrate"]
            if sub not in TRIO:
                continue
            b = r["brand"]
            il = float(r["R_cult_total"]) - float(r["R_cat_total"])
            out[(sub, b)] = {"il_direct": il, "c_p": float(r["C_P"]),
                             "recall_mean": float(r["mean_r"])}
            il_hash_rows.append(f"{sub}|{b}|{r['R_cat_total']}|{r['R_cult_total']}")
    # RECONCILIATION clause 3 [(implied) operationalization — see note]: record a
    # SHA256 over the consumed IL-Direct columns as deposit-of-record evidence.
    # The prose says "reproduce the v1.7-deposited values bit-for-bit"; the
    # v1.7 deposit IS this csv, so the bit-for-bit DV-side check is the Stage-0
    # reconciliation gate (r_per_model). This hash anchors the IL axis itself.
    il_hash = hashlib.sha256("\n".join(sorted(il_hash_rows)).encode()).hexdigest()
    # RECONCILIATION clause 3 -- halt-on-reuse teeth (moderator axis on the SAME
    # footing as DV-side inputs). The v1.7 deposit IS this csv (no standalone
    # reference-hash artifact), so: first run RECORDS the baseline; any subsequent
    # run HALTS on mismatch (reconciliation-failure-halts-phase extends to IL).
    baseline = ROOT / "osf/v37/.v37_il_direct_baseline.sha256"
    if baseline.exists():
        prior = baseline.read_text().strip()
        assert prior == il_hash, (
            "RECONCILIATION clause 3 HALT (moderator axis): IL-Direct source SHA256 "
            f"changed vs deposited baseline ({prior[:12]}.. -> {il_hash[:12]}..). "
            "Reconciliation failure halts the phase.")
        il_recon = "verified-against-baseline-bit-for-bit"
    else:
        il_recon = "first-run-baseline-to-be-recorded"
    return out, il_hash, il_recon


# ===========================================================================
# STAGE 2 — NEW: analysis set + pooled within-substrate stats + permutation
# ===========================================================================
def build_analysis_set(counts, frames):
    """Eligible iff phi-defined (Fork-A excludes pi_hat in {0,1}) AND IL-defined.
    TRANSCRIBED: ELIGIBILITY_ATTRITION. Returns
    (rows, attrition, fork_a, il_hash, il_recon). J is added as a DESCRIPTIVE column."""
    il_map, il_hash, il_recon = load_il_direct()
    rows, attrition, fork_a = [], {}, {}
    for sub in TRIO:
        trio_brands = list(counts[sub].keys())
        analyzable, n_zero, n_sat, excl_il, incl_il = 0, 0, 0, [], []
        for b in trio_brands:
            phi, pi, part = phi_of(counts[sub][b])
            ilrec = il_map.get((sub, b))
            if ilrec is None:                       # join coverage: fail loud
                raise AssertionError(f"IL-Direct missing for {sub}/{b} (join gap vs v1_7_cpc.csv)")
            if part == "zero":   n_zero += 1
            if part == "saturated": n_sat += 1
            if part == "defined":
                analyzable += 1
                incl_il.append(ilrec["il_direct"])
                J, nJ = jaccard_of(frames.get(sub, {}).get(b, {}))
                rows.append({"substrate": sub, "brand": b, "phi": phi, "pi_hat": pi,
                             "J": J, "J_defined": J is not None, "J_n_models": nJ, **ilrec})
            else:
                excl_il.append(ilrec["il_direct"])
        attrition[sub] = {"trio_brands": len(trio_brands), "analyzable": analyzable,
                          "fragile": analyzable < SUBSTRATE_FRAGILE_N}
        # Fork-A saturation diagnostic (TRANSCRIBED: ELIGIBILITY_ATTRITION) —
        # excluded-vs-included IL-Direct distribution CHARACTERIZES truncation sign.
        fork_a[sub] = {
            "n_zero_floor": n_zero, "n_saturation_ceiling": n_sat,
            "n_analyzable": analyzable,
            "excluded_il_mean": (float(np.mean(excl_il)) if excl_il else None),
            "included_il_mean": (float(np.mean(incl_il)) if incl_il else None),
            "n_excluded": len(excl_il),
        }
    return rows, attrition, fork_a, il_hash, il_recon


def _pooled_within_substrate_ranks(rows, keys):
    """Rank each variable in `keys` WITHIN substrate (avg-tie), pool across the
    trio. TRANSCRIBED: 'ranks computed WITHIN substrate, pooled.'
    (implied): tie method = average (scipy default). Returns dict key->pooled
    rank array, aligned, or None if <2 per every substrate."""
    cols = {k: [] for k in keys}
    for sub in TRIO:
        sr = [r for r in rows if r["substrate"] == sub]
        if len(sr) < 2:                  # cannot rank a singleton
            continue
        for k in keys:
            cols[k].append(stats.rankdata([r[k] for r in sr], method="average"))
    if not cols[keys[0]]:
        return None
    return {k: np.concatenate(v) for k, v in cols.items()}


def pooled_rho(rows, xkey, ykey):
    """Pooled within-substrate Spearman = Pearson on pooled within-substrate ranks.
    TRANSCRIBED: DECISION_RULES primary statistic."""
    pr = _pooled_within_substrate_ranks(rows, [xkey, ykey])
    if pr is None or len(pr[xkey]) < 3:
        return None, (0 if pr is None else len(pr[xkey]))
    rho, _ = stats.pearsonr(pr[xkey], pr[ykey])
    return float(rho), len(pr[xkey])


def partial_rho_il_phi(rows):
    """Partial Spearman rho(IL-Direct, phi | C_P, recall-mean) via the SINGLE
    locked computation: invert the 4-variable Spearman rank-correlation matrix
    over {il_direct, phi, c_p, recall_mean} (within-substrate ranks, pooled);
    partial = -P[il,phi]/sqrt(P[il,il]*P[phi,phi]) from precision matrix P.
    TRANSCRIBED: H_IL_Presence_Robustness r2 (the pairwise form is NOT implemented)."""
    keys = ["il_direct", "phi", "c_p", "recall_mean"]
    pr = _pooled_within_substrate_ranks(rows, keys)
    if pr is None or len(pr["il_direct"]) < 4:     # need n>=4 for a 4-var partial
        return None, (0 if pr is None else len(pr["il_direct"]))
    Rm = np.vstack([pr[k] for k in keys])
    C = np.corrcoef(Rm)
    try:
        P = np.linalg.inv(C)
    except np.linalg.LinAlgError:
        return None, len(pr["il_direct"])
    return float(-P[0, 1] / np.sqrt(P[0, 0] * P[1, 1])), len(pr["il_direct"])


def _perm_p(rows, stat_fn, obs):
    """Two-sided permutation p: shuffle IL-Direct labels WITHIN substrate (the
    locked scheme — primary AND, per r2, partial), recompute stat_fn, count
    |null| >= |obs|. Returns (p, mc_se, seed_sensitive_flag).
    TRANSCRIBED: HYPOTHESES + H_IL_Presence_Robustness r2."""
    if obs is None:
        return None, None, None
    rng = np.random.default_rng(PERM_SEED)
    sub_idx = {sub: [i for i, r in enumerate(rows) if r["substrate"] == sub] for sub in TRIO}
    il = np.array([r["il_direct"] for r in rows], float)
    ge = 0
    aobs = abs(obs)
    for _ in range(MC_DRAWS):
        perm_il = il.copy()
        for idx in sub_idx.values():          # permute WITHIN substrate only
            if len(idx) > 1:
                perm_il[idx] = rng.permutation(perm_il[idx])
        prows = [dict(r, il_direct=perm_il[i]) for i, r in enumerate(rows)]
        val, _ = stat_fn(prows)
        if val is not None and abs(val) >= aobs:
            ge += 1
    p = ge / MC_DRAWS
    mc_se = float(np.sqrt(p * (1.0 - p) / MC_DRAWS))     # DEVIATIONS Entry 2
    seed_sensitive = abs(p - P_ALPHA) <= MC_SE_FLAG_K * mc_se
    return p, mc_se, seed_sensitive


def loso(rows, full_rho):
    """Leave-one-substrate-out: drop each substrate, recompute pooled rho on the
    remaining two. NON-SURVIVAL = sign flip OR |rho| crossing a band boundary
    (0.30 / 0.15). TRANSCRIBED: DECISION_RULES robustness."""
    def coarse_band(r):
        a = abs(r)
        return "hi" if a >= RHO_CONFIRM else ("lo" if a < RHO_FALSIFY else "mid")
    full_cb = coarse_band(full_rho) if full_rho is not None else None
    out, nonsurvival = [], False
    for drop in TRIO:
        sub_rows = [r for r in rows if r["substrate"] != drop]
        rho, n = pooled_rho(sub_rows, "il_direct", "phi")
        rec = {"dropped": drop, "rho": rho, "n": n}
        out.append(rec)
        if rho is None or full_rho is None:
            continue
        if (full_rho > 0) != (rho > 0):       # sign flip
            nonsurvival = True
        if coarse_band(rho) != full_cb:        # band-boundary crossing
            nonsurvival = True
    return out, nonsurvival


# ===========================================================================
# STAGE 3 — NEW: verdict against the locked matrix (incl. r2 FALSIFIED row)
# ===========================================================================
def primary_band(rho, p_perm):
    """TRANSCRIBED: HYPOTHESES / DECISION_RULES (sign-split)."""
    a = abs(rho)
    if a >= RHO_CONFIRM and p_perm < P_ALPHA:
        return VK["CONFIRMED_REVERSED"] if rho < 0 else "CONFIRMED"   # CONFIRMED (predicted rho>0)
    if a < RHO_FALSIFY:
        return "FALSIFIED"
    return VK["MARGINAL"]


def partial_band(rho_p, p_perm_p):
    """TRANSCRIBED: H_IL_Presence_Robustness r2."""
    if rho_p is None:
        return "partial_UNCOMPUTABLE"
    a = abs(rho_p)
    if a >= PARTIAL_CONFIRM and p_perm_p is not None and p_perm_p < P_ALPHA:
        return "partial_CONFIRMED"
    if a < PARTIAL_NULL:
        return "partial_NULL"
    return "partial_MIDDLE"


def route_matrix(prim, pband, rho_p):
    """VERDICT_MATRIX routing (primary x presence-robustness). Returns the headline
    cell. TRANSCRIBED, incl. the r2 FALSIFIED-row completion. CONFIRMED-row uses
    the attenuation cut (|rho_partial| >= 0.15 = concordant); FALSIFIED-row uses
    the r2 partial bands."""
    concordant = (rho_p is not None and abs(rho_p) >= PARTIAL_NULL)
    if prim == "CONFIRMED":                          # predicted sign rho>0
        return VK["HEADLINE_POSITIVE"] if concordant else VK["PRESENCE_SCOPED_POSITIVE"]
    if prim == VK["CONFIRMED_REVERSED"]:             # real opposite finding;
        # "same partial-concordance qualifier applies" (prose) -> split like CONFIRMED row
        return VK["CONFIRMED_REVERSED"] + ("-presence-independent" if concordant
                                           else "-presence-scoped")
    if prim == VK["MARGINAL"]:
        return VK["MARGINAL"]
    if prim == "FALSIFIED":
        if pband == "partial_NULL":
            return VK["CLEAN_NULL"]                   # ONLY clean-negative cell
        # partial CONFIRMED or MIDDLE -> suppression, conservative (r2 Entry 2)
        return VK["SUPPRESSION_UNDETERMINED"]
    raise AssertionError(f"unroutable primary band: {prim}")


def verdicts(rows, attrition, fork_a, il_hash, il_recon, recon, comparator, cross_sub, t2):
    """Assemble the v0.37 verdict payload. The realized-n diagnostic is written
    on EVERY branch, including INDETERMINATE-UNDERPOWERED (your guarantee)."""
    n_pooled = len(rows)
    # primary statistic (always computed for the diagnostic record)
    rho, n = pooled_rho(rows, "il_direct", "phi")
    p_perm, mc_se, seed_sens = _perm_p(rows, lambda rr: pooled_rho(rr, "il_direct", "phi"), rho)

    realized_n = {
        "pooled_analyzable_n": n_pooled, "n_floor": N_FLOOR,
        "per_substrate": attrition, "fork_a_saturation_diagnostic": fork_a,
        "il_direct_source_sha256": il_hash, "il_direct_reconciliation": il_recon,
        "il_direct_reconciliation_note": (
            "DV-side bit-for-bit = Stage-0 r_per_model gate (DECISION-2); IL axis = "
            "SHA256 baseline with halt-on-mismatch on reuse (clause 3, same footing "
            "as DV-side inputs)."),
    }

    # --- n-floor SHORT-CIRCUIT — still writes the realized-n diagnostic --------
    if n_pooled < N_FLOOR:
        return {
            "H_IL_Consistency": {
                "verdict": VK["INDETERMINATE_UNDERPOWERED"],
                "reason": f"realized pooled analyzable n={n_pooled} < n_floor={N_FLOOR}",
                "stat": {"rho": rho, "p_perm": p_perm, "mc_se": mc_se, "n": n},
                "realized_n": realized_n,
            },
            "_note": "PRIMARY underpowered; matrix not entered (TRANSCRIBED ELIGIBILITY_ATTRITION).",
        }

    # --- partial arm (H_IL_Presence_Robustness r2) ----------------------------
    rho_p, n_p = partial_rho_il_phi(rows)
    p_perm_p, mc_se_p, seed_sens_p = _perm_p(rows, lambda rr: partial_rho_il_phi(rr), rho_p)

    prim_raw = primary_band(rho, p_perm)
    pband = partial_band(rho_p, p_perm_p)

    # --- LOSO one-band downgrade (DECISION_RULES) -----------------------------
    loso_rows, nonsurvival = loso(rows, rho)
    prim_final = prim_raw
    loso_applied = None
    if nonsurvival:
        if prim_raw in ("CONFIRMED", VK["CONFIRMED_REVERSED"]):
            prim_final = VK["MARGINAL"]; loso_applied = f"{prim_raw} -> MARGINAL (LOSO non-survival)"
        elif prim_raw == VK["MARGINAL"]:
            prim_final = VK["FRAGILE_MARGINAL"]; loso_applied = "MARGINAL -> fragile-MARGINAL (LOSO non-survival)"
    # (implied): the matrix routes on the LOSO-adjusted primary; raw band + the
    # downgrade are both reported so the adjustment is auditable.
    route_band = "FALSIFIED" if prim_final == "FALSIFIED" else (
        "CONFIRMED" if prim_final == "CONFIRMED" else
        VK["CONFIRMED_REVERSED"] if prim_final == VK["CONFIRMED_REVERSED"] else
        VK["MARGINAL"])   # fragile-MARGINAL routes as MARGINAL
    headline = route_matrix(route_band, pband, rho_p)

    return {
        "H_IL_Consistency": {
            "verdict": prim_final,
            "primary_band_raw": prim_raw,
            "headline_cell": headline,
            "stat": {"rho": rho, "p_perm": p_perm, "mc_se": mc_se,
                     "seed_sensitive_at_alpha": seed_sens, "n": n,
                     "predicted_sign": "rho>0 (IL up -> consistency down)"},
            "loso": {"per_drop": loso_rows, "nonsurvival": nonsurvival, "downgrade": loso_applied},
            "realized_n": realized_n,
        },
        "H_IL_Presence_Robustness": {
            "verdict": pband,
            "role": "SECONDARY (robustness; not a gate). Feeds the verdict-matrix cell.",
            "stat": {"rho_partial": rho_p, "p_perm": p_perm_p, "mc_se": mc_se_p,
                     "seed_sensitive_at_alpha": seed_sens_p, "n": n_p,
                     "method": "4-var Spearman rank-correlation-matrix inversion (r2 single locked computation)"},
        },
        "H_IL_Cross_Substrate": cross_sub,     # SECONDARY descriptive (N=3, no inference)
        "H_IL_t2_Stability": t2,               # TERTIARY walled (or dropped)
        "SUPPLEMENTARY_IL_CVCPC": comparator,  # non-gating instrument-sensitivity
    }


def cross_substrate(rows):
    """H_IL_Cross_Substrate — per-substrate rho sign table. N=3 -> NO inference.
    TRANSCRIBED: HYPOTHESES (descriptive-only)."""
    per = {}
    for sub in TRIO:
        sr = [r for r in rows if r["substrate"] == sub]
        if len(sr) < 3:
            per[sub] = {"rho": None, "n": len(sr), "note": "n<3"}
            continue
        rho, _ = stats.spearmanr([r["il_direct"] for r in sr], [r["phi"] for r in sr])
        per[sub] = {"rho": float(rho), "n": len(sr)}
    return {"verdict": "DESCRIPTIVE (N=3 substrates; no inferential claim)", "per_substrate": per}


def supplementary_il_cvcpc(rows, counts):
    """SUPPLEMENTARY_CONTRAST — pooled within-substrate Spearman rho(IL-Direct,
    CV-CPC) as an instrument-sensitivity illustration. EXPLICITLY NON-GATING."""
    enriched = []
    for r in rows:
        cv = cvcpc_of(counts[r["substrate"]][r["brand"]])
        if cv["cpc_raw_defined"]:
            enriched.append(dict(r, cpc_raw=cv["cpc_raw"]))
    rho, n = pooled_rho(enriched, "il_direct", "cpc_raw") if enriched else (None, 0)
    return {"role": "SUPPLEMENTARY-ILLUSTRATIVE — non-gating (touches no verdict)",
            "rho_il_cvcpc": rho, "n": n,
            "note": "retired v1.7 instrument; shown for the 'only the instrument that worked' objection"}


def tertiary_t2(rows):
    """H_IL_t2_Stability — TERTIARY walled: descriptive IL->phi test-retest where
    the v0.34 t2 wave intersects the trio. DROPPED SILENTLY if no t2 wave present.
    TRANSCRIBED: HYPOTHESES (quarantined; no threshold)."""
    t2dir = ROOT / "osf/v34/data"
    if not t2dir.exists():
        return {"verdict": "DROPPED", "reason": "no intersecting v0.34 t2 wave present (walled)"}
    # Recompute phi at t2 for trio brands via the certified extractor, pair with t1 phi.
    try:
        import score_v0_31 as S31
        import score_v33 as V33
        pairs = []
        t1 = {(r["substrate"], r["brand"]): r["phi"] for r in rows}
        for sub in TRIO:
            rk, rp, mod, _ = V33.RECON_CFG[sub]
            pb = t2dir / f"{sub.replace('v0.', 'v')}/phase_b_results.csv"
            if not pb.exists():
                continue
            c2, _ = S31.counts_raw_text(rk, rp, mod, pb)
            for b, vec in c2.items():
                p2, _, part = phi_of(vec)
                if part == "defined" and (sub, b) in t1:
                    pairs.append((t1[(sub, b)], p2))
        if len(pairs) < 3:
            return {"verdict": "DROPPED", "reason": f"insufficient intersecting defined pairs (n={len(pairs)})"}
        x, y = zip(*pairs)
        rho, _ = stats.spearmanr(x, y)
        return {"verdict": "DESCRIPTIVE (walled; no confirmatory threshold)",
                "phi_t1_t2_rank_agreement": float(rho), "n_pairs": len(pairs)}
    except Exception as e:        # walled: never let the tertiary break the run
        return {"verdict": "DROPPED", "reason": f"t2 path unavailable: {type(e).__name__}"}


# ===========================================================================
# STAGE 4 — outputs (verdicts JSON gate, then analysis-set CSV)
# ===========================================================================
def write_outputs(rows, verds, recon, il_hash, descriptive_j):
    outdir = ROOT / "osf/v37"
    outdir.mkdir(parents=True, exist_ok=True)
    payload = {
        "prereg_tag": PREREG_TAG, "design": "Identity-Load (IL-Direct) x phi moderation, trio n<=72",
        "constants": {"M": M, "F": F, "MF": MF, "rho_confirm": RHO_CONFIRM,
                      "rho_falsify": RHO_FALSIFY, "alpha": P_ALPHA, "mc_draws": MC_DRAWS,
                      "perm_seed": PERM_SEED, "n_floor": N_FLOOR},
        "reconciliation_gate": recon,
        "descriptive_J": descriptive_j,        # non-verdict (METRIC_DEFINITION 'reported where frame-resolved')
        "verdicts": verds,
    }
    (outdir / "v37_verdicts.json").write_text(json.dumps(payload, indent=2))
    # RECONCILIATION clause 3: record the IL-Direct baseline on first run (the
    # halt-on-mismatch teeth in load_il_direct engage on any subsequent run).
    baseline = outdir / ".v37_il_direct_baseline.sha256"
    if not baseline.exists():
        baseline.write_text(il_hash + "\n")
    cols = ["substrate", "brand", "phi", "pi_hat", "J", "J_defined", "J_n_models",
            "il_direct", "c_p", "recall_mean"]
    with open(outdir / "v37_il_phi_analysis_set.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    return outdir


# ===========================================================================
# main — guarded by --run (the one-way boundary)
# ===========================================================================
def main(do_run):
    if not do_run:
        print(__doc__.split("KERNEL KEPT")[0].strip())
        print("\n*** BOUNDARY: re-invoke with --run to perform the first scoring call. "
              "Nothing computed. ***")
        return 0

    print("[stage 0] certified surfacing extraction + reconciliation gate ...")
    counts, cells, recon, panel = stage0_primary_counts()
    print(f"           reconciliation: checked={recon['checked']} passed={recon['passed']}")

    print("[stage 1] frame surfacing (descriptive J) + v0.23 walled status ...")
    frames = trio_frame_surfacing(panel)
    v23 = v23_walled_status(panel)
    frame_resolved = {s: True for s in TRIO}
    frame_resolved["v0.23"] = bool(v23.get("frame_resolved"))
    descriptive_j = {"frame_resolved": frame_resolved, "v23_walled": v23,
                     "note": "J is descriptive, non-verdict (METRIC_DEFINITION 'reported where frame-resolved')"}

    print("[stage 1/2] phi + IL-Direct join, analysis set (trio, Fork-A) ...")
    rows, attrition, fork_a, il_hash, il_recon = build_analysis_set(counts, frames)
    print(f"           pooled analyzable n = {len(rows)} (floor {N_FLOOR}); J frame-resolved={frame_resolved}")

    print("[stage 2] supplementary contrast + cross-substrate + tertiary t2 ...")
    comparator = supplementary_il_cvcpc(rows, counts)
    cross_sub  = cross_substrate(rows)
    t2         = tertiary_t2(rows)

    print(f"[stage 3] primary rho + partial arm + matrix (seed={PERM_SEED}, {MC_DRAWS} MC) ...")
    verds = verdicts(rows, attrition, fork_a, il_hash, il_recon, recon, comparator, cross_sub, t2)

    print("[stage 4] writing verdicts JSON (the gate) + analysis-set CSV ...")
    outdir = write_outputs(rows, verds, recon, il_hash, descriptive_j)
    print(f"           H_IL_Consistency -> {verds['H_IL_Consistency']['verdict']}")
    if "headline_cell" in verds["H_IL_Consistency"]:
        print(f"           headline cell   -> {verds['H_IL_Consistency']['headline_cell']}")
    print(f"\nWrote {outdir/'v37_verdicts.json'} and {outdir/'v37_il_phi_analysis_set.csv'}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="AIAS v0.37 IL-Direct x phi scorer (one-way boundary; --run required).")
    ap.add_argument("--run", action="store_true",
                    help="perform the first scoring call (crosses the pre-registration boundary)")
    sys.exit(main(ap.parse_args().run))
