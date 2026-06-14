from __future__ import annotations

from apps.core.selectors import get_object_or_none, get_required_object
from apps.users.constants.lifecycle import UserRoleStatus
from apps.users.models import Role, UserRole
from django.db.models import QuerySet


def get_backoffice_roles_queryset() -> QuerySet:
    """
    Возвращает роли, доступные в административном контуре.
    """

    return Role.objects.filter(
        is_active=True,
    ).order_by(
        "sort_order",
        "label",
    )


def get_backoffice_role_by_code(*, role_code: str):
    """
    Возвращает активную роль по коду или None.
    """

    if not role_code:
        return None

    return get_object_or_none(
        get_backoffice_roles_queryset(),
        code=role_code,
    )


def get_required_backoffice_role_by_code(*, role_code: str):
    """
    Возвращает активную роль по коду или выбрасывает Http404.
    """

    return get_required_object(
        get_backoffice_roles_queryset(),
        code=role_code,
    )


def get_backoffice_user_roles_queryset(*, user_id: int | None = None) -> QuerySet:
    """
    Возвращает назначенные роли пользователей для backoffice.
    """

    queryset = UserRole.objects.select_related(
        "user",
        "role",
        "organization",
        "department",
        "group",
        "assigned_by",
        "revoked_by",
    ).order_by(
        "role__sort_order",
        "role__label",
    )

    if user_id is not None:
        queryset = queryset.filter(user_id=user_id)

    return queryset


def get_backoffice_active_user_roles_queryset(
    *,
    user_id: int | None = None,
) -> QuerySet:
    """
    Возвращает активные назначенные роли пользователей.
    """

    return get_backoffice_user_roles_queryset(
        user_id=user_id,
    ).filter(
        status=UserRoleStatus.ACTIVE,
    )


def get_backoffice_user_role_by_id(*, user_role_id: int):
    """
    Возвращает назначенную роль пользователя по ID или None.
    """

    if not user_role_id:
        return None

    return get_object_or_none(
        get_backoffice_user_roles_queryset(),
        id=user_role_id,
    )
