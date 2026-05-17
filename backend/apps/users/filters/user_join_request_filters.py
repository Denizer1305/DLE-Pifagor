from __future__ import annotations

import django_filters
from apps.users.constants.onboarding import JoinRequestStatus, JoinRequestType
from apps.users.models import UserJoinRequest


class UserJoinRequestFilter(django_filters.FilterSet):
    """
    Фильтр заявок пользователей.
    """

    request_type = django_filters.ChoiceFilter(
        field_name="request_type",
        choices=JoinRequestType.choices,
        label="Тип заявки",
    )
    status = django_filters.ChoiceFilter(
        field_name="status",
        choices=JoinRequestStatus.choices,
        label="Статус заявки",
    )
    user = django_filters.NumberFilter(
        field_name="user_id",
        label="ID пользователя",
    )
    target_user = django_filters.NumberFilter(
        field_name="target_user_id",
        label="ID целевого пользователя",
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
    reviewed_by = django_filters.NumberFilter(
        field_name="reviewed_by_id",
        label="ID проверяющего",
    )
    created_at_after = django_filters.IsoDateTimeFilter(
        field_name="created_at",
        lookup_expr="gte",
        label="Создана после",
    )
    created_at_before = django_filters.IsoDateTimeFilter(
        field_name="created_at",
        lookup_expr="lte",
        label="Создана до",
    )
    reviewed_at_after = django_filters.IsoDateTimeFilter(
        field_name="reviewed_at",
        lookup_expr="gte",
        label="Проверена после",
    )
    reviewed_at_before = django_filters.IsoDateTimeFilter(
        field_name="reviewed_at",
        lookup_expr="lte",
        label="Проверена до",
    )

    class Meta:
        model = UserJoinRequest
        fields = [
            "request_type",
            "status",
            "user",
            "target_user",
            "organization",
            "department",
            "group",
            "reviewed_by",
        ]
