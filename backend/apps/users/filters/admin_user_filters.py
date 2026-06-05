from __future__ import annotations

import django_filters
from apps.users.constants.lifecycle import UserRoleStatus, UserStatus
from apps.users.constants.roles import RoleCode
from apps.users.models import User
from apps.users.selectors.admin_user_selectors import (
    ADMIN_USER_ROLE_GROUPS,
    filter_admin_users_by_role_group,
)


class AdminUserFilter(django_filters.FilterSet):
    """
    Фильтр административного списка пользователей.

    Используется для страниц:
        - все пользователи;
        - учащиеся;
        - преподаватели;
        - родители.

    Важно:
        Фильтр не отвечает за права доступа.
        Права и область видимости пользователей задаются в selector'ах.
    """

    status = django_filters.ChoiceFilter(
        field_name="status",
        choices=UserStatus.choices,
        label="Статус пользователя",
    )
    role_group = django_filters.ChoiceFilter(
        method="filter_role_group",
        choices=[
            ("students", "Учащиеся"),
            ("teachers", "Преподаватели и сотрудники"),
            ("parents", "Родители"),
        ],
        label="Группа ролей",
    )
    role_code = django_filters.ChoiceFilter(
        field_name="user_roles__role__code",
        choices=RoleCode.choices,
        label="Код роли",
    )
    role_status = django_filters.ChoiceFilter(
        field_name="user_roles__status",
        choices=UserRoleStatus.choices,
        label="Статус роли",
    )
    organization = django_filters.NumberFilter(
        field_name="user_roles__organization_id",
        label="ID организации",
    )
    department = django_filters.NumberFilter(
        field_name="user_roles__department_id",
        label="ID отделения",
    )
    group = django_filters.NumberFilter(
        field_name="user_roles__group_id",
        label="ID группы",
    )
    is_active = django_filters.BooleanFilter(
        field_name="is_active",
        label="Активен",
    )
    is_staff = django_filters.BooleanFilter(
        field_name="is_staff",
        label="Есть доступ в Django admin",
    )
    is_superuser = django_filters.BooleanFilter(
        field_name="is_superuser",
        label="Django superuser",
    )
    is_email_verified = django_filters.BooleanFilter(
        field_name="is_email_verified",
        label="Email подтверждён",
    )
    is_phone_verified = django_filters.BooleanFilter(
        field_name="is_phone_verified",
        label="Телефон подтверждён",
    )
    is_login_allowed = django_filters.BooleanFilter(
        field_name="is_login_allowed",
        label="Самостоятельный вход разрешён",
    )
    created_at_after = django_filters.IsoDateTimeFilter(
        field_name="created_at",
        lookup_expr="gte",
        label="Создан после",
    )
    created_at_before = django_filters.IsoDateTimeFilter(
        field_name="created_at",
        lookup_expr="lte",
        label="Создан до",
    )
    updated_at_after = django_filters.IsoDateTimeFilter(
        field_name="updated_at",
        lookup_expr="gte",
        label="Обновлён после",
    )
    updated_at_before = django_filters.IsoDateTimeFilter(
        field_name="updated_at",
        lookup_expr="lte",
        label="Обновлён до",
    )
    scheduled_for_deletion = django_filters.BooleanFilter(
        method="filter_scheduled_for_deletion",
        label="Запланирован к удалению",
    )
    managed_by = django_filters.NumberFilter(
        field_name="account_managed_by_id",
        label="ID управляющего пользователя",
    )

    class Meta:
        model = User
        fields = [
            "status",
            "role_group",
            "role_code",
            "role_status",
            "organization",
            "department",
            "group",
            "is_active",
            "is_staff",
            "is_superuser",
            "is_email_verified",
            "is_phone_verified",
            "is_login_allowed",
            "managed_by",
        ]

    def filter_role_group(self, queryset, name, value):
        """
        Фильтрует пользователей по группе ролей.

        Args:
            queryset:
                Исходный QuerySet.
            name:
                Имя фильтра.
            value:
                Код группы ролей.

        Returns:
            QuerySet: Отфильтрованный QuerySet.
        """

        if value not in ADMIN_USER_ROLE_GROUPS:
            return queryset

        return filter_admin_users_by_role_group(
            queryset=queryset,
            role_group=value,
        )

    def filter_scheduled_for_deletion(self, queryset, name, value):
        """
        Фильтрует пользователей по признаку запланированного удаления.

        Args:
            queryset:
                Исходный QuerySet.
            name:
                Имя фильтра.
            value:
                True — только запланированные к удалению,
                False — только не запланированные.

        Returns:
            QuerySet: Отфильтрованный QuerySet.
        """

        if value is True:
            return queryset.filter(
                scheduled_for_deletion_at__isnull=False,
            )

        if value is False:
            return queryset.filter(
                scheduled_for_deletion_at__isnull=True,
            )

        return queryset
