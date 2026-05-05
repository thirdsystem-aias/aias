# Third System — Research Log

**Started:** May 3, 2026
**Owner:** Pablo Ulpiano Gonzalez Castro
**Purpose:** Running record of methodological work on AIAS. Time-stamped. Raw material for the forthcoming methodology paper, *Measuring AI Availability: Methodological Notes from the AIAS Protocol*.

---

## How to use this log

**Capture, don't curate.** Don't wait for the right framing. Don't wait until it's "ready." Three months from now you won't remember why olive oil's first registry needed expansion, or why the v0.4 maturity hypothesis felt convincing before v0.6 killed it. Right now you do. Write it down.

**Format per entry:**
- **Date** and what was being done
- **Expected** — what you thought would happen
- **Observed** — what actually happened
- **Hypothesis** — your best current explanation
- **Implication** — what this changes about the protocol or the framework

When an entry has all four, it's likely a paragraph or a figure in the methodology paper. Entries that don't fit the template (structural decisions, tooling notes, deferred questions) go below the dated entries in **§ Open threads**.

**Origin marker.** Sections labeled *backfilled* or *retrospective* were drafted by Claude from prior session records. They are not yet Pablo's words. Verify, edit, expand, or reject. Anything tagged `[VERIFY]` is Claude's interpretation of what was implied; anything tagged `[FILL]` is an operational detail only the local files have.

---

## 2026-05-04 — Phase 2 v0.7: BBB phantom measurement

**Doing:** Ran the first designed-for-test category from Phase 2 — Bed Bath & Beyond as a Pattern 6 (phantom-brand persistence) replication test of the v0.6 Mint observation. Single intensive session: pre-registration document locked → six-prompt × six-model × eight-run sweep (288 measurements) → manual valence review of every BBB mention → drafted v0.7 report. The session covered design, execution, analysis, and reframe in one continuous push.

**Expected:** The v0.6 Mint finding would replicate at lower magnitude (Mint 44% → BBB ~25–35%, with the H1 floor pre-registered at ≥25%). Within-Anthropic freshness would show Sonnet > Opus by ≥15 points (newer model = fresher training = less phantom). Pier 1 as the structural comparator would land below 15%. The phantom mechanism would be naive lag — AI hasn't updated on the closure.

**Observed:** BBB at 38.2% raw Presence — within four points of Mint and clearing H1 by 13 points. But the result fractured the naive-lag interpretation. Manual review of all 110 BBB mentions showed:
- 1.7% naive_phantom (AI presents BBB as fully live, no caveat)
- 25.0% live_with_caveat (AI surfaces BBB alongside disclosure of closure/rebrand)
- 2.4% status_correction (AI explicitly says BBB is closed)
- 8.7% historical_reference (past tense only)

**88% of BBB mentions demonstrate AI knows the entity has changed.** The 38.2% headline is *not* AI being unaware. AI is informed, and surfaces BBB anyway, with disclaimer.

H3 disconfirmed at raw level — Opus surfaced BBB *more* than Sonnet (56.2% vs 41.7%, reversing the predicted direction by 14.5 points). But Opus's mentions were 96% responsibly handled vs Sonnet's 90%. **Newer models phantom-mention better, not less.** Same pattern within-OpenAI — flagship gpt-5.5 had the lowest raw rate (14.6%) but gpt-5.4-mini (older, smaller) had the highest aware-mode rate.

H7 confirmed in the strongest possible form: Pier 1 = 0.0% across all 288 measurements. Zero. The structural comparator carrying smaller pre-collapse footprint and longer time-since-collapse produces zero phantom signal in the same registry, against the same prompts, across the same models.

H6 partially confirmed and produced a finding outside pre-registration: per-CEP analysis showed BBB occupies *different temporal frames* depending on the prompt. FUNCTIONAL prompts get BBB-as-current-online-retailer (70.8% Presence, mostly caveated). IDENTITY prompts get BBB-as-cultural-memory (81.2% Presence, 43.8% aware-mode). DISCOVERY produced zero BBB mentions. Same brand, six prompts, six different cognitive-time slots. The v0.6 framework didn't anticipate temporal-frame variance within a single brand.

**Hypothesis:** The phantom is a **recommendation slot, not a knowledge gap**. BBB's accumulated editorial volume in AI training corpora — decades of comparison articles, registry guides, household-essentials listicles, store-by-store rankings — encoded a recommendation slot. The slot persists in AI's recommendation logic regardless of the entity's current operating status. When the entity changes, AI does not vacate the slot. AI fills the slot with disclaimer.

This is structurally stronger than naive lag. Naive lag suggests training-data freshness as the variable to optimize. Recommendation-slot persistence suggests brand-mention pathways are reinforcement-encoded structures that retraining does not directly address. The same brand can live in different recommendation slots across different models — and across different prompts within the same model — even when every model's underlying knowledge of the entity is identical.

**When the reframe emerged:** During manual review, not before. The pre-registration treated the phantom mechanism as naive lag (consistent with how the Mint finding had been framed in v0.6). The valence taxonomy was designed to *quantify* lag — the assumption was that a meaningful fraction of BBB mentions would be live_recommendation (the "AI doesn't know" case). When manual review of the first ~30 mentions showed live_with_caveat dominating, the reframe forced itself. Recording this matters for the methodology paper because the reframe is exploratory, not confirmatory, and the paper should be honest about that.

**Why Pier 1 specifically as the structural comparator:** Considered Stadia and SVB during design. Stadia is a cleaner shutdown but the cloud-gaming category is too small for a proper registry comparison (only ~5 named competitors). SVB has the regulatory-category confound (banking would activate refusal modes that household goods doesn't). Pier 1 is structurally analogous to BBB on the dimension that matters — same fate (collapse → online-only revival under the same legacy domain) — but differs on the two variables we want to separate: pre-collapse footprint (~$1.5B revenue, smaller specialty) and time-since-collapse (70 months vs 37 months). Two variables not separable from a single brand; readable from the BBB-vs-Pier 1 contrast.

**Why six models from four labs, not the v0.6 two-model design:** The v0.6 Anthropic-vs-OpenAI 42-point spread on Mint was the second-largest in the personal finance dataset and the cleanest per-model freshness signal. To test whether that pattern was specific to the Anthropic-OpenAI pair or a structural property of the AI ecosystem, Phase 2 needed within-lab generational pairs (Sonnet 4.6 / Opus 4.7; gpt-5.4-mini / gpt-5.5) plus cross-lab diversity (Google Gemini 2.5 Flash, xAI Grok 4.1 Fast as the oldest-cutoff comparator at November 2024). The lineup was designed to separate "newer model" from "specific lab" as variables. The within-Anthropic and within-OpenAI patterns turned out to point the same direction — newer = more responsible handling, not less raw frequency — which is a stronger structural finding than any single-pair difference.

**Risk #2 from pre-registration materialized as predicted.** Walmart and Amazon ceiling-compressed the COMPARISON and FUNCTIONAL prompts at near-100% each, leaving BBB structurally constrained in the COMPARISON frame regardless of phantom strength. BBB COMPARISON Presence: 8.3%. The pre-registered risk identified this; the result confirmed it. This is the kind of methodological discipline the methodology paper will cite — predicting structural risks in writing before measurement, then observing whether they manifest.

**Spot-check audit on naive-phantom labels.** The 1.7% naive-phantom rate is the headline for Finding 02 (the recommendation-slot reframe). Independent audit on a stratified 25-row sample produced 88% strict agreement with the AI classifier. All five live_recommendation rows verified correct on independent review. Three boundary disagreements clustered on caveated/correction/historical adjacency, none affecting the headline number. This is what makes Finding 02 defensible.

**Failed-call recovery.** Initial sweep produced ~67% completion rate (192/288 successful) — the first time multi-lab + reasoning-model + temperature-handling complexity hit the runner. Pre-registered failed-call recovery cycle restored to 100%. Worth recording: the runner needed `supports_temperature: False` flags for both Opus 4.7 and gpt-5.5 (reasoning models that reject temperature parameter). The xAI integration uses the OpenAI SDK with a different base URL — two-line addition, no new SDK dependency.

**Implication for protocol:** Phase 2 surfaces enough new methodology to justify a v1.1 increment. The new sections needed:
- Pre-registration as standard practice (PRE_REGISTRATION_<category>_<version>.md template, eight-hypothesis structure, locked before measurement)
- Manual valence review with five-level + four-level taxonomies
- Multi-lab model lineup (six models, four labs, within-lab generational pairs, oldest-cutoff comparator) replacing the v0.6 two-model setup
- Phantom-brand methodology (phantom subject + structural comparator + valence taxonomy + entity-reference taxonomy + per-CEP temporal-frame analysis) as a reproducible category-design pattern

**Implication for framework:** The recommendation-slot reframe is the methodology paper's hero finding now. It says AI brand visibility is structurally different from any prior brand-visibility metric — not a measurement of consumer awareness, not a lagged indicator of consumer behavior, but a property of how AI mediation composes recommendation sets. The BBB-vs-Pier 1 contrast is the cleanest empirical demonstration in the AIAS dataset.

**Implication for Tri-System paper:** §9.5a (Corporate Portfolio Layer) currently cites AIAS with naive-lag as the implicit phantom mechanism. Recommendation-slot persistence is a stronger argument for AIAS-as-third-availability-layer because it says AI mediation has its own reinforcement structure that retraining doesn't directly address — earning the "third availability layer" label rather than inheriting the existing mental/physical framing.

**Promotion candidates for the methodology paper:**
- Finding 02 (recommendation-slot reframe) → Discussion section, the central thesis
- Finding 04 (per-CEP temporal frames) → Results section, novel sub-finding
- BBB/Pier 1 contrast → Methods section, designed-for-test exemplar
- Pre-registration document + spot-check audit → Methods section, rigor signal
- The reframe-emerged-during-analysis story → Discussion section, exploratory honesty

---

## 2026-05-03 — Phase C typesetting consolidation

**Doing:** Pushing v0.6 cross-category findings report from drafted Markdown into a fully typeset PDF, using the build pipeline (`build_report.py`). Resolving layout fights — orphaned titles, font compression, hero-chart placement, sandwich vs body-then-chart for non-hero patterns. Tag this as the canonical v0.6 reference render.

**Methodological observation (not a layout note):** Going through this typesetting fight surfaced something about how the report artifact relates to the protocol. The build pipeline as currently structured fuses the protocol-stable parts (palette, fonts, page templates, footer text) with the report-specific parts (which patterns, which charts, which sections in which order). For v1.0 to be a research instrument, those have to separate. Drafted `report_spec_template.json` and `MEASUREMENT_PROTOCOL.md` in this session as the start of that separation.

**Implication for protocol:** The protocol document is what stays constant across reports. The spec is what changes. This needs to be the structural decision before any v1.0 report is built.

**Implication for this log:** Start it now, not in two weeks. The framing recommendation from the parallel chat ("wait until you have substance") was wrong on perishability grounds.

---

## Version history — backfilled chronological entries

*Reconstruction by Claude from prior session records. Verify, edit, reject. The thematic v0.6 retrospective below is where the substantive observations live; this section exists to give the methodology paper a defensible chronological spine for its change-log section, and to resolve the v0.2-calibration-error `[FILL]` flagged in § Failure modes seen.*

---

### 2026-04-28 — v0.1 baseline (Day 2)

**Doing:** First measurement run on PM software. 5 prompts × 3 models × 5 runs = 75 calls. 15-brand registry. Detection by regex word-boundary matching against an alias list. Output metric: raw mention rate as percentage.

**Expected:** Mention rate by itself would already differentiate brands enough to publish a leaderboard.

**Observed:** Asana / Jira / Linear clustered tightly around 79% mention rate. Mention rate alone did not separate the leaders.

**Hypothesis:** Mention rate is necessary but not sufficient. A second signal — *where* the brand appears in the response, not just *whether* it appears — is needed to separate brands once a mention-rate ceiling is approached.

**Implication:** Triggered the v0.2 work on rank and primary-recommendation flags, which in turn triggered the calibration error documented below.

---

### 2026-04-29 morning — v0.2 calibration error

**Doing:** Re-extracted the same data with structured-output (function-calling) extraction. Added rank, sentiment, and primary-recommendation flags. Introduced a composite: `0.4 × MentionRate + 0.4 × RankSOM + 0.2 × PrimaryRecRate`, normalized so the leader = 100.

**Expected:** A clean 0–100 scale where the leader sits near 100 only if its absolute performance warrants it.

**Observed:** Rank-relative normalization forced the leader to 100 *regardless* of absolute performance. With Asana / Jira / Linear clustered near 79% mention rate, v0.2 displayed Linear at 100 and the others at 92 / 84 — implying a near-saturation that the underlying data did not support. This was inconsistent with the framework's own definition of AIAS as a 0–100 *absolute* scale.

**Hypothesis:** Two conceptual errors compounded. (1) Conflating relative ranking with absolute presence. (2) Treating the composite output as AIAS itself rather than as one component of it.

**Implication:** v0.2 output is superseded. Triggered the v0.3 reframe: output is the **AI Presence Index** (the first of six AIAS components), `presence_score = raw mention rate`, no normalization, with RankSOM / Primary-Rec as separate descriptive columns. Consistency added as a column with the explicit label "future AIAS component, displayed for transparency." This calibration error is preserved in the v0.3 methodology log because it is a non-trivial cautionary tale about scale construction in a multi-component framework, and it should be cited in the methodology paper rather than buried — a documented dead-end is more credible than a clean-only narrative.

---

### 2026-04-29 evening — v0.3 first stable methodology

**Doing:** Reframed metric per the v0.2 lesson. Added a sixth prompt (`COMPARISON`). Increased to eight runs per prompt (96 measurements per category). Published `methodology.md v0.3` and the PM software dataset (`presence_index_v0.3_pm.csv`).

**Expected:** Eight runs × six prompts would produce stable mention-rate estimates with within-prompt variance small enough to read leaderboard differences as signal, not noise.

**Observed:** Within-prompt variance stabilized at the level expected for the given run count. The COMPARISON prompt introduced a different structural property — it surfaces a "default winner" pattern that the other five prompts do not, and this matters for how Presence aggregates across prompt modes.

**Hypothesis:** Six prompts is the right minimum because the CEPs span structurally different cognitive entry points. Fewer prompts under-samples the brand's exposure surface; more prompts mostly add cost.

**Implication:** Six-prompt design locked. `[VERIFY: was eight runs/prompt empirically grounded — i.e., did variance plateau there — or chosen for cost/budget reasons? The methodology paper will need a defensible answer.]`

---

### 2026-04-30 to 2026-05-01 — v0.4 olive oil registry expansion

**Doing:** First measurement run on premium olive oil with a 16-brand curated registry.

**Expected:** A curated registry built from market share + editorial-discourse audit would cover the meaningful competitive set.

**Observed:** Cobram Estate surfaced as the top brand in the unknown-mentions list — at a level that materially affected the leaderboard. Three additional brands also appeared above the unknown-mentions threshold.

**Hypothesis:** Editorial-discourse audit alone systematically misses a tier of category players that AI mediation surfaces. Specifically, brands with strong specialty-press coverage but limited mainstream coverage are visible to AI but invisible to a registry built from mainstream sources.

**Implication:** Expanded registry to 20 brands. Re-measured. Formalized the **registry-revision protocol** (§2.4 of the protocol document) as a standard practice, not an exception: when the unknown-mentions list exceeds a threshold that affects the leaderboard, the registry is expanded and the category re-measured. Published v0.6 data is from post-revision runs only; pre-revision runs are preserved in the methodology log for traceability.

---

### 2026-05-01 to 2026-05-02 — v0.4 skincare registry expansion

**Doing:** First measurement run on premium facial skincare with the initial curated registry.

**Expected:** Olive oil's expansion was a one-off due to specialty-press dynamics; mainstream curation would suffice for skincare.

**Observed:** First run surfaced La Roche-Posay, Vanicream, and six additional dermatologist-recommended drugstore brands as significant unknown mentions.

**Hypothesis:** Skincare's editorial discourse has two distinct authority axes — *prestige beauty press* (Vogue, Allure, Harper's) and *dermatologist consensus* (clinical/medical-adjacent press). Registry construction from prestige beauty press alone misses the dermatologist axis, which AI mediation weighs heavily because dermatologist consensus has high textual coherence in training corpora.

**Implication:** Confirms that registry expansion is the standard practice, not the exception. Two of five v0.6 categories required revision. The unknown-mentions list is now framed as a continuing diagnostic for registry quality, not a one-time check. **Question for protocol:** what is the formal threshold for triggering revision? `[FILL: the operational rule used in v0.6 — likely "any unknown brand whose mention rate exceeds the lowest-ranked registry brand's mention rate," but confirm.]`

---

## v0.6 retrospective — methodological observations

The entries below are extracted from the v0.6 cross-category report content (`v06_content.py`) and framed as research-log observations. **Pablo to verify, edit, expand, or reject.** Anything tagged `[VERIFY]` is interpretation; anything tagged `[FILL]` is an observation Pablo has but isn't in the report content.

### What worked in the prompts

The six-CEP-anchored prompt structure produced clean signal. The asymmetry between Comparison-mode and Discovery-mode responses replicated across all five categories — that's the strongest result of v0.6 (Pattern 2). The fact that the asymmetry survives across software, durables, food, beauty, and financial services strongly suggests the prompt-mode structure is operating on something real about how AI models internally route category queries, not on category specifics.

The Constraint and Functional prompts surfaced Default Reinforcement (Pattern 5) in a way that more general prompts wouldn't have. Skincare's three near-deterministic prompts — Identity asking what dermatologists recommend, Constraint asking about sensitive skin, Functional asking about normal-to-dry moisturizers — all converged on the same small drugstore brand set. That triple-replication is what made Pattern 5 publishable.

Discovery prompts that named a specific market disruption (the personal finance Discovery prompt naming Mint) produced strong, useful convergence. Discovery prompts framed generically about "emerging brands" produced diffuse responses, particularly in skincare where no clear emerging tier exists.

`[FILL: any prompt-design tweaks that turned out to be load-bearing? Specific phrasings that surprised you in either direction?]`

### What didn't work

The v0.4 hypothesis that per-model variance was a function of **category maturity** turned out to be wrong. Olive oil is mature and produced wide variance; running shoes is similarly mature and produced narrow variance. The unifying variable is **discourse coherence**, not maturity. v0.6 is where the maturity hypothesis was retired in favor of the coherence hypothesis. This is paper-grade material — a hypothesis that died cleanly between versions because cross-category data forced it to.

`[FILL: any other hypotheses that died? The protocol's failure modes section in MEASUREMENT_PROTOCOL §6.3 has [FILL] markers where you should record the policy decisions made (what counts as model refusal, when registry expansion is triggered, how hallucinated brands are disambiguated).]`

The skincare Discovery prompt produced no clear emerging tier — Tatcha, Augustinus Bader, Youth to the People at 25%/25%/12%, none reaching 50%. Initially this looked like a measurement failure (the prompt isn't doing its job). But on reflection it's a structural finding: skincare's editorial discourse has been so thoroughly worked through that **no brand confidently occupies an "emerging" cognitive slot** in the AI's recommendation logic. Every plausible "emerging" skincare brand has been editorially established for 5+ years. So the diffuseness is the finding, not a failure.

This is methodologically important. It says: when a prompt mode produces a diffuse response, that doesn't automatically mean the prompt is broken. It can mean the AI's internal category structure has no occupant for the cognitive slot the prompt activates. **Distinguishing these two cases is hard and may require manual inspection of the response set.** This is a `[FILL]` for the protocol's QA section.

### Surprises

**Rocket Money 71-point spread.** The largest single-brand variance observed across any category, on a brand that exists in both training corpora. Two models, asked the same six prompts about the same category, produced effectively disjoint answers about whether Rocket Money exists as a category player. `[FILL: was this expected, or did it shock you when you saw it? The size of the gap or the existence of the gap — which was more surprising?]`

**CeraVe zero-spread.** The only zero-spread leader observed across any category in v0.6 — identical 67% Presence on both OpenAI and Anthropic. Zero spread on a brand that's a category leader. `[FILL: was this a confirmation of the discourse-coherence hypothesis or a surprise?]`

**Mint at 44% on a brand that no longer exists.** 25 months after decommissioning, Mint placed fifth in personal finance Presence — ahead of Rocket Money, EveryDollar, Quicken Simplifi, PocketGuard. The Anthropic-vs-OpenAI 42-point spread on Mint was the second-largest in the personal finance dataset. `[FILL: when did you first notice the phantom-brand pattern? Did it emerge from looking at the data or did you go looking for it?]`

**Beauty of Joseon at zero with strong English-media coverage.** A K-beauty brand with substantial *Allure*, *Vogue*, *Glamour*, *The Strategist* coverage scored zero across both runs. The English-media-coverage hypothesis (that brands well-covered in English-language media would score higher regardless of marketing language) failed cleanly here. The refined hypothesis — that **marketing-discourse language**, not editorial coverage, is the operative variable — was forced by Tatcha (Japanese aesthetic, English-language marketing, 18% Presence) sitting next to Beauty of Joseon (Korean aesthetic, Korean-language primary marketing, 0%).

**The authority-mode finding for the discourse-language hypothesis.** When the AI was asked Discovery-mode questions in skincare and olive oil, it named publications instead of brands. **Every publication named was English-language.** This was an unexpected secondary signal for Pattern 4 — not a finding about which brands the AI surfaces but a finding about which media infrastructure the AI treats as authoritative. The brand-mention bias is downstream of an authority-recognition bias. `[FILL: was this anticipated as a way to test the language hypothesis, or did it emerge from looking at component-mode and authority-mode responses for other reasons?]`

**The Functional-prompt component-mode finding in skincare.** "What moisturizer is best for fine lines in late thirties?" produced 95% component-mode responses (retinol, vitamin C, niacinamide, etc.) instead of brand names. Initially this looked like a Presence-measurement failure (the AI didn't surface brands). On reflection it's a foundational finding — **a brand-mode-conditional Presence measurement is not the same as the AI's full surface for that category**. This forced the three-modes formalization (§3.4 of the protocol). Without it, the framework would have been claiming category coverage it didn't have.

### Boundary conditions emerging

**Pattern 2 (comparison-discovery asymmetry) holds across 5/5 but weakens in skincare.** The mechanism — AI converges on incumbents in Comparison, elevates challengers in Discovery — is structural across all five categories. But the strength varies, and the variation tracks the existence of an "emerging" cognitive slot in the AI's category model. Where editorial discourse has filled that slot (skincare), the asymmetry is weaker. Where the slot is open (olive oil DTC, PM software niche tools, running shoes specialty brands), the asymmetry is sharp.

**Pattern 3 (AI-vs-awareness divergence) holds across 5/5 but inverts in personal finance.** Four of five categories show downward divergence (large brands under-perform in AI mediation). Personal finance inverts: a small brand (YNAB ~1M users) dominates over larger brands (Rocket Money ~5M users). The mechanism is the same — AI mediation rewards discourse position over commercial scale — but the directionality depends on which brands have the strong narratives. This is a clean two-directional finding and it's what makes Pattern 3 publishable.

**Pattern 4 (discourse-language bias) is preliminary.** Two categories support it; alternative explanations (US retail availability, English-targeted marketing investment, category-specific distribution) have not been controlled for. **A category designed-for-test is in scope for Phase 2.** Candidates: Japanese kitchen knives, French wine, Korean small electronics — categories where a non-English-discourse country dominates global production but has limited US-targeted English marketing.

**Pattern 6 (phantom brands) is single-category but striking.** Mint at 44% in a category with a 2-year-old shutdown is sufficiently large that it warrants standalone reporting. Phase 2 will add a category with a deliberate disruption-test (Twitter→X, Bed Bath & Beyond, etc.) to test whether the pattern replicates.

### Construct validity observations

`[FILL: this section is critically thin. The protocol §8.1 lists three observed correlations from v0.6 (with discourse coherence; inconsistent with consumer awareness; with editorial-consensus alignment). Each of those is a paper paragraph. Specifically: where in the data did you see the cleanest signal for each? What numbers would you put in the methodology paper?]`

The cleanest construct-validity observation from v0.6 is negative: **AI Presence is not predicted by marketing budget or distribution scale**. Nike (largest marketing budget in running shoes) at 6th. Bertolli (most distributed olive oil) at near-zero. La Mer (highest-priced skincare incumbent) outscored 30:1 by CeraVe. This negative result is a methodologically important paper claim — it says the construct AI Presence measures is not redundant with existing brand metrics.

### Failure modes seen

Documented in the protocol (§6.3). Specific instances from v0.6 worth recording:

- **Gemini Workspace-domain access restriction** during the study window. Operational, not protocol — but it shaped the v0.6 dataset substantially. v0.6's two-model variance is a lower bound; Gemini's reinstatement in Phase 2 will likely widen the spread.
- **Registry expansion in 2/5 categories** (olive oil, skincare). Both triggered by the unknown-mentions diagnostic. Both produced post-revision data that's the published v0.6 dataset. The pre-revision data is preserved in the methodology log for traceability. *Backfilled as dated entries in § Version history.*
- **The v0.2 calibration error** — preserved in the v0.3 methodology log; *backfilled as a dated entry in § Version history*. The composite formula was rank-relative-normalized so the leader was forced to 100 regardless of absolute performance, which contradicted the framework's definition of AIAS as a 0–100 absolute scale. A documented dead-end is more credible than a clean-only narrative.
- **Per-model training-data freshness asymmetry**, cleanest signal from Mint (Anthropic 65%, OpenAI 23%). This isn't a protocol failure but a methodological finding about the construct.

### Category-selection logic in retrospect

The v0.6 categories were chosen sequentially. Looking back:

- **Project management software** (inaugural) was chosen for B2B, mature, AI-delegation-heavy. Confirmed Pattern 2 and a mild form of Pattern 3.
- **Running shoes** chosen for contrast — physical/consumer/identity-heavy. Surfaced narrow per-model variance (Pattern 1's converged-discourse case). Demonstrated Nike's downward divergence (Pattern 3).
- **Premium olive oil** chosen for English-discourse-dominates-globally-fragmented-production. Surfaced the discourse-language bias (Pattern 4) before it was a hypothesis to test.
- **Premium facial skincare** chosen for very-coherent-editorial-consensus. Surfaced Default Reinforcement (Pattern 5) and the second confirmation of Pattern 4.
- **Personal finance** chosen for fragmented-discourse-with-recent-disruption. Surfaced the largest Pattern 1 variance (Rocket Money 71pt) and Pattern 6 (phantom Mint) — neither of which was the hypothesis going in.

**The axes that turned out to matter for AI Presence behavior, ranked by what we now know:**

1. **Discourse coherence** (Pattern 1, Pattern 5). The most operative variable.
2. **Editorial-consensus alignment to prompt framing** (Pattern 5). Determines deterministic-vs-stratified-vs-diffuse response shape.
3. **Marketing-discourse language** (Pattern 4, preliminary). Determines whether non-English-language-marketing brands surface.
4. **Recent disruption** (Pattern 6). Determines presence of phantom brands.
5. **Category maturity** — does NOT matter as much as v0.4 hypothesized. This is a retired hypothesis.

`[FILL: anything in this ranking you'd reorder or push back on?]`

---

## Open threads

Items that aren't dated entries but should not be lost.

- **Within-prompt variance plateau.** `[VERIFY]` whether eight runs/prompt was empirically grounded (variance plateaus) or budget-driven. The methodology paper needs a defensible answer.
- **Registry-revision threshold.** `[FILL]` the formal operational rule for triggering registry expansion. Currently described qualitatively as "unknown-mentions exceeding a level that affects the leaderboard."
- **Diffuse-response disambiguation.** `[FILL]` the provisional rule for distinguishing prompt failure from structurally empty cognitive slots. Needs to live in §6 of the protocol. Provisional candidate: diffuse-but-coherent responses where the model articulates *why* it can't pick a clear leader count as structural; diffuse-and-incoherent responses where the model lists candidates without justification count as prompt failure.
- **Phase 2 categories.** Two categories selected: one to test discourse-language bias (Pattern 4), one to test phantom-brand persistence (Pattern 6). **Pattern 6 closed: Bed Bath & Beyond designed-for-test ran 2026-05-04, replicates the v0.6 Mint phantom finding at 38.2%, reframes the mechanism from naive lag to recommendation-slot persistence (see 2026-05-04 dated entry).** Pattern 4 still open. Pattern 4 candidates: Japanese kitchen knives, French wine, Korean small electronics. Selection deferred until methodology paper draft has substance.
- **Construct validity.** Phase 3. The single biggest open question for the framework. Currently flagged in every report as "not yet established." The negative result (AI Presence ≠ marketing-budget-or-distribution) is the cleanest signal v0.6 produced; this is the place to start in Phase 3 design.
- **Hosting decision for v1.0.** Personal GitHub vs. thirdsystem.ai vs. SSRN as the canonical reference URL. Affects how the protocol cites itself.
- **Mode classifier as Phase 2 pre-step.** Operationalization of the three-modes formalization. Needs a decision on whether classification is automated (LLM-as-judge) or manual.

---

## Citation pattern for entries promoted to the methodology paper

When an entry from this log becomes a paragraph or figure in *Measuring AI Availability: Methodological Notes from the AIAS Protocol*, mark it here with the section it lands in. This keeps the log auditable as a primary source and makes it easy to revisit if a reviewer asks where a claim came from.

| Log entry | Methodology paper section |
|---|---|
| 2026-04-29 v0.2 calibration error | Methods §3 — scale-construction cautionary tale |
| 2026-04-30 / 2026-05-01 olive oil + skincare registry expansions | Methods §2.4 — registry-revision protocol |
| 2026-05-04 BBB Finding 02 (recommendation-slot reframe) | Discussion §1 — central thesis of the paper |
| 2026-05-04 BBB Finding 04 (per-CEP temporal frames) | Results §3 — novel within-brand sub-finding |
| 2026-05-04 BBB/Pier 1 structural-comparator design | Methods §4 — designed-for-test exemplar |
| 2026-05-04 BBB pre-registration + spot-check audit | Methods §5 — rigor signal |
| 2026-05-04 reframe-during-analysis | Discussion §3 — exploratory honesty |
| v0.6 maturity → discourse-coherence hypothesis revision | Results §1 — hypothesis dying cleanly between versions |
| v0.6 negative result (AI Presence ≠ marketing/distribution) | Discussion §2 — construct-non-redundancy claim |

---

## Template for new entries

```
## YYYY-MM-DD — short description of session

**Doing:** What was the actual activity. Be specific.

**Expected:** Your prior hypothesis going in. What did you think the outcome would be?

**Observed:** What actually happened. Numbers if available. Qualitative observations if not.

**Hypothesis:** Your best current explanation. May be tentative.

**Implication:** What this changes — for the protocol, for the framework, for the reports, for which paper this fits in.
```
