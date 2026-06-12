from __future__ import annotations

from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.testing.constants import TestAttemptStatus


def validate_attempt_time_limit(*, attempt) -> None:
    """
    Проверяет, что время попытки не истекло.
    """

    if not attempt.expires_at:
        return

    if attempt.status == TestAttemptStatus.EXPIRED:
        raise ValidationError(
            {
                "status": _("Время прохождения попытки уже истекло.")
            }
        )

    if timezone.now() <= attempt.expires_at:
        return

    raise ValidationError(
        {
            "expires_at": _("Время прохождения попытки истекло.")
        }
    )


def validate_attempt_can_accept_answers_by_time(*, attempt) -> None:
    """
    Проверяет, что попытка ещё может принимать ответы по времени.
    """

    validate_attempt_time_limit(attempt=attempt)


def validate_attempt_can_be_submitted_by_time(*, attempt) -> None:
    """
    Проверяет, что попытку можно отправить по времени.
    """

    validate_attempt_time_limit(attempt=attempt)