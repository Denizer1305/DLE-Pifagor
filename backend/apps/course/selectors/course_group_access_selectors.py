from __future__ import annotations

from apps.course.models import CourseGroupAccess
from django.db.models import Q, QuerySet


def course_group_access_base_queryset() -> QuerySet[CourseGroupAccess]:
    """
    Возвращает базовый queryset доступов групп к курсам.
    """

    return CourseGroupAccess.objects.select_related(
        "course",
        "group",
        "group_subject",
        "teacher_group_subject",
        "course__owner_teacher",
        "course__organization",
        "course__subject",
    )


def course_group_access_list_queryset(
    *,
    search: str | None = None,
    course_id: int | None = None,
    group_id: int | None = None,
    group_subject_id: int | None = None,
    teacher_group_subject_id: int | None = None,
    visibility: str | None = None,
    auto_enroll: bool | None = None,
    is_active: bool | None = None,
) -> QuerySet[CourseGroupAccess]:
    """
    Возвращает список доступов групп к курсам.
    """

    queryset = course_group_access_base_queryset()

    if search:
        queryset = queryset.filter(
            Q(course__title__icontains=search)
            | Q(course__code__icontains=search)
            | Q(group__name__icontains=search)
            | Q(group__code__icontains=search)
            | Q(course__organization__name__icontains=search)
            | Q(course__organization__short_name__icontains=search)
            | Q(course__subject__name__icontains=search)
            | Q(course__subject__code__icontains=search)
        )

    if course_id:
        queryset = queryset.filter(course_id=course_id)

    if group_id:
        queryset = queryset.filter(group_id=group_id)

    if group_subject_id:
        queryset = queryset.filter(group_subject_id=group_subject_id)

    if teacher_group_subject_id:
        queryset = queryset.filter(teacher_group_subject_id=teacher_group_subject_id)

    if visibility:
        queryset = queryset.filter(visibility=visibility)

    if auto_enroll is not None:
        queryset = queryset.filter(auto_enroll=auto_enroll)

    if is_active is not None:
        queryset = queryset.filter(is_active=is_active)

    return queryset.order_by(
        "course_id",
        "group_id",
    )


def course_group_access_detail_queryset() -> QuerySet[CourseGroupAccess]:
    """
    Возвращает queryset доступа группы с деталями.
    """

    return course_group_access_base_queryset().prefetch_related(
        "enrollments",
    )


def get_course_group_access_by_id(
    access_id: int,
) -> CourseGroupAccess:
    """
    Возвращает доступ группы к курсу по идентификатору.
    """

    return course_group_access_detail_queryset().get(id=access_id)


def get_course_group_access_by_course_and_group(
    *,
    course_id: int,
    group_id: int,
) -> CourseGroupAccess:
    """
    Возвращает доступ группы к конкретному курсу.
    """

    return course_group_access_detail_queryset().get(
        course_id=course_id,
        group_id=group_id,
    )
