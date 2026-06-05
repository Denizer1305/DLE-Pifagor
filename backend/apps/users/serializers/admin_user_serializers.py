from __future__ import annotations

from typing import Any

from apps.users.constants.lifecycle import UserRoleStatus
from apps.users.models import Role, User, UserAuditLog, UserRole
from apps.users.serializers.audit_serializers import UserAuditLogSerializer
from apps.users.serializers.profile_serializers import ProfileSerializer
from apps.users.serializers.role_serializers import RoleShortSerializer
from apps.users.serializers.user_serializers import UserShortSerializer
from apps.users.services.admin_users.bulk_services import AdminUserBulkAction
from rest_framework import serializers


def build_admin_related_object_payload(obj) -> dict | None:
    """
    Возвращает короткое представление связанного объекта.

    Используется для организации, отделения и группы без жёсткой зависимости
    от конкретных сериализаторов других приложений.

    Args:
        obj:
            Связанный объект или None.

    Returns:
        dict | None: Короткое представление объекта.
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


class AdminUserRoleSerializer(serializers.ModelSerializer):
    """
    Сериализатор роли пользователя для административного раздела.

    Возвращает не только ID связей, но и короткое представление роли,
    организации, отделения и группы.
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

        Args:
            obj:
                Назначенная роль пользователя.

        Returns:
            dict | None: Организация.
        """

        return build_admin_related_object_payload(obj.organization)

    def get_department_payload(self, obj) -> dict | None:
        """
        Возвращает короткое представление отделения.

        Args:
            obj:
                Назначенная роль пользователя.

        Returns:
            dict | None: Отделение.
        """

        return build_admin_related_object_payload(obj.department)

    def get_group_payload(self, obj) -> dict | None:
        """
        Возвращает короткое представление группы.

        Args:
            obj:
                Назначенная роль пользователя.

        Returns:
            dict | None: Группа.
        """

        return build_admin_related_object_payload(obj.group)


class AdminUserListSerializer(serializers.ModelSerializer):
    """
    Сериализатор пользователя для административной таблицы.

    Используется на страницах:
        - /admin/users;
        - /admin/users/students;
        - /admin/users/teachers;
        - /admin/users/parents.
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

        Args:
            obj:
                Пользователь.

        Returns:
            list[dict]: Активные роли.
        """

        active_user_roles = [
            user_role
            for user_role in obj.user_roles.all()
            if user_role.status == UserRoleStatus.ACTIVE
        ]

        return AdminUserRoleSerializer(
            active_user_roles,
            many=True,
            context=self.context,
        ).data

    def get_primary_role(self, obj) -> dict | None:
        """
        Возвращает первую активную роль пользователя для таблицы.

        Args:
            obj:
                Пользователь.

        Returns:
            dict | None: Основная роль.
        """

        active_roles = self.get_active_roles(obj)

        if not active_roles:
            return None

        return active_roles[0]

    def get_role_count(self, obj) -> int:
        """
        Возвращает количество активных ролей пользователя.

        Args:
            obj:
                Пользователь.

        Returns:
            int: Количество активных ролей.
        """

        return sum(
            1
            for user_role in obj.user_roles.all()
            if user_role.status == UserRoleStatus.ACTIVE
        )


class AdminUserDetailSerializer(serializers.ModelSerializer):
    """
    Детальная карточка пользователя для административного раздела.
    """

    full_name = serializers.CharField(
        source="get_full_name",
        read_only=True,
    )
    account_managed_by = UserShortSerializer(read_only=True)
    profile = ProfileSerializer(read_only=True)
    user_roles = AdminUserRoleSerializer(many=True, read_only=True)
    audit_logs = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "backup_email",
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
            "email_verified_at",
            "is_phone_verified",
            "phone_verified_at",
            "is_login_allowed",
            "account_managed_by",
            "login_available_from",
            "login_activation_requested_at",
            "login_activated_at",
            "scheduled_for_deletion_at",
            "anonymized_at",
            "created_at",
            "updated_at",
            "profile",
            "user_roles",
            "audit_logs",
        ]
        read_only_fields = fields

    def get_audit_logs(self, obj) -> list[dict]:
        """
        Возвращает последние записи аудита пользователя.

        Args:
            obj:
                Пользователь.

        Returns:
            list[dict]: Последние записи аудита.
        """

        audit_logs = UserAuditLog.objects.select_related(
            "actor",
            "target_user",
        ).filter(target_user=obj,)[:20]

        return UserAuditLogSerializer(
            audit_logs,
            many=True,
            context=self.context,
        ).data


class AdminUserUpdateSerializer(serializers.Serializer):
    """
    Сериализатор редактирования пользователя администратором.

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

        Args:
            attrs:
                Данные serializer'а.

        Returns:
            dict: Проверенные данные.

        Raises:
            ValidationError: Если нет данных для изменения.
        """

        editable_fields = {
            "email",
            "backup_email",
            "phone",
            "first_name",
            "last_name",
            "middle_name",
            "birth_date",
            "is_login_allowed",
            "account_managed_by",
        }

        if not any(field in attrs for field in editable_fields):
            raise serializers.ValidationError(
                "Необходимо передать хотя бы одно поле для изменения."
            )

        return attrs

    def get_service_payload(self) -> dict[str, Any]:
        """
        Возвращает данные для admin_update_user() без служебных полей.

        Returns:
            dict: Данные обновления пользователя.
        """

        service_payload = dict(self.validated_data)
        service_payload.pop("expected_updated_at", None)
        service_payload.pop("reason", None)

        return service_payload


class AdminUserStatusActionSerializer(serializers.Serializer):
    """
    Сериализатор действия над статусом пользователя.

    Используется для:
        - block;
        - unblock;
        - archive;
        - restore.
    """

    reason = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=500,
    )
    expected_updated_at = serializers.DateTimeField(
        required=False,
        write_only=True,
    )


class AdminUserDeleteSerializer(serializers.Serializer):
    """
    Сериализатор планирования удаления пользователя.
    """

    reason = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=500,
    )
    scheduled_for_deletion_at = serializers.DateTimeField(
        required=False,
        allow_null=True,
    )
    expected_updated_at = serializers.DateTimeField(
        required=False,
        write_only=True,
    )


class AdminUserRoleAssignmentSerializer(serializers.Serializer):
    """
    Сериализатор назначения роли пользователю.

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
        Преобразует role_id обратно в ID роли для сервисного слоя.

        Args:
            data:
                Исходные данные.

        Returns:
            dict: Внутреннее представление.
        """

        internal_data = super().to_internal_value(data)

        role = internal_data.pop("role")
        internal_data["role_id"] = role.id

        return internal_data


class AdminUserChangeRolesSerializer(serializers.Serializer):
    """
    Сериализатор изменения ролей пользователя администратором.
    """

    assigned_roles = AdminUserRoleAssignmentSerializer(
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
        Проверяет, что есть хотя бы одно изменение ролей.

        Args:
            attrs:
                Данные serializer'а.

        Returns:
            dict: Проверенные данные.
        """

        assigned_roles = attrs.get("assigned_roles") or []
        revoked_user_role_ids = attrs.get("revoked_user_role_ids") or []

        if not assigned_roles and not revoked_user_role_ids:
            raise serializers.ValidationError(
                "Нужно передать роли для назначения или отзыва."
            )

        return attrs


class AdminUserBulkSerializer(serializers.Serializer):
    """
    Сериализатор массового действия над пользователями.
    """

    action = serializers.ChoiceField(
        choices=[
            (AdminUserBulkAction.BLOCK, "Заблокировать"),
            (AdminUserBulkAction.UNBLOCK, "Разблокировать"),
            (AdminUserBulkAction.ARCHIVE, "Архивировать"),
            (AdminUserBulkAction.RESTORE, "Восстановить"),
            (AdminUserBulkAction.DELETE, "Удалить"),
            (AdminUserBulkAction.CHANGE_ROLES, "Изменить роли"),
        ],
    )
    user_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        allow_empty=False,
    )
    reason = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=500,
    )
    role_payload = serializers.DictField(
        required=False,
    )
    expected_updated_at_by_user_id = serializers.DictField(
        child=serializers.CharField(),
        required=False,
    )

    def validate_user_ids(self, value: list[int]) -> list[int]:
        """
        Нормализует список ID пользователей.

        Args:
            value:
                Список ID пользователей.

        Returns:
            list[int]: Уникальные ID пользователей с сохранением порядка.
        """

        normalized_ids = []
        seen_ids = set()

        for user_id in value:
            if user_id in seen_ids:
                continue

            seen_ids.add(user_id)
            normalized_ids.append(user_id)

        return normalized_ids

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """
        Проверяет совместимость action и role_payload.

        Args:
            attrs:
                Данные serializer'а.

        Returns:
            dict: Проверенные данные.
        """

        action = attrs.get("action")
        role_payload = attrs.get("role_payload") or {}

        if action == AdminUserBulkAction.CHANGE_ROLES:
            assigned_roles = role_payload.get("assigned_roles") or []
            revoked_user_role_ids = role_payload.get("revoked_user_role_ids") or []

            if not assigned_roles and not revoked_user_role_ids:
                raise serializers.ValidationError(
                    {
                        "role_payload": (
                            "Для массового изменения ролей нужно передать "
                            "assigned_roles или revoked_user_role_ids."
                        )
                    }
                )

        if action != AdminUserBulkAction.CHANGE_ROLES and role_payload:
            raise serializers.ValidationError(
                {
                    "role_payload": (
                        "role_payload используется только для действия change_roles."
                    )
                }
            )

        return attrs


class AdminUserBulkItemResultSerializer(serializers.Serializer):
    """
    Сериализатор результата обработки одного пользователя в bulk-операции.
    """

    user_id = serializers.IntegerField()
    success = serializers.BooleanField()
    message = serializers.CharField()
    error_code = serializers.CharField()


class AdminUserBulkResultSerializer(serializers.Serializer):
    """
    Сериализатор результата массового действия.
    """

    bulk_action_id = serializers.CharField()
    action = serializers.CharField()
    total_count = serializers.IntegerField()
    success_count = serializers.IntegerField()
    failed_count = serializers.IntegerField()
    items = AdminUserBulkItemResultSerializer(many=True)


class AdminUserAvailableRoleSerializer(serializers.ModelSerializer):
    """
    Сериализатор доступной роли для админского интерфейса.

    Пригодится для dropdown'а смены ролей на frontend.
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


class AdminUserAuditLogListSerializer(serializers.ModelSerializer):
    """
    Сериализатор истории действий по пользователю в админке.
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
