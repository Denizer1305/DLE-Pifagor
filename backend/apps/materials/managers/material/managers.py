from __future__ import annotations

from apps.materials.constants import (
    MATERIAL_STATUS_ARCHIVED,
    MATERIAL_STATUS_DRAFT,
    MATERIAL_STATUS_PUBLISHED,
    MATERIAL_VISIBILITY_PUBLIC,
)
from django.db import models


class MaterialQuerySet(models.QuerySet):
    """
    QuerySet учебных материалов.
    """

    def active(self):
        """
        Возвращает активные материалы.
        """

        return self.filter(is_active=True)

    def inactive(self):
        """
        Возвращает неактивные материалы.
        """

        return self.filter(is_active=False)

    def draft(self):
        """
        Возвращает черновики материалов.
        """

        return self.filter(status=MATERIAL_STATUS_DRAFT)

    def published(self):
        """
        Возвращает опубликованные материалы.
        """

        return self.filter(status=MATERIAL_STATUS_PUBLISHED)

    def archived(self):
        """
        Возвращает архивные материалы.
        """

        return self.filter(status=MATERIAL_STATUS_ARCHIVED)

    def public(self):
        """
        Возвращает публичные материалы.
        """

        return self.filter(visibility=MATERIAL_VISIBILITY_PUBLIC)

    def by_type(self, material_type: str):
        """
        Фильтрует материалы по типу.
        """

        return self.filter(material_type=material_type)

    def by_visibility(self, visibility: str):
        """
        Фильтрует материалы по видимости.
        """

        return self.filter(visibility=visibility)

    def by_source(self, source: str):
        """
        Фильтрует материалы по источнику.
        """

        return self.filter(source=source)

    def owned_by(self, owner_id: int):
        """
        Фильтрует материалы по владельцу.
        """

        return self.filter(owner_id=owner_id)

    def for_organization(self, organization_id: int):
        """
        Фильтрует материалы по организации.
        """

        return self.filter(organization_id=organization_id)

    def global_materials(self):
        """
        Возвращает материалы без организации.
        """

        return self.filter(organization__isnull=True)

    def for_subject(self, subject_id: int):
        """
        Фильтрует материалы по предмету.
        """

        return self.filter(subject_id=subject_id)

    def for_category(self, category_id: int):
        """
        Фильтрует материалы по категории.
        """

        return self.filter(category_id=category_id)

    def with_current_version(self):
        """
        Возвращает материалы, у которых есть текущая версия.
        """

        return self.filter(current_version__isnull=False)

    def ordered_for_library(self):
        """
        Возвращает материалы в порядке библиотеки.
        """

        return self.order_by(
            "organization_id",
            "category_id",
            "-updated_at",
            "title",
        )

    def ordered_recent(self):
        """
        Возвращает последние обновлённые материалы.
        """

        return self.order_by("-updated_at", "-id")


class MaterialManager(models.Manager.from_queryset(MaterialQuerySet)):
    """
    Менеджер учебных материалов.
    """

    use_in_migrations = False
