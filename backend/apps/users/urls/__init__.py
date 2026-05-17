from __future__ import annotations

from apps.users.urls.router import urlpatterns as router_urlpatterns
from django.urls import include, path

app_name = "users"


urlpatterns = [
    path(
        "auth/",
        include("apps.users.urls.auth_urls"),
    ),
    path(
        "",
        include(router_urlpatterns),
    ),
]
