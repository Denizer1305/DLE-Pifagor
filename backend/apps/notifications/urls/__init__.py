"""
Публичный интерфейс urls приложения notifications.
"""

from __future__ import annotations

from apps.notifications.urls.notification_urls import app_name, urlpatterns

__all__ = [
    "app_name",
    "urlpatterns",
]
