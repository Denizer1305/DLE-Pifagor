from __future__ import annotations

from typing import Any

from apps.backoffice.constants import (
    BACKOFFICE_USER_BULK_ACTION_CHOICES,
    BACKOFFICE_USER_BULK_MAX_ITEMS,
    BackofficeUserBulkAction,
    BackofficeUserMessage,
)
from apps.backoffice.serializers.users.roles import BackofficeUserChangeRolesSerializer
from rest_framework import serializers


class BackofficeUserBulkSerializer(serializers.Serializer):
    """
    Serializer массового административного действия над пользователями.
    """

    action = serializers.ChoiceField(
        choices=BACKOFFICE_USER_BULK_ACTION_CHOICES,
    )
    user_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        allow_empty=False,
        max_length=BACKOFFICE_USER_BULK_MAX_ITEMS,
    )
    reason = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=500,
    )
    role_payload = BackofficeUserChangeRolesSerializer(
        required=False,
        allow_null=True,
    )
    expected_updated_at_map = serializers.DictField(
        child=serializers.DateTimeField(),
        required=False,
        write_only=True,
    )

    def validate_user_ids(self, value: list[int]) -> list[int]:
        """
        Нормализует список пользователей для bulk-операции.
        """

        normalized_user_ids = list(dict.fromkeys(value))

        if not normalized_user_ids:
            raise serializers.ValidationError(BackofficeUserMessage.EMPTY_BULK_USER_IDS)

        return normalized_user_ids

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """
        Проверяет совместимость action и дополнительных payload.
        """

        action = attrs.get("action")
        role_payload = attrs.get("role_payload")

        if action == BackofficeUserBulkAction.CHANGE_ROLES and not role_payload:
            raise serializers.ValidationError(
                {
                    "role_payload": BackofficeUserMessage.ROLE_PAYLOAD_REQUIRED,
                }
            )

        if action != BackofficeUserBulkAction.CHANGE_ROLES and role_payload:
            raise serializers.ValidationError(
                {
                    "role_payload": BackofficeUserMessage.ROLE_PAYLOAD_FORBIDDEN,
                }
            )

        return attrs

    def get_expected_updated_at_for_user(self, user_id: int):
        """
        Возвращает expected_updated_at для конкретного пользователя.
        """

        expected_map = self.validated_data.get("expected_updated_at_map") or {}

        return expected_map.get(str(user_id)) or expected_map.get(user_id)


class BackofficeUserBulkItemResultSerializer(serializers.Serializer):
    """
    Serializer результата обработки одного пользователя в bulk-операции.
    """

    user_id = serializers.IntegerField()
    success = serializers.BooleanField()
    action = serializers.CharField()
    message = serializers.CharField(
        allow_blank=True,
        required=False,
    )
    error_code = serializers.CharField(
        allow_blank=True,
        required=False,
    )
    errors = serializers.DictField(
        required=False,
    )


class BackofficeUserBulkResultSerializer(serializers.Serializer):
    """
    Serializer итогового результата bulk-операции.
    """

    action = serializers.CharField()
    total_count = serializers.IntegerField()
    success_count = serializers.IntegerField()
    failed_count = serializers.IntegerField()
    items = BackofficeUserBulkItemResultSerializer(many=True)
