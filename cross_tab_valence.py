"""
AIAS Phase 2 — Cross-tab analysis of BBB valence + entity reference.

Reads:
  - manual_review_bbb_*.csv (110 BBB-classified rows)
  - results_enriched_household_v1.0_*.csv (288 base rows for denominators)

Computes:
  A. Valence × model_slot
  B. Entity_reference × model_slot
  C. Valence × CEP
  D. Valence × entity_reference (cross-tab)
  E. Per-slot adjusted Presence (naive / caveated / aware / total)
  F. Per-CEP adjusted Presence
"""
import csv
import glob
from collections import defaultdict, Counter
from datetime import datetime

# Find inputs
manual_review_files = sorted(glob.glob("manual_review_bbb_*.csv"))
# Filter out checkpoint
manual_review_files = [f for f in manual_review_files if "checkpoint" not in f]
MANUAL_CSV = manual_review_files[-1]

enriched_files = sorted(glob.glob("results_enriched_household_v1.0_*.csv"))
ENRICHED_CSV = enriched_files[-1]

print(f"Manual review:  {MANUAL_CSV}")
print(f"Enriched data:  {ENRICHED_CSV}")
print()

# Load classifications
with open(MANUAL_CSV, newline="", encoding="utf-8") as f:
    classifications = list(csv.DictReader(f))

# Compute run denominators from enriched
runs_per_slot = Counter()
runs_per_cep = Counter()
runs_per_slot_cep = defaultdict(Counter)
with open(ENRICHED_CSV, newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        if not r.get("raw_response", "").strip():
            continue
        slot = r.get("model_slot", "?")
        cep = r.get("cep", "?")
        runs_per_slot[slot] += 1
        runs_per_cep[cep] += 1
        runs_per_slot_cep[slot][cep] += 1

SLOTS = sorted(runs_per_slot.keys())
CEPS = sorted(runs_per_cep.keys())
VALENCES = ["live_recommendation", "live_with_caveat", "status_correction", "historical_reference", "ambiguous", "ERROR"]
ENTITIES = ["legacy_brand", "both", "corporate_parent", "unclear", "ERROR"]

print(f"Slots: {len(SLOTS)} ({sum(runs_per_slot.values())} runs)")
print(f"CEPs:  {len(CEPS)} ({sum(runs_per_cep.values())} runs)")
print(f"Classifications: {len(classifications)}")
print()
print("=" * 110)
print("AIAS PHASE 2 - BBB CROSS-TAB ANALYSIS")
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 110)


def percent(n, d):
    return (100.0 * n / d) if d > 0 else 0.0


# ============ A. VALENCE x SLOT ============
print()
print("-" * 110)
print("A. VALENCE x MODEL SLOT (count, % within slot's 48 runs)")
print("-" * 110)
val_slot = defaultdict(Counter)
for c in classifications:
    val_slot[c["model_slot"]][c["valence"]] += 1

# header
print(f"{'Slot':22s}", end="")
for v in VALENCES:
    print(f"{v[:12]:>14s}", end="")
print(f"{'Total':>10s}")
print("-" * 110)
for slot in SLOTS:
    runs = runs_per_slot[slot]
    print(f"{slot:22s}", end="")
    total = 0
    for v in VALENCES:
        n = val_slot[slot][v]
        total += n
        if n == 0:
            print(f"{'-':>14s}", end="")
        else:
            print(f"{n:>3d} ({percent(n, runs):>4.1f}%)", end="")
    print(f"  {total:>3d}/{runs}")


# ============ B. ENTITY x SLOT ============
print()
print("-" * 110)
print("B. ENTITY REFERENCE x MODEL SLOT (count, % within BBB-mention rows for that slot)")
print("-" * 110)
ent_slot = defaultdict(Counter)
slot_bbb_total = Counter()
for c in classifications:
    ent_slot[c["model_slot"]][c["entity_reference"]] += 1
    slot_bbb_total[c["model_slot"]] += 1

print(f"{'Slot':22s}", end="")
for e in ENTITIES:
    print(f"{e[:12]:>14s}", end="")
print(f"{'BBB rows':>10s}")
print("-" * 110)
for slot in SLOTS:
    bbb = slot_bbb_total[slot]
    print(f"{slot:22s}", end="")
    for e in ENTITIES:
        n = ent_slot[slot][e]
        if n == 0:
            print(f"{'-':>14s}", end="")
        else:
            print(f"{n:>3d} ({percent(n, bbb):>4.1f}%)", end="")
    print(f"  {bbb:>3d}")


# ============ C. VALENCE x CEP ============
print()
print("-" * 110)
print("C. VALENCE x CEP (count, % within CEP's 48 runs)")
print("-" * 110)
val_cep = defaultdict(Counter)
for c in classifications:
    val_cep[c["cep"]][c["valence"]] += 1

print(f"{'CEP':22s}", end="")
for v in VALENCES:
    print(f"{v[:12]:>14s}", end="")
print(f"{'Total':>10s}")
print("-" * 110)
for cep in CEPS:
    runs = runs_per_cep[cep]
    print(f"{cep:22s}", end="")
    total = 0
    for v in VALENCES:
        n = val_cep[cep][v]
        total += n
        if n == 0:
            print(f"{'-':>14s}", end="")
        else:
            print(f"{n:>3d} ({percent(n, runs):>4.1f}%)", end="")
    print(f"  {total:>3d}/{runs}")


# ============ D. VALENCE x ENTITY ============
print()
print("-" * 110)
print("D. VALENCE x ENTITY REFERENCE (count, % within row total)")
print("    Tests whether 'both' mentions correlate with caveat/correction (rebrand-aware)")
print("-" * 110)
val_ent = defaultdict(Counter)
total_rows = len(classifications)
for c in classifications:
    val_ent[c["valence"]][c["entity_reference"]] += 1

print(f"{'Valence':22s}", end="")
for e in ENTITIES:
    print(f"{e[:12]:>14s}", end="")
print(f"{'Total':>10s}")
print("-" * 110)
for v in VALENCES:
    row_total = sum(val_ent[v].values())
    if row_total == 0:
        continue
    print(f"{v:22s}", end="")
    for e in ENTITIES:
        n = val_ent[v][e]
        if n == 0:
            print(f"{'-':>14s}", end="")
        else:
            print(f"{n:>3d} ({percent(n, row_total):>4.1f}%)", end="")
    print(f"  {row_total:>3d}")


# ============ E. PER-SLOT ADJUSTED PRESENCE ============
print()
print("-" * 110)
print("E. PER-SLOT ADJUSTED PRESENCE (denominator = 48 runs per slot)")
print()
print("    naive_phantom    = live_recommendation only (AI treats BBB as fully live)")
print("    caveated_phantom = live_with_caveat (AI surfaces BBB, discloses closure)")
print("    aware            = historical_reference + status_correction (AI doesn't recommend)")
print("    raw_presence     = aggregate from analyze_v3 (any BBB mention, ignoring valence)")
print("-" * 110)
print(f"{'Slot':22s}{'naive%':>10s}{'caveated%':>12s}{'aware%':>10s}{'naive+cav%':>12s}{'raw%':>10s}")
print("-" * 110)
for slot in SLOTS:
    runs = runs_per_slot[slot]
    naive = val_slot[slot]["live_recommendation"]
    caveat = val_slot[slot]["live_with_caveat"]
    aware = val_slot[slot]["historical_reference"] + val_slot[slot]["status_correction"]
    total_bbb = slot_bbb_total[slot]
    print(f"{slot:22s}"
          f"{percent(naive, runs):>9.1f} "
          f"{percent(caveat, runs):>11.1f} "
          f"{percent(aware, runs):>9.1f} "
          f"{percent(naive+caveat, runs):>11.1f} "
          f"{percent(total_bbb, runs):>9.1f}")


# ============ F. PER-CEP ADJUSTED PRESENCE ============
print()
print("-" * 110)
print("F. PER-CEP ADJUSTED PRESENCE (denominator = 48 runs per CEP, across 6 slots)")
print("-" * 110)
print(f"{'CEP':22s}{'naive%':>10s}{'caveated%':>12s}{'aware%':>10s}{'naive+cav%':>12s}{'raw%':>10s}")
print("-" * 110)
cep_bbb_total = Counter()
for c in classifications:
    cep_bbb_total[c["cep"]] += 1
for cep in CEPS:
    runs = runs_per_cep[cep]
    naive = val_cep[cep]["live_recommendation"]
    caveat = val_cep[cep]["live_with_caveat"]
    aware = val_cep[cep]["historical_reference"] + val_cep[cep]["status_correction"]
    total_bbb = cep_bbb_total[cep]
    print(f"{cep:22s}"
          f"{percent(naive, runs):>9.1f} "
          f"{percent(caveat, runs):>11.1f} "
          f"{percent(aware, runs):>9.1f} "
          f"{percent(naive+caveat, runs):>11.1f} "
          f"{percent(total_bbb, runs):>9.1f}")


# ============ HEADLINE RECAP ============
naive_total = sum(val_slot[s]["live_recommendation"] for s in SLOTS)
caveat_total = sum(val_slot[s]["live_with_caveat"] for s in SLOTS)
aware_total = sum(val_slot[s]["historical_reference"] + val_slot[s]["status_correction"] for s in SLOTS)
total_runs = sum(runs_per_slot.values())

print()
print("=" * 110)
print("HEADLINE RECAP")
print("-" * 110)
print(f"  Total measurements:        {total_runs}")
print(f"  BBB mentions (any kind):   {len(classifications):>4d}  ({percent(len(classifications), total_runs):>5.1f}%) <- raw Presence")
print(f"    naive phantom:           {naive_total:>4d}  ({percent(naive_total, total_runs):>5.1f}%) <- AI presents BBB as fully live, no caveat")
print(f"    caveated phantom:        {caveat_total:>4d}  ({percent(caveat_total, total_runs):>5.1f}%) <- AI surfaces BBB but discloses closure/rebrand")
print(f"    aware (no recommend):    {aware_total:>4d}  ({percent(aware_total, total_runs):>5.1f}%) <- AI mentions BBB only as past/closed")
print()
print("  Reframed phantom rate (naive + caveated):")
print(f"    {percent(naive_total + caveat_total, total_runs):>5.1f}% of all measurements")
print(f"    {percent(naive_total + caveat_total, len(classifications)):>5.1f}% of BBB-containing responses")
print("=" * 110)


# ============ SAVE TO CSV ============
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
out_path = f"cross_tab_valence_{timestamp}.csv"
with open(out_path, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["analysis", "row_label", "col_label", "count", "denominator", "percent"])
    # A
    for slot in SLOTS:
        for v in VALENCES:
            w.writerow(["A_valence_x_slot", slot, v, val_slot[slot][v], runs_per_slot[slot],
                        round(percent(val_slot[slot][v], runs_per_slot[slot]), 2)])
    # B
    for slot in SLOTS:
        for e in ENTITIES:
            w.writerow(["B_entity_x_slot", slot, e, ent_slot[slot][e], slot_bbb_total[slot],
                        round(percent(ent_slot[slot][e], slot_bbb_total[slot]), 2)])
    # C
    for cep in CEPS:
        for v in VALENCES:
            w.writerow(["C_valence_x_cep", cep, v, val_cep[cep][v], runs_per_cep[cep],
                        round(percent(val_cep[cep][v], runs_per_cep[cep]), 2)])
    # D
    for v in VALENCES:
        row_total = sum(val_ent[v].values())
        for e in ENTITIES:
            w.writerow(["D_valence_x_entity", v, e, val_ent[v][e], row_total,
                        round(percent(val_ent[v][e], row_total), 2) if row_total else 0])
    # E
    for slot in SLOTS:
        runs = runs_per_slot[slot]
        naive = val_slot[slot]["live_recommendation"]
        caveat = val_slot[slot]["live_with_caveat"]
        aware = val_slot[slot]["historical_reference"] + val_slot[slot]["status_correction"]
        w.writerow(["E_adj_presence_slot", slot, "naive", naive, runs, round(percent(naive, runs), 2)])
        w.writerow(["E_adj_presence_slot", slot, "caveated", caveat, runs, round(percent(caveat, runs), 2)])
        w.writerow(["E_adj_presence_slot", slot, "aware", aware, runs, round(percent(aware, runs), 2)])
        w.writerow(["E_adj_presence_slot", slot, "raw_total", slot_bbb_total[slot], runs,
                    round(percent(slot_bbb_total[slot], runs), 2)])

print()
print(f"Saved cross-tab data: {out_path}")
