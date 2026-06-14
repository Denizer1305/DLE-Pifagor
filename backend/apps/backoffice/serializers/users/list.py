from __future__ import annotations

from apps.backoffice.serializers.users.related import (
    BackofficeUserRoleSerializer,
    get_active_user_roles,
)
from apps.users.models import User
from rest_framework import serializers


class BackofficeUserListSerializer(serializers.ModelSerializer):
    """
    Read-сериализатор пользователя для административной таблицы.
    """

    full_name = serializers.CharField(
        source="get_full_name",
        read_only=True,
    )
    active_roles = serializers.SerializerMethodField()
    primary_role = serializers.SerializerMethodField()
    role_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "phone",
            "first_name",
            "last_name",
            "middle_name",
            "full_name",
            "birth_date",
            "status",
            "is_active",
            "is_staff",
            "is_superuser",
            "is_email_verified",
            "is_phone_verified",
            "is_login_allowed",
            "scheduled_for_deletion_at",
            "anonymized_at",
            "created_at",
            "updated_at",
            "active_roles",
            "primary_role",
            "role_count",
        ]
        read_only_fields = fields

    def get_active_roles(self, obj) -> list[dict]:
        """
        Возвращает активные роли пользователя.
        """

        return BackofficeUserRoleSerializer(
            get_active_user_roles(obj),
            many=True,
            context=self.context,
        ).data

    def get_primary_role(self, obj) -> dict | None:
        """
        Возвращает первую активную роль пользователя для таблицы.
        """

        active_roles = self.get_active_roles(obj)

        if not active_roles:
            return None

        return active_roles[0]

    def get_role_count(self, obj) -> int:
        """
        Возвращает количество активных ролей пользователя.
        """

        return len(get_active_user_roles(obj))
