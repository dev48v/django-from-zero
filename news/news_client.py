"""
STEP 4: GNews API client — fetch headlines and search articles.
WHY: All external API calls live in this one file. The views don't know (or care)
     that we're using GNews — they just call fetch_top_headlines() and get back a
     list of articles. If we ever switch to a different news API, we change this
     file only. This is the same "isolate external dependencies" pattern used in
     the FastAPI weather_client from Day 7.
"""
import requests
from django.conf import settings

# WHY: GNews API base URL. Free tier: 100 requests/day, works from any server
#      (unlike NewsAPI which restricts free tier to localhost only).
GNEWS_BASE_URL = "https://gnews.io/api/v4"

# WHY: GNews supports these categories for top-headlines. We expose them so
#      the views can build the category navigation without hardcoding.
CATEGORIES = [
    "general",
    "world",
    "nation",
    "business",
    "technology",
    "entertainment",
    "sports",
    "science",
    "health",
]


def fetch_top_headlines(category=None, max_results=10):
    """
    Fetch top headlines from GNews API.

    Args:
        category: One of CATEGORIES, or None for general headlines.
        max_results: Number of articles to return (1-10 on free tier).

    Returns:
        List of article dicts, each with: title, description, content,
        url, image, publishedAt, source (name + url).

    WHY: We return an empty list on failure instead of raising an exception.
         A news page with "no articles found" is better than a 500 error page.
         The user can refresh and try again.
    """
    params = {
        "token": settings.GNEWS_API_KEY,
        "lang": "en",
        "max": min(max_results, 10),  # GNews free tier caps at 10
    }

    if category and category in CATEGORIES:
        params["category"] = category

    try:
        response = requests.get(
            f"{GNEWS_BASE_URL}/top-headlines",
            params=params,
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("articles", [])
    except requests.RequestException:
        # WHY: Catch all request errors (timeout, connection, HTTP errors) in one place.
        #      Log the error in production, return empty list so the page still renders.
        return []


def search_articles(query, max_results=10):
    """
    Search for articles matching a query string.

    Args:
        query: Search term (e.g., "climate change", "Python programming").
        max_results: Number of articles to return.

    Returns:
        List of article dicts (same shape as fetch_top_headlines).

    WHY: GNews search endpoint uses full-text search across titles and descriptions.
         The 'q' parameter supports AND/OR/NOT operators and quoted phrases.
    """
    if not query or not query.strip():
        return []

    params = {
        "q": query.strip(),
        "token": settings.GNEWS_API_KEY,
        "lang": "en",
        "max": min(max_results, 10),
    }

    try:
        response = requests.get(
            f"{GNEWS_BASE_URL}/search",
            params=params,
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("articles", [])
    except requests.RequestException:
        return []
