from __future__ import annotations

from django.db import models


class OrganizationQuerySet(models.QuerySet):
    """
    QuerySet образовательных организаций.
    """

    def active(self):
        """
        Возвращает активные организации.
        """

        return self.filter(is_active=True)

    def public(self):
        """
        Возвращает организации, доступные в публичной зоне.
        """

        return self.active().filter(is_public=True)

    def default_public(self):
        """
        Возвращает организацию по умолчанию для публичной зоны.
        """

        return self.public().filter(is_default_public=True)


class OrganizationManager(models.Manager.from_queryset(OrganizationQuerySet)):
    """
    Менеджер образовательных организаций.
    """