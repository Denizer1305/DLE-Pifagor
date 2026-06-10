from __future__ import annotations

from apps.course.constants import (
    COURSE_PLAN_IMPORT_STATUS_APPLIED,
    COURSE_PLAN_IMPORT_STATUS_FAILED,
    COURSE_PLAN_IMPORT_STATUS_PARSED,
    COURSE_PLAN_IMPORT_STATUS_UPLOADED,
)
from django.db import models


class CoursePlanImportQuerySet(models.QuerySet):
    """
    QuerySet импортов КТП.
    """

    def uploaded(self):
        """
        Возвращает загруженные импорты.
        """

        return self.filter(status=COURSE_PLAN_IMPORT_STATUS_UPLOADED)

    def parsed(self):
        """
        Возвращает разобранные импорты.
        """

        return self.filter(status=COURSE_PLAN_IMPORT_STATUS_PARSED)

    def failed(self):
        """
        Возвращает неудачные импорты.
        """

        return self.filter(status=COURSE_PLAN_IMPORT_STATUS_FAILED)

    def applied(self):
        """
        Возвращает применённые импорты.
        """

        return self.filter(status=COURSE_PLAN_IMPORT_STATUS_APPLIED)

    def for_course_plan(self, course_plan_id: int):
        """
        Фильтрует импорты по КТП.
        """

        return self.filter(course_plan_id=course_plan_id)

    def by_importer(self, user_id: int):
        """
        Фильтрует импорты по пользователю.
        """

        return self.filter(imported_by_id=user_id)

    def ordered_recent(self):
        """
        Возвращает последние импорты первыми.
        """

        return self.order_by("-imported_at", "-id")


class CoursePlanImportManager(models.Manager.from_queryset(CoursePlanImportQuerySet)):
    """
    Менеджер импортов КТП.
    """

    use_in_migrations = False
