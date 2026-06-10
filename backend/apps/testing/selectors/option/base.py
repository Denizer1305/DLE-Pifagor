from __future__ import annotations

from apps.testing.models import TestQuestionOption


def option_base_queryset():
    """
    Возвращает базовый queryset вариантов ответа.
    """

    return TestQuestionOption.objects.all()


def option_detail_queryset():
    """
    Возвращает queryset вариантов ответа для детального просмотра.
    """

    return option_base_queryset()
