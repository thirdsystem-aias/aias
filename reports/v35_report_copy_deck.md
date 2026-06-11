# v0.35 Third System(TM) brand-format report — CERTIFIED COPY DECK
#
# MAPPING INSTRUCTIONS (Claude Code):
# - Map each [SECTION] verbatim into the corresponding attribute of
#   reports/v35_phantom_cpc_omnibus_content.py, preserving the cloned module's
#   data types (string / list / tuple structure) exactly as build_report_v35.py
#   expects. Split prose into the clone's structural units without rewording.
# - Akkurat markup rules (apply mechanically, do not alter wording):
#     t1 / t2  ->  t<sub size='6'>1</sub> / t<sub size='6'>2</sub> in body text
#                  (size='10' at cover/18pt scale); NEVER Unicode subscripts.
#     Arrows: wrap with NBSP -> "t1\u00a0\u2192\u00a0t2" pattern where -> appears.
#     Greek rho: <font name='Helvetica'>(rho)</font> — but this deck avoids Greek
#                entirely; do not introduce it.
#     No ">=" glyph issues: deck uses "4 or more" / "4+" spellings — keep them.
# - Charts: chart refs named [CHART:chart_0N_...] — wire to the builder's
#   reservation slots in the order given.
# - Verdict-status labels in [HYPOTHESIS_SCORING] are final copy.

[COVER]
TITLE: The Question the Instrument Couldn't Answer
SUBTITLE: Phantom brands, AI consistency, and a measurement test that flipped on its own control
PROGRAM LINE: AIAS(TM) Measurement Program - Phase v0.35 - Third System(TM)

[STANDFIRST]
Some brands are recognized by AI models but never named by them — phantom brands. They score differently on consistency measures, and v0.35 asked the obvious question: is that difference real, or just an echo of how little AI recalls them? The pre-registered answer is neither yes nor no. The test itself cannot tell — and demonstrating that, with confirmatory rigor, is the deliverable.

[LEAD_DECK]
This phase re-analyzed five frozen category panels — 112 brands, six AI models, no new model calls — to test whether phantom brands carry a distinct consistency signature. The design knew its own trap in advance: the phantom label and the consistency metric are both built from recall, so a raw comparison is rigged from the start. The inferential weight sat entirely on a gate with two controls and a binding rule: if the controls disagree, the verdict is undetermined and the disagreement is the finding. The controls disagreed. Controlled for recognition, the phantom gap survives at full strength. Controlled for recall itself, it vanishes. Same data, same procedure, opposite verdicts — stable across category leave-outs and reproduced wave to wave. The instrument, not the brands, is what got measured.

[EXEC_SUMMARY]
Phantom brands sit at the bottom of the AI consistency table — but the test designed to find out whether that is a real signature or a recall echo returned "undetermined," by its own pre-registered rule, because its two controls flatly disagree.

The disagreement has a clean mechanical explanation. Recognition is maxed out: in three of five categories, every measurable brand is recognized by every model, so a recognition-based control has nothing to remove and waves the gap through. A recall-based control removes the very thing that defines a phantom brand, and the gap disappears with it.

The raw gap itself is enormous — phantom brands score far lower on consistency, unanimously, in every category, in both measurement waves. But the program's own rules label that a manipulation check, not a finding: the gap is built into how the pieces are defined.

The practical conclusion is about the measuring stick. A yes/no recognition signal cannot police a recall-based consistency metric. The next methodology revision (v1.8) now carries two requirements with pre-registered evidence behind them: a consistency measure that does not move with recall volume, and a graded recognition signal that still varies among well-known brands.

The phantom-signature question stays open — deliberately. It is now a designated re-test for the redesigned instrument, with this phase's frozen panel as the baseline.

[WHAT_WE_MEASURED]
v0.35 is a re-analysis: no new AI queries, no new brands. The inputs are the program's frozen omnibus panels — audiophile headphones (16 brands), skincare (24), cosmetics (24), automotive (24), and premium spirits (24): 112 brand units measured across the same six-model panel used since v0.17. A phantom brand is one the models recognize when asked directly but do not surface when asked to name brands in the category — recognized, never recalled. The frozen classification flags 57 of the 112. Twenty-eight of those 57 were never recalled by any model even once: with no recall at all, a consistency-of-recall score cannot be computed, so the measurable phantom set is 29 brands against 55 non-phantoms. One category (automotive) had only one measurable phantom and enters pooled analysis only; the other four cleared the pre-set floor of 4 or more.
[CHART:chart_06_roster_attrition]

[PATTERNS]
P1 — The verdict depends on the control, and that is the finding. The gate test asked whether the phantom consistency gap survives once you account for how present a brand already is. Accounted for via recognition, the gap survives essentially intact (effect -0.80, decisive). Accounted for via recall volume, it collapses to nothing (+0.07, indistinguishable from noise). The pre-registered rule for disagreement fired: verdict undetermined, disagreement reported as the result. It held in every category leave-out and repeated in the second wave.
[CHART:chart_01_gate_flip]

P2 — Why the flip happens: recognition has nowhere left to go. In three of five categories, every measurable brand — phantom or not — is recognized by all six models. A control that never varies cannot remove anything; it inherits whatever the raw data showed. Recall volume, by contrast, separates phantom from non-phantom in every category — because that separation is what the phantom label means. One control is blind, the other is circular. Neither can referee.
[CHART:chart_02_recognition_saturation]

P3 — The raw gap is huge, and built-in. Phantom brands score drastically lower on cross-model consistency: a pooled effect of -0.84 on a scale where -1 is total separation, decisive at 10,000 simulations. The program reports this as a manipulation check, not a discovery. The phantom label is defined by low recall, and the consistency metric mechanically drops when recall is low. The gap confirms the pipeline works; it does not yet tell you anything about the brands.
[CHART:chart_03_raw_manipulation_check]

P4 — Unanimous in direction, unprovable by design. Every category shows phantoms lower — headphones -0.94, skincare -0.96, cosmetics -0.89, automotive -1.00 (one brand; illustrative only), spirits -0.62. With only four categories eligible for the formal cross-category test, even perfect unanimity cannot clear the significance bar (floor p = 0.125). The pre-registration said so in advance; the unanimity is reported as description, not proof.
[CHART:chart_04_cross_substrate_concordance]

P5 — Run it again, get the same picture. On the second measurement wave, every element repeats: the big raw gap (-0.82), the recognition-controlled gap surviving (-0.79), the recall-controlled gap vanishing (+0.06), and the five-for-five negative direction. The flip is a stable property of the measurement structure, not a one-wave fluke.
[CHART:chart_05_t2_stability]

[LIMITATIONS]
The 28 phantom brands excluded for total silence are precisely the most extreme cases — the measurable phantom set is the moderate end of the phenomenon. The phantom flag itself captures "recognized but below the recall floor," which mixes brands that are genuinely gone with brands that are merely obscure; this design cannot tell them apart. The hypothesis was partly motivated by exploratory glimpses in earlier phases of this same data family, and the second wave is a near-replica panel, not an independent replication. Scope is five consumer categories, measured in English, on one six-model panel, at one pair of time points. And the consistency quantity itself holds characterization status only — it was never adopted as an instrument, which is, in the end, what this phase demonstrates the wisdom of.

[WHATS_NEXT]
The findings route directly into v1.8, the consistency-methodology revision, which now carries two design requirements with confirmatory evidence behind them: the consistency instrument must not move mechanically with recall volume, and the presence control must be graded — capable of telling well-known brands apart instead of flatlining at "yes, recognized." Once that instrument exists, the phantom-signature question returns as a designated re-test, with this phase's frozen 84-brand analysis set as the comparison baseline. Two further threads follow: separating gone-brands from merely-quiet brands inside the below-floor population, and asking whether consistency, properly measured, has a category structure of its own.

[HYPOTHESIS_SCORING]
P1 — ESTABLISHED. The gate verdict flips with the choice of control; the pre-registered disagreement rule declared it undetermined, and the flip is the finding.
P2 — ESTABLISHED. Recognition is saturated in three of five categories; the recognition control is structurally inert exactly where the comparison lives.
P3 — OBSERVED, BY CONSTRUCTION. The raw phantom consistency gap is large and decisive — and labeled a manipulation check, because both sides of it are built from recall.
P4 — OBSERVED, UNDERPOWERED BY DESIGN. Direction unanimous across all five categories; the formal cross-category test cannot reach significance at this scale, as pre-registered.
P5 — OBSERVED. The entire structure — gap, survival under one control, collapse under the other — reproduces on the second wave.

[HYPOTHESIS_DETAILS]
P1 (gate flip). Identical residualization procedure, two controls. Recognition control: effect -0.80, p = 0.0001 — would read CONFIRMED. Recall-volume control: +0.07, p = 0.655 — reads FALSIFIED. Binding pre-registered rule: disagreement means UNDETERMINED, flip reported as the finding, routed to the v1.8 methodology revision. Stable in all five leave-one-category-out runs.

P2 (saturation). Recognition count is constant across all measurable brands in cosmetics, automotive, and spirits — the control is a no-op there and inherits the raw signal. Recall volume separates phantom from non-phantom in every category, because the phantom flag is defined by it. The pairing demonstrates that a yes/no recognition signal cannot govern a recall-coupled metric.

P3 (raw gap, manipulation check). Pooled effect -0.84 (29 measurable phantoms vs 55 non-phantoms, 296 within-category pairs), p = 0.0001 at 10,000 simulations; leave-out range -0.93 to -0.79; verdict unchanged at stricter and looser thresholds. Reported as pipeline confirmation only, per the locked inferential-weight rule.

P4 (cross-category). Per-category effects: headphones -0.94, skincare -0.96, cosmetics -0.89, automotive -1.00 (single measurable phantom, illustrative), spirits -0.62. Four eligible categories, 4-of-4 concordant, exact-test floor p = 0.125 — significance structurally unreachable, stated in the pre-registration.

P5 (second wave). Wave-two values: raw -0.82; recognition-controlled -0.79; recall-controlled +0.06 (noise); per-category direction negative five-for-five. No brand left the panel between waves; the measurable phantom set, recomputed from wave-two recall, grew from 29 to 33 as four silent brands picked up nonzero recall. Descriptive check, kept outside all verdict logic.

[CLOSING]
The most useful thing a measurement program can publish is sometimes a precise account of what its instrument cannot yet measure. v0.35 set out to characterize phantom brands and ended up characterizing the yardstick — with pre-registered rigor, a binding rule that fired exactly as designed, and a result that converts an open question into an engineering specification. The phantom brands are still out there, still recognized, still unnamed. When the instrument is rebuilt to v1.8's requirements, the program will know precisely where to point it first.
