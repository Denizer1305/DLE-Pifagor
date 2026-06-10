from __future__ import annotations

from apps.course.models import CourseEnrollment, LessonProgress
from apps.course.services import (
    complete_lesson_progress,
    ensure_course_progress,
    ensure_lesson_progress,
    ensure_lesson_progresses_for_enrollment,
    recalculate_course_progress,
    reset_lesson_progress,
    start_lesson_progress,
    track_lesson_completed,
    track_lesson_opened,
)
from apps.course.tests.factories import (
    create_course,
    create_course_enrollment,
    create_course_lesson,
    create_course_progress,
    create_learner,
    create_lesson_progress,
    get_choice_value,
)
from django.test import TestCase


class CourseProgressServicesTestCase(TestCase):
    """
    Тесты сервисов прогресса курса.
    """

    def setUp(self) -> None:
        """
        Подготавливает курс, уроки и запись.
        """

        self.course = create_course()
        self.learner = create_learner(
            email="course-progress-services-learner@example.com",
        )
        self.enrollment = create_course_enrollment(
            course=self.course,
            learner=self.learner,
            progress_percent=0,
        )
        self.lesson = create_course_lesson(
            course=self.course,
            title="Первый урок прогресса",
            is_published=True,
            is_active=True,
        )
        self.second_lesson = create_course_lesson(
            course=self.course,
            title="Второй урок прогресса",
            order=2,
            lesson_number=2,
            is_published=True,
            is_active=True,
        )

    def test_ensure_course_progress_creates_progress(self) -> None:
        """
        Сервис гарантирует наличие прогресса курса.
        """

        progress = ensure_course_progress(enrollment=self.enrollment)

        self.assertEqual(progress.enrollment_id, self.enrollment.id)

    def test_ensure_lesson_progress_creates_progress(self) -> None:
        """
        Сервис гарантирует наличие прогресса урока.
        """

        lesson_progress = ensure_lesson_progress(
            enrollment=self.enrollment,
            lesson=self.lesson,
        )

        self.assertEqual(lesson_progress.enrollment_id, self.enrollment.id)
        self.assertEqual(lesson_progress.lesson_id, self.lesson.id)

    def test_ensure_lesson_progresses_for_enrollment_creates_missing(self) -> None:
        """
        Сервис создаёт недостающий прогресс по урокам.
        """

        result = ensure_lesson_progresses_for_enrollment(
            enrollment=self.enrollment,
        )

        self.assertEqual(result["created"], 2)

    def test_start_lesson_progress_sets_in_progress_status(self) -> None:
        """
        Сервис запускает прогресс урока.
        """

        lesson_progress = create_lesson_progress(
            enrollment=self.enrollment,
            lesson=self.lesson,
        )

        started_progress = start_lesson_progress(
            lesson_progress=lesson_progress,
        )

        expected_status = get_choice_value(
            LessonProgress,
            "StatusChoices",
            "IN_PROGRESS",
            default="in_progress",
        )

        self.assertEqual(started_progress.status, expected_status)
        self.assertIsNotNone(started_progress.started_at)

    def test_complete_lesson_progress_sets_completed_status(self) -> None:
        """
        Сервис завершает прогресс урока.
        """

        lesson_progress = create_lesson_progress(
            enrollment=self.enrollment,
            lesson=self.lesson,
        )

        completed_progress = complete_lesson_progress(
            lesson_progress=lesson_progress,
        )

        expected_status = get_choice_value(
            LessonProgress,
            "StatusChoices",
            "COMPLETED",
            default="completed",
        )

        self.assertEqual(completed_progress.status, expected_status)
        self.assertIsNotNone(completed_progress.completed_at)

    def test_reset_lesson_progress_sets_initial_status(self) -> None:
        """
        Сервис сбрасывает прогресс урока.
        """

        lesson_progress = create_lesson_progress(
            enrollment=self.enrollment,
            lesson=self.lesson,
            status=get_choice_value(
                LessonProgress,
                "StatusChoices",
                "COMPLETED",
                default="completed",
            ),
        )

        reset_progress = reset_lesson_progress(
            lesson_progress=lesson_progress,
        )

        initial_status = get_choice_value(
            LessonProgress,
            "StatusChoices",
            "NOT_STARTED",
            "ACTIVE",
            "NEW",
            default=reset_progress.status,
        )

        self.assertEqual(reset_progress.status, initial_status)
        self.assertIsNone(reset_progress.completed_at)

    def test_recalculate_course_progress_counts_completed_lessons(self) -> None:
        """
        Сервис пересчитывает общий прогресс курса.
        """

        course_progress = create_course_progress(
            enrollment=self.enrollment,
        )
        create_lesson_progress(
            enrollment=self.enrollment,
            course_progress=course_progress,
            lesson=self.lesson,
            status=get_choice_value(
                LessonProgress,
                "StatusChoices",
                "COMPLETED",
                default="completed",
            ),
        )

        progress = recalculate_course_progress(
            enrollment=self.enrollment,
        )

        self.assertEqual(progress.total_lessons_count, 2)
        self.assertEqual(progress.completed_lessons_count, 1)
        self.assertEqual(progress.progress_percent, 50)

    def test_track_lesson_opened_creates_and_starts_progress(self) -> None:
        """
        Сервис фиксирует открытие урока.
        """

        result = track_lesson_opened(
            enrollment=self.enrollment,
            lesson=self.lesson,
        )

        self.assertIn("lesson_progress", result)
        self.assertIn("course_progress", result)

        self.enrollment.refresh_from_db()

        self.assertEqual(
            self.enrollment.status,
            CourseEnrollment.StatusChoices.IN_PROGRESS,
        )

    def test_track_lesson_completed_completes_progress(self) -> None:
        """
        Сервис фиксирует завершение урока.
        """

        result = track_lesson_completed(
            enrollment=self.enrollment,
            lesson=self.lesson,
        )

        lesson_progress = result["lesson_progress"]
        expected_status = get_choice_value(
            LessonProgress,
            "StatusChoices",
            "COMPLETED",
            default="completed",
        )

        self.assertEqual(lesson_progress.status, expected_status)
