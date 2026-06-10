from __future__ import annotations

from apps.testing.constants import TestAttemptStatus
from apps.testing.tests.factories import create_attempt, create_learner, create_test
from apps.testing.validators import (
    validate_attempt_can_be_cancelled,
    validate_attempt_can_be_confirmed,
    validate_attempt_can_be_published,
    validate_attempt_can_be_submitted,
    validate_attempt_limit,
    validate_attempt_number,
    validate_confirmation_values,
    validate_no_active_attempt,
)
from django.core.exceptions import ValidationError
from django.test import TestCase


class TestAttemptLifecycleValidatorsTestCase(TestCase):
    """
    Тесты валидаторов жизненного цикла попытки.
    """

    def test_started_attempt_can_be_submitted(self) -> None:
        """
        Начатую попытку можно отправить.
        """

        attempt = create_attempt(status=TestAttemptStatus.STARTED)

        validate_attempt_can_be_submitted(attempt=attempt)

    def test_published_attempt_cannot_be_cancelled(self) -> None:
        """
        Опубликованную попытку нельзя отменить.
        """

        attempt = create_attempt(status=TestAttemptStatus.PUBLISHED)

        with self.assertRaises(ValidationError):
            validate_attempt_can_be_cancelled(attempt=attempt)

    def test_auto_checked_attempt_can_be_confirmed(self) -> None:
        """
        Автоматически проверенную попытку можно подтвердить.
        """

        attempt = create_attempt(status=TestAttemptStatus.AUTO_CHECKED)

        validate_attempt_can_be_confirmed(attempt=attempt)

    def test_started_attempt_cannot_be_confirmed(self) -> None:
        """
        Начатую попытку нельзя подтвердить.
        """

        attempt = create_attempt(status=TestAttemptStatus.STARTED)

        with self.assertRaises(ValidationError):
            validate_attempt_can_be_confirmed(attempt=attempt)


class TestAttemptLimitValidatorsTestCase(TestCase):
    """
    Тесты валидаторов лимита попыток.
    """

    def test_validate_attempt_limit_allows_less_than_limit(self) -> None:
        """
        Валидатор пропускает обучающегося с доступными попытками.
        """

        exam = create_test(max_attempts=3)
        learner = create_learner()

        create_attempt(test=exam, learner=learner)

        validate_attempt_limit(
            test=exam,
            learner=learner,
        )

    def test_validate_attempt_limit_rejects_after_three_attempts(self) -> None:
        """
        Валидатор запрещает новую попытку после лимита.
        """

        exam = create_test(max_attempts=3)
        learner = create_learner()

        create_attempt(test=exam, learner=learner, attempt_number=1)
        create_attempt(test=exam, learner=learner, attempt_number=2)
        create_attempt(test=exam, learner=learner, attempt_number=3)

        with self.assertRaises(ValidationError):
            validate_attempt_limit(
                test=exam,
                learner=learner,
            )

    def test_validate_no_active_attempt_rejects_started_attempt(self) -> None:
        """
        Нельзя создать новую попытку при незавершённой активной.
        """

        exam = create_test()
        learner = create_learner()

        create_attempt(
            test=exam,
            learner=learner,
            status=TestAttemptStatus.STARTED,
        )

        with self.assertRaises(ValidationError):
            validate_no_active_attempt(
                test=exam,
                learner=learner,
            )


class TestAttemptConfirmationValidatorsTestCase(TestCase):
    """
    Тесты валидаторов подтверждения результата.
    """

    def test_validate_attempt_number_rejects_number_above_limit(self) -> None:
        """
        Номер попытки не может превышать лимит теста.
        """

        exam = create_test(max_attempts=3)

        with self.assertRaises(ValidationError):
            validate_attempt_number(
                attempt_number=4,
                test=exam,
            )

    def test_validate_confirmation_values_allows_valid_values(self) -> None:
        """
        Валидатор пропускает корректные итоговые значения.
        """

        validate_confirmation_values(
            final_score=80,
            final_grade=4,
            max_score=100,
        )

    def test_validate_confirmation_values_rejects_invalid_grade(self) -> None:
        """
        Итоговая оценка должна быть от 2 до 5.
        """

        with self.assertRaises(ValidationError):
            validate_confirmation_values(
                final_score=80,
                final_grade=6,
                max_score=100,
            )

    def test_unconfirmed_attempt_cannot_be_published(self) -> None:
        """
        Неподтверждённую попытку нельзя опубликовать.
        """

        attempt = create_attempt(
            status=TestAttemptStatus.AUTO_CHECKED,
            is_confirmed_by_teacher=False,
        )

        with self.assertRaises(ValidationError):
            validate_attempt_can_be_published(attempt=attempt)
