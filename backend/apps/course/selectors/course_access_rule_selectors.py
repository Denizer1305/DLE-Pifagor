from __future__ import annotations

from apps.course.models import CourseAccessRule
from django.db.models import Q, QuerySet


def course_access_rule_base_queryset() -> QuerySet[CourseAccessRule]:
    """
    Возвращает базовый queryset правил доступа к курсам.
    """

    return CourseAccessRule.objects.select_related(
        "course",
        "learner",
        "organization",
        "course__owner_teacher",
        "course__organization",
    )


def course_access_rule_list_queryset(
    *,
    search: str | None = None,
    course_id: int | None = None,
    access_type: str | None = None,
    learner_id: int | None = None,
    organization_id: int | None = None,
    auto_enroll: bool | None = None,
    is_active: bool | None = None,
) -> QuerySet[CourseAccessRule]:
    """
    Возвращает список правил доступа к курсам.
    """

    queryset = course_access_rule_base_queryset()

    if search:
        queryset = queryset.filter(
            Q(course__title__icontains=search)
            | Q(course__code__icontains=search)
            | Q(access_code__icontains=search)
            | Q(learner__email__icontains=search)
            | Q(learner__first_name__icontains=search)
            | Q(learner__last_name__icontains=search)
            | Q(organization__name__icontains=search)
            | Q(organization__short_name__icontains=search)
            | Q(organization__code__icontains=search)
        )

    if course_id:
        queryset = queryset.filter(course_id=course_id)

    if access_type:
        queryset = queryset.filter(access_type=access_type)

    if learner_id:
        queryset = queryset.filter(learner_id=learner_id)

    if organization_id:
        queryset = queryset.filter(organization_id=organization_id)

    if auto_enroll is not None:
        queryset = queryset.filter(auto_enroll=auto_enroll)

    if is_active is not None:
        queryset = queryset.filter(is_active=is_active)

    return queryset.order_by(
        "course_id",
        "access_type",
        "id",
    )


def course_access_rule_detail_queryset() -> QuerySet[CourseAccessRule]:
    """
    Возвращает queryset правила доступа с деталями.
    """

    return course_access_rule_base_queryset().prefetch_related(
        "enrollments",
    )


def get_course_access_rule_by_id(
    rule_id: int,
) -> CourseAccessRule:
    """
    Возвращает правило доступа к курсу по идентификатору.
    """

    return course_access_rule_detail_queryset().get(id=rule_id)


def get_course_access_rule_by_code(
    access_code: str,
) -> CourseAccessRule:
    """
    Возвращает правило доступа по коду.
    """

    return course_access_rule_detail_queryset().get(access_code=access_code)
