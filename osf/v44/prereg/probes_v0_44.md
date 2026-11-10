# AIAS v0.44 probe set (DRAFT r0, not locked)

Built by `osf/v44/scripts/build_probes_v0_44.py` from `osf/v44/registries/`. 207 probes: Phase B 48 (6 per industry), Phase A 159 (one per unit). SHA-256 of `probes_v0_44.jsonl`: `107d9401c18d9ee00ee4d5d717642aaeac7eb812ce843ff559947fe8525c2bb6`.

## INS: Car insurance

| ID | Channel | Prompt |
|---|---|---|
| INS_B_q1 | R_cat | What are the best car insurance companies in the US? List several with descriptions. |
| INS_B_q2 | R_cat | What car insurance companies do insurance experts and consumer reviewers recommend in the US? Name several. |
| INS_B_q3 | R_cat | What car insurance companies in the US are highest quality and most reliable? Name several with descriptions. |
| INS_B_q4 | R_cult | What car insurance companies are popular in the US right now? List several. |
| INS_B_q5 | R_cult | What car insurance companies in the US have the most loyal customers? Name several. |
| INS_B_q6 | R_cult | Which car insurance companies in the US have the most iconic or storied identity in popular culture? Name several. |

Phase A (23 units), e.g. INS_A_INS01: "Is the brand State Farm commonly recognized as a car insurance brand? Answer yes or no."

## HOT: Hotel chains

| ID | Channel | Prompt |
|---|---|---|
| HOT_B_q1 | R_cat | What are the best hotel chains in the US? List several with descriptions. |
| HOT_B_q2 | R_cat | What hotel chains do travel experts and reviewers recommend in the US? Name several. |
| HOT_B_q3 | R_cat | What hotel chains in the US are highest quality and most reliable? Name several with descriptions. |
| HOT_B_q4 | R_cult | What hotel chains are popular in the US right now? List several. |
| HOT_B_q5 | R_cult | What hotel chains in the US have the most loyal customers? Name several. |
| HOT_B_q6 | R_cult | Which hotel chains in the US have the most iconic or storied identity in popular culture? Name several. |

Phase A (20 units), e.g. HOT_A_HOT01: "Is the brand Hilton commonly recognized as a hotel brand? Answer yes or no."

## GRO: Grocery store chains

| ID | Channel | Prompt |
|---|---|---|
| GRO_B_q1 | R_cat | What are the best grocery store chains in the US? List several with descriptions. |
| GRO_B_q2 | R_cat | What grocery store chains do food and consumer experts recommend in the US? Name several. |
| GRO_B_q3 | R_cat | What grocery store chains in the US are highest quality and most reliable? Name several with descriptions. |
| GRO_B_q4 | R_cult | What grocery store chains are popular in the US right now? List several. |
| GRO_B_q5 | R_cult | What grocery store chains in the US have the most loyal customers? Name several. |
| GRO_B_q6 | R_cult | Which grocery store chains in the US have the most iconic or storied identity in popular culture? Name several. |

Phase A (20 units), e.g. GRO_A_GRO01: "Is the brand Kroger commonly recognized as a grocery store brand? Answer yes or no."

## QSR: Fast-food chains

| ID | Channel | Prompt |
|---|---|---|
| QSR_B_q1 | R_cat | What are the best fast-food chains in the US? List several with descriptions. |
| QSR_B_q2 | R_cat | What fast-food chains do food critics and reviewers recommend in the US? Name several. |
| QSR_B_q3 | R_cat | What fast-food chains in the US are highest quality and most reliable? Name several with descriptions. |
| QSR_B_q4 | R_cult | What fast-food chains are popular in the US right now? List several. |
| QSR_B_q5 | R_cult | What fast-food chains in the US have the most loyal customers? Name several. |
| QSR_B_q6 | R_cult | Which fast-food chains in the US have the most iconic or storied identity in popular culture? Name several. |

Phase A (21 units), e.g. QSR_A_QSR01: "Is the brand McDonald's commonly recognized as a fast-food brand? Answer yes or no."

## APR: Clothing and department stores

| ID | Channel | Prompt |
|---|---|---|
| APR_B_q1 | R_cat | What are the best clothing and department store chains in the US? List several with descriptions. |
| APR_B_q2 | R_cat | What clothing and department store chains do fashion and shopping experts recommend in the US? Name several. |
| APR_B_q3 | R_cat | What clothing and department store chains in the US are highest quality and most reliable? Name several with descriptions. |
| APR_B_q4 | R_cult | What clothing and department store chains are popular in the US right now? List several. |
| APR_B_q5 | R_cult | What clothing and department store chains in the US have the most loyal customers? Name several. |
| APR_B_q6 | R_cult | Which clothing and department store chains in the US have the most iconic or storied identity in popular culture? Name several. |

Phase A (16 units), e.g. APR_A_APR01: "Is the brand T.J. Maxx commonly recognized as a clothing store brand? Answer yes or no."

## PHA: Pharmacies

| ID | Channel | Prompt |
|---|---|---|
| PHA_B_q1 | R_cat | What are the best pharmacies in the US? List several with descriptions. |
| PHA_B_q2 | R_cat | What pharmacies do health and consumer experts recommend in the US? Name several. |
| PHA_B_q3 | R_cat | What pharmacies in the US are highest quality and most reliable? Name several with descriptions. |
| PHA_B_q4 | R_cult | What pharmacies are popular in the US right now? List several. |
| PHA_B_q5 | R_cult | What pharmacies in the US have the most loyal customers? Name several. |
| PHA_B_q6 | R_cult | Which pharmacies in the US have the most iconic or storied identity in popular culture? Name several. |

Phase A (16 units), e.g. PHA_A_PHA01: "Is the brand CVS Pharmacy commonly recognized as a pharmacy brand? Answer yes or no."

## CVF: Convenience stores and gas stations

| ID | Channel | Prompt |
|---|---|---|
| CVF_B_q1 | R_cat | What are the best convenience store and gas station chains in the US? List several with descriptions. |
| CVF_B_q2 | R_cat | What convenience store and gas station chains do travel and consumer experts recommend in the US? Name several. |
| CVF_B_q3 | R_cat | What convenience store and gas station chains in the US are highest quality and most reliable? Name several with descriptions. |
| CVF_B_q4 | R_cult | What convenience store and gas station chains are popular in the US right now? List several. |
| CVF_B_q5 | R_cult | What convenience store and gas station chains in the US have the most loyal customers? Name several. |
| CVF_B_q6 | R_cult | Which convenience store and gas station chains in the US have the most iconic or storied identity in popular culture? Name several. |

Phase A (19 units), e.g. CVF_A_CVF01: "Is the brand 7-Eleven commonly recognized as a convenience store brand? Answer yes or no."

## FAS: Fashion and luxury

| ID | Channel | Prompt |
|---|---|---|
| FAS_B_q1 | R_cat | What are the best luxury fashion brands in the US? List several with descriptions. |
| FAS_B_q2 | R_cat | What luxury fashion brands do fashion editors and stylists recommend in the US? Name several. |
| FAS_B_q3 | R_cat | What luxury fashion brands in the US are highest quality and most reliable? Name several with descriptions. |
| FAS_B_q4 | R_cult | What luxury fashion brands are popular in the US right now? List several. |
| FAS_B_q5 | R_cult | What luxury fashion brands in the US have the most loyal customers? Name several. |
| FAS_B_q6 | R_cult | Which luxury fashion brands in the US have the most iconic or storied identity in popular culture? Name several. |

Phase A (24 units), e.g. FAS_A_FAS01: "Is the brand Hermès commonly recognized as a fashion brand? Answer yes or no."

