from __future__ import annotations

from apps.organizations.models import Department
from apps.organizations.selectors.access_selectors import (
    get_actor_admin_department_ids,
    get_actor_admin_organization_ids,
    is_authenticated_active_actor,
    is_superadmin_actor,
)
from django.db.models import Q


def get_departments_base_queryset() -> Q:
    """
    Возвращает базовый QuerySet отделений.

    Returns:
        QuerySet: Отделения.
    """

    return (
        Department.objects.select_related(
            "organization",
        )
        .all()
        .order_by(
            "organization__name",
            "name",
        )
    )


def get_active_departments_queryset() -> Q:
    """
    Возвращает активные отделения активных организаций.

    Returns:
        QuerySet: Активные отделения.
    """

    return get_departments_base_queryset().filter(
        is_active=True,
        organization__is_active=True,
    )


def get_departments_for_organization(*, organization) -> Q:
    """
    Возвращает активные отделения организации.

    Args:
        organization:
            Образовательная организация.

    Returns:
        QuerySet: Активные отделения организации.
    """

    if organization is None:
        return Department.objects.none()

    return get_active_departments_queryset().filter(
        organization=organization,
    )


def get_department_by_id(*, department_id: int | None) -> Department | None:
    """
    Возвращает отделение по ID.

    Args:
        department_id:
            ID отделения.

    Returns:
        Department | None: Отделение или None.
    """

    if not department_id:
        return None

    return get_departments_base_queryset().filter(
        id=department_id,
    ).first()


def get_active_department_by_id(
    *,
    department_id: int | None,
) -> Department | None:
    """
    Возвращает активное отделение по ID.

    Args:
        department_id:
            ID отделения.

    Returns:
        Department | None: Активное отделение или None.
    """

    if not department_id:
        return None

    return get_active_departments_queryset().filter(
        id=department_id,
    ).first()


def get_admin_departments_queryset_for_actor(*, actor) -> Q:
    """
    Возвращает отделения, доступные пользователю в административном разделе.

    Правила:
        - суперадминистратор видит все отделения;
        - администратор организации / директор видит отделения своих организаций;
        - заведующий отделением видит только свои отделения;
        - обычный пользователь ничего не видит.

    Args:
        actor:
            Пользователь, который выполняет административное действие.

    Returns:
        QuerySet: Доступные отделения.
    """

    queryset = get_departments_base_queryset()

    if not is_authenticated_active_actor(actor=actor):
        return Department.objects.none()

    if is_superadmin_actor(actor=actor):
        return queryset

    organization_ids = get_actor_admin_organization_ids(actor=actor)
    department_ids = get_actor_admin_department_ids(actor=actor)

    if not organization_ids and not department_ids:
        return Department.objects.none()

    scope_query = Q()

    if organization_ids:
        scope_query |= Q(organization_id__in=organization_ids)

    if department_ids:
        scope_query |= Q(id__in=department_ids)

    return queryset.filter(scope_query).distinct()


def get_admin_active_departments_queryset_for_actor(*, actor) -> Q:
    """
    Возвращает активные отделения, доступные пользователю в админке.

    Args:
        actor:
            Пользователь.

    Returns:
        QuerySet: Активные доступные отделения.
    """

    return get_admin_departments_queryset_for_actor(actor=actor).filter(
        is_active=True,
        organization__is_active=True,
    ).distinct()


def actor_can_access_department(*, actor, department: Department | None) -> bool:
    """
    Проверяет, может ли пользователь видеть отделение.

    Args:
        actor:
            Пользователь.
        department:
            Отделение.

    Returns:
        bool: True, если отделение доступно.
    """

    if department is None:
        return False

    if is_superadmin_actor(actor=actor):
        return True

    return get_admin_departments_queryset_for_actor(actor=actor).filter(
        id=department.id,
    ).exists()


def actor_can_manage_department(*, actor, department: Department | None) -> bool:
    """
    Проверяет, может ли пользователь управлять отделением.

    Сейчас правила совпадают с административной видимостью.
    Детальные ограничения операций будут в service-слое.

    Args:
        actor:
            Пользователь.
        department:
            Отделение.

    Returns:
        bool: True, если управление разрешено.
    """

    return actor_can_access_department(
        actor=actor,
        department=department,
    )