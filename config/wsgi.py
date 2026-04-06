"""
STEP 1: WSGI config — the bridge between Django and production servers.
WHY: Django's built-in runserver is for development only. In production, a WSGI server
     like gunicorn imports this file to get the 'application' callable. WSGI (Web Server
     Gateway Interface) is Python's standard for connecting web apps to web servers.
     Gunicorn calls application(environ, start_response) for every HTTP request.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()
