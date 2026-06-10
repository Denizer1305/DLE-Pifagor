from __future__ import annotations

from apps.testing.constants import TestAttemptStatus
from apps.testing.tests.factories import (
    create_attempt,
    create_choice_question_with_options,
    create_course,
    create_option,
    create_question,
    create_teacher,
    create_test,
    extract_results,
)
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TeacherTestingApiTestCase(APITestCase):
    """
    API-тесты пространства преподавателя testing.
    """

    def setUp(self) -> None:
        """
        Подготавливает базовые данные.
        """

        self.teacher = create_teacher()
        self.foreign_teacher = create_teacher()

        self.course = create_course(owner_teacher=self.teacher)
        self.exam = create_test(
            course=self.course,
            organization=self.course.organization,
            subject=self.course.subject,
            owner_teacher=self.teacher,
        )

        self.foreign_course = create_course(
            owner_teacher=self.foreign_teacher,
        )
        self.foreign_exam = create_test(
            course=self.foreign_course,
            organization=self.foreign_course.organization,
            subject=self.foreign_course.subject,
            owner_teacher=self.foreign_teacher,
        )

    def test_teacher_can_get_own_tests_list(self) -> None:
        """
        Преподаватель видит только свои тесты.
        """

        self.client.force_authenticate(user=self.teacher)

        response = self.client.get(
            reverse("testing_teacher:testing-teacher-tests-list")
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        test_ids = {item["id"] for item in extract_results(response.json())}

        self.assertIn(self.exam.id, test_ids)
        self.assertNotIn(self.foreign_exam.id, test_ids)

    def test_teacher_can_create_question_for_own_test(self) -> None:
        """
        Преподаватель создаёт вопрос для своего теста.
        """

        self.client.force_authenticate(user=self.teacher)

        response = self.client.post(
            reverse("testing_teacher:testing-teacher-questions-list"),
            {
                "test_id": self.exam.id,
                "title": "Вопрос 1",
                "text": "Сколько будет 2 + 2?",
                "order": 1,
                "score": 1,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["test"], self.exam.id)
        self.assertEqual(response.json()["title"], "Вопрос 1")

    def test_teacher_can_create_option_for_own_question(self) -> None:
        """
        Преподаватель создаёт вариант ответа.
        """

        question = create_question(test=self.exam)

        self.client.force_authenticate(user=self.teacher)

        response = self.client.post(
            reverse("testing_teacher:testing-teacher-options-list"),
            {
                "question_id": question.id,
                "text": "4",
                "order": 1,
                "is_correct": True,
                "score": 1,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["question"], question.id)
        self.assertEqual(response.json()["text"], "4")
        self.assertTrue(response.json()["is_correct"])

    def test_teacher_can_confirm_attempt_result(self) -> None:
        """
        Преподаватель подтверждает результат попытки.
        """

        attempt = create_attempt(
            test=self.exam,
            status=TestAttemptStatus.AUTO_CHECKED,
            auto_score=80,
            auto_grade=4,
        )

        self.client.force_authenticate(user=self.teacher)

        response = self.client.post(
            reverse(
                "testing_teacher:testing-teacher-attempts-confirm-result",
                args=[attempt.id],
            ),
            {
                "final_score": "80.00",
                "final_grade": 4,
                "teacher_comment": "Оценка подтверждена.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["status"], TestAttemptStatus.CONFIRMED)
        self.assertEqual(response.json()["final_grade"], 4)
        self.assertTrue(response.json()["is_confirmed_by_teacher"])

    def test_teacher_can_get_integrity_report(self) -> None:
        """
        Преподаватель получает отчёт о признаках возможного списывания.
        """

        attempt = create_attempt(test=self.exam)
        question = create_choice_question_with_options(test=self.exam)
        option = question.options.filter(is_correct=True).first()

        create_option(
            question=question,
            text="Дополнительный вариант",
            is_correct=False,
        )

        from apps.testing.tests.factories import create_answer

        create_answer(
            attempt=attempt,
            question=question,
            selected_option=option,
        )

        self.client.force_authenticate(user=self.teacher)

        response = self.client.get(
            reverse(
                "testing_teacher:testing-teacher-attempts-integrity-report",
                args=[attempt.id],
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("risk_level", response.json())
        self.assertIn("score", response.json())
        self.assertIn("flags", response.json())

    def test_teacher_cannot_confirm_foreign_attempt_result(self) -> None:
        """
        Преподаватель не подтверждает попытку чужого теста.
        """

        attempt = create_attempt(
            test=self.foreign_exam,
            status=TestAttemptStatus.AUTO_CHECKED,
            auto_score=80,
            auto_grade=4,
        )

        self.client.force_authenticate(user=self.teacher)

        response = self.client.post(
            reverse(
                "testing_teacher:testing-teacher-attempts-confirm-result",
                args=[attempt.id],
            ),
            {
                "final_score": "80.00",
                "final_grade": 4,
                "teacher_comment": "Попытка подтверждения.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
