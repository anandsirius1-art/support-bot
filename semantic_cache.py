from cache_config import EXCLUDED_CATEGORIES, SIMILARITY_THRESHOLD, TTL_HOURS


def is_cacheable(category: str) -> bool:
    return category not in EXCLUDED_CATEGORIES


def ttl_hours(category: str) -> int:
    return TTL_HOURS.get(category, TTL_HOURS["default"])


def is_hit(similarity: float, age_hours: float, category: str) -> bool:
    return (
        is_cacheable(category)
        and similarity >= SIMILARITY_THRESHOLD
        and age_hours < ttl_hours(category)
    )
