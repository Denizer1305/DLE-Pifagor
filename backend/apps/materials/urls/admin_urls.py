from __future__ import annotations

from django.urls import include, path

from .router import admin_router

app_name = "materials_admin"

urlpatterns = [
    path("", include(admin_router.urls)),
]
