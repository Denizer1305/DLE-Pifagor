from __future__ import annotations

from apps.testing.models import TestLearnerResult


def result_base_queryset():
    """
    Возвращает базовый queryset итоговых результатов.
    """

    return TestLearnerResult.objects.all()


def result_detail_queryset():
    """
    Возвращает queryset итоговых результатов для детального просмотра.
    """

    return result_base_queryset()
