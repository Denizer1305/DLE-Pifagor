from __future__ import annotations

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from apps.testing.constants import TestAttemptStatus


def validate_attempt_limit(
    *,
    test,
    learner,
) -> None:
    """
    Проверяет, что лимит попыток теста не исчерпан.
    """

    from apps.testing.models import TestAttempt

    attempts_count = (
        TestAttempt.objects.filter(
            test=test,
            learner=learner,
        )
        .exclude(status=TestAttemptStatus.CANCELLED)
        .count()
    )

    if attempts_count >= test.max_attempts:
        raise ValidationError(
            {
                "attempts": _("Лимит попыток прохождения теста исчерпан.")
            }
        )


def validate_no_active_attempt(
    *,
    test,
    learner,
) -> None:
    """
    Проверяет, что у обучающегося нет активной незавершённой попытки.
    """

    from apps.testing.models import TestAttempt

    has_active_attempt = TestAttempt.objects.filter(
        test=test,
        learner=learner,
        status=TestAttemptStatus.STARTED,
    ).exists()

    if has_active_attempt:
        raise ValidationError(
            {
                "attempt": _("У обучающегося уже есть незавершённая попытка.")
            }
        )


def validate_attempt_number(
    *,
    attempt_number: int,
    test,
) -> None:
    """
    Проверяет номер попытки.
    """

    if attempt_number < 1:
        raise ValidationError(
            {
                "attempt_number": _("Номер попытки должен быть не меньше 1.")
            }
        )

    if attempt_number > test.max_attempts:
        raise ValidationError(
            {
                "attempt_number": _("Номер попытки превышает лимит теста.")
            }
        )