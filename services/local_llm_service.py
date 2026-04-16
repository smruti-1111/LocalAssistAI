import requests
import json
import re

OLLAMA_URL = "http://localhost:11434/api/generate"


def call_llm(prompt: str):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "phi",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]


#  STRICT JSON EXTRACTION
def extract_json(text: str):
    matches = re.findall(r'\{.*?\}', text, re.DOTALL)

    for m in matches:
        try:
            json.loads(m)
            return m
        except:
            continue

    return None


#  ROBUST ANALYSIS FUNCTION
def analyze_text_local(text: str):
    prompt = f"""
You MUST return ONLY a valid JSON object.

DO NOT:
- Explain anything
- Write code
- Add markdown
- Add text before or after JSON

ONLY RETURN THIS FORMAT:

{{
  "sentiment": "positive | negative | neutral",
  "summary": "short summary",
  "category": "billing | technical | general",
  "priority": "low | medium | high"
}}

User query: {text}
"""

    output = call_llm(prompt)

    json_text = extract_json(output)

    if not json_text:
        #  FALLBACK (rule-based safety)
        return {
            "sentiment": "negative" if "frustrated" in text.lower() else "unknown",
            "summary": text,
            "category": "technical",
            "priority": "high" if "crash" in text.lower() else "low"
        }

    try:
        return json.loads(json_text)
    except:
        return {
            "sentiment": "unknown",
            "summary": output,
            "category": "general",
            "priority": "low"
        }


#  CLEAN + CONTROLLED RESPONSE
def generate_response_local(text: str, context: str):
    prompt = f"""
You are a professional customer support assistant.

Context: {context}
Query: {text}

Rules:
- If negative → show empathy
- If high priority → be urgent
- Be concise (2-3 lines)
- Provide actionable steps
- Do NOT include code or markdown

Generate response:
"""

    return call_llm(prompt).strip()
