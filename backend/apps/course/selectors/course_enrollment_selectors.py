from __future__ import annotations

from apps.course.models import CourseEnrollment
from django.db.models import Q, QuerySet


def course_enrollment_base_queryset() -> QuerySet[CourseEnrollment]:
    """
    Возвращает базовый queryset записей на курс.
    """

    return CourseEnrollment.objects.select_related(
        "course",
        "learner",
        "group_access",
        "access_rule",
        "course__organization",
        "course__subject",
        "course__owner_teacher",
    )


def course_enrollment_list_queryset(
    *,
    search: str | None = None,
    course_id: int | None = None,
    learner_id: int | None = None,
    group_access_id: int | None = None,
    access_rule_id: int | None = None,
    status: str | None = None,
) -> QuerySet[CourseEnrollment]:
    """
    Возвращает список записей на курс.
    """

    queryset = course_enrollment_base_queryset()

    if search:
        queryset = queryset.filter(
            Q(course__title__icontains=search)
            | Q(course__code__icontains=search)
            | Q(learner__email__icontains=search)
            | Q(learner__first_name__icontains=search)
            | Q(learner__last_name__icontains=search)
        )

    if course_id:
        queryset = queryset.filter(course_id=course_id)

    if learner_id:
        queryset = queryset.filter(learner_id=learner_id)

    if group_access_id:
        queryset = queryset.filter(group_access_id=group_access_id)

    if access_rule_id:
        queryset = queryset.filter(access_rule_id=access_rule_id)

    if status:
        queryset = queryset.filter(status=status)

    return queryset.order_by(
        "-last_activity_at",
        "-enrolled_at",
        "-id",
    )


def course_enrollment_detail_queryset() -> QuerySet[CourseEnrollment]:
    """
    Возвращает queryset записи на курс с деталями.
    """

    return (
        course_enrollment_base_queryset()
        .prefetch_related(
            "lesson_progresses",
        )
        .select_related(
            "progress",
        )
    )


def get_course_enrollment_by_id(
    enrollment_id: int,
) -> CourseEnrollment:
    """
    Возвращает запись на курс по идентификатору.
    """

    return course_enrollment_detail_queryset().get(id=enrollment_id)


def get_course_enrollment_by_course_and_learner(
    *,
    course_id: int,
    learner_id: int,
) -> CourseEnrollment:
    """
    Возвращает запись пользователя на конкретный курс.
    """

    return course_enrollment_detail_queryset().get(
        course_id=course_id,
        learner_id=learner_id,
    )
