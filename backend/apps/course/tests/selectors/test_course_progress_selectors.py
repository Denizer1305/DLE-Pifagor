from __future__ import annotations

from apps.course.models import CourseEnrollment, LessonProgress
from apps.course.selectors import (
    course_progress_list_queryset,
    get_course_progress_by_enrollment_id,
    get_course_progress_by_id,
    get_lesson_progress_by_enrollment_and_lesson,
    get_lesson_progress_by_id,
    lesson_progress_list_queryset,
)
from apps.course.tests.factories import (
    create_course,
    create_course_enrollment,
    create_course_lesson,
    create_course_progress,
    create_learner,
    create_lesson_progress,
)
from django.test import TestCase


class CourseProgressSelectorsTestCase(TestCase):
    """
    Тесты селекторов прогресса курса.
    """

    def setUp(self) -> None:
        """
        Подготавливает прогресс курса и уроков.
        """

        self.course = create_course(
            title="Progress Selectors Course",
        )
        self.learner = create_learner(
            email="course-progress-selector-learner@example.com",
        )
        self.enrollment = create_course_enrollment(
            course=self.course,
            learner=self.learner,
            status=CourseEnrollment.StatusChoices.IN_PROGRESS,
            progress_percent=50,
        )
        self.lesson = create_course_lesson(
            course=self.course,
            title="Progress Lesson",
        )
        self.course_progress = create_course_progress(
            enrollment=self.enrollment,
            progress_percent=50,
            total_lessons_count=2,
            completed_lessons_count=1,
            last_lesson=self.lesson,
        )
        self.lesson_progress = create_lesson_progress(
            enrollment=self.enrollment,
            course_progress=self.course_progress,
            lesson=self.lesson,
            status=LessonProgress.StatusChoices.COMPLETED,
        )

    def test_course_progress_list_filters_by_enrollment(self) -> None:
        """
        Прогресс курса фильтруется по записи на курс.
        """

        progress_ids = set(
            course_progress_list_queryset(
                enrollment_id=self.enrollment.id,
            ).values_list(
                "id",
                flat=True,
            )
        )

        self.assertIn(self.course_progress.id, progress_ids)

    def test_course_progress_list_filters_by_course(self) -> None:
        """
        Прогресс курса фильтруется по курсу.
        """

        progress_ids = set(
            course_progress_list_queryset(
                course_id=self.course.id,
            ).values_list(
                "id",
                flat=True,
            )
        )

        self.assertIn(self.course_progress.id, progress_ids)

    def test_course_progress_list_filters_by_learner(self) -> None:
        """
        Прогресс курса фильтруется по обучающемуся.
        """

        progress_ids = set(
            course_progress_list_queryset(
                learner_id=self.learner.id,
            ).values_list(
                "id",
                flat=True,
            )
        )

        self.assertIn(self.course_progress.id, progress_ids)

    def test_course_progress_list_filters_by_completed_false(self) -> None:
        """
        Незавершённый прогресс возвращается при completed=False.
        """

        progress_ids = set(
            course_progress_list_queryset(
                completed=False,
            ).values_list(
                "id",
                flat=True,
            )
        )

        self.assertIn(self.course_progress.id, progress_ids)

    def test_get_course_progress_by_id_returns_progress(self) -> None:
        """
        Селектор возвращает прогресс курса по id.
        """

        progress = get_course_progress_by_id(self.course_progress.id)

        self.assertEqual(progress.id, self.course_progress.id)

    def test_get_course_progress_by_enrollment_id_returns_progress(self) -> None:
        """
        Селектор возвращает прогресс курса по записи.
        """

        progress = get_course_progress_by_enrollment_id(self.enrollment.id)

        self.assertEqual(progress.id, self.course_progress.id)

    def test_lesson_progress_list_filters_by_enrollment(self) -> None:
        """
        Прогресс урока фильтруется по записи на курс.
        """

        progress_ids = set(
            lesson_progress_list_queryset(
                enrollment_id=self.enrollment.id,
            ).values_list(
                "id",
                flat=True,
            )
        )

        self.assertIn(self.lesson_progress.id, progress_ids)

    def test_lesson_progress_list_filters_by_lesson(self) -> None:
        """
        Прогресс урока фильтруется по уроку.
        """

        progress_ids = set(
            lesson_progress_list_queryset(
                lesson_id=self.lesson.id,
            ).values_list(
                "id",
                flat=True,
            )
        )

        self.assertIn(self.lesson_progress.id, progress_ids)

    def test_lesson_progress_list_filters_by_course(self) -> None:
        """
        Прогресс урока фильтруется по курсу.
        """

        progress_ids = set(
            lesson_progress_list_queryset(
                course_id=self.course.id,
            ).values_list(
                "id",
                flat=True,
            )
        )

        self.assertIn(self.lesson_progress.id, progress_ids)

    def test_lesson_progress_list_filters_by_learner(self) -> None:
        """
        Прогресс урока фильтруется по обучающемуся.
        """

        progress_ids = set(
            lesson_progress_list_queryset(
                learner_id=self.learner.id,
            ).values_list(
                "id",
                flat=True,
            )
        )

        self.assertIn(self.lesson_progress.id, progress_ids)

    def test_lesson_progress_list_filters_by_status(self) -> None:
        """
        Прогресс урока фильтруется по статусу.
        """

        progress_ids = set(
            lesson_progress_list_queryset(
                status=LessonProgress.StatusChoices.COMPLETED,
            ).values_list(
                "id",
                flat=True,
            )
        )

        self.assertIn(self.lesson_progress.id, progress_ids)

    def test_get_lesson_progress_by_id_returns_progress(self) -> None:
        """
        Селектор возвращает прогресс урока по id.
        """

        progress = get_lesson_progress_by_id(self.lesson_progress.id)

        self.assertEqual(progress.id, self.lesson_progress.id)

    def test_get_lesson_progress_by_enrollment_and_lesson_returns_progress(
        self,
    ) -> None:
        """
        Селектор возвращает прогресс урока по записи и уроку.
        """

        progress = get_lesson_progress_by_enrollment_and_lesson(
            enrollment_id=self.enrollment.id,
            lesson_id=self.lesson.id,
        )

        self.assertEqual(progress.id, self.lesson_progress.id)
