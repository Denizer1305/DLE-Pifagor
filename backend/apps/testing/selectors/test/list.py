from __future__ import annotations

from apps.testing.constants import TestStatus
from apps.testing.selectors.test.base import test_base_queryset
from django.db.models import Q


def test_list_queryset(
    *,
    search: str | None = None,
    course_id: int | None = None,
    lesson_id: int | None = None,
    organization_id: int | None = None,
    subject_id: int | None = None,
    owner_teacher_id: int | None = None,
    status: str | None = None,
    is_active: bool | None = None,
):
    """
    Возвращает список тестов с базовыми фильтрами.
    """

    queryset = test_base_queryset()

    if search:
        queryset = queryset.filter(
            Q(title__icontains=search)
            | Q(description__icontains=search)
            | Q(instructions__icontains=search)
        )

    if course_id is not None:
        queryset = queryset.filter(course_id=course_id)

    if lesson_id is not None:
        queryset = queryset.filter(lesson_id=lesson_id)

    if organization_id is not None:
        queryset = queryset.filter(organization_id=organization_id)

    if subject_id is not None:
        queryset = queryset.filter(subject_id=subject_id)

    if owner_teacher_id is not None:
        queryset = queryset.filter(owner_teacher_id=owner_teacher_id)

    if status:
        queryset = queryset.filter(status=status)

    if is_active is not None:
        queryset = queryset.filter(is_active=is_active)

    return queryset


def published_test_list_queryset():
    """
    Возвращает опубликованные активные тесты.
    """

    return test_list_queryset(
        status=TestStatus.PUBLISHED,
        is_active=True,
    )
