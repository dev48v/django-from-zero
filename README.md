# django-from-zero

**Day 8 of TechFromZero** — a real News Aggregator built with Django, server-side templates, and the GNews API. Deployed live on Render for free.

## Quick Start

```bash
git clone https://github.com/dev48v/django-from-zero.git
cd django-from-zero
python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
cp .env.example .env        # fill in your API key
python manage.py runserver
```

Open `http://localhost:8000` to browse the news.

You need:
- **GNews API key** — free at [gnews.io](https://gnews.io/) (100 requests/day, works from any server)

---

## Pages

| URL | Page | Description |
|-----|------|-------------|
| `/` | Home | Top headlines from around the world |
| `/category/{cat}/` | Category | Headlines filtered by category |
| `/search/?q=term` | Search | Search articles by keyword |
| `/article/{index}/` | Article Detail | Full article view with timeago |

**Categories:** general, world, nation, business, technology, entertainment, sports, science, health

---

## Step-by-Step Guide

Each commit = one concept. Read through these in order to understand how the app is built from scratch.

### STEP 1 — Project scaffold
**What:** Create `manage.py`, `requirements.txt`, `.env.example`, and the `config/` package.

**Why:** Django projects start with `django-admin startproject`. We name the project folder `config/` instead of the default because it's clearer — this folder contains configuration, not application code.

**Key files:** `manage.py`, `config/wsgi.py`, `requirements.txt`

---

### STEP 2 — Django settings
**What:** Configure `settings.py` with environment variables, WhiteNoise for static files, and project-level template dirs.

**Why:** `SECRET_KEY` and `DEBUG` come from `.env` so secrets never touch git. WhiteNoise serves CSS/JS in production without nginx. Template dirs point to a project-level `templates/` folder for simplicity.

**Key file:** `config/settings.py`

---

### STEP 3 — News app
**What:** Create the `news` Django app with `AppConfig`.

**Why:** Django apps are modular. The `news` app handles all news-related logic. Registering it in `INSTALLED_APPS` lets Django discover its templates and template tags.

**Key file:** `news/apps.py`

---

### STEP 4 — GNews API client
**What:** Create `news_client.py` with `fetch_top_headlines()` and `search_articles()`.

**Why:** All external API calls live in one file. Views call these functions without knowing anything about GNews. If we switch to a different API, we change one file.

**Key file:** `news/news_client.py`

---

### STEP 5 — Home page
**What:** Build the home page with Django template inheritance, function-based views, and dark theme CSS.

**Why:** `base.html` defines the layout (nav, footer, CSS). `home.html` extends it and fills in the content block. This is DRY — change the nav once, every page updates.

**Key files:** `templates/base.html`, `templates/news/home.html`, `static/css/style.css`

---

### STEP 6 — Article detail with custom template tag
**What:** Build the article detail page and a custom `|timeago` template filter.

**Why:** Django templates don't allow arbitrary Python. Custom template tags extend the template language. Our `|timeago` filter converts ISO dates to "2 hours ago" — a presentation concern that belongs in the template layer.

**Key files:** `templates/news/article_detail.html`, `news/templatetags/news_extras.py`

---

### STEP 7 — Search and category pages
**What:** Add search (GET /search?q=...) and category (/category/technology/) pages.

**Why:** Search uses GET (not POST) so URLs are bookmarkable. Categories use path parameters because they represent distinct resources. The category page includes clickable pills for switching.

**Key files:** `templates/news/search_results.html`, `templates/news/category.html`

---

### STEP 8 — Error pages and production polish
**What:** Custom 404 page, CSRF_TRUSTED_ORIGINS, SECURE_PROXY_SSL_HEADER.

**Why:** Production needs security settings that dev doesn't. Render terminates SSL at its proxy, so Django needs `SECURE_PROXY_SSL_HEADER` to know the original request was HTTPS.

**Key files:** `templates/404.html`, `config/settings.py`

---

### STEP 9 — Render deploy config
**What:** `render.yaml` — Infrastructure as Code for one-click deploys.

**Why:** The deploy config lives in the repo (not a dashboard). Build step installs dependencies and runs `collectstatic`. Gunicorn replaces the dev server. Secret key is auto-generated.

**Key file:** `render.yaml`

---

### STEP 10 — Documentation
**What:** This README, LinkedIn post, and social image card.

**Why:** A project without a README is hard to use. Every beginner-friendly project needs a clear quick start and step-by-step explanations.

---

## Deploy to Render (Free)

1. Push this repo to GitHub
2. Go to [render.com](https://render.com) → New Web Service → connect your repo
3. Render auto-detects `render.yaml`
4. Add your `GNEWS_API_KEY` in the Render dashboard
5. Deploy — your app is live at `https://django-from-zero.onrender.com`

---

## Architecture

```
Browser (any device)
        ↓
  Render (free hosting)
        ↓
  Django Views (Python)
    ├── requests lib → GNews API (fetch headlines/search)
    ├── Django Templates → render HTML server-side
    └── WhiteNoise → serve static CSS
        ↓
  HTML response → Browser
```

---

## Dependencies

| Package | Why |
|---------|-----|
| django | The web framework — handles URL routing, templates, static files |
| requests | HTTP client — fetches news from GNews API |
| python-dotenv | Loads `.env` into `os.environ` — keeps secrets out of code |
| gunicorn | Production WSGI server (replaces `runserver`) |
| whitenoise | Serves static files in production without nginx |

---

*Day 8 of the [TechFromZero series](https://dev48v.infy.uk/techfromzero.php) — one real project per day, built from scratch.*
