from __future__ import annotations

from apps.materials.constants import (
    MATERIAL_TYPE_ARCHIVE,
    MATERIAL_TYPE_CODE,
    MATERIAL_TYPE_DOCUMENT,
    MATERIAL_TYPE_EMBED,
    MATERIAL_TYPE_FILE,
    MATERIAL_TYPE_IMAGE,
    MATERIAL_TYPE_LINK,
    MATERIAL_TYPE_PRESENTATION,
    MATERIAL_TYPE_SPREADSHEET,
    MATERIAL_TYPE_TEXT,
    MATERIAL_TYPE_VIDEO,
    MAX_FILE_SIZE_BYTES,
    MAX_MATERIAL_VERSION_NUMBER,
    MIN_FILE_SIZE_BYTES,
    MIN_MATERIAL_VERSION_NUMBER,
)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_material_file_size(value) -> None:
    """
    Проверяет размер файла материала.
    """

    if not value:
        return

    file_size = getattr(value, "size", None)

    if file_size is None:
        return

    if file_size < MIN_FILE_SIZE_BYTES:
        raise ValidationError(_("Размер файла не может быть отрицательным."))

    if file_size > MAX_FILE_SIZE_BYTES:
        raise ValidationError(_("Файл материала слишком большой."))


def validate_material_version_number(value: int) -> None:
    """
    Проверяет номер версии материала.
    """

    if value < MIN_MATERIAL_VERSION_NUMBER:
        raise ValidationError(_("Номер версии должен быть положительным."))

    if value > MAX_MATERIAL_VERSION_NUMBER:
        raise ValidationError(_("Номер версии материала слишком большой."))


def validate_material_version_payload(
    *,
    material_type: str,
    file,
    external_url: str,
    content: str,
) -> None:
    """
    Проверяет содержимое версии материала в зависимости от типа материала.
    """

    errors: dict[str, str] = {}

    file_types = {
        MATERIAL_TYPE_FILE,
        MATERIAL_TYPE_IMAGE,
        MATERIAL_TYPE_PRESENTATION,
        MATERIAL_TYPE_DOCUMENT,
        MATERIAL_TYPE_SPREADSHEET,
        MATERIAL_TYPE_ARCHIVE,
    }
    url_types = {
        MATERIAL_TYPE_LINK,
        MATERIAL_TYPE_VIDEO,
        MATERIAL_TYPE_EMBED,
    }
    content_types = {
        MATERIAL_TYPE_TEXT,
        MATERIAL_TYPE_CODE,
    }

    if material_type in file_types and not file:
        errors["file"] = _("Для этого типа материала нужен файл.")

    if material_type in url_types and not external_url:
        errors["external_url"] = _("Для этого типа материала нужна ссылка.")

    if material_type in content_types and not content:
        errors["content"] = _("Для этого типа материала нужно содержимое.")

    if material_type == MATERIAL_TYPE_LINK and file:
        errors["file"] = _("Материал-ссылка не должен содержать файл.")

    if material_type == MATERIAL_TYPE_TEXT and file:
        errors["file"] = _("Текстовый материал не должен содержать файл.")

    if errors:
        raise ValidationError(errors)


def validate_current_version_flags(
    *,
    is_current: bool,
    status: str,
) -> None:
    """
    Проверяет флаг текущей версии.
    """

    if is_current and status == "archived":
        raise ValidationError(
            {"is_current": _("Архивная версия материала не может быть текущей.")}
        )
