from __future__ import annotations

from typing import Any

TEST_MUTABLE_FIELDS = {
    "title",
    "description",
    "instructions",
    "course",
    "course_id",
    "lesson",
    "lesson_id",
    "lesson_block",
    "lesson_block_id",
    "organization",
    "organization_id",
    "subject",
    "subject_id",
    "owner_teacher",
    "owner_teacher_id",
    "status",
    "visibility",
    "max_attempts",
    "time_limit_minutes",
    "max_score",
    "passing_score",
    "shuffle_questions",
    "shuffle_options",
    "show_correct_answers_after_publish",
    "is_active",
}


TEST_CREATE_REQUIRED_FIELDS = {
    "title",
    "course",
    "organization",
    "subject",
    "owner_teacher",
}


def filter_test_payload(*, data: dict[str, Any]) -> dict[str, Any]:
    """
    Возвращает только поля, разрешённые для изменения теста.
    """

    return {
        field_name: value
        for field_name, value in data.items()
        if field_name in TEST_MUTABLE_FIELDS
    }


def apply_test_payload(
    *,
    test,
    data: dict[str, Any],
) -> None:
    """
    Применяет разрешённые поля payload к тесту.
    """

    payload = filter_test_payload(data=data)

    for field_name, value in payload.items():
        setattr(test, field_name, value)
