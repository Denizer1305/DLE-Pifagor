from __future__ import annotations

from apps.testing.tests.factories import create_result
from apps.testing.validators import (
    validate_result_attempt_counters,
    validate_result_blocking,
    validate_result_scores,
    validate_result_visibility,
)
from django.core.exceptions import ValidationError
from django.test import TestCase


class TestResultCounterValidatorsTestCase(TestCase):
    """
    Тесты валидаторов счётчиков итогового результата.
    """

    def test_result_counters_allow_valid_values(self) -> None:
        """
        Валидатор пропускает корректные счётчики.
        """

        result = create_result(
            attempts_count=2,
            confirmed_attempts_count=1,
        )

        validate_result_attempt_counters(result=result)

    def test_result_counters_reject_confirmed_above_total(self) -> None:
        """
        Подтверждённых попыток не может быть больше общего количества.
        """

        result = create_result(
            attempts_count=1,
            confirmed_attempts_count=2,
        )

        with self.assertRaises(ValidationError):
            validate_result_attempt_counters(result=result)


class TestResultScoreValidatorsTestCase(TestCase):
    """
    Тесты валидаторов баллов и оценок результата.
    """

    def test_result_scores_allow_valid_values(self) -> None:
        """
        Валидатор пропускает корректные значения.
        """

        result = create_result(
            average_score=80,
            average_grade=4,
            best_score=90,
            best_grade=5,
        )

        validate_result_scores(result=result)

    def test_result_scores_reject_invalid_average_grade(self) -> None:
        """
        Средняя оценка должна быть от 2 до 5.
        """

        result = create_result(
            average_grade=6,
        )

        with self.assertRaises(ValidationError):
            validate_result_scores(result=result)


class TestResultVisibilityValidatorsTestCase(TestCase):
    """
    Тесты валидаторов видимости результата.
    """

    def test_result_visibility_rejects_guardian_without_learner(self) -> None:
        """
        Нельзя показать результат родителю, если он скрыт от ученика.
        """

        result = create_result(
            is_visible_to_learner=False,
            is_visible_to_guardian=True,
        )

        with self.assertRaises(ValidationError):
            validate_result_visibility(result=result)

    def test_visible_result_requires_grade(self) -> None:
        """
        Видимый результат должен иметь рассчитанную оценку.
        """

        result = create_result(
            is_visible_to_learner=True,
            average_grade=None,
            best_grade=None,
        )

        with self.assertRaises(ValidationError):
            validate_result_visibility(result=result)

    def test_result_blocking_rejects_block_before_third_attempt(self) -> None:
        """
        Нельзя блокировать прохождение раньше третьей попытки.
        """

        result = create_result(
            attempts_count=2,
            is_blocked=True,
        )

        with self.assertRaises(ValidationError):
            validate_result_blocking(result=result)
