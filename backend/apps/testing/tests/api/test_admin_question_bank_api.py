from __future__ import annotations

from apps.testing.constants import BankItemStatus
from apps.testing.tests.factories import (
    create_bank_item,
    create_bank_option,
    create_published_bank_item,
    create_superadmin,
    create_test,
    extract_results,
)
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AdminQuestionBankApiTestCase(APITestCase):
    """
    API-тесты банка тестовых заданий в административном пространстве.
    """

    def setUp(self) -> None:
        """
        Подготавливает базовые данные.
        """

        self.superadmin = create_superadmin()
        self.exam = create_test()
        self.bank_item = create_bank_item(
            organization=self.exam.organization,
            subject=self.exam.subject,
            owner_teacher=self.exam.owner_teacher,
        )

    def test_admin_can_get_bank_items_list(self) -> None:
        """
        Администратор получает список шаблонов вопросов.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.get(
            reverse("testing_admin:testing-admin-bank-items-list")
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        item_ids = {item["id"] for item in extract_results(response.json())}

        self.assertIn(self.bank_item.id, item_ids)

    def test_admin_can_create_bank_item(self) -> None:
        """
        Администратор создаёт шаблон вопроса.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse("testing_admin:testing-admin-bank-items-list"),
            {
                "title": "Админский шаблон",
                "text": "Выберите правильный ответ.",
                "question_type": "single_choice",
                "check_mode": "auto",
                "score": 1,
                "difficulty": "medium",
                "organization_id": self.exam.organization_id,
                "subject_id": self.exam.subject_id,
                "owner_teacher_id": self.exam.owner_teacher_id,
                "visibility": "private",
                "is_active": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["title"], "Админский шаблон")
        self.assertEqual(response.json()["status"], BankItemStatus.DRAFT)

    def test_admin_can_create_bank_option(self) -> None:
        """
        Администратор создаёт вариант ответа шаблона.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse("testing_admin:testing-admin-bank-options-list"),
            {
                "bank_item_id": self.bank_item.id,
                "text": "Ответ",
                "order": 1,
                "is_correct": True,
                "score": "1.00",
                "feedback": "",
                "is_active": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["bank_item"], self.bank_item.id)
        self.assertTrue(response.json()["is_correct"])

    def test_admin_can_publish_bank_item(self) -> None:
        """
        Администратор публикует шаблон вопроса.
        """

        create_bank_option(
            bank_item=self.bank_item,
            text="Верно",
            is_correct=True,
            score=1,
        )
        create_bank_option(
            bank_item=self.bank_item,
            text="Неверно",
            is_correct=False,
            score=0,
        )

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse(
                "testing_admin:testing-admin-bank-items-publish",
                args=[self.bank_item.id],
            ),
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["status"], BankItemStatus.PUBLISHED)

    def test_admin_can_archive_bank_item(self) -> None:
        """
        Администратор архивирует шаблон вопроса.
        """

        bank_item = create_published_bank_item(
            organization=self.exam.organization,
            subject=self.exam.subject,
            owner_teacher=self.exam.owner_teacher,
        )

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse(
                "testing_admin:testing-admin-bank-items-archive",
                args=[bank_item.id],
            ),
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["status"], BankItemStatus.ARCHIVED)

    def test_admin_can_restore_bank_item(self) -> None:
        """
        Администратор восстанавливает архивный шаблон вопроса.
        """

        bank_item = create_bank_item(
            organization=self.exam.organization,
            subject=self.exam.subject,
            owner_teacher=self.exam.owner_teacher,
            status=BankItemStatus.ARCHIVED,
            is_active=False,
        )

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse(
                "testing_admin:testing-admin-bank-items-restore",
                args=[bank_item.id],
            ),
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["status"], BankItemStatus.DRAFT)

    def test_admin_can_copy_bank_item_to_test(self) -> None:
        """
        Администратор копирует шаблон вопроса в тест.
        """

        bank_item = create_published_bank_item(
            organization=self.exam.organization,
            subject=self.exam.subject,
            owner_teacher=self.exam.owner_teacher,
        )

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse(
                "testing_admin:testing-admin-bank-items-copy-to-test",
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
