from __future__ import annotations

from django.db import models


class DepartmentQuerySet(models.QuerySet):
    """
    QuerySet отделений.
    """

    def active(self):
        """
        Возвращает активные отделения активных организаций.
        """

        return self.filter(
            is_active=True,
            organization__is_active=True,
        )

    def for_organization(self, organization):
        """
        Возвращает отделения организации.
        """

        if organization is None:
            return self.none()

        return self.filter(organization=organization)


class DepartmentManager(models.Manager.from_queryset(DepartmentQuerySet)):
    """
    Менеджер отделений.
    """
