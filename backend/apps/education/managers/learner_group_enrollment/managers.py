from __future__ import annotations

from apps.education.constants import (
    ENROLLMENT_STATUS_ACTIVE,
    FINISHED_ENROLLMENT_STATUS_CODES,
)
from django.db import models


class LearnerGroupEnrollmentQuerySet(models.QuerySet):
    """
    QuerySet академических зачислений обучающихся.
    """

    def active(self):
        """
        Возвращает активные зачисления.
        """

        return self.filter(status=ENROLLMENT_STATUS_ACTIVE)

    def finished(self):
        """
        Возвращает завершённые зачисления.
        """

        return self.filter(status__in=FINISHED_ENROLLMENT_STATUS_CODES)

    def primary(self):
        """
        Возвращает основные зачисления.
        """

        return self.filter(is_primary=True)

    def secondary(self):
        """
        Возвращает дополнительные зачисления.
        """

        return self.filter(is_primary=False)

    def for_learner(self, learner_id: int):
        """
        Фильтрует зачисления по обучающемуся.
        """

        return self.filter(learner_id=learner_id)

    def for_group(self, group_id: int):
        """
        Фильтрует зачисления по группе.
        """

        return self.filter(group_id=group_id)

    def for_year(self, academic_year_id: int):
        """
        Фильтрует зачисления по учебному году.
        """

        return self.filter(academic_year_id=academic_year_id)

    def for_organization(self, organization_id: int):
        """
        Фильтрует зачисления по организации группы.
        """

        return self.filter(group__organization_id=organization_id)

    def for_department(self, department_id: int):
        """
        Фильтрует зачисления по отделению группы.
        """

        return self.filter(group__department_id=department_id)

    def with_journal_number(self):
        """
        Возвращает зачисления с номером в журнале.
        """

        return self.filter(journal_number__isnull=False)

    def ordered_for_group_journal(self):
        """
        Возвращает зачисления в порядке журнала группы.
        """

        return self.order_by(
            "group",
            "journal_number",
            "learner",
        )


class LearnerGroupEnrollmentManager(
    models.Manager.from_queryset(LearnerGroupEnrollmentQuerySet)
):
    """
    Менеджер академических зачислений обучающихся.
    """
