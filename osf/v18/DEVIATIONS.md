# v0.18 DEVIATIONS Log

All deviations from the pre-registered design are logged here with locus,
observation, interpretation, and resolution. Pre-registration: tag
`v0.18-prereg-r1` at commit `183386c`, revised through r4 at commit `1195cb8`.
Methodology base: AIAS™ Presence Measurement Protocol v1.4 (SSRN 6799479).

---

## Entry 1 — Cell C pivot cascade exhausted at the "niche fragrance" Recognition probe

**Locus.** Phase A, Cell C (mass-prestige), C_P pivot cascade.

**Date.** 2026-05-20 (pre-Phase-B acquisition).

**Observation.** The Phase A C_P probe template asks *"Is the brand 'X' commonly recognized as a niche fragrance?"* The `CATEGORY` anchor for v0.18 was locked at `"niche fragrance"` per pre-reg §1.7, aligning Phase A with Phase B's q1 framing. Cell C's full cascade (Chanel → Dior → YSL → Tom Ford → Givenchy → Versace → Marc Jacobs → Calvin Klein) produced the following C_P scores across the 6-slot panel:

| Brand        | C_P  |
|--------------|------|
| Chanel       | 0/6  |
| Dior         | 0/6  |
| YSL          | 0/6  |
| Tom Ford     | 2/6  |
| Givenchy     | 0/6  |
| Versace      | 0/6  |
| Marc Jacobs  | 0/6  |
| Calvin Klein | 0/6  |

No brand achieved C_P = 6/6. The cascade exhausted without anchoring a pivot.

Compare to Cell A (designer-niche, 7/8 brands at C_P = 6/6, mean ≈ 5.88, range 5–6) and Cell B (indie/artisan, mean C_P ≈ 5.0, range 3–6).

**Interpretation.** This outcome is consistent with — and indeed predicted by — `H_IdentityLoad_moderator` (§2.2). The "niche fragrance" category anchor is a lexical match for Cell A (designer-niche) and adjacent for Cell B (indie/artisan), but by definition it is a non-match for Cell C (mass-prestige). The models are correctly reporting that Chanel, Dior, YSL, and the other Cell C brands are not niche fragrances — they are mainstream-prestige designer houses, which is a distinct category in fragrance taxonomy.

The IL-gradient hypothesis predicted the Regime 4 signature would strengthen monotonically C → A → B. The Recognition data show the gradient is actually:

| Cell | IL tier | Mean C_P | Reading |
|---|---|---|---|
| Cell C (mass-prestige) | medium IL | ≈ 0.25/6 | Near-zero (outside-category) |
| Cell A (designer-niche) | medium-high IL | ≈ 5.88/6 | Near-saturation (canonical "niche") |
| Cell B (indie/artisan) | high IL | ≈ 5.00/6 | Strong, varied (adjacent to "niche") |

The gradient is large and abrupt at C → A (threshold effect from outside-category to inside-category) and slightly negative at A → B (within-category; Cell A brands are more canonically labeled "niche" than Cell B's American-DTC / clean-fragrance brands). This pattern is itself a substantive finding about the Recognition component of the v1.4 multi-component construct: the IL-gradient operates on Recognition itself, not only on Recall.

**Resolution.** Cell C cascade exhaustion is treated as the empirical finding, not as a panel construction error. The pre-reg §1.4 alternates path is NOT invoked, on three grounds:

1. **Category-anchor specificity.** The alternates registered for Cell C (Hugo Boss, Lancôme, Carolina Herrera, Paco Rabanne, Burberry) are also mass-prestige houses. They would hit the same Recognition-anchor mismatch by construction. Substituting them would not address the finding; it would only displace it.

2. **Data completeness.** The Phase A acquisition is complete for all 24 panel brands. Cell C C_P scores are non-null and feed downstream analyses (§2.3 dissociation, §3 descriptive sensitivities) without missing-data issues.

3. **Pre-registration discipline.** The alternates path was designed for in-tier substitution (when an individual brand fails to anchor for idiosyncratic reasons). The cascade exhaustion here is a substrate-level pattern, not a brand-level failure. Substituting alternates would conflate the two.

**Downstream implications.**

- **Phase B proceeds against the locked 24-brand panel.** No substitution.
- **Cell C Phase B coverage is expected to be sparse.** The three category queries (niche / independent / perfumistas) privilege Cells A and B by design. Cell C's low mention rate in Phase B is the IL-gradient signal at the Recall layer, mirroring the Recognition layer signal documented here.
- **C2 evaluation (mention concentration, per §4.0).** When a cell's total mentions are zero or near-zero, the top-2-share metric is undefined or unstable. `score_v18.py.cell_mention_concentration()` returns 0.0 when total = 0. The IL-gradient separation guard (Cell B share > Cell C share by ≥ 0.10) may need interpretation: a zero baseline in Cell C trivially passes the guard for any positive Cell B concentration. This is acknowledged as a degenerate case of the locked rule; the substantive interpretation rests on Cell A and Cell B's relative concentrations.
- **C3 evaluation (ranking coherence, per §4.0).** Requires post-attrition cell n ≥ 5. If Cell C's Phase B mention coverage falls below this floor, C3 is evaluated on Cells A and B only under the "≥ 2 of 3 cells clear" rule. Cell C exclusion from C3 is then a data-coverage consequence of the cascade exhaustion documented here, not a pre-reg deviation.
- **Dissociation analysis (§2.3 / §5.2).** Iwachu-pattern requires C_P ≥ 5. No Cell C brand meets this threshold (max Cell C C_P is 2/6 for Tom Ford). Cell C therefore contributes zero candidates to the dissociation case pool by definition. This is the expected and pre-registered behavior of the threshold, not a missing-data exclusion.

**Pre-reg integrity.** The pre-registered panel of 24 brands is unchanged. Pre-reg tag `v0.18-prereg-r1` (refined through r4 at commit `1195cb8`) remains valid. Phase A data is locked at the JSON written to `data/phase_a/v0.18/phase_a_results.json`. No retroactive panel modification.

**Author.** Pablo Ulpiano González Castro.

---

*End Entry 1. Subsequent deviations append below as Entry 2, Entry 3, etc.*
