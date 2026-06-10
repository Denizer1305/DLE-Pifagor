from __future__ import annotations

from apps.testing.models import TestAttempt


def attempt_base_queryset():
    """
    Возвращает базовый queryset попыток теста.
    """

    return TestAttempt.objects.all()


def attempt_detail_queryset():
    """
    Возвращает queryset попыток для детального просмотра.
    """

    return attempt_base_queryset().prefetch_related(
        "answers",
        "answers__question",
        "answers__selected_option",
    )
