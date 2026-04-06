"""
STEP 2: Django settings — the central configuration file for the entire project.
WHY: Every Django setting lives here: database, templates, static files, middleware,
     installed apps. We use python-dotenv to load secrets from .env so they never
     get committed to git. This is the #1 security rule in web development.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# WHY: load_dotenv() reads .env file and puts values into os.environ.
#      Call this BEFORE reading any env vars so they're available.
load_dotenv()

# WHY: BASE_DIR points to the project root (where manage.py lives).
#      All paths in settings are relative to this, so the project works
#      on any machine regardless of where it's cloned.
BASE_DIR = Path(__file__).resolve().parent.parent


# --- Security ---

# WHY: SECRET_KEY is used for cryptographic signing (sessions, CSRF tokens, passwords).
#      NEVER hardcode it. In production, Render generates a random one via render.yaml.
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-change-me-in-production")

# WHY: DEBUG=True shows detailed error pages with stack traces — helpful for development
#      but a security risk in production (it exposes your code to the internet).
DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")

# WHY: Django rejects requests to hostnames not in this list. This prevents
#      HTTP Host header attacks. In production, add your Render domain here.
ALLOWED_HOSTS = [
    h.strip() for h in os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
]


# --- Apps ---

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    # WHY: We don't include auth, admin, sessions, or messages because this project
    #      has no database and no user accounts. Only what we actually use.
    "news",
    # WHY: Register our news app so Django discovers its templates, template tags,
    #      and AppConfig. The string 'news' matches the name in news/apps.py.
]


# --- Middleware ---

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # WHY: WhiteNoise serves static files (CSS, JS, images) in production.
    #      Django's built-in static file serving only works with DEBUG=True.
    #      WhiteNoise plugs in as middleware — no nginx or CDN needed.
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
]


# --- URL config ---

ROOT_URLCONF = "config.urls"


# --- Templates ---

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # WHY: We put templates in a project-level 'templates/' folder instead of
        #      inside each app. For a single-app project this is cleaner — all HTML
        #      lives in one place. Django searches these DIRS first, then app folders.
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
            ],
        },
    },
]


# --- WSGI ---

WSGI_APPLICATION = "config.wsgi.application"


# --- Database ---
# WHY: This project has NO database. We fetch everything from the GNews API
#      on each request. Django requires a DATABASES setting, but we use an
#      empty dict to signal "no database". This means no migrations needed.
DATABASES = {}


# --- Static files ---

# WHY: STATIC_URL is the URL prefix for static files in HTML.
#      {% static 'css/style.css' %} becomes '/static/css/style.css'.
STATIC_URL = "/static/"

# WHY: STATICFILES_DIRS tells Django where to find static files during development.
#      We use a project-level 'static/' folder (same idea as project-level templates).
STATICFILES_DIRS = [BASE_DIR / "static"]

# WHY: STATIC_ROOT is where 'collectstatic' copies all static files for production.
#      WhiteNoise serves files from this folder. It must be different from STATICFILES_DIRS.
STATIC_ROOT = BASE_DIR / "staticfiles"

# WHY: CompressedManifestStaticFilesStorage does two things:
#      1. Adds a hash to filenames (style.abc123.css) for cache busting
#      2. Compresses files with gzip/brotli for faster downloads
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# --- GNews API ---
# WHY: Store the API key in settings so any module can import it.
#      The actual value comes from .env (never hardcoded).
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY", "")


# --- Internationalization ---

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = False
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
