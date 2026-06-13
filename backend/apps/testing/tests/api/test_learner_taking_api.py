from __future__ import annotations

from apps.testing.constants import TestAttemptStatus, TestStatus
from apps.testing.tests.factories import (
    create_attempt,
    create_choice_question_with_options,
    create_course,
    create_course_enrollment,
    create_learner,
    create_test,
)
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class LearnerTakingApiTestCase(APITestCase):
    """
    API-тесты безопасного прохождения теста обучающимся.
    """

    def setUp(self) -> None:
        """
        Подготавливает базовые данные.
        """

        self.learner = create_learner()
        self.foreign_learner = create_learner()

        self.course = create_course()
        self.exam = create_test(
            course=self.course,
            organization=self.course.organization,
            subject=self.course.subject,
            status=TestStatus.PUBLISHED,
            is_active=True,
        )

        self.question = create_choice_question_with_options(
            test=self.exam,
            score=10,
        )
        self.correct_option = self.question.options.filter(
            is_correct=True,
        ).first()

        create_course_enrollment(
            course=self.course,
            learner=self.learner,
        )

    def test_learner_can_start_taking_attempt(self) -> None:
        """
        Обучающийся начинает прохождение теста.
        """

        self.client.force_authenticate(user=self.learner)

        response = self.client.post(
            reverse("testing_learner:testing-learner-taking-start"),
            {
                "test_id": self.exam.id,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()

        self.assertEqual(response_data["test"]["id"], self.exam.id)
        self.assertEqual(response_data["attempt"]["attempt_number"], 1)
        self.assertEqual(
            response_data["attempt"]["status"],
            TestAttemptStatus.STARTED,
        )
        self.assertEqual(len(response_data["questions"]), 1)

    def test_taking_payload_does_not_leak_correct_answers(self) -> None:
        """
        Payload прохождения не отдаёт правильные ответы.
        """

        self.client.force_authenticate(user=self.learner)

        response = self.client.post(
            reverse("testing_learner:testing-learner-taking-start"),
            {
                "test_id": self.exam.id,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        question_payload = response.json()["questions"][0]
        option_payload = question_payload["options"][0]

        self.assertNotIn("expected_text_answer", question_payload)
        self.assertNotIn("expected_number_answer", question_payload)
        self.assertNotIn("source_bank_item", question_payload)
        self.assertNotIn("is_correct", option_payload)
        self.assertNotIn("score", option_payload)
        self.assertNotIn("feedback", option_payload)

    def test_learner_can_get_active_taking_attempt(self) -> None:
        """
        Обучающийся получает активную попытку прохождения.
        """

        attempt = create_attempt(
            test=self.exam,
            learner=self.learner,
            status=TestAttemptStatus.STARTED,
        )

        self.client.force_authenticate(user=self.learner)

        response = self.client.get(
            reverse("testing_learner:testing-learner-taking-active"),
            {
                "test_id": self.exam.id,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["attempt"]["id"], attempt.id)

    def test_learner_can_save_taking_answers(self) -> None:
        """
        Обучающийся сохраняет ответы в своей попытке.
        """

        attempt = create_attempt(
            test=self.exam,
            learner=self.learner,
            status=TestAttemptStatus.STARTED,
        )

        self.client.force_authenticate(user=self.learner)

        response = self.client.post(
            reverse("testing_learner:testing-learner-taking-save-answers"),
            {
                "attempt_id": attempt.id,
                "answers": [
                    {
                        "question_id": self.question.id,
                        "selected_option_id": self.correct_option.id,
                    }
                ],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["saved_count"], 1)
        self.assertEqual(attempt.answers.count(), 1)

    def test_learner_can_submit_taking_attempt(self) -> None:
        """
        Обучающийся отправляет попытку на проверку.
        """

        attempt = create_attempt(
            test=self.exam,
            learner=self.learner,
            status=TestAttemptStatus.STARTED,
        )

        self.client.force_authenticate(user=self.learner)

        self.client.post(
            reverse("testing_learner:testing-learner-taking-save-answers"),
            {
                "attempt_id": attempt.id,
                "answers": [
                    {
                        "question_id": self.question.id,
                        "selected_option_id": self.correct_option.id,
                    }
                ],
            },
            format="json",
        )

        response = self.client.post(
            reverse("testing_learner:testing-learner-taking-submit"),
            {
                "attempt_id": attempt.id,
                "confirm": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(
            response.json()["status"],
            {
                TestAttemptStatus.AUTO_CHECKED,
                TestAttemptStatus.NEEDS_REVIEW,
                TestAttemptStatus.SUBMITTED,
            },
        )

    def test_learner_cannot_start_unavailable_test(self) -> None:
        """
        Обучающийся не начинает черновой тест.
        """

        draft_exam = create_test(
            course=self.course,
            organization=self.course.organization,
            subject=self.course.subject,
            status=TestStatus.DRAFT,
            is_active=True,
        )

        self.client.force_authenticate(user=self.learner)

        response = self.client.post(
            reverse("testing_learner:testing-learner-taking-start"),
            {
                "test_id": draft_exam.id,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_learner_cannot_save_answers_for_foreign_attempt(self) -> None:
        """
        Обучающийся не сохраняет ответы в чужую попытку.
        """

        foreign_attempt = create_attempt(
            test=self.exam,
            learner=self.foreign_learner,
            status=TestAttemptStatus.STARTED,
        )

        self.client.force_authenticate(user=self.learner)

        response = self.client.post(
            reverse("testing_learner:testing-learner-taking-save-answers"),
            {
                "attempt_id": foreign_attempt.id,
                "answers": [
                    {
                        "question_id": self.question.id,
                        "selected_option_id": self.correct_option.id,
                    }
                ],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
