from __future__ import annotations

from django.db import models

from apps.testing.constants import (
    BankItemStatus,
    BankItemVisibility,
)


class QuestionBankItemQuerySet(models.QuerySet):
    """
    QuerySet шаблонов вопросов банка тестовых заданий.
    """

    def active(self):
        """
        Возвращает активные шаблоны.
        """

        return self.filter(is_active=True)

    def published(self):
        """
        Возвращает опубликованные шаблоны.
        """

        return self.filter(
            status=BankItemStatus.PUBLISHED,
            is_active=True,
        )

    def archived(self):
        """
        Возвращает архивные шаблоны.
        """

        return self.filter(status=BankItemStatus.ARCHIVED)

    def for_teacher(self, teacher_id: int):
        """
        Фильтрует шаблоны по преподавателю-владельцу.
        """

        return self.filter(owner_teacher_id=teacher_id)

    def for_organization(self, organization_id: int):
        """
        Фильтрует шаблоны по организации.
        """

        return self.filter(organization_id=organization_id)

    def for_subject(self, subject_id: int):
        """
        Фильтрует шаблоны по предмету.
        """

        return self.filter(subject_id=subject_id)

    def reusable_for_teacher(
        self,
        *,
        teacher_id: int,
        organization_id: int | None = None,
    ):
        """
        Возвращает шаблоны, доступные преподавателю для переиспользования.
        """

        queryset = self.published()

        private_queryset = queryset.filter(
            visibility=BankItemVisibility.PRIVATE,
            owner_teacher_id=teacher_id,
        )
        public_queryset = queryset.filter(
            visibility=BankItemVisibility.PUBLIC,
        )

        if organization_id is None:
            return private_queryset | public_queryset

        organization_queryset = queryset.filter(
            visibility=BankItemVisibility.ORGANIZATION,
            organization_id=organization_id,
        )

        return private_queryset | organization_queryset | public_queryset


class QuestionBankOptionQuerySet(models.QuerySet):
    """
    QuerySet вариантов ответа шаблона вопроса.
    """

    def active(self):
        """
        Возвращает активные варианты.
        """

        return self.filter(is_active=True)

    def for_bank_item(self, bank_item_id: int):
        """
        Фильтрует варианты по шаблону вопроса.
        """

        return self.filter(bank_item_id=bank_item_id)

    def correct(self):
        """
        Возвращает правильные варианты.
        """

        return self.filter(is_correct=True)

    def incorrect(self):
        """
        Возвращает неправильные варианты.
        """

        return self.filter(is_correct=False)