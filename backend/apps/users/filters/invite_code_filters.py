from __future__ import annotations

import django_filters
from apps.users.constants.onboarding import InviteCodePurpose
from apps.users.models import InviteCode


class InviteCodeFilter(django_filters.FilterSet):
    """
    Фильтр кодов приглашения.
    """

    purpose = django_filters.ChoiceFilter(
        field_name="purpose",
        choices=InviteCodePurpose.choices,
        label="Назначение кода",
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
    created_by = django_filters.NumberFilter(
        field_name="created_by_id",
        label="ID создателя",
    )
    target_user = django_filters.NumberFilter(
        field_name="target_user_id",
        label="ID целевого пользователя",
    )
    is_active = django_filters.BooleanFilter(
        field_name="is_active",
        label="Активен",
    )
    expires_at_after = django_filters.IsoDateTimeFilter(
        field_name="expires_at",
        lookup_expr="gte",
        label="Истекает после",
    )
    expires_at_before = django_filters.IsoDateTimeFilter(
        field_name="expires_at",
        lookup_expr="lte",
        label="Истекает до",
    )
    available = django_filters.BooleanFilter(
        method="filter_available",
        label="Доступен",
    )

    class Meta:
        model = InviteCode
        fields = [
            "purpose",
            "organization",
            "department",
            "group",
            "created_by",
            "target_user",
            "is_active",
            "available",
        ]

    def filter_available(self, queryset, name, value):
        """
        Фильтрует коды по доступности.

        Args:
            queryset:
                Исходный QuerySet.
            name:
                Имя фильтра.
            value:
                True — только доступные, False — только недоступные.

        Returns:
            QuerySet: Отфильтрованный QuerySet.
        """

        if value is True:
            return queryset.available()

        if value is False:
            available_ids = queryset.available().values_list("id", flat=True)

            return queryset.exclude(id__in=available_ids)

        return queryset
