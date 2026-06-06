from __future__ import annotations

from apps.organizations.models import GroupCurator, StudyGroup
from apps.organizations.selectors.access_selectors import (
    is_authenticated_active_actor,
)
from apps.organizations.selectors.study_group_selectors import (
    get_admin_study_groups_queryset_for_actor,
)
from django.db.models import Q, QuerySet
from django.utils import timezone


def get_group_curators_base_queryset() -> QuerySet:
    """
    Возвращает базовый QuerySet кураторов групп.

    Returns:
        QuerySet: Кураторы групп.
    """

    return (
        GroupCurator.objects.select_related(
            "group",
            "group__organization",
            "group__department",
            "teacher",
        )
        .all()
        .order_by(
            "group__organization__name",
            "group__name",
            "-is_primary",
            "teacher__last_name",
            "teacher__first_name",
        )
    )


def get_active_group_curators_queryset() -> QuerySet:
    """
    Возвращает активные связи кураторов с активными группами.

    Returns:
        QuerySet: Активные кураторы групп.
    """

    today = timezone.localdate()

    return get_group_curators_base_queryset().filter(
        Q(starts_at__isnull=True) | Q(starts_at__lte=today),
        is_active=True,
        group__is_active=True,
        group__organization__is_active=True,
    )


def get_current_group_curators_queryset() -> QuerySet:
    """
    Возвращает текущие активные связи кураторов.

    Учитывает starts_at и ends_at.

    Returns:
        QuerySet: Текущие кураторы групп.
    """

    today = timezone.localdate()

    return get_active_group_curators_queryset().filter(
        Q(ends_at__isnull=True) | Q(ends_at__gte=today),
    ).distinct()


def get_curators_for_group(*, group) -> QuerySet:
    """
    Возвращает текущих кураторов учебной группы.

    Args:
        group:
            Учебная группа.

    Returns:
        QuerySet: Кураторы группы.
    """

    if group is None:
        return GroupCurator.objects.none()

    return get_current_group_curators_queryset().filter(
        group=group,
    )


def get_primary_curator_for_group(*, group) -> GroupCurator | None:
    """
    Возвращает основного текущего куратора группы.

    Args:
        group:
            Учебная группа.

    Returns:
        GroupCurator | None: Основной куратор или None.
    """

    if group is None:
        return None

    return (
        get_curators_for_group(group=group)
        .filter(is_primary=True)
        .first()
    )


def get_group_curator_by_id(
    *,
    group_curator_id: int | None,
) -> GroupCurator | None:
    """
    Возвращает связь куратора группы по ID.

    Args:
        group_curator_id:
            ID связи куратора группы.

    Returns:
        GroupCurator | None: Связь или None.
    """

    if not group_curator_id:
        return None

    return get_group_curators_base_queryset().filter(
        id=group_curator_id,
    ).first()


def get_current_group_curator_by_id(
    *,
    group_curator_id: int | None,
) -> GroupCurator | None:
    """
    Возвращает текущую активную связь куратора группы по ID.

    Args:
        group_curator_id:
            ID связи куратора группы.

    Returns:
        GroupCurator | None: Текущая связь или None.
    """

    if not group_curator_id:
        return None

    return get_current_group_curators_queryset().filter(
        id=group_curator_id,
    ).first()


def get_curated_groups_queryset_for_actor(*, actor) -> QuerySet:
    """
    Возвращает группы, которые курирует пользователь.

    Args:
        actor:
            Пользователь.

    Returns:
        QuerySet: Курируемые группы.
    """

    if not is_authenticated_active_actor(actor=actor):
        return StudyGroup.objects.none()

    group_ids = (
        get_current_group_curators_queryset()
        .filter(teacher=actor)
        .values_list("group_id", flat=True)
        .distinct()
    )

    return (
        StudyGroup.objects.select_related(
            "organization",
            "department",
        )
        .filter(
            id__in=group_ids,
        )
        .order_by(
            "organization__name",
            "department__name",
            "name",
        )
    )


def get_curated_group_ids_for_actor(*, actor) -> list[int]:
    """
    Возвращает ID групп, которые курирует пользователь.

    Args:
        actor:
            Пользователь.

    Returns:
        list[int]: ID курируемых групп.
    """

    if not is_authenticated_active_actor(actor=actor):
        return []

    return list(
        get_current_group_curators_queryset()
        .filter(teacher=actor)
        .values_list("group_id", flat=True)
        .distinct()
    )


def actor_is_group_curator(*, actor, group) -> bool:
    """
    Проверяет, является ли пользователь текущим куратором группы.

    Args:
        actor:
            Пользователь.
        group:
            Учебная группа.

    Returns:
        bool: True, если пользователь является куратором группы.
    """

    if not is_authenticated_active_actor(actor=actor):
        return False

    if group is None:
        return False

    return get_current_group_curators_queryset().filter(
        teacher=actor,
        group=group,
    ).exists()


def actor_is_primary_group_curator(*, actor, group) -> bool:
    """
    Проверяет, является ли пользователь основным куратором группы.

    Args:
        actor:
            Пользователь.
        group:
            Учебная группа.

    Returns:
        bool: True, если пользователь является основным куратором.
    """

    if not is_authenticated_active_actor(actor=actor):
        return False

    if group is None:
        return False

    return get_current_group_curators_queryset().filter(
        teacher=actor,
        group=group,
        is_primary=True,
    ).exists()


def get_admin_group_curators_queryset_for_actor(*, actor) -> QuerySet:
    """
    Возвращает кураторов групп, доступных пользователю в админке.

    Args:
        actor:
            Пользователь.

    Returns:
        QuerySet: Доступные кураторы групп.
    """

    group_ids = (
        get_admin_study_groups_queryset_for_actor(actor=actor)
        .values_list("id", flat=True)
        .distinct()
    )

    return get_group_curators_base_queryset().filter(
        group_id__in=group_ids,
    )