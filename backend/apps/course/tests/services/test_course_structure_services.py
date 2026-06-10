from __future__ import annotations

from apps.course.models import CourseLessonBlock, CourseMaterialLink
from apps.course.services import (
    archive_course_lesson,
    archive_course_section,
    create_course_lesson,
    create_course_lesson_block,
    create_course_material_link,
    create_course_section,
    hide_course_lesson_block,
    hide_course_material_link,
    publish_course_lesson,
    publish_course_section,
    recalculate_course_section_hours,
    reorder_course_lessons,
    reorder_course_material_links,
    reorder_course_sections,
    reorder_lesson_blocks,
    show_course_lesson_block,
    show_course_material_link,
    update_course_lesson,
    update_course_lesson_block,
    update_course_material_link,
    update_course_section,
)
from apps.course.tests.factories import create_course
from apps.course.tests.factories import (
    create_course_lesson as factory_create_course_lesson,
)
from apps.course.tests.factories import (
    create_course_lesson_block as factory_create_course_lesson_block,
)
from apps.course.tests.factories import (
    create_course_material_link as factory_create_course_material_link,
)
from apps.course.tests.factories import (
    create_course_section as factory_create_course_section,
)
from apps.course.tests.factories import create_material
from django.test import TestCase


class CourseStructureServicesTestCase(TestCase):
    """
    Тесты сервисов структуры курса.
    """

    def setUp(self) -> None:
        """
        Подготавливает курс.
        """

        self.course = create_course()
        self.section = factory_create_course_section(
            course=self.course,
            planned_hours=0,
        )
        self.lesson = factory_create_course_lesson(
            course=self.course,
            section=self.section,
            planned_hours=2,
        )
        self.material = create_material(
            organization=self.course.organization,
            subject=self.course.subject,
            owner=self.course.owner_teacher,
        )

    def test_create_course_section_creates_section(self) -> None:
        """
        Сервис создаёт раздел.
        """

        section = create_course_section(
            data={
                "course": self.course,
                "title": "Новый раздел",
                "order": 2,
                "planned_hours": 10,
                "is_required": True,
                "is_published": False,
                "is_active": True,
            }
        )

        self.assertEqual(section.course_id, self.course.id)
        self.assertEqual(section.title, "Новый раздел")

    def test_update_course_section_updates_fields(self) -> None:
        """
        Сервис обновляет раздел.
        """

        updated_section = update_course_section(
            section=self.section,
            data={
                "title": "Обновлённый раздел",
                "planned_hours": 12,
            },
        )

        self.assertEqual(updated_section.title, "Обновлённый раздел")
        self.assertEqual(updated_section.planned_hours, 12)

    def test_publish_course_section_sets_flags(self) -> None:
        """
        Сервис публикует раздел.
        """

        section = publish_course_section(section=self.section)

        self.assertTrue(section.is_published)
        self.assertTrue(section.is_active)

    def test_archive_course_section_sets_flags(self) -> None:
        """
        Сервис архивирует раздел.
        """

        section = archive_course_section(section=self.section)

        self.assertFalse(section.is_published)
        self.assertFalse(section.is_active)

    def test_create_course_lesson_creates_lesson(self) -> None:
        """
        Сервис создаёт урок.
        """

        lesson = create_course_lesson(
            data={
                "course": self.course,
                "section": self.section,
                "title": "Новый урок",
                "lesson_type": self.lesson.lesson_type,
                "planned_hours": 2,
                "order": 2,
                "is_required": True,
                "is_published": False,
                "is_active": True,
            }
        )

        self.assertEqual(lesson.course_id, self.course.id)
        self.assertEqual(lesson.section_id, self.section.id)

    def test_update_course_lesson_updates_fields(self) -> None:
        """
        Сервис обновляет урок.
        """

        lesson = update_course_lesson(
            lesson=self.lesson,
            data={
                "title": "Обновлённый урок",
                "planned_hours": 4,
            },
        )

        self.assertEqual(lesson.title, "Обновлённый урок")
        self.assertEqual(lesson.planned_hours, 4)

    def test_publish_course_lesson_sets_flags(self) -> None:
        """
        Сервис публикует урок.
        """

        lesson = publish_course_lesson(lesson=self.lesson)

        self.assertTrue(lesson.is_published)
        self.assertTrue(lesson.is_active)

    def test_archive_course_lesson_sets_flags(self) -> None:
        """
        Сервис архивирует урок.
        """

        lesson = archive_course_lesson(lesson=self.lesson)

        self.assertFalse(lesson.is_published)
        self.assertFalse(lesson.is_active)

    def test_create_course_lesson_block_creates_block(self) -> None:
        """
        Сервис создаёт блок урока.
        """

        block = create_course_lesson_block(
            data={
                "lesson": self.lesson,
                "block_type": CourseLessonBlock.BlockTypeChoices.TEXT,
                "title": "Блок",
                "content": "Содержимое",
                "order": 1,
                "is_visible": True,
            }
        )

        self.assertEqual(block.lesson_id, self.lesson.id)
        self.assertEqual(block.title, "Блок")

    def test_update_course_lesson_block_updates_fields(self) -> None:
        """
        Сервис обновляет блок урока.
        """

        block = factory_create_course_lesson_block(lesson=self.lesson)

        updated_block = update_course_lesson_block(
            block=block,
            data={
                "title": "Обновлённый блок",
            },
        )

        self.assertEqual(updated_block.title, "Обновлённый блок")

    def test_hide_and_show_course_lesson_block_change_visibility(self) -> None:
        """
        Сервисы скрывают и показывают блок урока.
        """

        block = factory_create_course_lesson_block(
            lesson=self.lesson,
            is_visible=True,
        )

        hidden_block = hide_course_lesson_block(block=block)

        self.assertFalse(hidden_block.is_visible)

        shown_block = show_course_lesson_block(block=hidden_block)

        self.assertTrue(shown_block.is_visible)

    def test_create_course_material_link_creates_link(self) -> None:
        """
        Сервис создаёт связь курса с материалом.
        """

        link = create_course_material_link(
            data={
                "course": self.course,
                "section": self.section,
                "lesson": self.lesson,
                "material": self.material,
                "placement": CourseMaterialLink.PlacementChoices.LESSON,
                "order": 1,
                "is_required": True,
                "is_visible": True,
            }
        )

        self.assertEqual(link.course_id, self.course.id)
        self.assertEqual(link.material_id, self.material.id)

    def test_update_course_material_link_updates_fields(self) -> None:
        """
        Сервис обновляет связь курса с материалом.
        """

        link = factory_create_course_material_link(
            course=self.course,
            section=self.section,
            lesson=self.lesson,
            material=self.material,
        )

        updated_link = update_course_material_link(
            link=link,
            data={
                "notes": "Новая заметка",
                "is_required": True,
            },
        )

        self.assertEqual(updated_link.notes, "Новая заметка")
        self.assertTrue(updated_link.is_required)

    def test_hide_and_show_course_material_link_change_visibility(self) -> None:
        """
        Сервисы скрывают и показывают материал курса.
        """

        link = factory_create_course_material_link(
            course=self.course,
            section=self.section,
            lesson=self.lesson,
            material=self.material,
            is_visible=True,
        )

        hidden_link = hide_course_material_link(link=link)

        self.assertFalse(hidden_link.is_visible)

        shown_link = show_course_material_link(link=hidden_link)

        self.assertTrue(shown_link.is_visible)

    def test_recalculate_course_section_hours_sets_sum_from_lessons(self) -> None:
        """
        Сервис пересчитывает часы раздела по урокам.
        """

        factory_create_course_lesson(
            course=self.course,
            section=self.section,
            planned_hours=3,
            order=2,
        )

        section = recalculate_course_section_hours(section=self.section)

        self.assertEqual(section.planned_hours, 5)

    def test_reorder_course_sections_updates_order(self) -> None:
        """
        Сервис переупорядочивает разделы.
        """

        second_section = factory_create_course_section(
            course=self.course,
            order=2,
        )

        reorder_course_sections(
            course_id=self.course.id,
            ordered_section_ids=[
                second_section.id,
                self.section.id,
            ],
        )

        self.section.refresh_from_db()
        second_section.refresh_from_db()

        self.assertEqual(second_section.order, 1)
        self.assertEqual(self.section.order, 2)

    def test_reorder_course_lessons_updates_order(self) -> None:
        """
        Сервис переупорядочивает уроки.
        """

        second_lesson = factory_create_course_lesson(
            course=self.course,
            section=self.section,
            order=2,
        )

        reorder_course_lessons(
            course_id=self.course.id,
            section_id=self.section.id,
            ordered_lesson_ids=[
                second_lesson.id,
                self.lesson.id,
            ],
        )

        self.lesson.refresh_from_db()
        second_lesson.refresh_from_db()

        self.assertEqual(second_lesson.order, 1)
        self.assertEqual(self.lesson.order, 2)

    def test_reorder_lesson_blocks_updates_order(self) -> None:
        """
        Сервис переупорядочивает блоки урока.
        """

        first_block = factory_create_course_lesson_block(
            lesson=self.lesson,
            order=1,
        )
        second_block = factory_create_course_lesson_block(
            lesson=self.lesson,
            order=2,
            title="Второй блок",
        )

        reorder_lesson_blocks(
            lesson_id=self.lesson.id,
            ordered_block_ids=[
                second_block.id,
                first_block.id,
            ],
        )

        first_block.refresh_from_db()
        second_block.refresh_from_db()

        self.assertEqual(second_block.order, 1)
        self.assertEqual(first_block.order, 2)

    def test_reorder_course_material_links_updates_order(self) -> None:
        """
        Сервис переупорядочивает материалы курса.
        """

        first_link = factory_create_course_material_link(
            course=self.course,
            section=self.section,
            lesson=self.lesson,
            order=1,
        )
        second_link = factory_create_course_material_link(
            course=self.course,
            section=self.section,
            lesson=self.lesson,
            order=2,
        )

        reorder_course_material_links(
            course_id=self.course.id,
            ordered_link_ids=[
                second_link.id,
                first_link.id,
            ],
        )

        first_link.refresh_from_db()
        second_link.refresh_from_db()

        self.assertEqual(second_link.order, 1)
        self.assertEqual(first_link.order, 2)
