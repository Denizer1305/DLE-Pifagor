from __future__ import annotations

BANK_ITEM_COPY_FIELDS = (
    "title",
    "text",
    "explanation",
    "question_type",
    "check_mode",
    "expected_text_answer",
    "expected_number_answer",
    "case_sensitive",
    "score",
    "difficulty",
    "tags_data",
)


BANK_OPTION_COPY_FIELDS = (
    "text",
    "order",
    "is_correct",
    "score",
    "feedback",
    "is_active",
)


def build_question_payload_from_bank_item(*, bank_item) -> dict:
    """
    Собирает payload вопроса теста из шаблона банка.
    """

    return {
        field_name: getattr(bank_item, field_name)
        for field_name in BANK_ITEM_COPY_FIELDS
    }


def build_option_payload_from_bank_option(*, bank_option) -> dict:
    """
    Собирает payload варианта ответа из варианта шаблона.
    """

    return {
        field_name: getattr(bank_option, field_name)
        for field_name in BANK_OPTION_COPY_FIELDS
    }


def build_bank_item_duplicate_payload(*, bank_item) -> dict:
    """
    Собирает payload для копии шаблона вопроса.
    """

    payload = build_question_payload_from_bank_item(bank_item=bank_item)

    payload.update(
        {
            "organization": bank_item.organization,
            "subject": bank_item.subject,
            "owner_teacher": bank_item.owner_teacher,
            "visibility": bank_item.visibility,
            "is_active": True,
        }
    )

    return payload
