from __future__ import annotations

from apps.testing.selectors import get_attempt_by_id
from apps.testing.services.integrity.persistence import (
    build_and_save_attempt_integrity_report,
)
from apps.testing.services.integrity.recalculation import (
    build_attempt_integrity_report_payload,
)
from django.db import transaction


@transaction.atomic
def build_attempt_integrity_report_task(*, attempt_id: int) -> dict:
    """
    Формирует отчёт о признаках возможного списывания без сохранения.

    Оставлено для обратной совместимости с существующим endpoint.
    """

    attempt = get_attempt_by_id(attempt_id)

    return build_attempt_integrity_report_payload(attempt=attempt)


@transaction.atomic
def build_and_save_attempt_integrity_report_task(*, attempt_id: int):
    """
    Формирует и сохраняет отчёт добросовестности попытки.
    """

    attempt = get_attempt_by_id(attempt_id)

    return build_and_save_attempt_integrity_report(attempt=attempt)
