"""
Маршруты API уведомлений.
"""

from __future__ import annotations

from apps.notifications.views import NotificationViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = "notifications"

router = DefaultRouter()
router.register(
    "",
    NotificationViewSet,
    basename="notifications",
)

urlpatterns = [
    path("", include(router.urls)),
]
