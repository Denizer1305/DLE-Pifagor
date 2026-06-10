from __future__ import annotations

from django.db import models


class CurriculumItemQuerySet(models.QuerySet):
    """
    QuerySet элементов учебного плана.
    """

    def active(self):
        """
        Возвращает активные элементы учебного плана.
        """

        return self.filter(is_active=True)

    def inactive(self):
        """
        Возвращает неактивные элементы учебного плана.
        """

        return self.filter(is_active=False)

    def required(self):
        """
        Возвращает обязательные элементы учебного плана.
        """

        return self.filter(is_required=True)

    def optional(self):
        """
        Возвращает необязательные элементы учебного плана.
        """

        return self.filter(is_required=False)

    def for_curriculum(self, curriculum_id: int):
        """
        Фильтрует элементы по учебному плану.
        """

        return self.filter(curriculum_id=curriculum_id)

    def for_period(self, period_id: int):
        """
        Фильтрует элементы по учебному периоду.
        """

        return self.filter(period_id=period_id)

    def for_subject(self, subject_id: int):
        """
        Фильтрует элементы по предмету.
        """

        return self.filter(subject_id=subject_id)

    def ordered_for_curriculum(self):
        """
        Возвращает элементы в порядке внутри учебного плана.
        """

        return self.order_by(
            "curriculum",
            "period__sequence",
            "sequence",
            "subject",
        )


class CurriculumItemManager(models.Manager.from_queryset(CurriculumItemQuerySet)):
    """
    Менеджер элементов учебного плана.
    """
