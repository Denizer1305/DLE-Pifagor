from __future__ import annotations

from apps.course.models import LessonProgress
from apps.course.tests.factories import (
    create_course,
    create_course_enrollment,
    create_course_lesson,
    create_course_progress,
    create_learner,
    create_lesson_progress,
    create_superadmin,
    extract_results,
    get_choice_value,
)
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class CourseProgressApiTestCase(APITestCase):
    """
    API-тесты прогресса курса и уроков.
    """

    def setUp(self) -> None:
        """
        Подготавливает прогресс.
        """

        self.superadmin = create_superadmin(
            email="course-progress-api-superadmin@example.com",
        )
        self.learner = create_learner(
            email="course-progress-api-learner@example.com",
        )
        self.course = create_course()
        self.lesson = create_course_lesson(
            course=self.course,
            is_published=True,
            is_active=True,
        )
        self.enrollment = create_course_enrollment(
            course=self.course,
            learner=self.learner,
        )
        self.course_progress = create_course_progress(
            enrollment=self.enrollment,
        )
        self.lesson_progress = create_lesson_progress(
            enrollment=self.enrollment,
            course_progress=self.course_progress,
            lesson=self.lesson,
        )

    def test_superadmin_can_get_course_progress_list(self) -> None:
        """
        Суперадмин получает список прогресса курсов.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.get(
            reverse("course_admin:course-admin-course-progress-list")
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        progress_ids = {item["id"] for item in extract_results(response.json())}

        self.assertIn(self.course_progress.id, progress_ids)

    def test_superadmin_can_recalculate_course_progress(self) -> None:
        """
        Суперадмин пересчитывает прогресс курса.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse(
                "course_admin:course-admin-course-progress-recalculate",
                kwargs={"pk": self.course_progress.id},
            ),
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["id"], self.course_progress.id)

    def test_superadmin_can_get_lesson_progress_list(self) -> None:
        """
        Суперадмин получает список прогресса уроков.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.get(
            reverse("course_admin:course-admin-lesson-progress-list")
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        progress_ids = {item["id"] for item in extract_results(response.json())}

        self.assertIn(self.lesson_progress.id, progress_ids)

    def test_superadmin_can_start_lesson_progress(self) -> None:
        """
        Суперадмин запускает прогресс урока.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse(
                "course_admin:course-admin-lesson-progress-start",
                kwargs={"pk": self.lesson_progress.id},
            ),
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_status = get_choice_value(
            LessonProgress,
            "StatusChoices",
            "IN_PROGRESS",
            default="in_progress",
        )

        self.assertEqual(response.json()["status"], expected_status)

    def test_superadmin_can_complete_lesson_progress(self) -> None:
        """
        Суперадмин завершает прогресс урока.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse(
                "course_admin:course-admin-lesson-progress-complete",
                kwargs={"pk": self.lesson_progress.id},
            ),
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_status = get_choice_value(
            LessonProgress,
            "StatusChoices",
            "COMPLETED",
            default="completed",
        )

        self.assertEqual(response.json()["status"], expected_status)

    def test_learner_can_track_opened_lesson(self) -> None:
        """
        Обучающийся фиксирует открытие урока.
        """

        self.client.force_authenticate(user=self.learner)

        response = self.client.post(
            reverse("course_learner:course-learner-lesson-progress-track-opened"),
            {
                "enrollment_id": self.enrollment.id,
                "lesson_id": self.lesson.id,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["lesson"]["id"], self.lesson.id)

    def test_learner_can_track_completed_lesson(self) -> None:
        """
        Обучающийся фиксирует завершение урока.
        """

        self.client.force_authenticate(user=self.learner)

        response = self.client.post(
            reverse("course_learner:course-learner-lesson-progress-track-completed"),
            {
                "enrollment_id": self.enrollment.id,
                "lesson_id": self.lesson.id,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["lesson"]["id"], self.lesson.id)
