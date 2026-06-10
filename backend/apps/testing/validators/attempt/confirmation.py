from __future__ import annotations

from apps.testing.constants import TestAttemptStatus
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_attempt_can_be_confirmed(*, attempt) -> None:
    """
    Проверяет, что преподаватель может подтвердить результат попытки.
    """

    allowed_statuses = {
        TestAttemptStatus.AUTO_CHECKED,
        TestAttemptStatus.NEEDS_REVIEW,
    }

    if attempt.status not in allowed_statuses:
        raise ValidationError(
            {"status": _("Подтвердить можно только проверенную попытку.")}
        )


def validate_confirmation_values(
    *,
    final_score,
    final_grade,
    max_score,
) -> None:
    """
    Проверяет итоговые значения перед подтверждением результата.
    """

    errors = {}

    if final_score is None:
        errors["final_score"] = _("Укажите итоговый балл.")

    if final_grade is None:
        errors["final_grade"] = _("Укажите итоговую оценку.")

    if final_score is not None and final_score < 0:
        errors["final_score"] = _("Итоговый балл не может быть отрицательным.")

    if final_score is not None and final_score > max_score:
        errors["final_score"] = _(
            "Итоговый балл не может быть больше максимального балла теста."
        )

    if final_grade is not None and final_grade not in {2, 3, 4, 5}:
        errors["final_grade"] = _("Итоговая оценка должна быть от 2 до 5.")

    if errors:
        raise ValidationError(errors)


def validate_attempt_can_be_published(*, attempt) -> None:
    """
    Проверяет, что результат попытки можно показать ученику и родителю.
    """

    if not attempt.is_confirmed_by_teacher:
        raise ValidationError(
            {
                "is_confirmed_by_teacher": _(
                    "Перед публикацией результата преподаватель должен "
                    "подтвердить оценку."
                )
            }
        )

    if attempt.status != TestAttemptStatus.CONFIRMED:
        raise ValidationError(
            {"status": _("Опубликовать можно только подтверждённую попытку.")}
        )
