from __future__ import annotations

from apps.organizations.models import Subject
from apps.organizations.selectors.access_selectors import (
    actor_has_organization_admin_access,
)
from django.db.models import QuerySet


def get_subjects_base_queryset() -> QuerySet:
    """
    Возвращает базовый QuerySet учебных предметов.

    Returns:
        QuerySet: Учебные предметы.
    """

    return Subject.objects.all().order_by("name")


def get_active_subjects_queryset() -> QuerySet:
    """
    Возвращает активные учебные предметы.

    Returns:
        QuerySet: Активные учебные предметы.
    """

    return get_subjects_base_queryset().filter(
        is_active=True,
    )


def get_subject_by_id(*, subject_id: int | None) -> Subject | None:
    """
    Возвращает учебный предмет по ID.

    Args:
        subject_id:
            ID учебного предмета.

    Returns:
        Subject | None: Учебный предмет или None.
    """

    if not subject_id:
        return None

    return get_subjects_base_queryset().filter(
        id=subject_id,
    ).first()


def get_active_subject_by_id(*, subject_id: int | None) -> Subject | None:
    """
    Возвращает активный учебный предмет по ID.

    Args:
        subject_id:
            ID учебного предмета.

    Returns:
        Subject | None: Активный учебный предмет или None.
    """

    if not subject_id:
        return None

    return get_active_subjects_queryset().filter(
        id=subject_id,
    ).first()


def get_active_subject_by_code(*, code: str) -> Subject | None:
    """
    Возвращает активный учебный предмет по коду.

    Args:
        code:
            Код учебного предмета.

    Returns:
        Subject | None: Активный учебный предмет или None.
    """

    normalized_code = (code or "").strip()

    if not normalized_code:
        return None

    return get_active_subjects_queryset().filter(
        code=normalized_code,
    ).first()


def get_admin_subjects_queryset_for_actor(*, actor) -> QuerySet:
    """
    Возвращает предметы, доступные пользователю в административном разделе.

    Предметы являются глобальным справочником, поэтому администратор
    организации видит весь справочник.

    Args:
        actor:
            Пользователь.

    Returns:
        QuerySet: Доступные учебные предметы.
    """

    if not actor_has_organization_admin_access(actor=actor):
        return Subject.objects.none()

    return get_subjects_base_queryset()


def get_admin_active_subjects_queryset_for_actor(*, actor) -> QuerySet:
    """
    Возвращает активные предметы, доступные пользователю в админке.

    Args:
        actor:
            Пользователь.

    Returns:
        QuerySet: Активные доступные предметы.
    """

    return get_admin_subjects_queryset_for_actor(actor=actor).filter(
        is_active=True,
    )