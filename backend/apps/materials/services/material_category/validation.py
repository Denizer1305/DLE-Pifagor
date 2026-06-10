from __future__ import annotations

from apps.materials.models import MaterialCategory
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_material_category_can_be_saved(
    *,
    category: MaterialCategory,
) -> None:
    """
    Проверяет, что категорию материала можно сохранить.
    """

    if category.parent_id and category.pk:
        if category.parent_id == category.pk:
            raise ValidationError(
                {"parent": _("Категория не может быть родителем самой себя.")}
            )

    if category.parent_id and category.organization_id:
        if (
            category.parent.organization_id
            and category.parent.organization_id != category.organization_id
        ):
            raise ValidationError(
                {
                    "parent": _(
                        "Родительская категория должна относиться "
                        "к той же организации."
                    )
                }
            )
