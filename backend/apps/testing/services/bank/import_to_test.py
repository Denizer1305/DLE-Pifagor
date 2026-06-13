from __future__ import annotations

from apps.testing.models import TestQuestion, TestQuestionOption
from apps.testing.services.bank.payloads import (
    build_option_payload_from_bank_option,
    build_question_payload_from_bank_item,
)
from apps.testing.services.bank.validation import (
    validate_bank_item_can_be_copied_to_test,
)
from django.db import transaction
from django.db.models import Max


@transaction.atomic
def copy_bank_item_to_test(
    *,
    bank_item,
    test,
    order: int | None = None,
) -> TestQuestion:
    """
    Копирует шаблон вопроса из банка в конкретный тест.
    """

    validate_bank_item_can_be_copied_to_test(
        bank_item=bank_item,
        test=test,
    )

    question_payload = build_question_payload_from_bank_item(
        bank_item=bank_item,
    )
    question_payload.update(
        {
            "test": test,
            "source_bank_item": bank_item,
            "order": order or _next_question_order(test=test),
            "is_active": True,
        }
    )

    question = TestQuestion(**question_payload)
    question.full_clean()
    question.save()

    _copy_bank_options_to_question(
        bank_item=bank_item,
        question=question,
    )

    return question


def _copy_bank_options_to_question(
    *,
    bank_item,
    question: TestQuestion,
) -> None:
    """
    Копирует варианты ответа шаблона в вопрос теста.
    """

    for bank_option in bank_item.options.filter(is_active=True).order_by(
        "order",
        "id",
    ):
        option_payload = build_option_payload_from_bank_option(
            bank_option=bank_option,
        )
        option_payload["question"] = question

        option = TestQuestionOption(**option_payload)
        option.full_clean()
        option.save()


def _next_question_order(*, test) -> int:
    """
    Возвращает следующий порядок вопроса внутри теста.
    """

    last_order = (
        TestQuestion.objects.filter(test=test)
        .aggregate(max_order=Max("order"))
        .get("max_order")
    )

    return (last_order or 0) + 1
