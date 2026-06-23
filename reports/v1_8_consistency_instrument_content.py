"""
v1.8 — CPC Consistency Instrument Redesign · brand-format report content (managerial register).

Third System™ brand-format report for the AIAS™ Measurement Program. Pure-data
content module consumed by reports/build_report_v1_8.py (ReportLab + pypdf two-pass).
Managerial register: P1–P5 propositional framing. The academic paper carries the
H_* hypotheses; this report does not. Same findings, different audience.

DEPLOY TARGET: reports/v1_8_consistency_instrument_content.py
STRUCTURE NOTE: the 11 attributes follow the documented content contract and preserve
the v1.7 fork base's keys/types exactly, so build_report_v1_8.py consumes them unchanged
(COVER dict; PATTERNS list[{label,text}]; HYPOTHESIS_SCORING list[{id,proposition,status}];
HYPOTHESIS_DETAILS list[{id,text}]; the rest strings). Prose is deliberately symbol-light
(no phi/rho glyph, no subscripts) to sit cleanly in Akkurat Pro; correlations are plain
digits. Voice is validated, not failed: the redesign holds. Every figure traces to sealed
v1.8-results-r1 (commit 85d2202).
"""

# 1. COVER — title block
COVER = {
    "title": "How Evenly, Not Just How Much",
    "kicker": "A pre-registered redesign of AI presence consistency, and why it now "
              "reads on its own, apart from how present a brand is.",
    "program_line": "AIAS™ Measurement Program · Methodology v1.8 · Third System™",
}

# 2. STANDFIRST
STANDFIRST = (
    "The programme set out to add a second dimension to AI brand presence: not how "
    "present a brand is, but how evenly. An earlier attempt collapsed into the first. "
    "At the mention volumes today's models produce, the evenness of a brand's presence "
    "could not be told apart from its level. The redesigned measure separates them, and "
    "evenness now reads on its own."
)

# 3. LEAD_DECK
LEAD_DECK = (
    "Brand teams face a widening menu of AI-visibility metrics, among them scores that "
    "claim to measure the consistency or stability of a brand's presence across models "
    "and prompts. An earlier study found that the obvious way of building such a measure "
    "restated presence rather than adding to it. This study redesigns it. Under a locked, "
    "pre-registered protocol, the new measure moves independently of presence level, "
    "reaches brands the old one could not score, and tells how evenly a brand surfaces "
    "apart from where it surfaces. Consistency becomes a second reading, not a second "
    "name for the first."
)

# 4. EXEC_SUMMARY
EXEC_SUMMARY = (
    "Consistency was defined as the evenness of a brand's presence across a fixed "
    "six-model panel and tested against a requirement set in advance: to count as a "
    "measure, it had to carry information that presence does not. An earlier version "
    "failed that test. It rose with presence in every category, at a pooled rank "
    "correlation of 0.77, because at low mention counts the spread of a count is "
    "governed by its average, so a score built from that spread restates the average. "
    "The redesigned measure removes the coupling by construction. Instead of dividing a "
    "brand's spread by its average, it weighs the spread the models actually show "
    "against the spread chance alone would produce, which cancels the level term. On the "
    "same brands, its correlation with presence falls to 0.091, far below the line fixed "
    "beforehand, against 0.682 for the measure it replaces. It also reaches further: "
    "twenty-nine brands recalled too rarely for the old measure to score at all now "
    "carry a reading, with no failure at the opposite, saturated end. A companion measure "
    "reads where a brand surfaces rather than how much, and moves separately enough to "
    "count as a distinct facet. Consistency is now a measurable second component of AI "
    "presence. The next step is combining the two readings into one; until then, a "
    "brand's evenness can be read as genuine information about its AI presence, no longer "
    "a restatement of its level."
)

# 5. WHAT_WE_MEASURED
WHAT_WE_MEASURED = (
    "The redesigned measure was tested not on fresh data but on an archive the programme "
    "had already collected and frozen: five categories, headphones, skincare, cosmetics, "
    "automotive, and premium spirits, each put to the same panel of six models, one "
    "hundred twelve brands in all. Holding the data fixed puts the test on the instrument "
    "rather than the brands, since the same records the earlier measure failed on were "
    "re-read under the redesign. For each brand, the six models' mention counts were set "
    "against what chance alone would produce if every model surfaced the brand at one "
    "underlying rate; a brand whose models agree beyond chance reads as consistent, one "
    "whose models disagree as inconsistent. A rule fixed before any value was computed "
    "required the new measure to move independently of presence, the test the earlier "
    "measure failed. Two companion readings were specified alongside it: one for where a "
    "brand surfaces rather than how evenly, and one for graded recognition depth, the "
    "second held for a later collection because the archived recognition signal is "
    "recorded only as yes or no."
)

# 6. PATTERNS
PATTERNS = [
    {
        "label": "Evenness now reads on its own",
        "text": (
            "The redesigned measure no longer tracks how present a brand is. Across the "
            "archive its rank correlation with presence level is 0.091, close to none, "
            "against 0.682 for the measure it replaces, read on the very same brands. The "
            "earlier coupling was not a fact about brands but about how the measure was "
            "built; rebuilt to weigh each brand's spread against what chance alone would "
            "produce, it carries no level term, and evenness becomes a reading in its own "
            "right."
        ),
    },
    {
        "label": "It reaches the brands the old measure could not score",
        "text": (
            "Twenty-nine brands are recalled so rarely that the earlier measure could "
            "return nothing for them, and these are exactly the brands a stability "
            "reading is most useful for. The redesigned measure scores all of them, and "
            "does so without breaking at the opposite extreme, where a brand is named by "
            "every model every time. The reading now spans the full range of presence, "
            "sparse to saturated, rather than only the well-recalled middle."
        ),
    },
    {
        "label": "How evenly and where are different questions",
        "text": (
            "A brand can be surfaced at a steady rate across the panel yet in scattered "
            "places, or named in the same places by models that disagree on how often. "
            "The redesign reads the first; a companion measure reads the second; and the "
            "two move apart enough, a correlation of 0.403, well below the line for "
            "redundancy, that nine brands sit consistent on one facet and inconsistent on "
            "the other. How much and where are genuinely two readings, not one."
        ),
    },
    {
        "label": "The reading is stable across measurements",
        "text": (
            "Re-measured at a second wave, the brands' order on the new measure holds at "
            "a rank correlation of 0.645, moderate, and reported as such rather than "
            "overstated. The ordering is not an artefact of a single draw, though one "
            "re-measurement is not yet the evidence a high-stakes index would need. "
            "Enough to trust the reading, not yet enough to stop checking it."
        ),
    },
]

# 7. LIMITATIONS
LIMITATIONS = (
    "The test rests on an archive of five categories, re-read rather than freshly "
    "collected, and read in three overlapping views rather than three independent ones; "
    "two of the views coincide on the same brands, so the headline figure summarizes the "
    "evidence rather than replicating it. The counts behind the secondary findings are "
    "modest: the coverage gain rests on twenty-nine brands, the split between how much "
    "and where on nine. The archived surfacing was recorded by three different methods "
    "across the categories, uniform within each but not across them, which the design "
    "accounts for and a single-method collection would tighten. Graded recognition depth "
    "could not be scored, because the archived recognition signal is yes or no only, and "
    "is held for a later collection. And the measure validated here is one component of a "
    "larger score, not the whole; its soundness does not yet establish the soundness of "
    "any combination."
)

# 8. WHATS_NEXT
WHATS_NEXT = (
    "With a measure of how evenly that holds and a measure of where beside it, the open "
    "task is composition: combining the two into a single consistency reading without "
    "letting the level dependence back in, and settling how they trade off where they "
    "disagree. That combination is the next pre-registered step. Graded recognition depth "
    "rejoins the programme at the first collection that records more than yes or no. "
    "Beyond consistency, the remaining parts of the score, ranking, coverage, grounding, "
    "and sentiment, each face the same build-and-validate arc this phase completed here "
    "before any of them enters the composite. The structure work the earlier, broken "
    "measure could not support is reopened now that a sound one exists."
)

# 9. HYPOTHESIS_SCORING — managerial propositions with status
HYPOTHESIS_SCORING = [
    {"id": "P1",
     "proposition": "The evenness of a brand's AI presence can now be measured on its "
                    "own, apart from how present the brand is.",
     "status": "Established"},
    {"id": "P2",
     "proposition": "The redesigned measure reads the sparsely recalled brands the "
                    "earlier one could not score, where a stability reading matters most.",
     "status": "Established"},
    {"id": "P3",
     "proposition": "How evenly a brand surfaces and where it surfaces are distinct "
                    "readings; a brand steady on one can be scattered on the other.",
     "status": "Established"},
    {"id": "P4",
     "proposition": "The reading holds across re-measurement: stable enough to track a "
                    "brand over time, not yet stable enough to stand as a high-stakes "
                    "single number.",
     "status": "Observed"},
    {"id": "P5",
     "proposition": "Consistency is a validated component, but the score that combines "
                    "it with the others is not yet built; read one consistency figure as "
                    "an input, not a finished verdict.",
     "status": "Open"},
]

# 10. HYPOTHESIS_DETAILS — elaboration per proposition
HYPOTHESIS_DETAILS = [
    {"id": "P1",
     "text": (
         "Read on the same brands the earlier measure restated presence on, the "
         "redesigned measure's correlation with presence level is 0.091, against 0.682 "
         "before. The difference is the construction, not the data: weighing each brand's "
         "spread against what chance would produce cancels the level term that dividing "
         "by the average had carried. A brand's evenness is now a separate lever from its "
         "presence."
     )},
    {"id": "P2",
     "text": (
         "Twenty-nine brands surface too rarely for a spread-over-average measure to "
         "return anything, and rarely surfaced brands are precisely where a stability "
         "reading earns its keep. The redesign scores every one of them, and holds at the "
         "other extreme too, where a brand is named by every model every time. The "
         "reading spans sparse to saturated rather than only the comfortable middle."
     )},
    {"id": "P3",
     "text": (
         "Two brands with the same evenness across the panel can occupy the same handful "
         "of prompts or scatter across many. The redesign reads how evenly; a companion "
         "reads where. They move together loosely enough, a correlation of 0.403, below "
         "the line at which one would make the other redundant, that nine brands land "
         "consistent on one and inconsistent on the other. Carrying both keeps a real "
         "distinction that a single number would erase."
     )},
    {"id": "P4",
     "text": (
         "Re-measured at a second wave, the brands' order on the new measure recurs at a "
         "rank correlation of 0.645. That is moderate, and stated as moderate: enough to "
         "say the ordering is not an accident of one measurement, short of the "
         "reliability a published single-number index would demand. The reading is "
         "trustworthy to track, and still worth re-checking."
     )},
    {"id": "P5",
     "text": (
         "The redesign makes consistency a sound input, not a finished score. Combining "
         "it with the other parts of AI presence, and with its own positional companion, "
         "is a separate problem with its own test, still ahead. Until that composite is "
         "built and validated, a consistency figure should be read as one well-made "
         "reading among several, not as a brand's standing on its own."
     )},
]

# 11. CLOSING
CLOSING = (
    "The redesigned measure was specified, locked, and tested in the open against the "
    "same rule the earlier one failed, and this time it held. That is the method "
    "compounding: a failure that named exactly what a sound measure had to do, followed "
    "by a measure built to do it. Consistency is now a second reading of AI presence "
    "rather than a second name for the first, and the programme moves from repairing an "
    "instrument to assembling a score from instruments that work."
)
