from __future__ import annotations

from typing import Any

from apps.backoffice.constants import (
    BACKOFFICE_USER_EDITABLE_FIELDS,
    BackofficeUserMessage,
)
from apps.users.models import User
from rest_framework import serializers


class BackofficeUserUpdateSerializer(serializers.Serializer):
    """
    Serializer редактирования пользователя через backoffice.

    Не меняет:
    - роли;
    - status;
    - is_staff;
    - is_superuser;
    - lifecycle-поля удаления и анонимизации.
    """

    email = serializers.EmailField(required=False)
    backup_email = serializers.EmailField(
        required=False,
        allow_blank=True,
    )
    phone = serializers.CharField(
        required=False,
        allow_blank=False,
        max_length=32,
    )
    first_name = serializers.CharField(
        required=False,
        allow_blank=False,
        max_length=150,
    )
    last_name = serializers.CharField(
        required=False,
        allow_blank=False,
        max_length=150,
    )
    middle_name = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=150,
    )
    birth_date = serializers.DateField(
        required=False,
        allow_null=True,
    )
    is_login_allowed = serializers.BooleanField(required=False)
    account_managed_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        allow_null=True,
    )
    expected_updated_at = serializers.DateTimeField(
        required=False,
        write_only=True,
    )
    reason = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=500,
        write_only=True,
    )

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """
        Проверяет payload редактирования пользователя.
        """

        if not any(field in attrs for field in BACKOFFICE_USER_EDITABLE_FIELDS):
            raise serializers.ValidationError(
                BackofficeUserMessage.UPDATE_PAYLOAD_EMPTY
            )

        return attrs

    def get_service_payload(self) -> dict[str, Any]:
        """
        Возвращает данные для service-слоя без служебных полей.
        """

        service_payload = dict(self.validated_data)
        service_payload.pop("expected_updated_at", None)
        service_payload.pop("reason", None)

        return service_payload
