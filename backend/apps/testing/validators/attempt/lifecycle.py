from __future__ import annotations

from apps.testing.constants import TestAttemptStatus
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_attempt_can_be_submitted(*, attempt) -> None:
    """
    Проверяет, что попытку можно отправить на проверку.
    """

    if attempt.status != TestAttemptStatus.STARTED:
        raise ValidationError({"status": _("Отправить можно только начатую попытку.")})


def validate_attempt_can_be_checked(*, attempt) -> None:
    """
    Проверяет, что попытку можно проверить.
    """

    allowed_statuses = {
        TestAttemptStatus.SUBMITTED,
        TestAttemptStatus.AUTO_CHECKED,
        TestAttemptStatus.NEEDS_REVIEW,
    }

    if attempt.status not in allowed_statuses:
        raise ValidationError(
            {"status": _("Проверить можно только отправленную попытку.")}
        )


def validate_attempt_can_be_cancelled(*, attempt) -> None:
    """
    Проверяет, что попытку можно отменить.
    """

    blocked_statuses = {
        TestAttemptStatus.CONFIRMED,
        TestAttemptStatus.PUBLISHED,
        TestAttemptStatus.CANCELLED,
    }

    if attempt.status in blocked_statuses:
        raise ValidationError({"status": _("Эту попытку уже нельзя отменить.")})
