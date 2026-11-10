# v1.11 judge prompt and output schema (r1, pre-lock; locked with the pre-registration)

The exact text sent to both judges (J1 primary, J2 reliability) for every unit. It is generated from, and tested byte-identical to, `SYSTEM_PROMPT`, `USER_TEMPLATE`, `TEXT_TYPES`, `OUTPUT_SCHEMA` and `CATEGORY_LABELS` in `scripts/score_v1_11.py` (`test_prompt_md_matches_script`). Placeholders in braces are filled per unit; nothing else varies. The prompt text is unchanged from draft r0; only the judges and call parameters below changed (runner decision 1, then the budget redesign, decision 21, 2026-11-10).

## Judges (PRE_REGISTRATION_v1_11.md §4.2)

| Role | Model | ID | Endpoint | Reasoning parameter sent (lowest documented effort) |
|---|---|---|---|---|
| J1 (primary) | Claude Opus 5.5 | `claude-opus-5-5` | Anthropic Message Batches API | `output_config.effort = "low"` (thinking cannot be disabled) |
| J2 (reliability) | GPT-6.1 Sol | `gpt-6.1-sol` | OpenAI Batch API, `/v1/responses` | `reasoning.effort = "low"` |
| Alternate (replaces J1 or J2 only under §4.2) | Gemini 4 Argon | `gemini-4-argon` | synchronous `generate_content` | `thinking_config.thinking_level = "low"` |

IDs and effort values as read on the vendors' documentation on 2026-11-10 (sources in PRE_REGISTRATION §4.2); prices and the cost design in §7.

## Call parameters (fixed; `JUDGE_CALL_POLICY` and `judge_v1_11.request_kwargs`)

- No sampling parameter is sent to any judge: no temperature, no top_p, no top_k. Claude Opus 5.5 cannot switch thinking off (Anthropic's effort page, 2026-11-10); GPT-6.1 Sol is sent no temperature; Gemini 4 Argon ignores temperature. Each call's full parameter set is recorded with its output (`request`), together with the served model ID, finish reason, token counts including reasoning, the endpoint and, for batch calls, the batch ID.
- Reasoning at the lowest effort each vendor documents for the model (table above), fixed for the whole run.
- The request body is the same in batch and synchronous mode (Anthropic: `{"custom_id", "params": <request>}`; OpenAI: one JSONL line `{"custom_id", "method": "POST", "url": "/v1/responses", "body": <request>}`).
- Maximum output 4,096 tokens, reasoning included (output cap, PRE_REGISTRATION §4.2 and §7; was 16,384); a reply cut by the cap is invalid output; no tools; no web search.
- System message = SYSTEM_PROMPT; one user message = USER_TEMPLATE filled; no prior turns.
- Prompt-only JSON for every judge: no response schema is sent (the vendors' schema features differ and are not documented in the program's records for these models); OUTPUT_SCHEMA below defines validity.
- The judge never sees the answering model, the wave, the answer set, or any AIAS score.
- `{text_type}` is TEXT_TYPES["recognition"] for v0.23 recognition answers and TEXT_TYPES["mention"] for mention windows.
- `{question}` is the exact user prompt that produced the answer (frame text, recorded prompt, or the phase's prompt file by prompt id); `{category}` is CATEGORY_LABELS[set category] below; `{brand}` is the registry display name.

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

## CATEGORY_LABELS

The registry's category in plain words (OMNI substrate ids and early-category codes as keys).

<!-- BEGIN CATEGORY_LABELS -->
```json
{
  "v0.19": "audiophile headphones",
  "v0.20": "skincare",
  "v0.21": "cosmetics",
  "v0.22": "automotive",
  "v0.23": "premium spirits",
  "pm": "project management software",
  "finance": "personal finance apps",
  "oliveoil": "premium olive oil",
  "running": "running shoes",
  "skincare": "premium facial skincare",
  "household": "household goods retail",
  "knives": "premium kitchen knives",
  "premium_tea": "premium tea"
}
```
<!-- END CATEGORY_LABELS -->

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
5. The served model ID must equal the requested ID (or a dated snapshot of it); otherwise the response counts as invalid.
6. Invalid output (including an empty answer or a served-ID mismatch): up to 2 retries with identical input, then JUDGE_FAIL (excluded, counted; > 2% of a set's units, per judge, halts the run before scoring). An API error that persists through the transient-retry policy is re-sent once; a unit never answered is UNJUDGED (counted).

## Scoring of a valid output

Unit score u = 25 x (valence + 2): -2 -> 0, -1 -> 25, 0 -> 50, +1 -> 75, +2 -> 100. Units with `refers_to_brand` false are excluded. Non-evaluative units stay in the score at 50 (PRE_REGISTRATION_v1_11.md §4.3).
