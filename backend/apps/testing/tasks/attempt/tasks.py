from __future__ import annotations

from apps.testing.selectors import get_attempt_for_update
from apps.testing.services.attempt.time_limit import expire_attempt_if_needed
from apps.testing.services.checking import auto_check_attempt
from django.db import transaction


@transaction.atomic
def auto_check_attempt_task(*, attempt_id: int):
    """
    Запускает автопроверку попытки теста.
    """

    attempt = get_attempt_for_update(attempt_id)

    return auto_check_attempt(attempt=attempt)


@transaction.atomic
def expire_attempt_task(*, attempt_id: int):
    """
    Помечает попытку истёкшей, если время прохождения закончилось.
    """

    attempt = get_attempt_for_update(attempt_id)

    return expire_attempt_if_needed(attempt=attempt)
