"""Semantic cache settings for the support bot.

Repeat questions are answered from cache instead of calling the model.
Customers see the same answers; we just stop paying to regenerate them.
"""

# Questions in these categories always go to the model, never the cache.
# Prices change on the 1st of every month, and account answers are per-customer.
EXCLUDED_CATEGORIES = {"pricing", "account"}

# How long a cached answer stays valid, in hours.
TTL_HOURS = {
    "faq": 24,
    "default": 24,
}

# Minimum similarity for two questions to count as "the same question".
SIMILARITY_THRESHOLD = 0.92
