from semantic_cache import is_cacheable, is_hit


def test_pricing_and_account_never_cached():
    assert not is_cacheable("pricing")
    assert not is_cacheable("account")
    assert not is_hit(1.0, 0, "pricing")


def test_faq_repeat_is_hit():
    assert is_hit(0.95, 1, "faq")


def test_low_similarity_misses():
    assert not is_hit(0.5, 1, "faq")
