from __future__ import annotations

from apps.testing.models import TestAttemptIntegrityReport


def integrity_report_base_queryset():
    """
    Возвращает базовый queryset отчётов добросовестности.
    """

    return TestAttemptIntegrityReport.objects.all()


def integrity_report_detail_queryset():
    """
    Возвращает queryset отчётов для детального просмотра.
    """

    return integrity_report_base_queryset()
