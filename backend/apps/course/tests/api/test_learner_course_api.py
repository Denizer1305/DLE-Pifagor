from __future__ import annotations

from apps.course.tests.factories import (
    create_course,
    create_course_enrollment,
    create_course_lesson,
    create_course_lesson_block,
    create_course_material_link,
    create_course_progress,
    create_course_section,
    create_learner,
    create_material,
    extract_results,
)
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class LearnerCourseApiTestCase(APITestCase):
    """
    API-тесты learner-пространства курсов.
    """

    def setUp(self) -> None:
        """
        Подготавливает обучающегося и курс.
        """

        self.learner = create_learner(
            email="course-learner-api@example.com",
        )
        self.other_learner = create_learner(
            email="course-learner-api-other@example.com",
        )
        self.course = create_course(
            title="Курс обучающегося",
        )
        self.foreign_course = create_course(
            title="Недоступный курс",
        )
        self.section = create_course_section(
            course=self.course,
            is_published=True,
            is_active=True,
        )
        self.lesson = create_course_lesson(
            course=self.course,
            section=self.section,
            is_published=True,
            is_active=True,
        )
        self.material = create_material(
            organization=self.course.organization,
            subject=self.course.subject,
            owner=self.course.owner_teacher,
        )
        self.block = create_course_lesson_block(
            lesson=self.lesson,
            is_visible=True,
        )
        self.material_link = create_course_material_link(
            course=self.course,
            section=self.section,
            lesson=self.lesson,
            material=self.material,
            is_visible=True,
        )
        self.enrollment = create_course_enrollment(
            course=self.course,
            learner=self.learner,
        )
        self.course_progress = create_course_progress(
            enrollment=self.enrollment,
        )

    def test_learner_can_get_available_courses_list(self) -> None:
        """
        Обучающийся получает доступные ему курсы.
        """

        self.client.force_authenticate(user=self.learner)

        response = self.client.get(
            reverse("course_learner:course-learner-courses-list")
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        course_ids = {item["id"] for item in extract_results(response.json())}

        self.assertIn(self.course.id, course_ids)
        self.assertNotIn(self.foreign_course.id, course_ids)

    def test_learner_can_get_available_lessons_list(self) -> None:
        """
        Обучающийся получает уроки доступного курса.
        """

        self.client.force_authenticate(user=self.learner)

        response = self.client.get(
            reverse("course_learner:course-learner-lessons-list")
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        lesson_ids = {item["id"] for item in extract_results(response.json())}

        self.assertIn(self.lesson.id, lesson_ids)

    def test_learner_can_get_available_lesson_blocks_list(self) -> None:
        """
        Обучающийся получает блоки доступного урока.
        """

        self.client.force_authenticate(user=self.learner)

        response = self.client.get(
            reverse("course_learner:course-learner-lesson-blocks-list")
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        block_ids = {item["id"] for item in extract_results(response.json())}

        self.assertIn(self.block.id, block_ids)

    def test_learner_can_get_own_enrollments_list(self) -> None:
        """
        Обучающийся получает свои записи на курс.
        """

        self.client.force_authenticate(user=self.learner)

        response = self.client.get(
            reverse("course_learner:course-learner-enrollments-list")
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        enrollment_ids = {item["id"] for item in extract_results(response.json())}

        self.assertIn(self.enrollment.id, enrollment_ids)

    def test_learner_cannot_create_course(self) -> None:
        """
        Обучающийся не создаёт курс.
        """

        self.client.force_authenticate(user=self.learner)

        response = self.client.post(
            reverse("course_learner:course-learner-courses-list"),
            {
                "title": "Нельзя создать",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
