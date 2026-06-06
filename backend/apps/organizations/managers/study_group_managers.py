from __future__ import annotations

from apps.organizations.constants import StudyGroupStatus
from django.db import models


class StudyGroupQuerySet(models.QuerySet):
    """
    QuerySet учебных групп.
    """

    def active(self):
        """
        Возвращает активные группы активных организаций.
        """

        return self.filter(
            is_active=True,
            organization__is_active=True,
        )

    def archived(self):
        """
        Возвращает архивные группы.
        """

        return self.filter(status=StudyGroupStatus.ARCHIVED)

    def for_organization(self, organization):
        """
        Возвращает группы организации.
        """

        if organization is None:
            return self.none()

        return self.filter(organization=organization)

    def for_department(self, department):
        """
        Возвращает группы отделения.
        """

        if department is None:
            return self.none()

        return self.filter(department=department)


class StudyGroupManager(models.Manager.from_queryset(StudyGroupQuerySet)):
    """
    Менеджер учебных групп.
    """