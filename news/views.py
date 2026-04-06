"""
STEP 5: Views — the functions that handle HTTP requests and return responses.
WHY: Django views are the "controller" in MVC. Each view receives a request,
     does some work (fetch data, process forms), and returns an HTML response
     by rendering a template with context data. We use function-based views
     (not class-based) because they're simpler and more explicit for beginners.
"""
from django.shortcuts import render
from .news_client import fetch_top_headlines, CATEGORIES


def home(request):
    """
    Home page — display top headlines.

    WHY: The home page fetches general top headlines on first load.
         If a ?category= query parameter is present, it filters by that category.
         This lets us reuse one view for both "all news" and "category news"
         without needing separate URL patterns.
    """
    articles = fetch_top_headlines()
    context = {
        "articles": articles,
        "categories": CATEGORIES,
        "current_category": None,
    }
    return render(request, "news/home.html", context)
