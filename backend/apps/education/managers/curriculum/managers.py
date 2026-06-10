from __future__ import annotations

from apps.education.constants import (
    CURRICULUM_STATUS_ACTIVE,
    CURRICULUM_STATUS_ARCHIVED,
    CURRICULUM_STATUS_DRAFT,
)
from django.db import models


class CurriculumQuerySet(models.QuerySet):
    """
    QuerySet учебных планов.
    """

    def active(self):
        """
        Возвращает активные учебные планы.
        """

        return self.filter(is_active=True)

    def inactive(self):
        """
        Возвращает неактивные учебные планы.
        """

        return self.filter(is_active=False)

    def draft(self):
        """
        Возвращает черновики учебных планов.
        """

        return self.filter(status=CURRICULUM_STATUS_DRAFT)

    def approved(self):
        """
        Возвращает активированные учебные планы.
        """

        return self.filter(status=CURRICULUM_STATUS_ACTIVE)

    def archived(self):
        """
        Возвращает архивные учебные планы.
        """

        return self.filter(status=CURRICULUM_STATUS_ARCHIVED)

    def for_organization(self, organization_id: int):
        """
        Фильтрует планы по организации.
        """

        return self.filter(organization_id=organization_id)

    def for_department(self, department_id: int):
        """
        Фильтрует планы по отделению.
        """

        return self.filter(department_id=department_id)

    def for_year(self, academic_year_id: int):
        """
        Фильтрует планы по учебному году.
        """

        return self.filter(academic_year_id=academic_year_id)

    def ordered_for_admin(self):
        """
        Возвращает планы в порядке для административного интерфейса.
        """

        return self.order_by(
            "organization",
            "-academic_year__start_date",
            "name",
        )


class CurriculumManager(models.Manager.from_queryset(CurriculumQuerySet)):
    """
    Менеджер учебных планов.
    """
