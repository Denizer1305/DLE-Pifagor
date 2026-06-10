from __future__ import annotations

from apps.testing.models import TestQuestion


def question_base_queryset():
    """
    Возвращает базовый queryset вопросов теста.
    """

    return TestQuestion.objects.all()


def question_detail_queryset():
    """
    Возвращает queryset вопросов для детального просмотра.
    """

    return question_base_queryset().prefetch_related("options")
