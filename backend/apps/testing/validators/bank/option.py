from __future__ import annotations

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_bank_option(option) -> None:
    """
    Валидирует вариант ответа шаблона вопроса.
    """

    validate_bank_option_score(option=option)


def validate_bank_option_score(option) -> None:
    """
    Проверяет балл варианта ответа.
    """

    if option.score < 0:
        raise ValidationError(
            {"score": _("Балл за вариант ответа не может быть отрицательным.")}
        )

    if option.score > option.bank_item.score:
        raise ValidationError(
            {
                "score": _(
                    "Балл за вариант ответа не может быть больше "
                    "балла шаблона вопроса."
                )
            }
        )


def validate_bank_option_relations(option) -> None:
    """
    Проверяет связи варианта ответа.
    """

    if option.bank_item_id is None:
        raise ValidationError({"bank_item": _("Укажите шаблон вопроса.")})
