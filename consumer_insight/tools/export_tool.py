"""
Export Tool → CSV output
Powered by OpenAI GPT-4o-mini — exports trends for ANY topic as CSV.
"""

import httpx, os, re

OPENAI_URL = "https://api.openai.com/v1/chat/completions"

SYSTEM_PROMPT = """You are a Consumer Insight Data Analyst.

When given any topic query, respond ONLY with a CSV string:
rank,trend,score,category,region
1,[trend name],[score 70-99],[one word category],[region]
2,[trend name],[score],[category],[region]
3,[trend name],[score],[category],[region]
4,[trend name],[score],[category],[region]
5,[trend name],[score],[category],[region]
6,[trend name],[score],[category],[region]

Rules:
- Exactly 6 data rows plus header
- Scores descending from 70-99
- Category: one word like Technology, Lifestyle, Health, Content, Social, AI, Fintech
- Region: infer from query or use Global
- Return ONLY the raw CSV, no markdown, no code blocks, no extra text"""

def run(query: str):
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        return "rank,trend,score,category,region\n1,OPENAI_API_KEY not set,0,Error,Global", "csv"
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
            return f"rank,trend,score,category,region\n1,{data['error']['message']},0,Error,Global", "csv"
        raw = data["choices"][0]["message"]["content"].strip()
        raw = re.sub(r"```csv|```", "", raw).strip()
        return raw, "csv"
    except Exception as e:
        return f"rank,trend,score,category,region\n1,Error: {str(e)},0,Error,Global", "csv"
