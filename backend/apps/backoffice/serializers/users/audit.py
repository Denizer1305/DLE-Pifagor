from __future__ import annotations

from apps.users.models import UserAuditLog
from apps.users.serializers.user_serializers import UserShortSerializer
from rest_framework import serializers


class BackofficeUserAuditLogListSerializer(serializers.ModelSerializer):
    """
    Read-сериализатор истории действий по пользователю в backoffice.
    """

    actor = UserShortSerializer(read_only=True)
    target_user = UserShortSerializer(read_only=True)

    class Meta:
        model = UserAuditLog
        fields = [
            "id",
            "actor",
            "actor_type",
            "target_user",
            "action",
            "message",
            "metadata",
            "ip_address",
            "user_agent",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields
