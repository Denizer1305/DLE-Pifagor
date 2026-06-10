from __future__ import annotations

from django.db import models


class AcademicYearQuerySet(models.QuerySet):
    """
    QuerySet учебных годов.
    """

    def active(self):
        """
        Возвращает активные учебные годы.
        """

        return self.filter(is_active=True)

    def inactive(self):
        """
        Возвращает неактивные учебные годы.
        """

        return self.filter(is_active=False)

    def current(self):
        """
        Возвращает текущий учебный год.
        """

        return self.filter(is_current=True)

    def by_name(self, name: str):
        """
        Фильтрует учебные годы по названию.
        """

        return self.filter(name=name)

    def ordered_for_admin(self):
        """
        Возвращает учебные годы в порядке для административного интерфейса.
        """

        return self.order_by("-start_date", "name")


class AcademicYearManager(models.Manager.from_queryset(AcademicYearQuerySet)):
    """
    Менеджер учебных годов.
    """
