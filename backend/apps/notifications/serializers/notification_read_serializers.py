"""
Сериализаторы чтения уведомлений.

Здесь находятся сериализаторы, которые отвечают за отдачу уведомлений
во frontend: список, детальная карточка, счётчик непрочитанных уведомлений.
"""

from __future__ import annotations

from apps.notifications.models import Notification
from rest_framework import serializers


class NotificationRecipientSerializer(serializers.Serializer):
    """
    Краткое представление получателя уведомления.
    """

    id = serializers.IntegerField()
    email = serializers.EmailField()
    full_name = serializers.CharField()


class NotificationListSerializer(serializers.ModelSerializer):
    """
    Сериализатор уведомления для списка и выпадающего меню.
    """

    has_action = serializers.BooleanField(read_only=True)
    is_unread = serializers.BooleanField(read_only=True)

    class Meta:
        model = Notification
        fields = [
            "id",
            "title",
            "message",
            "notification_type",
            "category",
            "level",
            "status",
            "recipient_role",
            "source_type",
            "source_id",
            "action_label",
            "action_url",
            "has_action",
            "is_unread",
            "event_at",
            "read_at",
            "completed_at",
            "expires_at",
            "created_at",
        ]


class NotificationDetailSerializer(serializers.ModelSerializer):
    """
    Детальный сериализатор уведомления.
    """

    has_action = serializers.BooleanField(read_only=True)
    is_unread = serializers.BooleanField(read_only=True)
    is_read = serializers.BooleanField(read_only=True)
    is_completed = serializers.BooleanField(read_only=True)
    is_archived = serializers.BooleanField(read_only=True)
    is_expired = serializers.BooleanField(read_only=True)
    recipient = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            "id",
            "recipient",
            "title",
            "message",
            "notification_type",
            "category",
            "level",
            "status",
            "recipient_role",
            "source_type",
            "source_id",
            "deduplication_key",
            "action_label",
            "action_url",
            "has_action",
            "delivery_channels",
            "delivery_statuses",
            "payload",
            "event_at",
            "read_at",
            "completed_at",
            "expires_at",
            "created_at",
            "updated_at",
            "is_unread",
            "is_read",
            "is_completed",
            "is_archived",
            "is_expired",
        ]
        read_only_fields = fields

    def get_recipient(self, obj: Notification) -> dict:
        """
        Возвращает краткое представление получателя.
        """

        user = obj.recipient

        return {
            "id": user.id,
            "email": user.email,
            "full_name": get_user_full_name(user),
        }


class NotificationUnreadCountSerializer(serializers.Serializer):
    """
    Сериализатор количества непрочитанных уведомлений.
    """

    unread_count = serializers.IntegerField()


class NotificationFeedSerializer(serializers.Serializer):
    """
    Сериализатор ленты уведомлений пользователя.
    """

    unread_count = serializers.IntegerField()
    items = NotificationListSerializer(many=True)


class NotificationQuerySerializer(serializers.Serializer):
    """
    Сериализатор query-параметров списка уведомлений.
    """

    status = serializers.CharField(required=False, allow_blank=True)
    level = serializers.CharField(required=False, allow_blank=True)
    category = serializers.CharField(required=False, allow_blank=True)
    notification_type = serializers.CharField(required=False, allow_blank=True)
    source_type = serializers.CharField(required=False, allow_blank=True)
    source_id = serializers.CharField(required=False, allow_blank=True)
    unread_only = serializers.BooleanField(required=False, default=False)

    def validate(self, attrs: dict) -> dict:
        """
        Нормализует query-параметры.
        """

        for field in [
            "status",
            "level",
            "category",
            "notification_type",
            "source_type",
            "source_id",
        ]:
            if field in attrs and isinstance(attrs[field], str):
                attrs[field] = attrs[field].strip()

        return attrs


def get_user_full_name(user) -> str:
    """
    Возвращает полное имя пользователя.
    """

    if hasattr(user, "get_full_name"):
        full_name = user.get_full_name()

        if full_name:
            return full_name

    return user.email
