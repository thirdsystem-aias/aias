"""
v0.34 - CPC Longitudinal t1->t2 Stability - Pre-Registration Content Module
AIAS(TM) Measurement Program - Third System(TM)

Locked pre-registration artifact (tag v0.34-prereg-r1).

PROSPECTIVE LONGITUDINAL re-acquisition. Full re-acquisition at t2 (June 2026) of
the five panel-uniform omnibus substrates first acquired at t1 (v0.19-v0.23), to
test whether the CPC-family quantities (CV-CPC, C_P) are temporally stable across a
~2-3 week interval at fixed registries, fixed probe wording, and the t1 model-alias
panel. Re-acquisition uses each substrate's t1 acquisition runner VERBATIM
(re-pointed only at osf/v34/data/); probe-set byte-fidelity is locked in
osf/v34/prereg/acquisition_manifest_v34.md (five SHA-256 checksums).

NOTE ON SCAFFOLD: this module was scaffolded from v0.33 and has been REPLACED in
full. v0.34 is not a re-analysis: it is a prospective re-acquisition with its own t2
data. The prior phase's between-provider variance-decomposition schema does not apply
and is not present below.
"""

PHASE_ID = "v0.34"
PHASE_TITLE = "CPC Longitudinal t1->t2 Stability"
METHODOLOGY_LOCK = "v1.7"          # CV-CPC definition inherited; walled (v1.7 did NOT adopt CV-CPC)
PRESENCE_LOCK = "v1.6"             # C_P (Presence) definition
INSTRUMENT_SOURCE = "v0.30"        # CV-CPC instrument origin (pilot spec)
PHASE_TYPE = "prospective_longitudinal"   # full re-acquisition at t2; NOT a re-analysis
PREREG_TAG = "v0.34-prereg-r1"

# Temporal anchors -----------------------------------------------------------
T1 = "original substrate-phase acquisition (May 2026); per-substrate dates in DESIGN.delta_t"
T2 = "v0.34 re-acquisition, first call >= 2026-06-10, recorded exactly at run time"

# ---------------------------------------------------------------------------
# LINEAGE (v0.31-uncited; locked).  t1 data routes through the substrate phases
# and the CPC methodology through v1.7 - NOT through v0.31 (SSRN 6880959).
# v0.31's extraction FUNCTIONS may be reused as a computational tool (score_v0_31
# extractors) without CITING v0.31; the citeable parity anchor is v1.7 r_per_model.
# See acquisition_manifest_v34.md.
# ---------------------------------------------------------------------------
LINEAGE = """
t1 substrate lineage: v0.19 audiophile headphones (6809182), v0.20 skincare
(6811441), v0.21 cosmetics (6815378), v0.22 automotive (6829118), v0.23 premium
spirits (6834298). CPC methodology lineage: v1.7 CV-CPC definition + negative
result (6878818); v1.6 C_P/Presence lock (6816340). Characterization arc:
v0.32 version-snapshot stability (6898581), v0.33 provider-asymmetric
characterization (6909019). v0.31 is deliberately uncited; the phase
is defensible regardless of 6880959's status.
"""

# ---------------------------------------------------------------------------
# SUBSTRATE SCOPE (the 5 panel-uniform omnibus substrates; 112 brand units).
# ---------------------------------------------------------------------------
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
N_BRAND_UNITS = 112        # 16 + 24*4
N_SUBSTRATE_UNITS = 5

# ===========================================================================
# METRIC DEFINITIONS (inherited verbatim; NOT redefined in this phase).
# ===========================================================================
PANEL_N = 6
DISPERSION = "CV = population_SD / mean (ddof=0)"
TRANSFORM = "CV-CPC = 1 / (1 + CV)"          # bounded (0, 1]; higher = more consistent
CPC_RANGE = "(0, 1]"
C_P_DEF = "C_P = count of panel models (0..6) recognizing the brand in Phase A (v1.6)"
FLOOR = {
    "rule": "mean(per-model recall count) < 1.0  ->  CV-CPC = UNDEFINED (N/A)",
    "handling": ("Undefined brands excluded PAIRWISE from a substrate's t1<->t2 "
                 "Spearman (a brand must be defined in BOTH waves to enter rho); "
                 "count of undefined-either-wave brands reported per substrate."),
    "note": "Inherited v1.7 floor; no phase-level floor introduced.",
}
# CV-CPC is reused as-computed; v1.7 found it Presence-coupled (|rho|=0.77) and did
# NOT adopt it. This phase measures the TEMPORAL stability of that quantity; it makes
# no claim that CV-CPC is a valid Consistency instrument. Walled accordingly.

# ---------------------------------------------------------------------------
# PANEL + MODEL-ID PINNING (resolved: alias verbatim; see acquisition_manifest).
# ---------------------------------------------------------------------------
PROVIDER_GROUPS = {
    "Anthropic": ["Claude Opus 4.5", "Claude Sonnet 4.5"],
    "OpenAI":    ["GPT-4o", "GPT-4o-mini"],
    "Google":    ["Gemini 2.5 Flash", "Gemini 2.5 Flash Lite"],
}
# Panel-status table. STATUS from the 2026-06-10 reachability probe (6/6 resolved).
# t1 pinning was by ALIAS in every substrate runner; no t1 substrate captured the
# provider-returned dated snapshot, so dated-ID pinning at t2 is INFEASIBLE. t2
# re-acquires with the SAME aliases (verbatim runner) and writes the provider-returned
# dated ID per call to a SIDECAR file (osf/v34/data/v34_provenance.csv) - runner OUTPUT
# SCHEMAS ARE UNTOUCHED, preserving the parity/smoke-test schema check (a t1->t2 forward
# improvement; baseline for a future t3). Silent version drift between waves is thus
# PART of the measured (in)stability - named in LIMITATIONS.
PANEL_STATUS = [
    {"alias": "claude-opus-4-5",        "provider": "Anthropic", "t2_resolved": "claude-opus-4-5-20251101",   "status": "OK", "t1_pin": "alias (verbatim)"},
    {"alias": "claude-sonnet-4-5",      "provider": "Anthropic", "t2_resolved": "claude-sonnet-4-5-20250929", "status": "OK", "t1_pin": "alias (verbatim)"},
    {"alias": "gpt-4o",                 "provider": "OpenAI",    "t2_resolved": "gpt-4o (alias)",              "status": "OK", "t1_pin": "alias (verbatim)"},
    {"alias": "gpt-4o-mini",            "provider": "OpenAI",    "t2_resolved": "gpt-4o-mini (alias)",         "status": "OK", "t1_pin": "alias (verbatim)"},
    {"alias": "gemini-2.5-flash",       "provider": "Google",    "t2_resolved": "models/gemini-2.5-flash",     "status": "OK", "t1_pin": "alias (verbatim)"},
    {"alias": "gemini-2.5-flash-lite",  "provider": "Google",    "t2_resolved": "models/gemini-2.5-flash-lite","status": "OK", "t1_pin": "alias (verbatim)"},
]
PANEL_RESOLVED_AT = "2026-06-10 (6/6 OK; min-viable-panel = 4)"

MODEL_DROP_RULE = """
Any pinned model alias unavailable at t2 acquisition is excluded PAIRWISE from all
paired statistics (the per-brand CV-CPC / C_P vectors drop that model in BOTH waves
for comparability), with a contemporaneous DEVIATIONS entry. Minimum viable panel =
4 models; below 4 the phase HALTS for re-scope rather than proceeding on a degraded
panel. At lock (2026-06-10) all six resolve; no drop in effect.
"""

# ---------------------------------------------------------------------------
# ACQUISITION (re-acquisition; verbatim t1 runners, re-pointed to osf/v34/data/).
# Probe-set byte-fidelity is locked by checksum in acquisition_manifest_v34.md.
# ---------------------------------------------------------------------------
ACQUISITION = {
    "design": "Full re-acquisition of Phase A (Recognition) + Phase B (two-channel "
              "six-frame Recall) for all 5 substrates at t2. Registries bit-identical "
              "to t1 locks; probe wording verbatim; panel = t1 aliases.",
    "per_wave_call_counts": {
        "phase_a_recognition": "672  (v19 16x6=96; v20-23 24x6=144 each)",
        "phase_b_recall":      "180  (5 substrates x 6 frames x 6 models)",
        "total_per_wave":      "852",
    },
    "runners_verbatim": [
        {"phase": "v0.19", "runner": "osf/v19/run_v0_19.py",
         "probe_set": ["osf/v19/phase_a_queries.jsonl", "osf/v19/phase_b_queries.jsonl",
                       "osf/v19/thresholds_v0_19.json"],
         "output_t2": "osf/v34/data/ (re-pointed from SCRIPT_DIR)"},
        {"phase": "v0.20", "runner": "scripts/run_acquisition_v20.py",
         "probe_set": ["prereg/v0_20_registry.json (phase_a_probe_template, phase_b_frames)"],
         "output_t2": "osf/v34/data/v34_v20_phase_{a,b}.csv"},
        {"phase": "v0.21", "runner": "scripts/run_acquisition_v21.py",
         "probe_set": ["prereg/v0_21_registry.json (phase_a_probe_template, phase_b_frames)"],
         "output_t2": "osf/v34/data/v34_v21_phase_{a,b}.csv"},
        {"phase": "v0.22", "runner": "scripts/run_acquisition_v22.py",
         "probe_set": ["prereg/v0_22_automotive_content.py (REGISTRY)",
                       "scripts/run_acquisition_v22.py (PHASE_A_PROBE_TEMPLATE, PHASE_B_FRAMES embedded)"],
         "output_t2": "osf/v34/data/v34_v22_phase_{a,b}.csv (re-pointed from osf/v22/)"},
        {"phase": "v0.23", "runner": "scripts/acquire_v0_23.py",
         "probe_set": ["scripts/acquire_v0_23.py (REGISTRY + prompt embedded)"],
         "output_t2": "osf/v34/data/ (re-pointed)"},
    ],
    "byte_fidelity_lock": "osf/v34/prereg/acquisition_manifest_v34.md (5 SHA-256 "
                          "checksums; re-verified immediately before each runner runs).",
    "dispatcher_note": "A run_acquisition_v34.py dispatcher, if used, is a LOGGING SHELL "
                       "only (invoke-and-log); it must not alter probe text, ordering, or "
                       "output schema. Default: manifest alone, five runners invoked directly.",
    "permitted_runner_edits": [
        "(i) the output-directory constant (re-point to osf/v34/data/);",
        "(ii) emission of the provenance SIDECAR (osf/v34/data/v34_provenance.csv).",
        "NOTHING ELSE. Probe text, frame ordering, registry, and the runner's own output "
        "schema (CSV/JSON columns) are byte-frozen against the t1 checksums; any change "
        "beyond (i)-(ii) voids the verbatim/parity commitment and the smoke-test check.",
    ],
    "provider_version_capture": "t2 runners append (substrate, phase, call_index, alias, "
                                 "returned_model_id, timestamp) to the SIDECAR file "
                                 "osf/v34/data/v34_provenance.csv. Runner output schemas "
                                 "are NOT modified (t1 did not capture returned IDs at all).",
}

# ---------------------------------------------------------------------------
# DESIGN: per-wave per-brand metric recovery + Delta_t covariate.
# ---------------------------------------------------------------------------
DESIGN = {
    "metric_recovery": (
        "Per-brand CV-CPC and per-brand C_P are computed IDENTICALLY in both waves via "
        "the locked t1 pipeline: the v1.4 certified brand matcher (detect_mention) for "
        "raw-text substrates (v0.20-22), per-model pivots for v0.19 (path A) and v0.23 "
        "(path C). Extraction is the score_v0_31/score_v33 function set reused as a "
        "computational tool (v0.31 uncited)."
    ),
    "extraction_paths": {
        "A_v19": "panel_model + mentioned/rank already per-model; pivot to x_{b,m}.",
        "B_v20_22": "brand NOT pre-coded; detect via v1.4 detect_mention on response_text, pivot per model.",
        "C_v23": "parse brand_mentions per model_id; recognition r_level normalized to binary (R0->0 else 1).",
    },
    "delta_t": [
        {"phase": "v0.19", "t1": "2026-05-20", "t2": ">=2026-06-10", "delta_days_approx": 21},
        {"phase": "v0.20", "t1": "2026-05-21", "t2": ">=2026-06-10", "delta_days_approx": 20},
        {"phase": "v0.21", "t1": "2026-05-22", "t2": ">=2026-06-10", "delta_days_approx": 19},
        {"phase": "v0.22", "t1": "2026-05-25", "t2": ">=2026-06-10", "delta_days_approx": 16},
        {"phase": "v0.23", "t1": "2026-05-26", "t2": ">=2026-06-10", "delta_days_approx": 15},
    ],
    "delta_t_role": "Descriptive covariate only. NO Delta_t-dependent hypothesis; "
                    "per-substrate Delta_t reported in the design table, heterogeneity "
                    "discussed in LIMITATIONS. Exact t2 dates stamped at acquisition.",
}

# ---------------------------------------------------------------------------
# HYPOTHESES
# ---------------------------------------------------------------------------
HYPOTHESES = [
    {"tag": "H_CPC_Temporal_Stability", "tier": "PRIMARY",
     "statement": "Per-brand CV-CPC rank order is stable from t1 to t2 within each substrate.",
     "statistic": "Per-substrate Spearman rho between per-brand CV-CPC at t1 and t2 "
                  "(brands defined in BOTH waves).",
     "confirmed_iff": "rho >= 0.70 in >= 4/5 substrates",
     "falsified_iff": "rho < 0.50 in >= 3/5 substrates",
     "undetermined": "otherwise MARGINAL",
     "null": "Monte Carlo permutation, >= 10,000 draws per substrate (v0.33 convention)."},

    {"tag": "H_CPC_Drift_Beyond_Presence", "tier": "PRIMARY (gate)",
     "statement": "CV-CPC temporal drift carries structure BEYOND Presence drift "
                  "(it is not merely Presence drift in costume).",
     "statistic": "(a) per-substrate Spearman rho(Delta-CV-CPC, Delta-C_P) across brands "
                  "[how much CPC drift tracks Presence drift]; (b) residual-CV-CPC "
                  "stability: Spearman rho between t1 and t2 of CV-CPC residualized on "
                  "C_P WITHIN each wave.",
     "confirmed_iff": "residual-CV-CPC rho >= 0.50 in >= 3/5 substrates",
     "falsified_iff": "residual-CV-CPC rho < 0.50 in > 2/5 substrates, or residualization "
                      "degenerate (see saturation caveat)",
     "undetermined": "marginal / fragile under the saturation caveat",
     "reported_alongside": "statistic (a) rho(Delta-CV-CPC, Delta-C_P) reported for every "
                           "substrate regardless of the gate verdict.",
     "directional_lean": "FALSIFIED-or-marginal. Given v1.7 Presence-coupling (rho=0.77) "
                         "and the v0.33 saturation-collapse finding, the expectation is "
                         "that CPC drift is largely Presence drift in costume."},

    {"tag": "H_Presence_Temporal_Stability", "tier": "SECONDARY",
     "statement": "Per-brand C_P (Presence) rank order is stable from t1 to t2 within each substrate.",
     "statistic": "Per-substrate Spearman rho between per-brand C_P at t1 and t2.",
     "confirmed_iff": "rho >= 0.80 in >= 4/5 substrates",
     "falsified_iff": "rho < 0.60 in >= 3/5 substrates",
     "undetermined": "otherwise MARGINAL",
     "threshold_rationale": "Higher bar than the 0.70 CV-CPC primary - deliberate. "
                            "Presence is the established/validated component; the v0.9 "
                            "Re-Baseline precedent supports strong temporal stability; and "
                            "it is the comparator floor for the Beyond_Presence gate."},

    {"tag": "H_Phantom_Temporal_Persistence", "tier": "TERTIARY (exploratory)",
     "statement": "t1 phantom-flagged brands retain phantom status at t2.",
     "statistic": "Proportion of t1 phantom-flagged brands still phantom-flagged at t2, "
                  "per substrate and pooled (phantom flag per v0.31/v1.7 recall-floor "
                  "classification).",
     "confirmed_iff": "-- descriptive only; no confirmation threshold --",
     "falsified_iff": "-- n/a (exploratory) --"},
]

# ---------------------------------------------------------------------------
# SCORING
# ---------------------------------------------------------------------------
SCORING = """
Output: osf/v34/v34_verdicts.json (per-hypothesis verdict against the locked
criteria above, plus per-substrate rho values, permutation p-values, defined-brand
counts, the rho(Delta-CV-CPC, Delta-C_P) table, residual-CV-CPC rho, phantom
persistence proportions, and the Delta_t design table).

Per-brand metrics (both waves, identical pipeline):
- CV-CPC_{b} = 1 / (1 + CV(x_{b,1..6})), x = per-model Phase B recall count (0..6);
  FLOOR mean(x) < 1.0 -> UNDEFINED.
- C_P_{b}    = count of panel models recognizing b in Phase A (0..6), v1.6.

PRIMARY (H_CPC_Temporal_Stability): per substrate, Spearman rho over brands defined
in BOTH waves between CV-CPC_t1 and CV-CPC_t2. Null: Monte Carlo permutation of the
t2 brand labels, >= 10,000 draws, one-sided; report observed rho, null mean/q95, p.
Verdict from the >=4/5 (CONFIRMED) / >=3/5 (FALSIFIED) substrate-count thresholds.

PRIMARY gate (H_CPC_Drift_Beyond_Presence):
  (a) Delta-coupling: Delta-CV-CPC_b = CV-CPC_t2 - CV-CPC_t1; Delta-C_P_b likewise;
      per-substrate Spearman rho(Delta-CV-CPC, Delta-C_P). Reported for all 5.
  (b) Residualization: within EACH wave, regress CV-CPC on C_P (OLS) across brands;
      take residuals; per-substrate Spearman rho between t1-residual and t2-residual.
      Gate CONFIRMED iff residual rho >= 0.50 in >= 3/5 substrates.
  SATURATION CAVEAT (carried from v0.33): if C_P is saturated among recalled brands,
  residual-CV-CPC ~ CV-CPC and the gate is uninformative rather than confirmed. SINGLE
  pre-registered trigger: a substrate is saturation-flagged iff all six models
  recognize >= 90% of its defined brands. A flagged substrate's gate contribution is
  down-weighted to MARGINAL (it counts toward neither the >=3/5 CONFIRMED nor the >=3/5
  FALSIFIED tally). var(C_P|defined) is reported descriptively for context, but the
  >=90% rule is the only verdict-bearing trigger.

  Note (design, not oversight): absent saturation the gate verdict space is deliberately
  BINARY - residual rho >= 0.50 in >= 3/5 (CONFIRMED) vs residual rho < 0.50 in >= 3/5
  (FALSIFIED) partition all five-substrate outcomes (k>=3 or 5-k>=3 for every k in 0..5).

SECONDARY (H_Presence_Temporal_Stability): per substrate Spearman rho(C_P_t1,
C_P_t2); same permutation null; >=4/5 at 0.80 (CONFIRMED) / >=3/5 below 0.60
(FALSIFIED).

TERTIARY (phantom persistence): descriptive proportion only.

PAIRWISE DEFINEDNESS: a brand enters a substrate's t1<->t2 Spearman only if defined
in both waves; undefined-either-wave counts reported. Tie handling: Spearman with
average ranks (scipy default).
"""

# ---------------------------------------------------------------------------
# PARITY / RECONCILIATION (scoped; do not conflate the two anchor regimes).
# ---------------------------------------------------------------------------
PARITY = """
t1-side recompute parity targets differ by substrate and MUST NOT be conflated:

- v0.20 / v0.21 / v0.22: the recomputed t1 per-model RECALL vectors MUST reproduce
  osf/methodology/v1_7/data/v1_7_cpc.csv 'r_per_model' BIT-FOR-BIT (aligned by model
  name; v1.7 stored sorted-model order, PANEL order differs). This is the citeable
  external anchor. Mismatch => computational-reproducibility note in the OSF README
  (NOT a DEVIATIONS entry); HALT recompute until resolved. score_v33 already gates
  on this for 72/72 brand units.

- v0.19 / v0.23: the v1.7 anchor's scope does NOT cover these (standing OSF README
  footnote). Parity target is instead BIT-FOR-BIT reproduction of the frozen
  per-model t1 inputs as consumed by the v0.31->v0.33 arc - i.e. the counts_v19 /
  counts_v23 extractor outputs. Correctness rests on the extraction-function
  provenance alone; stated, not overclaimed.

v0.23 normalization footnote (carried forward, binding): v0.23 recognition is scored
as r_level; it is normalized to binary (R0 -> 0, else -> 1) for C_P, identically in
both waves. This footnote appears in the OSF README and the paper's methods.
"""

# ---------------------------------------------------------------------------
# PREDICTIONS
# ---------------------------------------------------------------------------
PREDICTIONS = """
H_CPC_Temporal_Stability: lean CONFIRMED-or-marginal. CV-CPC tracks recall which is
fairly stable over ~2-3 weeks at fixed wording; but CV-CPC is a ratio of small
integer counts (0..6) and is noise-sensitive at low mean recall, so some substrates
may fall to MARGINAL.
H_CPC_Drift_Beyond_Presence: GENUINELY OPEN, lean FALSIFIED-or-marginal - the
substantive core of the phase. Presence-coupling (rho=0.77) and v0.33 saturation
make pure-Presence inheritance the prior.
H_Presence_Temporal_Stability: lean CONFIRMED. Presence (recognition) is the most
stable component; v0.9 Re-Baseline precedent.
H_Phantom_Temporal_Persistence: lean high persistence (phantom status is structural,
not sampling noise); descriptive only.
"""

# ---------------------------------------------------------------------------
# LIMITATIONS
# ---------------------------------------------------------------------------
LIMITATIONS = """
Two-wave design: a single t1->t2 interval (~15-21 days, heterogeneous across
substrates) supports a stability/instability READING, not a drift-rate model. No
Delta_t-dependent hypothesis; Delta_t heterogeneity is descriptive.

Version drift inside the alias panel: t1 pinned aliases and did not record the
resolved dated snapshot, so any t1->t2 model-version change (e.g. claude-opus-4-5
-> a newer dated snapshot) is SILENT and is PART of the measured (in)stability, not
controlled out. This is the honest reading: the study measures stability of the
quantity a fixed-alias caller would observe, version drift included. t2 captures the
dated ID forward, enabling a version-isolated t3.

Instrument inheritance: CV-CPC is Presence-coupled and not adopted (v1.7). The
Beyond_Presence gate, not the bare temporal-stability test, carries any
Consistency-specific claim - and is itself subject to the saturation caveat that
collapsed the analogous v0.33 gate.

Substrate N = 5: thresholds are substrate-COUNT rules (>=4/5, >=3/5); a single
substrate flip moves a verdict. Brand-level N (16-24/substrate) bounds per-substrate
Spearman precision; small-n rho is reported with its permutation p.

Recompute provenance: v0.20/0.21/0.22 externally anchored to v1.7 r_per_model;
v0.19 and v0.23 rest on extraction-function provenance alone (see PARITY).
"""

# ---------------------------------------------------------------------------
# FALSIFICATION
# ---------------------------------------------------------------------------
FALSIFICATION = """
Per-hypothesis falsification (falsified_iff in HYPOTHESES):
- H_CPC_Temporal_Stability:    rho < 0.50 in >= 3/5 substrates.
- H_CPC_Drift_Beyond_Presence: residual-CV-CPC rho < 0.50 in > 2/5 substrates, or
                               residualization degenerate under saturation.
- H_Presence_Temporal_Stability: rho < 0.60 in >= 3/5 substrates.
- H_Phantom_Temporal_Persistence: exploratory; not falsifiable in this phase.
"""

# ---------------------------------------------------------------------------
# FIGURES (confirmatory set; paper figure set)
# ---------------------------------------------------------------------------
FIGURES = [
    {"id": "fig1", "topic": "cpc_t1_t2_stability", "hypothesis": "H_CPC_Temporal_Stability (PRIMARY)",
     "desc": "Per-brand CV-CPC t1 vs t2 by substrate, per-substrate Spearman rho annotated, 0.70 reference line."},
    {"id": "fig2", "topic": "residual_cpc_stability", "hypothesis": "H_CPC_Drift_Beyond_Presence (PRIMARY gate)",
     "desc": "Residual-CV-CPC (on C_P) t1 vs t2 plus rho(Delta-CV-CPC, Delta-C_P) coupling; saturation-flagged substrates marked."},
    {"id": "fig3", "topic": "presence_t1_t2_stability", "hypothesis": "H_Presence_Temporal_Stability (SECONDARY)",
     "desc": "Per-brand C_P t1 vs t2 by substrate, per-substrate Spearman rho, 0.80 reference band."},
    {"id": "fig4", "topic": "phantom_persistence", "hypothesis": "H_Phantom_Temporal_Persistence (TERTIARY)",
     "desc": "t1->t2 phantom-flag retention proportions, per substrate and pooled (descriptive)."},
]

# ---------------------------------------------------------------------------
# CITATION SET (locked; v0.31 deliberately uncited)
# ---------------------------------------------------------------------------
CITATIONS = {
    "methodology": {"v1.6": "6816340", "v1.7": "6878818"},
    "characterization": {"v0.32": "6898581", "v0.33": "6909019"},
    "t1_substrates": {"v0.19": "6809182", "v0.20": "6811441", "v0.21": "6815378",
                      "v0.22": "6829118", "v0.23": "6834298"},
    "uncited_deliberate": {"v0.31": "6880959 — uncited by design"},
    "methodology_chain_for_paper_bib": ["v1.2 6761698", "v1.3 6797679", "v1.4 6799479",
                                        "v1.5 6810758", "v1.6 6816340", "foundational 6659000"],
}

# ---------------------------------------------------------------------------
# DEVIATIONS
# Entry 0 = (i) pre-acquisition COI screen (CLAUDE.md non-negotiable) and
#           (ii) external-anchor procedural preamble (the timestamp chain).
# No "Entry -1": prior phases (v0.30, v0.32) log the ex-ante lock as Entry 0; the
# anchor preamble lives WITHIN Entry 0.
# ---------------------------------------------------------------------------
DEVIATIONS = [
    {
        "entry_id": "Entry 0",
        "type": "ex-ante pre-acquisition lock (COI screen + external-anchor preamble)",
        "ex_ante": True,
        "logged_before_any_acquisition_call": True,
        "coi_screen": ("Registries are bit-identical to the t1 locks; v0.34 performs NO "
                       "new brand selection, so each substrate carries its source-phase "
                       "COI handling forward UNCHANGED - not a fresh 'no affiliation' "
                       "assertion. Items of record, paraphrased faithfully from the source "
                       "phases: (a) v0.22 automotive - the locked v0.22 Declarations COI "
                       "discloses that Samsung subsidiaries hold TIER-2/3 component supply "
                       "relationships with several registry brands (Harman International - "
                       "audio; Samsung SDI - battery cells; Samsung Display - infotainment), "
                       "characterized as non-competitive with no brand-level overlap and "
                       "imposing no operational restriction on registry composition (v0.22 "
                       "DEVIATIONS Entry 0 Part B); (b) v0.19 audiophile headphones - AKG was "
                       "SUBSTITUTED with Denon BEFORE the v0.19 pre-reg lock (AKG owned by "
                       "Harman International, a Samsung subsidiary, since 2016) to avoid "
                       "appearance of conflict (v0.19 DEVIATIONS Entry 1). The v0.34 paper's "
                       "Declarations COI carries the v0.22 tier-2/3 language forward; do NOT "
                       "lock a blanket 'no Samsung affiliation' claim."),
        "anchor_preamble": ("BINDING SEQUENCE, recorded before the first API call: "
                            "(1) content lock; (2) commit; (3) git tag v0.34-prereg-r1; "
                            "(4) git push origin v0.34 --tags; (5) osf_upload.py "
                            "osf/v34/prereg -> osf.io/ec6wh/v34/prereg/; (6) verify BOTH "
                            "remotes resolve; (7) ONLY THEN the first t2 acquisition call. "
                            "OSF_TOKEN confirmed present before step (5) so a failed "
                            "upload cannot leave a pushed tag without its deposit "
                            "(no half-anchored state)."),
        "lock_state": "v0.34-prereg-r1",
    },
]
