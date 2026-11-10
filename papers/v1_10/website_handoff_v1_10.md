# Website hand-off — v1.10 Ranking, Paper A

Prepared Tue Nov 10, 2026 for the coordinator (the website is not edited here). Source paper: `papers/v1_10/v1_10_ssrn_paper.pdf` (22 pages), built from `papers/v1_10/v1_10_ssrn_paper_draft.md`. Abstract taken from the regenerated SSRN packet (`papers/v1_10/ssrn_submission_packet_v1_10.md`), which matches the paper's abstract. Gate verdict: MARGINAL (not passed). No report PDF; no SSRN ID yet (add `"ssrn"` when it arrives).

## 1. PDF

Copy `papers/v1_10/v1_10_ssrn_paper.pdf` to `public/files/papers/v1_10_ssrn_paper.pdf`.

## 2. `DATA` entry for `boards/Studies.dc.html`

Insert newest first (before the `AIAS 2.0` entry, after the held v0.38/v0.39 entries):

```json
{"id": "v1.10", "date": "Nov 2026", "type": "Method", "title": "Where a Brand Sits in an AI Answer", "topic": "Ranking instrument, tested for a third component", "paper": "files/papers/v1_10_ssrn_paper.pdf", "paperPages": 22, "found": "Where AI places a brand in its answers can be measured reliably, but it partly follows how often the brand is named, so it isn’t added to the score for now.", "short": "We tested a possible third part of the score: where a brand appears among the brands an AI answer names. Measured with rules fixed in advance, a brand’s position was highly reliable and kept its order over three weeks and five months, and it was separate from consistency. It was not clearly separate from how often a brand is named: at two of three rounds it fell short of our bar, and brands named more often tend to be named earlier. By our own rule, ranking is not added to the score on this evidence.", "ind": []}
```

## 3. `content/abstracts.json` — key `"v1.10"`

```json
{
 "v1.10": [
  "The AIAS™ program measures AI brand availability with two validated components, Presence (how often a fixed panel of language models names a brand) and Consistency (how evenly the models name it). This paper tests a third: Ranking, where a brand sits in an answer's list of brands, given that it is named. A deterministic extractor recovered positions from 3,766 archived answers with text (100% parsed; mention sets identical to the certified Presence detectors). A rank statistic was selected by a pre-registered rule on a separate panel, blind to Presence and Consistency: mean normalised position (MNP), with split-half reliability 0.951 over 138 brands in nine categories, which fell to −0.017 when brand order was shuffled within answers. The confirmatory gate ran on five categories and three waves of a six-model panel (52–55 rated brands per comparison). Ranking is separable from Consistency (pooled within-category ρ = 0.252, 0.119, 0.142; CONFIRMED) and holds its brand order over three weeks far beyond what list composition produces (ρ = 0.897, both nulls p = 0.0001; CONFIRMED) and over five months (ρ = 0.846). It is not cleanly separable from Presence: ρ(R*, P) = 0.275, 0.366 and 0.307, inside the confirmation band at the first wave only (MARGINAL). On the early panel, Ranking tracked recall share at ρ = 0.663 (FALSIFIED). The gate is therefore MARGINAL: the program does not add Ranking as a component on this evidence, and a Paper B proceeds only on the author's recorded decision, with separability from Presence as its first confirmatory test. Brands that models name more often tend to be named earlier."
 ]
}
```

## 4. `content/plain.json` — `studies["v1.10"]` (drawn only from the abstract above)

```json
{
 "v1.10": {
  "found": "Where AI places a brand in its answers can be measured reliably, but it partly follows how often the brand is named, so it isn’t added to the score for now.",
  "short": "We tested a possible third part of the score: where a brand appears among the brands an AI answer names. Measured with rules fixed in advance, a brand’s position was highly reliable and kept its order over three weeks and five months, and it was separate from consistency. It was not clearly separate from how often a brand is named: at two of three rounds it fell short of our bar, and brands named more often tend to be named earlier. By our own rule, ranking is not added to the score on this evidence.",
  "ind": []
 }
}
```

Lengths: found 156 characters (list line cap 160); short 505 characters (v1.9: 333; AIAS 2.0: 569).

## 5. Methodology board, versions list (`boards/Methodology.dc.html`, `#versions`)

Insert above the `Nov 2026 · v1.9` item:

```html
<li style="display: flex; flex-direction: column; gap: 4px; padding: 14px 0; border-top: 1px solid #E4E2EC;"><span style="margin: 0; font-size: 13px; line-height: 1.4; font-weight: 500; color: #5E5A5B;">Nov 2026 · v1.10</span><a href="/studies/v1-10/" style="align-self: flex-start; display: inline-flex; align-items: center; min-height: 44px; margin: -6px 0 2px; font-size: 16px; line-height: 1.35; font-weight: 600; color: #37237B; text-decoration: underline; text-underline-offset: 3px; text-wrap: pretty;">Where a Brand Sits in an AI Answer</a><span style="margin: 0; font-size: 13px; line-height: 1.5; color: #5E5A5B;">Ranking instrument, tested for a third component</span></li>
```

## Notes

- The title, topic and plain summary are new copy: one Claims Register row each.
- `found` and `short` say plainly that the score was reliable and stable, separate from consistency, not clearly separate from how often a brand is named, and therefore not added (the MARGINAL gate).
