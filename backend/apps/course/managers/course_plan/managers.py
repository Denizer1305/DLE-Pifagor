from __future__ import annotations

from apps.course.constants import (
    COURSE_PLAN_STATUS_APPROVED,
    COURSE_PLAN_STATUS_ARCHIVED,
    COURSE_PLAN_STATUS_DRAFT,
    COURSE_PLAN_STATUS_IMPORTED,
    COURSE_PLAN_STATUS_REVIEWED,
)
from django.db import models


class CoursePlanQuerySet(models.QuerySet):
    """
    QuerySet КТП курса.
    """

    def active(self):
        """
        Возвращает активные КТП.
        """

        return self.filter(is_active=True)

    def inactive(self):
        """
        Возвращает неактивные КТП.
        """

        return self.filter(is_active=False)

    def draft(self):
        """
        Возвращает черновики КТП.
        """

        return self.filter(status=COURSE_PLAN_STATUS_DRAFT)

    def imported(self):
        """
        Возвращает импортированные КТП.
        """

        return self.filter(status=COURSE_PLAN_STATUS_IMPORTED)

    def reviewed(self):
        """
        Возвращает проверенные КТП.
        """

        return self.filter(status=COURSE_PLAN_STATUS_REVIEWED)

    def approved(self):
        """
        Возвращает утверждённые КТП.
        """

        return self.filter(status=COURSE_PLAN_STATUS_APPROVED)

    def archived(self):
        """
        Возвращает архивные КТП.
        """

        return self.filter(status=COURSE_PLAN_STATUS_ARCHIVED)

    def for_course(self, course_id: int):
        """
        Фильтрует КТП по курсу.
        """

        return self.filter(course_id=course_id)

    def ordered_for_admin(self):
        """
        Возвращает КТП в порядке для админки.
        """

        return self.order_by(
            "course__organization",
            "course__subject",
            "-updated_at",
        )


class CoursePlanManager(models.Manager.from_queryset(CoursePlanQuerySet)):
    """
    Менеджер КТП курса.
    """

    use_in_migrations = False
