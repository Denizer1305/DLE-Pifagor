from __future__ import annotations

from apps.materials.constants import (
    MATERIAL_VERSION_STATUS_ARCHIVED,
    MATERIAL_VERSION_STATUS_CURRENT,
    MATERIAL_VERSION_STATUS_DRAFT,
)
from django.db import models


class MaterialVersionQuerySet(models.QuerySet):
    """
    QuerySet версий материалов.
    """

    def draft(self):
        """
        Возвращает черновые версии.
        """

        return self.filter(status=MATERIAL_VERSION_STATUS_DRAFT)

    def current(self):
        """
        Возвращает текущие версии.
        """

        return self.filter(
            status=MATERIAL_VERSION_STATUS_CURRENT,
            is_current=True,
        )

    def archived(self):
        """
        Возвращает архивные версии.
        """

        return self.filter(status=MATERIAL_VERSION_STATUS_ARCHIVED)

    def for_material(self, material_id: int):
        """
        Фильтрует версии по материалу.
        """

        return self.filter(material_id=material_id)

    def by_creator(self, user_id: int):
        """
        Фильтрует версии по автору версии.
        """

        return self.filter(created_by_id=user_id)

    def ordered_for_material(self):
        """
        Возвращает версии в порядке материала.
        """

        return self.order_by(
            "material_id",
            "-version_number",
            "-created_at",
        )


class MaterialVersionManager(models.Manager.from_queryset(MaterialVersionQuerySet)):
    """
    Менеджер версий материалов.
    """

    use_in_migrations = False
