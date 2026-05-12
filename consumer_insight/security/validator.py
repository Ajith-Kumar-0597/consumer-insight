import re, html

def sanitize_input(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"[\x00-\x1F\x7F]", "", text)
    text = re.sub(r"\s{2,}", " ", text).strip()
    return text
