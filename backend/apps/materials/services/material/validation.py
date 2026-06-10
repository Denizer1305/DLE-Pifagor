from __future__ import annotations

from apps.materials.models import Material
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_material_can_be_saved(
    *,
    material: Material,
) -> None:
    """
    Проверяет, что материал можно сохранить.
    """

    errors: dict[str, str] = {}

    if material.category_id:
        category = material.category

        if category.organization_id and not material.organization_id:
            errors["organization"] = _(
                "Для материала в организационной категории нужна организация."
            )

        if (
            category.organization_id
            and material.organization_id
            and category.organization_id != material.organization_id
        ):
            errors["category"] = _("Категория должна относиться к той же организации.")

    if material.current_version_id and material.pk:
        if material.current_version.material_id != material.pk:
            errors["current_version"] = _(
                "Текущая версия должна относиться к этому материалу."
            )

    if errors:
        raise ValidationError(errors)
