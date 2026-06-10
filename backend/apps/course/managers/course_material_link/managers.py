from __future__ import annotations

from django.db import models


class CourseMaterialLinkQuerySet(models.QuerySet):
    """
    QuerySet связей курса с материалами.
    """

    def visible(self):
        """
        Возвращает видимые материалы.
        """

        return self.filter(is_visible=True)

    def hidden(self):
        """
        Возвращает скрытые материалы.
        """

        return self.filter(is_visible=False)

    def required(self):
        """
        Возвращает обязательные материалы.
        """

        return self.filter(is_required=True)

    def optional(self):
        """
        Возвращает необязательные материалы.
        """

        return self.filter(is_required=False)

    def by_placement(self, placement: str):
        """
        Фильтрует материалы по месту размещения.
        """

        return self.filter(placement=placement)

    def for_course(self, course_id: int):
        """
        Фильтрует материалы по курсу.
        """

        return self.filter(course_id=course_id)

    def for_section(self, section_id: int):
        """
        Фильтрует материалы по разделу.
        """

        return self.filter(section_id=section_id)

    def for_lesson(self, lesson_id: int):
        """
        Фильтрует материалы по уроку.
        """

        return self.filter(lesson_id=lesson_id)

    def for_material(self, material_id: int):
        """
        Фильтрует связи по материалу.
        """

        return self.filter(material_id=material_id)

    def ordered_for_course(self):
        """
        Возвращает материалы в порядке курса.
        """

        return self.order_by(
            "course",
            "section__order",
            "lesson__order",
            "order",
            "id",
        )


class CourseMaterialLinkManager(
    models.Manager.from_queryset(CourseMaterialLinkQuerySet)
):
    """
    Менеджер связей курса с материалами.
    """

    use_in_migrations = False
