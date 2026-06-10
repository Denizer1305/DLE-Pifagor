from __future__ import annotations

from typing import Any

from apps.testing.constants import TestAttemptStatus
from apps.testing.models import TestAttemptAnswer
from apps.testing.validators import validate_answer
from django.db import transaction

ANSWER_MUTABLE_FIELDS = {
    "attempt",
    "attempt_id",
    "question",
    "question_id",
    "selected_option",
    "selected_option_id",
    "selected_options_data",
    "text_answer",
    "number_answer",
}


@transaction.atomic
def save_attempt_answer(
    *,
    attempt,
    data: dict[str, Any],
) -> TestAttemptAnswer:
    """
    Создаёт или обновляет ответ обучающегося в рамках попытки.
    """

    _validate_attempt_accepts_answers(attempt=attempt)

    question_id = data["question_id"]

    answer, _ = TestAttemptAnswer.objects.get_or_create(
        attempt=attempt,
        question_id=question_id,
    )

    _apply_answer_payload(
        answer=answer,
        attempt=attempt,
        data=data,
    )

    validate_answer(answer=answer)

    answer.full_clean()
    answer.save()

    return answer


@transaction.atomic
def save_attempt_answers(
    *,
    attempt,
    answers_data: list[dict[str, Any]],
) -> list[TestAttemptAnswer]:
    """
    Создаёт или обновляет набор ответов обучающегося.
    """

    saved_answers = []

    for answer_data in answers_data:
        saved_answer = save_attempt_answer(
            attempt=attempt,
            data=answer_data,
        )
        saved_answers.append(saved_answer)

    return saved_answers


def _apply_answer_payload(
    *,
    answer: TestAttemptAnswer,
    attempt,
    data: dict[str, Any],
) -> None:
    """
    Применяет разрешённые поля к ответу.
    """

    answer.attempt = attempt

    for field_name, value in data.items():
        if field_name in ANSWER_MUTABLE_FIELDS:
            setattr(answer, field_name, value)


def _validate_attempt_accepts_answers(*, attempt) -> None:
    """
    Проверяет, что попытка принимает ответы.
    """

    if attempt.status != TestAttemptStatus.STARTED:
        from django.core.exceptions import ValidationError
        from django.utils.translation import gettext_lazy as _

        raise ValidationError(
            {"attempt": _("Ответы можно сохранять только для начатой попытки.")}
        )
