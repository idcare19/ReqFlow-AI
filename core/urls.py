from django.contrib import admin
from django.urls import include, path

from .views import health_check, home_redirect

urlpatterns = [
    path("", home_redirect, name="home"),
    path("health/", health_check, name="health_check"),
    path("django-admin/", admin.site.urls),
    path("dashboard/", include(("dashboard.urls", "dashboard"), namespace="dashboard")),
]
