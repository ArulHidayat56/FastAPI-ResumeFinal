import json
import re

def extract_json_from_llm_response(text: str):
    """Extract JSON data from LLM text response with improved handling."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    json_pattern = r"\{(?:[^{}]|(?:\{(?:[^{}]|(?:\{[^{}]*\}))*\}))*\}"
    matches = re.findall(json_pattern, text, re.DOTALL)

    if matches:
        for match in matches:
            try:
                return json.loads(match)
            except json.JSONDecodeError:
                continue

    raise ValueError("Could not extract valid JSON from LLM response.")
