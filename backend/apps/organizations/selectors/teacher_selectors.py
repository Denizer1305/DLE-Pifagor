from __future__ import annotations

from apps.organizations.models import Organization, Subject
from apps.users.constants.lifecycle import ProfileStatus
from apps.users.models import TeacherProfile
from django.db.models import Q, QuerySet


def get_public_teachers_queryset(
    organization: Organization,
    *,
    search: str = "",
    subject: str = "",
    position: str = "",
) -> QuerySet[TeacherProfile]:
    """
    Возвращает публичных подтверждённых преподавателей организации.

    Args:
        organization:
            Образовательная организация.
        search:
            Поиск по ФИО, email, должности, описанию и предметам.
        subject:
            Код или ID предмета.
        position:
            Фильтр по должности.

    Returns:
        QuerySet[TeacherProfile]: QuerySet публичных профилей преподавателей.
    """

    queryset = (
        TeacherProfile.objects.filter(
            organization=organization,
            status=ProfileStatus.VERIFIED,
            is_public=True,
            show_on_teachers_page=True,
            user__is_active=True,
        )
        .select_related(
            "user",
            "user__profile",
            "organization",
            "department",
        )
        .prefetch_related(
            "user__teacher_subjects__subject",
        )
        .order_by(
            "user__last_name",
            "user__first_name",
            "user__middle_name",
            "id",
        )
    )

    normalized_search = search.strip()

    if normalized_search:
        queryset = queryset.filter(
            Q(user__last_name__icontains=normalized_search)
            | Q(user__first_name__icontains=normalized_search)
            | Q(user__middle_name__icontains=normalized_search)
            | Q(user__email__icontains=normalized_search)
            | Q(position__icontains=normalized_search)
            | Q(public_title__icontains=normalized_search)
            | Q(short_bio__icontains=normalized_search)
            | Q(bio__icontains=normalized_search)
            | Q(user__teacher_subjects__subject__name__icontains=normalized_search)
            | Q(
                user__teacher_subjects__subject__short_name__icontains=normalized_search
            )
        )

    normalized_position = position.strip()

    if normalized_position:
        queryset = queryset.filter(position__icontains=normalized_position)

    normalized_subject = subject.strip()

    if normalized_subject:
        queryset = queryset.filter(
            Q(user__teacher_subjects__subject__id__iexact=normalized_subject)
            | Q(user__teacher_subjects__subject__code__iexact=normalized_subject)
        )

    return queryset.distinct()


def get_public_teacher_subjects_queryset(
    organization: Organization,
) -> QuerySet[Subject]:
    """
    Возвращает предметы публичных подтверждённых преподавателей организации.

    Args:
        organization:
            Образовательная организация.

    Returns:
        QuerySet[Subject]: QuerySet предметов.
    """

    return (
        Subject.objects.filter(
            is_active=True,
            teacher_links__is_active=True,
            teacher_links__teacher__teacher_profile__organization=organization,
            teacher_links__teacher__teacher_profile__status=ProfileStatus.VERIFIED,
            teacher_links__teacher__teacher_profile__is_public=True,
            teacher_links__teacher__teacher_profile__show_on_teachers_page=True,
            teacher_links__teacher__is_active=True,
        )
        .distinct()
        .order_by("name")
    )
