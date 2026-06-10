from __future__ import annotations

from django.db import models


class CourseLessonBlockQuerySet(models.QuerySet):
    """
    QuerySet блоков урока.
    """

    def visible(self):
        """
        Возвращает видимые блоки.
        """

        return self.filter(is_visible=True)

    def hidden(self):
        """
        Возвращает скрытые блоки.
        """

        return self.filter(is_visible=False)

    def by_type(self, block_type: str):
        """
        Фильтрует блоки по типу.
        """

        return self.filter(block_type=block_type)

    def for_lesson(self, lesson_id: int):
        """
        Фильтрует блоки по уроку.
        """

        return self.filter(lesson_id=lesson_id)

    def ordered_for_lesson(self):
        """
        Возвращает блоки в порядке урока.
        """

        return self.order_by("lesson", "order", "id")


class CourseLessonBlockManager(models.Manager.from_queryset(CourseLessonBlockQuerySet)):
    """
    Менеджер блоков урока.
    """

    use_in_migrations = False
