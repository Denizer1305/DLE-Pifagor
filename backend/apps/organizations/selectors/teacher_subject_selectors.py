from __future__ import annotations

from apps.organizations.models import TeacherSubject
from apps.organizations.selectors.access_selectors import (
    get_actor_admin_organization_ids,
    is_authenticated_active_actor,
    is_superadmin_actor,
)
from django.db.models import Q, QuerySet


def get_teacher_subjects_base_queryset() -> QuerySet:
    """
    Возвращает базовый QuerySet предметов преподавателей.

    Returns:
        QuerySet: Связи преподавателей с предметами.
    """

    return (
        TeacherSubject.objects.select_related(
            "teacher",
            "subject",
        )
        .all()
        .order_by(
            "teacher__last_name",
            "teacher__first_name",
            "-is_primary",
            "subject__name",
        )
    )


def get_active_teacher_subjects_queryset() -> QuerySet:
    """
    Возвращает активные связи преподавателей с активными предметами.

    Returns:
        QuerySet: Активные предметы преподавателей.
    """

    return get_teacher_subjects_base_queryset().filter(
        is_active=True,
        subject__is_active=True,
        teacher__is_active=True,
    )


def get_teacher_subject_by_id(
    *,
    teacher_subject_id: int | None,
) -> TeacherSubject | None:
    """
    Возвращает предмет преподавателя по ID.

    Args:
        teacher_subject_id:
            ID связи преподавателя с предметом.

    Returns:
        TeacherSubject | None: Связь или None.
    """

    if not teacher_subject_id:
        return None

    return (
        get_teacher_subjects_base_queryset()
        .filter(
            id=teacher_subject_id,
        )
        .first()
    )


def get_active_teacher_subject_by_id(
    *,
    teacher_subject_id: int | None,
) -> TeacherSubject | None:
    """
    Возвращает активный предмет преподавателя по ID.

    Args:
        teacher_subject_id:
            ID связи преподавателя с предметом.

    Returns:
        TeacherSubject | None: Активная связь или None.
    """

    if not teacher_subject_id:
        return None

    return (
        get_active_teacher_subjects_queryset()
        .filter(
            id=teacher_subject_id,
        )
        .first()
    )


def get_teacher_subjects_for_teacher(*, teacher) -> QuerySet:
    """
    Возвращает все предметы преподавателя.

    Args:
        teacher:
            Пользователь-преподаватель.

    Returns:
        QuerySet: Предметы преподавателя.
    """

    if teacher is None:
        return TeacherSubject.objects.none()

    return get_teacher_subjects_base_queryset().filter(
        teacher=teacher,
    )


def get_active_teacher_subjects_for_teacher(*, teacher) -> QuerySet:
    """
    Возвращает активные предметы преподавателя.

    Args:
        teacher:
            Пользователь-преподаватель.

    Returns:
        QuerySet: Активные предметы преподавателя.
    """

    if teacher is None:
        return TeacherSubject.objects.none()

    return get_active_teacher_subjects_queryset().filter(
        teacher=teacher,
    )


def get_primary_teacher_subject(*, teacher) -> TeacherSubject | None:
    """
    Возвращает основной активный предмет преподавателя.

    Args:
        teacher:
            Пользователь-преподаватель.

    Returns:
        TeacherSubject | None: Основной предмет или None.
    """

    if teacher is None:
        return None

    return (
        get_active_teacher_subjects_for_teacher(teacher=teacher)
        .filter(is_primary=True)
        .first()
    )


def get_teacher_subjects_for_subject(*, subject) -> QuerySet:
    """
    Возвращает связи преподавателей с конкретным предметом.

    Args:
        subject:
            Учебный предмет.

    Returns:
        QuerySet: Связи преподавателей с предметом.
    """

    if subject is None:
        return TeacherSubject.objects.none()

    return get_teacher_subjects_base_queryset().filter(
        subject=subject,
    )


def get_admin_teacher_subjects_queryset_for_actor(*, actor) -> QuerySet:
    """
    Возвращает предметы преподавателей, доступные пользователю в админке.

    Правила:
        - суперадминистратор видит все связи;
        - админ организации / директор видит связи преподавателей своей организации;
        - остальные пользователи ничего не видят.

    Args:
        actor:
            Пользователь.

    Returns:
        QuerySet: Доступные предметы преподавателей.
    """

    queryset = get_teacher_subjects_base_queryset()

    if not is_authenticated_active_actor(actor=actor):
        return TeacherSubject.objects.none()

    if is_superadmin_actor(actor=actor):
        return queryset

    organization_ids = get_actor_admin_organization_ids(actor=actor)

    if not organization_ids:
        return TeacherSubject.objects.none()

    return queryset.filter(
        Q(teacher__teacher_profile__organization_id__in=organization_ids)
        | Q(
            teacher__teacher_organizations__organization_id__in=organization_ids,
            teacher__teacher_organizations__is_active=True,
        )
    ).distinct()


def get_admin_active_teacher_subjects_queryset_for_actor(*, actor) -> QuerySet:
    """
    Возвращает активные предметы преподавателей, доступные в админке.

    Args:
        actor:
            Пользователь.

    Returns:
        QuerySet: Активные доступные предметы преподавателей.
    """

    return get_admin_teacher_subjects_queryset_for_actor(actor=actor).filter(
        is_active=True,
        subject__is_active=True,
        teacher__is_active=True,
    )


def actor_can_access_teacher_subject(
    *,
    actor,
    teacher_subject: TeacherSubject | None,
) -> bool:
    """
    Проверяет, может ли пользователь видеть предмет преподавателя.

    Args:
        actor:
            Пользователь.
        teacher_subject:
            Связь преподавателя с предметом.

    Returns:
        bool: True, если связь доступна.
    """

    if teacher_subject is None:
        return False

    if is_superadmin_actor(actor=actor):
        return True

    return (
        get_admin_teacher_subjects_queryset_for_actor(actor=actor)
        .filter(
            id=teacher_subject.id,
        )
        .exists()
    )


def actor_can_manage_teacher_subject(
    *,
    actor,
    teacher_subject: TeacherSubject | None,
) -> bool:
    """
    Проверяет, может ли пользователь управлять предметом преподавателя.

    Сейчас правила совпадают с административной видимостью.
    Более тонкие ограничения остаются в service-слое.

    Args:
        actor:
            Пользователь.
        teacher_subject:
            Связь преподавателя с предметом.

    Returns:
        bool: True, если управление разрешено.
    """

    return actor_can_access_teacher_subject(
        actor=actor,
        teacher_subject=teacher_subject,
    )
