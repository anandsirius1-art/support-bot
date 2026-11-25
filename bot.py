"""Support bot: answers customer questions with the LLM, reusing cached answers for repeats."""
import json
from pathlib import Path

from semantic_cache import SemanticCache

FAQS = json.loads((Path(__file__).parent / "data" / "faqs.json").read_text())

PRICING_WORDS = ("price", "cost", "plan", "discount", "invoice amount")
ACCOUNT_WORDS = ("my account", "my order", "my subscription", "refund")

CACHE = SemanticCache()


def classify(question: str) -> str:
    q = question.lower()
    if any(w in q for w in PRICING_WORDS):
        return "pricing"
    if any(w in q for w in ACCOUNT_WORDS):
        return "account"
    if any(f["question"].lower().rstrip("?") == q.rstrip("?") for f in FAQS):
        return "faq"
    return "other"


def call_model(question: str, category: str) -> str:
    """Placeholder for the paid LLM call."""
    return f"[model answer for {category}] {question}"


def answer(question: str, cache: SemanticCache = CACHE) -> str:
    category = classify(question)
    cached = cache.get(question, category)
    if cached is not None:
        return cached
    result = call_model(question, category)
    cache.put(question, category, result)
    return result
