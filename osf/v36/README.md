# AIAS v0.36 — CPC Regime Emergence

OSF deposit for the AIAS™ Presence Measurement Protocol, v0.36.

**Phase type — fully retrospective re-analysis (no new LLM acquisition).** Tests
whether cross-platform consistency (CPC) carries *regime structure* — whether
per-brand CPC clusters recover the brand-presence hierarchy (inheritance), form an
independent typology (autonomy), survive residualization on Presence (layered), or
collapse under recognition saturation (degeneracy). Inputs are frozen: the per-model
recall vectors for the five panel-uniform omnibus substrates (v0.19–v0.23; 112
brand-units; canonical six-model panel), read from the v0.33 deposit
(`osf/v33/data/v33_eta2.csv`). CV-CPC is used strictly as the characterization
quantity fixed by Protocol v1.7 (Presence-coupled, |ρ| = 0.77; *not adopted*). The
per-brand regime target and Presence composite are read as frozen fields from the
v0.23 deposit (`brand_details[].regime` / `composite_presence`), present for v0.23
only. **CPC inputs trace to the v0.31 phase (SSRN 6880959), consumed as archived data
provenance only — its paper is withdrawn and it is not cited as methodological
authority.**

**No brand registry this phase.** v0.36 introduces no new panel; it reuses the locked
v0.19–v0.23 registries by reference (and inherits their COI screen). The pre-registration's
"registry" slot is an analysis-set specification, not a brand list.

**Status:** scored and locked. Pre-registration tags `v0.36-prereg-r1/r2/r3` (see below);
scoring, figures, brand-format report, and SSRN paper complete. SSRN abstract ID pending
submission.

## Headline result

Pre-registered prediction **Cell A (borrowed structure)** was falsified; the phase
landed in **Cell D (unstructured)**. No hypothesis met its locked bar:
H_RegimeInheritance unevaluable at power (CV computability floor left 9 of 24 units in
the label-bearing substrate; gap k = 1; ARI = 0.0); H_RegimeAutonomy not supported
(omnibus k = 3, silhouette 0.2422 vs the locked 0.25, above the permutation null);
H_ResidualStructure not supported (k = 1), as predicted; H_SaturationDegeneracy not
supported and direction-reversed (saturated dispersion 0.095 vs 0.024; Levene p = .003
opposite sign; per-substrate gap 2/3/2/4/1). The failure modes converge on
mean-coupling pathology in the CV instrument, constraining the v1.8 specification
(mean-independence; graded recognition; defined coverage for low-recall brands).

## Pre-registration lineage

- **`v0.36-prereg-r1`** — initial lock; hypotheses, thresholds, decision rules, verdict
  matrix, predictions, deposited before any statistic was computed.
- **`v0.36-prereg-r2`** — outcome-blind corrections: data-lineage defect, construct-identity
  correction (the three-way "regime" overloading), recognition-commensurability finding,
  per-criterion scope assignment, gap range k = 1–8, and the seed-bearing scorer. (r2
  deposit timestamp postdates the deterministic run; authorship outcome-blind per the
  deviations log.)
- **`v0.36-prereg-r3`** — post-results deviations-log addition (DEVIATIONS Entry 5; **not**
  outcome-blind): records that the locked sensitivity arms were executed in a deterministic
  second pass after primary verdicts existed. No hypothesis, threshold, prediction, or
  primary verdict changed; Cell D stands at the primary floor. The 84-unit robustness arm
  returned discordant (silhouette 0.350 at the looser inclusion floor; configuration
  unmapped in the locked matrix), and the entry records that the locked verdict matrix is
  non-exhaustive (autonomy + no-residual maps to no cell).

Earlier tags remain intact in version history; r3 supersedes for the canonical record.

## Sensitivity / robustness (§3.5; r3 / Entry 5)

- Scalar CV-CPC arm: gap k = 1, ARI = 0.0 vs the 6-dim primary (structure is multivariate).
- K-means at gap-selected k = 3 (50 restarts): ARI = 0.43 vs Ward.
- v0.35 84-unit concordance: **discordant** — at the inclusion floor (mean recall > 0,
  n = 84) the omnibus silhouette rises to 0.350 and the autonomy criteria clear; the Cell D
  verdict is recall-floor-sensitive. Reported, not adjudicated.

## Tree

- `v36_verdicts.json` — per-hypothesis verdicts, scopes, statistics, verdict-matrix cell,
  selected k per arm, the sensitivity block, and the deviations note (seed 36).
- `prereg/` — locked pre-registration artifacts (content module + mega-prompt; tags r1–r3)
- `scoring/` — `v36_verdicts.json` and `data/` (cluster assignments, gap curves, ARI null,
  per-substrate variance, silhouette + sensitivity summaries, dendrogram linkage)
- `figures/` — five chart PDFs (`chart_01_omnibus_structure` … `chart_05_verdict_matrix`;
  register-neutral)
- `reports/` — brand-format report PDF
- `scripts/` — scoring code (`score_v0_36.py`; ARI/silhouette/k-means/gap implemented
  in-script, no external ML dependency; deterministic at seed 36)

## Pipeline (re-analysis; no acquisition)

1. Pre-registration locked at `v0.36-prereg-r1`; amended r2 (corrections) / r3 (deviations log)
2. Score: `python3 scripts/score_v0_36.py` → `v36_verdicts.json` (+ intermediates)
3. Build figures: `python3 scripts/build_charts_v36.py`
4. Build report: `python3 reports/build_report_v36.py`
5. Build SSRN paper: `python3 scripts/build_paper_v0_36.py`
6. OSF deposit: `python3 ~/aias/scripts/osf_upload.py ~/aias/osf/v36/<subdir> v36/<subdir>`
