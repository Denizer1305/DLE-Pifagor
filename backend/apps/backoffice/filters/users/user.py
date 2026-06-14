from __future__ import annotations

import django_filters
from apps.backoffice.constants import BACKOFFICE_USER_ROLE_GROUP_CHOICES
from apps.backoffice.filters.users.helpers import (
    filter_users_by_role_group,
    filter_users_by_scheduled_for_deletion,
)
from apps.core.filters import (
    CreatedAtRangeFilterMixin,
    IsActiveFilterMixin,
    UpdatedAtRangeFilterMixin,
)
from apps.users.constants.lifecycle import UserRoleStatus, UserStatus
from apps.users.constants.roles import RoleCode
from apps.users.models import User


class BackofficeUserFilter(
    CreatedAtRangeFilterMixin,
    UpdatedAtRangeFilterMixin,
    IsActiveFilterMixin,
    django_filters.FilterSet,
):
    """
    Фильтр административного списка пользователей.

    Фильтр отвечает только за параметры поиска и фильтрации.
    Права доступа и область видимости пользователей задаются в selectors.
    """

    status = django_filters.ChoiceFilter(
        field_name="status",
        choices=UserStatus.choices,
        label="Статус пользователя",
    )
    role_group = django_filters.ChoiceFilter(
        method="filter_role_group",
        choices=BACKOFFICE_USER_ROLE_GROUP_CHOICES,
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
        fields = (
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
            "scheduled_for_deletion",
            "created_at_after",
            "created_at_before",
            "updated_at_after",
            "updated_at_before",
        )

    def filter_role_group(self, queryset, name, value):
        """
        Фильтрует пользователей по административной группе ролей.
        """

        return filter_users_by_role_group(
            queryset=queryset,
            role_group=value,
        )

    def filter_scheduled_for_deletion(self, queryset, name, value):
        """
        Фильтрует пользователей по признаку запланированного удаления.
        """

        return filter_users_by_scheduled_for_deletion(
            queryset=queryset,
            value=value,
        )
