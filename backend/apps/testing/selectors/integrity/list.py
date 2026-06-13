from __future__ import annotations

from apps.testing.selectors.integrity.base import integrity_report_base_queryset


def integrity_report_list_queryset(
    *,
    attempt_id: int | None = None,
    test_id: int | None = None,
    learner_id: int | None = None,
    risk_level: str | None = None,
    min_score: int | None = None,
    max_score: int | None = None,
):
    """
    Возвращает список отчётов добросовестности с фильтрами.
    """

    queryset = integrity_report_base_queryset()

    if attempt_id is not None:
        queryset = queryset.filter(attempt_id=attempt_id)

    if test_id is not None:
        queryset = queryset.filter(attempt__test_id=test_id)

    if learner_id is not None:
        queryset = queryset.filter(attempt__learner_id=learner_id)

    if risk_level is not None:
        queryset = queryset.filter(risk_level=risk_level)

    if min_score is not None:
        queryset = queryset.filter(score__gte=min_score)

    if max_score is not None:
        queryset = queryset.filter(score__lte=max_score)

    return queryset.order_by("-checked_at", "-id")


def risky_integrity_report_list_queryset():
    """
    Возвращает отчёты со средним и высоким риском.
    """

    return (
        integrity_report_base_queryset()
        .risky()
        .order_by(
            "-score",
            "-checked_at",
            "-id",
        )
    )
