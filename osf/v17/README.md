# AIAS v0.17 — Premium Kitchenware

**Phase:** v0.17 Premium Kitchenware
**Substrate:** Premium cookware (16-brand panel, three tradition cells)
**Protocol:** AIAS Presence Measurement Protocol v1.4
**Status:** PUBLISHED — May 2026
**OSF project:** [ec6wh/v17](https://osf.io/ec6wh/) — this directory

---

## Publication

González Castro, P. U. (2026). *Panel Inadequacy and the Recognition × Recall Dissociation on the Premium Kitchenware Substrate: AIAS v0.17.* SSRN Working Paper 6802261. https://ssrn.com/abstract=6802261

**Companion methodology paper:**

González Castro, P. U. (2026). *The AIAS Presence Measurement Protocol v1.4: Recognition × Recall Decomposition and Multi-Component AI Availability.* SSRN Working Paper 6799479. https://ssrn.com/abstract=6799479

---

## Headline outcomes

Three principal outcomes from a single Phase B measurement against the locked six-LLM reference panel:

1. **H_Regime4_kitchenware FALSIFIED on panel inadequacy.** Worldwide eligible *n* = 10 below the pre-registered C1 floor of *n* ≥ 12, following Japanese cell full collapse (Phase A Vermicular descope + Phase B Iwachu / Sori Yanagi / Noda Horo exclusions) and partial American cell attrition (Phase B Field Company + Smithey exclusions). European cell intact at 6/6.

2. **H_IdentityLoad_moderator (joint v0.16 / v0.17) AMBIGUOUS.** The pre-registered joint verdict matrix at cell `PARTIAL × FALSIFIED` routes the Identity-Load moderator hypothesis to v0.18 indie fragrance (forthcoming) for resolution.

3. **Recognition × Recall dissociation — the Iwachu canonical case.** Phase A C_P PASS at 6/6 anchoring + Phase B EXCLUDED_E1a at 0/18 mention rate. The dissociation generalised across the Japanese cell and motivated the v1.4 Methodology paper revision specifying AI Availability as a multi-component construct comprising Recognition and Recall components.

---

## Audit chain

All thresholds, decision rules, and panel composition locked at git commit prior to any data acquisition. No post-acquisition rule modification or threshold adjustment.

| Stage | Git tag | Commit | Date |
|---|---|---|---|
| Pre-registration (r1) | `v0.17-prereg-r1` | `3ebe426` | 2026-05-19 |
| Phase A locked | `v0.17-phase-a-locked` | `8cdf0cd` | 2026-05-19 |
| Phase B locked | `v0.17-phase-b-locked` | `54c83ec` | 2026-05-20 |
| Verdict registered | (same as Phase B) | `54c83ec` | 2026-05-20 |

---

## Locked configuration

**Six-slot reference LLM panel** (Phase A + Phase B, identical):

- claude-opus-4-5
- claude-sonnet-4-5
- gpt-4o
- gpt-4o-mini
- gemini-2.5-flash
- gemini-2.5-flash-lite

**Phase A classifier configuration:** claude-opus-4-7, model-default sampling, max_tokens=200. Prompt template locked in `scripts/classify_phase_a_auto_v1_4.py` constant `CLASSIFIER_PROMPT_TEMPLATE`. Output schema: two-line response, `ANCHORED: <0 or 1>\nRATIONALE: <≤25-word sentence>`.

**Phase B category queries** (tradition-agnostic, three queries × six LLMs = 18 cells per brand):

- *q1_best_brands:* "What are the best premium cookware brands? Please list several with brief descriptions."
- *q2_serious_cooks:* "Recommend high-quality cookware brands for serious home cooks. Name several specific brands."
- *q3_pro_chefs:* "What cookware brands do professional chefs use? List several."

**Pre-registered C1 panel adequacy floor:** worldwide *n* ≥ 12 eligible brands at end of Phase B.

---

## Formal verdicts

Verdicts follow mechanically from the pre-registered decision rules in `registries/PRE_REGISTRATION_v0_17.md` §§2.1, 2.2, 2.3. See `v0_17_verdict.md` for the formal verdict document.

> **H_Regime4_kitchenware:** *FALSIFIED on panel inadequacy* (¬C1; worldwide *n* = 10 < 12). Per pre-reg decision rule `¬C1 ∨ ¬C2`.

> **H_IdentityLoad_moderator (joint v0.16 / v0.17):** *AMBIGUOUS* — kitchenware fails C1; Identity Load moderator hypothesis inconclusive pending v0.18 indie fragrance.

---

## Panel composition

Pre-registered worldwide *n* = 16 brands across three tradition cells:

| Cell | Pivot + alternates | Pre-Phase-A | Post-Phase-B | Δ |
|---|---|---|---|---|
| European | Le Creuset, Staub, Mauviel, Demeyere, Fissler, de Buyer | 6 | 6 | 0 |
| American | All-Clad, Lodge, Made In, Field Company, Smithey, Hestan | 6 | 4 | −2 |
| Japanese | Vermicular, Iwachu, Sori Yanagi, Noda Horo | 4 | 0 | −4 |
| **Worldwide** | | **16** | **10** | **−6** |

Attrition stages:

- **Phase A (Stage 1):** Vermicular C_P FAIL at 4/6 anchoring → descoped → Japanese cell cascaded to Iwachu (ordinal 2, 6/6 PASS).
- **Phase B (Stage 2):** Field Company + Smithey EXCLUDED_E1a (American); Iwachu + Sori Yanagi + Noda Horo EXCLUDED_E1a (Japanese full-cell collapse). Noda Horo's borderline classification resolved at Phase B as OUT_OF_SCOPE (enamelware-only).

---

## Methodological findings

Beyond the substantive verdict, v0.17 produced three methodologically significant findings that motivated the v1.4 Methodology paper revision (SSRN 6799479).

1. **Recognition × Recall dissociation — the Iwachu canonical case.** Phase A and Phase B measure dissociable constructs of AI Availability. AI Availability is multi-component (Recognition + Recall) rather than unidimensional. v1.4 §§2.1–2.5 formalize the construct revision; v0.17 is the empirical anchor.

2. **Substrate-substitution attrition.** LLM-substrate Phase B produced ~2× the attrition rate of Trends-substrate Phase B (5 brands vs 1–3 anticipated). Documented in v1.4 §5.2; forward action for v0.18 panel design (over-provision 30–50% per cell).

3. **Cross-cultural confound on cross-cultural substrates.** Japanese cell's full collapse is non-trivially confounded with Western-language LLM training-data bias. v0.17 cannot disambiguate this from the substantive Identity-Load null. v0.18 indie fragrance (entirely English-language) is the immediate forward action.

---

## File manifest

```
osf/v17/
├── README.md                           This file
├── PRE_REGISTRATION_v0_17.md           Pre-reg document (locked at 3ebe426)
├── DEVIATIONS.md                       Eight DEVIATIONS entries
├── phase_a_lock.md                     Phase A lock document
├── phase_b_lock.md                     Phase B lock document
├── v0_17_verdict.md                    Formal verdict document
├── classification_ledger.csv           Phase A C_P ledger (24 rows)
├── registries/
│   ├── brands_kitchenware_v0.17.json   16-brand panel
│   └── topic_id_resolution_log_v0.17.csv   15-row Phase B resolution log
├── data/
│   └── phaseB_queries/
│       ├── q1_best_brands/             18 cached LLM responses
│       ├── q2_serious_cooks/           18 cached LLM responses
│       └── q3_pro_chefs/               18 cached LLM responses
├── figures/                            (Mirror of papers/v0_17/figures/)
│   ├── chart_v17_phase_b_mention_rates.pdf
│   ├── chart_v17_cell_collapse.pdf
│   └── chart_v17_dissociation.pdf
├── papers/                             (Mirror of papers/v0_17/)
│   ├── v0_17_ssrn_paper_draft.md
│   └── v0_17_ssrn_paper.pdf            Submitted as SSRN 6802261
├── reports/
│   └── v17_kitchenware.pdf             Brand-format report
└── scripts/                            (Mirror of acquisition + analysis scripts)
    ├── acquire_phase_a_v1_3.py
    ├── classify_phase_a_auto_v1_4.py
    ├── classify_phase_a_v17.py
    └── phaseB_resolve_v17.py
```

---

## DEVIATIONS summary

Eight entries documented contemporaneously in `DEVIATIONS.md`. No deviation involved post-acquisition modification of a pre-registered decision rule, threshold, or routing rule.

| # | Topic | Commit chain | Pre-reg impact |
|---|---|---|---|
| 1 | Pre-reg revision r0 → r1 (Trends → C_P framing correction) | `→ 3ebe426` | Pre-reg structure |
| 2 | Google SDK migration | `→ 12e66db` | None |
| 3 | gemini-2.0-flash → gemini-2.5-flash-lite (provider sunsetting) | `→ b5efea3` | None — substitution before pivot validation |
| 4 | Operator judgment → automated LLM classifier (provisional v1.4 §6.4.2) | `2097c9f → a6974e6` | None |
| 5 | Claude-opus-4-7 temperature parameter deprecated; dropped from API call | `9042dea → 8fc966c` | None |
| 6 | Vermicular C_P FAIL → Iwachu cascade activation | `d09182c → 1304237` | Pre-registered cascade path; ledger extension |
| 7 | Substrate substitution Trends → LLM for Phase B (provisional v1.4 §5.2) | `55e28ed → 9174d10` | Provisional v1.4 spec adoption; documented limitation |
| 8 | Phase B outcome event record (Japanese collapse, C1 breach) | `1b560d2 → cf0c370` | None — outcome documentation |

Each deviation has a stable commit hash chain (substantive change → backfill of hash placeholder), making the entire audit trail bit-reproducible from the git repo.

---

## Reproducibility

To reproduce the v0.17 verdicts from source:

```bash
git clone https://github.com/thirdsystem-aias/aias.git
cd aias
git checkout v0.17-phase-b-locked

# Phase A pivot validation (~20 LLM calls)
python3 scripts/acquire_phase_a_v1_3.py
python3 scripts/classify_phase_a_auto_v1_4.py

# Phase B LLM-substrate measurement (~108 LLM calls = 18 cells × 6 LLMs)
python3 scripts/phaseB_resolve_v17.py

# Charts (3 PDFs)
python3 scripts/build_charts_v17.py

# SSRN paper PDF
python3 scripts/build_paper_v0_17.py

# Brand-format report PDF
python3 reports/build_report_v17.py
```

API keys needed: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GOOGLE_API_KEY`. Phase B response caches are deposited here under `data/phaseB_queries/`, so re-running phaseB_resolve is idempotent against the cache.

---

## Programmatic cross-references

v0.17 fits in the AIAS Presence Measurement Protocol research line as follows:

- **Immediately prior phase:** v0.16 Kitchen Knives (SSRN 6791999) — first leg of joint Identity-Load moderator test
- **Immediately next phase:** v0.18 indie fragrance (forthcoming) — deciding test of joint Identity-Load moderator
- **Canonical methodology:** v1.4 (SSRN 6799479), superseding v1.3 (SSRN 6797679) and v1.2 (SSRN 6761698)
- **Programmatic anchor:** AI Availability foundational paper (SSRN 6659000)

Full v0.6 → v0.16 phase chronology and SSRN ID registry available in the parent OSF project README.

---

## Contact

**Author:** Pablo Ulpiano González Castro
**Correspondence:** pablou@pablou.com · [pablou.com](https://pablou.com)
**ORCID:** [0009-0003-8968-9990](https://orcid.org/0009-0003-8968-9990)
**Primary academic affiliation:** School of Visual Arts, MPS Branding Program, New York, NY
**Research entity:** [Third System™](https://thirdsystem.ai) (data archive and methodology venue)

---

*Deposited: May 2026. Last updated: May 2026 (post v0.17 SSRN publication; v1.4 methodology cross-citation locked).*
