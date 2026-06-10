from __future__ import annotations

from apps.materials.constants import (
    MATERIAL_CATEGORY_NAME_MAX_LENGTH,
    MATERIAL_CATEGORY_SLUG_MAX_LENGTH,
)
from apps.materials.managers import MaterialCategoryManager
from apps.materials.validators import (
    validate_material_category_parent,
    validate_material_slug,
)
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class MaterialCategory(models.Model):
    """
    Категория учебных материалов.

    Категория может быть глобальной или привязанной к организации.
    Глобальные категории доступны как общая библиотечная структура,
    организационные категории используются внутри конкретной организации.
    """

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="material_categories",
        verbose_name=_("Организация"),
        blank=True,
        null=True,
    )
    parent = models.ForeignKey(
        "materials.MaterialCategory",
        on_delete=models.CASCADE,
        related_name="children",
        verbose_name=_("Родительская категория"),
        blank=True,
        null=True,
    )

    name = models.CharField(
        _("Название"),
        max_length=MATERIAL_CATEGORY_NAME_MAX_LENGTH,
    )
    slug = models.SlugField(
        _("Slug"),
        max_length=MATERIAL_CATEGORY_SLUG_MAX_LENGTH,
        validators=[validate_material_slug],
    )
    description = models.TextField(
        _("Описание"),
        blank=True,
    )
    is_active = models.BooleanField(
        _("Активна"),
        default=True,
    )

    created_at = models.DateTimeField(
        _("Дата создания"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _("Дата обновления"),
        auto_now=True,
    )

    objects = MaterialCategoryManager()

    class Meta:
        db_table = "materials_category"
        verbose_name = _("Категория материала")
        verbose_name_plural = _("Категории материалов")
        ordering = (
            "organization_id",
            "parent_id",
            "name",
        )
        constraints = [
            models.UniqueConstraint(
                fields=(
                    "organization",
                    "slug",
                ),
                condition=models.Q(organization__isnull=False),
                name="mat_cat_unique_org_slug",
            ),
            models.UniqueConstraint(
                fields=("slug",),
                condition=models.Q(organization__isnull=True),
                name="mat_cat_unique_global_slug",
            ),
        ]
        indexes = [
            models.Index(
                fields=("organization",),
                name="mat_category_org_idx",
            ),
            models.Index(
                fields=("parent",),
                name="mat_category_parent_idx",
            ),
            models.Index(
                fields=("slug",),
                name="mat_category_slug_idx",
            ),
            models.Index(
                fields=("is_active",),
                name="mat_category_active_idx",
            ),
        ]

    def __str__(self) -> str:
        return self.name

    def clean(self) -> None:
        """
        Проверяет категорию материала.
        """

        super().clean()

        try:
            validate_material_category_parent(
                category=self,
                parent=self.parent,
            )
        except ValidationError as error:
            raise error
