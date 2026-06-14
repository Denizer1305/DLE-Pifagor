from __future__ import annotations

from typing import Any

from apps.users.models import Role
from rest_framework import serializers


class BackofficeUserRoleAssignmentSerializer(serializers.Serializer):
    """
    Serializer назначения роли пользователю.

    Формат:
    {
        "role_id": 1,
        "organization_id": 1,
        "department_id": 2,
        "group_id": 3
    }
    """

    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.filter(is_active=True),
        source="role",
    )
    organization_id = serializers.IntegerField(
        required=False,
        allow_null=True,
    )
    department_id = serializers.IntegerField(
        required=False,
        allow_null=True,
    )
    group_id = serializers.IntegerField(
        required=False,
        allow_null=True,
    )

    def to_internal_value(self, data):
        """
        Преобразует role_id обратно в ID роли для service-слоя.
        """

        internal_data = super().to_internal_value(data)

        role = internal_data.pop("role")
        internal_data["role_id"] = role.id

        return internal_data


class BackofficeUserChangeRolesSerializer(serializers.Serializer):
    """
    Serializer изменения ролей пользователя через backoffice.
    """

    assigned_roles = BackofficeUserRoleAssignmentSerializer(
        many=True,
        required=False,
    )
    revoked_user_role_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        required=False,
    )
    reason = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=500,
    )
    expected_updated_at = serializers.DateTimeField(
        required=False,
        write_only=True,
    )

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """
        Проверяет, что передано хотя бы одно изменение ролей.
        """

        assigned_roles = attrs.get("assigned_roles") or []
        revoked_user_role_ids = attrs.get("revoked_user_role_ids") or []

        if not assigned_roles and not revoked_user_role_ids:
            raise serializers.ValidationError(
                "Нужно передать роли для назначения или отзыва."
            )

        return attrs


class BackofficeUserAvailableRoleSerializer(serializers.ModelSerializer):
    """
    Serializer доступной роли для dropdown'а в backoffice.
    """

    class Meta:
        model = Role
        fields = [
            "id",
            "code",
            "label",
            "description",
            "is_system",
            "is_active",
            "sort_order",
        ]
        read_only_fields = fields
