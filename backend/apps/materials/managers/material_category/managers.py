from __future__ import annotations

from django.db import models


class MaterialCategoryQuerySet(models.QuerySet):
    """
    QuerySet категорий материалов.
    """

    def active(self):
        """
        Возвращает активные категории.
        """

        return self.filter(is_active=True)

    def inactive(self):
        """
        Возвращает неактивные категории.
        """

        return self.filter(is_active=False)

    def global_categories(self):
        """
        Возвращает глобальные категории.
        """

        return self.filter(organization__isnull=True)

    def for_organization(self, organization_id: int):
        """
        Возвращает категории организации.
        """

        return self.filter(organization_id=organization_id)

    def root(self):
        """
        Возвращает корневые категории.
        """

        return self.filter(parent__isnull=True)

    def children_of(self, parent_id: int):
        """
        Возвращает дочерние категории.
        """

        return self.filter(parent_id=parent_id)

    def ordered_for_library(self):
        """
        Возвращает категории в порядке библиотеки.
        """

        return self.order_by(
            "organization_id",
            "parent_id",
            "name",
        )


class MaterialCategoryManager(models.Manager.from_queryset(MaterialCategoryQuerySet)):
    """
    Менеджер категорий материалов.
    """

    use_in_migrations = False
