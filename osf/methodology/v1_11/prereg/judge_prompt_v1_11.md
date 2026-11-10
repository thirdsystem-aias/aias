# v1.11 judge prompt and output schema (DRAFT r0, not locked)

The exact text sent to both judges (J1 primary, J2 reliability) for every unit. It is generated from, and tested byte-identical to, `SYSTEM_PROMPT`, `USER_TEMPLATE`, `TEXT_TYPES` and `OUTPUT_SCHEMA` in `scripts/score_v1_11.py` (`test_prompt_md_matches_script`). Placeholders in braces are filled per unit; nothing else varies. Model IDs: **TO VERIFY at lock** (PRE_REGISTRATION_v1_11.md §4.2).

## Call parameters (fixed)

- temperature 0; maximum output 200 tokens; no tools; no web search; extended reasoning off (or the vendor's minimum, recorded).
- System message = SYSTEM_PROMPT; one user message = USER_TEMPLATE filled; no prior turns.
- Where the vendor supports schema-constrained output, OUTPUT_SCHEMA is passed as the response schema; the prompt text is unchanged.
- The judge never sees the answering model, the wave, the answer set, or any AIAS score.
- `{text_type}` is TEXT_TYPES["recognition"] for v0.23 recognition answers and TEXT_TYPES["mention"] for mention windows.
- `{question}` is the exact user prompt that produced the answer; `{category}` is the registry's category description; `{brand}` is the registry display name.

## SYSTEM_PROMPT

<!-- BEGIN SYSTEM_PROMPT -->
```text
You are an annotator in a research study of how AI assistants describe brands. You will read a text written by an AI assistant and rate how favourably it describes one target brand. Rate only what the text says; do not add what you know about the brand. Reply with one JSON object and nothing else.
```
<!-- END SYSTEM_PROMPT -->

## USER_TEMPLATE

<!-- BEGIN USER_TEMPLATE -->
```text
TARGET BRAND: {brand}
CATEGORY: {category}
QUESTION THE ASSISTANT WAS ANSWERING: {question}
TEXT TYPE: {text_type}

TEXT:
<<<
{text}
>>>

Rate how favourably the TEXT describes the TARGET BRAND.

Rules:
1. Rate only statements about the target brand: its products, quality, performance, value, reputation, people and conduct, and comparisons that involve it. Ignore statements about other brands unless they compare the target brand with them.
2. Being named, listed or recommended by inclusion is not an evaluation in itself. List labels and phrases that only repeat the question (for example "Top picks:" or "Brands for beginners:") are not evaluations of the target brand. Rate the words that describe the target brand itself.
3. Plain facts are neutral: history, founding date, ownership, location, product range, ingredients, price level or market position stated without judgement.
4. Evaluations count: praise or criticism by the assistant, and judgements by others that the text reports (awards, ratings, critical acclaim, complaints, recalls, controversies, lawsuits).
5. "evaluative" is true if the text contains at least one evaluation of the target brand under rule 4, and false if it contains only facts or description.
6. If favourable and unfavourable evaluations are both present, set "mixed" to true and choose the valence that reflects their overall balance (0 if they are of similar weight).
7. If the text does not refer to the target brand (the name is used as an ordinary word or for a different company, or the assistant says it does not know the brand and describes nothing), set "refers_to_brand" to false, "evaluative" to false, "mixed" to false and "valence" to 0.

Valence scale:
2 = strongly favourable: emphatic praise or endorsement of the brand ("outstanding", "the best", "exceptional quality") with no substantive reservation.
1 = favourable: a positive evaluation ("well regarded", "reliable", "good value", "award-winning"), possibly with minor reservations.
0 = neutral: no evaluation of the brand (facts or description only), or favourable and unfavourable evaluations of similar weight.
-1 = unfavourable: a negative evaluation ("overpriced", "inconsistent quality", "mixed reviews", "less refined than"), possibly with some positives.
-2 = strongly unfavourable: emphatic criticism or warning ("avoid", "poor quality", a scandal or recall presented as defining) with no substantive positive.

Reply with one JSON object with exactly these keys:
"refers_to_brand" (true or false), "evaluative" (true or false), "mixed" (true or false), "valence" (one of -2, -1, 0, 1, 2), "evidence" (the shortest quote from the TEXT, at most 20 words, that best supports the valence; an empty string if "evaluative" is false).
```
<!-- END USER_TEMPLATE -->

## TEXT_TYPES

<!-- BEGIN TEXT_TYPES -->
```json
{
  "recognition": "the assistant's full answer about the target brand",
  "mention": "the sentences of a longer answer that mention the target brand (the rest of the answer is omitted and marked [...])"
}
```
<!-- END TEXT_TYPES -->

## OUTPUT_SCHEMA

<!-- BEGIN OUTPUT_SCHEMA -->
```json
{
  "type": "object",
  "additionalProperties": false,
  "required": [
    "refers_to_brand",
    "evaluative",
    "mixed",
    "valence",
    "evidence"
  ],
  "properties": {
    "refers_to_brand": {
      "type": "boolean"
    },
    "evaluative": {
      "type": "boolean"
    },
    "mixed": {
      "type": "boolean"
    },
    "valence": {
      "type": "integer",
      "enum": [
        -2,
        -1,
        0,
        1,
        2
      ]
    },
    "evidence": {
      "type": "string"
    }
  }
}
```
<!-- END OUTPUT_SCHEMA -->

## Validation applied to every output (`parse_judge_output`)

1. One JSON object with exactly the five keys; booleans are booleans; valence is an integer in -2..2.
2. `refers_to_brand` false requires valence 0, `evaluative` false, `mixed` false.
3. `evaluative` false requires valence 0 and `mixed` false.
4. An evidence quote over 20 words is flagged, not rejected.
5. Invalid output: up to 2 retries with identical input, then JUDGE_FAIL (excluded, counted; > 2% of a set's units halts the run before scoring).

## Scoring of a valid output

Unit score u = 25 x (valence + 2): -2 -> 0, -1 -> 25, 0 -> 50, +1 -> 75, +2 -> 100. Units with `refers_to_brand` false are excluded. Non-evaluative units stay in the score at 50 (PRE_REGISTRATION_v1_11.md §4.3).
