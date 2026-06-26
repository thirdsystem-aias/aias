"""
v0.37 — Identity-Load × CPC — Brand-format report content module.
Third System(TM) managerial register. Companion to the v0.37 SSRN paper
(the pre-registered component-dissociation null), written for brand teams,
not reviewers. The finding, in managerial terms: identity-load positioning
moves WHETHER AI surfaces a brand, not HOW CONSISTENTLY it does so across
models — you cannot buy cross-model consistency through the identity lever.

Register discipline:
  - No academic hypothesis labels (H_*), no "moderator/dissociation/verdict-
    matrix/partial/permutation" jargon in body text. Plain brand-strategy voice.
  - A clean null renders italic-neutral (status_class "neutral"), never bold —
    nothing in v0.37 is CONFIRMED, so every proposition is neutral.
  - The null is a REDIRECTION, not reassurance: "this lever is inert on this
    outcome," never "consistency is fine here." That framing is structural,
    carried through EXEC_SUMMARY, WHATS_NEXT, and CLOSING — not a lone caveat.
  - No Samsung anywhere (COI lives only in the SSRN paper Declarations).

Attributes: COVER, STANDFIRST, LEAD_DECK, EXEC_SUMMARY, WHAT_WE_MEASURED,
PATTERNS, LIMITATIONS, WHATS_NEXT, HYPOTHESIS_SCORING, HYPOTHESIS_DETAILS, CLOSING.
Finding body renders from HYPOTHESIS_SCORING (headline) + HYPOTHESIS_DETAILS (text).
Every figure is bound to one proposition (P1→dissociation, P2→precise-null,
P3→cross-substrate, P4→floor); the cross-substrate figure is report-only.
"""

COVER = {
    "title": "The Lever That Moves Visibility, Not Consistency",
    "subtitle": "Identity-load positioning changes whether AI names your brand — not how consistently it does so across models",
    "tagline": "AIAS™ Measurement Program · Phase v0.37 · Third System™",
}

STANDFIRST = "When a customer asks three different AI assistants which brands to consider in your category, do they hear the same names — or a different set each time? That steadiness, model to model, is its own axis of AI visibility, separate from getting named at all. This phase asked whether a brand's cultural identity — the lever that already shifts whether AI names you — also makes that naming steadier across assistants. It does not. The identity lever buys visibility, not consistency; and knowing that, with pre-registered rigor, tells brand teams where not to spend."

LEAD_DECK = "v0.37 re-analyzed three frozen category panels — skincare, cosmetics, and automotive; 53 analyzable brands across six AI models, no new model calls. Identity load — how much a brand leans on cultural rather than category-standard retrieval — was already a confirmed driver of whether AI surfaces a brand. Here it shows no relationship to how consistently the six models surface it: the association sits at zero, and the test was strong enough to have caught a real effect. The practical reading is a redirection, not an all-clear — if a brand's AI presence is inconsistent across assistants, identity positioning is not the lever that fixes it."

EXEC_SUMMARY = "Cultural identity moves whether AI names a brand. It does not move how consistently AI names it across models. Tested directly on three categories, the association between a brand's identity load and its cross-model consistency is essentially zero (−0.01, on a scale where ±1 is a perfect relationship) — no relationship, in either direction.\n\nThis is not reassurance. A zero here does not mean a brand's cross-model consistency is fine; it means the identity lever is inert on that outcome. If the six assistants disagree about whether to name a brand, leaning harder into cultural positioning will not steady them. Consistency is a separate problem, and it needs a separate lever — one the program does not yet have, and is openly building toward.\n\nThat separation is the contribution. Identity load drives one axis of AI visibility (whether a brand surfaces) and is inert on another (how consistently it surfaces). Two axes that answer to different things are two different problems — which is exactly why a brand cannot treat \"get named\" and \"get named consistently\" as the same campaign.\n\nThe result is a real absence, not a test too weak to find an effect. The sample cleared the pre-set minimum, and the method could have detected an effect of the size that would matter. It found essentially nothing — and nothing in any single category either: the three categories disagree in direction and all sit near zero, so there is no hidden \"works in my category\" exception.\n\nThe reading is bounded, and the bounds are real rather than hedging: one identity lever, one consistency measure, three English-language categories, one panel of six models, one point in time. It is one clean result that identity does not buy consistency — not the last word on either."

WHAT_WE_MEASURED = "v0.37 is a re-analysis — no new AI queries, no new brands. It draws on three frozen category panels the program built earlier: skincare, cosmetics, and automotive, 24 brands each, measured across the same six AI models used since 2025. \"Identity load\" is how much a brand surfaces through cultural cues — a celebrity founder, a lifestyle following, a cult reputation — rather than plain category membership. \"Cross-model consistency\" is whether the six models agree on surfacing a brand, or whether one names it and another does not. Of the 72 brands, 53 could be scored for consistency; the other 19 were recognized by the models but never actually named, so there was no naming over which to measure consistency — the subject of the fourth figure."

PATTERNS = ""  # findings render from HYPOTHESIS_SCORING (headline) + HYPOTHESIS_DETAILS (body)

LIMITATIONS = "This is one result, read within its edges. It tests one lever — identity load — against one measure of consistency; a different identity signal, or a different way of measuring agreement across models, could behave differently. It covers three categories, in English, on one panel of six models, at one moment; a larger or different set of assistants could show structure these six do not. And it is silent on the brands set aside — the ones AI recognizes but never names — because consistency cannot be measured where there is no naming to begin with. None of these edges weakens the finding inside them: identity does not buy cross-model consistency, on the categories and the measure tested here. They mark where the claim stops, not where it wobbles."

WHATS_NEXT = "Consistency being a separate problem from visibility is not a dead end — it is a redirection, and the program is already following it. The next phase (v0.38) tests a second, different identity-type lever — phantom brand persistence — against the same consistency measure: if it also comes back null, the case strengthens that consistency answers to something other than how a brand is positioned; if it moves the needle, it tells brand teams which lever does. In parallel, the program is building the instrument that can finally measure consistency among the brands set aside here — the ones AI knows but never names — which today's naming-based measure cannot reach. The honest state is plain: identity is not the lever for cross-model consistency, and the search for the lever that is continues, in public, one pre-registered phase at a time."

HYPOTHESIS_SCORING = [
    {"id": "P1", "headline": "Identity moves visibility, not consistency",
     "proposition": "A brand's cultural identity, which already shifts whether AI names it, has no relationship to how consistently AI names it across models — the lever that buys visibility does not buy consistency.",
     "verdict": "NO EFFECT ON CONSISTENCY", "qualifier": "", "status_class": "neutral"},
    {"id": "P2", "headline": "A real absence, not a weak test",
     "proposition": "The zero is a measured absence, not a test too small to find an effect: the method could have detected an effect of the size that would matter, and found essentially none.",
     "verdict": "A REAL ABSENCE", "qualifier": "", "status_class": "neutral"},
    {"id": "P3", "headline": "No category is the exception",
     "proposition": "Run category by category, the three disagree in direction and all sit near zero — no overall effect, and none hiding inside any single category.",
     "verdict": "NO CATEGORY PATTERN", "qualifier": "", "status_class": "neutral"},
    {"id": "P4", "headline": "Recognized, but never named",
     "proposition": "The brands set aside from the measure are recognized by the models — most by all six — yet never named; recognition and naming are different things, and consistency can only speak to what gets named.",
     "verdict": "RECOGNITION ISN'T RECALL", "qualifier": "", "status_class": "neutral"},
]

HYPOTHESIS_DETAILS = {
    "P1": "Identity load was already established as a driver of AI Presence — whether and how strongly AI surfaces a brand. In these same three categories, leaning on cultural identity measurably raised whether the models named a brand. This phase asked the next question: does it also make that naming steadier across models? The answer is no. Measured brand by brand, the association between identity load and cross-model consistency is −0.01 — indistinguishable from zero.\n\nThe practical translation: identity positioning and cross-model consistency are different levers on different outcomes. A brand can invest in cultural identity and move whether AI names it, without moving how consistently it does so. If the six assistants disagree about a brand, that disagreement will not close by leaning harder into identity — it is governed by something else. (Left panel: the confirmed identity-on-visibility effect. Right panel: the same identity signal, flat against consistency. Two different measurements shown side by side, not one analysis.)",
    "P2": "A zero is only worth acting on if the test could have found something. This one could. The 53 brands cleared the pre-registered minimum, and the method was precise enough to detect an effect of the size the program treats as meaningful. It detected essentially nothing — the estimate sits on zero, and its range of uncertainty stays well short of the threshold that would count as a real effect.\n\nSo the right reading is \"identity does not move consistency,\" not \"we couldn't tell.\" That distinction matters for a brand team: this is evidence to redirect spend away from identity as a consistency lever, not an inconclusive result to revisit when there's more data. The absence is the finding.",
    "P3": "Run separately, the three categories do not line up: skincare leans slightly positive (+0.14), cosmetics slightly negative (−0.17), automotive slightly negative (−0.13). The signs disagree, and all three sit close to zero. With only three categories this carries no statistical claim — it is shown to answer the obvious managerial question directly.\n\nThat question is \"fine overall, but does it hold in my category?\" The honest answer: there is no category-specific effect being averaged away into the overall zero. A real identity-to-consistency relationship hiding in one category would show the categories pointing the same way, not disagreeing in sign around zero. They disagree. There is no \"works in my category\" exception waiting to be found here.",
    "P4": "Nineteen of the 72 brands could not be scored for consistency, and which ones is telling. They are not obscure brands the models had never heard of — most were recognized by all six models. They simply were never named when the models were asked to list brands in the category. Recognized, never recalled.\n\nConsistency is about agreement in naming, so it cannot be computed where there is no naming. These brands — recognized but unnamed — fall outside what this measure can see, which is a real boundary worth stating plainly: the finding speaks to brands AI actually surfaces, not to the ones it knows but stays silent on. Closing that gap needs a different instrument than naming, and building it is on the program's roadmap.",
}

CLOSING = "The most useful thing a measurement program can hand a brand team is sometimes a lever that does not work, named precisely. Identity positioning moves whether AI surfaces a brand; it does not move how consistently AI does so across models. That is not the end of the consistency question — it is a redirection of where to look for the answer, and the program keeps looking, in public, one pre-registered phase at a time. The brands AI knows but never names are still out there, waiting for an instrument that can finally measure them."
