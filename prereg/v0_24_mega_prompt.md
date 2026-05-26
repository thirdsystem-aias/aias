# AIAS v0.24 — B2B SaaS Mega-Prompt
# Pre-registered at v0.24-prereg-r1
# Methodology: v1.6

## Substrate

B2B SaaS — 8th substrate family in the AIAS Presence Measurement Program.
Cross-vertical scope: enterprise incumbents, high-identity challengers,
infrastructure/developer platforms, and phantom (defunct/acquired) candidates.

## Model Panel (fixed from v0.17)

1. Claude Opus 4.5
2. Claude Sonnet 4.5
3. GPT-4o
4. GPT-4o-mini
5. Gemini 2.5 Flash
6. Gemini 2.5 Flash Lite

## Phase A — Recognition (24 brands × 6 models = 144 probes)

### Probe format

> Do you know the brand [BRAND]? What does it do?

### Brand list (run each against all 6 models)

**Cell A — Enterprise Incumbents:**
1. Salesforce
2. HubSpot
3. ServiceNow
4. Workday
5. SAP
6. Oracle
7. Zendesk

**Cell B — High-Identity Challengers:**
1. Notion
2. Figma
3. Linear
4. Airtable
5. Slack
6. Miro

**Cell C — Infrastructure / Developer Platform:**
1. Datadog
2. Snowflake
3. Stripe
4. Twilio
5. Cloudflare
6. MongoDB

**Cell D — Phantom Candidates:**
1. Quip
2. Yammer
3. Wunderlist
4. HipChat
5. Stride

## Phase B — Two-Channel Recall (6 probes × 6 models = 36 queries)

Each probe is run against all 6 models. Record all brands mentioned in each
response. Score per-brand recall rates (R_cat, R_cult) across the full output set.

### R_cat — Category Recall (6 probes)

1. "What are the leading B2B SaaS platforms?"
2. "What software-as-a-service tools do enterprises use?"
3. "What are the most important B2B software companies?"
4. "Name the top SaaS platforms for business."
5. "What B2B cloud software would you recommend for a company?"
6. "What are the major enterprise SaaS providers?"

### R_cult — Cultural Recall (6 probes)

1. "What B2B SaaS products have the most passionate user communities?"
2. "Which enterprise software brands are considered innovative or cool?"
3. "What SaaS tools do developers and product teams love?"
4. "What B2B software companies have cult-like followings?"
5. "Which SaaS brands are changing how teams work?"
6. "What enterprise software brands have strong brand identities?"

## Post-Acquisition Coding — Marketing-Language Coverage (MLC)

After Phase B acquisition, code each recall output for the presence of
marketing-language tokens (MLTs) from the locked dictionary below.

**MLC = proportion of Phase B outputs containing ≥ 1 MLT.**

### Locked MLT Dictionary

| Brand       | Marketing-Language Tokens                                   |
|-------------|-------------------------------------------------------------|
| Salesforce  | Customer 360, Trailblazer, Einstein (AI branding), Ohana    |
| HubSpot     | inbound marketing, flywheel, growth stack                   |
| ServiceNow  | Now Platform, workflow automation                           |
| Snowflake   | Data Cloud, data sharing economy                            |
| Notion      | all-in-one workspace, connected workspace                   |
| Figma       | design in the browser, multiplayer design                   |
| Airtable    | no-code, spreadsheet-database                               |
| Linear      | issue tracking for modern teams                             |

Case-insensitive matching. Partial matches accepted (e.g., "inbound" alone
does not trigger; "inbound marketing" does). No tokens added post-acquisition.

## Scoring

All scoring per v1.6 lock:

- **Recognition:** C_P (count of models recognizing brand, out of 6)
- **Recall:** R_cat + R_cult split rates per v1.5
- **Dissociation:** per v1.4 multi-component construct
- **Regime:** per v1.2 four-regime taxonomy + v1.5 C2 refinement
- **Identity Load:** v1.6 R4-independent bootstrap
- **Phantom:** v1.6 Inc3 R_phantom
- **MLC:** Marketing-Language Coverage (new coded metric, v0.24)

## Hypotheses

| ID                              | Type    | Prediction                                        |
|---------------------------------|---------|----------------------------------------------------|
| H_Discourse_Language_SaaS       | Primary | MLC_SaaS > MLC_baseline                           |
| H_Regime4_saas                  | Battery | Regime 1 or 2 (uniform/near-uniform saturation)   |
| H_Dissoc_substrate_generalization | Battery | ≥ 2 Iwachu cases (Cell C likely source)          |
| H_IL_direct                     | Battery | Cell B R_cult-lead > Cell A                        |
| H_SubstrateRecognition          | Battery | Uniform A+C; possibly differential B               |
| H_Phantom_SaaS                  | Battery | ≥ 3/5 Cell D R_phantom > 0                        |

## Notes

- Slack (B5) / Salesforce (A1) parent-subsidiary relationship flagged.
  Maintained as separate entries; analytically noted, not a confound.
- MLC is the first quantified operationalization of Discourse-Language
  carryforward (observed qualitatively in v0.16). Runs under v1.6 —
  no methodology increment.
- DEVIATIONS: empty at r1. Entry 0 reserved for pre-acquisition amendments.
