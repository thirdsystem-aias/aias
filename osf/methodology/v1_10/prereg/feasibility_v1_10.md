# v1.10 Ranking Paper A — declared parsing feasibility

Draft r1, 2026-11-10. Script: `osf/methodology/v1_10/scoping/feasibility_v1_10.py` (imports the extractor in `scripts/score_v1_10.py`); output: `osf/methodology/v1_10/scoping/feasibility_v1_10.json`.

**Declaration.** This look uses only a development sample that every confirmatory analysis excludes: v0.17 phase B (18 frame answers, premium kitchenware) and v0.18 phase B (18 frame answers, indie fragrance), both legacy-panel frames. It measures parsing only. It computes **no** statistic involving Presence, Consistency, separability or stability, and no brand-level score. It informed extraction rules E3, E4 and E6; it is not a result.

| Parsing property | v0.17 B | v0.18 B |
|---|---|---|
| Answers (with text) | 18 (18) | 18 (18) |
| Any list (≥ 2 top-level items) | 100% | 83.3% |
| Explicit numbered list (≥ 2 numbered items) | 44.4% | 33.3% |
| List-structured (≥ 2 items led by a registry brand) | 100% | 72.2% |
| Answers naming ≥ 1 registry brand | 100% | 83.3% |
| Rankable (≥ 2 registry brands named) | 100% | 77.8% |
| Registry brands named per answer: mean, median, range | 6.17, 6, 4–8 | 4.00, 4, 0–7 |
| Registry brands found at least once in the set | 10 of 16 | 11 of 24 |
| Top-level items with no registry brand | 51.0% | 65.9% |
| List answers naming a brand before the first item | 0% | 0% |
| Brand-answer pairs named twice or more | 55.0% | 12.5% |
| Brands named in a list answer without leading any item | 2.7% | 0% |
| Rankable answers with a tie (primary rule) | 0% | 0% |
| Rankable answers where lead-item and first-mention orders differ | 11.1% (2 of 18) | 0% (0 of 14) |
| Mean Kendall τ, lead-item vs first-mention | 0.958 | 1.000 |
| Nested-match events (one brand's match inside another's) | 0 | 0 |
| Detector parity with the archived per-cell mention flags | not stored for v0.17 | 99.54% of 432 cells (2 disagree) |

**What this means for the rules.**
1. Almost all frame answers are lists, but fewer than half use explicit numbers: the item parser has to treat bullets, bold-led lines and headings as items (E3).
2. Brands are often named again later in an answer (up to 55% of pairs in v0.17), so first-occurrence-wins (E4) matters.
3. The lead-item and first-mention rules rarely disagree. When they do, the cause is a brand named in passing inside another brand's item, so lead-item stays primary and first-mention becomes sensitivity S1 (open question 1).
4. Half or more of list items carry no registry brand, so Ranking is rank **among registry brands**, not absolute list position (Limitations).
5. Ties and nested matches did not occur here. They are expected in substrates with family names, such as v0.22's Samsung entries (E7).
6. The parity check runs as built. The 2 disagreeing v0.18 cells set the expectation for MQ2's 0.98 floor on coded mention files.

**Not covered.** The sample contains only legacy-panel frames, so EARLY-6 prompt types (identity, comparison, constraint) are not tested here (open question 15). The sample has no answers with errors or missing text.
