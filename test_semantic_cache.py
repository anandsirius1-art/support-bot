from unittest.mock import patch

import bot
from semantic_cache import SemanticCache, is_cacheable


class Clock:
    def __init__(self):
        self.t = 0.0

    def __call__(self):
        return self.t


def test_pricing_and_account_never_cached():
    assert not is_cacheable("pricing")
    assert not is_cacheable("account")
    c = SemanticCache()
    c.put("How much is the Pro plan?", "pricing", "x")
    assert c.get("How much is the Pro plan?", "pricing") is None


def test_repeat_faq_is_hit_and_skips_model():
    c = SemanticCache()
    q = "What are your support hours?"
    with patch.object(bot, "call_model", wraps=bot.call_model) as m:
        first = bot.answer(q, cache=c)
        second = bot.answer("what are your support hours", cache=c)
    assert first == second
    assert m.call_count == 1


def test_pricing_always_calls_model():
    c = SemanticCache()
    with patch.object(bot, "call_model", wraps=bot.call_model) as m:
        bot.answer("How much is the Pro plan?", cache=c)
        bot.answer("How much is the Pro plan?", cache=c)
    assert m.call_count == 2


def test_different_question_misses():
    c = SemanticCache()
    c.put("What are your support hours?", "faq", "a")
    assert c.get("Do you ship internationally?", "faq") is None


def test_expires_after_24h():
    clock = Clock()
    c = SemanticCache(clock=clock)
    c.put("How long does delivery take?", "faq", "a")
    clock.t = 23 * 3600
    assert c.get("How long does delivery take?", "faq") == "a"
    clock.t = 24 * 3600
    assert c.get("How long does delivery take?", "faq") is None
