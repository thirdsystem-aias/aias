"""
v0.32 — CPC Version-Snapshot Stability
Third System™ brand-format report content module.

Pure-data module. Managerial register (P1–P5 propositional framing; NOT the
paper's H_* framing). Consumed by reports/build_report_v32.py; the builder maps
the three v0.32 managerial chart PDFs into the proposition slots:

    report_fig_01  -> P1 & P3  (standings hold weakly; instability in the largest jump — LOO inset)
    report_fig_02  -> P2       (score not reproducible to the measure's resolution)
    report_fig_03  -> P4       (emerging brands a movement to WATCH, not measured)
    (P5 is the closing recommendation — no figure.)

Same underlying findings as the SSRN paper, intentionally divergent register.
Numbers held to osf/v32/v32_verdicts.json.
"""

# ----------------------------------------------------------------------------
COVER = {
    "eyebrow": "Third System™ · AIAS™ Measurement Program · v0.32",
    "title": "When the Models Change, What Holds?",
    "subtitle": (
        "AI brand-consistency rankings tested across a major model upgrade: the broad "
        "order holds, the score itself does not reproduce, and the instability concentrates "
        "in whichever model family jumps furthest — with consequences for tracking a brand "
        "over time."
    ),
    "deck": "",
}

# ----------------------------------------------------------------------------
STANDFIRST = (
    "Generative AI increasingly decides which brands surface when a buyer asks for a "
    "recommendation — and the models doing the deciding are retired and replaced every "
    "few months. That puts a blunt question ahead of any AI-brand metric: when the model "
    "changes, does the reading change with it? We tested one consistency measure across a "
    "deliberately large model upgrade. The answer is useful, with a caution attached."
)

# ----------------------------------------------------------------------------
LEAD_DECK = (
    "An AI-availability reading earns its keep only if it tracks the brand, not the tool "
    "beneath it. To test whether one does, we held twenty-four automotive brands fixed and "
    "measured their AI-presence consistency twice — once on an older generation of the "
    "six-model panel we use, once on the current frontier — changing nothing but the models. "
    "The jump was deliberately large, to stress the measure rather than flatter it. Three "
    "findings came back, and a fourth to watch. The broad order of brands held across the "
    "upgrade, but only just. The consistency score for any given brand did not hold: it "
    "moved, on average, by more than the gap separating one brand from the next. The "
    "instability was not evenly spread — it concentrated in the single model family that "
    "made the largest version jump. And the newest electric challengers are beginning to "
    "register in AI recall, though not yet enough to move the measure."
)

# ----------------------------------------------------------------------------
# Five takeaways (paragraphs; the builder splits EXEC_SUMMARY on blank lines).
EXEC_SUMMARY = (
    "<b>Standings broadly survive an upgrade — weakly.</b> The order of brands on AI "
    "consistency holds across a model change, but the margin is thin. Read a single ranking "
    "as indicative, not settled. (P1)"
    "\n\n"
    "<b>The score does not reproduce.</b> A brand's consistency reading is not stable across "
    "a model change to within the measure's own resolution — it can move more than the "
    "spacing between brands. Don't over-read a period-to-period score change. (P2)"
    "\n\n"
    "<b>The wobble has an address.</b> Instability concentrates in whichever model family "
    "makes the largest version jump; a panel is only as stable as its most volatile member. (P3)"
    "\n\n"
    "<b>Emerging brands: watch, don't act.</b> Electric challengers are gaining AI recall "
    "under newer models but remain below the threshold this measure reads — a movement to "
    "watch, not yet a measured effect. (P4)"
    "\n\n"
    "<b>Comparability is a choice.</b> A consistency reading is comparable across periods "
    "only on a version-controlled panel — pinned, dated models migrated deliberately — or "
    "the score partly reflects the tools rather than the brands. (P5)"
)

# ----------------------------------------------------------------------------
WHAT_WE_MEASURED = (
    "We measured consistency: how steadily a brand surfaces across the different AI models a "
    "buyer might use, rather than depending on which model happens to answer. The test bed "
    "was twenty-four automotive brands — a deliberate mix of heritage names, electric "
    "challengers, mass-market makes, and discontinued marques — read across a panel of six "
    "models from three providers. We ran the full measurement twice: once on an older "
    "generation of those six models, once on the current generation, holding the brands, the "
    "questions, and everything else fixed. Only the models changed, and we made the gap "
    "between old and new deliberately large so the test would expose version sensitivity "
    "rather than hide it. One note on what “consistency” counts: it reads from how "
    "often each model names a brand unprompted across a battery of category and cultural "
    "questions; a brand the models rarely name falls below a floor and carries no reading at all."
)

# ----------------------------------------------------------------------------
PATTERNS = (
    "Four patterns came back. First, the standings broadly held: rank the brands by "
    "consistency on the old models and on the new, and the two orders largely agree — but the "
    "agreement is thin, and fragile. Second, the score itself did not hold. A given brand's "
    "consistency reading moved between old and new models by more than the typical gap "
    "separating one brand from the next, and in no consistent direction: newer models did not "
    "make brands look uniformly more or less consistent, they reshuffled which brands read as "
    "consistent. The measure is reproducible enough to rank by once, but not to track period "
    "over period. Third, the instability has an address — it concentrated in the single "
    "provider whose models made the largest version jump; remove that provider and the "
    "standings snap back into agreement. A panel is only as steady as its most volatile member. "
    "Fourth, and to watch rather than bank: the electric challengers are rising. Rivian and "
    "Lucid, recalled essentially never by the older models, began to surface under the newer "
    "ones — but not often enough to cross the floor where the measure starts reading. The "
    "direction is right; the magnitude isn't there yet."
)

# ----------------------------------------------------------------------------
LIMITATIONS = (
    "Read these within their bounds. This is one category — automotive, chosen for its spread "
    "of brand types; consistency may behave differently where the surrounding discourse is "
    "denser or thinner. It is one moment in time: we changed the models but not the calendar, "
    "so this isolates the effect of upgrading the models, not drift that would occur anyway. "
    "And it rests on the fourteen brands that carried a reading; the other ten — discontinued "
    "marques, the newest EVs, and even a mainstream name like Nissan — sat below the recall "
    "floor, a reminder that this measure tracks how often a brand is named, not how large it "
    "is. Most important to weigh: the consistency measure itself is an early version, one we "
    "are actively redefining. These results are partly a stress test of the gauge and feed "
    "that redefinition as much as they describe the market. Treat the propositions as "
    "directionally sound and the exact scores as provisional."
)

# ----------------------------------------------------------------------------
WHATS_NEXT = (
    "Three moves follow. We are redefining the consistency measure to remove a known "
    "dependence on how often a brand is recalled, and the next step is to re-run this exact "
    "old-versus-new test on the redefined version — version-robustness becomes a bar any "
    "future gauge must clear before it can be trusted over time. We will widen the test beyond "
    "automotive, to see whether the partial, provider-dependent stability here holds in "
    "categories with denser or sparser discourse. And we will keep watching the challengers "
    "below the floor: a sub-threshold rise, tracked deliberately, is the kind of signal that "
    "becomes a measured shift before competitors notice it. For anyone using an AI-availability "
    "reading operationally, the immediate move is the fifth proposition — control the panel: "
    "pin the exact model versions you measure on, migrate them on a deliberate schedule rather "
    "than letting them update underneath you, and record which versions produced each reading. "
    "Otherwise a change in a brand's score is partly a change in the instrument."
)

# ----------------------------------------------------------------------------
# Proposition scoreboard — plain-language status (NEVER CONFIRMED/FALSIFIED).
HYPOTHESIS_SCORING = [
    {"id": "P1", "proposition": "Standings hold across a model upgrade",
     "verdict": "Holds — weakly",
     "basis": "Old-vs-new rank agreement 0.71 — clears the bar, but only just, and it leans on two of the three providers."},
    {"id": "P2", "proposition": "The score reproduces across a model upgrade",
     "verdict": "Does not hold",
     "basis": "A brand's score moved 0.077 on average — more than 0.069, the gap separating brands — with no net direction."},
    {"id": "P3", "proposition": "Instability is spread across the panel",
     "verdict": "No — it concentrates in the largest jump",
     "basis": "Drop the largest-jump provider and agreement rises to 0.82; drop either other and it falls to about 0.5."},
    {"id": "P4", "proposition": "Emerging brands register on the measure",
     "verdict": "Not yet — watch",
     "basis": "Rivian and Lucid gained AI recall under newer models but stayed below the reading floor — no crossing."},
    {"id": "P5", "proposition": "A reading is comparable over time as-is",
     "verdict": "No — comparability needs a version-controlled panel",
     "basis": "The score moves with the panel vintage; comparability is recoverable only by pinning and migrating versions deliberately."},
]

# ----------------------------------------------------------------------------
HYPOTHESIS_DETAILS = {
    "P1": (
        "Ranked by consistency, the brands sit in nearly the same order on the old and new "
        "models (rank correlation 0.71). But the margin is slim and the result leans on two of "
        "the three providers; the third's models, taken alone, would put the orders in "
        "substantial disagreement."
    ),
    "P2": (
        "Across the brands that carried a reading, the average score moved by 0.077 between old "
        "and new models — larger than 0.069, the mark for half the spread between brands. The "
        "moves had no net direction (they averaged near zero): newer models reshuffled which "
        "brands read as consistent rather than raising or lowering all of them."
    ),
    "P3": (
        "Removing the provider whose models jumped furthest — an older-to-current leap spanning "
        "a full model-family change — raised the ranking agreement from 0.71 to 0.82; removing "
        "either other provider dropped it to about 0.5. The instability lives in the largest jump."
    ),
    "P4": (
        "Rivian and Lucid were recalled essentially never by the older models and began to be "
        "named by the newer ones — Rivian's average mentions rose from zero to roughly "
        "two-thirds of one across the panel. Real movement, but below the threshold at which "
        "the measure begins to read, so it registers as no change."
    ),
    "P5": (
        "Because the score moves with the models (P2) and the movement tracks the largest "
        "version jump (P3), a reading taken on one panel vintage is not directly comparable to "
        "one taken on another. Comparability is recoverable only by fixing the panel's versions "
        "and migrating them deliberately."
    ),
}

# ----------------------------------------------------------------------------
CLOSING = (
    "The headline is not that AI brand-consistency is stable across model upgrades, nor that "
    "it collapses. It is that the standings survive while the scores do not — and the "
    "difference governs how the reading should be used. As a one-time ranking, the measure "
    "separates brands meaningfully. As a tracker, it cannot yet tell a real change in a brand "
    "from the turnover of the models beneath it, unless the panel is held still. For now, that "
    "is the operative instruction: pin the versions, migrate them on your terms, and record "
    "what produced each reading. The gauge is being sharpened; until it is, treat the order as "
    "signal and the scores as provisional — and don't mistake the instrument moving for the "
    "market moving."
)
