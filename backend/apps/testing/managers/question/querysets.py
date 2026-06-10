from __future__ import annotations

from apps.testing.constants import QuestionCheckMode, QuestionType
from django.db import models


class TestQuestionQuerySet(models.QuerySet):
    """
    QuerySet вопросов тестов.
    """

    def active(self):
        """
        Возвращает активные вопросы.
        """

        return self.filter(is_active=True)

    def for_test(self, test_id: int):
        """
        Фильтрует вопросы по тесту.
        """

        return self.filter(test_id=test_id)

    def by_type(self, question_type: str):
        """
        Фильтрует вопросы по типу.
        """

        return self.filter(question_type=question_type)

    def auto_checked(self):
        """
        Возвращает вопросы с автоматической проверкой.
        """

        return self.filter(check_mode=QuestionCheckMode.AUTO)

    def semi_auto_checked(self):
        """
        Возвращает вопросы с полуавтоматической проверкой.
        """

        return self.filter(check_mode=QuestionCheckMode.SEMI_AUTO)

    def manual_checked(self):
        """
        Возвращает вопросы с ручной проверкой.
        """

        return self.filter(check_mode=QuestionCheckMode.MANUAL)

    def choice_questions(self):
        """
        Возвращает вопросы с вариантами ответа.
        """

        return self.filter(
            question_type__in=[
                QuestionType.SINGLE_CHOICE,
                QuestionType.MULTIPLE_CHOICE,
                QuestionType.TRUE_FALSE,
            ]
        )

    def ordered(self):
        """
        Сортирует вопросы в порядке прохождения.
        """

        return self.order_by(
            "test_id",
            "order",
            "id",
        )
