# v0.18 Verdict — Indie Fragrance / IL-Gradient

**Pre-reg tag:** `v0.18-prereg-r1`
**Protocol version:** `v1.4`
**Scored:** 2026-05-20T20:32:27.439518+00:00

---

## H_Regime4_indie_fragrance (within-phase substantive)

**Verdict:** `PARTIAL`
**Resolved at:** C3

C2 conditions met; C3 cells clearing ρ ≥ 0.5 = 1 < 2 required (clearing: ['cell_c_mass_prestige']; excluded for n < 5: [])

### Per-cell diagnostics

| Cell | n post-attrition | Top-2 share (C2) | Phase D ρ (C3) |
|---|---|---|---|
| cell_a_designer_niche | 8 | 0.446 | 0.247 |
| cell_b_indie_artisan | 8 | 1.000 | 0.434 |
| cell_c_mass_prestige | 8 | 0.688 | 0.615 |

**C2 — within-cell:** ✓ satisfied
  - threshold: `0.5`
  - cells_meeting_threshold: `['cell_b_indie_artisan', 'cell_c_mass_prestige']`

**C2 — IL-gradient separation:** ✓ satisfied
  - cell_b_top2_share: `1.0`
  - cell_c_top2_share: `0.6875`
  - separation: `0.3125`
  - min_required: `0.1`

**C3 — within-cell ranking coherence:** ✗ not satisfied
  - threshold_per_cell: `0.5`
  - cells_clearing: `['cell_c_mass_prestige']`
  - cells_excluded_n_floor: `[]`
  - min_cells_clearing_required: `2`

---

## H_IdentityLoad_moderator (three-leg joint v0.16 × v0.17 × v0.18)

**Joint verdict:** `PARTIAL`

- v0.16: `PARTIAL`
- v0.17: `FALSIFIED`
- v0.18: `PARTIAL`

Moderator operates but bounded; substrate-specific qualifications

---

## H_Recognition_Recall_dissociation_generalization (methodological)

**Verdict:** `DISSOCIATION_PARTIAL`

Cases present but cell-clustered (2/3 cells)

### Dissociation cases (9 total)

**cell_a_designer_niche** (3 cases):
  - Comme des Garçons Parfums: C_P=5/6, mentions=2/18
  - Memo Paris: C_P=6/6, mentions=0/18
  - Etat Libre d'Orange: C_P=6/6, mentions=1/18

**cell_b_indie_artisan** (6 cases):
  - D.S. & Durga: C_P=6/6, mentions=2/18
  - Boy Smells: C_P=5/6, mentions=0/18
  - Heretic Parfum: C_P=6/6, mentions=0/18
  - Vyrao: C_P=6/6, mentions=0/18
  - Phlur: C_P=5/6, mentions=0/18
  - Snif: C_P=5/6, mentions=0/18

**cell_c_mass_prestige**: 0 cases
