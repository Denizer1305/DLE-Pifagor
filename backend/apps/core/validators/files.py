from __future__ import annotations

from collections.abc import Iterable

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

IMAGE_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
    "webp",
    "svg",
}
"""Разрешённые расширения изображений."""


def get_file_extension(value) -> str:
    """
    Возвращает расширение файла в нижнем регистре.
    """

    file_name = getattr(value, "name", "")

    if "." not in file_name:
        return ""

    return file_name.rsplit(".", 1)[-1].lower()


def validate_file_size(max_size_mb: int):
    """
    Создаёт валидатор размера файла.
    """

    max_size_bytes = max_size_mb * 1024 * 1024

    def validator(file) -> None:
        """
        Проверяет размер файла.
        """

        if file.size > max_size_bytes:
            raise ValidationError(
                _("Размер файла не должен превышать %(max_size_mb)s МБ.")
                % {
                    "max_size_mb": max_size_mb,
                }
            )

    return validator


def validate_file_extension(
    value,
    *,
    allowed_extensions: Iterable[str],
    message: str | None = None,
) -> None:
    """
    Проверяет расширение файла.
    """

    normalized_extensions = {
        extension.lower().lstrip(".") for extension in allowed_extensions
    }
    extension = get_file_extension(value)

    if extension not in normalized_extensions:
        raise ValidationError(
            message
            or _("Недопустимый формат файла. Разрешённые форматы: %(extensions)s.")
            % {
                "extensions": ", ".join(sorted(normalized_extensions)),
            }
        )


def validate_image_extension(value) -> None:
    """
    Проверяет расширение изображения.

    Разрешённые форматы:
    - jpg;
    - jpeg;
    - png;
    - webp;
    - svg.
    """

    validate_file_extension(
        value,
        allowed_extensions=IMAGE_EXTENSIONS,
        message=_("Допустимые форматы изображения: jpg, jpeg, png, webp, svg."),
    )
