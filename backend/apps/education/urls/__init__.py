from __future__ import annotations

from django.urls import include, path

urlpatterns = [
    path("admin/", include("apps.education.urls.admin_urls")),
    path("public/", include("apps.education.urls.public_urls")),
]
