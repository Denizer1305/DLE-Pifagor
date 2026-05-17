from __future__ import annotations

from apps.users.models import InviteCode
from apps.users.serializers.user_serializers import UserShortSerializer
from apps.users.validators.invite_code_validators import validate_invite_code_context
from rest_framework import serializers


class InviteCodeSerializer(serializers.ModelSerializer):
    """
    Сериализатор кода приглашения.

    Открытый код не хранится в базе и здесь не отображается.
    """

    created_by = UserShortSerializer(read_only=True)
    target_user = UserShortSerializer(read_only=True)
    is_expired = serializers.BooleanField(read_only=True)
    is_available = serializers.BooleanField(read_only=True)

    class Meta:
        model = InviteCode
        fields = [
            "id",
            "purpose",
            "organization",
            "department",
            "group",
            "created_by",
            "target_user",
            "expires_at",
            "max_uses",
            "used_count",
            "is_active",
            "last_used_at",
            "is_expired",
            "is_available",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_by",
            "target_user",
            "used_count",
            "last_used_at",
            "is_expired",
            "is_available",
            "created_at",
            "updated_at",
        ]


class InviteCodeCreateSerializer(serializers.Serializer):
    """
    Сериализатор создания кода приглашения.
    """

    purpose = serializers.CharField(max_length=64)
    organization_id = serializers.IntegerField(required=False, allow_null=True)
    department_id = serializers.IntegerField(required=False, allow_null=True)
    group_id = serializers.IntegerField(required=False, allow_null=True)
    target_user_id = serializers.IntegerField(required=False, allow_null=True)
    ttl_hours = serializers.IntegerField(required=False, min_value=1, max_value=720)
    max_uses = serializers.IntegerField(required=False, min_value=1, max_value=100)

    def validate(self, attrs):
        """
        Проверяет минимальный контекст кода приглашения.

        Args:
            attrs:
                Данные serializer.

        Returns:
            dict: Проверенные данные.
        """

        validate_invite_code_context(
            purpose=attrs.get("purpose"),
            organization=attrs.get("organization"),
            group=attrs.get("group"),
            target_user=attrs.get("target_user"),
        )

        return attrs


class InviteCodeCreatedSerializer(serializers.Serializer):
    """
    Сериализатор ответа после создания кода.

    Важно:
        raw_code показывается только один раз.
    """

    invite_code = InviteCodeSerializer()
    raw_code = serializers.CharField()
