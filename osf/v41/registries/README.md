# v0.41 frozen references

Copies of the v1.8 outputs used by parity gates P1 and P2 (score_v41.py). They live on
branch v1.8 only, not on the v0.37+ line this phase branches from, so they are frozen here.

| File | Source | git blob | SHA-256 |
|---|---|---|---|
| v1_8_instrument_table.csv | branch v1.8, commit 21ce11c, osf/methodology/v1_8/ | 715870d8e50d311452242c69c96a550491edbfff | 2d0ea5e83b01a39d1b120fe75b79178b78c85a649837f0d40a473a38f041f6e6 |
| v1_8_verdicts.json | branch v1.8, commit 21ce11c, osf/methodology/v1_8/ | bc202b146fc27c02cf5c07e92ee56f16df91f92b | a280385f1868cfdff06d6c3dfae6eb4288fb1a6ad01129d6d23320a3b88b7e78 |

Extracted 2026-11-09 with `git show 21ce11c:osf/methodology/v1_8/<file>`. The scorer
checks both SHA-256 values before any gate runs.
