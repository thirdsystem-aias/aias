# SSRN Submission Packet — v1.6 (methodology paper)

**Target:** papers.ssrn.com webform submission
**Paper PDF:** `~/aias/papers/v1_6/v1_6_ssrn_paper.pdf`
**Lock state at submission:** `v1.6-prereg-r1` (commit `f10616a`)

Work through the webform top-to-bottom; each section below maps to the corresponding webform step.

---

## Step 1 — Title

Paste-ready (single line):

```
Substrate Pre-Screening, Independent Moderator Pathway, and Phantom Brand Persistence Phase B Extension
```

Subtitle field (if SSRN exposes one):

```
AIAS™ Presence Measurement Protocol, v1.6 — Three Methodology Increments under Retrospective Test against the v0.16–v0.21 Corpus
```

If subtitle field is unavailable, append to title with em-dash:

```
Substrate Pre-Screening, Independent Moderator Pathway, and Phantom Brand Persistence Phase B Extension — AIAS™ Presence Measurement Protocol, v1.6
```

---

## Step 2 — Authors

Single-author submission. Standard AIAS author block:

| Field | Value |
|---|---|
| First name | Pablo |
| Middle name | Ulpiano |
| Last name | González Castro |
| Email | pablou@pablou.com |
| ORCID | 0009-0003-8968-9990 |
| Primary affiliation | School of Visual Arts, MPS Branding Program, New York, NY |
| Secondary affiliation | Third System™ (research entity; data archive and methodology venue) |

**Reminder:** Samsung Electronics America goes in Declarations §COI only, never the author block.

---

## Step 3 — Abstract, Keywords, JEL

### Abstract (paste in full)

The AIAS™ Presence Measurement Protocol v1.5 (SSRN 6810758) closed the within-cell adequacy and two-channel Recall layers of the multi-component construct. Two prospective phases under v1.5 — v0.20 (skincare, SSRN 6811441) and v0.21 (cosmetics, SSRN 6815378) — surfaced three open items that the v1.5 routing matrix could not resolve at the methodology layer. First, v0.21 produced uniform-saturation C2 failure (distinct C_P count = 1 in all three cells); v0.20 produced differential C2 failure. Under v1.5 both routed to FALSIFIED, collapsing two structurally distinct substrate states to one verdict. Second, the moderator hypothesis H_IdentityLoad_moderator returned NARROWED in both phases despite increasingly strong substantive channel-asymmetry signals; the five-leg joint structure was pessimistic in the presence of Regime 4 falsification regardless of within-phase signal direction. Third, v0.21 surfaced strong Phantom Brand Persistence — Glossier (a v0.20 Cell B panel brand, not on the v0.21 panel) appearing in cultural-channel frames for all six panel LLMs in q6 — as a case-study observation but not a measured component of the construct.

Protocol v1.6 introduces three methodology increments. Increment 1 is a substrate-level Recognition pre-screen: a substrate with distinct C_P count = 1 in all three cells routes to a fifth Regime 4 verdict state, REGIME-4-UNAVAILABLE-AT-RECOGNITION, distinct from FALSIFIED. Increment 2 introduces H_IdentityLoad_Direct, a parallel hypothesis evaluable independently of Regime 4's C2 conditions, scored per cell via δ = mean(R_cult) − mean(R_cat) with bootstrap percentile confidence intervals (n = 10,000; methodology-level seed locked at 1621 for retrospective scoring). The verdict matrix is anchored to the IL-gradient prediction with a monotonic-gradient check on Cell C. Increment 3 lifts Phantom Brand Persistence from a descriptive observation to a measured component: R_phantom counts off-panel reference-vocabulary mentions across the 36 Phase B responses against a substrate-specific vocabulary constructed as the union of the panel, a pre-registered top-50 market-share list, and prior-phase Phase B emergents cross-validated by the market-share list. Persistence threshold K = 6.

Retrospective scoring against the v0.16–v0.21 corpus reports three results. v0.21 returns CONFIRMED for H_IdentityLoad_Direct (Cell A δ = −3.13 with 95% CI excluding zero; Cell B δ = +7.12 with CI excluding zero; Cell C δ = +1.00 satisfies the monotonic-gradient check) — an uplift from the v1.5 NARROWED moderator verdict. v0.21 returns CONFIRMED for H_PhantomBrandPersistence with six off-panel brands clearing K = 6 (Urban Decay 13, Estée Lauder 13, Glossier 12, Too Faced 9, Make Up For Ever 7, Clinique 6); the validity anchor passes with margin. The off-panel phantom cohort exhibits channel signature tracking the brands' Identity Load — Estée Lauder and Clinique pure canonical (R_cult = 0); Glossier pure cultural (R_cat = 0). The IL-gradient mechanism that produces panel-level channel asymmetry also produces off-panel phantom channel asymmetry. v0.20 returns PARTIAL for H_IdentityLoad_Direct, with a substantive substrate finding that the skincare IL-gradient signal lives in Cell B vs. Cell C rather than Cell A vs. Cell B. For v0.16–v0.19, Increment 1 narrative classification is feasible from published Phase A distributions; Increment 2 retrospective bootstrap is not feasible because two-channel R_cult decomposition was a v1.5 prospective increment first acquired in v0.20. Increment 3 retrospective scoring is locked to v0.21 only; the construct's prospective scope begins at v0.22.

The pre-registration discipline (tag v1.6-prereg-r1, deposited at osf.io/ec6wh/methodology/v1_6/) locks the three increment specifications, the verdict matrices, the bootstrap parameters, the reference vocabulary construction rule, the persistence threshold, and the retrospective vs. prospective application boundary before retrospective scoring is run.

### Keywords (semicolon-separated)

Paste-ready:

```
AI availability; brand availability; AIAS; pre-registration; Ehrenberg-Bass; methodology paper; substrate classification; channel asymmetry; bootstrap inference; phantom brand persistence; identity load; multi-component measurement
```

### JEL Codes

| Slot | Code | Topic |
|---|---|---|
| Primary | M31 | Marketing |
| Secondary | L86 | Information and Internet Services; Computer Software |
| Secondary | L15 | Information and Product Quality; Standardization and Compatibility |
| Secondary | D83 | Search; Learning; Information and Knowledge; Communication; Belief; Unawareness |
| Secondary | M37 | Advertising |

---

## Step 4 — eJournal Classification (up to 7)

| Slot | eJournal |
|---|---|
| 1 | Marketing eJournal |
| 2 | Marketing Strategy eJournal |
| 3 | Consumer Behavior eJournal |
| 4 | Advertising & Marketing Communications eJournal |
| 5 | Information Systems & eBusiness Network |
| 6 | Artificial Intelligence eJournal |
| 7 | Decision-Making Under Risk & Uncertainty eJournal |

---

## Step 5 — Disclosures

**Funder:** Self-funded.

**Ethics:** Not applicable; no human subjects.

**Conflict of interest:** Per AIAS standard disclosure — the author is employed by Samsung Electronics America (Director, Corporate Brand Creative & Governance). The methodology program's pre-registration discipline includes a per-phase ex-ante COI screen confirming no brand in the panel is Samsung-affiliated. The v1.6 methodology paper introduces no new panel; the COI screen carries forward from the empirical anchor phases. The employer has no role in the research program's methodology, pre-registration, scoring, or publication decisions.

**Data availability:** All pre-registrations, registries, scoring scripts, retrospective scoring outputs, and reference vocabularies are deposited at osf.io/ec6wh/methodology/v1_6/. Pre-registration is locked at git commit, tag `v1.6-prereg-r1`.

---

## Step 6 — File Upload

Upload `papers/v1_6/v1_6_ssrn_paper.pdf` (19 pages).

---

## Post-submission backfill

After SSRN returns the abstract ID (1–3 business days):

1. **Add to phase SSRN registry in CLAUDE.md:** new row for v1.6 methodology paper with abstract ID.
2. **Backfill citation in v0.22+ phase papers:** v1.6 enters the methodology citation chain (v1.2 → v1.3 → v1.4 → v1.5 → **v1.6**) for all subsequent phase papers.
3. **Cross-citation backfill:** update the Tri-System MSI WP and Routledge monograph bibliographies to include v1.6.

---

## Submission checklist

- [ ] Paper PDF built and reviewed (`papers/v1_6/v1_6_ssrn_paper.pdf`, 19pp)
- [ ] OSF deposit complete at `osf.io/ec6wh/methodology/v1_6/`
- [ ] Author block matches AIAS standard (no Samsung in author block)
- [ ] Keywords include the 5 program-standard items
- [ ] JEL M31 primary
- [ ] eJournal slots filled (7 max)
- [ ] Funder, ethics, COI fields completed
- [ ] Webform submitted; SSRN abstract ID captured upon return
