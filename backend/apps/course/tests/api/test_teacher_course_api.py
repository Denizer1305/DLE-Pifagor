from __future__ import annotations

from apps.course.models import Course
from apps.course.tests.factories import (
    create_academic_year,
    create_course,
    create_education_period,
    create_organization,
    create_subject,
    create_teacher,
    extract_results,
    unique_code,
    unique_slug,
)
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TeacherCourseApiTestCase(APITestCase):
    """
    API-тесты преподавательского пространства курсов.
    """

    def setUp(self) -> None:
        """
        Подготавливает преподавателя и курс.
        """

        self.teacher = create_teacher(
            email="course-teacher-api-owner@example.com",
        )
        self.other_teacher = create_teacher(
            email="course-teacher-api-foreign@example.com",
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
            title="Курс преподавателя",
        )
        self.foreign_course = create_course(
            owner_teacher=self.other_teacher,
            title="Чужой курс",
        )

    def test_teacher_can_get_own_courses_list(self) -> None:
        """
        Преподаватель получает список доступных ему курсов.
        """

        self.client.force_authenticate(user=self.teacher)

        response = self.client.get(
            reverse("course_teacher:course-teacher-courses-list")
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        course_ids = {item["id"] for item in extract_results(response.json())}

        self.assertIn(self.course.id, course_ids)
        self.assertNotIn(self.foreign_course.id, course_ids)

    def test_teacher_can_get_own_course_detail(self) -> None:
        """
        Преподаватель получает свой курс.
        """

        self.client.force_authenticate(user=self.teacher)

        response = self.client.get(
            reverse(
                "course_teacher:course-teacher-courses-detail",
                kwargs={"pk": self.course.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["id"], self.course.id)

    def test_teacher_can_create_course(self) -> None:
        """
        Преподаватель создаёт курс.
        """

        self.client.force_authenticate(user=self.teacher)

        response = self.client.post(
            reverse("course_teacher:course-teacher-courses-list"),
            {
                "code": unique_code("teacher_course"),
                "slug": unique_slug("teacher-course"),
                "title": "Курс через teacher API",
                "course_type": Course.CourseTypeChoices.ACADEMIC,
                "origin": Course.OriginChoices.MANUAL,
                "status": Course.StatusChoices.DRAFT,
                "visibility": Course.VisibilityChoices.PRIVATE,
                "owner_teacher_id": self.teacher.id,
                "organization_id": self.organization.id,
                "subject_id": self.subject.id,
                "academic_year_id": self.academic_year.id,
                "period_id": self.period.id,
                "is_active": True,
                "allow_self_enrollment": False,
                "enrollment_code": unique_code("enroll"),
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["title"], "Курс через teacher API")

    def test_teacher_cannot_get_foreign_course_detail(self) -> None:
        """
        Преподаватель не получает чужой курс.
        """

        self.client.force_authenticate(user=self.teacher)

        response = self.client.get(
            reverse(
                "course_teacher:course-teacher-courses-detail",
                kwargs={"pk": self.foreign_course.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
