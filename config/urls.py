"""
STEP 2: Root URL configuration — the entry point for all URL routing.
WHY: Django matches incoming URLs against these patterns top-to-bottom.
     We use include() to delegate all news-related URLs to the news app's
     own urls.py file. This keeps routing modular — each app owns its URLs.
"""
from django.urls import path, include

urlpatterns = [
    # WHY: Empty string "" means the news app handles the root URL (/).
    #      include('news.urls') delegates to news/urls.py for all patterns.
    path("", include("news.urls")),
]
