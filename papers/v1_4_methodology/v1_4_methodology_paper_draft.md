---
title: |
  The AIAS Presence Measurement Protocol v1.4:\
  Recognition $\times$ Recall Decomposition and\
  Multi-Component AI Availability
author: |
  Pablo Ulpiano González Castro\
  School of Visual Arts, MPS Branding Program, New York, NY\
  (primary academic affiliation)\
  Third System™ (research entity; data archive and methodology venue)\
  Correspondence: pablou@pablou.com $\cdot$ pablou.com\
  ORCID: 0009-0003-8968-9990
date: May 2026
keywords: AI Availability; AIAS; LLM-mediated retrieval; brand measurement; recognition memory; recall memory; pre-registration; methodological protocol
abstract: |
  This paper introduces v1.4 of the AIAS™ Presence Measurement Protocol, a major revision that supersedes Methodology v1.2 (SSRN 6761698) and v1.3 (SSRN 6797679). The revision is anchored in an empirical finding from v0.17 Premium Kitchenware: Phase A and Phase B of the protocol measure dissociable constructs. AI Availability—the third-system variable the AIAS framework is designed to estimate—has at least two component dimensions: Recognition (does the LLM identify the brand as belonging to the substrate?) and Recall (does the LLM spontaneously surface the brand when asked about the substrate?). These components are robustly dissociable across the six-slot LLM reference panel and across category substrates. v1.4 formalizes this decomposition as the protocol's foundational measurement structure, re-states the Phase A and Phase B specifications under canonical Recognition and Recall labels, defines a composite AI Availability formula across the two components, and specifies the implications for the AIAS six-component composite. The paper also formalizes the automated C_P classifier and the LLM-substrate Phase B—both provisional in v0.17 DEVIATIONS Entries 4–7—as canonical. A documented cross-cultural confound from v0.17 motivates a methodological caveat and a same-language Identity Load test recommendation for v0.18 onward. v1.4 supersedes prior versions as the canonical AIAS Presence Measurement Protocol reference.
---

# 1. Introduction

## 1.1 Historical Context

The AIAS™ Presence Measurement Protocol originated as a programmatic effort to operationalize a third system of brand availability—AI Availability—alongside the well-established two-system architecture of Mental Availability and Physical Availability inherited from the Ehrenberg-Bass tradition (Sharp 2010; Romaniuk 2018; Sharp and Romaniuk 2021). The theoretical foundation locating AI Availability as a measurable, manageable brand-level variable was established in González Castro (2026a, SSRN 6659000).

The Methodology paper v1.2 (González Castro 2026b, SSRN 6761698) formalized the four-regime taxonomy as the canonical category-classification step, established the worldwide and United States sub-panel reporting structure, and specified the Phase D scoring rule (Spearman $\rho$ with age and tradition controls, evaluated across two measurement windows). Methodology v1.3 (González Castro 2026c, SSRN 6797679) added the Phase A pivot-validation step—a five-stage substrate-anchoring rule using a six-slot LLM reference panel—as a pre-acquisition gate, and specified the Phase A C_P (Cell-Pivot) classification as an operator-judgement step.

By the close of v1.3, the protocol's measurement architecture comprised three sequential phases: Phase A (pivot validation against the substrate-anchoring rule), Phase B (topic-ID resolution for downstream measurement), and Phase D (the canonical scoring rule). The Phase B specification in v1.3 was inherited from the earlier Trends-substrate research line (v0.13–v0.15), where the substrate of measurement was Google Trends signal over an out-of-sample window. This inheritance was operationally workable for the Trends-era programmes but produced an unresolved methodological inconsistency once v0.16 (González Castro 2026d, SSRN 6791999) pivoted to LLM-mediated retrieval as the canonical measurement substrate.

## 1.2 Motivation for v1.4 Revision

v1.4 is motivated by three observations from the v0.17 Premium Kitchenware program (González Castro 2026e, forthcoming), each with implications for the protocol's foundational measurement structure.

**Observation 1: Substrate Coherence.** v0.17 Phase A operated on the LLM-mediated retrieval substrate per the v1.3 §6.4.2 specification. Continuing v1.3's Trends-substrate Phase B in v0.17 would have produced a methodologically incoherent pipeline—a substrate mismatch between adjacent measurement stages, each gating brands by different constructs (Trends search interest at Phase B; LLM identity anchoring at Phase A). The substrate substitution was implemented as a provisional protocol revision and documented in v0.17 DEVIATIONS Entry 7.

**Observation 2: Phase A and Phase B Dissociation.** The provisional LLM-substrate Phase B specification produced a striking empirical pattern in v0.17. Iwachu—a Japanese cast iron cookware brand with approximately 400 years of nambu-tekki heritage—achieved Phase A C_P PASS at 6/6 anchoring against the six-slot LLM reference panel: every reference model identified Iwachu as a Japanese cast iron cookware manufacturer when asked "Who or what is Iwachu?". The same six reference models, queried about premium cookware brands in three unprompted category queries, mentioned Iwachu zero times across all eighteen response cells. This is not classifier disagreement, prompt artifact, or measurement noise. It is a structurally robust dissociation between two measurement surfaces, each holding across all six LLMs and (for Phase B) across all three category queries. Recognition anchoring (Phase A) and recall presence (Phase B) are dissociable cognitive-architectural properties of LLM-mediated brand retrieval.

**Observation 3: Cross-Cultural Confound.** All three Japanese-tradition brands in the v0.17 panel that survived Phase A (Iwachu, Sori Yanagi, Noda Horo) received zero mentions across the eighteen Phase B response cells. The Japanese-cell full collapse pattern is hard to disambiguate from Western-language LLM training-data bias on a cross-cultural substrate. The cell collapse breached the pre-registered C1 worldwide-n adequacy criterion ($n \geq 12$; observed $n = 10$) and produced a FALSIFIED-on-panel-inadequacy verdict for the substantive hypothesis $H_{\text{Regime4\_kitchenware}}$. The cross-cultural reading of this collapse motivates a methodological caveat for cross-substrate AIAS measurement and a same-language Identity Load test as the immediate forward direction.

## 1.3 Contribution

v1.4 formalizes three protocol revisions, all anchored in the v0.17 empirical findings, plus two procedural revisions inherited from earlier v0.17 DEVIATIONS entries.

The three protocol revisions are: (1) **Recognition $\times$ Recall decomposition** as the foundational measurement structure of AI Availability, with Phase A and Phase B re-stated under canonical Recognition and Recall labels (§§2, 5, 7); (2) **LLM-substrate Phase B** as canonical, replacing the v1.3-inherited Trends-substrate Phase B for the v0.16-onward research line (§4); (3) **Composite AI Availability formula** that aggregates over Recognition and Recall components with documented dissociation behavior (§7).

The two procedural revisions are: (4) **Automated C_P classifier** at Phase A, formalizing the v0.17 DEVIATIONS Entries 4–5 substitution of operator-judgement with a locked LLM classifier (§3.2); (5) **Cascade pipeline** with ledger-extension semantics, formalizing the v0.17 DEVIATIONS Entry 6 infrastructure (§3.3).

v1.4 supersedes v1.2 (SSRN 6761698) and v1.3 (SSRN 6797679) as the canonical AIAS Presence Measurement Protocol reference. Prior versions remain valid historical references for the v0.13–v0.15 Trends-substrate research line; v0.16-onward research operates under v1.4.

# 2. AI Availability as Multi-Component Construct

## 2.1 The Dissociation Problem

The foundational AI Availability paper (González Castro 2026a) defined AI Availability as the probability that a brand surfaces in an LLM-mediated retrieval event within a relevant category context. This definition is theoretically clean but operationally underspecified: "surfaces" can mean at least two distinct cognitive-architectural properties of an LLM's response behavior.

Consider a brand $b$ in category substrate $S$. Two operationally distinct retrieval events are possible:

**Event R1 (Recognition):** The user names the brand explicitly. The query is something like "Who or what is $b$?" or "Tell me about $b$." The LLM responds with an identification statement that either does or does not place $b$ within $S$. The measurement question is whether the LLM has anchored $b$ to $S$ as the primary referent.

**Event R2 (Recall):** The user does not name the brand. The query is something like "What are the best brands in $S$?" or "Recommend a high-quality brand in $S$." The LLM responds with a brand list (typically) that either does or does not include $b$. The measurement question is whether the LLM spontaneously surfaces $b$ given $S$ alone.

R1 and R2 are not interchangeable. R1 is recognition-mediated retrieval; R2 is recall-mediated retrieval. The distinction parallels the well-established recognition / recall distinction in human memory research (Mandler 1980; Yonelinas 2002) but transposed onto the LLM substrate, where the cognitive architecture is materially different but the functional dissociation is empirically demonstrable.

## 2.2 The v0.17 Empirical Demonstration

The Iwachu case from v0.17 Premium Kitchenware is the cleanest empirical demonstration in the AIAS programme that R1 and R2 are dissociable.

Iwachu is a Japanese cast iron cookware manufacturer with a documented heritage of approximately 400 years in the nambu-tekki tradition of Iwate Prefecture. In v0.17 Phase A (the R1 measurement surface), the brand was queried against the six-slot LLM reference panel with the disambiguation query "Who or what is Iwachu?". All six reference models—claude-opus-4-5, claude-sonnet-4-5, gpt-4o, gpt-4o-mini, gemini-2.5-flash, gemini-2.5-flash-lite—led their responses with statements identifying Iwachu as a Japanese cast iron cookware manufacturer. The Phase A C_P anchoring score was 6/6, well above the pre-registered 5/6 supermajority threshold for substrate anchoring.

In v0.17 Phase B (the R2 measurement surface), the same six reference models were queried with three unprompted category queries: "What are the best premium cookware brands? Please list several with brief descriptions"; "Recommend high-quality cookware brands for serious home cooks. Name several specific brands"; "What cookware brands do professional chefs use? List several." The eighteen response cells (3 queries $\times$ 6 LLMs) produced a Phase B Iwachu mention count of 0/18. Not a single LLM, in any of the three query framings, spontaneously surfaced Iwachu when asked about premium cookware brands.

The pattern is structurally robust. Phase A R1 anchoring is positive across all six LLMs. Phase B R2 mention rate is zero across all six LLMs and all three queries. The dissociation is not a single-model artifact, a single-query artifact, or a thresholding noise event. It is a cognitive-architectural property of the brand's representation in the LLM panel: Iwachu has stable identity (the panel knows what it is) but no recall presence (the panel does not produce it when asked about its category).

Two further v0.17 cases reinforce the pattern. Sori Yanagi (Japanese designer-craft stainless cookware) achieved Phase A pivot-eligible status but was not measured at Phase A in v0.17 because Iwachu was the activated Japanese-cell pivot; Sori Yanagi nevertheless received 0/18 mentions at Phase B. Noda Horo (Japanese enamelware borderline brand) similarly received 0/18 mentions. The full Japanese cell collapse at Phase B, against a panel where Iwachu had robust Phase A identity, demonstrates that the dissociation generalizes beyond the canonical Iwachu case and operates at the cell level on cross-cultural substrates.

## 2.3 Recognition Component: Formal Definition

Recognition is the protocol's measurement of whether an LLM, given the brand name as input, anchors the brand to the substrate as the primary identification referent.

Let $b$ be a brand and $S$ a substrate. Let $\mathcal{L} = \{L_1, L_2, \ldots, L_K\}$ be the reference panel (in current protocol practice, $K = 6$). For each $L_k \in \mathcal{L}$, let $r_k(b)$ be the response of $L_k$ to the disambiguation query "Who or what is $b$?". Let $\tau(b, k)$ be the first 100 whitespace-tokenized words of $r_k(b)$. Define the Recognition indicator:

$$\rho_R(b, k) = \begin{cases} 1 & \text{if the primary referent in } \tau(b, k) \text{ places } b \text{ within } S \\ 0 & \text{otherwise} \end{cases}$$

The Recognition score for brand $b$ is the supermajority indicator across the panel:

$$R(b) = \mathbb{1}\left[ \sum_{k=1}^{K} \rho_R(b, k) \geq \theta_R \cdot K \right]$$

where $\theta_R = 5/6$ is the supermajority threshold from v1.3 §6.4.2 (preserved unchanged in v1.4). $R(b) = 1$ corresponds to the Phase A C_P PASS verdict; $R(b) = 0$ corresponds to C_P FAIL.

The Recognition score is computed at Phase A. Operationally, the indicator $\rho_R(b, k)$ is determined by the automated classifier specified in §3.2 (replacing v1.3's operator-judgement procedure).

## 2.4 Recall Component: Formal Definition

Recall is the protocol's measurement of whether an LLM, given the substrate but not the brand, spontaneously surfaces the brand in a category-relevant retrieval event.

Let $\mathcal{Q} = \{Q_1, Q_2, \ldots, Q_M\}$ be a set of unprompted category queries about $S$ (in current protocol practice, $M = 3$). For each $(Q_m, L_k)$, let $r_{m,k}$ be the response of $L_k$ to $Q_m$. Define the Recall indicator:

$$\rho_C(b, m, k) = \begin{cases} 1 & \text{if } b \text{ (or a mechanical alias) appears in } r_{m,k} \\ 0 & \text{otherwise} \end{cases}$$

The Recall rate for brand $b$ is the mean mention rate across all $(m, k)$ cells:

$$C(b) = \frac{1}{M \cdot K} \sum_{m=1}^{M} \sum_{k=1}^{K} \rho_C(b, m, k)$$

In current protocol practice, $M \cdot K = 18$. Tier assignments based on $C(b)$ are: PASS if $C(b) \geq 1/K$; PASS_E5 if $0 < C(b) < 1/K$; EXCLUDED_E1a if $C(b) = 0$. The threshold $1/K$ corresponds to "approximately one mention per LLM on average across queries," chosen to ensure measurability for the downstream Phase D scoring rule without imposing a strict prominence filter.

The Recall rate is computed at Phase B. Operationally, the indicator $\rho_C(b, m, k)$ is determined by mechanical alias matching (case-insensitive word-boundary regex) against an alias set generated from the brand's canonical name; see §4.3.

## 2.5 Composite AI Availability

Composite AI Availability for brand $b$ in substrate $S$ aggregates over Recognition and Recall:

$$A(b) = w_R \cdot R(b) + w_C \cdot C(b)$$

where $w_R, w_C \geq 0$ and $w_R + w_C = 1$. The weighting parameters $w_R$ and $w_C$ encode the measurement objective: recognition-dominated weighting (high $w_R$) is appropriate when the substantive question is brand identification accuracy; recall-dominated weighting (high $w_C$) is appropriate when the substantive question is unprompted retrieval competition.

Two reference weightings are recommended for v1.4 reporting:

**Balanced ($w_R = 0.5$, $w_C = 0.5$).** Equal weighting of recognition and recall. Appropriate for general-purpose AIAS reporting and for the AIAS six-component composite (§2.6) when no prior specifies a measurement-objective bias.

**Recall-leaning ($w_R = 0.3$, $w_C = 0.7$).** Higher weighting on recall. Appropriate when the AIAS Presence component is intended to estimate brand-mediated purchase consideration—the construct closest to the Tri-System architecture's substantive theoretical motivation, where AI Availability is operationally defined as "the probability that an AI intermediary recommends or selects the brand in a category-relevant decision context." Recall presence is the cleaner proxy for this construct than Recognition anchoring.

Both reference weightings are reported in v1.4-compliant AIAS measurement deliverables. The Recall-leaning weighting is treated as the primary AIAS Presence score; the Balanced weighting is reported as a sensitivity.

## 2.6 Relation to the AIAS Six-Component Composite

The full AIAS™ composite is defined across six components: Presence, Ranking, Consistency, Coverage, Grounding, and Sentiment. Prior protocol versions (v1.2, v1.3) implicitly treated Presence as a unidimensional construct measured by a single score. v1.4's decomposition revises this: Presence is itself composite, aggregating Recognition and Recall per the §2.5 formula. The remaining five components (Ranking, Consistency, Coverage, Grounding, Sentiment) are scheduled for v1.5 and beyond per the AIAS 1.0 roadmap and are not affected by v1.4's revision.

Importantly, the v1.4 decomposition does not alter the AIAS six-component framework's overall architecture. It refines the Presence component's internal structure. Researchers extending the framework to additional substrates or to the remaining five components can proceed against the v1.4 specification of Presence without architectural conflict.

# 3. Phase A — Recognition Anchoring Measurement

## 3.1 Pivot Validation

Phase A operates on tradition cells within the brand panel. Each cell is assigned an ordinal sequence of pivot candidates per the pre-registered panel design. The cell's first ordinal pivot enters Phase A measurement. If the pivot achieves Recognition score $R(\cdot) = 1$ (Phase A C_P PASS), the cell pivot is locked. If $R(\cdot) = 0$ (C_P FAIL), the cell's next ordinal alternate is activated and the procedure repeats. Cascade depth is bounded by the cell's pre-registered alternate list; cascade exhaustion produces a cell-collapse event (§3.5).

## 3.2 Automated C_P Classifier

In v1.3, the Phase A Recognition indicator $\rho_R(b, k)$ was determined by operator judgement: the operator read $\tau(b, k)$ for each (brand, slot) cell and assigned $\rho_R(b, k) \in \{0, 1\}$. v1.4 supersedes this with an automated classifier.

**Classifier specification.** The automated C_P classifier is locked at the following parameters:

- **Model:** claude-opus-4-7
- **Sampling:** model-default (the `temperature`, `top_p`, and `top_k` parameters were deprecated on this model in the April 2026 Anthropic API revision; sampling is now model-default and not configurable via the API)
- **Maximum output tokens:** 200
- **Prompt template:** the `CLASSIFIER_PROMPT_TEMPLATE` constant, locked in the v1.4 classifier script
- **Output schema:** two-line response, format `ANCHORED: <0 or 1>\nRATIONALE: <one short sentence, max 25 words>`

The classifier reads $\tau(b, k)$ for each cell, returns $\rho_R(b, k) \in \{0, 1\}$, and writes a one-sentence rationale to the classification ledger as audit trail. The ledger column `anchoring_note` preserves this rationale for external review.

**Reproducibility commitment.** The (model, prompt template) pair constitutes the methodological lock. Two invocations of the classifier against the same ledger with the same (model, prompt template) should produce identical anchoring calls on stable classification cases. Anthropic documentation states that `temperature = 0` did not guarantee bit-exact determinism on this model in any case; v1.4's reproducibility commitment is therefore at the (model, prompt) level rather than the bit-exact-output level. Genuinely borderline classification cases may flip on rare re-runs; this is an empirical property of the substrate, not a protocol defect.

**Audit-trail property.** The classifier's per-row rationale is methodologically substantive. Operator-judgement protocols typically produce a verdict without a row-level rationale; the automated classifier produces a structured rationale for every cell. External reviewers can audit any classification decision in detail. This is a credibility property of v1.4 that v1.3 did not possess.

**v0.17 first-cascade case study.** v0.17 Premium Kitchenware was the first phase to operate the automated classifier in production. The Japanese-cell primary pivot (Vermicular) C_P FAILED at 4/6 anchoring: classifiers led with "Japanese cookware brand" for four cells but with non-substrate referents for two cells (one slot framed "vermicular" as a multi-meaning term; another defined it as an adjective meaning worm-like). The first alternate (Iwachu) C_P PASSED at 6/6 with classifier rationales reading uniformly as "Japanese manufacturer of cast iron cookware." The cascade resolved the Japanese cell at depth 1. The classifier's row-level rationales preserved both verdicts in defensible detail.

## 3.3 Cascade Pipeline

The Phase A cascade pipeline is implemented in `scripts/classify_phase_a_v1_4.py` (v17-versioned phase script; structurally identical pattern across phases). The pipeline has three operational modes auto-detected from ledger state and BRANDS extension:

- **Fresh ledger:** Generate ledger rows for all (brand, slot) pairs in the BRANDS list. All rows have empty `anchored` column.
- **Cascade extension:** Existing ledger present with prior classifications; BRANDS list extended (e.g., with a cascaded alternate). New rows added for the alternate's six slots; existing rows preserved with their classifications intact.
- **Tally:** All rows in ledger have $\rho_R$ filled; produce per-brand anchoring counts and PASS/FAIL verdicts.

The cascade-extension mode is methodologically important. Cascade events do not invalidate prior classifications; they extend the ledger forward. Each cascade round is an additive operation. External reviewers can reconstruct the complete sequence of cascade events from the ledger plus the corresponding DEVIATIONS entries, with every row's verdict preserved from its original commit.

**Idempotency property.** The automated classifier (§3.2) is idempotent against already-filled ledger rows: rows with $\rho_R \in \{0, 1\}$ are skipped. Re-running the classifier after a cascade extension consumes API quota only for the newly added rows. This composes with the cascade-extension mode to produce a clean pipeline: extend ledger, invoke classifier, re-tally; existing classifications are never recomputed.

## 3.4 Recognition Score Output

Phase A produces, per brand $b$:
- Per-slot indicator $\rho_R(b, k)$ for $k = 1, \ldots, 6$.
- Per-row classifier rationale (one sentence, $\leq 25$ words).
- Aggregate Recognition score $R(b) \in \{0, 1\}$ per §2.3.
- Phase A verdict (C_P PASS if $R(b) = 1$; C_P FAIL otherwise).

The Phase A classification ledger is the canonical artifact. For each phase, the ledger is committed to `osf/v<NN>/classification_ledger.csv` and is preserved unchanged through downstream phases.

## 3.5 Cell-Collapse Mechanics

Per v1.3 §6.4.7.3 (preserved unchanged in v1.4): if all alternates in a cell's pre-registered ordinal sequence return C_P FAIL, the cell is dropped from the operational panel for downstream phases. The pre-registered C1 worldwide-n adequacy criterion is evaluated against the surviving (post-cascade) panel.

The bounded-override provision per v1.3 §6.4.7.2 (preserved unchanged in v1.4) permits a one-time-per-cell-per-phase operator-judgement override of a C_P FAIL verdict if the operator determines the failure is a methodological-edge anchoring noise event rather than a substantive disqualification. Use of bounded override requires contemporaneous DEVIATIONS entry. v0.17 did not invoke bounded override (the Vermicular cascade resolved at Iwachu at depth 1).

# 4. Phase B — Recall Presence Measurement

## 4.1 Substrate-Coherence Rationale

v1.3 inherited Phase B from the v0.13–v0.15 Trends-substrate research line. Phase B in v1.3 was a Google Trends signal validation step: each brand's bare canonical name was queried against the SerpAPI Google Trends interface for an out-of-sample window; brands with non-zero signal received PASS, brands with zero signal received an E5 bundled rescue attempt, and brands with persistent zero signal received EXCLUDED_E1a.

The Trends-substrate Phase B specification gates brands by search interest—a Physical Availability proxy under the Ehrenberg-Bass tradition. v0.16-onward research operates on the LLM-mediated retrieval substrate (per the Methodology v1.3 specification of Phase A and per the substantive theoretical framing of AI Availability). Continuing the Trends-substrate Phase B in v0.16-onward research produces a substrate mismatch between Phase A (LLM-substrate) and Phase B (Trends-substrate). The substrate mismatch is methodologically incoherent: the two phases gate brands by different constructs, yet Phase B's PASS or FAIL determines downstream Phase D measurability against a third construct (LLM-mediated retrieval).

v1.4 resolves this by specifying Phase B on the LLM substrate. The substrate-coherence principle: **Phase B's measurement substrate must match Phase D's measurement substrate.** Phase A may measure on a different substrate if the substantive question requires it; Phase A is a recognition-anchoring gate, not a measurability gate. Phase B is a measurability gate; it must measure on the substrate Phase D will score against.

## 4.2 LLM-Substrate Phase B

The LLM-substrate Phase B specification:

**Inputs.** A brand panel of $n$ brands; a category substrate $S$; a six-slot LLM reference panel $\mathcal{L}$ (identical to Phase A's panel); a set $\mathcal{Q}$ of $M$ category queries about $S$ that are tradition-agnostic and unprompted with respect to any specific brand.

**Acquisition.** For each $(Q_m, L_k) \in \mathcal{Q} \times \mathcal{L}$, the protocol issues a single-shot query $Q_m$ to $L_k$ and caches the response $r_{m,k}$ to `osf/v<NN>/data/phaseB_queries/{Q_m_id}/slot_{k}.json`. The query set is locked at script-commit time; modifications require a new pre-registration event or DEVIATIONS entry.

**Mention detection.** For each $(b, Q_m, L_k)$ triple, the protocol determines the Recall indicator $\rho_C(b, m, k)$ by case-insensitive word-boundary regex matching against an alias set generated from $b$'s canonical name (per §4.3).

**Tier assignment.** Per §2.4, brand $b$ receives:
- **PASS** if Recall rate $C(b) \geq 1/K$.
- **PASS_E5** if $0 < C(b) < 1/K$.
- **EXCLUDED_E1a** if $C(b) = 0$.

The tier vocabulary (PASS, PASS_E5, EXCLUDED_E1a) is preserved from the v0.13–v0.15 Trends-substrate Phase B. Cross-phase grammar is intact; the underlying substrate is different.

## 4.3 Mechanical Alias Generation

For each brand canonical name $b$, the protocol generates a mechanical alias set $\text{aliases}(b)$ by composing three rules:

1. **Canonical forms.** Always include $b$ and $\text{lower}(b)$.
2. **Hyphen variants.** If $b$ contains hyphens, additionally include $b$ with hyphens replaced by spaces and $b$ with hyphens removed.
3. **Space variants.** If $b$ contains spaces, additionally include $b$ with spaces replaced by hyphens and $b$ with spaces removed.

For example, canonical "All-Clad" generates aliases \{"All-Clad", "all-clad", "All Clad", "AllClad"\}. Canonical "Made In" generates \{"Made In", "made in", "Made-In", "MadeIn"\}.

**Mechanical alias generation is not semantic.** Variants like "Field and Company" or "Field Co." for canonical "Field Company" are not generated. Semantic aliases require registry-level alias entries. This is a documented limitation; the v1.4 brand registry schema specifies an optional `aliases` field for brands requiring semantic-variant matching. Mechanical alias generation handles the most common variant patterns at zero registry-maintenance cost; semantic-alias registration is recommended for brands with documented variant usage.

## 4.4 Recall Rate Output

Phase B produces, per brand $b$:
- Per-cell indicator $\rho_C(b, m, k)$ for $(m, k) \in \mathcal{Q} \times \mathcal{L}$.
- Per-query mention counts (max $K$) and per-slot mention counts (max $M$).
- Aggregate Recall rate $C(b) \in [0, 1]$ per §2.4.
- Phase B tier (PASS, PASS_E5, or EXCLUDED_E1a).

The Phase B resolution log `osf/v<NN>/registries/topic_id_resolution_log_v<NN>.csv` is the canonical artifact. Cross-phase grammar is preserved with the Trends-substrate predecessor: column names, tier vocabulary, and notes-field structure are parallel.

## 4.5 Substrate-Substitution Attrition

The LLM-substrate Phase B specified above has substantially different natural attrition characteristics than the Trends-substrate Phase B it supersedes. This is a methodologically substantive observation, anchored in v0.17 evidence.

The v0.17 pre-registration anticipated 1–3 brands of Trends-substrate Phase B attrition (the pre-registration was written prior to the substrate substitution decision). v0.17 actual LLM-substrate Phase B attrition was 5 brands: the entire Japanese cell (Iwachu, Sori Yanagi, Noda Horo) and two American brands (Field Company, Smithey). Observed attrition was approximately 2$\times$ the worst-case Trends-substrate estimate.

The mechanism is intuitive in retrospect. Google Trends signal is approximately democratic across brands with non-trivial market presence: even niche brands with modest search volume produce non-zero signal on a 14-day out-of-sample window. LLM unprompted category recall is approximately winner-take-most: when asked "What are the best cookware brands?", LLMs concentrate their responses on the most prominent five-to-ten brands and rarely mention beyond that band. The two substrates measure approximately the same construct (brand prominence in market awareness) on the surface but differ sharply in their concentration profiles. LLM-substrate Phase B is a stricter filter than Trends-substrate Phase B at the long-tail end.

**Operational implication for panel design.** Programs designed under v1.4 should over-provision their cell sizes more conservatively than programs designed under v1.3's Trends-substrate Phase B assumptions. The v0.17 panel was designed with conservative 1–3 brand attrition; the actual 5 brand attrition produced a C1 floor breach. v0.18 and subsequent programs should design panel cell sizes assuming approximately 30–50% Phase B attrition at the long-tail end of each cell. For three-cell panels with worldwide-n adequacy floor at $n = 12$, this implies cell sizes of at least 6 to maintain margin against simultaneous mid-tier attrition across multiple cells.

# 5. Recognition $\times$ Recall Decomposition — Empirical Anchor

## 5.1 v0.17 Premium Kitchenware Case Study

v0.17 Premium Kitchenware is the empirical anchor for the v1.4 decomposition. The substantive program tested $H_{\text{Regime4\_kitchenware}}$ on a 16-brand panel spanning three tradition cells (European, American, Japanese). The substantive hypothesis verdict was FALSIFIED on panel inadequacy after Phase B reduced the operational panel to $n = 10$, below the pre-registered C1 floor of $n = 12$. The pre-registration anticipated this outcome path; the joint $H_{\text{IdentityLoad\_moderator}}$ verdict is AMBIGUOUS pending v0.18 indie fragrance.

The substantive verdict is not the methodological contribution of v0.17. The methodological contribution is the empirical demonstration of Recognition $\times$ Recall dissociation, which is the foundation of v1.4's revision.

## 5.2 The Iwachu Canonical Case

Iwachu's Phase A and Phase B verdicts are reproduced in Table 1 for reference.

\begin{table}[h]
\centering
\begin{tabular}{lll}
\hline
\textbf{Phase} & \textbf{Indicator value} & \textbf{Interpretation} \\
\hline
Phase A (Recognition) & 6/6 anchoring & Substrate identity unambiguous in all 6 LLMs \\
Phase B (Recall) & 0/18 mentions & Never surfaces in unprompted category retrieval \\
\hline
\end{tabular}
\caption{Iwachu Phase A and Phase B verdicts. The brand has stable recognition anchoring across the full panel but zero recall presence across all 18 measurement cells.}
\end{table}

The classifier rationales at Phase A read uniformly as variations of "Japanese manufacturer of cast iron cookware." The LLM responses at Phase B (the eighteen response cells across three queries and six models) list cookware brands prominently but never include Iwachu in any list. The dissociation is observable at the response level: the same LLM that wrote "Iwachu is a Japanese manufacturer of cast iron cookware" in response to "Who or what is Iwachu?" did not include Iwachu in its response to "What are the best premium cookware brands?".

This pattern admits two non-trivial readings, neither of which weakens the decomposition claim:

**Reading 1: Storage vs Retrieval.** Iwachu is stored in the LLM's knowledge representation but is not retrieved by the category-based query patterns the LLM applies. The storage and retrieval pathways are not equivalent. Recognition queries access storage directly via the brand-name pointer; recall queries access storage via category-based retrieval mechanisms that have additional filtering or salience criteria. This reading suggests Recognition and Recall are operationally dissociable by design of the LLM architecture.

**Reading 2: Salience vs Identification.** Iwachu's knowledge representation in the LLM is identification-quality (the LLM can describe what it is) but not salience-quality (the LLM does not list it among prominent brands). Salience and identification are dissociable: a brand can be identifiable without being prominent. Recognition queries probe identification quality; Recall queries probe salience.

Both readings are consistent with the empirical pattern and with cognitive-science precedent on human memory. The v1.4 decomposition does not require selecting between them; it requires only that the two components be measured separately, which the protocol now does.

## 5.3 Generalization Across the v0.17 Panel

Iwachu is the canonical case but not the only case. The full Japanese cell post-Phase-A-cascade (Iwachu, Sori Yanagi, Noda Horo) showed the same pattern at Phase B: zero mentions across all 18 cells. The American cell showed partial dissociation: Field Company and Smithey received Recognition-quality treatment in their respective LLM training but zero Phase B mentions. The European cell showed near-complete consistency between Recognition and Recall: Le Creuset, Mauviel, All-Clad, and Staub all received Recognition-quality identification and near-saturated Recall (15-18/18 mentions); only Fissler showed marginal Recall (2/18, the borderline PASS_E5 case).

The pattern is not uniform across cells. The European cell behaves near-equivalently on both surfaces. The American cell shows mid-tier dissociation. The Japanese cell shows full dissociation. The cell-level variation is itself informative: dissociation depends on the cell's training-data coverage and category-query salience, not on the brand's substantive importance in the substrate.

## 5.4 Theoretical Significance

The decomposition is theoretically significant for the Tri-System architecture. AI Availability, as the third system alongside Mental Availability and Physical Availability, requires a measurable construct definition. v1.4 establishes the measurable construct as Recognition $\times$ Recall, with Recall as the recommended primary aggregator (per §2.5's recall-leaning weighting).

The recall-leaning weighting reflects the substantive theoretical claim that AI-mediated commerce depends on what AI intermediaries spontaneously surface, not on what they can identify when prompted. A consumer asking an AI assistant "What's a good cookware brand?" receives an answer that depends on Recall, not Recognition. The Recognition score is methodologically valuable as a substrate-anchoring gate and as the foundation of the protocol's Phase A pivot validation, but the substantive theoretical interest is in Recall.

# 6. Cross-Cultural Confound — Methodological Caveat

## 6.1 v0.17 Western-LLM Bias Observation

The Japanese-cell full collapse at v0.17 Phase B is hard to disambiguate from Western-language LLM training-data bias. All three Japanese brands carried high Identity Load by the Tri-System theoretical framework: Iwachu's nambu-tekki heritage; Sori Yanagi's designer-craft heritage; Noda Horo's enamelware heritage. By the substantive prediction of $H_{\text{IdentityLoad\_moderator}}$, these brands should have shown stronger AI Availability than low-Identity-Load brands in the same cell. The opposite pattern was observed: zero Recall across the cell.

The reading "Identity Load does not moderate AI Availability" is one possible interpretation. The reading "Western-language LLM training-data bias is large enough on cross-cultural substrates to swamp the Identity Load signal" is another. The v0.17 data does not distinguish between them. The substantive hypothesis verdict was FALSIFIED on panel inadequacy (independent grounds: C1 floor breach), which the pre-registration explicitly committed to; the joint $H_{\text{IdentityLoad\_moderator}}$ verdict is AMBIGUOUS pending v0.18.

## 6.2 Same-Language Identity Load Test Recommendation

v0.18 is pre-positioned to test Identity Load on indie fragrance, a substrate with entirely English-language category surface (Maison Margiela, Le Labo, D.S. & Durga, Byredo, Diptyque, and related brands all have substantial English-language LLM training coverage). The same-language design eliminates the Western-language training-data bias confound that contaminated the v0.17 cross-cultural substrate. The Identity Load gradient within the indie-fragrance substrate is testable on equal LLM-coverage terms.

The v1.4 methodological caveat for cross-cultural AIAS measurement: **AIAS scores on cross-cultural substrates require an explicit confound-control reporting protocol.** Programs measuring cross-cultural substrates (e.g., a future substrate including non-English-coverage brands) should pre-register language-coverage controls and report cross-cultural cell results with explicit confound annotation. Programs measuring same-language substrates (the v0.18 indie-fragrance design) are not subject to this caveat.

## 6.3 Multi-Language Test Infrastructure — Forward Action for v1.5

The fundamental research question—whether AIAS scores are cross-culturally comparable—requires a multi-language LLM reference panel. v1.4 operates on a six-slot English-language reference panel. v1.5 should extend the reference panel to include native-language LLMs for each major non-English market (Japanese, Mandarin, French, Spanish, German, Portuguese) and pre-register a cross-language AIAS measurement protocol. Cross-language AIAS comparison is a methodologically substantial undertaking that is outside v1.4's scope but is positioned as the natural successor research direction.

# 7. Composite AI Availability — Formal Definition

## 7.1 The Composite Formula

Composite AI Availability for brand $b$ in substrate $S$:

$$A(b) = w_R \cdot R(b) + w_C \cdot C(b)$$

where $R(b) \in \{0, 1\}$ is the Recognition score (§2.3), $C(b) \in [0, 1]$ is the Recall rate (§2.4), and $w_R + w_C = 1$.

The composite is defined for all $b$ in the operational panel after Phase A and Phase B have completed. For brands with $R(b) = 0$ (C_P FAIL), the brand is descoped from the panel and the composite is not computed. For brands with $R(b) = 1$ and Phase B tier EXCLUDED_E1a (i.e., $C(b) = 0$), the composite is reported as $A(b) = w_R$ (Recognition contribution only).

## 7.2 Reference Weightings

**Balanced weighting ($w_R = 0.5$, $w_C = 0.5$).** $A(b) = 0.5 R(b) + 0.5 C(b)$. Reported in all v1.4-compliant deliverables.

**Recall-leaning weighting ($w_R = 0.3$, $w_C = 0.7$).** $A(b) = 0.3 R(b) + 0.7 C(b)$. Reported in all v1.4-compliant deliverables as the primary AIAS Presence score.

Programs may report additional weightings as substantive variants if motivated by a specific measurement objective; the two reference weightings are mandatory for v1.4 compliance.

## 7.3 Composite Behavior on Iwachu

The Iwachu canonical case (§5.2) produces composite values that demonstrate the formula's behavior in the dissociation limit:

- $R(\text{Iwachu}) = 1$, $C(\text{Iwachu}) = 0$.
- Balanced: $A(\text{Iwachu}) = 0.5$.
- Recall-leaning: $A(\text{Iwachu}) = 0.3$.

A brand with zero Recall presence but full Recognition anchoring receives a composite AI Availability of 0.3–0.5. This is a meaningful intermediate value: the brand has stable LLM identity (substantive partial AI Availability) but no unprompted recall (no contribution to AI-mediated category retrieval). The composite formula captures both halves of the brand's AI Availability profile.

Compare to a brand with no Recognition anchoring and zero Recall (Vermicular in v0.17): $A(\text{Vermicular})$ is undefined under v1.4 because the brand is descoped at Phase A. The composite formula is not computed for C_P FAIL brands.

Compare to a brand with full Recognition and full Recall (Le Creuset in v0.17, $R = 1$, $C = 1$): $A(\text{Le Creuset}) = 1.0$ under both weightings. The brand has the strongest possible v1.4 composite AI Availability.

## 7.4 Composite as Phase D Input

Phase D scoring (per Methodology v1.2 §3, preserved unchanged in v1.4) operates on the composite $A(b)$ across the operational panel. Spearman $\rho$ correlations with brand age and tradition controls are computed using $A(b)$ values per the recall-leaning weighting as primary and per the balanced weighting as sensitivity. Per-cell ρ values are reported per pre-reg §2.3.2 conventions where cell $n \geq 5$.

The Phase D scoring rule itself is not revised in v1.4. The revision affects only the input: $A(b)$ now aggregates Recognition and Recall per the §7.1 formula rather than being measured as a single unidimensional Presence score.

# 8. Forward Actions for v1.5 and Beyond

## 8.1 Inter-Rater Reliability Across Classifier Models

v1.4 locks the automated C_P classifier at claude-opus-4-7. Cross-classifier reliability—running the classifier against a second model (e.g., gpt-4o or gemini-2.5-pro) on the same ledger and measuring anchoring disagreements—is a methodologically substantive robustness check that v1.4 specifies as a v1.5 forward action. The disagreement rate would establish the empirical floor of classifier non-determinism and inform whether the (model, prompt) reproducibility commitment is sufficient or requires a multi-classifier consensus protocol.

## 8.2 Operator-Override Interface

The automated classifier produces a verdict and rationale for every cell. Cells with genuinely borderline classifications—where the LLM response could reasonably be classified either way—are at present indistinguishable from cells with confident classifications. v1.5 should add a classifier confidence indicator and an operator-override interface for cells flagged as low-confidence. The override mechanism would be limited to low-confidence flagged cells; high-confidence classifications would not be overrideable, preserving the audit-trail integrity.

## 8.3 Composite Formula Maturation

v1.4's composite formula uses two reference weightings (Balanced and Recall-leaning). v1.5 should extend the formula in two directions: (1) a substrate-conditioned weighting that adjusts $w_R$ and $w_C$ based on the substrate's Identity Load (high-IL substrates lean further toward Recall; low-IL substrates lean further toward Recognition); (2) a confidence-weighted composite that incorporates classifier confidence (§8.1) as a multiplier on the per-cell indicators.

## 8.4 Multi-Language Reference Panel

v1.5 should extend the six-slot reference panel to include native-language LLMs per §6.3. The extension is methodologically substantial; it requires a parallel locked-panel specification per supported language and a cross-language composite formula that handles measurement on potentially asymmetric reference panels.

## 8.5 Remaining AIAS Components

The AIAS™ composite has six components: Presence, Ranking, Consistency, Coverage, Grounding, Sentiment. v1.4 refines Presence (the only component currently measured) to multi-component status. v1.5 should add Ranking measurement; v1.6 and beyond should add the remaining four components. The AIAS 1.0 roadmap targets full six-component measurement by v2.0 of the protocol.

# 9. Audit Chain and Reproducibility

## 9.1 v0.17 Audit Chain

The v0.17 program, which serves as the empirical anchor for v1.4, has a complete git audit chain from pre-registration through formal verdict. Key references:

- Pre-registration v0.17-prereg-r1 (commit `3ebe426`, tagged on `2026-05-19`).
- Phase A automation: DEVIATIONS Entries 4–5 (commits `2097c9f`, `9042dea`).
- Phase A cascade: DEVIATIONS Entry 6, Vermicular C_P FAILED, Iwachu activated and C_P PASSED (commits `d09182c`, `1304237`).
- Phase A lock: tag `v0.17-phase-a-locked` (commit `8cdf0cd`).
- Phase B substrate substitution: DEVIATIONS Entry 7 (commit `55e28ed`).
- Phase B outcome: DEVIATIONS Entry 8, Japanese cell collapse, C1 floor breach (commit `1b560d2`).
- Phase B lock and verdict: tag `v0.17-phase-b-locked` (commit `54c83ec`).

The audit chain is publicly accessible at the AIAS programmatic repository. Each entry in the chain is reproducible against the original commit state.

## 9.2 v1.4 Reproducibility Commitments

v1.4 commits to reproducibility at the following levels:

1. **Classifier reproducibility:** automated C_P classifier reproduces anchoring calls modulo upstream model non-determinism. The (model, prompt template) pair is locked.
2. **Cascade reproducibility:** ledger-extension semantics preserve all prior classifications; cascade events are additive, not destructive.
3. **Phase B reproducibility:** LLM-substrate Phase B response cache is committed to git; mention detection is mechanical regex matching; cache regeneration requires `--force` flag.
4. **Audit-trail reproducibility:** every classifier verdict carries a row-level rationale; every cascade event carries a contemporaneous DEVIATIONS entry; every phase carries a lock document and (where substantive) a verdict document.

These reproducibility properties are stronger than v1.3's and substantially stronger than the v0.13–v0.15 Trends-substrate programs.

## 9.3 OSF Deposit Structure

v1.4 introduces no new OSF deposit conventions beyond v1.3's. Per-phase deposits follow the pattern: pre-registration markdown, brand registry JSON, classification ledger CSV, Phase B resolution log CSV, response cache directory tree, DEVIATIONS markdown, phase lock documents, verdict document (where applicable), per-phase SSRN paper PDF, supplementary figures.

The OSF project ID for the AIAS programmatic deposits is `ec6wh` (preserved from prior versions).

# 10. Declarations

**Author affiliations.** Pablo Ulpiano González Castro. School of Visual Arts, MPS Branding Program, New York, NY (primary academic affiliation). Third System™ (research entity; data archive and methodology venue).

**Correspondence.** pablou@pablou.com $\cdot$ pablou.com. ORCID 0009-0003-8968-9990.

**Declaration of Interest.** The author is employed by Samsung Electronics America in a corporate brand governance role. The AIAS research program is conducted outside the scope of employment, on personal time, with no Samsung resources or data. Samsung has no review, approval, or veto rights over AIAS publications. The author has no financial or material interest in any of the brands measured in the AIAS program, including the v0.17 Premium Kitchenware panel brands.

**Funding.** Self-funded.

**Ethics.** Not applicable. No human subjects. Measurement is on publicly accessible APIs (Anthropic, OpenAI, Google) and pre-specified LLM prompts.

**Data availability.** All v0.17 data, code, classification ledgers, Phase B response caches, DEVIATIONS entries, and lock documents are publicly available via the AIAS programmatic git repository and OSF project `ec6wh`. The v1.4 methodology specification is fully detailed in this paper.

**JEL classification.** M31 (primary); L86, L15, D83, M37 (secondary).

**Keywords.** AI Availability; AIAS; LLM-mediated retrieval; brand measurement; recognition memory; recall memory; pre-registration; methodological protocol.

# References

González Castro, P. U. (2026a). *AI Availability: A Third System of Brand Presence*. SSRN Working Paper 6659000.

González Castro, P. U. (2026b). *The AIAS Presence Measurement Protocol: Methodological Notes on Construct Validity and the Four-Regime Taxonomy*. SSRN Working Paper 6761698.

González Castro, P. U. (2026c). *The AIAS Presence Measurement Protocol: Phase A Pivot-Validation Specification*. SSRN Working Paper 6797679.

González Castro, P. U. (2026d). *Regime 4 Boundary and Discourse-Language Carryforward on the Kitchen-Knives Substrate*. SSRN Working Paper 6791999.

González Castro, P. U. (2026e). *Panel Inadequacy and the Recognition-Recall Dissociation on the Premium Kitchenware Substrate*. SSRN Working Paper (forthcoming, v0.17 program report).

Mandler, G. (1980). Recognizing: The judgment of previous occurrence. *Psychological Review*, 87(3), 252–271.

Romaniuk, J. (2018). *Building Distinctive Brand Assets*. Oxford University Press.

Sharp, B. (2010). *How Brands Grow: What Marketers Don't Know*. Oxford University Press.

Sharp, B., and Romaniuk, J. (2021). *How Brands Grow Part 2: Including Emerging Markets, Services, Durables, B2B and Luxury Brands* (Revised Edition). Oxford University Press.

Yonelinas, A. P. (2002). The nature of recollection and familiarity: A review of 30 years of research. *Journal of Memory and Language*, 46(3), 441–517.

---

*Version v1.4 of the AIAS Presence Measurement Protocol. Supersedes v1.2 (SSRN 6761698) and v1.3 (SSRN 6797679). Submitted to SSRN, May 2026.*
