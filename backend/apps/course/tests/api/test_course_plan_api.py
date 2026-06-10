from __future__ import annotations

from apps.course.models import CoursePlan, CoursePlanImport
from apps.course.tests.factories import (
    create_course,
    create_course_plan,
    create_course_plan_import,
    create_superadmin,
    extract_results,
    unique_code,
)
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class CoursePlanApiTestCase(APITestCase):
    """
    API-тесты КТП и импортов КТП.
    """

    def setUp(self) -> None:
        """
        Подготавливает курс и КТП.
        """

        self.superadmin = create_superadmin(
            email="course-plan-api-superadmin@example.com",
        )
        self.course = create_course()
        self.plan = create_course_plan(course=self.course)
        self.plan_import = create_course_plan_import(course_plan=self.plan)

    def test_superadmin_can_get_plans_list(self) -> None:
        """
        Суперадмин получает список КТП.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.get(reverse("course_admin:course-admin-plans-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        plan_ids = {item["id"] for item in extract_results(response.json())}

        self.assertIn(self.plan.id, plan_ids)

    def test_superadmin_can_create_plan(self) -> None:
        """
        Суперадмин создаёт КТП.
        """

        second_course = create_course()

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse("course_admin:course-admin-plans-list"),
            {
                "course_id": second_course.id,
                "discipline_name": "API дисциплина",
                "discipline_code": "ОП.02",
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
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["discipline_name"], "API дисциплина")

    def test_superadmin_can_review_plan(self) -> None:
        """
        Суперадмин помечает КТП как проверенный.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse(
                "course_admin:course-admin-plans-review",
                kwargs={"pk": self.plan.id},
            ),
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["status"], CoursePlan.StatusChoices.REVIEWED)

    def test_superadmin_can_approve_plan(self) -> None:
        """
        Суперадмин утверждает КТП.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse(
                "course_admin:course-admin-plans-approve",
                kwargs={"pk": self.plan.id},
            ),
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["status"], CoursePlan.StatusChoices.APPROVED)

    def test_superadmin_can_archive_plan(self) -> None:
        """
        Суперадмин архивирует КТП.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse(
                "course_admin:course-admin-plans-archive",
                kwargs={"pk": self.plan.id},
            ),
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["status"], CoursePlan.StatusChoices.ARCHIVED)

    def test_superadmin_can_get_plan_imports_list(self) -> None:
        """
        Суперадмин получает список импортов КТП.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.get(
            reverse("course_admin:course-admin-plan-imports-list")
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        import_ids = {item["id"] for item in extract_results(response.json())}

        self.assertIn(self.plan_import.id, import_ids)

    def test_superadmin_can_create_plan_import(self) -> None:
        """
        Суперадмин создаёт импорт КТП.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse("course_admin:course-admin-plan-imports-list"),
            {
                "course_plan_id": self.plan.id,
                "source_file": SimpleUploadedFile(
                    "api-ktp.pdf",
                    b"%PDF-1.4\n% api ktp file\n",
                    content_type="application/pdf",
                ),
                "original_filename": "api-ktp.pdf",
                "file_hash": unique_code("hash"),
                "status": CoursePlanImport.StatusChoices.UPLOADED,
                "parser_version": "api-parser",
                "imported_by_id": self.superadmin.id,
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["original_filename"], "api-ktp.pdf")

    def test_superadmin_can_mark_import_parsed(self) -> None:
        """
        Суперадмин помечает импорт КТП как разобранный.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse(
                "course_admin:course-admin-plan-imports-mark-parsed",
                kwargs={"pk": self.plan_import.id},
            ),
            {
                "parsed_payload": {
                    "rows": [
                        {
                            "title": "Урок 1",
                        }
                    ]
                },
                "parser_version": "api-parser-2",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json()["status"], CoursePlanImport.StatusChoices.PARSED
        )

    def test_superadmin_can_mark_import_failed(self) -> None:
        """
        Суперадмин помечает импорт КТП как ошибочный.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse(
                "course_admin:course-admin-plan-imports-mark-failed",
                kwargs={"pk": self.plan_import.id},
            ),
            {
                "errors": [
                    {
                        "message": "Ошибка импорта.",
                    }
                ]
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json()["status"], CoursePlanImport.StatusChoices.FAILED
        )

    def test_superadmin_can_mark_import_applied(self) -> None:
        """
        Суперадмин помечает импорт КТП как применённый.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse(
                "course_admin:course-admin-plan-imports-mark-applied",
                kwargs={"pk": self.plan_import.id},
            ),
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json()["status"], CoursePlanImport.StatusChoices.APPLIED
        )
