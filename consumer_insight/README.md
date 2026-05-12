# 📊 Consumer Insight MCP

A **Model Context Protocol (MCP)** server exposing 3 consumer insight tools with a built-in web UI.

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the server
cd server
uvicorn mcp_server:app --reload --port 8000

# 3. Open browser
# http://localhost:8000

# 4. Run tests
pytest tests/test_consumer_insight.py -v
```

---

## 🛠️ MCP Tools

| Tool | Output | Description |
|------|--------|-------------|
| `trend_tool` | **Markdown** | Consumer trends for any topic & region |
| `sentiment_tool` | **JSON** | Sentiment analysis with score & keywords |
| `export_tool` | **CSV** | Downloadable trend data |

---

## 📡 API Usage

### Invoke a Tool
```bash
curl -X POST http://localhost:8000/invoke \
  -H "X-API-Key: insight-key-2024" \
  -H "Content-Type: application/json" \
  -d '{"tool": "trend_tool", "query": "skincare trends in Japan"}'
```

### List Available Tools
```bash
curl http://localhost:8000/tools \
  -H "X-API-Key: insight-key-2024"
```

---

## 🔐 Security

| Layer | Implementation |
|-------|---------------|
| Authentication | `X-API-Key` header on every request |
| Tool Allowlist | Only 3 registered tools can be invoked |
| Input Validation | Pydantic schema + length + injection check |
| Input Sanitisation | HTML escape + control char stripping |
| Rate Limiting | 30 requests/minute per IP |

---

## 📂 Project Structure

```
consumer_insight/
├── server/
│   └── mcp_server.py         ← FastAPI MCP server + web UI route
├── tools/
│   ├── trend_tool.py         ← Returns Markdown
│   ├── sentiment_tool.py     ← Returns JSON
│   └── export_tool.py        ← Returns CSV
├── security/
│   ├── auth.py               ← API key authentication
│   └── validator.py          ← Input sanitisation
├── static/
│   └── index.html            ← Web UI
├── tests/
│   └── test_consumer_insight.py  ← 14 pytest tests
├── requirements.txt
└── README.md
```

---

## 🧪 Example Outputs

### trend_tool → Markdown
```
## 📊 Skincare Trends – Japan 🇯🇵
| # | Trend | Score | Strength |
|---|-------|-------|----------|
| 1 | AI skin analysis apps | 94 | ██████████ |
| 2 | Short-form beauty content | 91 | █████████░ |
```

### sentiment_tool → JSON
```json
{
  "sentiment": "positive",
  "score": 0.85,
  "confidence": "high",
  "analysis": {
    "positive_signals": 3,
    "negative_signals": 0,
    "keywords_detected": ["amazing", "love", "best"]
  },
  "summary": "The query carries a positive consumer sentiment."
}
```

### export_tool → CSV
```
rank,trend,score,category,region
1,AI skin analysis apps,94,Technology,Japan
2,Short-form beauty content,91,Content,Global
```

---

## 💬 Demo Statement

> *"This project demonstrates that MCP is not just about exposing tools — it's about making them secure, structured, and reliable for agentic workflows."*
