"""Support bot: answers customer questions with the LLM."""
import json
from pathlib import Path

FAQS = json.loads((Path(__file__).parent / "data" / "faqs.json").read_text())

PRICING_WORDS = ("price", "cost", "plan", "discount", "invoice amount")
ACCOUNT_WORDS = ("my account", "my order", "my subscription", "refund")


def classify(question: str) -> str:
    q = question.lower()
    if any(w in q for w in PRICING_WORDS):
        return "pricing"
    if any(w in q for w in ACCOUNT_WORDS):
        return "account"
    if any(f["question"].lower() == q for f in FAQS):
        return "faq"
    return "other"


def call_model(question: str, category: str) -> str:
    """Placeholder for the paid LLM call (one call per question, no reuse)."""
    return f"[model answer for {category}] {question}"


def answer(question: str) -> str:
    return call_model(question, classify(question))
