from __future__ import annotations

from apps.testing.selectors import teacher_testing_summary, test_review_summary


def build_test_review_summary(*, test_id: int) -> dict:
    """
    Возвращает сводку по конкретному тесту.
    """

    return _normalize_summary(
        summary=test_review_summary(test_id=test_id),
    )


def build_teacher_testing_summary(*, teacher_id: int) -> dict:
    """
    Возвращает общую сводку по тестированию преподавателя.
    """

    return _normalize_summary(
        summary=teacher_testing_summary(teacher_id=teacher_id),
    )


def _normalize_summary(*, summary: dict) -> dict:
    """
    Заменяет None на нули в числовой сводке.
    """

    return {key: value if value is not None else 0 for key, value in summary.items()}
