from __future__ import annotations

from django.db import models


class CourseProgressQuerySet(models.QuerySet):
    """
    QuerySet прогресса по курсу.
    """

    def completed(self):
        """
        Возвращает завершённый прогресс.
        """

        return self.filter(progress_percent=100)

    def not_completed(self):
        """
        Возвращает незавершённый прогресс.
        """

        return self.filter(progress_percent__lt=100)

    def for_enrollment(self, enrollment_id: int):
        """
        Фильтрует прогресс по записи на курс.
        """

        return self.filter(enrollment_id=enrollment_id)

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

    def ordered_recent_activity(self):
        """
        Возвращает прогресс по последней активности.
        """

        return self.order_by("-last_activity_at", "-updated_at", "-id")


class CourseProgressManager(models.Manager.from_queryset(CourseProgressQuerySet)):
    """
    Менеджер прогресса курса.
    """

    use_in_migrations = False
