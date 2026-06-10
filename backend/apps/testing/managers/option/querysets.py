from __future__ import annotations

from django.db import models


class TestQuestionOptionQuerySet(models.QuerySet):
    """
    QuerySet вариантов ответа.
    """

    def active(self):
        """
        Возвращает активные варианты ответа.
        """

        return self.filter(is_active=True)

    def for_question(self, question_id: int):
        """
        Фильтрует варианты по вопросу.
        """

        return self.filter(question_id=question_id)

    def correct(self):
        """
        Возвращает правильные варианты ответа.
        """

        return self.filter(is_correct=True)

    def incorrect(self):
        """
        Возвращает неправильные варианты ответа.
        """

        return self.filter(is_correct=False)

    def ordered(self):
        """
        Сортирует варианты в порядке отображения.
        """

        return self.order_by(
            "question_id",
            "order",
            "id",
        )
