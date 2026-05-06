# Registries — schema notes

Registries in this folder follow one of two schemas, reflecting when each
category was first measured.

## v1.1 schema (v0.7+ categories)

Object with metadata wrapper:

```json
{
  "category": "household_goods_retail",
  "registry_version": "household_v1.0",
  "registry_date": "2026-05-03",
  "brands": [
    {"canonical": "...", "tier": "...", "aliases": [...]}
  ]
}
```

Files using v1.1 schema:
- `brands_household.json` (v0.7 BBB designed-for-test)
- `brands_skincare.json` (v0.6 reconstruction; original schema lost)
- `brands_knives.json` (v0.8, forthcoming)

## v0.6 schemas (mixed, preserved as-is)

Two minor variants in v0.6 originals, depending on when they were created:

**Variant A — bare list (`brands_pm.json`):**
```json
[
  {"canonical": "...", "tier": "...", "aliases": [...]}
]
```

**Variant B — partial wrapper (`brands_running.json`, `brands_oliveoil.json`,
`brands_finance.json`):**
```json
{
  "category": "Running Shoes",
  "brands": [...]
}
```
No `registry_version` field; category strings use display capitalization
rather than the canonical snake_case introduced in v1.1.

## Why we don't migrate

The v0.6 files document the actual brands.json state at measurement time.
Migrating them to v1.1 schema would erase history for negligible gain — the
v0.6 cross-category report has already shipped against these registries, and
no future measurement will use them as inputs (the runner reads from
`brands.json` at root, swapped per category).

When the runner is refactored to take a `--category` argument and read
`registries/brands_<cat>.json` directly, it should accept both schemas:

```python
data = json.load(open(registry_path))
brands = data if isinstance(data, list) else data['brands']
```

## Equivalent for prompts/

The same split exists in `prompts/`. Bare lists for v0.6 originals (running,
oliveoil, finance, pm), full v1.1 wrapper for household, skincare reconstruction,
and v0.8 onward.
