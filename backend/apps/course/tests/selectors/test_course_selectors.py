from __future__ import annotations

from apps.course.models import Course
from apps.course.selectors import (
    course_base_queryset,
    course_detail_queryset,
    course_list_queryset,
    get_course_by_code,
    get_course_by_id,
    get_course_by_slug,
    get_teacher_courses,
    get_user_available_courses,
)
from apps.course.tests.factories import (
    create_academic_year,
    create_course,
    create_course_enrollment,
    create_education_period,
    create_learner,
    create_organization,
    create_subject,
    create_teacher,
    unique_code,
    unique_slug,
)
from django.test import TestCase


class CourseSelectorsTestCase(TestCase):
    """
    Тесты селекторов курсов.
    """

    def setUp(self) -> None:
        """
        Подготавливает общие данные.
        """

        self.organization = create_organization()
        self.subject = create_subject()
        self.academic_year = create_academic_year()
        self.period = create_education_period(
            academic_year=self.academic_year,
        )

        self.teacher = create_teacher(
            email="course-selectors-teacher@example.com",
        )
        self.other_teacher = create_teacher(
            email="course-selectors-other-teacher@example.com",
        )
        self.learner = create_learner(
            email="course-selectors-learner@example.com",
        )

        self.course = create_course(
            title="Alpha Programming Course",
            code=unique_code("alpha_course"),
            slug=unique_slug("alpha-course"),
            owner_teacher=self.teacher,
            organization=self.organization,
            subject=self.subject,
            academic_year=self.academic_year,
            period=self.period,
            status=Course.StatusChoices.PUBLISHED,
            is_active=True,
        )
        self.draft_course = create_course(
            title="Beta Draft Course",
            code=unique_code("beta_course"),
            slug=unique_slug("beta-course"),
            owner_teacher=self.teacher,
            organization=self.organization,
            subject=self.subject,
            academic_year=self.academic_year,
            period=self.period,
            status=Course.StatusChoices.DRAFT,
            is_active=True,
        )
        self.foreign_course = create_course(
            title="Foreign Hidden Course",
            code=unique_code("foreign_course"),
            slug=unique_slug("foreign-course"),
            owner_teacher=self.other_teacher,
            status=Course.StatusChoices.DRAFT,
            is_active=True,
        )

        self.enrollment = create_course_enrollment(
            course=self.course,
            learner=self.learner,
        )

    def test_course_base_queryset_contains_courses(self) -> None:
        """
        Базовый queryset возвращает курсы.
        """

        course_ids = set(
            course_base_queryset().values_list(
                "id",
                flat=True,
            )
        )

        self.assertIn(self.course.id, course_ids)
        self.assertIn(self.draft_course.id, course_ids)

    def test_course_list_queryset_filters_by_search(self) -> None:
        """
        Список курсов фильтруется по поисковой строке.
        """

        course_ids = set(
            course_list_queryset(search="Alpha").values_list(
                "id",
                flat=True,
            )
        )

        self.assertIn(self.course.id, course_ids)
        self.assertNotIn(self.draft_course.id, course_ids)

    def test_course_list_queryset_filters_by_status(self) -> None:
        """
        Список курсов фильтруется по статусу.
        """

        course_ids = set(
            course_list_queryset(
                status=Course.StatusChoices.PUBLISHED,
            ).values_list(
                "id",
                flat=True,
            )
        )

        self.assertIn(self.course.id, course_ids)
        self.assertNotIn(self.draft_course.id, course_ids)

    def test_course_list_queryset_filters_by_teacher(self) -> None:
        """
        Список курсов фильтруется по владельцу-преподавателю.
        """

        course_ids = set(
            course_list_queryset(
                owner_teacher_id=self.teacher.id,
            ).values_list(
                "id",
                flat=True,
            )
        )

        self.assertIn(self.course.id, course_ids)
        self.assertIn(self.draft_course.id, course_ids)
        self.assertNotIn(self.foreign_course.id, course_ids)

    def test_course_detail_queryset_contains_prefetched_course(self) -> None:
        """
        Детальный queryset возвращает курс.
        """

        course = course_detail_queryset().get(id=self.course.id)

        self.assertEqual(course.id, self.course.id)

    def test_get_course_by_id_returns_course(self) -> None:
        """
        Селектор возвращает курс по id.
        """

        course = get_course_by_id(self.course.id)

        self.assertEqual(course.id, self.course.id)

    def test_get_course_by_slug_returns_course(self) -> None:
        """
        Селектор возвращает курс по slug.
        """

        course = get_course_by_slug(self.course.slug)

        self.assertEqual(course.id, self.course.id)

    def test_get_course_by_code_returns_course(self) -> None:
        """
        Селектор возвращает курс по code.
        """

        course = get_course_by_code(self.course.code)

        self.assertEqual(course.id, self.course.id)

    def test_get_teacher_courses_returns_owner_courses(self) -> None:
        """
        Селектор возвращает курсы преподавателя.
        """

        course_ids = set(
            get_teacher_courses(
                teacher_id=self.teacher.id,
            ).values_list(
                "id",
                flat=True,
            )
        )

        self.assertIn(self.course.id, course_ids)
        self.assertIn(self.draft_course.id, course_ids)
        self.assertNotIn(self.foreign_course.id, course_ids)

    def test_get_user_available_courses_for_owner_teacher(self) -> None:
        """
        Владелец-преподаватель видит свои курсы.
        """

        course_ids = set(
            get_user_available_courses(
                user=self.teacher,
                is_active=None,
            ).values_list(
                "id",
                flat=True,
            )
        )

        self.assertIn(self.course.id, course_ids)
        self.assertIn(self.draft_course.id, course_ids)

    def test_get_user_available_courses_for_enrolled_learner(self) -> None:
        """
        Обучающийся видит курс, на который записан.
        """

        course_ids = set(
            get_user_available_courses(
                user=self.learner,
                is_active=None,
            ).values_list(
                "id",
                flat=True,
            )
        )

        self.assertIn(self.course.id, course_ids)
        self.assertNotIn(self.foreign_course.id, course_ids)
