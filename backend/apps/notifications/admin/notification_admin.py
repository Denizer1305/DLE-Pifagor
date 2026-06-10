"""
Админ-панель уведомлений.
"""

from __future__ import annotations

from apps.notifications.models import Notification
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Админ-панель модели уведомления.
    """

    list_display = [
        "id",
        "title",
        "recipient",
        "notification_type",
        "category",
        "level",
        "status",
        "recipient_role",
        "created_at",
        "read_at",
        "expires_at",
    ]
    list_filter = [
        "status",
        "level",
        "category",
        "notification_type",
        "recipient_role",
        "source_type",
        "created_at",
        "expires_at",
    ]
    search_fields = [
        "title",
        "message",
        "recipient__email",
        "recipient__first_name",
        "recipient__last_name",
        "source_id",
        "deduplication_key",
    ]
    readonly_fields = [
        "created_at",
        "updated_at",
        "read_at",
        "completed_at",
        "expires_at",
    ]
    ordering = [
        "status",
        "-created_at",
        "-id",
    ]
    date_hierarchy = "created_at"
    list_per_page = 50

    fieldsets = [
        (
            _("Получатель"),
            {
                "fields": [
                    "recipient",
                    "recipient_role",
                ],
            },
        ),
        (
            _("Содержание"),
            {
                "fields": [
                    "title",
                    "message",
                    "level",
                    "status",
                ],
            },
        ),
        (
            _("Тип и источник"),
            {
                "fields": [
                    "notification_type",
                    "category",
                    "source_type",
                    "source_id",
                    "deduplication_key",
                ],
            },
        ),
        (
            _("Действие"),
            {
                "fields": [
                    "action_label",
                    "action_url",
                ],
            },
        ),
        (
            _("Доставка"),
            {
                "fields": [
                    "delivery_channels",
                    "delivery_statuses",
                    "payload",
                ],
            },
        ),
        (
            _("Даты"),
            {
                "fields": [
                    "event_at",
                    "read_at",
                    "completed_at",
                    "expires_at",
                    "created_at",
                    "updated_at",
                ],
            },
        ),
    ]
