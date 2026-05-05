"""AIAS — Brand Extraction Module (category-agnostic)"""
import json
import re
from openai import OpenAI

EXTRACTOR_MODEL = "gpt-5.4-mini"


def make_extraction_tool(category_description):
    return {
        "type": "function",
        "function": {
            "name": "record_brand_mentions",
            "description": f"Record every {category_description} brand mentioned, in order.",
            "parameters": {
                "type": "object",
                "properties": {
                    "brands_mentioned": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "rank": {"type": "integer"},
                                "sentiment": {"type": "string", "enum": ["positive", "neutral", "negative"]},
                                "is_primary_recommendation": {"type": "boolean"}
                            },
                            "required": ["name", "rank", "sentiment", "is_primary_recommendation"]
                        }
                    }
                },
                "required": ["brands_mentioned"]
            }
        }
    }


def extract_via_function_calling(response_text, openai_client, category_description):
    system_prompt = (
        f"You extract brand mentions from text about {category_description}. "
        "List every brand mentioned in the order they appear. Do not invent brands. "
        "If a brand appears multiple times, record it only at its first appearance."
    )
    tool = make_extraction_tool(category_description)
    completion = openai_client.chat.completions.create(
        model=EXTRACTOR_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": response_text}
        ],
        tools=[tool],
        tool_choice={"type": "function", "function": {"name": "record_brand_mentions"}},
        temperature=0,
    )
    tool_call = completion.choices[0].message.tool_calls[0]
    args = json.loads(tool_call.function.arguments)
    return args.get("brands_mentioned", [])


def map_to_canonical(extracted_name, brand_registry):
    name_lower = extracted_name.lower().strip()
    for brand in brand_registry:
        if name_lower == brand["canonical"].lower():
            return brand["canonical"]
        for alias in brand["aliases"]:
            if name_lower == alias.lower():
                return brand["canonical"]
    for brand in brand_registry:
        for alias in brand["aliases"]:
            if alias.lower() in name_lower or name_lower in alias.lower():
                return brand["canonical"]
    return None


def extract_via_regex(response_text, brand_registry):
    text_lower = response_text.lower()
    found = []
    for brand in brand_registry:
        for alias in brand["aliases"]:
            pattern = r"\b" + re.escape(alias.lower()) + r"\b"
            if re.search(pattern, text_lower):
                found.append({
                    "canonical": brand["canonical"],
                    "rank": None,
                    "sentiment": "unknown",
                    "is_primary_recommendation": None,
                    "raw_mention": alias,
                    "extraction_method": "regex_fallback"
                })
                break
    return found


def extract_brands(response_text, brand_registry, openai_client, category_description="brands"):
    if not response_text or not response_text.strip():
        return []
    try:
        extracted = extract_via_function_calling(response_text, openai_client, category_description)
        results = []
        for item in extracted:
            canonical = map_to_canonical(item["name"], brand_registry)
            results.append({
                "canonical": canonical,
                "raw_mention": item["name"],
                "rank": item["rank"],
                "sentiment": item["sentiment"],
                "is_primary_recommendation": item["is_primary_recommendation"],
                "extraction_method": "function_calling"
            })
        return results
    except Exception as e:
        print(f"      [extractor] function-calling failed ({type(e).__name__}), using regex fallback")
        return extract_via_regex(response_text, brand_registry)