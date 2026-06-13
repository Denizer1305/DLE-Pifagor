from __future__ import annotations

from decimal import Decimal

from apps.testing.constants import (
    BankItemDifficulty,
    BankItemStatus,
    BankItemVisibility,
    QuestionCheckMode,
    QuestionType,
)
from apps.testing.models import (
    QuestionBankItem,
    QuestionBankOption,
)
from apps.testing.tests.factories.common import unique_title
from apps.testing.tests.factories.structure import create_test


def create_bank_item(**overrides) -> QuestionBankItem:
    """
    Создаёт шаблон вопроса в банке тестовых заданий.
    """

    exam = overrides.pop("exam", None) or create_test()

    data = {
        "title": overrides.pop("title", unique_title("Шаблон вопроса")),
        "text": overrides.pop("text", "Выберите правильный ответ."),
        "explanation": overrides.pop("explanation", ""),
        "question_type": overrides.pop(
            "question_type",
            QuestionType.SINGLE_CHOICE,
        ),
        "check_mode": overrides.pop(
            "check_mode",
            QuestionCheckMode.AUTO,
        ),
        "expected_text_answer": overrides.pop("expected_text_answer", ""),
        "expected_number_answer": overrides.pop(
            "expected_number_answer",
            None,
        ),
        "case_sensitive": overrides.pop("case_sensitive", False),
        "score": overrides.pop("score", 1),
        "difficulty": overrides.pop(
            "difficulty",
            BankItemDifficulty.MEDIUM,
        ),
        "tags_data": overrides.pop("tags_data", []),
        "organization": overrides.pop("organization", exam.organization),
        "subject": overrides.pop("subject", exam.subject),
        "owner_teacher": overrides.pop(
            "owner_teacher",
            exam.owner_teacher,
        ),
        "visibility": overrides.pop(
            "visibility",
            BankItemVisibility.PRIVATE,
        ),
        "status": overrides.pop("status", BankItemStatus.DRAFT),
        "is_active": overrides.pop("is_active", True),
        "published_at": overrides.pop("published_at", None),
        "archived_at": overrides.pop("archived_at", None),
    }
    data.update(overrides)

    return QuestionBankItem.objects.create(**data)


def create_bank_option(
    *,
    bank_item: QuestionBankItem | None = None,
    **overrides,
) -> QuestionBankOption:
    """
    Создаёт вариант ответа шаблона вопроса.
    """

    bank_item = bank_item or create_bank_item()

    data = {
        "bank_item": bank_item,
        "text": overrides.pop("text", unique_title("Вариант")),
        "order": overrides.pop(
            "order",
            _next_bank_option_order(bank_item=bank_item),
        ),
        "is_correct": overrides.pop("is_correct", False),
        "score": overrides.pop("score", Decimal("0")),
        "feedback": overrides.pop("feedback", ""),
        "is_active": overrides.pop("is_active", True),
    }
    data.update(overrides)

    return QuestionBankOption.objects.create(**data)


def create_bank_item_with_options(**overrides) -> QuestionBankItem:
    """
    Создаёт шаблон вопроса с двумя вариантами ответа.
    """

    bank_item = create_bank_item(**overrides)

    create_bank_option(
        bank_item=bank_item,
        text="Правильный ответ",
        is_correct=True,
        score=Decimal(str(bank_item.score)),
    )
    create_bank_option(
        bank_item=bank_item,
        text="Неправильный ответ",
        is_correct=False,
        score=Decimal("0"),
    )

    return bank_item


def create_published_bank_item(**overrides) -> QuestionBankItem:
    """
    Создаёт опубликованный шаблон вопроса с вариантами.
    """

    return create_bank_item_with_options(
        status=overrides.pop("status", BankItemStatus.PUBLISHED),
        is_active=overrides.pop("is_active", True),
        **overrides,
    )


def _next_bank_option_order(*, bank_item: QuestionBankItem) -> int:
    """
    Возвращает следующий порядок варианта шаблона.
    """

    last_order = (
        QuestionBankOption.objects.filter(bank_item=bank_item)
        .order_by("-order")
        .values_list("order", flat=True)
        .first()
    )

    return (last_order or 0) + 1