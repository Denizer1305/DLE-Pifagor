from __future__ import annotations

from apps.course.models import Course
from apps.course.tests.factories import (
    create_academic_year,
    create_course,
    create_education_period,
    create_organization,
    create_subject,
    create_superadmin,
    create_teacher,
    extract_results,
    unique_code,
    unique_slug,
)
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AdminCourseApiTestCase(APITestCase):
    """
    API-тесты административного управления курсами.
    """

    def setUp(self) -> None:
        """
        Подготавливает пользователя и курс.
        """

        self.superadmin = create_superadmin(
            email="course-api-superadmin@example.com",
        )
        self.teacher = create_teacher(
            email="course-api-teacher@example.com",
        )
        self.organization = create_organization()
        self.subject = create_subject()
        self.academic_year = create_academic_year()
        self.period = create_education_period(
            academic_year=self.academic_year,
        )
        self.course = create_course(
            owner_teacher=self.teacher,
            organization=self.organization,
            subject=self.subject,
            academic_year=self.academic_year,
            period=self.period,
            title="Админский тестовый курс",
        )

    def test_superadmin_can_get_courses_list(self) -> None:
        """
        Суперадмин получает список курсов.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.get(reverse("course_admin:course-admin-courses-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        course_ids = {item["id"] for item in extract_results(response.json())}

        self.assertIn(self.course.id, course_ids)

    def test_superadmin_can_get_course_detail(self) -> None:
        """
        Суперадмин получает карточку курса.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.get(
            reverse(
                "course_admin:course-admin-courses-detail",
                kwargs={"pk": self.course.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["id"], self.course.id)

    def test_superadmin_can_create_course(self) -> None:
        """
        Суперадмин создаёт курс.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse("course_admin:course-admin-courses-list"),
            {
                "code": unique_code("api_course"),
                "slug": unique_slug("api-course"),
                "title": "Новый API курс",
                "subtitle": "",
                "description": "Описание курса.",
                "course_type": Course.CourseTypeChoices.ACADEMIC,
                "origin": Course.OriginChoices.MANUAL,
                "status": Course.StatusChoices.DRAFT,
                "visibility": Course.VisibilityChoices.PRIVATE,
                "level": "Базовый",
                "language": "ru",
                "owner_teacher_id": self.teacher.id,
                "organization_id": self.organization.id,
                "subject_id": self.subject.id,
                "academic_year_id": self.academic_year.id,
                "period_id": self.period.id,
                "is_template": False,
                "is_active": True,
                "allow_self_enrollment": False,
                "enrollment_code": unique_code("enroll"),
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["title"], "Новый API курс")

    def test_superadmin_can_update_course(self) -> None:
        """
        Суперадмин обновляет курс.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.patch(
            reverse(
                "course_admin:course-admin-courses-detail",
                kwargs={"pk": self.course.id},
            ),
            {
                "title": "Обновлённый API курс",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["title"], "Обновлённый API курс")

    def test_superadmin_can_publish_course(self) -> None:
        """
        Суперадмин публикует курс.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse(
                "course_admin:course-admin-courses-publish",
                kwargs={"pk": self.course.id},
            ),
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["status"], Course.StatusChoices.PUBLISHED)

    def test_superadmin_can_archive_course(self) -> None:
        """
        Суперадмин архивирует курс.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse(
                "course_admin:course-admin-courses-archive",
                kwargs={"pk": self.course.id},
            ),
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["status"], Course.StatusChoices.ARCHIVED)

    def test_superadmin_can_restore_course(self) -> None:
        """
        Суперадмин восстанавливает курс в черновик.
        """

        self.course.status = Course.StatusChoices.ARCHIVED
        self.course.is_active = False
        self.course.save(
            update_fields=[
                "status",
                "is_active",
                "updated_at",
            ]
        )

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse(
                "course_admin:course-admin-courses-restore",
                kwargs={"pk": self.course.id},
            ),
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["status"], Course.StatusChoices.DRAFT)

    def test_superadmin_can_duplicate_course(self) -> None:
        """
        Суперадмин копирует курс.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse(
                "course_admin:course-admin-courses-duplicate",
                kwargs={"pk": self.course.id},
            ),
            {
                "title": "Копия API курса",
                "code": unique_code("api_course_copy"),
                "slug": unique_slug("api-course-copy"),
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["title"], "Копия API курса")
