#!/usr/bin/env python
"""
STEP 1: Django's command-line utility for administrative tasks.
WHY: manage.py is the entry point for every Django command — runserver, migrate,
     collectstatic, createsuperuser. It sets DJANGO_SETTINGS_MODULE so Django
     knows which settings file to load. We point it to 'config.settings' because
     we named our project folder 'config' instead of the default project name.
"""
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
