# AIAS v0.23 Premium Spirits: errata

## 8 November 2026

Three corrections. No data, scores, hypotheses or verdicts changed.

### 1. The brand-format report carried the wrong content

The May 2026 build of `reports/v23_premium_spirits.pdf` imported a copy of the
v0.22 automotive content module, so the file named for premium spirits
reported automotive findings. It was rebuilt from the scored spirits content
(`reports/v0_23_premium_spirits_content.py` in the repository). The wrong
build is kept as `reports/_superseded_v23_premium_spirits_automotive.pdf`.

### 2. Counting errors in the text

`v23_verdicts.json` shows five brands with zero recall mentions and the 40.0
floor composite: Bombay Sapphire, The Balvenie, Casamigos, Compass Box and
Fernet-Branca. Jameson has one recall mention (composite 57.63) and sits with
them in the Absent regime. Nineteen brands have at least one recall mention.
Some sentences said six brands were never recommended, or that 18 brands were
recalled.

| Where | May 2026 text | Corrected text |
|---|---|---|
| Paper, Section 1 | six brands ... are never surfaced in recommendation contexts | five brands ... are never surfaced in recommendation contexts, and a sixth (Jameson) only once |
| Paper, Section 3.4 | Among the 18 brands with at least one recall mention | Among the 19 brands with at least one recall mention |
| Paper, Figure 3 caption | n = 18 plotted | n = 19 plotted (the figure itself already showed 19) |
| Paper, Section 4.2 | ... are absent from recommendation outputs | ... are absent or nearly absent from recommendation outputs |
| Report, lead deck (p. 3) | with six brands perfectly known yet never recommended | with five brands perfectly known yet never recommended |
| Report, summary (p. 3) | never surface in recommendation contexts | rarely or never surface in recommendation contexts |
| Report, Finding 02 (p. 5) | Six brands score a composite of 40.0 | Five brands score a composite of 40.0 |

### 3. Prior phases mislabeled in the paper

Section 1 and the reference list named the six earlier Presence phases one
version off. The version numbers and SSRN links were right; the categories
were not.

| Phase | May 2026 text | Corrected |
|---|---|---|
| v0.17 (SSRN 6802261) | kitchen knives | premium kitchenware |
| v0.18 (SSRN 6806558) | kitchenware | indie fragrance |
| v0.19 (SSRN 6809182) | indie fragrance | audiophile headphones |
| v0.20 (SSRN 6811441) | audiophile headphones | skincare |
| v0.21 (SSRN 6815378) | skincare | cosmetics |
| v0.22 (SSRN 6829118) | cosmetics | automotive |

The paper's title page carries a revision note, and accented names that the
May build printed as LaTeX escapes (for example Gonz'{a}lez, Patr'{o}n) now
print correctly. The report's methodology log records the correction.

### Files

| File | MD5 |
|---|---|
| `reports/v0_23_premium_spirits.pdf` (working paper, 14 pages) | `20c4457d772da82597f066c4a02c591c` |
| `reports/v23_premium_spirits.pdf` (brand-format report, 13 pages) | `4361ce02af9c312a656fbbd926fbb302` |

The May 2026 paper PDF is in the repository history (commit de2223c). The
report's spirits rebuild from earlier on 8 November 2026, before the counting
fix, is kept as `reports/_superseded_v23_premium_spirits_pre-erratum.pdf`.
The `_superseded_` files are records, not part of the public deposit.
