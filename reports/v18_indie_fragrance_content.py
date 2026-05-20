"""
v18_indie_fragrance_content.py — v0.18 brand-format report content

Pre-reg lock:    v0.18-prereg-r1 @ commit 183386c
Branch:          v0.18-il-gradient
Consumed by:     reports/build_report_v18.py (ReportLab + pypdf two-pass)

Brand tokens:    brand/third_system_brand.json (Indigo #37237B primary)
Typography:      ReportLab + Akkurat Pro
                 Subscripts use <sub>N</sub> markup (Akkurat lacks Unicode ₁/₂)
                 NBSP \\u00a0 wraps arrow connectors to prevent line-splits

Pre-acquisition state:
  Pre-acquisition prose fully populated for: COVER, REPORT_METADATA,
  EXECUTIVE_SUMMARY (lede + what_we_tested), SECTIONS 01_substrate
  and 02_methods, BACK_MATTER.
  Marked [TBD-VERDICT] in: EXECUTIVE_SUMMARY (what_we_found,
  what_this_means), SECTIONS 03_findings_recognition, 04_findings_recall,
  05_findings_dissociation, 06_verdict, 07_implications.
  Marked [TBD-DEVIATIONS] in: SECTIONS 08_methodology_notes (DEVIATIONS log).
"""

# ============================================================
# REPORT METADATA — for build_report_v18.py header/footer plumbing
# ============================================================

REPORT_METADATA = {
    "phase": "v0.18",
    "substrate": "Indie Fragrance — IL-Gradient",
    "version_label": "v0.18",
    "pre_reg_tag": "v0.18-prereg-r1",
    "lock_commit": "183386c",
    "branch": "v0.18-il-gradient",
    "ssrn_abstract_id": None,  # backfill after SSRN submission
    "osf_url": "https://osf.io/ec6wh/v18/",
    "github_url": "https://github.com/thirdsystem-aias/aias",
    "report_date": "2026-05-XX",  # locks at PDF build time
}


# ============================================================
# COVER — title page content
# ============================================================

COVER = {
    "publisher_mark": "Third\u00a0System™",
    "series_title": "AIAS™ Presence Measurement Protocol",
    "phase_designation": "Phase v0.18",
    "substrate_label": "Indie Fragrance — IL-Gradient",
    "report_title": (
        "Identity-Load Moderator Test and "
        "Recognition\u00a0×\u00a0Recall Dissociation Generalization"
    ),
    # Interpretive subtitle locks post-verdict (cf. v0.17 pattern); placeholder for now
    "interpretive_subtitle": "[TBD-VERDICT — locks post-acquisition]",
    "author_block": (
        "Pablo Ulpiano González Castro\n"
        "School of Visual Arts, MPS Branding Program (primary academic affiliation)\n"
        "Third\u00a0System™ (research entity)"
    ),
    "deposit_line": (
        "Pre-registered at osf.io/ec6wh/v18/  ·  "
        "git tag v0.18-prereg-r1 @ commit 183386c"
    ),
    "trademark_line": "AIAS™ and Third\u00a0System™ are trademarks of the research program.",
}


# ============================================================
# EXECUTIVE SUMMARY — front-matter brief for managerial audience
# ============================================================

EXECUTIVE_SUMMARY = {
    "lede": (
        "AI Availability — the brand-level probability of retrieval by an AI "
        "intermediary — is now measurable. The AIAS™ Presence Measurement Protocol "
        "operationalizes it. Phase v0.18 tests two questions on a single substrate: "
        "whether Identity Load moderates AI Availability across categories, and "
        "whether the Recognition\u00a0×\u00a0Recall dissociation observed in the v0.17 "
        "Iwachu case generalizes beyond a cross-cultural substrate to a same-language one. "
        "Both questions are consequential for the canonical methodology that AIAS 1.0 will ship."
    ),
    "what_we_tested": (
        "Indie fragrance, panel of 24 brands across three cells stratified by Identity Load: "
        "mass-prestige (medium IL) → designer-niche (medium-high IL) → indie/artisan (high IL). "
        "Six-slot reference panel of frontier language models. Phase A measures Recognition "
        "(can the model anchor the brand to the category at all). Phase B measures Recall "
        "across three retrieval frames (niche / independent / perfumistas). All hypotheses, "
        "panel composition, decision rules, and verdict thresholds locked ex-ante at "
        "commit 183386c on git tag v0.18-prereg-r1."
    ),
    "what_we_found": "[TBD-VERDICT — 2–3 sentence finding summary, fills after score_v18.py emits.]",
    "what_this_means": "[TBD-VERDICT — 2–3 sentence implication summary for brand teams and the measurement protocol.]",
}


# ============================================================
# SECTIONS — body content; each item is one section in the PDF
# ============================================================

SECTIONS = [
    # ----------------------------------------------------------------
    # 01 — Substrate (pre-writable)
    # ----------------------------------------------------------------
    {
        "id": "01_substrate",
        "title": "The substrate: why indie fragrance, why now",
        "chart_slot": None,
        "body": [
            (
                "Two previous phases left the Identity-Load moderator hypothesis at "
                "AMBIGUOUS. v0.16 (kitchen knives, medium IL) returned PARTIAL. v0.17 "
                "(premium kitchenware, medium IL) returned FALSIFIED — but on panel "
                "inadequacy, not on substantive moderator failure. The two legs do not "
                "converge to a verdict, and v0.18 is the deciding third leg."
            ),
            (
                "Fragrance is the cleanest available high-IL substrate. Fragrance "
                "selection is itself part of what the purchase accomplishes; "
                "perfumistas occupy a connoisseur community with its own vocabulary; "
                "small-house identity is part of the brand's signal. Within indie "
                "fragrance, three Identity-Load tiers stratify cleanly on the "
                "consumer-discovery surface: mass-prestige houses with iconic "
                "signature-scent roles (medium IL); designer-niche houses with "
                "curatorial signaling (medium-high IL); indie and artisan houses "
                "where discovery is bound to the brand's small-house identity "
                "(high IL)."
            ),
            (
                "The substrate is entirely English-language-anchored. v0.17's "
                "Japanese cell introduced a cross-cultural LLM-coverage confound "
                "that this design removes. The three cells compete on equal "
                "training-data terms, and any Identity-Load gradient signal is "
                "isolated from language-substrate variance."
            ),
            (
                "If Identity Load moderates AI Availability, the within-phase "
                "Regime\u00a04 signature should strengthen monotonically from "
                "Cell\u00a0C through Cell\u00a0A to Cell\u00a0B."
            ),
        ],
    },

    # ----------------------------------------------------------------
    # 02 — Methods summary (pre-writable)
    # ----------------------------------------------------------------
    {
        "id": "02_methods",
        "title": "What we measured, how we locked it",
        "chart_slot": None,
        "body": [
            (
                "Twenty-four brands, eight per cell. The pre-floor of n\u00a0=\u00a024 "
                "absorbs up to fifty percent attrition while still clearing the C1 "
                "panel-adequacy floor of n\u00a0≥\u00a012 — the lesson v0.17 paid for "
                "with a thirty-one percent attrition and a FALSIFICATION on inadequacy."
            ),
            (
                "Reference panel: claude-opus-4-5, claude-sonnet-4-5, gpt-4o, "
                "gpt-4o-mini, gemini-2.5-flash, gemini-2.5-flash-lite. Same "
                "six-slot panel as v0.16 and v0.17. Provider model substitutions "
                "documented in the DEVIATIONS log."
            ),
            (
                "Phase\u00a0A probes Recognition — does the model anchor each brand "
                "to the category at all (C_P\u00a0∈\u00a00..6, one point per model)? "
                "Phase\u00a0B probes Recall through three category-anchored frames "
                "(niche, independent, perfumistas) — eighteen observations per brand. "
                "Phase\u00a0D scoring (Spearman ρ between Recognition and Recall, "
                "within-cell at n\u00a0≥\u00a05) is planned from the start, not "
                "conditional on verdict resolution."
            ),
            (
                "Three hypotheses are pre-registered as orthogonal, operating at "
                "three scopes: within-phase (Regime\u00a04 signature on this "
                "substrate), three-leg joint (Identity-Load moderator across "
                "v0.16/v0.17/v0.18), and methodological generalization "
                "(Recognition\u00a0×\u00a0Recall dissociation against the "
                "v0.17 Iwachu anchor)."
            ),
            (
                "Lock state: every panel choice, threshold, decision rule, and "
                "verdict matrix is committed at hash 183386c and tagged "
                "v0.18-prereg-r1 before any acquisition. The lock artifact lives "
                "at osf.io/ec6wh/v18/."
            ),
        ],
    },

    # ----------------------------------------------------------------
    # 03 — Findings: Recognition (Phase A) [TBD-VERDICT]
    # ----------------------------------------------------------------
    {
        "id": "03_findings_recognition",
        "title": "Recognition: do the models know who these brands are?",
        "chart_slot": "chart_02_cell_attrition.pdf",
        "body": [
            "[TBD-VERDICT — Phase A C_P score distribution per cell.]",
            "[TBD-VERDICT — Pivot anchoring outcomes per cell; cascade history.]",
            "[TBD-VERDICT — Brands clearing the dissociation C_P floor (≥ 5/6) feeding Phase B.]",
            "[TBD-VERDICT — Interpretive paragraph: what the recognition profile says about LLM training-data coverage of the IL-gradient substrate.]",
        ],
    },

    # ----------------------------------------------------------------
    # 04 — Findings: Recall (Phase B) [TBD-VERDICT]
    # ----------------------------------------------------------------
    {
        "id": "04_findings_recall",
        "title": "Recall: which brands do the models surface unprompted?",
        "chart_slot": "chart_01_mention_rate_distribution.pdf",
        "body": [
            "[TBD-VERDICT — Per-cell Phase B mention rate distributions.]",
            "[TBD-VERDICT — Cross-frame divergence: how much does the q1 / q2 / q3 lexical anchor matter?]",
            "[TBD-VERDICT — Cell-internal sensitivity: does Cell C split into icon-tier vs. mainstream-tier sub-clusters?]",
            "[TBD-VERDICT — Interpretive paragraph: does the mention-rate signature strengthen monotonically across the IL gradient as the moderator hypothesis predicts?]",
        ],
    },

    # ----------------------------------------------------------------
    # 05 — Findings: Dissociation (Recognition × Recall) [TBD-VERDICT]
    # ----------------------------------------------------------------
    {
        "id": "05_findings_dissociation",
        "title": "Dissociation: when recognition doesn't predict recall",
        "chart_slot": "chart_03_dissociation_scatter.pdf",
        "body": [
            (
                "The v0.17 Iwachu case showed Phase\u00a0A C_P\u00a0=\u00a06/6 "
                "alongside Phase\u00a0B mention rate\u00a0=\u00a00/18 — perfect "
                "recognition, zero recall. A single anchor is not yet a regularity. "
                "v0.18 is the first test of whether the pattern generalizes beyond "
                "the cross-cultural Japanese-cell substrate."
            ),
            "[TBD-VERDICT — Brands in the v0.18 panel satisfying the Iwachu-pattern threshold (C_P ≥ 5/6 ∧ mentions ≤ 2/18).]",
            "[TBD-VERDICT — Per-cell distribution: cross-cell generalization, cell-clustered, or absent?]",
            "[TBD-VERDICT — If zero cases: pooled Spearman ρ between Recognition and Recall, with bootstrap 95% CI; routes to NARROWED or UNDETERMINED per pre-reg §5.2.]",
        ],
    },

    # ----------------------------------------------------------------
    # 06 — Three-orthogonal verdict [TBD-VERDICT]
    # ----------------------------------------------------------------
    {
        "id": "06_verdict",
        "title": "Three verdicts, three scopes",
        "chart_slot": None,
        "body": [
            "**H_Regime4_indie_fragrance (within-phase):** [TBD-VERDICT]",
            "**H_IdentityLoad_moderator (three-leg joint, v0.16\u00a0×\u00a0v0.17\u00a0×\u00a0v0.18):** [TBD-VERDICT]",
            "**H_Recognition\u00a0×\u00a0Recall_dissociation_generalization (methodological):** [TBD-VERDICT]",
            "[TBD-VERDICT — Brief reading of the joint signal: substantive theory layer + methodological construct layer.]",
        ],
    },

    # ----------------------------------------------------------------
    # 07 — Implications [TBD-VERDICT]
    # ----------------------------------------------------------------
    {
        "id": "07_implications",
        "title": "What this means",
        "chart_slot": None,
        "body": [
            "**For the substantive theory.** [TBD-VERDICT — implication of the joint H_IdentityLoad_moderator verdict for the three-system framework.]",
            "**For the canonical methodology.** [TBD-VERDICT — implication of the dissociation generalization verdict for v1.4's multi-component construct as it ships in AIAS 1.0.]",
            "**For brand teams operating in mediated categories.** [TBD-VERDICT — translation of the verdict into a managerial-audience reading: what changes about how brand teams should think about AI-mediated retrieval in their own category.]",
            "**For v0.19 and beyond.** [TBD-VERDICT — forward-looking note on what v0.19 should test, if any verdict routes to deferred resolution.]",
        ],
    },

    # ----------------------------------------------------------------
    # 08 — Methodology notes & DEVIATIONS [TBD-DEVIATIONS]
    # ----------------------------------------------------------------
    {
        "id": "08_methodology_notes",
        "title": "Methodology notes and deviations",
        "chart_slot": None,
        "body": [
            (
                "Full methodology specification is at osf.io/ec6wh/v18/ "
                "(PRE_REGISTRATION_v0_18.md). Canonical protocol citation chain: "
                "v1.2 (SSRN\u00a06761698), v1.3 (SSRN\u00a06797679), "
                "v1.4 (SSRN\u00a06799479). Foundational reference: AI\u00a0Availability "
                "— A\u00a0Third\u00a0System in Brand Availability Theory "
                "(SSRN\u00a06659000)."
            ),
            (
                "Borderline classifications carried into the panel: Le\u00a0Labo "
                "(EL ownership since 2014), Frederic\u00a0Malle (EL\u00a02014), "
                "Byredo (LVMH\u00a02022). Designer-niche brand identity retained "
                "under conglomerate ownership; Cell\u00a0A placement canonical at "
                "lock with Phase\u00a0B retrieval-frame resolution per pre-reg §1.5."
            ),
            "**Deviations log:** [TBD-DEVIATIONS — entries accumulate during Phase\u00a0A and Phase\u00a0B acquisition.]",
        ],
    },
]


# ============================================================
# BACK MATTER — methodology citations, declarations, contact
# ============================================================

BACK_MATTER = {
    "citation_chain": {
        "title": "Methodology citation chain",
        "items": [
            (
                "González\u00a0Castro,\u00a0P.\u00a0U. AI\u00a0Availability — "
                "A\u00a0Third\u00a0System in Brand Availability Theory. "
                "SSRN\u00a06659000."
            ),
            (
                "González\u00a0Castro,\u00a0P.\u00a0U. The AIAS Presence "
                "Measurement Protocol: Methodological Notes on Construct "
                "Validity and the Four-Regime Taxonomy (v1.2). SSRN\u00a06761698."
            ),
            (
                "González\u00a0Castro,\u00a0P.\u00a0U. The AIAS Presence "
                "Measurement Protocol: Phase\u00a0A Pivot-Validation "
                "Specification (v1.3). SSRN\u00a06797679."
            ),
            (
                "González\u00a0Castro,\u00a0P.\u00a0U. The AIAS Presence "
                "Measurement Protocol: Recognition\u00a0×\u00a0Recall "
                "Decomposition and Multi-Component AI\u00a0Availability "
                "(v1.4). SSRN\u00a06799479."
            ),
        ],
    },
    "predecessor_phases": {
        "title": "Predecessor phases (Identity-Load joint matrix legs)",
        "items": [
            (
                "v0.16 (Regime\u00a04 Boundary and Discourse-Language "
                "Carryforward on the Kitchen-Knives Substrate) — "
                "SSRN\u00a06791999. Leg verdict: PARTIAL."
            ),
            (
                "v0.17 (Panel Inadequacy and Recognition\u00a0×\u00a0Recall "
                "Dissociation on the Premium Kitchenware Substrate) — "
                "SSRN\u00a06802261. Leg verdict: FALSIFIED on panel inadequacy."
            ),
        ],
    },
    "declarations": {
        "conflict_of_interest": (
            "The author is employed by Samsung Electronics America (Director, "
            "Corporate Brand Creative and Governance). The AIAS™ Presence "
            "Measurement Protocol and the work reported here are the author's "
            "independent academic research, conducted outside the scope of "
            "employment, in his role as faculty at the School of Visual Arts "
            "MPS Branding Program and founder of Third\u00a0System™. Samsung "
            "had no role in the design, execution, analysis, or interpretation "
            "of this work."
        ),
        "funder": "Self-funded.",
        "ethics": (
            "Not applicable; no human subjects. Research uses publicly "
            "accessible LLM APIs queried with non-personal, category-anchored "
            "prompts."
        ),
        "data_and_code": (
            "All pre-registration artifacts, acquisition data, scoring code, "
            "and verdict outputs deposited under Open Science Framework project "
            "ec6wh at osf.io/ec6wh/v18/. Pre-registration locked at commit "
            "183386c on git tag v0.18-prereg-r1, branch v0.18-il-gradient."
        ),
        "trademark": "AIAS™ and Third\u00a0System™ are trademarks of the research program.",
    },
    "contact": {
        "correspondence": "Pablo Ulpiano González Castro · pablou@pablou.com · pablou.com",
        "orcid": "0009-0003-8968-9990",
        "research_entity": "Third\u00a0System™ — thirdsystem.ai · hello@thirdsystem.ai",
    },
}


# ============================================================
# CHART SLOT REGISTRY — used by build_report_v18.py Pass 1 layout
# ============================================================

CHART_SLOT_REGISTRY = {
    "chart_01_mention_rate_distribution.pdf": {
        "title": "Phase B mention rate distribution per cell",
        "caption": (
            "Per-brand Phase\u00a0B mention counts (max\u00a0=\u00a018, "
            "six models × three frames) plotted as strip plots per cell. "
            "IL-gradient ordering: Cell\u00a0C (medium IL, light Indigo) → "
            "Cell\u00a0A (medium-high IL) → Cell\u00a0B (high IL, primary Indigo). "
            "Dotted line marks the Iwachu-pattern mention ceiling (≤\u00a02/18)."
        ),
        "source_path": "reports/figs/v18/chart_01_mention_rate_distribution.pdf",
    },
    "chart_02_cell_attrition.pdf": {
        "title": "Cell attrition: Phase A registered → Phase B mention-positive",
        "caption": (
            "Paired bars per cell. Light bar: Phase\u00a0A registered brands. "
            "Dark bar: Phase\u00a0B mention-positive brands (≥\u00a01 mention "
            "across the 18-observation panel). Dotted line marks the per-cell "
            "equivalent of the C1 worldwide floor (n\u00a0≥\u00a012\u00a0/\u00a03)."
        ),
        "source_path": "reports/figs/v18/chart_02_cell_attrition.pdf",
    },
    "chart_03_dissociation_scatter.pdf": {
        "title": "Recognition × Recall dissociation scatter",
        "caption": (
            "One point per brand. Horizontal: Phase\u00a0A C_P (Recognition, "
            "max\u00a06). Vertical: Phase\u00a0B mention count (Recall, max\u00a018). "
            "Brands colored by cell. Shaded quadrant marks the Iwachu-pattern "
            "dissociation region (C_P\u00a0≥\u00a05 ∧ mentions\u00a0≤\u00a02). "
            "Black cross marks the v0.17 Iwachu reference point (6,\u00a00)."
        ),
        "source_path": "reports/figs/v18/chart_03_dissociation_scatter.pdf",
    },
}


# ============================================================
# Build-time validation hooks (called by build_report_v18.py)
# ============================================================

def validate_content():
    """Sanity check that all sections referencing charts have valid slot IDs."""
    valid_slots = set(CHART_SLOT_REGISTRY.keys())
    issues = []
    for section in SECTIONS:
        slot = section.get("chart_slot")
        if slot is not None and slot not in valid_slots:
            issues.append(f"Section {section['id']} references unknown chart slot: {slot}")
    return issues


if __name__ == "__main__":
    issues = validate_content()
    if issues:
        print("Content validation issues:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("✓ Content validates. Charts referenced:")
        for section in SECTIONS:
            if section.get("chart_slot"):
                print(f"  - {section['id']}: {section['chart_slot']}")
        print(f"\n{len(SECTIONS)} sections, {len(CHART_SLOT_REGISTRY)} chart slots registered.")
        tbd_count = sum(
            1 for s in SECTIONS
            for b in s["body"] if "[TBD-" in b
        )
        print(f"{tbd_count} [TBD-*] markers awaiting post-acquisition fill.")
