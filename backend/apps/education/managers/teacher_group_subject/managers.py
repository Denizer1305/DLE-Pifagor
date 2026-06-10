from __future__ import annotations

from django.db import models


class TeacherGroupSubjectQuerySet(models.QuerySet):
    """
    QuerySet назначений преподавателей на предметы групп.
    """

    def active(self):
        """
        Возвращает активные назначения.
        """

        return self.filter(is_active=True)

    def inactive(self):
        """
        Возвращает неактивные назначения.
        """

        return self.filter(is_active=False)

    def primary(self):
        """
        Возвращает основные назначения.
        """

        return self.filter(is_primary=True)

    def secondary(self):
        """
        Возвращает дополнительные назначения.
        """

        return self.filter(is_primary=False)

    def for_teacher(self, teacher_id: int):
        """
        Фильтрует назначения по преподавателю.
        """

        return self.filter(teacher_id=teacher_id)

    def for_group_subject(self, group_subject_id: int):
        """
        Фильтрует назначения по предмету группы.
        """

        return self.filter(group_subject_id=group_subject_id)

    def for_group(self, group_id: int):
        """
        Фильтрует назначения по учебной группе.
        """

        return self.filter(group_subject__group_id=group_id)

    def for_subject(self, subject_id: int):
        """
        Фильтрует назначения по предмету.
        """

        return self.filter(group_subject__subject_id=subject_id)

    def for_year(self, academic_year_id: int):
        """
        Фильтрует назначения по учебному году.
        """

        return self.filter(group_subject__academic_year_id=academic_year_id)

    def for_period(self, period_id: int):
        """
        Фильтрует назначения по учебному периоду.
        """

        return self.filter(group_subject__period_id=period_id)

    def for_organization(self, organization_id: int):
        """
        Фильтрует назначения по организации группы.
        """

        return self.filter(
            group_subject__group__organization_id=organization_id,
        )

    def ordered_for_group_subject(self):
        """
        Возвращает назначения в порядке внутри предмета группы.
        """

        return self.order_by(
            "group_subject",
            "-is_primary",
            "teacher",
        )


class TeacherGroupSubjectManager(
    models.Manager.from_queryset(TeacherGroupSubjectQuerySet)
):
    """
    Менеджер назначений преподавателей на предметы групп.
    """
