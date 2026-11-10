# Number provenance — combined v0.27 + v0.28 paper (program study 67)

Every number in `v0_27_28_combined_validity_paper.md`, with its source file and key, for verification. Paths are relative to the repository root of branch `v0.27-28-combined` unless marked OSF. Abbreviations: V27 = `osf/v27/v0.27_verdicts.json`, V28 = `osf/v28/v28_verdicts.json`, V25 = OSF `v25/v25_verdicts.json` (sha256 e9a34e6c…16bf, byte-identical to `git show cc36d7a:osf/v25/v25_verdicts.json`), P27 = `prereg/v0_27_b2b_saas_convergent_validity_content.py` (= tag v0.27-prereg-r5), P28 = `prereg/v0_28_tech_brand_discriminant_content.py` (= tag v0.28-prereg-r2), D27 = `papers/v0_27/v0_27_convergent_validity_DRAFT.md` (locked v0.27 paper). Rounding only; no value was computed for the paper.

## Study 1 (v0.27)

| Paper value | Where in paper | Source and key |
|---|---|---|
| ρ = 0.294 (abstract 0.29); n = 24; adjusted p = 0.164; 95% CI [−0.171, 0.638] (abstract [−0.17, 0.64]); FALSIFIED | Abstract, §3.6, Table 4 | V27 `verdicts.H_CV3_Primary.block.{rho 0.29367, n, ci}`, `.p_adj 0.16367`, `.status` |
| Thresholds 0.60 with p < 0.05 (CONFIRMED), 0.74 (STRONG), < 0.30 or n.s. (FALSIFIED) | §3.5 | V27 `H_CV3_Primary.locked_threshold`, `.implemented`; P27 `HYPOTHESES.H_CV3_Primary.thresholds/falsification` |
| 10,000 resamples; min n 12 | §3.5 | V27 `_meta.n_boot`, `_meta.min_n`; P27 `SCORING` |
| Seed 20270527; percentile bootstrap | §3.5 | `scripts/score_v27.py` lines 47 and 73 |
| Type-2 sensitivity ρ = 0.359, n = 20, change +0.065; four brands Linear, Airtable, Miro, Cloudflare | Abstract (0.36 not quoted), §3.5, §3.6, Table 4 | V27 `_sensitivity_type2_construct_gap.H_CV3_Primary.{rho 0.35900, n, delta_vs_primary}`, `.excluded_brand_ids [B3,B4,B6,C5]` |
| Stride sensitivity ρ = 0.223, n = 23, change −0.071 | §3.6, Table 4 | V27 `_sensitivity_stride_confound.H_CV3_Primary.{rho 0.22265, n, delta_vs_primary}` |
| C_P = 6 of 6, mean 6.0, SD 0; CONFIRMED | Abstract, §3.2, §3.6, Table 4 | V27 `H_CV3_Recognition_Null.{C_P_mean, C_P_sd, status}` |
| Exploratory matrix (15 values: 0.294, 0.133, 0.798, 0.748, 0.297; 0.326, 0.383, 0.842, 0.792, 0.354; 0.250, 0.536, −0.317, −0.252, 0.264); abstract 0.80, 0.75; EXPLORATORY | Abstract, §3.6, Table 3 | V27 `H_CV3_Component.matrix.{recall_channel_som, aias_composite, identity_load}.{I1_sov, I1_sentiment, I1_presence_quality, I1_brand_recognition, I1_market_competition}`, `.status` |
| Grader overall score ρ = 0.44 | §3.6 (Figure 3 reference) | Locked figure `papers/v0_27/figs/v0_27_component_rho.pdf` ("Composite (/100) +0.44"); D27 Table 3 (+0.443). Not in V27. |
| Share of Voice SD 8.7%, presence quality 5.6%, brand recognition 4.8% of scale, over 19 live brands | §3.6 corrected account | D27 §4 (states "across the 24 brands"); verified Nov 10 as sample SD of the 19 non-Cell-D brands ÷ scale maximum in `osf/v27/data/v0.27_I1_normalized.csv` (8.69, 5.56, 4.83). Over all 24 brands the same ordering holds (not used in the paper). |
| 7 of 19 live brands at 7.33/10 | §3.6 | D27 §4; `osf/v27/data/v0.27_I1_normalized.csv` (I1_sov) |
| SoV 0.33 (Wunderlist, HipChat), 2.00 (Yammer) | §3.6 | `osf/v27/data/v0.27_I1_normalized.csv` I1_sov rows D3, D4, D2 |
| Table 2: R_cat, R_cult, recall-SOM (1 dp), SoV, ranks, rank gaps | Table 2 | `osf/v27/data/v0.27_aias_side.csv` (R_cat, R_cult, recall_channel_som); `osf/v27/data/v0.27_I1_normalized.csv` (I1_sov); rank columns reproduce D27 Table 2 (competition ranks) |
| recall-SOM = (R_cat / 36) × 100; six prompts × six models | §2.2, §3.2, Table 1 | P27 `SCORING.som_definition`, Entry 3 |
| Cells A 7, B 6, C 6, D 5 brands | §3.2 | `osf/v27/registries/v27_registry.json`; D27 §2.1 |
| Grader maxima 40, 20, 20, 10, 10; overall 100; three engines | §3.3, Table 1 | D27 §2.3; column set of `v0.27_I1_normalized.csv` |
| Model panel Claude Opus 4.7, Claude Sonnet 4.6, GPT-4o, GPT-4o mini, Gemini 2.5 Flash, Flash-Lite | Table 1 | P27 `PANEL` (Entry 2); `model_id` column of OSF/`cc36d7a:osf/v24/data/v24_phase_b.csv` |
| Revisions r1–r5; Entries 0–5; r3 alignment rule; r4 deferral | §3.1, §3.3, §3.4 | git tags v0.27-prereg-r1…r5; P27 `DEVIATIONS`; rule text present from r3 (`git show v0.27-prereg-r3:prereg/…`) |

## Study 2 (v0.28)

| Paper value | Where in paper | Source and key |
|---|---|---|
| ρ = 0.379 (abstract 0.38); p = 0.068; Pearson r = 0.461, p = 0.024; BCa [−0.076, 0.714]; absolute 0 to 0.713; CONFIRMED, not provisional | Abstract, §4.5, Table 6 | V28 `verdicts.H_Disc_Recognition.{spearman_rho 0.3794, spearman_p 0.06751, pearson_r 0.4605, pearson_p 0.02353, bca_ci_95, flags.ci_abs_interval, flags.ci_excludes_reducibility, flags.provisional, status}` |
| ρ = 0.593 (abstract 0.59); p = 0.002; Pearson r = 0.569, p = 0.004; BCa [0.179, 0.832] (abstract [0.18, 0.83]); point PARTIAL; UNDETERMINED | Abstract, §4.5, Table 6 | V28 `H_Disc_Familiarity.{spearman_rho, spearman_p 0.00226, pearson_r 0.5691, pearson_p 0.00371, bca_ci_95, point_verdict, status}` |
| Bands 0.50 / 0.74; benchmark 0.74; 10,000 resamples; seed 280400; min n 12 | §4.4, Table 1 | V28 `_meta.{convergent_benchmark, n_boot, seed, min_n}`; P28 `BANDS_ABS_RHO`, `SCORING` |
| Prediction 0.30–0.60, PARTIAL modal | §4.4 | P28 `PREDICTIONS` |
| Dissociation: 11 of 24; FULL; ±1.0; ≥ 4 cases; amplified +1.228, +1.150, +1.066, +1.065; suppressed −1.043, −1.050, −1.253, −1.052, −1.711, −1.031, −1.559 | §4.4, §4.5, Table 6 | V28 `H_Dissociation.{n_cases, status, amplified, suppressed}`; P28 `HYPOTHESES.H_Dissociation` |
| Frame 80 → 70 → 69; tertiles of 23; 8 per tertile; familiarity range 1.00–6.83 | §4.2, Table 1 | P28 `PANEL_CONSTRUCTION`, `VERIFICATION.binary_certified`, `DEVIATIONS[0].frame_counts` |
| 24 joined | §4.5 | V28 `_meta.presence_n_joined` |
| Presence 0.0 (QVC), 100.0 (Apple), 94.4 (Microsoft), 85.2 (Google); C_P 0–6 | §4.5 | `osf/v28/data/v0.28_presence.csv` |
| Table 5 familiarity, d′ (2 dp) | Table 5 | `prereg/v0_28_brand_validator.csv` (frozen at v0.28-prereg-r1) |
| Table 5 C_P, R_cat, R_cult, Presence (1 dp) | Table 5, §4.5 | `osf/v28/data/v0.28_presence.csv` |
| Presence = (C_P/6 + R_cat/18 + R_cult/18)/3 × 100; 18 per channel; 36 on v0.25 | §2.2, §4.1, §4.3, Table 1 | P28 `DEVIATIONS[2]` (Entry 2, r2); `scripts/bridge_v28.py` |
| 144 probes, 36 queries; probe wording; June 1, 2026 | §4.3 | `osf/v28/data/v0.28_run_metadata.json` (`acquired_utc` 2026-06-01, `phase_a_probe`, `phase_b_frames`); P28 `PRESENCE_PROTOCOL` |
| Model panel claude-opus-4-5 … gemini-2.5-flash-lite | Table 1 | `v0.28_run_metadata.json reference_panel`; P28 `REFERENCE_PANEL` |

## Program records outside the two studies

| Paper value | Where in paper | Source and key |
|---|---|---|
| v0.25 composite ρ = 0.74 / 0.7411; recall-only ρ = 0.67; 24 brands | Introduction, §2.2, §6 | V25 `hypotheses[H_CV_Primary].statistics.rho`, `hypotheses[H_CV_Recall].statistics.rho`, `n_brands` |
| v0.25 six cues per channel vs three in v0.28 | §6 | P28 `DEVIATIONS[2].finding / anchor_commensurability_caveat` |
| BRAND norms collected 2020 and 2024, US residents; IRB approvals Bocconi and City University of London | §6, Ethics | Raffaelli et al. (2025), abstract and Declarations (`git show cc36d7a:external/brand_db/brand_paper.txt`) |
| CC BY 4.0 for ResearchBox 1892 content | Data availability | https://researchbox.org/1892 (read Nov 10, 2026: "All content posted to ResearchBox is under a CC By 4.0 License") |
| SSRN IDs 6659000, 6761698, 6797679, 6799479, 6810758, 6816340, 6838802, 6847678, 6870778; MSI Report No. 26-132 | References | CLAUDE.md (master copy) Phase SSRN ID registry, methodology chain, current state. Declined IDs (6842138, 6854758, 6865478) cited by title with OSF copy, per CLAUDE.md. |
| Reference titles for v0.24, v0.25, v0.26, v0.29, v0.27, v0.28 | References | v0.24: OSF/`cc36d7a:osf/v24/papers/v0_24_b2b_saas.pdf` p.1; v0.25: OSF `v25/reports/v0_25_b2b_saas_construct_validity.pdf` p.1; v0.26: `papers/v0_26/ssrn_submission_packet_v0_26.md`; v0.29: `papers/v0_29/v0_29_ssrn_paper_draft.md` YAML; v0.27/v0.28: their paper YAML |
