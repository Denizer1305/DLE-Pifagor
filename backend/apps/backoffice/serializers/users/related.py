from __future__ import annotations

from apps.users.constants.lifecycle import UserRoleStatus
from apps.users.models import UserRole
from apps.users.serializers.role_serializers import RoleShortSerializer
from apps.users.serializers.user_serializers import UserShortSerializer
from rest_framework import serializers


def build_backoffice_related_object_payload(obj) -> dict | None:
    """
    Возвращает короткое представление связанного объекта.

    Используется для организации, отделения и группы без жёсткой зависимости
    от конкретных serializer'ов других приложений.
    """

    if obj is None:
        return None

    name = (
        getattr(obj, "name", "")
        or getattr(obj, "title", "")
        or getattr(obj, "short_name", "")
        or str(obj)
    )

    return {
        "id": obj.id,
        "name": name,
        "code": getattr(obj, "code", ""),
    }


class BackofficeUserRoleSerializer(serializers.ModelSerializer):
    """
    Read-сериализатор роли пользователя для backoffice.

    Возвращает:
    - саму роль;
    - организацию;
    - отделение;
    - группу;
    - кто назначил и кто отозвал роль.
    """

    role = RoleShortSerializer(read_only=True)
    organization_payload = serializers.SerializerMethodField()
    department_payload = serializers.SerializerMethodField()
    group_payload = serializers.SerializerMethodField()
    assigned_by = UserShortSerializer(read_only=True)
    revoked_by = UserShortSerializer(read_only=True)

    class Meta:
        model = UserRole
        fields = [
            "id",
            "role",
            "organization",
            "organization_payload",
            "department",
            "department_payload",
            "group",
            "group_payload",
            "status",
            "assigned_by",
            "assigned_at",
            "revoked_by",
            "revoked_at",
            "revoke_reason",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields

    def get_organization_payload(self, obj) -> dict | None:
        """
        Возвращает короткое представление организации.
        """

        return build_backoffice_related_object_payload(obj.organization)

    def get_department_payload(self, obj) -> dict | None:
        """
        Возвращает короткое представление отделения.
        """

        return build_backoffice_related_object_payload(obj.department)

    def get_group_payload(self, obj) -> dict | None:
        """
        Возвращает короткое представление группы.
        """

        return build_backoffice_related_object_payload(obj.group)


def get_active_user_roles(user) -> list[UserRole]:
    """
    Возвращает активные роли пользователя из prefetched user_roles.
    """

    return [
        user_role
        for user_role in user.user_roles.all()
        if user_role.status == UserRoleStatus.ACTIVE
    ]
