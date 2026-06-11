# AIAS v0.35 — Naive-Phantom × CPC Omnibus

OSF deposit for AIAS™ Presence Measurement Protocol, v0.35.

**Phase type — re-analysis (no new LLM acquisition; v0.33 pattern).** Tests whether
phantom-flagged brands carry a distinct CV-CPC consistency signature beyond Presence,
on the frozen t₁ inputs of the five panel-uniform omnibus substrates (v0.19–v0.23;
112 brand units; canonical six-model panel). CV-CPC is used strictly as a
characterization quantity per v1.7 (Presence-coupled, |ρ|=0.77; *not adopted*). The
phase's inferential weight rests on a gating hypothesis with two co-primary controls
and a binding flip rule. t₁ lineage routes through the substrate phases and v1.7;
**v0.31 (SSRN 6880959) is consumed as archived data provenance only — its paper is
withdrawn and it is not cited as methodological authority.**

**Status:** scored and locked. Pre-registration tag `v0.35-prereg-r1` (externally
anchored before analysis); scoring, figures, brand-format report, and SSRN paper
complete. **SSRN abstract ID 6921758** (https://ssrn.com/abstract=6921758).

## Headline result

PRIMARY gate **H_Phantom_Beyond_Presence: UNDETERMINED (control flip).** Residualized
on recognition (C_P) the phantom contrast survives (pooled Cliff's δ = −0.797,
p = 0.0001); residualized on recall-mean it vanishes (δ = +0.068, p = 0.655). Recognition
is saturated (C_P constant) in three of five substrates, so the C_P control is inert
exactly where the contrast lives; the recall-mean control removes the axis that defines
the phantom flag. The flip is leave-one-substrate-out stable and reproduces on the v0.34
t₂ wave; it is the pre-registered finding, routed to v1.8. The raw arm (δ = −0.838) is
reported as a manipulation check only (both sides recall-coupled by construction).

## Recompute parity (scoped — do not conflate)

- **v0.20 / 0.21 / 0.22:** recomputed per-model recall reproduces
  `osf/methodology/v1_7/data/v1_7_cpc.csv` `r_per_model` **bit-for-bit** (citeable external
  anchor; `score_v33` gate 72/72). Mismatch → computational-reproducibility note, halt.
- **v0.19 / 0.23:** the v1.7 anchor does **not** cover these. Parity rests on bit-for-bit
  reproduction of the frozen per-model t₁ inputs as consumed by the v0.31→v0.33 arc
  (`counts_v19` / `counts_v23` outputs); correctness rests on extraction-function provenance
  alone — stated, not overclaimed.
- **v0.33-deposit check (this phase):** the consumed per-model recall and recognition vectors
  reproduce the v0.33 deposit (`osf/v33/data/v33_eta2.csv`) **bit-for-bit** (SHA-256, all five
  substrates, 112 units). Defined-unit CV-CPC reproduces the frozen `cpc_score` exactly. See
  `data/v35_reconciliation_log.txt`.

**v0.23 normalization footnote.** v0.23 recognition is scored as `r_level`; it is normalized
to binary (R0→0, else→1) for C_P, identically to the consuming phases.

## Tree

- `v35_verdicts.json` — per-hypothesis verdicts, statistics, per-substrate tables, sensitivity (LOSO, threshold reruns), RNG seed, draw counts
- `data/` — reconciliation log (`v35_reconciliation_log.txt`) and phantom roster (`v35_phantom_roster.csv`)
- `prereg/` — locked pre-registration artifacts (content module + mega-prompt)
- `figures/` — six chart PDFs (`chart_01_gate_flip` … `chart_06_roster_attrition`)
- `reports/` — brand-format report PDF
- `scripts/` — scoring code (`score_v35.py`) and methods log (`v35_scoring_methods_log.md`)
- `registries/` — the five reused t₁ locked registries (v0.19–v0.23), referenced not re-locked (see `registries/README.md`)

## Pipeline (re-analysis; no acquisition)

1. Pre-registration locked at git tag `v0.35-prereg-r1` (externally anchored before analysis)
2. Reconciliation gate — bit-for-bit vs the v0.33 deposit + v1.7 anchor (`data/v35_reconciliation_log.txt`)
3. Score: `python3 scripts/score_v35.py` → `v35_verdicts.json`
4. Build figures: `python3 reports/build_charts_v35.py`
5. Build report: `python3 reports/build_report_v35.py`
6. Build SSRN paper: `python3 scripts/build_paper_v0_35.py`
7. Submit per `papers/v0_35/ssrn_submission_packet_v0_35.md` (SSRN 6921758)
8. OSF deposit: `python3 ~/aias/scripts/osf_upload.py ~/aias/osf/v35 v35`
