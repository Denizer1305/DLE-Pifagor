from __future__ import annotations

from apps.materials.models import MaterialVersion
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_material_version_can_be_saved(
    *,
    version: MaterialVersion,
) -> None:
    """
    Проверяет, что версию материала можно сохранить.
    """

    if not version.material_id:
        raise ValidationError({"material": _("Для версии нужно указать материал.")})
