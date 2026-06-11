# v0.35 reused registries — pointers

v0.35 is a re-analysis of the frozen t₁ inputs of five omnibus substrates. There is no
new brand selection: each substrate's registry is the bit-identical lock from its source
phase, **referenced, not re-locked**. Canonical sources in the program repository:

- **v0.19 audiophile headphones (16 brands)** — locked v0.19 phase (`osf/v19/`; AKG→Denon
  substitution made before the v0.19 pre-registration lock, per the v0.19 record).
- **v0.20 skincare (24)** — `prereg/v0_20_registry.json`
- **v0.21 cosmetics (24)** — `prereg/v0_21_registry.json`
- **v0.22 automotive (24)** — `prereg/v0_22_registry.json` (+ `prereg/v0_22_automotive_content.py`)
- **v0.23 premium spirits (24)** — `prereg/v0_23_premium_spirits_content.py`

Each registry's conflict-of-interest handling is carried forward from its source phase
unchanged (v0.22 tier-2/3 component-supply disclosure — Harman International / Samsung SDI /
Samsung Display; v0.19 AKG→Denon substitution). Per program convention that disclosure lives
only in the SSRN paper's Declarations §COI, never in this deposit.
