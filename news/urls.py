"""
STEP 5: News app URL patterns.
WHY: Each app has its own urls.py so URL routing stays modular.
     The root config/urls.py includes this file with include('news.urls').
     'app_name' enables namespacing — {% url 'news:home' %} in templates
     avoids name collisions if you add more apps later.
"""
from django.urls import path
from . import views

# WHY: app_name enables URL namespacing. In templates, you write {% url 'news:home' %}
#      instead of {% url 'home' %}. This prevents name conflicts between apps.
app_name = "news"

urlpatterns = [
    path("", views.home, name="home"),
]
