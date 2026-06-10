from __future__ import annotations

from apps.testing.constants import AttemptCheckStatus, TestAttemptStatus, TestStatus
from apps.testing.models import TestAttempt
from apps.testing.services.attempt.payloads import apply_attempt_payload
from apps.testing.validators import (
    validate_attempt_can_be_cancelled,
    validate_attempt_can_be_submitted,
    validate_attempt_limit,
    validate_attempt_number,
    validate_no_active_attempt,
)
from django.db import transaction
from django.utils import timezone


@transaction.atomic
def start_test_attempt(
    *,
    test,
    learner,
) -> TestAttempt:
    """
    Начинает новую попытку прохождения теста.
    """

    _validate_test_available_for_attempt(test=test)

    validate_attempt_limit(
        test=test,
        learner=learner,
    )
    validate_no_active_attempt(
        test=test,
        learner=learner,
    )

    attempt_number = _get_next_attempt_number(
        test=test,
        learner=learner,
    )
    validate_attempt_number(
        attempt_number=attempt_number,
        test=test,
    )

    attempt = TestAttempt(
        test=test,
        learner=learner,
        attempt_number=attempt_number,
        status=TestAttemptStatus.STARTED,
        check_status=AttemptCheckStatus.NOT_CHECKED,
        started_at=timezone.now(),
    )

    attempt.full_clean()
    attempt.save()

    return attempt


@transaction.atomic
def submit_test_attempt(
    *,
    attempt: TestAttempt,
) -> TestAttempt:
    """
    Отправляет попытку на проверку.
    """

    validate_attempt_can_be_submitted(attempt=attempt)

    attempt.status = TestAttemptStatus.SUBMITTED
    attempt.submitted_at = timezone.now()

    attempt.full_clean()
    attempt.save(
        update_fields=[
            "status",
            "submitted_at",
            "updated_at",
        ]
    )

    return attempt


@transaction.atomic
def cancel_test_attempt(
    *,
    attempt: TestAttempt,
) -> TestAttempt:
    """
    Отменяет попытку прохождения теста.
    """

    validate_attempt_can_be_cancelled(attempt=attempt)

    attempt.status = TestAttemptStatus.CANCELLED

    attempt.full_clean()
    attempt.save(
        update_fields=[
            "status",
            "updated_at",
        ]
    )

    return attempt


@transaction.atomic
def update_test_attempt(
    *,
    attempt: TestAttempt,
    data: dict,
) -> TestAttempt:
    """
    Обновляет попытку теста.
    """

    apply_attempt_payload(
        attempt=attempt,
        data=data,
    )

    attempt.full_clean()
    attempt.save()

    return attempt


def _get_next_attempt_number(
    *,
    test,
    learner,
) -> int:
    """
    Возвращает следующий номер попытки.
    """

    attempts_count = (
        TestAttempt.objects.filter(
            test=test,
            learner=learner,
        )
        .exclude(status=TestAttemptStatus.CANCELLED)
        .count()
    )

    return attempts_count + 1


def _validate_test_available_for_attempt(*, test) -> None:
    """
    Проверяет, что тест доступен для прохождения.
    """

    if test.status != TestStatus.PUBLISHED or not test.is_active:
        from django.core.exceptions import ValidationError
        from django.utils.translation import gettext_lazy as _

        raise ValidationError({"test": _("Тест недоступен для прохождения.")})
