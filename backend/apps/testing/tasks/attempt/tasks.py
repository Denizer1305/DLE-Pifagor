from __future__ import annotations

from apps.testing.selectors import get_attempt_for_update
from apps.testing.services import auto_check_attempt
from django.db import transaction


@transaction.atomic
def auto_check_attempt_task(*, attempt_id: int):
    """
    Запускает автопроверку попытки теста.

    Сейчас задача вызывается синхронно. При подключении Celery/RQ
    эту функцию можно будет обернуть в shared_task без изменения сервисов.
    """

    attempt = get_attempt_for_update(attempt_id)

    return auto_check_attempt(attempt=attempt)
