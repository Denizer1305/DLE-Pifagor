from __future__ import annotations

from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.testing.constants import (
    AttemptCheckStatus,
    TestAttemptStatus,
)
from apps.testing.tests.factories import (
    create_answer,
    create_attempt,
    create_choice_question_with_options,
    create_teacher,
    create_test,
)


class TeacherReviewApiTestCase(APITestCase):
    """
    API-тесты очереди проверки и summary преподавателя.
    """

    def setUp(self) -> None:
        """
        Подготавливает базовые данные.
        """

        self.teacher = create_teacher()
        self.foreign_teacher = create_teacher()

        self.exam = create_test(owner_teacher=self.teacher)
        self.foreign_exam = create_test(owner_teacher=self.foreign_teacher)

    def test_teacher_can_get_review_queue(self) -> None:
        """
        Преподаватель получает очередь проверки своих тестов.
        """

        attempt = create_attempt(
            test=self.exam,
            status=TestAttemptStatus.NEEDS_REVIEW,
            check_status=AttemptCheckStatus.NEEDS_REVIEW,
            requires_manual_review=True,
        )
        foreign_attempt = create_attempt(
            test=self.foreign_exam,
            status=TestAttemptStatus.NEEDS_REVIEW,
            check_status=AttemptCheckStatus.NEEDS_REVIEW,
            requires_manual_review=True,
        )

        self.client.force_authenticate(user=self.teacher)

        response = self.client.get(
            reverse("testing_teacher:testing-teacher-review-queue")
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        attempt_ids = {
            item["id"]
            for item in response.json()
        }

        self.assertIn(attempt.id, attempt_ids)
        self.assertNotIn(foreign_attempt.id, attempt_ids)

    def test_teacher_can_filter_review_queue_by_test(self) -> None:
        """
        Преподаватель фильтрует очередь проверки по тесту.
        """

        attempt = create_attempt(
            test=self.exam,
            status=TestAttemptStatus.NEEDS_REVIEW,
            check_status=AttemptCheckStatus.NEEDS_REVIEW,
            requires_manual_review=True,
        )
        another_exam = create_test(owner_teacher=self.teacher)
        another_attempt = create_attempt(
            test=another_exam,
            status=TestAttemptStatus.NEEDS_REVIEW,
            check_status=AttemptCheckStatus.NEEDS_REVIEW,
            requires_manual_review=True,
        )

        self.client.force_authenticate(user=self.teacher)

        response = self.client.get(
            reverse("testing_teacher:testing-teacher-review-queue"),
            {
                "test_id": self.exam.id,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        attempt_ids = {
            item["id"]
            for item in response.json()
        }

        self.assertIn(attempt.id, attempt_ids)
        self.assertNotIn(another_attempt.id, attempt_ids)

    def test_teacher_can_get_teacher_summary(self) -> None:
        """
        Преподаватель получает общую сводку по своим тестам.
        """

        create_attempt(
            test=self.exam,
            status=TestAttemptStatus.NEEDS_REVIEW,
            check_status=AttemptCheckStatus.NEEDS_REVIEW,
            requires_manual_review=True,
        )

        self.client.force_authenticate(user=self.teacher)

        response = self.client.get(
            reverse("testing_teacher:testing-teacher-review-teacher-summary")
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("attempts_count", response.json())
        self.assertIn("needs_review_count", response.json())
        self.assertEqual(response.json()["needs_review_count"], 1)

    def test_teacher_can_get_test_summary(self) -> None:
        """
        Преподаватель получает сводку по конкретному тесту.
        """

        create_attempt(
            test=self.exam,
            status=TestAttemptStatus.CONFIRMED,
            final_score=Decimal("80"),
            final_grade=4,
        )

        self.client.force_authenticate(user=self.teacher)

        response = self.client.get(
            reverse("testing_teacher:testing-teacher-review-test-summary"),
            {
                "test_id": self.exam.id,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("attempts_count", response.json())
        self.assertIn("confirmed_count", response.json())
        self.assertEqual(response.json()["confirmed_count"], 1)

    def test_teacher_can_recalculate_attempt_score(self) -> None:
        """
        Преподаватель пересчитывает баллы попытки по ответам.
        """

        attempt = create_attempt(
            test=self.exam,
            status=TestAttemptStatus.NEEDS_REVIEW,
            check_status=AttemptCheckStatus.NEEDS_REVIEW,
        )

        first_question = create_choice_question_with_options(
            test=self.exam,
            score=50,
        )
        second_question = create_choice_question_with_options(
            test=self.exam,
            score=50,
        )

        create_answer(
            attempt=attempt,
            question=first_question,
            final_score=Decimal("40"),
            requires_manual_review=False,
        )
        create_answer(
            attempt=attempt,
            question=second_question,
            final_score=Decimal("45"),
            requires_manual_review=False,
        )

        self.client.force_authenticate(user=self.teacher)

        response = self.client.post(
            reverse(
                "testing_teacher:"
                "testing-teacher-review-recalculate-attempt"
            ),
            {
                "attempt_id": attempt.id,
                "confirm": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["final_score"], "85.00")
        self.assertEqual(response.json()["final_grade"], 5)

    def test_teacher_cannot_recalculate_foreign_attempt(self) -> None:
        """
        Преподаватель не пересчитывает чужую попытку.
        """

        attempt = create_attempt(
            test=self.foreign_exam,
            status=TestAttemptStatus.NEEDS_REVIEW,
            check_status=AttemptCheckStatus.NEEDS_REVIEW,
        )

        self.client.force_authenticate(user=self.teacher)

        response = self.client.post(
            reverse(
                "testing_teacher:"
                "testing-teacher-review-recalculate-attempt"
            ),
            {
                "attempt_id": attempt.id,
                "confirm": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)