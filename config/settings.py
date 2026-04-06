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
#      on each request. Django still requires a DATABASES setting with a
#      'default' key, even if we never use it. Using SQLite with an in-memory
#      database satisfies Django's requirement without creating any files.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


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

# WHY: In production (DEBUG=False), CompressedManifestStaticFilesStorage:
#      1. Adds a hash to filenames (style.abc123.css) for cache busting
#      2. Compresses files with gzip/brotli for faster downloads
#      In development (DEBUG=True), we skip this because it requires collectstatic.
if not DEBUG:
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


# --- STEP 8: Production security settings ---
# WHY: These settings only matter when DEBUG=False (production on Render).
#      They protect against common web attacks.

if not DEBUG:
    # WHY: Render terminates SSL at its proxy and forwards requests over HTTP.
    #      This header tells Django the original request was HTTPS, so it doesn't
    #      reject the request or redirect infinitely.
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

    # WHY: CSRF_TRUSTED_ORIGINS is required for POST requests in production.
    #      Without it, Django blocks form submissions with a 403 Forbidden error.
    #      We trust any .onrender.com subdomain.
    CSRF_TRUSTED_ORIGINS = [
        "https://*.onrender.com",
    ]
