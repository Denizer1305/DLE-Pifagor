from __future__ import annotations

from apps.course.models import CourseEnrollment
from apps.testing.constants import TestAttemptStatus, TestStatus
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_test_available_for_taking(*, test) -> None:
    """
    Проверяет, что тест доступен для прохождения.
    """

    if test.status != TestStatus.PUBLISHED or not test.is_active:
        raise ValidationError({"test": _("Тест недоступен для прохождения.")})


def validate_learner_has_test_access(
    *,
    test,
    learner,
) -> None:
    """
    Проверяет доступ обучающегося к тесту через запись на курс.
    """

    has_access = CourseEnrollment.objects.filter(
        course_id=test.course_id,
        learner_id=learner.id,
    ).exists()

    if not has_access:
        raise ValidationError(
            {"learner": _("У обучающегося нет доступа к этому тесту.")}
        )


def validate_attempt_belongs_to_learner(
    *,
    attempt,
    learner,
) -> None:
    """
    Проверяет, что попытка принадлежит обучающемуся.
    """

    if attempt.learner_id != learner.id:
        raise ValidationError(
            {"attempt": _("Попытка не принадлежит текущему обучающемуся.")}
        )


def validate_attempt_available_for_taking(*, attempt) -> None:
    """
    Проверяет, что попытку можно продолжать проходить.
    """

    if attempt.status != TestAttemptStatus.STARTED:
        raise ValidationError(
            {"attempt": _("Продолжить можно только начатую попытку.")}
        )


def ensure_learner_can_take_test(
    *,
    test,
    learner,
) -> None:
    """
    Проверяет полный доступ обучающегося к прохождению теста.
    """

    validate_test_available_for_taking(test=test)
    validate_learner_has_test_access(
        test=test,
        learner=learner,
    )


def ensure_learner_can_continue_attempt(
    *,
    attempt,
    learner,
) -> None:
    """
    Проверяет, что обучающийся может продолжить попытку.
    """

    validate_attempt_belongs_to_learner(
        attempt=attempt,
        learner=learner,
    )
    validate_attempt_available_for_taking(attempt=attempt)
