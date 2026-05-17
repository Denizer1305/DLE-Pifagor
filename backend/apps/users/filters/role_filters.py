from __future__ import annotations

import django_filters
from apps.users.constants.lifecycle import UserRoleStatus
from apps.users.constants.roles import RoleCode
from apps.users.models import Role, UserRole


class RoleFilter(django_filters.FilterSet):
    """
    Фильтр справочника ролей.
    """

    code = django_filters.ChoiceFilter(
        field_name="code",
        choices=RoleCode.choices,
        label="Код роли",
    )
    is_system = django_filters.BooleanFilter(
        field_name="is_system",
        label="Системная роль",
    )
    is_active = django_filters.BooleanFilter(
        field_name="is_active",
        label="Активна",
    )

    class Meta:
        model = Role
        fields = [
            "code",
            "is_system",
            "is_active",
        ]


class UserRoleFilter(django_filters.FilterSet):
    """
    Фильтр назначенных ролей пользователей.

    Позволяет фильтровать роли по пользователю, роли,
    организации, отделению, группе и статусу.
    """

    user = django_filters.NumberFilter(
        field_name="user_id",
        label="ID пользователя",
    )
    role = django_filters.NumberFilter(
        field_name="role_id",
        label="ID роли",
    )
    role_code = django_filters.ChoiceFilter(
        field_name="role__code",
        choices=RoleCode.choices,
        label="Код роли",
    )
    status = django_filters.ChoiceFilter(
        field_name="status",
        choices=UserRoleStatus.choices,
        label="Статус роли",
    )
    organization = django_filters.NumberFilter(
        field_name="organization_id",
        label="ID организации",
    )
    department = django_filters.NumberFilter(
        field_name="department_id",
        label="ID отделения",
    )
    group = django_filters.NumberFilter(
        field_name="group_id",
        label="ID группы",
    )
    assigned_at_after = django_filters.IsoDateTimeFilter(
        field_name="assigned_at",
        lookup_expr="gte",
        label="Назначена после",
    )
    assigned_at_before = django_filters.IsoDateTimeFilter(
        field_name="assigned_at",
        lookup_expr="lte",
        label="Назначена до",
    )

    class Meta:
        model = UserRole
        fields = [
            "user",
            "role",
            "role_code",
            "status",
            "organization",
            "department",
            "group",
        ]
