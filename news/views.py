"""
STEP 5: Views — the functions that handle HTTP requests and return responses.
WHY: Django views are the "controller" in MVC. Each view receives a request,
     does some work (fetch data, process forms), and returns an HTML response
     by rendering a template with context data. We use function-based views
     (not class-based) because they're simpler and more explicit for beginners.
"""
from django.shortcuts import render
from django.http import Http404
from .news_client import fetch_top_headlines, search_articles, CATEGORIES


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


def article_detail(request, index):
    """
    STEP 6: Article detail page — display a single article by its list index.

    WHY: GNews articles don't have persistent IDs. We use the article's position
         in the headlines list as a temporary identifier. This works because the
         home page and detail page fetch the same headlines list. The index comes
         from the URL: /article/0/ shows the first article, /article/1/ the second.

    Limitation: If GNews updates its headlines between the list page load and the
    detail page click, the index might point to a different article. For a learning
    project this is acceptable. A production app would store articles in a database.
    """
    articles = fetch_top_headlines()

    if index < 0 or index >= len(articles):
        raise Http404("Article not found")

    article = articles[index]
    context = {
        "article": article,
        "categories": CATEGORIES,
    }
    return render(request, "news/article_detail.html", context)


def search(request):
    """
    STEP 7: Search view — find articles matching a query string.

    WHY: We use GET (not POST) for search because:
         1. The URL is bookmarkable: /search?q=python
         2. The URL is shareable: send someone a link to your search
         3. The browser back button works naturally
         4. No CSRF token needed (CSRF protects POST, not GET)

    Django reads query parameters from request.GET — a dict-like object
    that parses the URL's ?key=value pairs automatically.
    """
    query = request.GET.get("q", "").strip()
    articles = search_articles(query) if query else []

    context = {
        "articles": articles,
        "search_query": query,
        "categories": CATEGORIES,
    }
    return render(request, "news/search_results.html", context)


def category(request, cat):
    """
    STEP 7: Category view — display headlines filtered by news category.

    WHY: The category comes from the URL path (/category/technology/), not from
         a query parameter. In Django, path('<str:cat>') captures the URL segment
         and passes it as a keyword argument to the view function. We validate
         that the category exists in our CATEGORIES list to prevent API errors.
    """
    if cat not in CATEGORIES:
        raise Http404(f"Category '{cat}' not found")

    articles = fetch_top_headlines(category=cat)
    context = {
        "articles": articles,
        "categories": CATEGORIES,
        "current_category": cat,
    }
    return render(request, "news/category.html", context)
