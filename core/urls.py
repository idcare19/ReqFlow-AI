from django.contrib import admin
from django.urls import include, path

from .api_views import api_health, api_login, api_logout, api_me
from .views import health_check, home_redirect

urlpatterns = [
    path("", home_redirect, name="home"),
    path("health/", health_check, name="health_check"),
    path("api/health/", api_health, name="api_health"),
    path("api/auth/login/", api_login, name="api_login"),
    path("api/auth/logout/", api_logout, name="api_logout"),
    path("api/auth/me/", api_me, name="api_me"),
    path("django-admin/", admin.site.urls),
    path("dashboard/", include(("dashboard.urls", "dashboard"), namespace="dashboard")),
]
