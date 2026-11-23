"""
Text of the brief of the combined v0.27 + v0.28 validity paper (TS-BR-v0.27-r1; v0.28 named in the title block).
Managerial register: plain findings, no hypothesis labels. Every number is a {KEY} placeholder filled by
reports/build_brief_v0_27.py from brief_v0_27_values.py (unknown key -> KeyError). Note markers are {N1}, {N2}, ...
(small_print.NoteSeq, per page).
"""

TITLE = "AI Presence did not match a commercial visibility score and is distinct from recognition memory"
KICKER = "BRIEF · CONSTRUCT VALIDITY (v0.27 AND v0.28)"
RUNNING_LABEL = "AIAS™ v0.27 and v0.28 · November 2026"

STANDFIRST = ("Two pre-registered tests asked what Presence, the programme's measure of how AI models recognise "
              "and name a brand{N1}, agrees with. It did not order brands like a commercial tool's AI Share of "
              "Voice{N2}. It is distinct from how reliably people recognise a brand; whether it is more than "
              "familiarity could not be decided{N3} with {F_N} brands.")

NUMBERS = [
    {"value": "{P_RHO}", "unit": "", "label": "Rank agreement with the commercial tool's Share of Voice",
     "source": "Falsified: under {FALS}; {CONF} needed"},
    {"value": "{R_RHO}", "unit": "", "label": "Link with how reliably people recognise a brand",
     "source": "Distinct: under {CEIL}; upper end {R_HI}"},
    {"value": "{F_RHO}", "unit": "", "label": "Link with how familiar people say a brand is",
     "source": "Undetermined: interval {F_LO} to {F_HI}"},
]

NOTES_P1 = [
    "Presence: whether each of six AI models recognises a brand as part of its category, and how often they name "
    "it in answers to open questions about the category. In Study 1 all six recognised every brand, so only "
    "naming varied; in Study 2 most brands were never named, so the score moved mostly with recognition.",
    "Study 1 (v0.27), {P_N} B2B software brands: rank correlation (Spearman; 1 is the same order, 0 none) of "
    "naming with the HubSpot AEO Grader's within-category Share of Voice: {P_RHO}, 95% interval {P_LO} to "
    "{P_HI}, adjusted p {P_PADJ}. Confirmed at {CONF} or more with p under {ALPHA}, strong at {STRONG} or more, "
    "falsified under {FALS} or if not significant.",
    "Study 2 (v0.28), {F_N} technology brands, against human norms (BRAND database): under {CEIL} counts as "
    "distinct, {BENCH} or more as reducible, in between as partial; undetermined if the 95% interval spans all "
    "three. Familiarity {F_RHO} ({F_LO} to {F_HI}); recognition {R_RHO} ({R_LO} to {R_HI}).",
]

# ---------------------------------------------------------------- page 2
KICKER_P2 = "WHAT WE FOUND AND WHAT IT MEANS"

SECTIONS = [
    ("What we found", [
        "<b>Naming did not follow the tool's Share of Voice.</b> Across {P_N} B2B software brands, how often AI "
        "answers named a brand did not order brands as the tool's Share of Voice did ({P_RHO}; {CONF} needed): "
        "Study 1's main test is falsified.",
        "<b>Recognition could not vary there.</b> All six models recognised every brand, as the plan expected "
        "(confirmed), so Study 1 tested naming only.",
        "<b>Two tool subscores did track naming.</b> In a scan registered as exploratory, naming followed the "
        "Grader's presence quality ({PQ}) and brand recognition ({BRR}), not its sentiment ({SENT}) or market "
        "competition ({MKT}). Share of Voice was fixed in advance; neither replaces it.",
        "<b>Presence is distinct from recognition memory.</b> Across {F_N} technology brands, its link with how "
        "reliably people recognise a brand in a memory test was {R_RHO}, the interval's upper end ({R_HI}) under "
        "{BENCH}: confirmed, though the interval is wide.",
        "<b>Against familiarity it is undecided.</b> The link was {F_RHO}, in the partial band as predicted, but "
        "its interval ({F_LO} to {F_HI}) spans all three bands: undetermined.",
    ]),
    ("How firm it is", [
        "Checks beside the result carry no verdict: without the {T2_NEX} brands named only in answers about "
        "cultural standing, {T2_RHO}; without Stride, a name other companies share, {ST_RHO}; neither nears "
        "{CONF}. Three planned Study 1 tests, on two tools not used, were not run. In Study 2, "
        "{DISS} brands differ by more than {Z} standard deviation between Presence and familiarity ({AMP} above, "
        "{SUP} below): a full dissociation (at least {CASES}, both ways), which shares the familiarity test's data and is not separate evidence.",
    ]),
    ("What it means for a marketer", [
        "On these brands, a dashboard's headline Share of Voice was the reading least aligned with how often AI "
        "answers name a brand in its category: a caution, not a verdict on any tool.",
    ]),
    ("How the result was reached", [
        "Each study was pre-registered and scored once. Study 1 set an earlier six-model study's answers against "
        "the free Grader, queried once for every brand; Study 2 asked six models about brands drawn at "
        "random within familiarity groups, blind to the human norms.",
    ]),
    ("What comes next", [
        "Four tests: a tool scoring a brand's share of AI answers in its category; the two subscores on new "
        "brands; a larger familiarity test in a consumer category; a test against how readily brands come to "
        "mind.",
    ]),
]

NOTES_P2 = [
    "Data: Study 1, {P_N} B2B software brands (some defunct) and the free HubSpot AEO Grader, averaged over its "
    "three engines; Study 2, {F_N} technology brands of the BRAND database (Raffaelli et al., 2025), human values "
    "frozen before any model was asked.",
    "Pre-registered at tags v0.27-prereg-r1 to r5 and v0.28-prereg-r1 and r2; results locked at "
    "v0.27-report-locked and v0.28-results-locked. Data and code: osf.io/ec6wh, folders v27 and v28 (AI Brand "
    "Presence against a Commercial Visibility Score and Human Brand Norms, AIAS™ v0.27 and v0.28).",
]

SOURCE_LINE = ("Every number in this brief is read by code from the studies' verdict files "
               "(osf/v27/v0.27_verdicts.json, osf/v28/v28_verdicts.json) and the locked scorers' decision lines; "
               "none is typed.")

DISCLOSURES = {
    "conflicts_of_interest": "{COI}",
    "held_out_brands": ("Harman International was removed by Study 2's pre-registered screen before the draw; no "
                        "other brand was held out or added."),
    "ai_use": "{AI_USE}",
    "independence": ("Self-funded. No brand was contacted, sponsored the work or saw it before publication. Third "
                     "System does not accept compensation contingent on improving a brand's AI Availability Score."),
}
