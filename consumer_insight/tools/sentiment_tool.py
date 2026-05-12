"""
Sentiment Tool → JSON output
Powered by OpenAI GPT-4o-mini — analyses ANY text or topic.
"""

import httpx, os, json, re

OPENAI_URL = "https://api.openai.com/v1/chat/completions"

SYSTEM_PROMPT = """You are a Consumer Sentiment Analyst.

Analyse the sentiment of the given text and respond ONLY with a valid JSON object:
{
  "sentiment": "positive" or "neutral" or "negative",
  "emoji": "😊" or "😐" or "😟",
  "score": float between 0.0 and 1.0,
  "confidence": "high" or "medium" or "low",
  "analysis": {
    "positive_signals": integer,
    "negative_signals": integer,
    "word_count": integer,
    "keywords_detected": list of up to 5 words
  },
  "summary": "One sentence explaining the sentiment in consumer context"
}

Rules:
- score > 0.62 = positive, < 0.38 = negative, else neutral
- Return ONLY raw JSON, no markdown, no code blocks, no extra text"""

def run(query: str):
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        return json.dumps({"error": "OPENAI_API_KEY not found in .env file."}, indent=2), "json"
    try:
        resp = httpx.post(
            OPENAI_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": query},
                ],
                "max_tokens": 400,
            },
            timeout=20,
        )
        data = resp.json()
        if "error" in data:
            return json.dumps({"error": data["error"]["message"]}, indent=2), "json"
        raw = data["choices"][0]["message"]["content"].strip()
        raw = re.sub(r"```json|```", "", raw).strip()
        json.loads(raw)
        return raw, "json"
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2), "json"
