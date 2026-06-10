from __future__ import annotations

import re

from apps.course.constants import COURSE_CODE_MAX_LENGTH, COURSE_SLUG_MAX_LENGTH
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

COURSE_CODE_PATTERN = re.compile(r"^[A-Za-zА-Яа-я0-9\-_]+$")
COURSE_SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:[-_][a-z0-9]+)*$")


def validate_course_code(value: str) -> None:
    """
    Проверяет технический код курса.
    """

    if not value:
        raise ValidationError(_("Код курса обязателен."))

    normalized_value = value.strip()

    if len(normalized_value) > COURSE_CODE_MAX_LENGTH:
        raise ValidationError(_("Код курса слишком длинный."))

    if not COURSE_CODE_PATTERN.fullmatch(normalized_value):
        raise ValidationError(
            _("Код курса может содержать буквы, цифры, дефис и подчёркивание.")
        )


def validate_course_slug(value: str) -> None:
    """
    Проверяет slug курса.
    """

    if not value:
        raise ValidationError(_("Slug курса обязателен."))

    normalized_value = value.strip()

    if len(normalized_value) > COURSE_SLUG_MAX_LENGTH:
        raise ValidationError(_("Slug курса слишком длинный."))

    if not COURSE_SLUG_PATTERN.fullmatch(normalized_value):
        raise ValidationError(
            _(
                "Slug может содержать латинские строчные буквы, цифры, "
                "дефис и подчёркивание."
            )
        )


def validate_course_date_range(
    *,
    starts_at,
    ends_at,
) -> None:
    """
    Проверяет даты доступности курса.
    """

    if starts_at and ends_at and ends_at < starts_at:
        raise ValidationError(
            {"ends_at": _("Дата окончания курса не может быть раньше даты начала.")}
        )


def validate_course_publication_dates(
    *,
    published_at,
    archived_at,
) -> None:
    """
    Проверяет даты публикации и архивации курса.
    """

    if published_at and archived_at and archived_at < published_at:
        raise ValidationError(
            {"archived_at": _("Дата архивации не может быть раньше даты публикации.")}
        )
