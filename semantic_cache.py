"""Semantic cache: reuse the answer to a question we've already answered."""
import time
from difflib import SequenceMatcher

from cache_config import EXCLUDED_CATEGORIES, SIMILARITY_THRESHOLD, TTL_HOURS


def _norm(text: str) -> str:
    return " ".join(text.lower().strip(" ?!.").split())


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, _norm(a), _norm(b)).ratio()


def is_cacheable(category: str) -> bool:
    return category not in EXCLUDED_CATEGORIES


def ttl_hours(category: str) -> int:
    return TTL_HOURS.get(category, TTL_HOURS["default"])


class SemanticCache:
    def __init__(self, clock=time.time):
        self._clock = clock
        self._entries = []  # (question, category, answer, stored_at)

    def get(self, question: str, category: str):
        if not is_cacheable(category):
            return None
        now = self._clock()
        best, best_sim = None, 0.0
        for q, cat, ans, stored_at in self._entries:
            if cat != category or (now - stored_at) / 3600 >= ttl_hours(cat):
                continue
            s = similarity(question, q)
            if s >= SIMILARITY_THRESHOLD and s > best_sim:
                best, best_sim = ans, s
        return best

    def put(self, question: str, category: str, answer: str) -> None:
        if is_cacheable(category):
            self._entries.append((question, category, answer, self._clock()))
