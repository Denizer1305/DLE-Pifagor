from __future__ import annotations

from apps.course.constants import (
    LESSON_PROGRESS_STATUS_COMPLETED,
    LESSON_PROGRESS_STATUS_IN_PROGRESS,
    LESSON_PROGRESS_STATUS_NOT_STARTED,
    LESSON_PROGRESS_STATUS_SKIPPED,
)
from django.db import models


class LessonProgressQuerySet(models.QuerySet):
    """
    QuerySet прогресса по урокам.
    """

    def not_started(self):
        """
        Возвращает непройденные уроки.
        """

        return self.filter(status=LESSON_PROGRESS_STATUS_NOT_STARTED)

    def in_progress(self):
        """
        Возвращает уроки в процессе прохождения.
        """

        return self.filter(status=LESSON_PROGRESS_STATUS_IN_PROGRESS)

    def completed(self):
        """
        Возвращает завершённые уроки.
        """

        return self.filter(status=LESSON_PROGRESS_STATUS_COMPLETED)

    def skipped(self):
        """
        Возвращает пропущенные уроки.
        """

        return self.filter(status=LESSON_PROGRESS_STATUS_SKIPPED)

    def for_enrollment(self, enrollment_id: int):
        """
        Фильтрует прогресс по записи на курс.
        """

        return self.filter(enrollment_id=enrollment_id)

    def for_course_progress(self, course_progress_id: int):
        """
        Фильтрует прогресс по агрегированному прогрессу курса.
        """

        return self.filter(course_progress_id=course_progress_id)

    def for_lesson(self, lesson_id: int):
        """
        Фильтрует прогресс по уроку.
        """

        return self.filter(lesson_id=lesson_id)

    def for_course(self, course_id: int):
        """
        Фильтрует прогресс по курсу.
        """

        return self.filter(enrollment__course_id=course_id)

    def for_learner(self, learner_id: int):
        """
        Фильтрует прогресс по обучающемуся.
        """

        return self.filter(enrollment__learner_id=learner_id)

    def ordered_for_course(self):
        """
        Возвращает прогресс в порядке уроков курса.
        """

        return self.order_by(
            "lesson__section__order",
            "lesson__order",
            "lesson__lesson_number",
        )


class LessonProgressManager(models.Manager.from_queryset(LessonProgressQuerySet)):
    """
    Менеджер прогресса уроков.
    """

    use_in_migrations = False
