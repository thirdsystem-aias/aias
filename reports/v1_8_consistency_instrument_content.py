# NOTE: cloned from v1_7_cpc_consistency_content.py on phase scaffold.
# All COVER, STANDFIRST, LEAD_DECK, EXEC_SUMMARY, PATTERNS,
# LIMITATIONS, WHATS_NEXT, HYPOTHESIS_DETAILS, CLOSING text
# must be re-written for the v1.8 consistency instrument
# substrate. Do not ship this file as-is.

"""
v1.8 — CPC Consistency Methodology Lock · brand-format report content (managerial register).

Third System™ brand-format report for the AIAS™ Measurement Program. Pure-data
content module consumed by reports/build_report_v1_8.py (ReportLab + pypdf two-pass).
Managerial register: P1–P5 propositional framing. The academic paper carries the
H_CPC_* hypotheses; this report does not. Same findings, different audience.

DEPLOY TARGET: reports/v1_8_consistency_instrument_content.py
STRUCTURE NOTE: the 11 attributes below follow the documented content contract.
Reconcile exact keys/types against the prior phase's reports/*_content.py that
build_report_v1_8.py imports, and align the shapes if the builder expects different
ones. Prose is deliberately symbol-light (no rho glyph, no subscripts) to sit
cleanly in Akkurat Pro; the recognition–recall en-dash is the only special mark.
"""

# 1. COVER — title block
COVER = {
    "title": "Measuring Presence Twice",
    "kicker": "A pre-registered test of AI presence consistency, and why it could "
              "not be measured as proposed.",
    "program_line": "AIAS™ Measurement Program · Methodology v1.8 · Third System™",
}

# 2. STANDFIRST
STANDFIRST = (
    "The programme set out to add a second dimension to AI brand presence: not how "
    "present a brand is, but how evenly. The dimension collapsed into the first. At "
    "the mention volumes today's models produce, the evenness of a brand's AI "
    "presence cannot be told apart from its level."
)

# 3. LEAD_DECK
LEAD_DECK = (
    "Brand teams face a widening menu of AI-visibility metrics, among them scores "
    "that claim to measure the consistency or stability of a brand's presence across "
    "models and prompts. This study tested whether such a measure carries "
    "information that presence does not. Under a locked, pre-registered protocol, it "
    "does not. The reason is arithmetic rather than incidental, and it applies to any "
    "consistency score built the same way."
)

# 4. EXEC_SUMMARY
EXEC_SUMMARY = (
    "Consistency was defined as the evenness of a brand's recall across a fixed "
    "six-model panel and tested against a requirement set in advance: to count as a "
    "new measure, it had to carry information beyond presence. It did not. Consistency "
    "rose with presence in every category tested, at a pooled rank correlation of "
    "0.77, well above the threshold fixed beforehand. The cause is a property of small "
    "counts. Where mentions are few, the spread of a count is governed by its average, "
    "so a score built from that spread restates the average. A second pattern surfaced "
    "along the way: many brands that every model recognizes draw almost no spontaneous "
    "mention, a gap widest among prestige labels. No consistency measure is adopted on "
    "this evidence. The measure returns for redefinition, and practitioners should read "
    "consistency scores of this construction as presence under another name."
)

# 5. WHAT_WE_MEASURED
WHAT_WE_MEASURED = (
    "Twenty-four brands in each of three categories (skincare, cosmetics, and "
    "automotive) were put to a fixed panel of six language models. Each model was "
    "asked in a category framing and a cultural framing, and a brand's recall was the "
    "count of mentions it drew. A consistency score was formed from the spread of "
    "those counts across the six models, higher where a brand read evenly and lower "
    "where it scattered. A rule fixed before any score was computed required the "
    "consistency score to move independently of presence; a close correlation would "
    "mark it as a restatement rather than a measure. Defunct brands were included as a "
    "control and were expected to return no reading."
)

# 6. PATTERNS
PATTERNS = [
    {
        "label": "Consistency followed presence",
        "text": (
            "In every category, brands with stronger presence scored as more "
            "consistent and brands with weaker presence as less so. Pooled across the "
            "three categories the rank correlation was 0.77, and it was positive in "
            "each one. The two quantities moved together rather than apart."
        ),
    },
    {
        "label": "The link is arithmetic, not incidental",
        "text": (
            "At the mention counts the panel produced, the spread of a count is "
            "governed by its average: rare mentions vary little in absolute terms, "
            "frequent ones more. A score built from spread divided by average "
            "therefore tracks the average. The coupling is a feature of counting at "
            "low volumes, so it would recur for any brand set and any consistency "
            "score of the same construction, including those sold by visibility tools."
        ),
    },
    {
        "label": "Known is not the same as named",
        "text": (
            "Many brands recognized by every model in the panel drew almost no "
            "spontaneous mention when a buyer's question invited one. The gap was "
            "widest for prestige and heritage labels; functional and category-defining "
            "brands held the recalled set. Recognition proved necessary but not "
            "sufficient for presence in AI answers."
        ),
    },
    {
        "label": "Absent brands read as absent",
        "text": (
            "Defunct brands drew no recall and returned no consistency score, as the "
            "design intended. A brand with no presence yields no reading rather than a "
            "misleading one."
        ),
    },
]

# 7. LIMITATIONS
LIMITATIONS = (
    "The finding is bounded to the three categories for which the panel measure "
    "exists, and to the mention volumes the current design produces. A denser set of "
    "prompts would raise those volumes and might loosen the coupling, so the result "
    "states that the measure fails at present volumes, not that presence stability is "
    "unmeasurable in principle. Recognition stood at its ceiling for every scored "
    "brand, which prevented a direct test against recognition alone; the conclusion "
    "rests instead on the measured coupling between the consistency score and mention "
    "level, which is unambiguous."
)

# 8. WHATS_NEXT
WHATS_NEXT = (
    "Consistency returns for redefinition on a measure that is independent of level at "
    "the volumes a model panel produces. Candidate measures exist and will each face "
    "the same independence test before any is adopted. The recognition–recall gap is "
    "taken up as a line of work in its own right, since it bears on how a brand known "
    "to AI becomes a brand named by it. No consistency score is shipped until a "
    "measure clears the test."
)

# 9. HYPOTHESIS_SCORING — managerial propositions with status
HYPOTHESIS_SCORING = [
    {"id": "P1",
     "proposition": "At current mention volumes, the consistency of a brand's AI "
                    "presence cannot be separated from its level.",
     "status": "Established"},
    {"id": "P2",
     "proposition": "Consistency or variance scores computed as spread over mention "
                    "level restate presence; they add no second diagnostic.",
     "status": "Established"},
    {"id": "P3",
     "proposition": "Recognition by AI is not recall by AI; a brand every model knows "
                    "can still go unnamed.",
     "status": "Established"},
    {"id": "P4",
     "proposition": "The recognition–recall gap is widest for prestige and heritage "
                    "brands; functional brands tend to own recall.",
     "status": "Observed"},
    {"id": "P5",
     "proposition": "No defensible measure of AI presence stability exists yet; treat "
                    "any AI-consistency score as presence relabelled until one passes "
                    "an independence test.",
     "status": "Open"},
]

# 10. HYPOTHESIS_DETAILS — elaboration per proposition
HYPOTHESIS_DETAILS = [
    {"id": "P1",
     "text": (
         "Across skincare, cosmetics, and automotive, the consistency score and the "
         "presence measure moved together at a pooled rank correlation of 0.77. A "
         "brand's evenness across models is, in practice, a function of how present it "
         "is. There is no separate consistency lever to pull."
     )},
    {"id": "P2",
     "text": (
         "The correlation is not a quirk of these brands. Spread over level is "
         "mechanically tied to level when counts are small, which they are throughout "
         "model output. Any score of this construction, whoever supplies it, carries "
         "the same defect: it reports presence a second time."
     )},
    {"id": "P3",
     "text": (
         "Recognition and recall came apart in the data. A brand can be identified by "
         "every model in the panel and still almost never be offered when a category "
         "or cultural question is asked unprompted. In AI-mediated discovery the second "
         "is what reaches the buyer."
     )},
    {"id": "P4",
     "text": (
         "The brands most exposed are those whose standing rests on being known. "
         "Prestige and heritage labels were recognized everywhere and recalled rarely, "
         "while functional and category-defining brands occupied the recalled set. An "
         "awareness-led position is the one most at risk when answers, not shelves, do "
         "the surfacing."
     )},
    {"id": "P5",
     "text": (
         "Stability of AI presence may yet be measurable, but not as specified here. "
         "Until a measure demonstrates independence from presence at realistic mention "
         "volumes, a consistency score should be read as presence under another label, "
         "and bought or built accordingly."
     )},
]

# 11. CLOSING
CLOSING = (
    "The measure was specified, locked, and tested in the open, and it failed a rule "
    "set before the data were seen. That is the method working, not faltering. The "
    "result narrows what a consistency measure can be, warns against scores already on "
    "sale, and leaves the programme with a sharper question than the one it began with."
)
