# AIAS v0.44 — DEVIATIONS log

Industry-breadth wave on the newest models. Entries are numbered; Entry 0 is the pre-acquisition conflict-of-interest screen required for every phase. It documents how conflicts are handled; it is not a blanket "no affiliation" finding.

---

## Entry 0 — Samsung-group conflict-of-interest screen (pre-acquisition; written 2026-11-10, DRAFT r0, before any study call)

**Context.** The pre-registrant is Director, Corporate Brand Creative and Governance at Samsung Electronics America. The registries of this wave are new (eight industries, 159 units, `osf/v44/registries/`), so the screen covers brand selection itself, not a carried-forward registry. Rules applied (programme rules of 2026-11-09 and 2026-11-10): categories in which Samsung competes (phones, TVs, appliances, semiconductors, displays) stay out or are screened first; every brand is screened for Samsung-group ownership; Samsung may appear only in a paper's Declarations §COI; independence rule for public studies (no focal brand, no lessons addressed to a brand, no brand contacted).

**Samsung-group list screened against.** Samsung Electronics; Harman International and its brands (among them JBL, AKG, Harman Kardon, Infinity, Mark Levinson, Revel, Arcam, Lexicon); the Sound United brands Harman acquired from Masimo on 2025-09-23 (among them Denon, Marantz, Bowers & Wilkins, Polk Audio, Definitive Technology, Boston Acoustics, Classé); Samsung affiliates Cheil Worldwide, Samsung Life, Samsung Fire & Marine, Samsung C&T (including its fashion business), Hotel Shilla (The Shilla, Shilla Stay, Shilla Duty Free), and Samsung Bioepis (found during this screen, Part C).

### Part A — Brand ownership (all 159 units)

Each unit's owner was read from the registry source entity (column `source_entity`: NAIC group, retailer, chain or brand owner as named by the source) and checked by name against the list above. **Result: no registry unit is a Samsung-group brand or is owned by a Samsung-group company.** Column `samsung_group_owned` = `no` for every row. Method limit: ownership rests on the source entity names and the name check; no ownership filing was opened per brand.

### Part B — Industries in which a Samsung-group company competes

| Industry | Samsung-group activity | Handling |
|---|---|---|
| Car insurance (INS) | Samsung Fire & Marine (property-casualty) and Samsung Life are Samsung affiliates in insurance, outside the US consumer car-insurance market | Neither appears among the NAIC top 25 private passenger auto groups (2024 data), the registry source; no group brand in the registry. Disclosed; no restriction on composition. |
| Hotel chains (HOT) | Hotel Shilla operates hotels (The Shilla, Shilla Stay) | Not a US brand in either registry source; listed in `excluded_v0_44.csv` and would be excluded on COI grounds in any case. Disclosed. |
| Fashion and luxury (FAS) | Samsung C&T's fashion business sells its own brands and distributes imported brands in Korea: Ami, Maison Kitsuné, Lemaire (Asia Economy, https://www.asiae.co.kr/en/article/2022122110051040460 and https://www.asiae.co.kr/en/article/2021111900272804715, accessed 2026-11-10); its Thom Browne distribution ended in 2023 (https://www.asiae.co.kr/en/article/2023012710501841446) | None of these brands is a registry unit; the registry comes from Interbrand 2026 and the Lyst Index Q3 2026 by rule. Open item: whether Samsung C&T's multi-brand stores or Shilla Duty Free retail any registry brand was not screened from a public source; to be disclosed generally. |
| Grocery, fast food, clothing and department stores, convenience and fuel | No Samsung-group company identified in the US category by this screen | None. |

**Industries not selected on COI grounds** (from the programme's candidate list): telecom (Samsung Electronics sells phones through US carriers and is a network-equipment supplier to them; phones are a Samsung category) and media and streaming (Samsung TV Plus is Samsung Electronics' own streaming service). Phones, TVs, appliances, semiconductors and displays are not measured. Health and pharma: pharmaceutical manufacturers were not selected because a Samsung affiliate (Samsung Bioepis) markets biosimilars that compete with originator products; pharmacies were selected and screened (Part C).

### Part C — Supply relationship disclosed (pharmacies)

Samsung Bioepis, a Samsung affiliate, developed the ustekinumab biosimilar Pyzchiva (commercialised in the US by Sandoz) and supplies private-label versions through Cordavis, a CVS Caremark subsidiary, and Quallent, an Express Scripts subsidiary; CVS Caremark and Express Scripts placed Pyzchiva on their formularies in 2026 (Pearce IP, 2026-07-13: https://www.pearceip.law/2026/07/13/samsung-bioepis-secures-preferred-formulary-status-for-biosimilar-to-janssens-stelara-ustekinumab-with-2-us-pbms/, accessed 2026-11-10). Two registry units, **CVS Pharmacy (PHA01)** and **Express Scripts (PHA03)**, therefore have a commercial supply relationship with a Samsung affiliate. Characterisation: a supplier relationship at the level of a specialty drug, non-competitive, with no brand-level overlap. Proposed handling, following the v0.22 precedent for tier-2/3 supply relationships: disclose in Declarations §COI; no operational restriction on registry composition. **Decision for the pre-registrant before the lock:** keep the pharmacy industry with this disclosure (the draft's default) or drop it (seven industries; cost falls by about $3.8 central). *r1 update (2026-11-10): the drop is pre-specified in PRE_REGISTRATION_v0_44.md §3.4 (807 calls; at November prices the central estimate falls from $27.24 to $24.06, $3.18; at December prices from $30.10 to $26.59; `cost_estimate_v0_44.py`), with a seven-industry COI text in §8.*

### Part D — Other relationships and independence

- **Cheil Worldwide** (Samsung affiliate, advertising, sells AI-visibility work) is not a registry unit and is not a probe. Whether it serves any registry brand as a client was not screened (client lists are not public); disclosed generally.
- **Retail channel.** Several excluded retailers (mass merchants, clubs, home-improvement chains) sell Samsung products; they were excluded on industry-definition grounds, recorded in `excluded_v0_44.csv`. Retained units Walmart Pharmacy and Costco Pharmacy (pharmacy industry) belong to companies that also retail Samsung products; disclosed generally, no restriction.
- **Independence rule.** No unit is focal; tiers come from public rankings by fixed rules; no lesson is addressed to a brand; no brand has been or will be contacted.

**Samsung in the paper.** Samsung appears only in the Declarations §COI of the v0.44 paper (draft text in PRE_REGISTRATION_v0_44.md §8).
