from __future__ import annotations

from apps.testing.constants import BankItemStatus, QuestionType
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_bank_item_can_be_published(*, item) -> None:
    """
    Проверяет, что шаблон вопроса можно опубликовать.
    """

    errors = {}

    if item.status == BankItemStatus.ARCHIVED:
        errors["status"] = _("Архивный шаблон вопроса нельзя опубликовать.")

    if not item.is_active:
        errors["is_active"] = _("Неактивный шаблон вопроса нельзя опубликовать.")

    if errors:
        raise ValidationError(errors)

    _validate_bank_item_options_for_publication(item=item)


def validate_bank_item_can_be_archived(*, item) -> None:
    """
    Проверяет, что шаблон вопроса можно архивировать.
    """

    if item.status == BankItemStatus.ARCHIVED:
        raise ValidationError({"status": _("Шаблон вопроса уже находится в архиве.")})


def validate_bank_item_can_be_restored(*, item) -> None:
    """
    Проверяет, что шаблон вопроса можно восстановить.
    """

    if item.status != BankItemStatus.ARCHIVED:
        raise ValidationError(
            {"status": _("Восстановить можно только архивный шаблон вопроса.")}
        )


def _validate_bank_item_options_for_publication(*, item) -> None:
    """
    Проверяет варианты ответа перед публикацией шаблона.
    """

    if item.question_type in {
        QuestionType.NUMBER,
        QuestionType.SHORT_TEXT,
    }:
        return

    active_options = item.options.filter(is_active=True)

    if not active_options.exists():
        raise ValidationError(
            {"options": _("Перед публикацией добавьте хотя бы один активный вариант.")}
        )

    correct_options_count = active_options.filter(is_correct=True).count()

    if item.question_type == QuestionType.SINGLE_CHOICE:
        _validate_single_choice_options_count(
            correct_options_count=correct_options_count,
        )

    if item.question_type == QuestionType.TRUE_FALSE:
        _validate_true_false_options_count(
            active_options_count=active_options.count(),
            correct_options_count=correct_options_count,
        )

    if item.question_type == QuestionType.MULTIPLE_CHOICE:
        _validate_multiple_choice_options_count(
            correct_options_count=correct_options_count,
        )


def _validate_single_choice_options_count(*, correct_options_count: int) -> None:
    """
    Проверяет количество правильных вариантов для single choice.
    """

    if correct_options_count != 1:
        raise ValidationError(
            {
                "options": _(
                    "В вопросе с одним ответом должен быть ровно "
                    "один правильный вариант."
                )
            }
        )


def _validate_true_false_options_count(
    *,
    active_options_count: int,
    correct_options_count: int,
) -> None:
    """
    Проверяет варианты для true/false вопроса.
    """

    if active_options_count != 2:
        raise ValidationError(
            {"options": _("В вопросе верно/неверно должно быть два варианта.")}
        )

    if correct_options_count != 1:
        raise ValidationError(
            {
                "options": _(
                    "В вопросе верно/неверно должен быть один правильный вариант."
                )
            }
        )


def _validate_multiple_choice_options_count(
    *,
    correct_options_count: int,
) -> None:
    """
    Проверяет варианты для multiple choice.
    """

    if correct_options_count < 1:
        raise ValidationError(
            {
                "options": _(
                    "В вопросе с несколькими ответами должен быть хотя бы "
                    "один правильный вариант."
                )
            }
        )
