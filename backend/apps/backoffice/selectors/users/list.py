from __future__ import annotations

from apps.backoffice.filters.users.helpers import filter_users_by_role_group
from apps.backoffice.selectors.users.base import get_backoffice_users_queryset_for_actor
from django.db.models import QuerySet


def get_backoffice_users_list_queryset(*, actor) -> QuerySet:
    """
    Возвращает список пользователей, доступных администратору.

    Фильтры поиска и query params применяются уже на уровне FilterSet.
    """

    return get_backoffice_users_queryset_for_actor(actor=actor)


def get_backoffice_students_queryset_for_actor(*, actor) -> QuerySet:
    """
    Возвращает учащихся, доступных администратору.
    """

    return filter_users_by_role_group(
        queryset=get_backoffice_users_queryset_for_actor(actor=actor),
        role_group="students",
    )


def get_backoffice_teachers_queryset_for_actor(*, actor) -> QuerySet:
    """
    Возвращает преподавателей и сотрудников, доступных администратору.
    """

    return filter_users_by_role_group(
        queryset=get_backoffice_users_queryset_for_actor(actor=actor),
        role_group="teachers",
    )


def get_backoffice_parents_queryset_for_actor(*, actor) -> QuerySet:
    """
    Возвращает родителей, доступных администратору.
    """

    return filter_users_by_role_group(
        queryset=get_backoffice_users_queryset_for_actor(actor=actor),
        role_group="parents",
    )
