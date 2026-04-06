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


# STEP 8: Custom 404 handler — uses our dark-themed 404 template.
# WHY: handler404 tells Django which view to call when no URL pattern matches.
#      We use Django's built-in page_not_found view, which renders templates/404.html
#      automatically. This only activates when DEBUG=False.
handler404 = "django.views.defaults.page_not_found"
