from __future__ import annotations

from apps.testing.models import TestAttemptIntegrityReport
from apps.testing.services.integrity.recalculation import (
    build_attempt_integrity_report_payload,
)
from django.db import transaction
from django.utils import timezone


@transaction.atomic
def save_attempt_integrity_report(
    *,
    attempt,
    report_data: dict,
) -> TestAttemptIntegrityReport:
    """
    Создаёт или обновляет сохранённый отчёт добросовестности попытки.
    """

    report, _created = TestAttemptIntegrityReport.objects.get_or_create(
        attempt=attempt,
        defaults={
            "score": report_data["score"],
            "risk_level": report_data["risk_level"],
            "flags_data": report_data["flags_data"],
            "checked_at": timezone.now(),
        },
    )

    if not _created:
        report.score = report_data["score"]
        report.risk_level = report_data["risk_level"]
        report.flags_data = report_data["flags_data"]
        report.checked_at = timezone.now()

    report.full_clean()
    report.save()

    return report


@transaction.atomic
def build_and_save_attempt_integrity_report(*, attempt):
    """
    Формирует и сохраняет отчёт добросовестности попытки.
    """

    report_data = build_attempt_integrity_report_payload(attempt=attempt)

    return save_attempt_integrity_report(
        attempt=attempt,
        report_data=report_data,
    )
