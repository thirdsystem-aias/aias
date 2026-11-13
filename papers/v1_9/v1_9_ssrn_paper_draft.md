---
title: "One Score or Two? Calibrating a Presence and Consistency Composite for AI Brand Availability"
subtitle: "A Pre-Registered Calibration with Blind Five-Month Confirmation (AIAS™ Methodology v1.9)"
date: "November 2026"
mainfont: "Carlito"
fontsize: 11pt
geometry: [letterpaper, margin=1in]
header-includes: |
  \usepackage{setspace}
  \usepackage{float}
  \usepackage{caption}
  \usepackage{titlesec}
  \usepackage{needspace}
  \setstretch{1.36}
  \setlength{\parskip}{8pt}
  \setlength{\parindent}{0pt}
  \renewcommand{\maketitle}{}
  \providecommand{\xmpquote}[1]{#1}
---

\begin{titlepage}
\setstretch{1.0}
\setlength{\parskip}{0pt}
\begin{center}

{\LARGE \textbf{One Score or Two? Calibrating a Presence and\\ Consistency Composite for AI Brand Availability}}\\[8pt]

{\large A Pre-Registered Calibration with Blind Five-Month Confirmation\\ (AIAS™ Methodology v1.9)}\\[28pt]

Pablo Ulpiano González Castro\\[4pt]
School of Visual Arts, MPS Branding Program, New York, NY \textit{(primary academic affiliation)}\\
Third System™ (research entity; data archive and methodology venue)\\[8pt]
Correspondence: pablou@pablou.com · pablou.com\\
ORCID: 0009-0003-8968-9990\\[20pt]

Pre-registration: \texttt{v1.9-prereg-r1} (deposited on OSF before any confirmation-wave data existed)\\
Materials: OSF \texttt{ec6wh/methodology/v1\_9}\\

\end{center}
\end{titlepage}

# Abstract {-}

The AIAS™ measurement program now has two validated components of AI brand availability: Presence, how often a fixed panel of large language models names a brand (v1.6), and Consistency, whether the panel's models agree about it, measured by the mean-independent dispersion statistic $\varphi$ (v1.8). This paper asks whether the two should be combined into one score. Stage 1, declared as calibration on two frozen waves (112 brand units, five product categories, six models), evaluated a pre-specified grid of eight composite specifications (two Consistency scores, two rules for brands with few mentions, two composition forms) against three constraints: the Consistency score must stay separable from Presence ($|\rho| \le 0.50$), the composite must carry information Presence does not ($|\rho(A, P)| \le 0.95$), and one or two mentions must not buy more credit than Presence already gives. No specification passed all three at both waves. Every composite that withheld Consistency from brands with few mentions ranked brands almost exactly as Presence did ($\rho(A, P) = 0.971$--$0.997$), and shrinking low-count scores toward the scale midpoint tied Consistency to Presence ($\rho = 0.715$--$0.773$). Under the pre-registered rule, v1.9 locks no single composite: the program's next synthesis reports Presence and Consistency as two scores. The Consistency score is locked as $C_\varphi = 100(1 - \varphi/7.2)$, rated only for brands with at least six mentions. Stage 2 confirmed the locked specification blind, on a third wave collected after the lock, 152 days after the second: Presence retest $\rho = 0.954$ ($n = 112$); Consistency separable from Presence ($\rho = 0.190$, $n = 54$); Consistency retest $\rho = 0.647$ ($n = 52$), beyond a frame-structure null ($p_{\text{frame}} = 0.008$); and the best composite still tracked Presence ($\rho = 0.969$).

**Keywords:** AI availability; brand availability; AIAS; pre-registration; Ehrenberg-Bass; large language models; composite measurement; consistency; test--retest reliability; scale construction

**JEL codes:** M31; L86, L15, D83, M37

**Paper status:** Pre-registered methodology lock (tag `v1.9-prereg-r1`). Stage 1 is declared calibration on data already in the record; Stage 2 is confirmatory and blind, scored on the v0.41 third wave, which did not exist when the specification was locked. One procedural deviation, recorded before the first confirmation-wave call (§3.5). Part of the AIAS measurement program.

# 1. Introduction

AI Availability --- the discoverability and representation of a brand in the outputs of large language models --- has been proposed as a third measurable layer of brand availability (González Castro, 2026, SSRN 6659000), alongside the Mental and Physical Availability of the Ehrenberg-Bass tradition (Sharp, 2010; Romaniuk & Sharp, 2022). The Tri-System framework that places it in a model of brand growth describes the AI Availability Score (AIAS) as a 0--100 score built from several dimensions (MSI Working Paper 26-132). The empirical program has so far validated two of them.

Presence was locked first. Its composite combines recognition (does the model know the brand) with recall (does the model name the brand unprompted in a buyer-style question), and it was anchored across five product categories in the AIAS 1.0 synthesis (SSRN 6817841) under the v1.6 protocol (SSRN 6816340). Consistency followed a longer path. A coefficient-of-variation quantity was falsified as a Consistency instrument because it tracked recall level (v1.7, SSRN 6878818); its replacement, the quasi-binomial dispersion statistic $\varphi$, is independent of the recall level ($|\rho(\varphi, \mu)| = 0.091$) and reproducible over three weeks (v1.8, SSRN 6963359). A component-dissociation study then found that Consistency does not move with a brand's identity load (v0.37), and a five-month third wave found that both components hold their brand order and change independently of each other (v0.41).

With two components in hand, the obvious next step is to combine them. The v1.8 record and the program roadmap both named v1.9 as the calibration of a two-component composite. Combining is not free, however. A composite earns its place only if it carries information that its strongest component does not; otherwise it adds a weighting convention, and a source of confusion, without adding measurement. And a Consistency score has a specific weakness at low counts: a brand named once or twice across the panel has a dispersion close to its binomial expectation whatever the models do, so a naive Consistency score is high by default for exactly the brands about which it knows least.

This paper reports a pre-registered calibration designed to settle the question by rule rather than by preference. Stage 1 evaluates every specification in a small, fixed grid against three constraints, on two frozen waves, and selects by a rule written before the grid was run. The rule includes a make-or-break outcome: if no specification passes, the program locks "no composite" and reports the components side by side. Stage 2 then tests the locked outcome blind on a third wave that was collected after the lock. The result is that outcome: no single composite passes, and the program reports two scores. The paper's contribution is the evidence for that decision, the locked definition of the Consistency score that enters reporting, and a five-month confirmation that both reported scores are reliable and separable.

# 2. Components and candidate scores

## 2.1 Notation

For brand $b$ and model $m$ in a fixed panel of $M = 6$ models, $k(b,m) \in \{0, \ldots, 6\}$ counts the recall frames ($F = 6$: three category and three cultural frames, pooled) in which $m$ names $b$. Recall share is $\hat\pi_b = \sum_m k(b,m) / 36$, and $n_b = \sum_m k(b,m)$ is the brand's total number of mentions. Recognition $C_P \in \{0, \ldots, 6\}$ counts the models that recognize the brand.

## 2.2 Presence

Presence is taken as a locked input, not calibrated here. It is the v0.25 presence composite of the AIAS 1.0 lineage,

$$P = 100 \cdot \frac{C_P/6 + R_{\text{cat}}/18 + R_{\text{cult}}/18}{3}.$$

Because $R_{\text{cat}} + R_{\text{cult}} = n_b$ and $\hat\pi_b = n_b/36$, this is exactly $P = 100\,(C_P/6 + 2\hat\pi_b)/3$, which defines $P$ identically for all five substrates, including the single-channel headphones substrate and the spirits substrate with non-canonical channels. $P$ runs from 0 to 100 and is defined for every brand.

## 2.3 The Consistency score

$\varphi$ is the v1.8 between-model quasi-binomial dispersion,

$$\varphi_b = \frac{1}{M-1}\sum_{m}\frac{\bigl(k(b,m) - F\hat\pi_b\bigr)^2}{F\hat\pi_b\,(1-\hat\pi_b)},$$

with null expectation 1 when every model draws from the common rate; higher values mean less agreement. To place it on the same 0--100 orientation as Presence, the calibration scores Consistency as

$$C_\varphi = 100 \left(1 - \frac{\varphi_b}{\varphi_{\max}}\right), \qquad \varphi_{\max} = \frac{F M}{M-1} = 7.2,$$

where $\varphi_{\max}$ is the value reached when every model names the brand either in all frames or in none. $C_\varphi = 100$ means identical counts across models, and $C_\varphi = 0$ maximal polarization. The scale is absolute and bounded, so it is comparable across categories without within-category ranking. Two boundary cases are fixed in advance: a brand named by every model in every frame ($\hat\pi_b = 1$) has no dispersion and scores 100; a brand never named ($\hat\pi_b = 0$) is not rated, because consistency of absence is not consistency of availability.

The second candidate Consistency score adds the v1.8 positional diagnostic $J$, the mean pairwise Jaccard overlap of the frame sets in which models name the brand: $C_{\varphi J} = (C_\varphi + 100J)/2$ where $J$ is defined (at least two models name the brand), and $C_\varphi$ otherwise. v1.8 found $\rho(\varphi, J) = -0.40$, so $J$ is not redundant with $\varphi$.

## 2.4 The low-count problem

A scoping look at the frozen waves, run before the grid was specified and declared as such, showed the problem the calibration had to solve. For brands with one or two total mentions, mean $C_\varphi$ was 85, against 86 for brands with 3--18 mentions and 76 for brands with 19--36. At one or two mentions $\varphi$ sits near its binomial expectation regardless of model behaviour, so $C_\varphi$ is high by default and carries no information. Averaged naively with Presence, this produces a windfall: in the scoping data, brands named once scored 58.0 on average ($n = 9$) against 30.4 for brands never named ($n = 28$). The same look found $C_\varphi$ nearly unrelated to Presence ($\rho = 0.096$ at $t_1$, $n = 84$; $-0.041$ at $t_2$, $n = 88$; within-substrate ranks) and a three-week retest of 0.533 for raw $\varphi$ on the same basis ($n = 83$), against 0.970 for Presence.

## 2.5 The candidate grid

Three binary choices define eight candidates, all computed and none dropped after the fact:

- **Consistency score:** $C_\varphi$ or $C_{\varphi J}$.
- **Low-count rule.** SHRINK: $C^* = wC + (1-w)\,50$ with $w = n_b/(n_b + 6)$, pulling low-count scores toward the scale midpoint (the shrinkage constant is one model's full frame set); defined for every recalled brand. FLOOR: $C^* = C$ if $n_b \ge 6$, otherwise not rated.
- **Composition form.** ADD: $A = (P + C^*)/2$, with $A = P$ where $C^*$ is not rated. MOD: $A = P\,(0.5 + 0.5\,C^*/100)$, with $A = 0.5P$ where $C^*$ is not rated, so that Consistency modulates Presence and a brand cannot score on Consistency alone.

# 3. Design

## 3.1 Data

The data are the five omnibus substrates of the program (audiophile headphones, 16 brands; skincare, cosmetics, automotive and premium spirits, 24 each; 112 brand units), measured on the six-model legacy panel: Claude Opus 4.5 and Claude Sonnet 4.5, GPT-4o and GPT-4o mini, Gemini 2.5 Flash and Gemini 2.5 Flash Lite. Stage 1 uses $t_1$ (the original acquisitions, 20--26 May 2026) and $t_2$ (the v0.34 re-acquisition, 10 June 2026). Stage 2 uses $t_3$ (the v0.41 re-acquisition, 9 November 2026). Extraction is identical to v1.8 and v0.41, and the v0.41 computational-parity gates P1--P4 had to pass before any Stage 1 statistic was computed; they did.

## 3.2 Stage 1: constraints and selection rule

Each candidate had to pass three constraints at $t_1$ and at $t_2$ separately:

- **K1 Dissociation:** $|\rho(C^*, P)| \le 0.50$, on within-substrate ranks, over brands with $C^*$ rated. This is the make-or-break constraint for the Consistency score: a score that tracks Presence cannot be the second component.
- **K2 Incremental information:** $|\rho(A, P)| \le 0.95$, on within-substrate ranks over all 112 brands. A composite that ranks brands as Presence does carries no information Presence does not.
- **K3 No windfall:** the gap in mean $A$ between brands with one or two mentions and brands never named may exceed the corresponding gap in mean $P$ by at most 5 points.

Among candidates passing all three at both waves, the rule selects the highest test--retest reliability $\rho(A_{t_1}, A_{t_2})$; candidates within 0.01 of the best tie, and ties go to the simpler choice ($C_\varphi$ over $C_{\varphi J}$, FLOOR over SHRINK, ADD over MOD). If no candidate passes, v1.9 locks "no composite". The rule as written does not say which Consistency score then enters reporting; that choice was made in Stage 1, before the lock, and recorded with its reason in the pre-registration (§4.2).

Because Stage 1 runs on data already in the record, it is declared as calibration, not as a test. Predictions were written before it ran and are kept in the record: the expected selection was $C_\varphi$ with a low-count rule and the ADD form.

## 3.3 Stage 2: confirmation hypotheses

The Stage 2 hypotheses were revised for the Stage 1 outcome before the lock, and test the scores that reporting will use:

- **`H_Presence_Score_Reliability` (primary).** $P$ keeps its brand order over five months: $\rho(P_{t_2}, P_{t_3})$ on pooled within-substrate ranks, all brands, with a one-sided stratified permutation test (10,000 draws, $t_3$ ranks permuted within substrate). CONFIRMED iff $\rho \ge 0.80$ and $p_{\text{perm}} < .05$; FALSIFIED iff $\rho < 0.60$ or $p_{\text{perm}} \ge .05$.
- **`H_Dissociation_t3` (primary).** Consistency stays separable from Presence at $t_3$: $|\rho(C^*_{t_3}, P_{t_3})|$ over brands with $C^*$ rated. CONFIRMED iff $|\rho| \le 0.30$; FALSIFIED iff $|\rho| \ge 0.50$.
- **`H_Consistency_Reliability` (primary).** The locked Consistency score is reliable beyond frame structure: $\rho(C^*_{t_2}, C^*_{t_3})$ over brands rated in both waves, judged against the v0.41 within-frame model-shuffle null applied to $C^*$ (10,000 draws). CONFIRMED iff $\rho \ge 0.50$ and $p_{\text{frame}} < .05$; FALSIFIED iff $\rho < 0.30$ or $p_{\text{frame}} \ge .05$.
- **`H_NoComposite_t3` (secondary, descriptive).** The Stage 1 outcome replicates: $\rho(A, P)$ at $t_3$ for the best FLOOR composite, reported against the K2 line of 0.95.

The frame-structure null matters for Consistency. Shuffling which model gave which answer within each question preserves the questions' structure, and v0.41 found that this alone leaves a substantial correlation in $\varphi$ between waves. A Consistency score must beat that baseline, not only a shuffle of brand labels. Stage 2 does not double-count v0.41: v0.41 tests raw $\varphi$ and recall share; Stage 2 tests the calibrated scores that reporting will use.

## 3.4 Analysis conventions

Correlations are Pearson correlations on within-substrate percentile ranks, pooled across substrates, so that category-level differences in base rates do not drive them. Permutations are stratified by substrate. Seeds, draw counts and every threshold are fixed in the pre-registration.

## 3.5 Pre-registration, anchoring and deviation

Stage 1 was run on 9 November 2026, the selection rule was applied, the outcome and the full table were written into the pre-registration, and the content was locked at tag `v1.9-prereg-r1` and deposited on OSF, where it was verified byte for byte (about 06:40 UTC). The author confirmed the no-composite outcome before the lock. All of this preceded the first $t_3$ call of v0.41, so Stage 2 is blind: the specification was fixed before the confirmation data existed.

One deviation was recorded, before the first $t_3$ call. The locked sequence called for the tag to be pushed to the public code repository before the OSF deposit; the push could not be made because write access to the repository was unavailable from the acquisition machine. With the author's approval, OSF served as the external anchor: the deviation record and an anchor file (tag object, commit and tree hashes, and the SHA-256 of every locked file) were deposited on OSF, which timestamps them, before the first $t_3$ call. The tag is to be pushed when access exists and must resolve to the recorded hashes. The deviation changes the order of the two external anchors, not the content or the timing of the lock relative to the data.

# 4. Results

## 4.1 Stage 1: no candidate passes

Table 1 reports every candidate at both waves. No candidate passes K1--K3 at both waves, and the failures fall into two patterns.

The FLOOR candidates built on $C_\varphi$ pass K1 comfortably ($\rho = 0.073$ and $0.082$) and pass K3 (under FLOOR, low-count brands are not rated, so they receive no Consistency credit), but fail K2: the composite ranks brands at $\rho(A, P) = 0.971$--$0.992$ with Presence. The reason is a difference in spread. Presence spans most of the 0--100 range, from brands never named to brands named almost everywhere; rated Consistency scores mostly lie between 60 and 100. Any average of a wide component and a narrow one is ranked by the wide one. The MOD form, which multiplies Presence by a factor between 0.5 and 1, is ranked by Presence even more closely.

\needspace{14\baselineskip}

Table: Stage 1 calibration grid on frozen $t_1$ and $t_2$. K1 = $|\rho(C^*, P)|$ (limit 0.50); K2 = $|\rho(A, P)|$ (limit 0.95); K3 = windfall excess, mean-$A$ gap minus mean-$P$ gap, low-count versus never-named brands (limit 5 points). Retest = $\rho(A_{t_1}, A_{t_2})$ and $\rho(C^*_{t_1}, C^*_{t_2})$. Within-substrate ranks.

| Specification | K1 $t_1$ | K1 $t_2$ | K2 $t_1$ | K2 $t_2$ | K3 $t_1$ | K3 $t_2$ | Retest $A$ | Retest $C^*$ | Fails |
|---------------------|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
| $C_\varphi$ FLOOR ADD | 0.073 | 0.082 | 0.971 | 0.975 | 0.00 | 0.00 | 0.962 | 0.736 | K2 |
| $C_\varphi$ FLOOR MOD | 0.073 | 0.082 | 0.989 | 0.992 | $-1.16$ | $-1.33$ | 0.971 | 0.736 | K2 |
| $C_\varphi$ SHRINK ADD | 0.715 | 0.773 | 0.950 | 0.972 | 11.85 | 12.34 | 0.961 | 0.882 | all |
| $C_\varphi$ SHRINK MOD | 0.715 | 0.773 | 0.988 | 0.993 | 8.08 | 7.78 | 0.973 | 0.882 | all |
| $C_{\varphi J}$ FLOOR ADD | 0.456 | 0.530 | 0.977 | 0.978 | 0.00 | 0.00 | 0.968 | 0.868 | K1 K2 |
| $C_{\varphi J}$ FLOOR MOD | 0.456 | 0.530 | 0.992 | 0.997 | $-1.16$ | $-1.33$ | 0.970 | 0.868 | K1 K2 |
| $C_{\varphi J}$ SHRINK ADD | 0.524 | 0.501 | 0.944 | 0.946 | 11.62 | 11.62 | 0.938 | 0.808 | K1 K3 |
| $C_{\varphi J}$ SHRINK MOD | 0.524 | 0.501 | 0.991 | 0.995 | 7.99 | 7.58 | 0.974 | 0.808 | all |

The SHRINK candidates fail K1 and K3. Pulling a score toward the midpoint by mention count makes the shrinkage weight a function of the mention count, and the mention count is Presence; the result is a Consistency score that tracks Presence ($\rho = 0.715$ and $0.773$ for $C_\varphi$). Shrinkage also leaves low-count brands with substantial Consistency credit, which K3 catches: their composite advantage over never-named brands exceeds their Presence advantage by 8--12 points against a limit of 5.

Adding $J$ raises the reliability of the Consistency score ($0.868$ against $0.736$ under FLOOR) but moves it toward Presence: under FLOOR, $C_{\varphi J}$ sits at 0.456 at $t_1$ and crosses the K1 line at $t_2$ (0.530). A likely reason is that $J$ is defined only where at least two models name the brand, and the overlap of two frame sets drawn from six frames rises with their size, so $J$ partly re-expresses how often the brand is named.

## 4.2 The locked outcome

Under the selection rule, v1.9 locks no single composite. The program's next synthesis reports Presence and Consistency as two scores side by side. The Consistency score that enters reporting is $C_\varphi$ with FLOOR: $C^* = 100(1 - \varphi/7.2)$, rated only for brands with at least six total mentions across the panel, and not rated otherwise. It is the only Consistency score in the grid that passes K1 at both waves, so the choice involved no discretion; it is also more reliable over three weeks than raw $\varphi$ on the same rank basis (0.736 against 0.533), because the floor removes the low-count brands whose scores are noise. Its cost is coverage: 50.9% of brands at $t_1$ and 51.8% at $t_2$ are not rated, either because they were never named or because they were named fewer than six times.

## 4.3 Stage 2: blind confirmation on the third wave

All four parity gates of v0.41 passed, all 852 third-wave calls returned, and all six models were retained. Table 2 reports the Stage 2 verdicts.

\needspace{10\baselineskip}

Table: Stage 2 verdicts on $t_2 \rightarrow t_3$ (152 days), under the locked specification; hypotheses as defined in §3.3, in the same order. The composite is $C_\varphi$ FLOOR ADD. Within-substrate ranks.

| Hypothesis | Statistic | Value | $n$ | Rule | Verdict |
|----------------------------|:------------------|:-----:|:----:|:-------------------------|:-----------:|
| Presence reliability | $\rho(P_{t_2}, P_{t_3})$ | 0.954 | 112 | $\ge 0.80$, $p_{\text{perm}} < .05$ | CONFIRMED |
| Dissociation at $t_3$ | $\lvert\rho(C^*_{t_3}, P_{t_3})\rvert$ | 0.190 | 54 | $\le 0.30$ | CONFIRMED |
| Consistency reliability | $\rho(C^*_{t_2}, C^*_{t_3})$ | 0.647 | 52 | $\ge 0.50$, $p_{\text{frame}} < .05$ | CONFIRMED |
| No composite | $\rho(A, P)$ | 0.969 | 112 | K2 line 0.95 (descriptive) | above |

Presence kept its brand order over five months ($\rho = 0.954$, $p_{\text{perm}} = 0.0001$, the smallest value 10,000 draws can return). Consistency remained separable from Presence at $t_3$ ($|\rho| = 0.190$ over the 54 rated brands); the dissociation is somewhat weaker than at $t_1$ and $t_2$ (0.073, 0.082) but well inside the confirmation band. The Consistency score held its brand order ($\rho = 0.647$ over the 52 brands rated in both waves). Against the frame-structure null, shuffled versions averaged 0.438, with a 95th percentile of 0.585; 80 of 10,000 reached the observed value ($p_{\text{frame}} = 0.008$). Part of the score's stability therefore comes from the structure of the questions, as v0.41 found for raw $\varphi$, but the score is reliably more stable than that structure alone produces.

The descriptive check replicated the Stage 1 outcome: at $t_3$ the best FLOOR composite still ranked brands at $\rho(A, P) = 0.969$ with Presence, above the K2 line. K1 and K3 also held at $t_3$, and 51.8% of brands were not rated.

# 5. Discussion

The calibration answers the question it was designed to answer, and the answer is negative for a single score at this stage. With two components measured on this panel, a 0--100 composite of Presence and Consistency is, to within a few hundredths of a rank correlation, a relabelled Presence score. Reporting it would add a weighting convention without adding information, and it would hide the one thing the second component contributes: a reading of agreement among models that is unrelated to how often they name the brand.

Two features of the data produce this result, and neither is a defect of either component. The first is spread. Presence separates brands across almost its whole range; Consistency, among brands named often enough to rate, separates them within a narrower band. Equal weights do not give equal influence, and re-weighting Consistency upward would introduce a convention chosen to manufacture a result. The second is coverage. A Consistency score that means something needs mentions to work with, and about half of the brands in these categories do not have enough. For those brands, any composite has to fall back on Presence, which pulls it further toward Presence.

The calibration also settles a definitional question that matters independently of composition. Three natural ways of handling low-count brands were available. Shrinking toward the midpoint ties the score to Presence by construction; adding the positional diagnostic $J$ raises reliability but moves the score toward Presence; rating low-count brands as measured gives them a windfall from noise. A floor at six mentions avoids all three problems, at the cost of saying nothing about brands the panel rarely names. That cost is honest: for a brand named once or twice, the panel's agreement is not observable.

The blind confirmation strengthens the decision. Both reported scores held their brand order over five months, the Consistency score beat the frame-structure baseline, and the two stayed separable. The program can therefore report two reliable, separable scores, which is a stronger position than one composite that could not be shown to add information.

For the Tri-System framework, which describes AIAS as a multi-dimensional 0--100 score, the result is a constraint on timing rather than a contradiction. A composite becomes worth computing when a component is added that separates brands across a comparable range and is defined for the brands that Consistency cannot rate. Until then, side-by-side reporting is the measurement the data support.

# 6. Limitations

Stage 1 selects on data already seen, and is declared as calibration for that reason; only Stage 2 is confirmatory. The grid is small by design --- eight specifications fixed in advance --- and other forms (rank-based composites, re-weighted components, a different floor) were not tested; the conclusion is that none of the pre-specified forms adds information, not that no composite could. Presence was taken as locked, so the balance between recognition and recall inside it was not revisited. All results bind one panel: the six-model legacy panel, which is retiring, and whose models answer without web search; a new panel needs its own calibration. Five substrates and 112 brand units, with 16 to 24 brands per substrate, limit the precision of every correlation, and the Stage 2 Consistency tests rest on 52 and 54 brands. The confirmation interval is a single five-month interval on mature consumer categories. Finally, neither score has been validated against buyer behaviour; reliability and separability are necessary conditions for a useful measure, not evidence that it predicts market outcomes.

# 7. Future research

Three steps follow. First, the program's next synthesis reports Presence and Consistency side by side under the locked definitions, with the share of unrated brands reported alongside Consistency. Second, the calibration should be repeated on the current-generation panel, with web search off and on, before any score from that panel is compared with legacy-panel scores. Third, the composite question should be reopened when a third component is available: the calibration grid, constraints and selection rule defined here can be carried forward unchanged, so that a future composite is admitted or refused by the same rule.

# Declarations {-}

## Conflict of interest {-}

The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. This study re-analyses measurements taken against brand registries fixed in earlier phases (v0.19--v0.23); it performs no new brand selection, and each registry carries its source-phase conflict-of-interest handling forward unchanged. Two items of record apply. In the automotive registry, Samsung subsidiaries hold tier-2/3 component supply relationships with several registry brands --- Harman International (audio systems), Samsung SDI (battery cells), and Samsung Display (infotainment) --- characterized in the source phase as non-competitive, with no brand-level overlap, and imposing no operational restriction on registry composition (v0.22 Declarations; screened in v0.22 DEVIATIONS Entry 0, Part B). In the audiophile-headphones registry, AKG was substituted with Denon before the v0.19 pre-registration lock because AKG's parent, Harman International, is a Samsung subsidiary. Scoring is fully automated against the locked registries and the locked specification; the pre-registration was locked and deposited before any confirmation-wave data existed; and the author's affiliation played no role in registry construction, calibration, scoring, or the resulting verdicts. Samsung Electronics had no role in the design, conduct, analysis, or reporting of this work.

## Funding {-}

Self-funded. No external funding supported this research.

## Ethics {-}

Not applicable; no human subjects. The study analyses responses of large language models queried under their public interfaces.

## Data and code availability {-}

Materials are deposited at OSF, `ec6wh/methodology/v1_9`: the locked pre-registration with the Stage 1 calibration table, the anchor record (tag, commit and file hashes) and the deviations record. At publication the deposit adds the scorer (`score_v1_9.py`), the Stage 1 calibration output (`v1_9_calibration.json`), the Stage 2 verdicts (`v1_9_verdicts.json`) and the scoping script. The underlying waves are deposited with their source studies (OSF `ec6wh/v19`--`v23`, `v34`, `v41`).

# References {-}

González Castro, P. U. (2026). *AI Availability: Extending Mental and Physical Availability into Algorithmic Retrieval*. SSRN 6659000.

González Castro, P. U. (2026). *Tri-System Brand Growth: The AI Mediation Layer*. MSI Working Paper, Report No. 26-132. Marketing Science Institute.

González Castro, P. U. (2026). *The AIAS™ Presence Measurement Protocol: Methodological Notes on Construct Validity and the Four-Regime Taxonomy* (v1.2). SSRN 6761698.

González Castro, P. U. (2026). *The AIAS Presence Measurement Protocol: Phase A Pivot-Validation Specification* (v1.3). SSRN 6797679.

González Castro, P. U. (2026). *The AIAS Presence Measurement Protocol v1.4: Recognition × Recall Decomposition and Multi-Component AI Availability*. SSRN 6799479.

González Castro, P. U. (2026). *The AIAS™ Presence Measurement Protocol: Multi-Statistic C2 Specification and Two-Channel Recall Decomposition* (v1.5). SSRN 6810758.

González Castro, P. U. (2026). *Substrate Pre-Screening, Independent Moderator Pathway, and Phantom Brand Persistence Phase B Extension* (AIAS Methodology v1.6). SSRN 6816340.

González Castro, P. U. (2026). *The AIAS Presence Measurement Protocol: CPC Consistency --- A Pre-Registered Negative Result* (v1.7). SSRN 6878818.

González Castro, P. U. (2026). *A Mean-Independent Consistency Instrument for Cross-Model AI Presence: Redesigning CPC on a Quasi-Binomial Dispersion Basis* (AIAS Methodology v1.8). SSRN 6963359.

González Castro, P. U. (2026). *AI Availability as a Third Measurable Layer of Brand Availability: Five-Substrate Empirical Anchoring of the AIAS™ Presence Measurement Protocol* (AIAS 1.0). SSRN 6817841.

González Castro, P. U. (2026). *Two-Wave Temporal Stability of an AI Brand-Recall Consistency Quantity: A Pre-Registered Longitudinal Re-Acquisition Across Five Product Categories* (v0.34). SSRN 6915458.

González Castro, P. U. (2026). *Identity Load Does Not Moderate Cross-Model Consistency: A Pre-Registered Component-Dissociation Null* (v0.37). Working paper; OSF `ec6wh/v37`.

González Castro, P. U. (2026). *Five-Month Stability of AI Brand Consistency and Presence: A Pre-Registered Third Wave on a Retiring Six-Model Panel* (v0.41). Working paper; OSF `ec6wh/v41`.

González Castro, P. U. (2026). *AI Presence in Audiophile headphones: AIAS v0.19*. SSRN 6809182.

González Castro, P. U. (2026). *AI Presence in Skincare: AIAS v0.20*. SSRN 6811441.

González Castro, P. U. (2026). *AI Presence in Cosmetics: AIAS v0.21*. SSRN 6815378.

González Castro, P. U. (2026). *AIAS™ v0.22 --- Automotive Substrate: Phantom Brand Persistence on a Heritage-Saturated Category*. SSRN 6829118.

González Castro, P. U. (2026). *AIAS™ v0.23 --- Premium Spirits Substrate*. SSRN 6834298.

Romaniuk, J., & Sharp, B. (2022). *How Brands Grow, Part 2* (Revised ed.). Oxford University Press.

Sharp, B. (2010). *How Brands Grow: What Marketers Don't Know*. Oxford University Press.
