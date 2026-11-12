> SYNTHETIC DATA (dry run). These numbers describe made-up data with a known answer.

# v1.17 results note: how many runs are enough (exploratory)

## Runs needed, by category size

- All brands (n = 672 units, 30 answer cells): one run's standard error 0.148; three runs 0.086. Below 0.10: 3 runs (95% interval 2–3); below 0.05: 9 runs (95% interval 8–10), assuming independent runs with the same variance as t4's three.
- 24-brand categories (n = 576 units, 24 answer cells): one run's standard error 0.150; three runs 0.086. Below 0.10: 3 runs (95% interval 2–3); below 0.05: 9 runs (95% interval 8–10), assuming independent runs with the same variance as t4's three.
- 16-brand category (v0.19) (n = 96 units, 6 answer cells): one run's standard error 0.139; three runs 0.080. Below 0.10: 2 runs (95% interval 2–3) (interval flagged: fewer than 10 clusters); below 0.05: 8 runs (95% interval 7–10) (interval flagged: fewer than 10 clusters), assuming independent runs with the same variance as t4's three.

Without Denon and the five brands with agency ties (S-COI):
- All (n = 672 units, 30 answer cells): one run's standard error 0.148; three runs 0.086. Below 0.10: 3 runs (95% interval 2–3); below 0.05: 9 runs (95% interval 8–10), assuming independent runs with the same variance as t4's three.
- 24-brand (n = 576 units, 24 answer cells): one run's standard error 0.150; three runs 0.086. Below 0.10: 3 runs (95% interval 2–3); below 0.05: 9 runs (95% interval 8–10), assuming independent runs with the same variance as t4's three.
- 16-brand (n = 96 units, 6 answer cells): one run's standard error 0.139; three runs 0.080. Below 0.10: 2 runs (95% interval 2–3) (interval flagged: fewer than 10 clusters); below 0.05: 8 runs (95% interval 7–10) (interval flagged: fewer than 10 clusters), assuming independent runs with the same variance as t4's three.

## By how often a brand is named

- zero: n = 156 units; one run's standard error 0.000.
- low: n = 178 units; one run's standard error 0.153.
- middle: n = 225 units; one run's standard error 0.196.
- high: n = 105 units; one run's standard error 0.138.
- full: n = 8 units; one run's standard error 0.000.

## Other scales

- Per question (frame level) (n = 4,032 unit-question pairs, 30 answer cells): one run's standard error 0.362; three runs 0.209. Below 0.10: 14 runs (95% interval 13–14); below 0.05: 53 runs (95% interval 50–55), assuming independent runs with the same variance as t4's three.
- Three-model panel (published N3 Presence) (n = 224 brand-condition pairs, 10 answer cells): one run's standard error 0.089; three runs 0.052. Below 0.10: 1 run (95% interval 1–1); below 0.05: 4 runs (95% interval 3–4), assuming independent runs with the same variance as t4's three.
- Per unit, from its own three runs (2 degrees of freedom each): 517 of 672 units have a three-run standard error below 0.10 and 197 below 0.05; 197 did not move at all.

## Measured once instead of three times

- Per model: 856 of 2,016 brand-runs change place against at least one brand (42.5%); 862 of 22,032 pairs reverse (3.9%).
- Three-model panel: 311 of 672 brand-runs (46.3%); 279 of 7,344 pairs reverse (3.8%).
- Recall floor, search off: 37 of 112 brands below it with three runs; one run alone would change the status of 6 (run 1), 2 (run 2), 2 (run 3) (mean 3.3).
- Recall floor, search on: 40 of 112 brands below it with three runs; one run alone would change the status of 6 (run 1), 8 (run 2), 9 (run 3) (mean 7.7).
- Of 516 units named at least once in three runs, a single run would show 67, 60, 58 (runs 1, 2, 3) as never named.

## Omnibus waves (time drift plus run noise; legacy models; never pooled with t4)

- All (n = 672 units): wave-to-wave standard deviation 0.167 (95% interval 0.161–0.174).
- 24-brand (n = 576 units): wave-to-wave standard deviation 0.169 (95% interval 0.162–0.177).
- 16-brand (n = 96 units): wave-to-wave standard deviation 0.155 (95% interval 0.143–0.164).
- Half mean squared change: t1→t2 0.027, t2→t3 0.029, t1→t3 0.029 (all units).

## What v0.40 should check (recommendation only; v0.40's own pre-registration decides)

- At 3 runs per cell, v1.17 suggests a per-model standard error of about 0.086 (95% interval 0.081–0.090), assuming independent runs with the same variance as t4's three; enough for 0.10 and not enough for 0.05.
- Legacy arm (one call per probe and model): t4 has no legacy runs; the omnibus figures above mix drift and noise and are not a run-to-run estimate for it.
