"""
Сериализаторы bootstrap-синхронизации уведомлений.

Bootstrap вызывается frontend частью при входе пользователя в личный кабинет.
Он проверяет, что уведомления на текущий день созданы, и догенерирует
недостающие без дублей.
"""

from __future__ import annotations

from apps.notifications.constants import NotificationBootstrapReason
from rest_framework import serializers

BOOTSTRAP_REASONS = {
    NotificationBootstrapReason.DASHBOARD_LOGIN,
    NotificationBootstrapReason.MANUAL_SYNC,
    NotificationBootstrapReason.CELERY_FALLBACK,
}


class NotificationBootstrapRequestSerializer(serializers.Serializer):
    """
    Сериализатор запроса bootstrap-синхронизации.
    """

    reason = serializers.CharField(
        required=False,
        allow_blank=True,
        default=NotificationBootstrapReason.DASHBOARD_LOGIN,
    )
    target_date = serializers.DateField(
        required=False,
        allow_null=True,
    )

    def validate_reason(self, value: str) -> str:
        """
        Проверяет причину bootstrap-синхронизации.
        """

        if not value:
            return NotificationBootstrapReason.DASHBOARD_LOGIN

        if value not in BOOTSTRAP_REASONS:
            raise serializers.ValidationError(
                "Недопустимая причина синхронизации уведомлений."
            )

        return value


class NotificationBootstrapResponseSerializer(serializers.Serializer):
    """
    Сериализатор ответа bootstrap-синхронизации.
    """

    target_date = serializers.DateField()
    created_count = serializers.IntegerField()
    created_ids = serializers.ListField(
        child=serializers.IntegerField(),
    )
    unread_count = serializers.IntegerField()
