"""
STEP 3: App configuration — registers the news app with Django.
WHY: Every Django app needs an AppConfig class. It tells Django the app's name,
     label, and where to find it. When you add 'news' to INSTALLED_APPS, Django
     looks for this class to register the app. Without it, Django can't discover
     the app's templates, template tags, or static files.
"""
from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "news"
    # WHY: verbose_name appears in Django admin and error messages.
    #      It's a human-readable label for the app.
    verbose_name = "News Aggregator"
