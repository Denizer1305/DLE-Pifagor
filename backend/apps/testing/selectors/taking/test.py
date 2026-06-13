from __future__ import annotations

from apps.testing.constants import TestAttemptStatus, TestStatus
from apps.testing.models import Test, TestAttempt
from django.shortcuts import get_object_or_404


def taking_test_queryset():
    """
    Возвращает queryset тестов, доступных для прохождения.
    """

    return (
        Test.objects.filter(
            status=TestStatus.PUBLISHED,
            is_active=True,
        )
        .select_related(
            "course",
            "lesson",
            "lesson_block",
            "organization",
            "subject",
            "owner_teacher",
        )
        .prefetch_related(
            "questions",
            "questions__options",
        )
    )


def get_taking_test_by_id(test_id: int):
    """
    Возвращает опубликованный тест для прохождения.
    """

    return get_object_or_404(
        taking_test_queryset(),
        id=test_id,
    )


def get_active_attempt_for_taking(
    *,
    test_id: int,
    learner_id: int,
):
    """
    Возвращает активную попытку обучающегося для прохождения теста.
    """

    return (
        TestAttempt.objects.filter(
            test_id=test_id,
            learner_id=learner_id,
            status=TestAttemptStatus.STARTED,
        )
        .select_related(
            "test",
            "learner",
        )
        .order_by("-attempt_number", "-id")
        .first()
    )


def get_taking_attempt_by_id(
    *,
    attempt_id: int,
    learner_id: int,
):
    """
    Возвращает попытку обучающегося для прохождения.
    """

    return get_object_or_404(
        TestAttempt.objects.select_related(
            "test",
            "learner",
        ).prefetch_related(
            "answers",
            "answers__question",
            "answers__selected_option",
        ),
        id=attempt_id,
        learner_id=learner_id,
    )
