from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("dashboard/", include(("dashboard.urls", "dashboard"), namespace="dashboard")),
]
