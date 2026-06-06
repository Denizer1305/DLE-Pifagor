from __future__ import annotations

from apps.organizations.models import TeacherOrganization
from apps.organizations.selectors.access_selectors import (
    get_actor_admin_organization_ids,
    is_authenticated_active_actor,
    is_superadmin_actor,
)
from django.db.models import Q, QuerySet
from django.utils import timezone


def get_teacher_organizations_base_queryset() -> QuerySet:
    """
    Возвращает базовый QuerySet связей преподавателей с организациями.

    Returns:
        QuerySet: Связи преподавателей с организациями.
    """

    return (
        TeacherOrganization.objects.select_related(
            "teacher",
            "organization",
        )
        .all()
        .order_by(
            "teacher__last_name",
            "teacher__first_name",
            "-is_primary",
            "organization__name",
        )
    )


def get_active_teacher_organizations_queryset() -> QuerySet:
    """
    Возвращает активные связи преподавателей с активными организациями.

    Returns:
        QuerySet: Активные связи преподавателей с организациями.
    """

    today = timezone.localdate()

    return get_teacher_organizations_base_queryset().filter(
        Q(starts_at__isnull=True) | Q(starts_at__lte=today),
        is_active=True,
        organization__is_active=True,
        teacher__is_active=True,
    )


def get_current_teacher_organizations_queryset() -> QuerySet:
    """
    Возвращает текущие активные связи преподавателей с организациями.

    Учитывает starts_at и ends_at.

    Returns:
        QuerySet: Текущие связи преподавателей с организациями.
    """

    today = timezone.localdate()

    return get_active_teacher_organizations_queryset().filter(
        Q(ends_at__isnull=True) | Q(ends_at__gte=today),
    ).distinct()


def get_teacher_organization_by_id(
    *,
    teacher_organization_id: int | None,
) -> TeacherOrganization | None:
    """
    Возвращает связь преподавателя с организацией по ID.

    Args:
        teacher_organization_id:
            ID связи.

    Returns:
        TeacherOrganization | None: Связь или None.
    """

    if not teacher_organization_id:
        return None

    return get_teacher_organizations_base_queryset().filter(
        id=teacher_organization_id,
    ).first()


def get_current_teacher_organization_by_id(
    *,
    teacher_organization_id: int | None,
) -> TeacherOrganization | None:
    """
    Возвращает текущую связь преподавателя с организацией по ID.

    Args:
        teacher_organization_id:
            ID связи.

    Returns:
        TeacherOrganization | None: Текущая связь или None.
    """

    if not teacher_organization_id:
        return None

    return get_current_teacher_organizations_queryset().filter(
        id=teacher_organization_id,
    ).first()


def get_teacher_organizations_for_teacher(*, teacher) -> QuerySet:
    """
    Возвращает все связи преподавателя с организациями.

    Args:
        teacher:
            Пользователь-преподаватель.

    Returns:
        QuerySet: Связи преподавателя с организациями.
    """

    if teacher is None:
        return TeacherOrganization.objects.none()

    return get_teacher_organizations_base_queryset().filter(
        teacher=teacher,
    )


def get_current_teacher_organizations_for_teacher(*, teacher) -> QuerySet:
    """
    Возвращает текущие связи преподавателя с организациями.

    Args:
        teacher:
            Пользователь-преподаватель.

    Returns:
        QuerySet: Текущие связи преподавателя с организациями.
    """

    if teacher is None:
        return TeacherOrganization.objects.none()

    return get_current_teacher_organizations_queryset().filter(
        teacher=teacher,
    )


def get_primary_teacher_organization(*, teacher) -> TeacherOrganization | None:
    """
    Возвращает основную текущую организацию преподавателя.

    Args:
        teacher:
            Пользователь-преподаватель.

    Returns:
        TeacherOrganization | None: Основная организация или None.
    """

    if teacher is None:
        return None

    return (
        get_current_teacher_organizations_for_teacher(teacher=teacher)
        .filter(is_primary=True)
        .first()
    )


def get_teachers_for_organization(*, organization) -> QuerySet:
    """
    Возвращает текущие связи преподавателей с организацией.

    Args:
        organization:
            Образовательная организация.

    Returns:
        QuerySet: Связи преподавателей с организацией.
    """

    if organization is None:
        return TeacherOrganization.objects.none()

    return get_current_teacher_organizations_queryset().filter(
        organization=organization,
    )


def get_admin_teacher_organizations_queryset_for_actor(*, actor) -> QuerySet:
    """
    Возвращает связи преподавателей с организациями, доступные в админке.

    Правила:
        - суперадминистратор видит все связи;
        - админ организации / директор видит связи своих организаций;
        - остальные пользователи ничего не видят.

    Args:
        actor:
            Пользователь.

    Returns:
        QuerySet: Доступные связи преподавателей с организациями.
    """

    queryset = get_teacher_organizations_base_queryset()

    if not is_authenticated_active_actor(actor=actor):
        return TeacherOrganization.objects.none()

    if is_superadmin_actor(actor=actor):
        return queryset

    organization_ids = get_actor_admin_organization_ids(actor=actor)

    if not organization_ids:
        return TeacherOrganization.objects.none()

    return queryset.filter(
        organization_id__in=organization_ids,
    ).distinct()


def actor_can_access_teacher_organization(
    *,
    actor,
    teacher_organization: TeacherOrganization | None,
) -> bool:
    """
    Проверяет, может ли пользователь видеть связь преподавателя с организацией.

    Args:
        actor:
            Пользователь.
        teacher_organization:
            Связь преподавателя с организацией.

    Returns:
        bool: True, если связь доступна.
    """

    if teacher_organization is None:
        return False

    if is_superadmin_actor(actor=actor):
        return True

    return get_admin_teacher_organizations_queryset_for_actor(actor=actor).filter(
        id=teacher_organization.id,
    ).exists()


def actor_can_manage_teacher_organization(
    *,
    actor,
    teacher_organization: TeacherOrganization | None,
) -> bool:
    """
    Проверяет, может ли пользователь управлять связью преподавателя с организацией.

    Сейчас правила совпадают с административной видимостью.
    Детальная проверка операций будет в service-слое.

    Args:
        actor:
            Пользователь.
        teacher_organization:
            Связь преподавателя с организацией.

    Returns:
        bool: True, если управление разрешено.
    """

    return actor_can_access_teacher_organization(
        actor=actor,
        teacher_organization=teacher_organization,
    )