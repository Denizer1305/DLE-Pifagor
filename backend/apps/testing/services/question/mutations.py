from __future__ import annotations

from typing import Any

from apps.testing.models import TestQuestion, TestQuestionOption
from apps.testing.services.question.payloads import (
    apply_option_payload,
    apply_question_payload,
)
from django.db import transaction


@transaction.atomic
def create_question(*, data: dict[str, Any]) -> TestQuestion:
    """
    Создаёт вопрос теста.
    """

    question = TestQuestion()

    apply_question_payload(
        question=question,
        data=data,
    )

    question.full_clean()
    question.save()

    return question


@transaction.atomic
def update_question(
    *,
    question: TestQuestion,
    data: dict[str, Any],
) -> TestQuestion:
    """
    Обновляет вопрос теста.
    """

    apply_question_payload(
        question=question,
        data=data,
    )

    question.full_clean()
    question.save()

    return question


@transaction.atomic
def create_question_option(*, data: dict[str, Any]) -> TestQuestionOption:
    """
    Создаёт вариант ответа.
    """

    option = TestQuestionOption()

    apply_option_payload(
        option=option,
        data=data,
    )

    option.full_clean()
    option.save()

    return option


@transaction.atomic
def update_question_option(
    *,
    option: TestQuestionOption,
    data: dict[str, Any],
) -> TestQuestionOption:
    """
    Обновляет вариант ответа.
    """

    apply_option_payload(
        option=option,
        data=data,
    )

    option.full_clean()
    option.save()

    return option
