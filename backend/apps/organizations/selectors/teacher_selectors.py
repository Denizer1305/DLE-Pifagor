from __future__ import annotations

from apps.organizations.models import Subject, TeacherSubject
from apps.users.constants.lifecycle import ProfileStatus
from apps.users.models import TeacherProfile
from django.db.models import Prefetch, Q, QuerySet


def get_public_teachers_base_queryset(organization) -> QuerySet:
    """
    Возвращает базовый QuerySet публичных преподавателей организации.

    Args:
        organization:
            Образовательная организация.

    Returns:
        QuerySet: Публичные преподаватели.
    """

    if organization is None:
        return TeacherProfile.objects.none()

    return (
        TeacherProfile.objects.select_related(
            "user",
            "organization",
            "department",
        )
        .prefetch_related(
            Prefetch(
                "user__teacher_subjects",
                queryset=TeacherSubject.objects.select_related(
                    "subject",
                ).filter(
                    is_active=True,
                    subject__is_active=True,
                ),
            ),
        )
        .filter(
            organization=organization,
            status=ProfileStatus.VERIFIED,
            is_public=True,
            show_on_teachers_page=True,
            user__is_active=True,
        )
        .order_by(
            "user__last_name",
            "user__first_name",
            "user__middle_name",
        )
    )


def filter_public_teachers_queryset(
    *,
    queryset: QuerySet,
    search: str = "",
    subject: str = "",
    position: str = "",
) -> QuerySet:
    """
    Фильтрует публичных преподавателей.

    Args:
        queryset:
            Исходный QuerySet преподавателей.
        search:
            Поиск по ФИО, должности, описанию и достижениям.
        subject:
            Код предмета.
        position:
            Поиск по должности или публичному заголовку.

    Returns:
        QuerySet: Отфильтрованный QuerySet.
    """

    search = (search or "").strip()
    subject = (subject or "").strip()
    position = (position or "").strip()

    if search:
        queryset = queryset.filter(
            Q(user__first_name__icontains=search)
            | Q(user__last_name__icontains=search)
            | Q(user__middle_name__icontains=search)
            | Q(position__icontains=search)
            | Q(public_title__icontains=search)
            | Q(short_bio__icontains=search)
            | Q(bio__icontains=search)
            | Q(achievements__icontains=search)
            | Q(user__teacher_subjects__subject__name__icontains=search)
            | Q(user__teacher_subjects__subject__short_name__icontains=search)
        )

    if subject:
        queryset = queryset.filter(
            user__teacher_subjects__is_active=True,
            user__teacher_subjects__subject__is_active=True,
            user__teacher_subjects__subject__code=subject,
        )

    if position:
        queryset = queryset.filter(
            Q(position__icontains=position) | Q(public_title__icontains=position)
        )

    return queryset.distinct()


def get_public_teachers_queryset(
    organization,
    *,
    search: str = "",
    subject: str = "",
    position: str = "",
) -> QuerySet:
    """
    Возвращает публичных преподавателей с применёнными фильтрами.

    Args:
        organization:
            Образовательная организация.
        search:
            Поисковая строка.
        subject:
            Код предмета.
        position:
            Фильтр по должности.

    Returns:
        QuerySet: Публичные преподаватели.
    """

    queryset = get_public_teachers_base_queryset(organization)

    return filter_public_teachers_queryset(
        queryset=queryset,
        search=search,
        subject=subject,
        position=position,
    )


def get_public_teacher_subjects_queryset(organization) -> QuerySet:
    """
    Возвращает предметы публичных преподавателей организации.

    Args:
        organization:
            Образовательная организация.

    Returns:
        QuerySet: Предметы для фильтра публичной страницы преподавателей.
    """

    if organization is None:
        return Subject.objects.none()

    return (
        Subject.objects.filter(
            is_active=True,
            teacher_subjects__is_active=True,
            teacher_subjects__teacher__is_active=True,
            teacher_subjects__teacher__teacher_profile__organization=organization,
            teacher_subjects__teacher__teacher_profile__status=ProfileStatus.VERIFIED,
            teacher_subjects__teacher__teacher_profile__is_public=True,
            teacher_subjects__teacher__teacher_profile__show_on_teachers_page=True,
        )
        .distinct()
        .order_by("name")
    )
