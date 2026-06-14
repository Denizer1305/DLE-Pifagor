from __future__ import annotations

from apps.backoffice.constants import BACKOFFICE_USER_ROLE_GROUPS
from apps.users.constants.lifecycle import UserRoleStatus
from django.db.models import QuerySet


def filter_users_by_role_group(
    *,
    queryset: QuerySet,
    role_group: str,
) -> QuerySet:
    """
    Фильтрует пользователей по административной группе ролей.

    Группы ролей живут в backoffice, потому что это не доменная роль,
    а удобная группировка для административного интерфейса:
    - учащиеся;
    - преподаватели и сотрудники;
    - родители.
    """

    role_codes = BACKOFFICE_USER_ROLE_GROUPS.get(role_group)

    if not role_codes:
        return queryset

    return queryset.filter(
        user_roles__role__code__in=role_codes,
        user_roles__status=UserRoleStatus.ACTIVE,
    ).distinct()


def filter_users_by_scheduled_for_deletion(
    *,
    queryset: QuerySet,
    value: bool | None,
) -> QuerySet:
    """
    Фильтрует пользователей по признаку запланированного удаления.
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
