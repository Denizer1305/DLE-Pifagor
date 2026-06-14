from __future__ import annotations

from django.urls import include, path

urlpatterns = [
    path(
        "users/",
        include("apps.backoffice.urls.users_urls"),
    ),
]
