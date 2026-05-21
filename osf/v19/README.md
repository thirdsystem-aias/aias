# AIAS™ Presence Measurement Protocol — v0.19 Audiophile Headphones

OSF deposit for the v0.19 phase of the AIAS™ Presence Measurement Protocol research program.

Methodology base: Protocol v1.4 (SSRN 6799479) — Recognition × Recall multi-component AI Availability construct. Predecessor phases: v0.16 (SSRN 6791999), v0.17 (SSRN 6802261), v0.18 (SSRN 6806558).

**SSRN abstract:** https://ssrn.com/abstract=6809182

## Phase state

| Stage | Git ref | Commit |
|---|---|---|
| Pre-registration locked | tag `v0.19-prereg-r1` | `2cbd36c` |
| Phase A + Phase B acquired, scored | tag `v0.19-acquired` | `c56ea8b` |
| Brand-format report rendered | (no tag) | `cbecd3c` |
| SSRN paper compiled | (no tag) | `08664e7` |
| SSRN submission | abstract ID 6809182 | published May 2026 |

All commits on branch `v0.18-il-gradient` (working trunk).

## Substrate

Audiophile headphones, English-language anchored. Two same-Identity-Load cells stratified by audiophile-segment product-line emergence year:

- **Cell A_Heritage (pre-2008):** Sennheiser, Beyerdynamic, Denon, Grado, Sony, Audio-Technica, Stax, Koss.
- **Cell B_Boutique (post-2008):** Audeze, HiFiMan, Focal, Meze, ZMF Headphones, Spirit Torino, Final Audio, Dan Clark Audio.

n = 16 worldwide; 8 per cell. Cross-cultural flags: Stax, HiFiMan. Borderline (product-line rule): Focal, Final Audio. Panel composition note: AKG → Denon substitution made before pre-reg lock to avoid Samsung COI (Harman International, AKG's parent, is a Samsung subsidiary); recorded in DEVIATIONS Entry 1 and §5 of the SSRN paper.

## Reference panel

Six LLMs (locked since v0.17, reused unchanged):

`claude-opus-4-5`, `claude-sonnet-4-5`, `gpt-4o`, `gpt-4o-mini`, `gemini-2.5-flash`, `gemini-2.5-flash-lite`.

## Acquisition

| Phase | Queries | Successes | Errors | Mentions |
|---|---|---|---|---|
| Phase A (Recognition) | 96 | 96 | 0 | n/a |
| Phase B (Recall, 6-frame battery) | 36 | 36 | 0 | 165 / 576 |

## Verdicts (post-acquisition)

| Hypothesis | Verdict | Notes |
|---|---|---|
| H_C3 | **UNDETERMINED** | DEVIATIONS Rule 4 routing. Cell A_Heritage C_P modal share = 0.500 (FAIL at strict-less-than boundary by single brand at ceiling); Cell B_Boutique modal share = 0.875 (FAIL, saturated). C3 SKIPPED; panel NOT substituted. |
| H_Recognition_Recall_Dissociation_Replication | **REPLICATED_PARTIAL** | 3 Iwachu-pattern cases, all Cell B_Boutique: ZMF Headphones (C_P 6/6, mentions 1/18), Spirit Torino (5/6, 0/18), Final Audio (6/6, 0/18). |
| H_CulturalFootprint_Dissociation_Sensitivity | **DESCRIPTIVE** | 3 Type 1 cases (Audeze, HiFiMan, Dan Clark Audio — all Cell B); 0 Type 2 cases (panel-composition limit, not absent pathway). |
| Cross-cultural robustness (Rule 6) | not applicable | No per-cell ρ computed (Rule 4 routing). |

**Cumulative anchor base for v1.4 multi-component construct:** 13 cases across 3 substrate families (1 from v0.17 Japanese kitchenware + 9 from v0.18 indie fragrance + 3 from v0.19 audiophile electronics).

## Files in this deposit

**Pre-registration and DEVIATIONS:**
- `PRE_REGISTRATION_v0_19.md` — hypothesis specs, decision rules, verdict matrices, panel composition rationale
- `DEVIATIONS.md` — running log; Rule 4 invocation (post-Phase-A) recorded post-scoring
- `panel_registry_v0_19.csv` — 16 brands with cell, founding year, audiophile product-line emergence year, flags, cascade order
- `thresholds_v0_19.json` — machine-readable decision rules; C1/C2/C3/Iwachu/channel-asymmetry thresholds

**Acquisition pipeline:**
- `acquire_v0_19.py` — query batch generation + Phase A/B response parsing (v1.4 brand-mention detection rules)
- `run_v0_19.py` — multi-provider acquisition driver (Anthropic/OpenAI/Google APIs via env vars)
- `phase_a_queries.jsonl` — 96 single-brand Recognition probes
- `phase_b_queries.jsonl` — 36 enumeration queries (3 load-bearing + 3 cultural-footprint frames × 6 models)

**Acquisition outputs:**
- `phase_a_results.csv` — 96 rows: brand × panel_model × recognition_yes
- `phase_b_results.csv` — 576 rows: brand × panel_model × frame × mentioned × rank
- `scoring_output_v0_19.txt` — full canonical scoring run output

**Scoring:**
- `score_v0_19.py` — C1/C2/C3 cascade, Spearman ρ + bootstrap CI, Iwachu detection, channel-asymmetry classification, cross-cultural robustness

**Brand-format report:**
- `reports/v19_audiophile.pdf` — 14-page brand-format report companion (rendered via `~/aias/reports/build_report_v19.py`; figures at `~/aias/reports/figs/v19/chart_0{1,2,3}_*.pdf`)

**SSRN paper:** maintained separately at `~/aias/papers/v0_19/v0_19_ssrn_paper.pdf`; not duplicated in the OSF deposit. SSRN abstract: https://ssrn.com/abstract=6809182.

## Citation

González Castro, P. U. (2026). *Recognition Ceiling, Dissociation Replication, and Cultural-Channel Asymmetry on an Audiophile Headphones Substrate: AIAS v0.19*. Third System™. SSRN Working Paper. https://ssrn.com/abstract=6809182

OSF DOI: assigned at deposit lock by Open Science Framework.

## Integrity

`MANIFEST.md` carries SHA-256 hashes for every file in this deposit, computed at the commit hash recorded in the manifest header. Regenerate with `python3 build_manifest_v0_19.py` to verify.

## License and contact

Data, code, and analysis: CC-BY-4.0. Underlying LLM API responses: subject to provider terms.

Correspondence: pablou@pablou.com · pablou.com · ORCID 0009-0003-8968-9990. Inquiries: hello@thirdsystem.ai.
