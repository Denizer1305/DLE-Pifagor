from __future__ import annotations

from apps.course.models import CourseLesson, CourseLessonBlock, CourseMaterialLink
from apps.course.selectors import (
    course_lesson_block_list_queryset,
    course_lesson_list_queryset,
    course_material_link_list_queryset,
    course_section_list_queryset,
    get_course_lesson_block_by_id,
    get_course_lesson_by_id,
    get_course_material_link_by_id,
    get_course_section_by_id,
)
from apps.course.tests.factories import (
    create_course,
    create_course_lesson,
    create_course_lesson_block,
    create_course_material_link,
    create_course_section,
    create_material,
)
from django.test import TestCase


class CourseStructureSelectorsTestCase(TestCase):
    """
    Тесты селекторов структуры курса.
    """

    def setUp(self) -> None:
        """
        Подготавливает структуру курса.
        """

        self.course = create_course(
            title="Structure Selectors Course",
        )
        self.other_course = create_course(
            title="Other Structure Course",
        )

        self.section = create_course_section(
            course=self.course,
            title="Раздел структуры",
            is_published=True,
            is_active=True,
        )
        self.other_section = create_course_section(
            course=self.other_course,
            title="Чужой раздел",
        )

        self.lesson = create_course_lesson(
            course=self.course,
            section=self.section,
            title="Урок структуры",
            lesson_type=CourseLesson.LessonTypeChoices.LECTURE,
            is_published=True,
            is_active=True,
        )
        self.other_lesson = create_course_lesson(
            course=self.other_course,
            section=self.other_section,
            title="Чужой урок",
        )

        self.material = create_material(
            organization=self.course.organization,
            subject=self.course.subject,
            owner=self.course.owner_teacher,
        )

        self.block = create_course_lesson_block(
            lesson=self.lesson,
            block_type=CourseLessonBlock.BlockTypeChoices.TEXT,
            title="Текстовый блок структуры",
            is_visible=True,
        )
        self.material_link = create_course_material_link(
            course=self.course,
            section=self.section,
            lesson=self.lesson,
            material=self.material,
            placement=CourseMaterialLink.PlacementChoices.LESSON,
            is_visible=True,
        )

    def test_section_list_filters_by_course(self) -> None:
        """
        Разделы фильтруются по курсу.
        """

        section_ids = set(
            course_section_list_queryset(
                course_id=self.course.id,
            ).values_list(
                "id",
                flat=True,
            )
        )

        self.assertIn(self.section.id, section_ids)
        self.assertNotIn(self.other_section.id, section_ids)

    def test_section_list_filters_by_search(self) -> None:
        """
        Разделы фильтруются по поиску.
        """

        section_ids = set(
            course_section_list_queryset(
                search="структуры",
            ).values_list(
                "id",
                flat=True,
            )
        )

        self.assertIn(self.section.id, section_ids)

    def test_get_section_by_id_returns_section(self) -> None:
        """
        Селектор возвращает раздел по id.
        """

        section = get_course_section_by_id(self.section.id)

        self.assertEqual(section.id, self.section.id)

    def test_lesson_list_filters_by_course(self) -> None:
        """
        Уроки фильтруются по курсу.
        """

        lesson_ids = set(
            course_lesson_list_queryset(
                course_id=self.course.id,
            ).values_list(
                "id",
                flat=True,
            )
        )

        self.assertIn(self.lesson.id, lesson_ids)
        self.assertNotIn(self.other_lesson.id, lesson_ids)

    def test_lesson_list_filters_by_section(self) -> None:
        """
        Уроки фильтруются по разделу.
        """

        lesson_ids = set(
            course_lesson_list_queryset(
                section_id=self.section.id,
            ).values_list(
                "id",
                flat=True,
            )
        )

        self.assertIn(self.lesson.id, lesson_ids)

    def test_lesson_list_filters_by_lesson_type(self) -> None:
        """
        Уроки фильтруются по типу.
        """

        lesson_ids = set(
            course_lesson_list_queryset(
                lesson_type=CourseLesson.LessonTypeChoices.LECTURE,
            ).values_list(
                "id",
                flat=True,
            )
        )

        self.assertIn(self.lesson.id, lesson_ids)

    def test_get_lesson_by_id_returns_lesson(self) -> None:
        """
        Селектор возвращает урок по id.
        """

        lesson = get_course_lesson_by_id(self.lesson.id)

        self.assertEqual(lesson.id, self.lesson.id)

    def test_lesson_block_list_filters_by_lesson(self) -> None:
        """
        Блоки урока фильтруются по уроку.
        """

        block_ids = set(
            course_lesson_block_list_queryset(
                lesson_id=self.lesson.id,
            ).values_list(
                "id",
                flat=True,
            )
        )

        self.assertIn(self.block.id, block_ids)

    def test_lesson_block_list_filters_by_block_type(self) -> None:
        """
        Блоки урока фильтруются по типу блока.
        """

        block_ids = set(
            course_lesson_block_list_queryset(
                block_type=CourseLessonBlock.BlockTypeChoices.TEXT,
            ).values_list(
                "id",
                flat=True,
            )
        )

        self.assertIn(self.block.id, block_ids)

    def test_get_lesson_block_by_id_returns_block(self) -> None:
        """
        Селектор возвращает блок урока по id.
        """

        block = get_course_lesson_block_by_id(self.block.id)

        self.assertEqual(block.id, self.block.id)

    def test_material_link_list_filters_by_course(self) -> None:
        """
        Связи материалов фильтруются по курсу.
        """

        link_ids = set(
            course_material_link_list_queryset(
                course_id=self.course.id,
            ).values_list(
                "id",
                flat=True,
            )
        )

        self.assertIn(self.material_link.id, link_ids)

    def test_material_link_list_filters_by_lesson(self) -> None:
        """
        Связи материалов фильтруются по уроку.
        """

        link_ids = set(
            course_material_link_list_queryset(
                lesson_id=self.lesson.id,
            ).values_list(
                "id",
                flat=True,
            )
        )

        self.assertIn(self.material_link.id, link_ids)

    def test_material_link_list_filters_by_material(self) -> None:
        """
        Связи материалов фильтруются по материалу.
        """

        link_ids = set(
            course_material_link_list_queryset(
                material_id=self.material.id,
            ).values_list(
                "id",
                flat=True,
            )
        )

        self.assertIn(self.material_link.id, link_ids)

    def test_get_material_link_by_id_returns_link(self) -> None:
        """
        Селектор возвращает связь материала по id.
        """

        link = get_course_material_link_by_id(self.material_link.id)

        self.assertEqual(link.id, self.material_link.id)
