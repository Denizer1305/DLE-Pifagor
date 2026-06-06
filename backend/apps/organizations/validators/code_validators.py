from __future__ import annotations

from apps.organizations.constants import (
    MAX_GROUP_JOIN_CODE_LENGTH,
    MAX_TEACHER_REGISTRATION_CODE_LENGTH,
    MIN_GROUP_JOIN_CODE_LENGTH,
    MIN_TEACHER_REGISTRATION_CODE_LENGTH,
)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_raw_code(
    *,
    raw_code: str,
    min_length: int,
    max_length: int,
    field_name: str,
    empty_message: str,
    min_length_message: str,
    max_length_message: str,
) -> None:
    """
    Проверяет открытое значение кода.

    Args:
        raw_code:
            Открытое значение кода.
        min_length:
            Минимальная длина.
        max_length:
            Максимальная длина.
        field_name:
            Имя поля для ValidationError.
        empty_message:
            Сообщение, если код пустой.
        min_length_message:
            Сообщение, если код слишком короткий.
        max_length_message:
            Сообщение, если код слишком длинный.

    Raises:
        ValidationError: Если код некорректен.
    """

    normalized_code = (raw_code or "").strip()

    if not normalized_code:
        raise ValidationError(
            {
                field_name: _(empty_message),
            }
        )

    if len(normalized_code) < min_length:
        raise ValidationError(
            {
                field_name: _(min_length_message),
            }
        )

    if len(normalized_code) > max_length:
        raise ValidationError(
            {
                field_name: _(max_length_message),
            }
        )


def validate_raw_teacher_registration_code(raw_code: str) -> None:
    """
    Проверяет открытый код регистрации преподавателя.

    Args:
        raw_code:
            Открытое значение кода.

    Raises:
        ValidationError: Если код некорректен.
    """

    validate_raw_code(
        raw_code=raw_code,
        min_length=MIN_TEACHER_REGISTRATION_CODE_LENGTH,
        max_length=MAX_TEACHER_REGISTRATION_CODE_LENGTH,
        field_name="teacher_registration_code",
        empty_message="Код регистрации преподавателя не может быть пустым.",
        min_length_message=(
            "Код регистрации преподавателя короче минимальной длины."
        ),
        max_length_message=(
            "Код регистрации преподавателя превышает максимальную длину."
        ),
    )


def validate_raw_group_join_code(raw_code: str) -> None:
    """
    Проверяет открытый код вступления в группу.

    Args:
        raw_code:
            Открытое значение кода.

    Raises:
        ValidationError: Если код некорректен.
    """

    validate_raw_code(
        raw_code=raw_code,
        min_length=MIN_GROUP_JOIN_CODE_LENGTH,
        max_length=MAX_GROUP_JOIN_CODE_LENGTH,
        field_name="join_code",
        empty_message="Код вступления в группу не может быть пустым.",
        min_length_message="Код вступления в группу короче минимальной длины.",
        max_length_message="Код вступления в группу превышает максимальную длину.",
    )