from __future__ import annotations

from apps.course.models import Course
from apps.course.services import (
    archive_course,
    create_course,
    duplicate_course,
    publish_course,
    restore_course,
    update_course,
)
from apps.course.tests.factories import create_academic_year
from apps.course.tests.factories import create_course as factory_create_course
from apps.course.tests.factories import (
    create_course_lesson,
    create_course_lesson_block,
    create_course_material_link,
    create_course_section,
    create_education_period,
    create_organization,
    create_subject,
    create_teacher,
    unique_code,
    unique_slug,
)
from django.test import TestCase


class CourseServicesTestCase(TestCase):
    """
    Тесты сервисов курсов.
    """

    def setUp(self) -> None:
        """
        Подготавливает данные.
        """

        self.teacher = create_teacher(
            email="course-services-teacher@example.com",
        )
        self.organization = create_organization()
        self.subject = create_subject()
        self.academic_year = create_academic_year()
        self.period = create_education_period(
            academic_year=self.academic_year,
        )

    def test_create_course_creates_course(self) -> None:
        """
        Сервис создаёт курс.
        """

        course = create_course(
            data={
                "code": unique_code("service_course"),
                "slug": unique_slug("service-course"),
                "title": "Сервисный курс",
                "course_type": Course.CourseTypeChoices.ACADEMIC,
                "origin": Course.OriginChoices.MANUAL,
                "status": Course.StatusChoices.DRAFT,
                "visibility": Course.VisibilityChoices.PRIVATE,
                "owner_teacher": self.teacher,
                "organization": self.organization,
                "subject": self.subject,
                "academic_year": self.academic_year,
                "period": self.period,
                "enrollment_code": unique_code("enroll"),
                "is_active": True,
            }
        )

        self.assertEqual(course.title, "Сервисный курс")
        self.assertEqual(course.owner_teacher_id, self.teacher.id)
        self.assertEqual(course.organization_id, self.organization.id)

    def test_update_course_updates_fields(self) -> None:
        """
        Сервис обновляет курс.
        """

        course = factory_create_course(
            owner_teacher=self.teacher,
            organization=self.organization,
            subject=self.subject,
            academic_year=self.academic_year,
            period=self.period,
        )

        updated_course = update_course(
            course=course,
            data={
                "title": "Обновлённый курс",
                "subtitle": "Новый подзаголовок",
            },
        )

        self.assertEqual(updated_course.title, "Обновлённый курс")
        self.assertEqual(updated_course.subtitle, "Новый подзаголовок")

    def test_publish_course_sets_published_status(self) -> None:
        """
        Сервис публикует курс.
        """

        course = factory_create_course(
            status=Course.StatusChoices.DRAFT,
            is_active=False,
        )

        published_course = publish_course(course=course)

        self.assertEqual(
            published_course.status,
            Course.StatusChoices.PUBLISHED,
        )
        self.assertTrue(published_course.is_active)
        self.assertIsNotNone(published_course.published_at)

    def test_archive_course_sets_archived_status(self) -> None:
        """
        Сервис архивирует курс.
        """

        course = factory_create_course(
            status=Course.StatusChoices.PUBLISHED,
            is_active=True,
        )

        archived_course = archive_course(course=course)

        self.assertEqual(
            archived_course.status,
            Course.StatusChoices.ARCHIVED,
        )
        self.assertFalse(archived_course.is_active)
        self.assertIsNotNone(archived_course.archived_at)

    def test_restore_course_returns_course_to_draft(self) -> None:
        """
        Сервис восстанавливает курс в черновик.
        """

        course = factory_create_course(
            status=Course.StatusChoices.ARCHIVED,
            is_active=False,
        )

        restored_course = restore_course(course=course)

        self.assertEqual(restored_course.status, Course.StatusChoices.DRAFT)
        self.assertTrue(restored_course.is_active)
        self.assertIsNone(restored_course.archived_at)

    def test_duplicate_course_copies_structure(self) -> None:
        """
        Сервис копирует курс вместе со структурой.
        """

        course = factory_create_course(
            owner_teacher=self.teacher,
            organization=self.organization,
            subject=self.subject,
            academic_year=self.academic_year,
            period=self.period,
        )
        section = create_course_section(course=course)
        lesson = create_course_lesson(course=course, section=section)
        create_course_lesson_block(lesson=lesson)
        create_course_material_link(
            course=course,
            section=section,
            lesson=lesson,
        )

        duplicated_course = duplicate_course(
            course=course,
            title="Копия курса",
            code=unique_code("course_copy"),
            slug=unique_slug("course-copy"),
        )

        self.assertNotEqual(duplicated_course.id, course.id)
        self.assertEqual(duplicated_course.title, "Копия курса")
        self.assertEqual(duplicated_course.sections.count(), 1)
        self.assertEqual(duplicated_course.lessons.count(), 1)
        self.assertEqual(duplicated_course.material_links.count(), 1)
