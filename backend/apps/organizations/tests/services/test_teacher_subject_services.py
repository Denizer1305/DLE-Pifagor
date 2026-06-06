from __future__ import annotations

from apps.organizations.models import TeacherSubject
from apps.organizations.services import (
    assign_subject_to_teacher,
    deactivate_teacher_subject,
    restore_teacher_subject,
    set_primary_teacher_subject,
    update_teacher_subject,
)
from apps.organizations.tests.factories import (
    create_organization,
    create_subject,
    create_superadmin,
    create_teacher,
    create_teacher_subject,
    create_test_user,
)
from django.test import TestCase
from rest_framework.exceptions import PermissionDenied, ValidationError


class TeacherSubjectServicesTestCase(TestCase):
    """
    Тесты сервисов предметов преподавателей.
    """

    def setUp(self) -> None:
        self.superadmin = create_superadmin(
            email="superadmin-teacher-subject-services@example.com",
            phone="+79998300001",
        )
        self.regular_user = create_test_user(
            email="regular-teacher-subject-services@example.com",
            phone="+79998300002",
        )

        self.organization = create_organization(
            name="Организация предметов преподавателей",
            short_name="Предметы",
            code="teacher_subject_services_org",
            slug="teacher-subject-services-org",
        )

        self.teacher = create_teacher(
            organization=self.organization,
            email="teacher-subject-services@example.com",
            phone="+79998300003",
            first_name="Иван",
            last_name="Иванов",
            position="Преподаватель",
        )
        self.second_teacher = create_teacher(
            organization=self.organization,
            email="second-teacher-subject-services@example.com",
            phone="+79998300004",
            first_name="Пётр",
            last_name="Петров",
            position="Преподаватель",
        )

        self.math = create_subject(
            name="Математика",
            short_name="Математика",
            code="math",
            is_active=True,
        )
        self.physics = create_subject(
            name="Физика",
            short_name="Физика",
            code="physics",
            is_active=True,
        )

        self.teacher_subject = create_teacher_subject(
            teacher=self.teacher,
            subject=self.math,
            is_primary=True,
            is_active=True,
        )

    def test_assign_subject_to_teacher(self) -> None:
        """
        Сервис назначает предмет преподавателю.
        """

        teacher_subject = assign_subject_to_teacher(
            actor=self.superadmin,
            teacher=self.second_teacher,
            subject=self.physics,
            data={
                "is_primary": True,
                "notes": "Назначено сервисом.",
            },
        )

        self.assertEqual(teacher_subject.teacher, self.second_teacher)
        self.assertEqual(teacher_subject.subject, self.physics)
        self.assertTrue(teacher_subject.is_primary)
        self.assertEqual(teacher_subject.notes, "Назначено сервисом.")

    def test_regular_user_cannot_assign_subject_to_teacher(self) -> None:
        """
        Обычный пользователь не может назначить предмет преподавателю.
        """

        with self.assertRaises(PermissionDenied):
            assign_subject_to_teacher(
                actor=self.regular_user,
                teacher=self.second_teacher,
                subject=self.physics,
                data={
                    "is_primary": True,
                },
            )

    def test_cannot_assign_subject_to_user_without_teacher_role(self) -> None:
        """
        Нельзя назначить предмет пользователю без роли преподавателя.
        """

        not_teacher = create_test_user(
            email="not-teacher-subject-services@example.com",
            phone="+79998300005",
        )

        with self.assertRaises(ValidationError):
            assign_subject_to_teacher(
                actor=self.superadmin,
                teacher=not_teacher,
                subject=self.physics,
                data={
                    "is_primary": True,
                },
            )

        self.assertFalse(
            TeacherSubject.objects.filter(
                teacher=not_teacher,
                subject=self.physics,
            ).exists()
        )

    def test_cannot_assign_inactive_subject_to_teacher(self) -> None:
        """
        Нельзя назначить преподавателю неактивный предмет.
        """

        inactive_subject = create_subject(
            name="Неактивный предмет",
            short_name="Неактивный",
            code="inactive_subject_services",
            is_active=False,
        )

        with self.assertRaises(ValidationError):
            assign_subject_to_teacher(
                actor=self.superadmin,
                teacher=self.second_teacher,
                subject=inactive_subject,
                data={
                    "is_primary": True,
                },
            )

    def test_update_teacher_subject(self) -> None:
        """
        Сервис обновляет предмет преподавателя.
        """

        teacher_subject = update_teacher_subject(
            actor=self.superadmin,
            teacher_subject=self.teacher_subject,
            data={
                "subject": self.physics,
                "is_primary": False,
                "notes": "Обновлено сервисом.",
            },
        )

        self.assertEqual(teacher_subject.subject, self.physics)
        self.assertFalse(teacher_subject.is_primary)
        self.assertEqual(teacher_subject.notes, "Обновлено сервисом.")

    def test_regular_user_cannot_update_teacher_subject(self) -> None:
        """
        Обычный пользователь не может обновить предмет преподавателя.
        """

        with self.assertRaises(PermissionDenied):
            update_teacher_subject(
                actor=self.regular_user,
                teacher_subject=self.teacher_subject,
                data={
                    "notes": "Нет доступа",
                },
            )

    def test_deactivate_teacher_subject(self) -> None:
        """
        Сервис деактивирует предмет преподавателя.
        """

        teacher_subject = deactivate_teacher_subject(
            actor=self.superadmin,
            teacher_subject=self.teacher_subject,
        )

        self.assertFalse(teacher_subject.is_active)
        self.assertFalse(teacher_subject.is_primary)

    def test_deactivate_inactive_teacher_subject_raises_error(self) -> None:
        """
        Повторная деактивация предмета преподавателя возвращает ошибку.
        """

        self.teacher_subject.is_active = False
        self.teacher_subject.is_primary = False
        self.teacher_subject.save(
            update_fields=[
                "is_active",
                "is_primary",
            ]
        )

        with self.assertRaises(ValidationError):
            deactivate_teacher_subject(
                actor=self.superadmin,
                teacher_subject=self.teacher_subject,
            )

    def test_restore_teacher_subject(self) -> None:
        """
        Сервис восстанавливает предмет преподавателя.
        """

        self.teacher_subject.is_active = False
        self.teacher_subject.is_primary = False
        self.teacher_subject.save(
            update_fields=[
                "is_active",
                "is_primary",
            ]
        )

        teacher_subject = restore_teacher_subject(
            actor=self.superadmin,
            teacher_subject=self.teacher_subject,
        )

        self.assertTrue(teacher_subject.is_active)

    def test_cannot_restore_teacher_subject_with_inactive_subject(self) -> None:
        """
        Нельзя восстановить связь с неактивным предметом.
        """

        self.teacher_subject.is_active = False
        self.teacher_subject.is_primary = False
        self.teacher_subject.save(
            update_fields=[
                "is_active",
                "is_primary",
            ]
        )

        self.math.is_active = False
        self.math.save(update_fields=["is_active"])

        with self.assertRaises(ValidationError):
            restore_teacher_subject(
                actor=self.superadmin,
                teacher_subject=self.teacher_subject,
            )

    def test_set_primary_teacher_subject(self) -> None:
        """
        Сервис делает предмет основным и снимает primary с другого предмета.
        """

        second_subject = create_teacher_subject(
            teacher=self.teacher,
            subject=self.physics,
            is_primary=False,
            is_active=True,
        )

        teacher_subject = set_primary_teacher_subject(
            actor=self.superadmin,
            teacher_subject=second_subject,
        )

        self.teacher_subject.refresh_from_db()

        self.assertTrue(teacher_subject.is_primary)
        self.assertFalse(self.teacher_subject.is_primary)

    def test_cannot_set_inactive_teacher_subject_as_primary(self) -> None:
        """
        Неактивный предмет преподавателя нельзя сделать основным.
        """

        self.teacher_subject.is_active = False
        self.teacher_subject.is_primary = False
        self.teacher_subject.save(
            update_fields=[
                "is_active",
                "is_primary",
            ]
        )

        with self.assertRaises(ValidationError):
            set_primary_teacher_subject(
                actor=self.superadmin,
                teacher_subject=self.teacher_subject,
            )