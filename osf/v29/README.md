# AIAS™ Measurement Program — v0.29 (CV.05)
## The Presence Component Is Construct-Valid: A Convergent–Discriminant (Campbell–Fiske) Baseline

**Verdict:** `H_CV_Baseline` **CONFIRMED** · Campbell–Fiske gap `C3 = 0.7409`
**Design class:** Synthesis (no acquisition)
**Protocol:** v1.6 · **Pre-registration:** `v0.29-prereg-r1` (commit `a66c8d8`) · **Scored:** `191a793`

---

### What this is

v0.29 (CV.05) is a **synthesis**. It performs no measurement — no probes, no new
panel, no new brand registry. It assembles two locked component verdicts into a
single multitrait–multimethod (MTMM) frame and computes one quantity, the
convergent–discriminant gap, to evaluate whether the Presence component (`C_P`)
of the AIAS™ (AI Availability Score) clears a Campbell–Fiske construct-validity
baseline.

A measure is construct-valid when it correlates with conceptually related measures
(convergent) and not with unrelated ones (discriminant). Each half had been
established separately; this synthesis evaluates the joint condition that defines
a baseline.

### Result

| Condition | Source | Value | Pass |
|---|---|---|---|
| C1 — convergent (`C_P` × Google Trends) | v0.25 `H_CV_Primary` | ρ = 0.7411, p = 3.4e-05, n = 24 | significant ✓ |
| C2 — discriminant (`C_P` × Amazon BSR) | v0.26 `H_PV_Pooled` | ρ = −0.0002, p = 0.998, n = 88 | \|ρ\| < 0.20, n.s. ✓ |
| C3 — Campbell–Fiske gap | computed here | \|0.7411\| − \|0.0002\| = 0.7409 | > 0 ✓ |
| **H_CV_Baseline** | C1 ∧ C2 ∧ C3 | — | **CONFIRMED** |

The realized gap (0.7409) exceeded the pre-registered point estimate (~0.55)
because the inherited discriminant coefficient landed near zero rather than near
the registered |ρ| < 0.20 ceiling. This is a forecast-versus-realization
observation; the pre-registration lock is untouched. **Predictive validity is not
claimed** (DEVIATIONS Entry 0): it requires a longitudinal t1→t2 external
criterion not yet in the pipeline, and is gated to a subsequent wave.

### Provenance (inherited, not re-derived)

| Leg | Phase | SSRN | Pre-reg | Instrument |
|---|---|---|---|---|
| Convergent | v0.25 | 6842138 | `v0.25-prereg-r1` | Google Trends (SerpAPI) |
| Discriminant | v0.26 | 6847678 | `v0.26-prereg-r2` | Amazon Best Sellers Rank |

The six-model reference panel and both external instruments are inherited as
published. No data were collected for v0.29; the inherited per-point data live
with their respective component deposits.

### Contents

- `README.md` — this file
- `papers/` — SSRN synthesis paper (PDF)
- `reports/` — Third System™ brand-format report (PDF)
- `figures/` — `chart_29_mtmm_gap.pdf`, `chart_29_convergent_scatter.pdf`
- `prereg/` — locked pre-registration content module + assembly spec
- `scripts/` — synthesis scorer and build pipeline (paper, charts, report)
- `data/` — `v29_verdicts.json` (the assembled MTMM matrix + verdict; the single computed output)

There is no `registries/` or acquisition `data/` for this phase — a synthesis has
neither.

### References

- SSRN paper: ssrn.com/abstract=6870778
- Convergent component: ssrn.com/abstract=6842138 · Discriminant component: ssrn.com/abstract=6847678
- Methodology: 6761698 · 6797679 · 6799479 · 6810758 · 6816340
- AIAS™ 1.0 synthesis: 6817841
- OSF project: osf.io/ec6wh

Campbell, D. T., & Fiske, D. W. (1959). *Psychological Bulletin, 56*(2), 81–105.
Cronbach, L. J., & Meehl, P. E. (1955). *Psychological Bulletin, 52*(4), 281–302.
