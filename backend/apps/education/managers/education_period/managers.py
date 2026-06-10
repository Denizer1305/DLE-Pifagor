from __future__ import annotations

from django.db import models


class EducationPeriodQuerySet(models.QuerySet):
    """
    QuerySet учебных периодов.
    """

    def active(self):
        """
        Возвращает активные учебные периоды.
        """

        return self.filter(is_active=True)

    def inactive(self):
        """
        Возвращает неактивные учебные периоды.
        """

        return self.filter(is_active=False)

    def current(self):
        """
        Возвращает текущие учебные периоды.
        """

        return self.filter(is_current=True)

    def for_year(self, academic_year_id: int):
        """
        Фильтрует периоды по учебному году.
        """

        return self.filter(academic_year_id=academic_year_id)

    def by_type(self, period_type: str):
        """
        Фильтрует периоды по типу.
        """

        return self.filter(period_type=period_type)

    def ordered_for_year(self):
        """
        Возвращает периоды в порядке внутри учебного года.
        """

        return self.order_by("academic_year", "sequence", "start_date")


class EducationPeriodManager(models.Manager.from_queryset(EducationPeriodQuerySet)):
    """
    Менеджер учебных периодов.
    """
