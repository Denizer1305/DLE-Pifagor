from __future__ import annotations

from apps.testing.models import Test


def test_base_queryset():
    """
    Возвращает базовый queryset тестов.
    """

    return Test.objects.all()


def test_detail_queryset():
    """
    Возвращает queryset тестов для детального просмотра.
    """

    return test_base_queryset().prefetch_related(
        "questions",
        "questions__options",
    )
