# v1.12 Coverage Paper A: CEP sets and the procedure that produced them

DRAFT r1 (2026-11-10), sent to Pablo for the 24-hour review. **Not locked.** Written before any v1.12 answer exists. No model API call was used to generate, test or screen any situation. Exact probe wording: `probes_v1_12.md` (generated from the same table by `build_probes_v1_12.py`).

## 1. Framework

A category entry point (CEP) is a buying situation that brings the category to mind, in the Ehrenberg-Bass sense (Romaniuk & Sharp 2016, *How Brands Grow: Part 2*, Oxford University Press). The cue list is the program’s own operationalisation of category entry points after Romaniuk & Sharp: seven cue types, labelled W: **why** (need or motive), **when** (time, season, occasion, life stage), **where** (place of use), **while** (concurrent activity), **with whom** (social context, including buying for someone), **with what** (products or settings used together), **how feeling** (emotional or physical state).

The archive has no designed CEP set (archive inventory, Nov 10: only six frames per category, which are Presence's frames). The inventory names "Phase Q's taxonomy step" as an input; no Phase Q document was found on any branch or in the project docs at this draft (open question Q12 in the pre-registration). This procedure does not depend on it.

## 2. Procedure (rules fixed before drafting; every CEP satisfies all of them)

- **R1 One cue.** Each CEP instantiates exactly one cue type (W).
- **R2 Fixed count and balance.** Exactly **2 CEPs per W per category = 14 per category, 70 in all**. The two CEPs of a W are labelled A and B; half A (7 CEPs, one per W) and half B (7) are the pre-declared split halves for the reliability leg (H4).
- **R3 Wording.** One first-person sentence in plain US English, **at most 20 words** (drafted: 7 to 17), describing the buyer's situation only, followed by the fixed question sentence of `probes_v1_12.md`.
- **R4 Brand-free.** No brand, product line, model, retailer, person, publication, competition or award. Checked by `build_probes_v1_12.py` against the canonical names of all 112 registry units plus a list of non-registry names (Samsung, Galaxy, AKG, JBL, Harman, Apple, AirPods, Bose, Beats): **0 hits**. The check is re-run at lock with every registry alias (MC_BrandFree).
- **R5 No segment labels.** No registry cell label or near-synonym (prestige, luxury, celebrity, cult, viral, clinical, dermatologist, drugstore, mass, heritage, disruptor, defunct, craft), no country of origin, and no product sub-type that is part of a registry entry's definition (no spirit type such as whisky, tequila or gin; no "electric car" or "SUV"), so that no CEP points at one registry brand or cell. Price wording is allowed only as a buyer's constraint ("on a tight budget", "without overspending"), never as a tier name.
- **R6 Not a Presence frame.** No expert, critic, reviewer, professional, celebrity, influencer, popularity, cult, heritage, prestige, status or cultural-icon cue, and no superlative about brands ("best", "most famous", "top"): those are the omnibus Phase B frames that Presence already asks.
- **R7 Category-wide.** The situation must be one in which a buyer of the substrate's category, as named by its category noun, could plausibly be shopping. The category noun is taken from the substrate's first Phase B frame (v0.19 "audiophile headphones"; v0.20 "skincare"; v0.21 "cosmetics", the noun of its frames q1, q3 and q4, while q2, q5 and q6 say "makeup"; v0.22 "car"; v0.23 "premium spirits").
- **R8 Category-specific constraints (declared).** (a) Automotive asks for brands to buy **new**, so a defunct brand (v0.22 cell D) is never a correct answer and serves as a known-group check (MC_Defunct); used-car situations are excluded. (b) Headphone situations stay inside audiophile listening: no sport, gym, commuting-with-noise-cancelling or true-wireless uses, which lie outside the substrate's category and are where Samsung-owned brands compete (conflict-of-interest care; §8 of the pre-registration).
- **R9 Responsible content.** No medical treatment or prescription claims (skincare, cosmetics); spirits situations involve adults at social or home occasions, never driving, minors or drinking to cope with stress.
- **R10 Authoring record.** Drafted on 2026-11-10 by the AIAS runner's sub-agent (Claude Opus 5.5, running in Claude Code) as plain text, with no API call to any panel model, before any v1.12 answer existed and without consulting any brand-level statistic. Registries were read only for category nouns, cell labels and spirit types (R5, R7). **Disclosure:** the drafting model is the same model as one panel arm (Claude Opus 5.5, C3). The CEPs name no brand and were never tried on any model; Pablo's review before lock is the human check, and Paper B's CEP-set sensitivity study uses an independently, human-authored set.
- **R11 Freeze.** Pablo may edit, replace or drop CEPs before the lock (each change logged in the pre-registration's change log, keeping R1 to R10 and the 2-per-W balance). At lock the table is frozen (SHA-256 of `probes_v1_12.jsonl` in the lock manifest); after lock no CEP changes.

**Reproducibility.** The rules, the cue-type definitions and the category nouns are sufficient for another team to draft a parallel set; the exact set used here is reproducible from `build_probes_v1_12.py` (one table, one generator). That a parallel set gives the same brand breadth ordering is a Paper B question (CEP-set sensitivity), not assumed here.

**Control probe (C0).** One situation-free probe per category (the question sentence alone), used only for MC_Situation. It is not a CEP and enters no Coverage statistic.

## 3. The CEP sets (14 per category; 70 in all)

### v0.19 audiophile headphones (16 registry brands)

| W | A | B |
|---|---|---|
| why | I want to hear every detail in my high-resolution music files. | I want my first serious pair of headphones without spending a fortune. |
| when | I do most of my listening late at night when the house is quiet. | I'm upgrading after several years with entry-level headphones. |
| where | I want headphones for long listening sessions in a quiet room at home. | I need headphones for a small home recording studio. |
| while | I want headphones to wear while working at my desk all day. | I want headphones for watching films at night without disturbing anyone. |
| with whom | I'm buying a gift for a relative who loves classical music. | I listen on my own for hours at a time, so comfort matters a lot to me. |
| with what | I'm pairing them with a dedicated headphone amplifier and DAC. | I'll plug them into a turntable and a vintage stereo receiver. |
| how feeling | I'm tired of headphones that sound harsh and fatigue my ears. | I want to treat myself after a long, stressful year. |

### v0.20 skincare (24)

| W | A | B |
|---|---|---|
| why | My skin is sensitive and reacts easily to new products. | I want to start a simple skincare routine on a tight budget. |
| when | Winter has arrived and my skin gets very dry. | My wedding is in three months and I want my skin to look its healthiest. |
| where | I spend long days outdoors and need to protect my skin from the sun. | I travel often and need products that fit in a carry-on bag. |
| while | I want a routine I can finish in five minutes while getting ready for work. | I work out every day and need skincare that keeps up with sweat and showers. |
| with whom | I'm buying a gift for my mother, who loves a pampering routine. | My teenage son is starting his first skincare routine. |
| with what | I want skincare that works well under my makeup. | I already use a retinol and want products that pair well with it. |
| how feeling | Lately my skin looks tired and dull. | I want to feel pampered and indulge myself a little. |

### v0.21 cosmetics (24)

| W | A | B |
|---|---|---|
| why | I want long-lasting makeup that stays put through a full working day. | I'm a student and need affordable makeup basics. |
| when | I'm doing my own makeup for my wedding day. | I'm getting ready for a night out this weekend. |
| where | I need makeup that holds up in hot, humid weather on a beach holiday. | I want a polished, natural look for the office. |
| while | I need to touch up my makeup on the go during busy days. | I film videos for social media and need makeup that looks good on camera. |
| with whom | I'm buying a first makeup gift for my teenage daughter. | I'm putting together a kit to do my friends' makeup for special events. |
| with what | I want makeup that layers well over my daily skincare and sunscreen. | I want a bold eye and lip look to go with a black-tie outfit. |
| how feeling | I want to feel confident before a big job interview. | I'm in the mood to try something bold and playful. |

### v0.22 automotive (24; question asks for brands to buy new)

| W | A | B |
|---|---|---|
| why | I need a dependable car that will be cheap to run for many years. | I want a car that is fun to drive on winding roads. |
| when | Our first child is due in a few months. | I'm about to retire and want a comfortable car for long road trips. |
| where | I live in a big city and need something easy to park. | Where I live, winters bring heavy snow and icy roads. |
| while | I commute more than an hour each way on the highway. | I need to tow a small boat on weekends. |
| with whom | I'm buying a first car for my newly licensed teenager. | We are a family of five with a large dog. |
| with what | I have solar panels at home and can charge a car in my garage. | I need room for camping gear and two bikes. |
| how feeling | After a recent accident, feeling safe matters more to me than anything else. | I want a car that feels calm and quiet after stressful workdays. |

### v0.23 premium spirits (24)

| W | A | B |
|---|---|---|
| why | I want a bottle to sip slowly and enjoy neat. | I want something good for mixing cocktails at home without overspending. |
| when | I'm celebrating a big promotion this weekend. | It's the holiday season and I'm stocking up for the month. |
| where | I'm bringing a bottle to a backyard barbecue. | I'm setting up a small home bar from scratch. |
| while | I want something to enjoy while watching the big game. | I want something to sip while listening to records in the evening. |
| with whom | I'm buying a gift for my father-in-law, who appreciates fine spirits. | I'm hosting friends who like to try something new. |
| with what | I want a spirit to serve with dessert after dinner. | I want something to go with a cheese and charcuterie board. |
| how feeling | I want something comforting on a cold winter night. | I'm in the mood to treat myself to something special. |

## 4. Known soft spots for Pablo's review (during the 24-hour review)

1. Two CEPs touch a sub-segment through function rather than label (HP-WHERE-B home studio; AU-WHAT-A home charging). They keep R5 (no sub-type named) but will favour some registry cells; that is what situations do, and it is why Coverage is measured across 14 of them.
2. AU-WHEN-B "comfortable car for long road trips" and AU-FEEL-B "calm and quiet" are close in meaning; SK-FEEL-B and SP-FEEL-B are both self-treat cues (allowed: different categories).
3. CO-WHEN-A (own wedding makeup) and SK-WHEN-B (wedding skin) share an occasion across categories (allowed).
4. "How feeling" items are the hardest to keep free of brand-reputation cues; HP-FEEL-B, SK-FEEL-B, SP-FEEL-B ("treat myself") may elicit premium tiers more than other W.
