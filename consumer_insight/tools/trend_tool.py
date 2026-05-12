"""
Trend Tool → Markdown output
Powered by OpenAI GPT-4o-mini — answers ANY consumer trend question.
"""

import httpx, os

OPENAI_URL = "https://api.openai.com/v1/chat/completions"

SYSTEM_PROMPT = """You are a Consumer Insight Analyst specializing in market trends.

When given any consumer trend query, respond ONLY in this exact Markdown format:

## 📊 [Topic Title with relevant flag emoji if region mentioned]

| # | Trend | Score | Strength |
|---|-------|-------|----------|
| 1 | [trend name] | `[score 70-99]` | [fill █ blocks out of 10 based on score, remaining ░] |
| 2 | [trend name] | `[score]` | [bar] |
| 3 | [trend name] | `[score]` | [bar] |
| 4 | [trend name] | `[score]` | [bar] |
| 5 | [trend name] | `[score]` | [bar] |

### 🔥 Key Takeaway
**[top trend]** is the top trend with a score of `[score]`.

> *Scores represent relative trend strength (0–100 scale)*

Rules:
- Always return exactly 5 trends
- Scores between 70-99, descending order
- Strength bar: score//10 filled █ + remaining ░ = 10 total
- Be specific and relevant to the query
- Return ONLY the markdown, no extra text"""

def run(query: str):
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        return "## ❌ Error\nOPENAI_API_KEY not found in .env file.", "markdown"
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
                "max_tokens": 600,
            },
            timeout=20,
        )
        data = resp.json()
        if "error" in data:
            return f"## ❌ OpenAI Error\n`{data['error']['message']}`", "markdown"
        return data["choices"][0]["message"]["content"].strip(), "markdown"
    except Exception as e:
        return f"## ❌ Error\n{str(e)}", "markdown"
