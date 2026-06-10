from __future__ import annotations

from django.db import models
from django.utils import timezone


class CourseLessonQuerySet(models.QuerySet):
    """
    QuerySet уроков курса.
    """

    def active(self):
        """
        Возвращает активные уроки.
        """

        return self.filter(is_active=True)

    def inactive(self):
        """
        Возвращает неактивные уроки.
        """

        return self.filter(is_active=False)

    def published(self):
        """
        Возвращает опубликованные уроки.
        """

        return self.filter(is_published=True)

    def unpublished(self):
        """
        Возвращает неопубликованные уроки.
        """

        return self.filter(is_published=False)

    def required(self):
        """
        Возвращает обязательные уроки.
        """

        return self.filter(is_required=True)

    def optional(self):
        """
        Возвращает необязательные уроки.
        """

        return self.filter(is_required=False)

    def preview(self):
        """
        Возвращает уроки для предпросмотра.
        """

        return self.filter(is_preview=True)

    def by_type(self, lesson_type: str):
        """
        Фильтрует уроки по типу.
        """

        return self.filter(lesson_type=lesson_type)

    def for_course(self, course_id: int):
        """
        Фильтрует уроки по курсу.
        """

        return self.filter(course_id=course_id)

    def for_section(self, section_id: int):
        """
        Фильтрует уроки по разделу.
        """

        return self.filter(section_id=section_id)

    def available_on_date(self, reference_datetime=None):
        """
        Возвращает уроки, доступные на указанную дату и время.
        """

        current_datetime = reference_datetime or timezone.now()

        return self.filter(
            models.Q(available_from__isnull=True)
            | models.Q(available_from__lte=current_datetime),
        )

    def ordered_for_course(self):
        """
        Возвращает уроки в порядке курса.
        """

        return self.order_by(
            "course",
            "section__order",
            "order",
            "lesson_number",
        )


class CourseLessonManager(models.Manager.from_queryset(CourseLessonQuerySet)):
    """
    Менеджер уроков курса.
    """

    use_in_migrations = False
