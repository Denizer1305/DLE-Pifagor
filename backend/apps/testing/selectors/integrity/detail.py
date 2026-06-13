from __future__ import annotations

from apps.testing.selectors.integrity.base import integrity_report_detail_queryset
from django.shortcuts import get_object_or_404


def get_integrity_report_by_id(report_id: int):
    """
    Возвращает отчёт добросовестности по идентификатору.
    """

    return get_object_or_404(
        integrity_report_detail_queryset(),
        id=report_id,
    )


def get_integrity_report_by_attempt_id(attempt_id: int):
    """
    Возвращает отчёт добросовестности по попытке.
    """

    return get_object_or_404(
        integrity_report_detail_queryset(),
        attempt_id=attempt_id,
    )


def get_integrity_report_for_update(report_id: int):
    """
    Возвращает отчёт добросовестности для изменения.
    """

    return get_object_or_404(
        integrity_report_detail_queryset().select_for_update(),
        id=report_id,
    )
