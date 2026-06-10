from __future__ import annotations

from apps.testing.models import TestAttemptAnswer


def answer_base_queryset():
    """
    Возвращает базовый queryset ответов на вопросы теста.
    """

    return TestAttemptAnswer.objects.all()


def answer_detail_queryset():
    """
    Возвращает queryset ответов для детального просмотра.
    """

    return answer_base_queryset()
