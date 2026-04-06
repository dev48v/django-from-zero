"""
STEP 6: Custom template tags — extend Django's template language with our own filters.
WHY: Django templates are intentionally limited — no arbitrary Python in HTML.
     But sometimes you need custom logic in templates. Django's solution: template
     tags and filters. You write Python, register it, and use it in HTML with
     {% load news_extras %} and {{ value|timeago }}. This keeps logic in Python
     while templates stay clean.
"""
from datetime import datetime, timezone
from django import template

# WHY: register is required. Django discovers template tags by looking for a
#      module-level 'register' variable of type template.Library in files
#      inside a 'templatetags/' directory. Without it, {% load news_extras %} fails.
register = template.Library()


@register.filter(name="timeago")
def timeago(value):
    """
    Convert an ISO 8601 date string to a human-readable "time ago" format.

    Usage in templates: {{ article.publishedAt|timeago }}
    Output: "2 hours ago", "3 days ago", "just now"

    WHY: GNews returns dates as ISO strings like "2026-04-06T14:30:00Z".
         Showing "2 hours ago" is more intuitive than a raw timestamp.
         We parse the string here instead of in the view because formatting
         is a presentation concern — it belongs in the template layer.
    """
    if not value:
        return ""

    try:
        # WHY: GNews dates end with 'Z' (UTC) or have timezone offset.
        #      Replace 'Z' with '+00:00' for Python's fromisoformat parser.
        if isinstance(value, str):
            clean = value.replace("Z", "+00:00")
            dt = datetime.fromisoformat(clean)
        else:
            dt = value

        now = datetime.now(timezone.utc)
        diff = now - dt

        seconds = int(diff.total_seconds())
        if seconds < 60:
            return "just now"
        elif seconds < 3600:
            minutes = seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif seconds < 86400:
            hours = seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif seconds < 604800:
            days = seconds // 86400
            return f"{days} day{'s' if days != 1 else ''} ago"
        else:
            # WHY: For anything older than a week, show the actual date.
            #      "23 days ago" is less useful than "Mar 14, 2026".
            return dt.strftime("%b %d, %Y")
    except (ValueError, TypeError):
        # WHY: If the date string is malformed, return it as-is rather than crashing.
        #      A template filter should never raise an exception.
        return str(value) if value else ""
