from __future__ import annotations

from typing import Any

QUESTION_MUTABLE_FIELDS = {
    "test",
    "test_id",
    "question_type",
    "check_mode",
    "title",
    "text",
    "explanation",
    "expected_text_answer",
    "expected_number_answer",
    "case_sensitive",
    "order",
    "score",
    "is_required",
    "is_active",
}


OPTION_MUTABLE_FIELDS = {
    "question",
    "question_id",
    "text",
    "order",
    "is_correct",
    "score",
    "feedback",
    "is_active",
}


def apply_question_payload(
    *,
    question,
    data: dict[str, Any],
) -> None:
    """
    Применяет разрешённые поля к вопросу.
    """

    for field_name, value in data.items():
        if field_name in QUESTION_MUTABLE_FIELDS:
            setattr(question, field_name, value)


def apply_option_payload(
    *,
    option,
    data: dict[str, Any],
) -> None:
    """
    Применяет разрешённые поля к варианту ответа.
    """

    for field_name, value in data.items():
        if field_name in OPTION_MUTABLE_FIELDS:
            setattr(option, field_name, value)
