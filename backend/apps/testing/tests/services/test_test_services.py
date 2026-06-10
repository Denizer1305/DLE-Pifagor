from __future__ import annotations

from apps.testing.constants import TestStatus
from apps.testing.services import (
    archive_test,
    create_test,
    publish_test,
    restore_test,
    update_test,
)
from apps.testing.tests.factories import (
    create_choice_question_with_options,
    create_course,
    create_teacher,
)
from apps.testing.tests.factories import create_test as create_test_factory
from django.test import TestCase


class TestServicesTestCase(TestCase):
    """
    Тесты сервисов учебного теста.
    """

    def test_create_test_creates_test(self) -> None:
        """
        Сервис создаёт учебный тест.
        """

        course = create_course()
        teacher = create_teacher()

        exam = create_test(
            data={
                "title": "Итоговый тест",
                "description": "Описание.",
                "instructions": "Ответьте на вопросы.",
                "course": course,
                "organization": course.organization,
                "subject": course.subject,
                "owner_teacher": teacher,
            }
        )

        self.assertEqual(exam.title, "Итоговый тест")
        self.assertEqual(exam.course, course)
        self.assertEqual(exam.status, TestStatus.DRAFT)

    def test_update_test_updates_title(self) -> None:
        """
        Сервис обновляет тест.
        """

        exam = create_test_factory(title="Старое название")

        updated_exam = update_test(
            test=exam,
            data={
                "title": "Новое название",
            },
        )

        self.assertEqual(updated_exam.title, "Новое название")

    def test_publish_test_sets_published_status(self) -> None:
        """
        Сервис публикует тест.
        """

        exam = create_test_factory()
        create_choice_question_with_options(test=exam)

        published_exam = publish_test(test=exam)

        self.assertEqual(published_exam.status, TestStatus.PUBLISHED)
        self.assertTrue(published_exam.is_active)
        self.assertIsNotNone(published_exam.published_at)
        self.assertIsNone(published_exam.archived_at)

    def test_archive_test_sets_archived_status(self) -> None:
        """
        Сервис архивирует тест.
        """

        exam = create_test_factory(status=TestStatus.PUBLISHED)

        archived_exam = archive_test(test=exam)

        self.assertEqual(archived_exam.status, TestStatus.ARCHIVED)
        self.assertFalse(archived_exam.is_active)
        self.assertIsNotNone(archived_exam.archived_at)

    def test_restore_test_returns_test_to_draft(self) -> None:
        """
        Сервис восстанавливает архивный тест в черновик.
        """

        exam = create_test_factory(
            status=TestStatus.ARCHIVED,
            is_active=False,
        )

        restored_exam = restore_test(test=exam)

        self.assertEqual(restored_exam.status, TestStatus.DRAFT)
        self.assertTrue(restored_exam.is_active)
        self.assertIsNone(restored_exam.archived_at)
