from __future__ import annotations

import django_filters
from apps.users.constants.lifecycle import UserStatus
from apps.users.models import User


class UserFilter(django_filters.FilterSet):
    """
    Фильтр пользователей.

    Используется в API для поиска и фильтрации пользователей
    по статусу, активности, подтверждению контактов и датам.
    """

    status = django_filters.ChoiceFilter(
        field_name="status",
        choices=UserStatus.choices,
        label="Статус аккаунта",
    )
    is_active = django_filters.BooleanFilter(
        field_name="is_active",
        label="Активен",
    )
    is_staff = django_filters.BooleanFilter(
        field_name="is_staff",
        label="Доступ в админ-панель",
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
            "is_active",
            "is_staff",
            "is_email_verified",
            "is_phone_verified",
            "is_login_allowed",
            "managed_by",
        ]

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
            return queryset.filter(scheduled_for_deletion_at__isnull=False)

        if value is False:
            return queryset.filter(scheduled_for_deletion_at__isnull=True)

        return queryset
