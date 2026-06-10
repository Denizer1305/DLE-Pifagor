from __future__ import annotations

from django.db import models


class TestAttemptAnswerQuerySet(models.QuerySet):
    """
    QuerySet ответов на вопросы теста.
    """

    def for_attempt(self, attempt_id: int):
        """
        Фильтрует ответы по попытке.
        """

        return self.filter(attempt_id=attempt_id)

    def for_question(self, question_id: int):
        """
        Фильтрует ответы по вопросу.
        """

        return self.filter(question_id=question_id)

    def correct(self):
        """
        Возвращает верные ответы.
        """

        return self.filter(is_correct=True)

    def incorrect(self):
        """
        Возвращает неверные ответы.
        """

        return self.filter(is_correct=False)

    def unchecked(self):
        """
        Возвращает ответы без итоговой проверки.
        """

        return self.filter(is_correct__isnull=True)

    def needs_review(self):
        """
        Возвращает ответы, требующие ручной проверки.
        """

        return self.filter(requires_manual_review=True)

    def checked_by_teacher(self):
        """
        Возвращает ответы, проверенные преподавателем.
        """

        return self.filter(
            teacher_score__isnull=False,
            final_score__isnull=False,
        )
