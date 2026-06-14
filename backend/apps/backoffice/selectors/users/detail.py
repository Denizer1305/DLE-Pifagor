from __future__ import annotations

from apps.backoffice.constants import BackofficeUserMessage
from apps.backoffice.selectors.users.base import get_backoffice_users_queryset_for_actor
from apps.core.selectors import get_object_or_none, get_required_object
from django.db.models import QuerySet


def get_backoffice_user_detail_queryset_for_actor(*, actor) -> QuerySet:
    """
    Возвращает QuerySet для детальной карточки пользователя.
    """

    return get_backoffice_users_queryset_for_actor(actor=actor)


def get_backoffice_user_by_id_for_actor(*, actor, user_id: int):
    """
    Возвращает пользователя по ID с учётом прав администратора.

    Если пользователь не найден или недоступен, возвращает None.
    """

    if not user_id:
        return None

    return get_object_or_none(
        get_backoffice_user_detail_queryset_for_actor(actor=actor),
        id=user_id,
    )


def get_required_backoffice_user_by_id_for_actor(*, actor, user_id: int):
    """
    Возвращает пользователя по ID или выбрасывает Http404.
    """

    return get_required_object(
        get_backoffice_user_detail_queryset_for_actor(actor=actor),
        id=user_id,
        message=BackofficeUserMessage.USER_NOT_FOUND_OR_FORBIDDEN,
    )


def actor_can_access_backoffice_user(*, actor, target_user) -> bool:
    """
    Проверяет, может ли администратор получить доступ к пользователю.
    """

    if not actor or not target_user:
        return False

    return (
        get_backoffice_user_detail_queryset_for_actor(actor=actor)
        .filter(id=target_user.id)
        .exists()
    )


def actor_can_manage_backoffice_user(*, actor, target_user) -> bool:
    """
    Проверяет, может ли администратор управлять пользователем.

    Детальные бизнес-запреты:
    - нельзя менять собственный статус;
    - нельзя удалять самого себя;
    - нельзя менять финальный статус;
    проверяются в service-слое.
    """

    return actor_can_access_backoffice_user(
        actor=actor,
        target_user=target_user,
    )
