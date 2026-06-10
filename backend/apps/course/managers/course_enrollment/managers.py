from __future__ import annotations

from apps.course.constants import (
    ACTIVE_COURSE_ENROLLMENT_STATUS_CODES,
    COURSE_ENROLLMENT_STATUS_COMPLETED,
    COURSE_ENROLLMENT_STATUS_ENROLLED,
    COURSE_ENROLLMENT_STATUS_IN_PROGRESS,
    FINISHED_COURSE_ENROLLMENT_STATUS_CODES,
)
from django.db import models


class CourseEnrollmentQuerySet(models.QuerySet):
    """
    QuerySet записей обучающихся на курс.
    """

    def active(self):
        """
        Возвращает активные записи.
        """

        return self.filter(status__in=ACTIVE_COURSE_ENROLLMENT_STATUS_CODES)

    def finished(self):
        """
        Возвращает завершённые записи.
        """

        return self.filter(status__in=FINISHED_COURSE_ENROLLMENT_STATUS_CODES)

    def enrolled(self):
        """
        Возвращает записи в статусе зачисления.
        """

        return self.filter(status=COURSE_ENROLLMENT_STATUS_ENROLLED)

    def in_progress(self):
        """
        Возвращает записи в процессе обучения.
        """

        return self.filter(status=COURSE_ENROLLMENT_STATUS_IN_PROGRESS)

    def completed(self):
        """
        Возвращает завершённые курсы.
        """

        return self.filter(status=COURSE_ENROLLMENT_STATUS_COMPLETED)

    def for_course(self, course_id: int):
        """
        Фильтрует записи по курсу.
        """

        return self.filter(course_id=course_id)

    def for_learner(self, learner_id: int):
        """
        Фильтрует записи по обучающемуся.
        """

        return self.filter(learner_id=learner_id)

    def for_group_access(self, group_access_id: int):
        """
        Фильтрует записи по групповому доступу.
        """

        return self.filter(group_access_id=group_access_id)

    def for_access_rule(self, access_rule_id: int):
        """
        Фильтрует записи по правилу доступа.
        """

        return self.filter(access_rule_id=access_rule_id)

    def ordered_recent_activity(self):
        """
        Возвращает записи по последней активности.
        """

        return self.order_by("-last_activity_at", "-enrolled_at", "-id")


class CourseEnrollmentManager(models.Manager.from_queryset(CourseEnrollmentQuerySet)):
    """
    Менеджер записей обучающихся на курс.
    """

    use_in_migrations = False
