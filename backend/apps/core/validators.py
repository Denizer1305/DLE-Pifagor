import re
from datetime import date

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


PHONE_PATTERN = re.compile(r"^\+?[1-9]\d{7,14}$")


def validate_phone_number(value: str) -> None:
    """
    Проверяет номер телефона в международном формате.

    Допускает:
        - цифры;
        - необязательный символ + в начале;
        - длину от 8 до 15 цифр.

    Args:
        value:
            Номер телефона.

    Raises:
        ValidationError: Если номер телефона имеет неверный формат.
    """

    if not value:
        raise ValidationError(_("Номер телефона обязателен."))

    normalized_value = value.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")

    if not PHONE_PATTERN.match(normalized_value):
        raise ValidationError(
            _("Введите корректный номер телефона в международном формате.")
        )


def validate_birth_date_not_future(value: date) -> None:
    """
    Проверяет, что дата рождения не находится в будущем.

    Args:
        value:
            Дата рождения.

    Raises:
        ValidationError: Если дата рождения больше текущей даты.
    """

    if value and value > date.today():
        raise ValidationError(_("Дата рождения не может быть в будущем."))


def validate_file_size(max_size_mb: int):
    """
    Создаёт валидатор размера файла.

    Args:
        max_size_mb:
            Максимальный размер файла в мегабайтах.

    Returns:
        callable: Валидатор файла.
    """

    max_size_bytes = max_size_mb * 1024 * 1024

    def validator(file) -> None:
        """
        Проверяет размер файла.

        Args:
            file:
                Загруженный файл.

        Raises:
            ValidationError: Если файл превышает допустимый размер.
        """

        if file.size > max_size_bytes:
            raise ValidationError(
                _(f"Размер файла не должен превышать {max_size_mb} МБ.")
            )

    return validator


def validate_image_extension(value) -> None:
    """
    Проверяет расширение изображения.

    Разрешённые форматы:
        - jpg;
        - jpeg;
        - png;
        - webp;
        - svg.

    Args:
        value:
            Загруженный файл.

    Raises:
        ValidationError: Если расширение файла не поддерживается.
    """

    allowed_extensions = {"jpg", "jpeg", "png", "webp", "svg"}

    file_name = getattr(value, "name", "")
    extension = file_name.rsplit(".", 1)[-1].lower() if "." in file_name else ""

    if extension not in allowed_extensions:
        raise ValidationError(
            _("Допустимые форматы изображения: jpg, jpeg, png, webp, svg.")
        )


def validate_positive_integer(value: int) -> None:
    """
    Проверяет, что число является положительным.

    Args:
        value:
            Проверяемое число.

    Raises:
        ValidationError: Если число меньше или равно нулю.
    """

    if value <= 0:
        raise ValidationError(_("Значение должно быть положительным числом."))
