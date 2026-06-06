from __future__ import annotations

from apps.organizations.models import StudyGroup
from apps.organizations.selectors.access_selectors import (
    get_actor_admin_department_ids,
    get_actor_admin_organization_ids,
    get_actor_group_ids,
    is_authenticated_active_actor,
    is_superadmin_actor,
)
from django.db.models import Q, QuerySet


def get_study_groups_base_queryset() -> QuerySet:
    """
    Возвращает базовый QuerySet учебных групп.

    Returns:
        QuerySet: Учебные группы.
    """

    return (
        StudyGroup.objects.select_related(
            "organization",
            "department",
        )
        .all()
        .order_by(
            "organization__name",
            "department__name",
            "name",
        )
    )


def get_active_study_groups_queryset() -> QuerySet:
    """
    Возвращает активные учебные группы активных организаций.

    Returns:
        QuerySet: Активные учебные группы.
    """

    return get_study_groups_base_queryset().filter(
        is_active=True,
        organization__is_active=True,
    )


def get_study_groups_for_organization(*, organization) -> QuerySet:
    """
    Возвращает активные группы организации.

    Args:
        organization:
            Образовательная организация.

    Returns:
        QuerySet: Активные группы организации.
    """

    if organization is None:
        return StudyGroup.objects.none()

    return get_active_study_groups_queryset().filter(
        organization=organization,
    )


def get_study_groups_for_department(*, department) -> QuerySet:
    """
    Возвращает активные группы отделения.

    Args:
        department:
            Отделение.

    Returns:
        QuerySet: Активные группы отделения.
    """

    if department is None:
        return StudyGroup.objects.none()

    return get_active_study_groups_queryset().filter(
        department=department,
    )


def get_study_group_by_id(*, group_id: int | None) -> StudyGroup | None:
    """
    Возвращает учебную группу по ID.

    Args:
        group_id:
            ID учебной группы.

    Returns:
        StudyGroup | None: Учебная группа или None.
    """

    if not group_id:
        return None

    return get_study_groups_base_queryset().filter(
        id=group_id,
    ).first()


def get_active_study_group_by_id(
    *,
    group_id: int | None,
) -> StudyGroup | None:
    """
    Возвращает активную учебную группу по ID.

    Args:
        group_id:
            ID учебной группы.

    Returns:
        StudyGroup | None: Активная учебная группа или None.
    """

    if not group_id:
        return None

    return get_active_study_groups_queryset().filter(
        id=group_id,
    ).first()


def get_admin_study_groups_queryset_for_actor(*, actor) -> QuerySet:
    """
    Возвращает учебные группы, доступные пользователю в админке.

    Правила:
        - суперадминистратор видит все группы;
        - администратор организации / директор видит группы своих организаций;
        - заведующий отделением видит группы своих отделений;
        - куратор видит свои группы;
        - обычный пользователь ничего не видит.

    Args:
        actor:
            Пользователь, который выполняет административное действие.

    Returns:
        QuerySet: Доступные учебные группы.
    """

    queryset = get_study_groups_base_queryset()

    if not is_authenticated_active_actor(actor=actor):
        return StudyGroup.objects.none()

    if is_superadmin_actor(actor=actor):
        return queryset

    organization_ids = get_actor_admin_organization_ids(actor=actor)
    department_ids = get_actor_admin_department_ids(actor=actor)
    group_ids = get_actor_group_ids(actor=actor)

    scope_query = Q()

    if organization_ids:
        scope_query |= Q(organization_id__in=organization_ids)

    if department_ids:
        scope_query |= Q(department_id__in=department_ids)

    if group_ids:
        scope_query |= Q(id__in=group_ids)

    if not scope_query:
        return StudyGroup.objects.none()

    return queryset.filter(scope_query).distinct()


def get_admin_active_study_groups_queryset_for_actor(*, actor) -> QuerySet:
    """
    Возвращает активные группы, доступные пользователю в админке.

    Args:
        actor:
            Пользователь.

    Returns:
        QuerySet: Активные доступные группы.
    """

    return get_admin_study_groups_queryset_for_actor(actor=actor).filter(
        is_active=True,
        organization__is_active=True,
    ).distinct()


def get_admin_study_groups_for_organization(
    *,
    actor,
    organization,
) -> QuerySet:
    """
    Возвращает доступные администратору группы конкретной организации.

    Args:
        actor:
            Пользователь.
        organization:
            Организация.

    Returns:
        QuerySet: Доступные группы организации.
    """

    if organization is None:
        return StudyGroup.objects.none()

    return get_admin_study_groups_queryset_for_actor(actor=actor).filter(
        organization=organization,
    )


def get_admin_study_groups_for_department(
    *,
    actor,
    department,
) -> QuerySet:
    """
    Возвращает доступные администратору группы конкретного отделения.

    Args:
        actor:
            Пользователь.
        department:
            Отделение.

    Returns:
        QuerySet: Доступные группы отделения.
    """

    if department is None:
        return StudyGroup.objects.none()

    return get_admin_study_groups_queryset_for_actor(actor=actor).filter(
        department=department,
    )


def actor_can_access_study_group(*, actor, group: StudyGroup | None) -> bool:
    """
    Проверяет, может ли пользователь видеть учебную группу.

    Args:
        actor:
            Пользователь.
        group:
            Учебная группа.

    Returns:
        bool: True, если группа доступна.
    """

    if group is None:
        return False

    if is_superadmin_actor(actor=actor):
        return True

    return get_admin_study_groups_queryset_for_actor(actor=actor).filter(
        id=group.id,
    ).exists()


def actor_can_manage_study_group(*, actor, group: StudyGroup | None) -> bool:
    """
    Проверяет, может ли пользователь управлять учебной группой.

    Сейчас правила совпадают с административной видимостью.
    Более тонкие ограничения будут в service-слое.

    Args:
        actor:
            Пользователь.
        group:
            Учебная группа.

    Returns:
        bool: True, если управление разрешено.
    """

    return actor_can_access_study_group(
        actor=actor,
        group=group,
    )