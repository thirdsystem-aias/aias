# COI screen — combined v0.27 + v0.28 validity paper (program study #67)

**Date:** November 10, 2026
**Scope:** every brand named in the combined paper's tables, figures or text: the v0.27 panel (24 B2B SaaS brands, `osf/v27/registries/v27_registry.json`, inherited verbatim from v0.24) and the v0.28 panel (24 Technology brands, `prereg/v0_28_panel_brands.txt`, frozen at tag `v0.28-prereg-r1`).
**Screen list:** Samsung Electronics and the Samsung group: Harman International and its brands (JBL, AKG, Harman Kardon and others), Denon and the other Sound United brands (Harman-owned since September 23, 2025; CLAUDE.md "Denon / Harman"), Samsung SDI, Samsung Display, Samsung SDS, Samsung Biologics, SmartThings, Cheil Worldwide. Second pass: brands that compete directly with Samsung in its product categories (phones, tablets, PCs, TVs, monitors, appliances, memory and storage, displays) and brands with a known financial or commercial tie to a Samsung group company.
**Source records conformed to:** v0.28 DEVIATIONS Entry 0 (`prereg/v0_28_tech_brand_discriminant_content.py`, tag `v0.28-prereg-r1`); v0.27 locked paper Declarations (`papers/v0_27/v0_27_convergent_validity_DRAFT.md`).

## Result

**No Samsung-group brand is a panel brand in either leg.** The paper can proceed; Samsung is named only in Declarations §COI.

- **v0.27 (B2B SaaS, n = 24):** Salesforce, HubSpot, ServiceNow, Workday, SAP, Oracle, Zendesk, Notion, Figma, Linear, Airtable, Slack, Miro, Datadog, Snowflake, Stripe, Twilio, Cloudflare, MongoDB, Quip, Yammer, Wunderlist, HipChat, Stride. No Samsung-group brand. No brand competes with Samsung in its product categories. Parent-level note only: Yammer and Wunderlist are Microsoft products (Microsoft competes with Samsung in PCs and tablets); Samsung SDS sells enterprise IT and collaboration software, adjacent to some panel brands. Neither is material to a recall-share measurement; not disclosed brand by brand.
- **v0.28 (Technology, n = 24):** Google, Apple, Netflix, Microsoft, Instagram, Uber, Airbnb, Dell Technologies, Whirlpool, 3M, QVC, Motorola Solutions, Seagate Technology, Corning, VMware, Pitney Bowes, Thermo Fisher Scientific, Flex, HPE, CDW, NetApp, Jabil, Lam Research, Parker-Hannifin. No Samsung-group brand. Harman International (Samsung-owned) was in the 70-brand usable frame and was removed at frame level before the seeded tertile draw (v0.28 DEVIATIONS Entry 0; frame 80 → 70 → 69). Motorola Solutions is the independent public-safety and enterprise-communications company, not the Motorola phone brand.

## Flags (v0.28 panel)

| Brand | Relationship to Samsung | Handling |
|---|---|---|
| Apple | Direct competitor (phones, tablets, PCs, wearables) | Disclosed in §COI |
| Google | Direct competitor (Pixel phones, tablets, watches); also Android platform partner | Disclosed in §COI |
| Microsoft | Competitor (Surface PCs and tablets); also software partner | Disclosed in §COI |
| Dell Technologies | Competitor (PCs, monitors) | Disclosed in §COI |
| Whirlpool | Direct competitor (home appliances) | Disclosed in §COI |
| Seagate Technology | Competitor (data storage; Samsung sells SSDs) | Disclosed in §COI |
| Corning | Samsung Display is a significant minority shareholder (about 9% of common shares after an April 2021 conversion, committed to remain a significant shareholder until at least 2028; Corning news release, April 5, 2021, corning.com). Not Samsung-controlled, so not a Samsung-group brand. | Disclosed in §COI; **open question for Pablo** (see below) |
| Thermo Fisher Scientific | Competes with a Samsung affiliate (Samsung Biologics) in contract drug development and manufacturing; not a Samsung Electronics category | Covered by the general disclosure in §COI |
| Lam Research, Flex, Jabil, CDW, HPE, NetApp | Supply-chain or channel relationships with Samsung companies are possible (semiconductor equipment, contract manufacturing, IT resale, servers and storage); not verified individually | Covered by the general disclosure in §COI |
| Netflix, Instagram, Uber, Airbnb, 3M, QVC, VMware, Pitney Bowes, Parker-Hannifin, Motorola Solutions | No relationship identified | None |

Mitigation that applies to every flag: the v0.28 panel was drawn by a fixed seed (280400), eight per familiarity tertile, from the screened BRAND Technology frame; no brand was chosen or excluded by the author after the frame screen. The v0.27 panel is the v0.24 registry, inherited verbatim. Presence for v0.28 was acquired blind and scored once.

## Notes

1. The v0.28 frame-level screen matched `samsung|harman|jbl|akg|smartthings`. It would not have caught Denon or other Sound United brands, Samsung SDI, Samsung Display or Cheil Worldwide by name. None of these is in the 24-brand panel (checked by name today). The completeness of the 69-brand frame against the longer list was not re-checked here (the BRAND workbook is not in this branch); this does not affect any brand named in the paper.
2. The v0.19 AKG → Denon disclosure is not carried into this paper (it concerns a different panel), so the Denon / Harman correction does not apply. v0.28's Entry 0 cites v0.19 only as procedural precedent.
3. Cheil Worldwide (a Samsung affiliate) sells AI-visibility services (CLAUDE.md, COI note of November 10, 2026). The v0.27 leg evaluates commercial AI-visibility instruments and draws a practitioner conclusion about their headline scores, so §COI states this relationship.
4. v0.28's original paper named Samsung in §2.2 of its method ("Samsung ownership"). The combined paper names only Harman in the method and keeps Samsung in §COI.

## Declarations §COI text used in the paper (verbatim)

The author is employed by Samsung Electronics America. Samsung had no role in the design, conduct, analysis or reporting of either study. Neither panel contains a Samsung-group brand: in Study 2, Harman International, a Samsung subsidiary, was removed from the eligible sampling frame by a pre-registered screen before the seeded draw. The Study 2 Technology panel includes brands that compete with Samsung in some product categories (Apple, Dell Technologies, Google, Microsoft, Seagate Technology, Whirlpool) and one brand in which a Samsung subsidiary holds a significant minority equity stake (Corning, in which Samsung Display is a shareholder); other panel brands may have supplier, customer or channel relationships with Samsung group companies. The panel was drawn by a fixed random seed within familiarity tertiles, and no brand was selected or excluded by the author after the screen. Study 1 evaluates commercial AI-visibility instruments; Cheil Worldwide, a Samsung affiliate, sells AI-visibility services. The author develops the AIAS measurement program through Third System. The author declares no other competing interests.

## Open questions for Pablo

1. **Corning (Samsung Display shareholding).** Default: keep Corning in the paper (removing a seeded panel brand after scoring would alter locked results) and disclose the stake in §COI as above.
2. **Cheil Worldwide and the AIAS program as competing interests for the v0.27 leg.** Default: keep both one-line disclosures.
