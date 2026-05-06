# AIAS Phase 2 — Pre-registration: Household Goods Retail (Pattern 6 / Phantom-Brand Persistence)

**Pre-registration lock date:** 2026-05-04
**Registry version:** household_v1.0
**Prompt set version:** household_v1.0
**Methodology version:** 0.3

## Hypotheses

**H1 (PRIMARY — phantom persistence).** Bed Bath & Beyond aggregate Presence across all 6 models ≥ 25%, with the headline scoring on the 5-prompt phantom-conditional set (excluding p5_discovery).
- Confirmation: BBB Presence ≥ 25%
- Partial: 15% ≤ Presence < 25%
- Disconfirmation: Presence < 15%

**H2 (cross-model spread).** Range across 6 models in BBB Presence ≥ 25 percentage points.
- Confirmation: spread ≥ 25 pts
- Partial: 10 ≤ spread < 25
- Disconfirmation: spread < 10 pts

**H3 (within-lab freshness, Anthropic).** Sonnet 4.6 BBB Presence > Opus 4.7 BBB Presence by ≥ 15 pts.
- Confirmation: Sonnet > Opus by ≥ 15 pts
- Partial: Sonnet > Opus by 5–15 pts
- Disconfirmation: Opus ≥ Sonnet OR difference < 5 pts

**H4 (within-lab freshness, OpenAI).** No directional pre-registration. Reported as descriptive finding. Confounded test (size + freshness).

**H5 (xAI as oldest-cutoff comparator).** Grok-4-1-fast BBB Presence ≥ Sonnet 4.6 BBB Presence.
- Confirmation: Grok ≥ Sonnet
- Disconfirmation: Grok < Sonnet by ≥ 10 pts

**H6 (CEP distribution).** BBB Presence highest in p2_contextual and p6_comparison; lowest in p5_discovery.

**H7 (Pier 1 comparator).** Pier 1 Presence < BBB Presence AND Pier 1 < 15%.

**H8 (rebrand recognition).** "Beyond, Inc." mentions < 25% of total BBB+Beyond mentions.

## Locked statement

We predict Bed Bath & Beyond achieves aggregate AI Presence ≥ 25% across 288 measurements (8 runs × 6 prompts × 6 models), despite having ceased to operate as a physical retailer ~37 months pre-measurement. The 6-model lineup spans 4 labs (Anthropic Sonnet 4.6 + Opus 4.7, OpenAI gpt-5.4-mini + gpt-5.5, Google Gemini 2.5 Flash, xAI Grok 4.1 Fast) and includes two within-lab generational comparisons (Sonnet/Opus, mini/flagship). We predict cross-model spread ≥ 25 percentage points in BBB Presence, with Grok-4-1-fast (Nov 2024 cutoff) ≥ Sonnet 4.6 as the lab-cutoff prediction. We predict Sonnet 4.6 BBB Presence exceeds Opus 4.7 BBB Presence by ≥ 15 points, isolating training-data freshness within the Anthropic lab. We make no directional pre-registration on within-OpenAI freshness because the gpt-5.4-mini → gpt-5.5 comparison confounds size with freshness. We predict Pier 1 Presence < BBB Presence AND Pier 1 < 15%, isolating pre-collapse footprint size. We predict "Beyond, Inc." mentions < 25% of total BBB+Beyond mentions.

## Lock conditions

- brands.json (registry_version=household_v1.0, 21 brands including BBB and Pier 1) committed before any measurement
- prompts.json (prompt_set_version=household_v1.0, 6 CEP-anchored prompts) committed before any measurement
- Registry revision per Protocol §2.4 permitted only after first run with unknown-mentions list as trigger
- BBB / Pier 1 / DTC-challenger composition held constant across any registry revision
- Disaggregated post-measurement analysis (BBB-strict vs. BBB+Beyond combined) part of analysis plan
- Manual sentiment/valence coding for all BBB mentions per Risk #7 part of analysis plan