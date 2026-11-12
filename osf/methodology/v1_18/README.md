# v1.18 — Grounding under four competing definitions

Exploratory re-analysis beside v1.13 (Grounding Paper A) on t4's search-on category answers (v0.42; three runs per cell on N3). It asks how much Grounding's headline share depends on what counts as the brand's: its own domain only (K, as Kumar), any company's site (P, as Profound), its own site plus listings (Y, as Yext), or everything it does not own (M, as Muck Rack). v1.13's locked tests and verdicts are unchanged.

Status: pre-registration r1 final (2026-11-12), locked at tag `v1.18-prereg-r1` with the OSF deposit of `prereg/` and `registries/` (`methodology/v1_18`); audit done before the lock (pre-registration §4.4). The real run follows the lock, once.

## Run

```
python3 -m unittest discover -s osf/methodology/v1_18/scripts/tests -v                  # tests (synthetic)
python3 osf/methodology/v1_18/scripts/analyse_v1_18.py --synthetic --n-boot 2000         # dry run, known answer
python3 osf/methodology/v1_18/prereg/write_manifest_v1_18.py                             # manifest (re-run at lock)
python3 osf/methodology/v1_18/scripts/analyse_v1_18.py --run \
  --t4 ~/aias/_worktrees/v0.42/osf/v42/data/t4_raw.jsonl \
  --coded ~/aias/_worktrees/v0.42/osf/v42/data/coded                                     # refuses until the lock
```

Pre-lock only (already run once, declared): `scripts/extract_domains_v1_18.py --t4 …` (counts and blind domain lists), `registries/build_domain_table_v1_18.py`, `registries/draw_audit_sample_v1_18.py`.

## Files

See pre-registration §14. Code re-uses v1.13's parser and record selection by importing `osf/methodology/v1_13/scripts/score_v1_13.py` read-only.
