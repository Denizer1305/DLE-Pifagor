from __future__ import annotations

from django.urls import include, path

from .router import public_router

app_name = "materials_public"

urlpatterns = [
    path("", include(public_router.urls)),
]
