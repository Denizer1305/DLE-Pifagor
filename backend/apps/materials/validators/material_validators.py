from __future__ import annotations

import re
from typing import Any

from apps.materials.constants import (
    MATERIAL_SLUG_MAX_LENGTH,
    MATERIAL_TAG_MAX_LENGTH,
    MATERIAL_TAGS_MAX_COUNT,
    MATERIAL_VISIBILITY_ORGANIZATION,
    MATERIAL_VISIBILITY_PUBLIC,
)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

MATERIAL_SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:[-_][a-z0-9]+)*$")


def validate_material_slug(value: str) -> None:
    """
    Проверяет slug материала.
    """

    if not value:
        raise ValidationError(_("Slug материала обязателен."))

    normalized_value = value.strip()

    if len(normalized_value) > MATERIAL_SLUG_MAX_LENGTH:
        raise ValidationError(_("Slug материала слишком длинный."))

    if not MATERIAL_SLUG_PATTERN.fullmatch(normalized_value):
        raise ValidationError(
            _(
                "Slug может содержать латинские строчные буквы, цифры, "
                "дефис и подчёркивание."
            )
        )


def validate_material_tags(value: Any) -> None:
    """
    Проверяет список тегов материала.
    """

    if value in (None, ""):
        return

    if not isinstance(value, list):
        raise ValidationError(_("Теги должны быть списком строк."))

    if len(value) > MATERIAL_TAGS_MAX_COUNT:
        raise ValidationError(_("Слишком много тегов у материала."))

    for tag in value:
        if not isinstance(tag, str):
            raise ValidationError(_("Каждый тег должен быть строкой."))

        normalized_tag = tag.strip()

        if not normalized_tag:
            raise ValidationError(_("Тег не может быть пустым."))

        if len(normalized_tag) > MATERIAL_TAG_MAX_LENGTH:
            raise ValidationError(_("Тег материала слишком длинный."))


def validate_material_visibility_scope(
    *,
    visibility: str,
    organization,
) -> None:
    """
    Проверяет согласованность видимости материала и организации.
    """

    if visibility == MATERIAL_VISIBILITY_ORGANIZATION and organization is None:
        raise ValidationError(
            {
                "organization": _(
                    "Для материала с видимостью внутри организации "
                    "нужно указать организацию."
                )
            }
        )

    if visibility == MATERIAL_VISIBILITY_PUBLIC and organization is None:
        return


def validate_material_category_parent(
    *,
    category,
    parent,
) -> None:
    """
    Проверяет родительскую категорию материала.
    """

    if category is None or parent is None:
        return

    if category.pk and parent.pk == category.pk:
        raise ValidationError(
            {"parent": _("Категория не может быть родителем самой себя.")}
        )

    if category.organization_id and parent.organization_id:
        if category.organization_id != parent.organization_id:
            raise ValidationError(
                {
                    "parent": _(
                        "Родительская категория должна относиться "
                        "к той же организации."
                    )
                }
            )

    if category.organization_id and parent.organization_id is None:
        return

    if category.organization_id is None and parent.organization_id:
        raise ValidationError(
            {
                "parent": _(
                    "Глобальная категория не может иметь родителя "
                    "из конкретной организации."
                )
            }
        )


def validate_material_publish_dates(
    *,
    published_at,
    archived_at,
) -> None:
    """
    Проверяет даты публикации и архивации материала.
    """

    if published_at and archived_at and archived_at < published_at:
        raise ValidationError(
            {"archived_at": _("Дата архивации не может быть раньше даты публикации.")}
        )
