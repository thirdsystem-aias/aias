"""
v0.41 - Long-Horizon Stability t1->t2->t3: A Last Wave on the Retiring Six-Model Panel
Pre-Registration Content Module
AIAS(TM) Measurement Program - Third System(TM)

DRAFT r1 (Nov 9, 2026) - NOT LOCKED. Lock = tag v0.41-prereg-r1, pushed, plus the
OSF deposit of osf/v41/prereg/, before the first study call (Pablo's go).

PROSPECTIVE LONGITUDINAL re-acquisition (third wave). Full re-acquisition at t3
(November 2026) of the five panel-uniform omnibus substrates first acquired at t1
(May 2026, v0.19-v0.23) and re-acquired at t2 (June 10, 2026, v0.34), with each
substrate's t1 runner VERBATIM (re-pointed only at osf/v41/data/), the same
probe text (byte-locked by checksum in osf/v41/prereg/acquisition_manifest_v41.md)
and the same model aliases. Why now: the six-model panel starts retiring on
2026-11-24 (Claude Opus 4.5 not sooner than that date; Claude Sonnet 4.5 on
2026-11-30; GPT-4o and GPT-4o mini snapshots on 2027-01-14; source
osf/v40/registries/model_cutoffs.csv). This is the last wave this panel can give.

What it adds: v0.34 (t1->t2, 15-21 days) and v1.8 (phi reproducibility 0.645
over the same interval) measured short-horizon stability only. v0.41 measures the
long horizon (~5 months, t2->t3) for both AIAS components on a version-matched
panel - t2 recorded the dated snapshot each alias served, and the pre-lock check
on 2026-11-09 found the same four dated snapshots - and gives the AIAS 2.0
synthesis and the v1.9 composite calibration a long-horizon reliability input.

NOTE ON SCAFFOLD: scaffolded from v0.34 and REPLACED in full.
"""

PHASE_ID = "v0.41"
PHASE_TITLE = "Long-Horizon Stability t1->t2->t3: A Last Wave on the Retiring Six-Model Panel"
CONSISTENCY_LOCK = "v1.8"          # phi (primary), J (positional diagnostic); mean-independent
PRESENCE_LOCK = "v1.6"             # C_P recognition count; recall per v1.4 two-channel decomposition
PHASE_TYPE = "prospective_longitudinal"   # full re-acquisition at t3; NOT a re-analysis
PREREG_TAG = "v0.41-prereg-r1"

# Temporal anchors -----------------------------------------------------------
T1 = "original substrate-phase acquisition, 2026-05-20..05-26 (per substrate below)"
T2 = "v0.34 re-acquisition, 2026-06-10 14:07-17:14 UTC (osf/v34/data/v34_provenance.csv)"
T3 = "v0.41 re-acquisition, first call >= the anchored lock (planned 2026-11-17..11-21), recorded at run time"

LINEAGE = """
t1 substrate lineage: v0.19 audiophile headphones (SSRN 6809182), v0.20 skincare
(6811441), v0.21 cosmetics (6815378), v0.22 automotive (6829118), v0.23 premium
spirits (6834298). t2: v0.34 CPC longitudinal t1->t2 (6915458). Consistency
instrument: v1.8 mean-independent phi (6963359), superseding the CV-based CPC
falsified in v1.7 (6878818). Presence: v1.6 (6816340). Characterization arc:
v0.32 (6898581), v0.33 (6909019). v0.35 and v0.36 were removed from SSRN; if cited,
cite them by title with the OSF deposit (osf.io/ec6wh, v35/v36).
"""

SUBSTRATES = [
    {"phase": "v0.19", "name": "audiophile headphones", "brands": 16, "panel": "canonical-6",
     "extraction_path": "A", "t1_acq": "2026-05-20"},
    {"phase": "v0.20", "name": "skincare",              "brands": 24, "panel": "canonical-6",
     "extraction_path": "B", "t1_acq": "2026-05-21"},
    {"phase": "v0.21", "name": "cosmetics",             "brands": 24, "panel": "canonical-6",
     "extraction_path": "B", "t1_acq": "2026-05-22"},
    {"phase": "v0.22", "name": "automotive",            "brands": 24, "panel": "canonical-6",
     "extraction_path": "B", "t1_acq": "2026-05-25"},
    {"phase": "v0.23", "name": "premium spirits",       "brands": 24, "panel": "canonical-6",
     "extraction_path": "C", "t1_acq": "2026-05-26"},
]
N_BRAND_UNITS = 112
N_SUBSTRATE_UNITS = 5

# ===========================================================================
# METRIC DEFINITIONS (inherited verbatim from v1.8 and v1.6; NOT redefined here).
# ===========================================================================
M = 6            # panel models
F = 6            # frames per model (3 category + 3 cultural), pooled channel-agnostically
METRICS = {
    "k_bm": "per-model recall count k(b,m) in 0..F: frames in which model m surfaces brand b (Phase B)",
    "pi_hat": "pooled recall rate pi_hat_b = sum_m k(b,m) / (M*F); total on [0,1] (the recall face of Presence)",
    "phi": ("v1.8 between-model quasi-binomial dispersion: "
            "phi_b = [1/(M-1)] * sum_m (k(b,m) - F*pi_hat_b)^2 / [F*pi_hat_b*(1-pi_hat_b)]; "
            "defined for pi_hat in (0,1); higher phi = LESS consistent; E[phi]=1 under homogeneity"),
    "J": "v1.8 positional diagnostic: mean pairwise Jaccard overlap of per-model frame sets "
         "(defined when >= 2 models surface b); chance-corrected J_adj if |rho(J, mu)| > 0.50 (v1.8 rule)",
    "C_P": "v1.6 Presence recognition count: models (0..6) recognizing b in Phase A; v0.23 r_level "
           "normalized to binary (R0 -> 0, else 1), identically in every wave",
    "cv_cpc": "CV-CPC = 1/(1+CV) of k(b,.), floor mean(k) >= 1.0; WALLED (v1.7: not adopted); "
              "reported only as the v0.34 comparability baseline",
    "phantom": "below the recall floor (mean per-model recall count < 1.0), the v0.34 rule",
}
PHI_PARTITION = ("phi undefined at pi_hat = 0 (true zero) and pi_hat = 1 (saturation); "
                 "partitioned out per wave before analysis, as in v1.8")

# ---------------------------------------------------------------------------
# PANEL + MODEL-ID PINNING
# ---------------------------------------------------------------------------
PROVIDER_GROUPS = {
    "Anthropic": ["Claude Opus 4.5", "Claude Sonnet 4.5"],
    "OpenAI":    ["GPT-4o", "GPT-4o-mini"],
    "Google":    ["Gemini 2.5 Flash", "Gemini 2.5 Flash Lite"],
}
PANEL_STATUS = [
    # t2 = served id recorded in osf/v34/data/v34_provenance.csv (2026-06-10)
    # pre-lock = served id in osf/v41/prereg/feasibility_v0_41.json (2026-11-09 05:23 UTC)
    {"alias": "claude-opus-4-5",       "t2_served": "claude-opus-4-5-20251101",   "prelock_served": "claude-opus-4-5-20251101",   "match": True},
    {"alias": "claude-sonnet-4-5",     "t2_served": "claude-sonnet-4-5-20250929", "prelock_served": "claude-sonnet-4-5-20250929", "match": True},
    {"alias": "gpt-4o",                "t2_served": "gpt-4o-2024-08-06",          "prelock_served": "gpt-4o-2024-08-06",          "match": True},
    {"alias": "gpt-4o-mini",           "t2_served": "gpt-4o-mini-2024-07-18",     "prelock_served": "gpt-4o-mini-2024-07-18",     "match": True},
    {"alias": "gemini-2.5-flash",      "t2_served": "gemini-2.5-flash (undated)", "prelock_served": "gemini-2.5-flash (undated)", "match": None},
    {"alias": "gemini-2.5-flash-lite", "t2_served": "gemini-2.5-flash-lite (undated)", "prelock_served": "gemini-2.5-flash-lite (undated)", "match": None},
]
PINNING = """
Aliases verbatim (the t1 runners pin aliases; v0.34 precedent). Version isolation is
checked, not assumed: MC_Snapshot compares the dated id each call serves at t3 with
the t2 record. Gemini serves undated aliases at both waves, so silent Gemini drift
cannot be excluded and is named in LIMITATIONS.
"""
MODEL_DROP_RULE = """
A pinned alias unavailable at t3 (after logged retries) is excluded PAIRWISE from every
paired statistic (dropped in all waves for comparability), with a contemporaneous
DEVIATIONS entry. Minimum viable panel = 4 models; below 4 the phase HALTS for
re-scope. If a dated-id model serves a different snapshot at t3 than at t2, it is NOT
dropped; every primary statistic is ALSO reported without it (sensitivity), and its
t2->t3 contrast is read as version-confounded.
"""

# ---------------------------------------------------------------------------
# ACQUISITION
# ---------------------------------------------------------------------------
ACQUISITION = {
    "design": "Full re-acquisition of Phase A (Recognition) + Phase B (two-channel six-frame "
              "Recall) for all 5 substrates at t3. Registries bit-identical to the t1 locks; "
              "probe wording verbatim; panel = t1 aliases.",
    "per_wave_call_counts": {
        "phase_a_recognition": "672  (v19 16x6=96; v20-23 24x6=144 each)",
        "phase_b_recall":      "180  (5 substrates x 6 frames x 6 models)",
        "total_per_wave":      "852",
        "coding_not_acquisition": "v0.23 recognition judge (claude-sonnet-4-5, ~144 calls), as at t2",
    },
    "dispatcher": "osf/v41/scripts/run_acquisition_v41.py (fork of run_acquisition_v34.py): "
                  "imports each verbatim t1 runner and calls its own phase functions; "
                  "wraps only the SDK call boundary for provenance.",
    "permitted_runner_edits": [
        "(i) the output directory (re-point to osf/v41/data/);",
        "(ii) the provenance SIDECAR osf/v41/data/v41_provenance.csv (served id, finish "
        "reason, output and thinking tokens per call).",
        "NOTHING ELSE. Probe text, frame ordering, registry and each runner's own output "
        "schema are byte-frozen against the t1 checksums.",
    ],
    "environment": "Mac, isolated venv ~/aias/.venv-v41 (Python 3.14.4; anthropic 0.97.0, "
                   "openai 2.33.0, google-genai 1.74.0, google-generativeai 0.8.6). The "
                   "v0.19-v0.22 runners call the deprecated google-generativeai SDK "
                   "(support ended upstream; still served on 2026-11-09, 18/18 feasibility "
                   "calls ok); it is kept to honour the verbatim commitment.",
    "window": "One continuous run of all five substrates (t2 took ~3 h), after the lock is "
              "anchored and outside v0.40's acquisition window, no later than 2026-11-21. "
              "Transient failures (network, 429, 5xx) are retried with the same prompt, "
              "alias and parameters and logged; auth or quota failures halt the run.",
    "byte_fidelity_lock": "osf/v41/prereg/acquisition_manifest_v41.md (8 SHA-256 checksums; "
                          "8/8 reproduced the t1 values on 2026-11-09; re-verified before "
                          "each runner runs).",
}

DESIGN = {
    "metric_recovery": (
        "Per-model counts k(b,m) and recognition are recovered IDENTICALLY in all three "
        "waves with the certified extraction lineage used by v0.34 and v1.8: per-model "
        "pivots for v0.19 (path A); the v1.4 certified matcher (detect_mention) on "
        "response_text for v0.20-v0.22 (path B); brand_mentions per model_id for v0.23 "
        "(path C), with the same recognition judge as t1/t2. phi and J use the v1.8 "
        "kernel as carried verbatim into score_v0_37.py (phi_of, jaccard_of)."
    ),
    "waves": ["t1 (May 2026)", "t2 (2026-06-10)", "t3 (planned 2026-11-17..21)"],
    "delta_t_days_approx": {"t1->t2": "15-21", "t2->t3": "~160", "t1->t3": "~175-185"},
    "delta_t_role": "Descriptive covariate; the horizon contrast is H_Horizon_Decay.",
}

# ---------------------------------------------------------------------------
# PARITY GATES (scoring step 0; HALT on any failure, before any t3 statistic)
# ---------------------------------------------------------------------------
PARITY = """
P1  t1 phi: per-brand phi recomputed from the frozen t1 inputs reproduces
    osf/methodology/v1_8/v1_8_instrument_table.csv for all 112 rows (definedness
    identical; |diff| <= 1e-9 where defined).
P2  t1->t2 phi reproducibility: the recomputed pooled Spearman rho(phi_t1, phi_t2)
    over brands phi-defined in both waves equals the v1.8 record 0.6454 (n = 83),
    to four decimals.
P3  v0.34 baseline: recomputed per-substrate CV-CPC t1->t2 rho reproduces
    osf/v34/v34_verdicts.json for all five substrates.
P4  Probe parity: the 8 probe artifacts reproduce the t1 SHA-256 (acquisition manifest).
A parity failure is a computational-reproducibility finding: halt, record it in
DEVIATIONS, fix the root cause, re-run the gate; no t3 statistic is computed first.
"""

# ---------------------------------------------------------------------------
# HYPOTHESES (verdicts: CONFIRMED / MARGINAL / FALSIFIED; UNDETERMINED only when the
# pre-specified n floor is not met)
# ---------------------------------------------------------------------------
HYPOTHESES = [
    {"tag": "H_Phi_LongHorizon", "tier": "PRIMARY",
     "statement": "The v1.8 Consistency instrument phi keeps its brand rank order over ~5 months.",
     "statistic": "Pooled Spearman rho(phi_t2, phi_t3) over brands phi-defined in BOTH waves "
                  "(computed exactly as v1.8's two-wave statistic). Null: stratified permutation "
                  "(t3 values permuted WITHIN substrate), 10,000 draws, one-sided, seed 410041.",
     "confirmed_iff": "rho >= 0.50 AND p_perm < 0.05",
     "falsified_iff": "rho < 0.30 OR p_perm >= 0.05",
     "marginal": "otherwise (0.30 <= rho < 0.50 with p_perm < 0.05)",
     "undetermined_iff": "fewer than 40 brands phi-defined in both waves",
     "sensitivity": "pooled within-substrate-rank Spearman (v0.37 convention); leave-one-"
                    "substrate-out range; without any snapshot-mismatched model (MC_Snapshot).",
     "threshold_rationale": "v1.8 found 0.645 over 15-21 days. 0.50 is the program's bar for a "
                            "rank-stable derived quantity (v0.34 residual gate; v1.8 ceiling)."},

    {"tag": "H_Presence_LongHorizon", "tier": "PRIMARY",
     "statement": "Brand recall Presence (pi_hat) keeps its rank order over ~5 months within substrates.",
     "statistic": "Per-substrate Spearman rho(pi_hat_t2, pi_hat_t3) over all registry brands "
                  "(pi_hat is total; ties by average rank). Null: permutation of t3 labels, "
                  "10,000 draws per substrate, one-sided.",
     "confirmed_iff": "rho >= 0.70 in >= 4/5 substrates",
     "falsified_iff": "rho < 0.50 in >= 3/5 substrates",
     "marginal": "otherwise",
     "threshold_rationale": "Same substrate-count rule as v0.34's primary. Recall carries the "
                            "variation that recognition (C_P, saturated) does not."},

    {"tag": "H_Horizon_Decay", "tier": "SECONDARY",
     "statement": "Stability is lower over the long horizon than over the short one.",
     "statistic": "For phi (pooled) and for pi_hat (pooled within-substrate ranks): "
                  "D = rho(t1,t2) - rho(t1,t3) over brands defined in all three waves; "
                  "95% CI by paired bootstrap of brand units stratified by substrate "
                  "(10,000 resamples, seed 410042).",
     "confirmed_iff": "CI lies above 0 (per instrument)",
     "falsified_iff": "CI lies below 0 (long horizon MORE stable)",
     "marginal": "CI includes 0 (no detectable decay)",
     "reported_alongside": "rho(t2,t3), rho(t1,t3) and rho(t1,t2) for phi, pi_hat, J and C_P."},

    {"tag": "H_Drift_Dissociation", "tier": "SECONDARY",
     "statement": "Long-horizon change in Consistency is not a by-product of change in Presence.",
     "statistic": "Pooled Spearman rho(delta_phi, delta_pi) over brands phi-defined at t2 and t3, "
                  "where delta = within-substrate percentile rank at t3 minus at t2. Null: "
                  "stratified permutation, 10,000 draws, two-sided.",
     "confirmed_iff": "|rho| <= 0.30",
     "falsified_iff": "|rho| >= 0.50 with p_perm < 0.05",
     "marginal": "otherwise",
     "threshold_rationale": "Extends v1.8's static mean-independence (|rho(phi, mu)| = 0.091) to "
                            "change over time; a two-component AIAS needs components that move "
                            "separately."},

    {"tag": "H_Phantom_LongPersistence", "tier": "TERTIARY (descriptive)",
     "statement": "Brands below the recall floor at t2 are still below it at t3.",
     "statistic": "Proportion of t2 phantom-flagged brands retained at t3, per substrate and "
                  "pooled; v0.34 reported 56/57 retained t1->t2.",
     "confirmed_iff": "-- descriptive only --",
     "falsified_iff": "-- n/a --"},
]

MANIPULATION_CHECKS = [
    {"tag": "MC_ProbeParity", "rule": "8/8 probe artifacts reproduce the t1 SHA-256 immediately "
                                      "before each runner runs; any mismatch halts the run."},
    {"tag": "MC_Snapshot", "rule": "For the four dated-id aliases, the t3 served id equals the t2 "
                                   "served id on every call. PASS = 4/4 models; otherwise the "
                                   "mismatched model is named and the sensitivity rule applies."},
    {"tag": "MC_Completeness", "rule": "852/852 calls return a response after logged retries; "
                                       "residual failures route to MODEL_DROP_RULE."},
    {"tag": "MC_Truncation", "rule": "descriptive: share of calls ending on a token limit "
                                     "(max_tokens / MAX_TOKENS / length) per model at t3; t1/t2 "
                                     "did not record finish reasons, so no wave contrast."},
]

SCORING = """
Output: osf/v41/v41_verdicts.json (parity gates, per-hypothesis verdicts, all rho values
with permutation p and n, the three-wave table, manipulation checks) and
osf/v41/v41_three_wave_table.csv (brand x wave: k vector, pi_hat, phi, J, C_P, CV-CPC,
phantom flag). Scorer: osf/v41/scripts/score_v41.py (fork of score_v34.py with the
v1.8 phi/J kernel from score_v0_37.py), tested on synthetic t3 data before the lock.
Spearman with average ranks; pairwise definedness per statistic; counts of brands
undefined in either wave reported per substrate.
"""

PREDICTIONS = """
H_Phi_LongHorizon: lean MARGINAL. Five months is long for a dispersion statistic over
small counts; v1.8's 0.645 at three weeks leaves room to fall below 0.50.
H_Presence_LongHorizon: lean CONFIRMED. Recall ranks have been the program's most
stable signal (v0.9 re-baseline; v0.34).
H_Horizon_Decay: lean CONFIRMED for phi, MARGINAL for pi_hat.
H_Drift_Dissociation: lean CONFIRMED, following v1.8's mean-independence.
H_Phantom_LongPersistence: lean high retention (phantom status is structural).
"""

LIMITATIONS = """
Three waves, unequal intervals (short then long): supports a horizon contrast, not a
drift-rate model. Gemini serves undated aliases, so Gemini-side version drift between
waves cannot be excluded; t1 recorded no served ids, so t1-anchored contrasts may
include version drift on any model. Default generation settings in the verbatim
runners (v0.20-v0.22 Gemini calls) follow server defaults, which may have changed
since June without a version change. Substrate N = 5 (count rules move on one
substrate); brand N = 16-24 per substrate. The verdicts bind this six-model panel;
whether they carry to the current models is a question for a new panel, after the
retirements. The deprecated google-generativeai SDK is used for verbatim fidelity.
"""

FALSIFICATION = """
- H_Phi_LongHorizon: rho < 0.30, or p_perm >= 0.05.
- H_Presence_LongHorizon: rho < 0.50 in >= 3/5 substrates.
- H_Horizon_Decay: bootstrap CI of D below 0 (per instrument).
- H_Drift_Dissociation: |rho| >= 0.50 with p_perm < 0.05.
- H_Phantom_LongPersistence: descriptive; not falsifiable.
"""

FIGURES = [
    {"id": "fig1", "topic": "phi_t2_t3", "hypothesis": "H_Phi_LongHorizon",
     "desc": "phi at t2 vs t3, pooled, substrate-coded; rho annotated; 0.50 reference."},
    {"id": "fig2", "topic": "presence_t2_t3", "hypothesis": "H_Presence_LongHorizon",
     "desc": "pi_hat t2 vs t3 by substrate; per-substrate rho; 0.70 reference."},
    {"id": "fig3", "topic": "horizon_curve", "hypothesis": "H_Horizon_Decay",
     "desc": "rho by horizon (t1-t2, t2-t3, t1-t3) for phi, pi_hat, J, C_P, with bootstrap CIs."},
    {"id": "fig4", "topic": "drift_dissociation", "hypothesis": "H_Drift_Dissociation",
     "desc": "delta-rank phi vs delta-rank pi_hat, t2->t3."},
]

CITATIONS = {
    "methodology": {"v1.6": "6816340", "v1.7": "6878818", "v1.8": "6963359"},
    "waves": {"t2 (v0.34)": "6915458"},
    "characterization": {"v0.32": "6898581", "v0.33": "6909019"},
    "t1_substrates": {"v0.19": "6809182", "v0.20": "6811441", "v0.21": "6815378",
                      "v0.22": "6829118", "v0.23": "6834298"},
    "removed_from_ssrn_cite_via_osf": {"v0.31": "6880959", "v0.35": "6921758", "v0.36": "6927958"},
    "methodology_chain_for_paper_bib": ["v1.2 6761698", "v1.3 6797679", "v1.4 6799479",
                                        "v1.5 6810758", "v1.6 6816340", "foundational 6659000"],
    "framework": "MSI Working Paper Report No. 26-132, only if the paper invokes the Tri-System framework",
}

DEVIATIONS = [
    {
        "entry_id": "Entry 0",
        "type": "ex-ante pre-acquisition lock (COI screen + external-anchor preamble)",
        "ex_ante": True,
        "logged_before_any_acquisition_call": True,
        "coi_screen": ("Registries are bit-identical to the t1 locks; v0.41 performs NO new "
                       "brand selection, so each substrate carries its source-phase COI "
                       "handling forward UNCHANGED - not a fresh 'no affiliation' assertion. "
                       "Items of record, as carried by v0.34 Entry 0: (a) v0.22 automotive - the "
                       "locked v0.22 Declarations COI discloses that Samsung subsidiaries hold "
                       "TIER-2/3 component supply relationships with several registry brands "
                       "(Harman International - audio; Samsung SDI - battery cells; Samsung "
                       "Display - infotainment), characterized as non-competitive with no "
                       "brand-level overlap and imposing no operational restriction on registry "
                       "composition (v0.22 DEVIATIONS Entry 0 Part B); (b) v0.19 audiophile "
                       "headphones - AKG was SUBSTITUTED with Denon BEFORE the v0.19 pre-reg lock "
                       "(AKG owned by Harman International, a Samsung subsidiary, since 2016) to "
                       "avoid appearance of conflict (v0.19 DEVIATIONS Entry 1). Do NOT lock a "
                       "blanket 'no Samsung affiliation' claim."),
        "non_acquisition_steps_declared": ("Pre-lock feasibility check, 2026-11-09 05:23 UTC: one "
                       "neutral prompt ('Reply with the single word: ready') to each alias through "
                       "each runner call path, 18 calls, 18 ok; no study probe sent "
                       "(osf/v41/prereg/feasibility_v0_41.json)."),
        "anchor_preamble": ("BINDING SEQUENCE, before the first t3 call: (1) content lock; "
                            "(2) commit; (3) tag v0.41-prereg-r1; (4) git push origin v0.41 --tags; "
                            "(5) osf_upload.py osf/v41/prereg -> osf.io/ec6wh/v41/prereg/; "
                            "(6) verify BOTH remotes resolve; (7) ONLY THEN the first t3 call. "
                            "OSF_TOKEN confirmed present before (5)."),
        "lock_state": "DRAFT (not locked)",
    },
]
