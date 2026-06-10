from __future__ import annotations

from apps.course.models import CoursePlan, CoursePlanImport
from apps.course.services import (
    approve_course_plan,
    archive_course_plan,
    create_course_plan,
    create_course_plan_import,
    mark_course_plan_import_applied,
    mark_course_plan_import_failed,
    mark_course_plan_import_parsed,
    mark_course_plan_reviewed,
    update_course_plan,
)
from apps.course.tests.factories import create_course
from apps.course.tests.factories import create_course_plan as factory_create_course_plan
from apps.course.tests.factories import (
    create_course_plan_import as factory_create_course_plan_import,
)
from apps.course.tests.factories import create_teacher, unique_code
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase


class CoursePlanServicesTestCase(TestCase):
    """
    Тесты сервисов КТП.
    """

    def setUp(self) -> None:
        """
        Подготавливает курс.
        """

        self.course = create_course()
        self.teacher = create_teacher(
            email="course-plan-services-teacher@example.com",
        )

    def test_create_course_plan_creates_plan(self) -> None:
        """
        Сервис создаёт КТП.
        """

        plan = create_course_plan(
            data={
                "course": self.course,
                "discipline_name": "Основы Django",
                "discipline_code": "ОП.01",
                "specialty_code": "09.02.07",
                "specialty_name": "Информационные системы",
                "semester_number": 1,
                "total_hours": 72,
                "semester_hours": 72,
                "theory_hours": 30,
                "practice_hours": 30,
                "lab_hours": 12,
                "self_study_hours": 0,
                "consultation_hours": 0,
                "status": CoursePlan.StatusChoices.DRAFT,
                "is_active": True,
            }
        )

        self.assertEqual(plan.course_id, self.course.id)
        self.assertEqual(plan.discipline_name, "Основы Django")

    def test_update_course_plan_updates_fields(self) -> None:
        """
        Сервис обновляет КТП.
        """

        plan = factory_create_course_plan(course=self.course)

        updated_plan = update_course_plan(
            plan=plan,
            data={
                "discipline_name": "Обновлённая дисциплина",
                "total_hours": 80,
            },
        )

        self.assertEqual(
            updated_plan.discipline_name,
            "Обновлённая дисциплина",
        )
        self.assertEqual(updated_plan.total_hours, 80)

    def test_mark_course_plan_reviewed_sets_status(self) -> None:
        """
        Сервис переводит КТП в статус проверки.
        """

        plan = factory_create_course_plan(course=self.course)

        reviewed_plan = mark_course_plan_reviewed(plan=plan)

        self.assertEqual(
            reviewed_plan.status,
            CoursePlan.StatusChoices.REVIEWED,
        )

    def test_approve_course_plan_sets_status_and_active(self) -> None:
        """
        Сервис утверждает КТП.
        """

        plan = factory_create_course_plan(
            course=self.course,
            is_active=False,
        )

        approved_plan = approve_course_plan(plan=plan)

        self.assertEqual(
            approved_plan.status,
            CoursePlan.StatusChoices.APPROVED,
        )
        self.assertTrue(approved_plan.is_active)

    def test_archive_course_plan_sets_status_and_inactive(self) -> None:
        """
        Сервис архивирует КТП.
        """

        plan = factory_create_course_plan(course=self.course)

        archived_plan = archive_course_plan(plan=plan)

        self.assertEqual(
            archived_plan.status,
            CoursePlan.StatusChoices.ARCHIVED,
        )
        self.assertFalse(archived_plan.is_active)

    def test_create_course_plan_import_creates_import(self) -> None:
        """
        Сервис создаёт импорт КТП.
        """

        plan = factory_create_course_plan(course=self.course)

        plan_import = create_course_plan_import(
            data={
                "course_plan": plan,
                "source_file": SimpleUploadedFile(
                    "ktp-test.pdf",
                    b"%PDF-1.4\n% test ktp file content\n",
                    content_type="application/pdf",
                ),
                "original_filename": "ktp-test.pdf",
                "file_hash": unique_code("hash"),
                "status": CoursePlanImport.StatusChoices.UPLOADED,
                "parser_version": "test-parser",
                "parsed_payload": {},
                "errors": [],
                "imported_by": self.teacher,
            }
        )

        self.assertEqual(plan_import.course_plan_id, plan.id)
        self.assertEqual(plan_import.original_filename, "ktp-test.pdf")

    def test_mark_course_plan_import_parsed_sets_payload(self) -> None:
        """
        Сервис помечает импорт КТП как разобранный.
        """

        plan_import = factory_create_course_plan_import(
            course_plan=factory_create_course_plan(course=self.course),
        )

        parsed_import = mark_course_plan_import_parsed(
            plan_import=plan_import,
            parsed_payload={
                "rows": [
                    {
                        "title": "Урок 1",
                    }
                ]
            },
            parser_version="parser-2",
        )

        self.assertEqual(
            parsed_import.status,
            CoursePlanImport.StatusChoices.PARSED,
        )
        self.assertEqual(parsed_import.parser_version, "parser-2")
        self.assertEqual(len(parsed_import.parsed_payload["rows"]), 1)

    def test_mark_course_plan_import_failed_sets_errors(self) -> None:
        """
        Сервис помечает импорт КТП как ошибочный.
        """

        plan_import = factory_create_course_plan_import(
            course_plan=factory_create_course_plan(course=self.course),
        )

        failed_import = mark_course_plan_import_failed(
            plan_import=plan_import,
            errors=[
                {
                    "message": "Ошибка тестового импорта.",
                }
            ],
        )

        self.assertEqual(
            failed_import.status,
            CoursePlanImport.StatusChoices.FAILED,
        )
        self.assertEqual(len(failed_import.errors), 1)

    def test_mark_course_plan_import_applied_sets_applied_at(self) -> None:
        """
        Сервис помечает импорт КТП как применённый.
        """

        plan_import = factory_create_course_plan_import(
            course_plan=factory_create_course_plan(course=self.course),
        )

        applied_import = mark_course_plan_import_applied(
            plan_import=plan_import,
        )

        self.assertEqual(
            applied_import.status,
            CoursePlanImport.StatusChoices.APPLIED,
        )
        self.assertIsNotNone(applied_import.applied_at)
