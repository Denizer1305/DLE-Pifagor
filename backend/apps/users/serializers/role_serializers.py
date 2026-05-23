from __future__ import annotations

from apps.users.models import Role, UserRole
from apps.users.serializers.user_serializers import UserShortSerializer
from rest_framework import serializers


class RoleSerializer(serializers.ModelSerializer):
    """
    Сериализатор системной роли.
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
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "code",
            "is_system",
            "created_at",
            "updated_at",
        ]


class RoleShortSerializer(serializers.ModelSerializer):
    """
    Краткий сериализатор роли.
    """

    class Meta:
        model = Role
        fields = [
            "id",
            "code",
            "label",
        ]
        read_only_fields = fields


class UserRoleSerializer(serializers.ModelSerializer):
    """
    Сериализатор назначенной роли пользователя.
    """

    user = UserShortSerializer(read_only=True)
    role = RoleShortSerializer(read_only=True)

    class Meta:
        model = UserRole
        fields = [
            "id",
            "user",
            "role",
            "organization",
            "department",
            "group",
            "status",
            "assigned_by",
            "assigned_at",
            "revoked_by",
            "revoked_at",
            "revoke_reason",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "role",
            "status",
            "assigned_by",
            "assigned_at",
            "revoked_by",
            "revoked_at",
            "created_at",
            "updated_at",
        ]


class UserRoleCreateSerializer(serializers.Serializer):
    """
    Сериализатор назначения роли пользователю.

    Финальная бизнес-проверка выполняется в сервисном слое.
    """

    user_id = serializers.IntegerField()
    role_code = serializers.CharField(max_length=64)
    organization_id = serializers.IntegerField(required=False, allow_null=True)
    department_id = serializers.IntegerField(required=False, allow_null=True)
    group_id = serializers.IntegerField(required=False, allow_null=True)

    def validate_role_code(self, value: str) -> str:
        """
        Нормализует код роли.

        Args:
            value:
                Код роли.

        Returns:
            str: Нормализованный код роли.
        """

        return value.strip()
