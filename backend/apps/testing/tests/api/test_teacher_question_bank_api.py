from __future__ import annotations

from apps.testing.constants import BankItemStatus
from apps.testing.tests.factories import (
    create_bank_item,
    create_bank_option,
    create_published_bank_item,
    create_teacher,
    create_test,
    extract_results,
)
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TeacherQuestionBankApiTestCase(APITestCase):
    """
    API-тесты банка тестовых заданий в пространстве преподавателя.
    """

    def setUp(self) -> None:
        """
        Подготавливает базовые данные.
        """

        self.teacher = create_teacher()
        self.foreign_teacher = create_teacher()

        self.exam = create_test(owner_teacher=self.teacher)
        self.foreign_exam = create_test(owner_teacher=self.foreign_teacher)

        self.bank_item = create_bank_item(
            organization=self.exam.organization,
            subject=self.exam.subject,
            owner_teacher=self.teacher,
        )
        self.foreign_bank_item = create_bank_item(
            organization=self.foreign_exam.organization,
            subject=self.foreign_exam.subject,
            owner_teacher=self.foreign_teacher,
        )

    def test_teacher_can_get_own_bank_items_list(self) -> None:
        """
        Преподаватель видит свои шаблоны вопросов.
        """

        self.client.force_authenticate(user=self.teacher)

        response = self.client.get(
            reverse("testing_teacher:testing-teacher-bank-items-list")
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        item_ids = {item["id"] for item in extract_results(response.json())}

        self.assertIn(self.bank_item.id, item_ids)
        self.assertNotIn(self.foreign_bank_item.id, item_ids)

    def test_teacher_can_create_bank_item(self) -> None:
        """
        Преподаватель создаёт шаблон вопроса.
        """

        self.client.force_authenticate(user=self.teacher)

        response = self.client.post(
            reverse("testing_teacher:testing-teacher-bank-items-list"),
            {
                "title": "Шаблон вопроса",
                "text": "Сколько будет 2 + 2?",
                "question_type": "single_choice",
                "check_mode": "auto",
                "score": 1,
                "difficulty": "medium",
                "organization_id": self.exam.organization_id,
                "subject_id": self.exam.subject_id,
                "visibility": "private",
                "is_active": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["title"], "Шаблон вопроса")
        self.assertEqual(response.json()["status"], BankItemStatus.DRAFT)
        self.assertEqual(response.json()["owner_teacher"], self.teacher.id)

    def test_teacher_can_create_bank_option_for_own_item(self) -> None:
        """
        Преподаватель создаёт вариант ответа для своего шаблона.
        """

        self.client.force_authenticate(user=self.teacher)

        response = self.client.post(
            reverse("testing_teacher:testing-teacher-bank-options-list"),
            {
                "bank_item_id": self.bank_item.id,
                "text": "4",
                "order": 1,
                "is_correct": True,
                "score": "1.00",
                "feedback": "Верно.",
                "is_active": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["bank_item"], self.bank_item.id)
        self.assertEqual(response.json()["text"], "4")
        self.assertTrue(response.json()["is_correct"])

    def test_teacher_can_publish_own_bank_item(self) -> None:
        """
        Преподаватель публикует свой шаблон вопроса.
        """

        create_bank_option(
            bank_item=self.bank_item,
            text="4",
            is_correct=True,
            score=1,
        )
        create_bank_option(
            bank_item=self.bank_item,
            text="5",
            is_correct=False,
            score=0,
        )

        self.client.force_authenticate(user=self.teacher)

        response = self.client.post(
            reverse(
                "testing_teacher:testing-teacher-bank-items-publish",
                args=[self.bank_item.id],
            ),
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["status"], BankItemStatus.PUBLISHED)

        self.bank_item.refresh_from_db()

        self.assertEqual(self.bank_item.status, BankItemStatus.PUBLISHED)
        self.assertTrue(self.bank_item.is_active)

    def test_teacher_can_duplicate_own_bank_item(self) -> None:
        """
        Преподаватель создаёт копию своего шаблона.
        """

        create_bank_option(
            bank_item=self.bank_item,
            text="4",
            is_correct=True,
            score=1,
        )

        self.client.force_authenticate(user=self.teacher)

        response = self.client.post(
            reverse(
                "testing_teacher:testing-teacher-bank-items-duplicate",
                args=[self.bank_item.id],
            ),
            {
                "title": "Копия шаблона",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["title"], "Копия шаблона")
        self.assertEqual(response.json()["status"], BankItemStatus.DRAFT)
        self.assertNotEqual(response.json()["id"], self.bank_item.id)

    def test_teacher_can_copy_published_bank_item_to_own_test(self) -> None:
        """
        Преподаватель копирует опубликованный шаблон в свой тест.
        """

        bank_item = create_published_bank_item(
            organization=self.exam.organization,
            subject=self.exam.subject,
            owner_teacher=self.teacher,
        )

        self.client.force_authenticate(user=self.teacher)

        response = self.client.post(
            reverse(
                "testing_teacher:testing-teacher-bank-items-copy-to-test",
                args=[bank_item.id],
            ),
            {
                "test_id": self.exam.id,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["test"], self.exam.id)
        self.assertEqual(response.json()["source_bank_item"], bank_item.id)

    def test_teacher_cannot_update_foreign_bank_item(self) -> None:
        """
        Преподаватель не изменяет чужой шаблон вопроса.
        """

        self.client.force_authenticate(user=self.teacher)

        response = self.client.patch(
            reverse(
                "testing_teacher:testing-teacher-bank-items-detail",
                args=[self.foreign_bank_item.id],
            ),
            {
                "title": "Попытка изменения",
            },
            format="json",
        )

        self.assertIn(
            response.status_code,
            {
                status.HTTP_403_FORBIDDEN,
                status.HTTP_404_NOT_FOUND,
            },
        )
