from __future__ import annotations

from apps.testing.constants import TestAttemptStatus, TestStatus
from apps.testing.tests.factories import (
    create_attempt,
    create_choice_question_with_options,
    create_course,
    create_course_enrollment,
    create_learner,
    create_result,
    create_test,
    create_visible_result,
    extract_results,
)
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class LearnerTestingApiTestCase(APITestCase):
    """
    API-тесты пространства обучающегося testing.
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

    def test_learner_can_get_available_tests_list(self) -> None:
        """
        Обучающийся видит опубликованный тест доступного курса.
        """

        hidden_exam = create_test(
            course=self.course,
            organization=self.course.organization,
            subject=self.course.subject,
            status=TestStatus.DRAFT,
            is_active=True,
        )

        self.client.force_authenticate(user=self.learner)

        response = self.client.get(
            reverse("testing_learner:testing-learner-tests-list")
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        test_ids = {item["id"] for item in extract_results(response.json())}

        self.assertIn(self.exam.id, test_ids)
        self.assertNotIn(hidden_exam.id, test_ids)

    def test_learner_can_start_attempt(self) -> None:
        """
        Обучающийся начинает попытку прохождения теста.
        """

        self.client.force_authenticate(user=self.learner)

        response = self.client.post(
            reverse("testing_learner:testing-learner-attempts-start"),
            {
                "test_id": self.exam.id,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["test"], self.exam.id)
        self.assertEqual(response.json()["learner"], self.learner.id)
        self.assertEqual(response.json()["attempt_number"], 1)
        self.assertEqual(response.json()["status"], TestAttemptStatus.STARTED)

    def test_learner_can_save_attempt_answers(self) -> None:
        """
        Обучающийся сохраняет ответы внутри своей попытки.
        """

        attempt = create_attempt(
            test=self.exam,
            learner=self.learner,
            status=TestAttemptStatus.STARTED,
        )

        self.client.force_authenticate(user=self.learner)

        response = self.client.post(
            reverse("testing_learner:testing-learner-answers-save-bulk"),
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

        response_data = response.json()

        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]["attempt"], attempt.id)
        self.assertEqual(response_data[0]["question"], self.question.id)
        self.assertEqual(
            response_data[0]["selected_option"],
            self.correct_option.id,
        )

    def test_learner_can_submit_attempt(self) -> None:
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
            reverse("testing_learner:testing-learner-answers-save-bulk"),
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
            reverse(
                "testing_learner:testing-learner-attempts-submit",
                args=[attempt.id],
            ),
            {
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
            },
        )

    def test_learner_does_not_see_hidden_result(self) -> None:
        """
        Обучающийся не видит результат до публикации.
        """

        create_result(
            test=self.exam,
            learner=self.learner,
            average_score=80,
            average_grade=4,
            best_score=80,
            best_grade=4,
            is_visible_to_learner=False,
            is_visible_to_guardian=False,
        )

        self.client.force_authenticate(user=self.learner)

        response = self.client.get(
            reverse("testing_learner:testing-learner-results-list")
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(extract_results(response.json()), [])

    def test_learner_can_see_visible_result(self) -> None:
        """
        Обучающийся видит опубликованный итоговый результат.
        """

        result = create_visible_result(
            test=self.exam,
            learner=self.learner,
        )

        self.client.force_authenticate(user=self.learner)

        response = self.client.get(
            reverse("testing_learner:testing-learner-results-list")
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result_ids = {item["id"] for item in extract_results(response.json())}

        self.assertIn(result.id, result_ids)

    def test_learner_cannot_save_answers_for_foreign_attempt(self) -> None:
        """
        Обучающийся не может сохранять ответы в чужую попытку.
        """

        foreign_attempt = create_attempt(
            test=self.exam,
            learner=self.foreign_learner,
            status=TestAttemptStatus.STARTED,
        )

        self.client.force_authenticate(user=self.learner)

        response = self.client.post(
            reverse("testing_learner:testing-learner-answers-save-bulk"),
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

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_learner_cannot_see_foreign_result(self) -> None:
        """
        Обучающийся не видит результат другого обучающегося.
        """

        foreign_result = create_visible_result(
            test=self.exam,
            learner=self.foreign_learner,
        )

        self.client.force_authenticate(user=self.learner)

        response = self.client.get(
            reverse("testing_learner:testing-learner-results-list")
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result_ids = {item["id"] for item in extract_results(response.json())}

        self.assertNotIn(foreign_result.id, result_ids)
