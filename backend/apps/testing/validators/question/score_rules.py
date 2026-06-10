from __future__ import annotations

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_question_score(*, question) -> None:
    """
    Проверяет балл вопроса.
    """

    if question.score < 1:
        raise ValidationError({"score": _("Балл за вопрос должен быть не меньше 1.")})
