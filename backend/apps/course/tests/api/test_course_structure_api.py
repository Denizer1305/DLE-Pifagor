from __future__ import annotations

from apps.course.models import CourseLessonBlock, CourseMaterialLink
from apps.course.tests.factories import (
    create_course,
    create_course_lesson,
    create_course_lesson_block,
    create_course_material_link,
    create_course_section,
    create_material,
    create_superadmin,
    extract_results,
)
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class CourseStructureApiTestCase(APITestCase):
    """
    API-тесты структуры курса.
    """

    def setUp(self) -> None:
        """
        Подготавливает структуру курса.
        """

        self.superadmin = create_superadmin(
            email="course-structure-api-superadmin@example.com",
        )
        self.course = create_course()
        self.section = create_course_section(course=self.course)
        self.lesson = create_course_lesson(
            course=self.course,
            section=self.section,
        )
        self.material = create_material(
            organization=self.course.organization,
            subject=self.course.subject,
            owner=self.course.owner_teacher,
        )
        self.block = create_course_lesson_block(lesson=self.lesson)
        self.material_link = create_course_material_link(
            course=self.course,
            section=self.section,
            lesson=self.lesson,
            material=self.material,
        )

    def test_superadmin_can_get_sections_list(self) -> None:
        """
        Суперадмин получает список разделов.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.get(reverse("course_admin:course-admin-sections-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        section_ids = {item["id"] for item in extract_results(response.json())}

        self.assertIn(self.section.id, section_ids)

    def test_superadmin_can_create_section(self) -> None:
        """
        Суперадмин создаёт раздел.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse("course_admin:course-admin-sections-list"),
            {
                "course_id": self.course.id,
                "title": "API раздел",
                "description": "",
                "section_number": 10,
                "order": 10,
                "planned_hours": 12,
                "is_required": True,
                "is_published": False,
                "is_active": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["title"], "API раздел")

    def test_superadmin_can_publish_section(self) -> None:
        """
        Суперадмин публикует раздел.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse(
                "course_admin:course-admin-sections-publish",
                kwargs={"pk": self.section.id},
            ),
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json()["is_published"])

    def test_superadmin_can_get_lessons_list(self) -> None:
        """
        Суперадмин получает список уроков.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.get(reverse("course_admin:course-admin-lessons-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        lesson_ids = {item["id"] for item in extract_results(response.json())}

        self.assertIn(self.lesson.id, lesson_ids)

    def test_superadmin_can_create_lesson(self) -> None:
        """
        Суперадмин создаёт урок.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse("course_admin:course-admin-lessons-list"),
            {
                "course_id": self.course.id,
                "section_id": self.section.id,
                "lesson_number": 10,
                "lesson_type": self.lesson.lesson_type,
                "title": "API урок",
                "short_content": "Описание урока.",
                "planned_hours": 2,
                "theory_hours": 1,
                "practice_hours": 1,
                "lab_hours": 0,
                "self_study_hours": 0,
                "order": 10,
                "is_required": True,
                "is_preview": False,
                "is_published": False,
                "is_active": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["title"], "API урок")

    def test_superadmin_can_get_lesson_blocks_list(self) -> None:
        """
        Суперадмин получает список блоков урока.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.get(
            reverse("course_admin:course-admin-lesson-blocks-list")
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        block_ids = {item["id"] for item in extract_results(response.json())}

        self.assertIn(self.block.id, block_ids)

    def test_superadmin_can_create_lesson_block(self) -> None:
        """
        Суперадмин создаёт блок урока.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse("course_admin:course-admin-lesson-blocks-list"),
            {
                "lesson_id": self.lesson.id,
                "block_type": CourseLessonBlock.BlockTypeChoices.TEXT,
                "title": "API блок",
                "content": "Контент API блока.",
                "external_url": "",
                "order": 10,
                "is_visible": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["title"], "API блок")

    def test_superadmin_can_hide_lesson_block(self) -> None:
        """
        Суперадмин скрывает блок урока.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse(
                "course_admin:course-admin-lesson-blocks-hide",
                kwargs={"pk": self.block.id},
            ),
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.json()["is_visible"])

    def test_superadmin_can_get_material_links_list(self) -> None:
        """
        Суперадмин получает список материалов курса.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.get(
            reverse("course_admin:course-admin-material-links-list")
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        link_ids = {item["id"] for item in extract_results(response.json())}

        self.assertIn(self.material_link.id, link_ids)

    def test_superadmin_can_create_material_link(self) -> None:
        """
        Суперадмин создаёт связь курса с материалом.
        """

        second_material = create_material(
            organization=self.course.organization,
            subject=self.course.subject,
            owner=self.course.owner_teacher,
            title="Второй материал для курса",
        )

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse("course_admin:course-admin-material-links-list"),
            {
                "course_id": self.course.id,
                "section_id": self.section.id,
                "lesson_id": self.lesson.id,
                "material_id": second_material.id,
                "placement": CourseMaterialLink.PlacementChoices.LESSON,
                "order": 10,
                "is_required": True,
                "is_visible": True,
                "notes": "",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.json()["placement"],
            CourseMaterialLink.PlacementChoices.LESSON,
        )

    def test_superadmin_can_hide_material_link(self) -> None:
        """
        Суперадмин скрывает материал курса.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse(
                "course_admin:course-admin-material-links-hide",
                kwargs={"pk": self.material_link.id},
            ),
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.json()["is_visible"])
