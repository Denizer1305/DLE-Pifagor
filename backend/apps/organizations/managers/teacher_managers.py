from __future__ import annotations

from django.db import models
from django.db.models import Q
from django.utils import timezone


class CurrentDateRangeQuerySet(models.QuerySet):
    """
    QuerySet для моделей с is_active, starts_at и ends_at.
    """

    def active(self):
        """
        Возвращает активные записи.
        """

        return self.filter(is_active=True)

    def current(self):
        """
        Возвращает текущие активные записи с учётом дат.
        """

        today = timezone.localdate()

        return self.active().filter(
            Q(starts_at__isnull=True) | Q(starts_at__lte=today),
            Q(ends_at__isnull=True) | Q(ends_at__gte=today),
        )


class TeacherOrganizationManager(
    models.Manager.from_queryset(CurrentDateRangeQuerySet)
):
    """
    Менеджер связей преподавателей с организациями.
    """


class GroupCuratorManager(
    models.Manager.from_queryset(CurrentDateRangeQuerySet)
):
    """
    Менеджер кураторов групп.
    """