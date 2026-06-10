from __future__ import annotations

from decimal import Decimal

from apps.testing.constants import LearnerResultStatus, TestAttemptStatus
from apps.testing.services import (
    hide_learner_result,
    publish_attempt_result,
    publish_learner_result,
    recalculate_learner_result,
)
from apps.testing.tests.factories import (
    create_attempt,
    create_learner,
    create_result,
    create_test,
)
from django.test import TestCase


class TestResultServicesTestCase(TestCase):
    """
    Тесты сервисов итоговых результатов.
    """

    def test_recalculate_learner_result_counts_average_grade(self) -> None:
        """
        Сервис считает среднюю оценку по подтверждённым попыткам.
        """

        exam = create_test(max_attempts=3)
        learner = create_learner()

        create_attempt(
            test=exam,
            learner=learner,
            attempt_number=1,
            status=TestAttemptStatus.CONFIRMED,
            is_confirmed_by_teacher=True,
            final_score=Decimal("70"),
            final_grade=4,
        )
        create_attempt(
            test=exam,
            learner=learner,
            attempt_number=2,
            status=TestAttemptStatus.CONFIRMED,
            is_confirmed_by_teacher=True,
            final_score=Decimal("90"),
            final_grade=5,
        )

        result = recalculate_learner_result(
            test=exam,
            learner=learner,
        )

        self.assertEqual(result.confirmed_attempts_count, 2)
        self.assertEqual(result.average_score, Decimal("80.00"))
        self.assertEqual(result.average_grade, Decimal("4.50"))
        self.assertEqual(result.best_grade, 5)

    def test_recalculate_learner_result_blocks_after_three_attempts(self) -> None:
        """
        После трёх попыток повторное прохождение блокируется.
        """

        exam = create_test(max_attempts=3)
        learner = create_learner()

        for attempt_number in range(1, 4):
            create_attempt(
                test=exam,
                learner=learner,
                attempt_number=attempt_number,
                status=TestAttemptStatus.CONFIRMED,
                is_confirmed_by_teacher=True,
                final_score=Decimal("80"),
                final_grade=4,
            )

        result = recalculate_learner_result(
            test=exam,
            learner=learner,
        )

        self.assertEqual(result.attempts_count, 3)
        self.assertTrue(result.is_blocked)
        self.assertEqual(result.status, LearnerResultStatus.BLOCKED)

    def test_publish_attempt_result_makes_attempt_visible(self) -> None:
        """
        Публикация результата показывает попытку ученику и родителю.
        """

        attempt = create_attempt(
            status=TestAttemptStatus.CONFIRMED,
            is_confirmed_by_teacher=True,
            final_score=Decimal("80"),
            final_grade=4,
        )

        published_attempt = publish_attempt_result(attempt=attempt)

        self.assertEqual(
            published_attempt.status,
            TestAttemptStatus.PUBLISHED,
        )
        self.assertTrue(published_attempt.is_visible_to_learner)
        self.assertTrue(published_attempt.is_visible_to_guardian)

    def test_publish_and_hide_learner_result_change_visibility(self) -> None:
        """
        Сервисы публикации и скрытия результата меняют видимость.
        """

        result = create_result(
            average_grade=4,
            best_grade=4,
        )

        publish_learner_result(result=result)
        result.refresh_from_db()

        self.assertTrue(result.is_visible_to_learner)
        self.assertTrue(result.is_visible_to_guardian)

        hide_learner_result(result=result)
        result.refresh_from_db()

        self.assertFalse(result.is_visible_to_learner)
        self.assertFalse(result.is_visible_to_guardian)
