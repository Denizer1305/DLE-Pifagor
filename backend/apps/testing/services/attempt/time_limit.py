from __future__ import annotations

from datetime import timedelta

from apps.testing.constants import TestAttemptStatus
from apps.testing.validators import (
    validate_attempt_can_accept_answers_by_time,
    validate_attempt_can_be_submitted_by_time,
)
from django.db import transaction
from django.utils import timezone


def calculate_attempt_expires_at(*, attempt):
    """
    Рассчитывает время истечения попытки.
    """

    if not attempt.test.time_limit_minutes:
        return None

    if not attempt.started_at:
        return None

    return attempt.started_at + timedelta(
        minutes=attempt.test.time_limit_minutes,
    )


@transaction.atomic
def set_attempt_expires_at(*, attempt):
    """
    Устанавливает время истечения попытки.
    """

    attempt.expires_at = calculate_attempt_expires_at(attempt=attempt)

    attempt.save(
        update_fields=[
            "expires_at",
            "updated_at",
        ]
    )

    return attempt


@transaction.atomic
def expire_attempt_if_needed(*, attempt):
    """
    Помечает попытку истёкшей, если время прохождения закончилось.
    """

    if not attempt.expires_at:
        return attempt

    if attempt.status != TestAttemptStatus.STARTED:
        return attempt

    if timezone.now() <= attempt.expires_at:
        return attempt

    attempt.status = TestAttemptStatus.EXPIRED
    attempt.expired_at = timezone.now()

    attempt.save(
        update_fields=[
            "status",
            "expired_at",
            "updated_at",
        ]
    )

    return attempt


def ensure_attempt_accepts_answers_by_time(*, attempt) -> None:
    """
    Проверяет, что попытка может принимать ответы по времени.
    """

    expire_attempt_if_needed(attempt=attempt)

    attempt.refresh_from_db()

    validate_attempt_can_accept_answers_by_time(attempt=attempt)


def ensure_attempt_can_be_submitted_by_time(*, attempt) -> None:
    """
    Проверяет, что попытку можно отправить по времени.
    """

    expire_attempt_if_needed(attempt=attempt)

    attempt.refresh_from_db()

    validate_attempt_can_be_submitted_by_time(attempt=attempt)
