from __future__ import annotations

from apps.testing.selectors import get_attempt_by_id
from apps.testing.services import build_attempt_integrity_report
from django.db import transaction


@transaction.atomic
def build_attempt_integrity_report_task(*, attempt_id: int) -> dict:
    """
    Формирует отчёт о признаках возможного списывания.

    Отчёт не является доказательством списывания.
    Он только помогает преподавателю обратить внимание на попытку.
    """

    attempt = get_attempt_by_id(attempt_id)

    return build_attempt_integrity_report(attempt=attempt)
