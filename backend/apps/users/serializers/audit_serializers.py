from __future__ import annotations

from apps.users.models import RegistrationAttemptLog, UserAuditLog
from apps.users.serializers.user_serializers import UserShortSerializer
from rest_framework import serializers


class UserAuditLogSerializer(serializers.ModelSerializer):
    """
    Сериализатор записи аудита пользователя.
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


class RegistrationAttemptLogSerializer(serializers.ModelSerializer):
    """
    Сериализатор попытки регистрации.
    """

    class Meta:
        model = RegistrationAttemptLog
        fields = [
            "id",
            "email_hash",
            "phone_hash",
            "role_code",
            "status",
            "failure_reason",
            "ip_address",
            "user_agent",
            "metadata",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields
