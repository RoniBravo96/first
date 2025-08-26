import re

def normalize_text(x: str) -> str:
    return re.sub(r"\s+", " ", (x or "")).strip()

def contains_any(text: str, words):
    t = (text or "").lower()
    return any(w.lower() in t for w in words)

def definitely_remote(text: str) -> bool:
    t = (text or "").lower()
    return any(w in t for w in ["remote","work from home","hybrid"])
