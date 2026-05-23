from __future__ import annotations

import django_filters
from apps.users.constants.audit import AuditActorType, UserAuditAction
from apps.users.constants.onboarding import RegistrationAttemptStatus
from apps.users.models import RegistrationAttemptLog, UserAuditLog


class UserAuditLogFilter(django_filters.FilterSet):
    """
    Фильтр записей аудита пользователей.
    """

    actor = django_filters.NumberFilter(
        field_name="actor_id",
        label="ID инициатора",
    )
    target_user = django_filters.NumberFilter(
        field_name="target_user_id",
        label="ID целевого пользователя",
    )
    actor_type = django_filters.ChoiceFilter(
        field_name="actor_type",
        choices=AuditActorType.choices,
        label="Тип инициатора",
    )
    action = django_filters.ChoiceFilter(
        field_name="action",
        choices=UserAuditAction.choices,
        label="Действие",
    )
    ip_address = django_filters.CharFilter(
        field_name="ip_address",
        label="IP-адрес",
    )
    created_at_after = django_filters.IsoDateTimeFilter(
        field_name="created_at",
        lookup_expr="gte",
        label="Создано после",
    )
    created_at_before = django_filters.IsoDateTimeFilter(
        field_name="created_at",
        lookup_expr="lte",
        label="Создано до",
    )

    class Meta:
        model = UserAuditLog
        fields = [
            "actor",
            "target_user",
            "actor_type",
            "action",
            "ip_address",
        ]


class RegistrationAttemptLogFilter(django_filters.FilterSet):
    """
    Фильтр попыток регистрации.
    """

    status = django_filters.ChoiceFilter(
        field_name="status",
        choices=RegistrationAttemptStatus.choices,
        label="Статус попытки",
    )
    role_code = django_filters.CharFilter(
        field_name="role_code",
        label="Код роли",
    )
    failure_reason = django_filters.CharFilter(
        field_name="failure_reason",
        label="Причина ошибки",
    )
    ip_address = django_filters.CharFilter(
        field_name="ip_address",
        label="IP-адрес",
    )
    created_at_after = django_filters.IsoDateTimeFilter(
        field_name="created_at",
        lookup_expr="gte",
        label="Создано после",
    )
    created_at_before = django_filters.IsoDateTimeFilter(
        field_name="created_at",
        lookup_expr="lte",
        label="Создано до",
    )

    class Meta:
        model = RegistrationAttemptLog
        fields = [
            "status",
            "role_code",
            "failure_reason",
            "ip_address",
        ]
