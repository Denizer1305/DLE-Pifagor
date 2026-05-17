from __future__ import annotations

from apps.users.constants.lifecycle import ProfileStatus
from apps.users.models import TeacherProfile
from django.db.models import QuerySet


def get_teacher_profiles_queryset() -> QuerySet:
    """
    Возвращает базовый QuerySet профилей преподавателей.

    Returns:
        QuerySet: Профили преподавателей.
    """

    return TeacherProfile.objects.select_related(
        "user",
        "organization",
        "department",
        "verified_by",
    )


def get_teacher_profile_by_user(user):
    """
    Возвращает профиль преподавателя по пользователю.

    Args:
        user:
            Пользователь.

    Returns:
        TeacherProfile | None: Профиль преподавателя или None.
    """

    if not user:
        return None

    return get_teacher_profiles_queryset().filter(user=user).first()


def get_teacher_profile_by_id(profile_id: int):
    """
    Возвращает профиль преподавателя по ID.

    Args:
        profile_id:
            ID профиля преподавателя.

    Returns:
        TeacherProfile | None: Профиль преподавателя или None.
    """

    if not profile_id:
        return None

    return get_teacher_profiles_queryset().filter(id=profile_id).first()


def get_verified_teacher_profiles_queryset() -> QuerySet:
    """
    Возвращает подтверждённые профили преподавателей.

    Returns:
        QuerySet: Подтверждённые профили преподавателей.
    """

    return get_teacher_profiles_queryset().filter(status=ProfileStatus.VERIFIED)


def get_public_teacher_profiles_queryset() -> QuerySet:
    """
    Возвращает публичные профили преподавателей.

    Returns:
        QuerySet: Публичные профили преподавателей.
    """

    return get_verified_teacher_profiles_queryset().filter(
        is_public=True,
        show_on_teachers_page=True,
    )


def get_teachers_by_organization(organization) -> QuerySet:
    """
    Возвращает преподавателей образовательной организации.

    Args:
        organization:
            Образовательная организация.

    Returns:
        QuerySet: Профили преподавателей организации.
    """

    if not organization:
        return TeacherProfile.objects.none()

    return get_teacher_profiles_queryset().filter(organization=organization)


def get_teachers_by_department(department) -> QuerySet:
    """
    Возвращает преподавателей отделения.

    Args:
        department:
            Отделение.

    Returns:
        QuerySet: Профили преподавателей отделения.
    """

    if not department:
        return TeacherProfile.objects.none()

    return get_teacher_profiles_queryset().filter(department=department)


def get_public_teachers_by_organization(organization) -> QuerySet:
    """
    Возвращает публичных преподавателей образовательной организации.

    Args:
        organization:
            Образовательная организация.

    Returns:
        QuerySet: Публичные профили преподавателей организации.
    """

    if not organization:
        return TeacherProfile.objects.none()

    return get_public_teacher_profiles_queryset().filter(organization=organization)
