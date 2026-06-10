from __future__ import annotations

from django.db import models


class GroupSubjectQuerySet(models.QuerySet):
    """
    QuerySet предметов учебных групп.
    """

    def active(self):
        """
        Возвращает активные предметы групп.
        """

        return self.filter(is_active=True)

    def inactive(self):
        """
        Возвращает неактивные предметы групп.
        """

        return self.filter(is_active=False)

    def required(self):
        """
        Возвращает обязательные предметы групп.
        """

        return self.filter(is_required=True)

    def optional(self):
        """
        Возвращает необязательные предметы групп.
        """

        return self.filter(is_required=False)

    def for_group(self, group_id: int):
        """
        Фильтрует предметы по учебной группе.
        """

        return self.filter(group_id=group_id)

    def for_subject(self, subject_id: int):
        """
        Фильтрует предметы по предмету.
        """

        return self.filter(subject_id=subject_id)

    def for_year(self, academic_year_id: int):
        """
        Фильтрует предметы по учебному году.
        """

        return self.filter(academic_year_id=academic_year_id)

    def for_period(self, period_id: int):
        """
        Фильтрует предметы по учебному периоду.
        """

        return self.filter(period_id=period_id)

    def for_organization(self, organization_id: int):
        """
        Фильтрует предметы по организации группы.
        """

        return self.filter(group__organization_id=organization_id)

    def for_department(self, department_id: int):
        """
        Фильтрует предметы по отделению группы.
        """

        return self.filter(group__department_id=department_id)

    def ordered_for_group(self):
        """
        Возвращает предметы в порядке внутри группы.
        """

        return self.order_by(
            "group",
            "period__sequence",
            "subject",
        )


class GroupSubjectManager(models.Manager.from_queryset(GroupSubjectQuerySet)):
    """
    Менеджер предметов учебных групп.
    """
