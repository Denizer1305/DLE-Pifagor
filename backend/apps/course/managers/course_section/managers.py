from __future__ import annotations

from django.db import models


class CourseSectionQuerySet(models.QuerySet):
    """
    QuerySet разделов курса.
    """

    def active(self):
        """
        Возвращает активные разделы.
        """

        return self.filter(is_active=True)

    def inactive(self):
        """
        Возвращает неактивные разделы.
        """

        return self.filter(is_active=False)

    def published(self):
        """
        Возвращает опубликованные разделы.
        """

        return self.filter(is_published=True)

    def unpublished(self):
        """
        Возвращает неопубликованные разделы.
        """

        return self.filter(is_published=False)

    def required(self):
        """
        Возвращает обязательные разделы.
        """

        return self.filter(is_required=True)

    def optional(self):
        """
        Возвращает необязательные разделы.
        """

        return self.filter(is_required=False)

    def for_course(self, course_id: int):
        """
        Фильтрует разделы по курсу.
        """

        return self.filter(course_id=course_id)

    def ordered_for_course(self):
        """
        Возвращает разделы в порядке курса.
        """

        return self.order_by("course", "order", "section_number", "title")


class CourseSectionManager(models.Manager.from_queryset(CourseSectionQuerySet)):
    """
    Менеджер разделов курса.
    """

    use_in_migrations = False
