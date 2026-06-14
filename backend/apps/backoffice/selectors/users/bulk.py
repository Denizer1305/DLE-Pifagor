from __future__ import annotations

from apps.backoffice.selectors.users.base import get_backoffice_users_queryset_for_actor
from apps.users.models import User
from django.db.models import QuerySet


def get_backoffice_users_for_bulk_action(
    *,
    actor,
    user_ids: list[int] | tuple[int, ...] | set[int],
) -> QuerySet:
    """
    Возвращает пользователей для bulk-операции с учётом прав администратора.
    """

    if not user_ids:
        return User.objects.none()

    return get_backoffice_users_queryset_for_actor(
        actor=actor,
    ).filter(
        id__in=user_ids,
    )


def get_accessible_backoffice_user_ids_for_bulk_action(
    *,
    actor,
    user_ids: list[int] | tuple[int, ...] | set[int],
) -> set[int]:
    """
    Возвращает ID пользователей, доступных для bulk-операции.
    """

    return set(
        get_backoffice_users_for_bulk_action(
            actor=actor,
            user_ids=user_ids,
        ).values_list(
            "id",
            flat=True,
        )
    )


def actor_can_access_all_backoffice_users_for_bulk_action(
    *,
    actor,
    user_ids: list[int] | tuple[int, ...] | set[int],
) -> bool:
    """
    Проверяет, что администратору доступны все выбранные пользователи.
    """

    requested_ids = set(user_ids)

    if not requested_ids:
        return False

    accessible_ids = get_accessible_backoffice_user_ids_for_bulk_action(
        actor=actor,
        user_ids=requested_ids,
    )

    return requested_ids == accessible_ids
