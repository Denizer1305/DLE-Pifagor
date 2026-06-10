from __future__ import annotations

from apps.course.models import CourseAccessRule, CourseEnrollment, CourseGroupAccess
from apps.course.tests.factories import (
    create_course,
    create_course_access_rule,
    create_course_enrollment,
    create_course_group_access,
    create_learner,
    create_study_group,
    create_superadmin,
    extract_results,
    get_choice_value,
    unique_code,
)
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class CourseAccessApiTestCase(APITestCase):
    """
    API-тесты доступов и записей на курс.
    """

    def setUp(self) -> None:
        """
        Подготавливает доступы.
        """

        self.superadmin = create_superadmin(
            email="course-access-api-superadmin@example.com",
        )
        self.course = create_course()
        self.group = create_study_group(
            organization=self.course.organization,
        )
        self.learner = create_learner(
            email="course-access-api-learner@example.com",
        )
        self.group_access = create_course_group_access(
            course=self.course,
            group=self.group,
        )
        self.access_rule = create_course_access_rule(
            course=self.course,
            learner=self.learner,
            access_type=CourseAccessRule.AccessTypeChoices.LEARNER,
        )
        self.enrollment = create_course_enrollment(
            course=self.course,
            learner=self.learner,
            group_access=self.group_access,
            access_rule=self.access_rule,
        )

    def test_superadmin_can_get_group_accesses_list(self) -> None:
        """
        Суперадмин получает список групповых доступов.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.get(
            reverse("course_admin:course-admin-group-accesses-list")
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        access_ids = {item["id"] for item in extract_results(response.json())}

        self.assertIn(self.group_access.id, access_ids)

    def test_superadmin_can_create_group_access(self) -> None:
        """
        Суперадмин создаёт групповой доступ.
        """

        second_group = create_study_group(
            organization=self.course.organization,
        )

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse("course_admin:course-admin-group-accesses-list"),
            {
                "course_id": self.course.id,
                "group_id": second_group.id,
                "visibility": CourseGroupAccess.VisibilityChoices.VISIBLE,
                "auto_enroll": True,
                "is_active": True,
                "notes": "",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["group"], second_group.id)

    def test_superadmin_can_hide_group_access(self) -> None:
        """
        Суперадмин скрывает курс от группы.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse(
                "course_admin:course-admin-group-accesses-hide",
                kwargs={"pk": self.group_access.id},
            ),
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json()["visibility"], CourseGroupAccess.VisibilityChoices.HIDDEN
        )

    def test_superadmin_can_get_access_rules_list(self) -> None:
        """
        Суперадмин получает список правил доступа.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.get(
            reverse("course_admin:course-admin-access-rules-list")
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        rule_ids = {item["id"] for item in extract_results(response.json())}

        self.assertIn(self.access_rule.id, rule_ids)

    def test_superadmin_can_create_access_rule(self) -> None:
        """
        Суперадмин создаёт правило доступа.
        """

        second_learner = create_learner(
            email="course-access-api-second-learner@example.com",
        )

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse("course_admin:course-admin-access-rules-list"),
            {
                "course_id": self.course.id,
                "access_type": CourseAccessRule.AccessTypeChoices.LEARNER,
                "learner_id": second_learner.id,
                "access_code": unique_code("access"),
                "auto_enroll": True,
                "is_active": True,
                "notes": "",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["learner"]["id"], second_learner.id)

    def test_superadmin_can_deactivate_access_rule(self) -> None:
        """
        Суперадмин деактивирует правило доступа.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse(
                "course_admin:course-admin-access-rules-deactivate",
                kwargs={"pk": self.access_rule.id},
            ),
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.json()["is_active"])

    def test_superadmin_can_get_enrollments_list(self) -> None:
        """
        Суперадмин получает список записей на курс.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.get(
            reverse("course_admin:course-admin-enrollments-list")
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        enrollment_ids = {item["id"] for item in extract_results(response.json())}

        self.assertIn(self.enrollment.id, enrollment_ids)

    def test_superadmin_can_create_enrollment(self) -> None:
        """
        Суперадмин создаёт запись на курс.
        """

        second_learner = create_learner(
            email="course-enrollment-api-second@example.com",
        )
        initial_status = get_choice_value(
            CourseEnrollment,
            "StatusChoices",
            "ENROLLED",
            "ACTIVE",
            "IN_PROGRESS",
            default="active",
        )

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse("course_admin:course-admin-enrollments-list"),
            {
                "course_id": self.course.id,
                "learner_id": second_learner.id,
                "status": initial_status,
                "progress_percent": 0,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["learner"]["id"], second_learner.id)

    def test_superadmin_can_start_enrollment(self) -> None:
        """
        Суперадмин запускает прохождение курса.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse(
                "course_admin:course-admin-enrollments-start",
                kwargs={"pk": self.enrollment.id},
            ),
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json()["status"], CourseEnrollment.StatusChoices.IN_PROGRESS
        )

    def test_superadmin_can_complete_enrollment(self) -> None:
        """
        Суперадмин завершает прохождение курса.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse(
                "course_admin:course-admin-enrollments-complete",
                kwargs={"pk": self.enrollment.id},
            ),
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json()["status"], CourseEnrollment.StatusChoices.COMPLETED
        )
        self.assertEqual(response.json()["progress_percent"], 100)
