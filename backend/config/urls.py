"""
Корневая маршрутизация проекта.

Здесь подключаются:
    - Django admin;
    - API v1;
    - OpenAPI schema;
    - Swagger UI;
    - Redoc;
    - media/static для локальной разработки.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

api_v1_patterns = [
    path("users/", include("apps.users.urls")),
    path("organizations/", include("apps.organizations.urls")),
    path("feedback/", include("apps.feedback.urls")),
    path("dashboard/", include("apps.dashboard.urls")),
    path("notifications/", include("apps.notifications.urls")),
    path("education/", include("apps.education.urls")),
    path("materials/", include("apps.materials.urls")),
    path("courses/", include("apps.course.urls")),
    path("testing/", include("apps.testing.urls")),
]


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("api/v1/", include(api_v1_patterns)),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    if "debug_toolbar" in settings.INSTALLED_APPS:
        urlpatterns += [
            path("__debug__/", include("debug_toolbar.urls")),
        ]
