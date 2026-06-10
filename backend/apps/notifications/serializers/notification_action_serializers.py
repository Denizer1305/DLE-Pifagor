"""
Сериализаторы действий с уведомлениями.

Здесь находятся сериализаторы для ответов после действий:
прочитать, прочитать все, выполнить, архивировать, удалить.
"""

from __future__ import annotations

from apps.notifications.serializers.notification_read_serializers import (
    NotificationDetailSerializer,
)
from rest_framework import serializers


class NotificationActionResponseSerializer(serializers.Serializer):
    """
    Сериализатор ответа после действия с одним уведомлением.
    """

    detail = serializers.CharField()
    notification = NotificationDetailSerializer()


class NotificationBulkActionResponseSerializer(serializers.Serializer):
    """
    Сериализатор ответа после массового действия.
    """

    detail = serializers.CharField()
    updated_count = serializers.IntegerField()
    unread_count = serializers.IntegerField()


class NotificationDeleteResponseSerializer(serializers.Serializer):
    """
    Сериализатор ответа после удаления уведомления.
    """

    detail = serializers.CharField()


class NotificationCompleteResponseSerializer(serializers.Serializer):
    """
    Сериализатор ответа после выполнения уведомления.
    """

    detail = serializers.CharField()
    notification = NotificationDetailSerializer()
