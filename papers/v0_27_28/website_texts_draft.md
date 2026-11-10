# Website texts — DRAFT, not published (program study 67, combined v0.27 + v0.28 paper)

Prepared November 10, 2026, for the coordinator's site hand-off. Nothing here has been pushed to github.com/thirdsystem-aias/website. Format follows the site's `content/abstracts.json` (abstract as published) and `content/plain.json` (found = one line on the Studies list; short = "In short" on the study page; ind = industries covered). The plain summary is drawn only from the abstract below. The site already carries separate v0.27 and v0.28 entries; whether this paper replaces them, sits beside them, or links them is the coordinator's and Pablo's call.

**Paper title:** AI Brand Presence against a Commercial Visibility Score and Human Brand Norms: Two pre-registered construct-validity tests of the AIAS™ Presence component
**Paper PDF:** `papers/v0_27_28/v0_27_28_ssrn_paper.pdf` (20 pages)
**SSRN:** not submitted (no ID).

## Abstract (verbatim from `ssrn_submission_packet_v0_27_28.md`)

AI availability, the propensity of a brand to be surfaced when people ask large language models about its category, is measured in the AIAS program by a Presence component built from model recognition and two recall channels. This paper reports two pre-registered construct-validity tests of Presence, first written up separately, with every hypothesis and verdict as locked and no new analysis. Study 1 (convergent; 24 B2B SaaS brands) correlated a recall-share form of Presence with the Share-of-Voice score of a commercial AI-visibility instrument, the HubSpot AEO Grader. The primary hypothesis was falsified (Spearman ρ = 0.29, 95% CI [−0.17, 0.64]); neither pre-specified sensitivity changed that. Model recognition sat at ceiling for every brand, confirming the recognition-null control. An exploratory scan found recall share tracking the instrument's presence-quality (ρ = 0.80) and brand-recognition (ρ = 0.75) subscores; the Share-of-Voice gap is one of rank alignment, not restricted range. Study 2 (discriminant; 24 Technology brands drawn by seeded stratified sampling) correlated blind-acquired Presence with human brand norms from the BRAND database. Presence was discriminant from recognition sensitivity d′ (ρ = 0.38; the BCa interval stays below the 0.74 reducibility threshold), so that hypothesis was confirmed. Against familiarity the point estimate (ρ = 0.59) fell in the partial band, but the BCa interval [0.18, 0.83] spanned all three pre-registered bands, and the locked rule returned undetermined. Because recognition was saturated in Study 1 and recall floored for most brands in Study 2, the two studies tested different facets of Presence: recall in the first, recognition in the second. Convergence with a commercial visibility score was not established, and the familiarity question remains open at n = 24.

## Plain summary (draft `content/plain.json` entry)

```json
{
  "found": "Our Presence score didn’t match a commercial AI share-of-voice score, and it was distinct from how well people recognize tech brands; against familiarity the result was undetermined.",
  "short": "This paper puts two of our pre-registered tests side by side, with no new analysis. Across 24 B2B software brands, our Presence score didn’t match the Share-of-Voice score of a commercial AI visibility tool, HubSpot’s AEO Grader, so our prediction failed, although two of the tool’s sub-scores tracked ours in an exploratory check. Across 24 technology brands, Presence was distinct from how reliably people recognize the brands, while the test against how familiar people are with them was undetermined. The two tests covered different parts of the score: how often AI names a brand in the first, whether AI recognizes it in the second.",
  "ind": ["Software", "Tech brands"]
}
```

Source check (each clause to the abstract): two pre-registered tests, no new analysis (sentence 2); 24 B2B SaaS brands, HubSpot AEO Grader Share of Voice, falsified (sentences 3–4); two sub-scores tracked, exploratory (sentence 6); 24 Technology brands, BRAND human norms, recognition confirmed, familiarity undetermined (sentences 7–9); recall in the first, recognition in the second (sentence 10). "Software" and "Tech brands" are the labels the site already uses for v0.27 and v0.28.

## Site hand-off items not drafted here

Three headline numbers with sources, explorer CSVs and Claims Register rows are the coordinator's step; candidate headline numbers, all from the locked verdict files: ρ = 0.29 (Study 1 primary, `osf/v27/v0.27_verdicts.json` H_CV3_Primary), ρ = 0.38 with BCa upper bound 0.71 (Study 2 recognition, `osf/v28/v28_verdicts.json` H_Disc_Recognition), BCa [0.18, 0.83] (Study 2 familiarity, H_Disc_Familiarity).
