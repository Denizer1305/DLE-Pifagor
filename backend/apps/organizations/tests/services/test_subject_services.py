from __future__ import annotations

from apps.organizations.services import (
    create_subject,
    deactivate_subject,
    restore_subject,
    update_subject,
)
from apps.organizations.tests.factories import (
    create_subject as create_test_subject,
)
from apps.organizations.tests.factories import (
    create_superadmin,
    create_test_user,
)
from django.test import TestCase
from rest_framework.exceptions import PermissionDenied, ValidationError


class SubjectServicesTestCase(TestCase):
    """
    Тесты сервисов учебных предметов.
    """

    def setUp(self) -> None:
        self.superadmin = create_superadmin(
            email="superadmin-subject-services@example.com",
            phone="+79998200001",
        )
        self.regular_user = create_test_user(
            email="regular-subject-services@example.com",
            phone="+79998200002",
        )
        self.subject = create_test_subject(
            name="Математика",
            short_name="Математика",
            code="math",
            is_active=True,
        )

    def test_superadmin_can_create_subject(self) -> None:
        """
        Суперадмин может создать учебный предмет.
        """

        subject = create_subject(
            actor=self.superadmin,
            data={
                "name": "Физика",
                "short_name": "Физика",
                "code": "physics",
                "description": "Учебный предмет.",
            },
        )

        self.assertEqual(subject.name, "Физика")
        self.assertEqual(subject.code, "physics")
        self.assertTrue(subject.is_active)

    def test_regular_user_cannot_create_subject(self) -> None:
        """
        Обычный пользователь не может создать учебный предмет.
        """

        with self.assertRaises(PermissionDenied):
            create_subject(
                actor=self.regular_user,
                data={
                    "name": "История",
                    "code": "history",
                },
            )

    def test_superadmin_can_update_subject(self) -> None:
        """
        Суперадмин может обновить учебный предмет.
        """

        subject = update_subject(
            actor=self.superadmin,
            subject=self.subject,
            data={
                "short_name": "Мат.",
                "description": "Обновлённое описание.",
            },
        )

        self.assertEqual(subject.short_name, "Мат.")
        self.assertEqual(subject.description, "Обновлённое описание.")

    def test_regular_user_cannot_update_subject(self) -> None:
        """
        Обычный пользователь не может обновить учебный предмет.
        """

        with self.assertRaises(PermissionDenied):
            update_subject(
                actor=self.regular_user,
                subject=self.subject,
                data={
                    "short_name": "Нет доступа",
                },
            )

    def test_deactivate_subject(self) -> None:
        """
        Сервис деактивирует учебный предмет.
        """

        subject = deactivate_subject(
            actor=self.superadmin,
            subject=self.subject,
        )

        self.assertFalse(subject.is_active)

    def test_deactivate_inactive_subject_raises_error(self) -> None:
        """
        Повторная деактивация предмета возвращает ошибку.
        """

        self.subject.is_active = False
        self.subject.save(update_fields=["is_active"])

        with self.assertRaises(ValidationError):
            deactivate_subject(
                actor=self.superadmin,
                subject=self.subject,
            )

    def test_restore_subject(self) -> None:
        """
        Сервис восстанавливает учебный предмет.
        """

        self.subject.is_active = False
        self.subject.save(update_fields=["is_active"])

        subject = restore_subject(
            actor=self.superadmin,
            subject=self.subject,
        )

        self.assertTrue(subject.is_active)

    def test_restore_active_subject_raises_error(self) -> None:
        """
        Повторное восстановление активного предмета возвращает ошибку.
        """

        with self.assertRaises(ValidationError):
            restore_subject(
                actor=self.superadmin,
                subject=self.subject,
            )