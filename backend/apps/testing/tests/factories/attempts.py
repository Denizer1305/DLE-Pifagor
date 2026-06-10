from __future__ import annotations

from decimal import Decimal

from apps.course.tests.factories import create_learner
from apps.testing.constants import AttemptCheckStatus, TestAttemptStatus
from apps.testing.models import (
    TestAttempt,
    TestAttemptAnswer,
    TestQuestion,
    TestQuestionOption,
)
from apps.testing.tests.factories.structure import (
    create_choice_question_with_options,
    create_test,
)
from django.utils import timezone


def create_attempt(
    *,
    test=None,
    learner=None,
    **overrides,
) -> TestAttempt:
    """
    Создаёт попытку прохождения теста.
    """

    test = test or create_test()
    learner = learner or create_learner()

    data = {
        "test": test,
        "learner": learner,
        "attempt_number": overrides.pop(
            "attempt_number",
            _next_attempt_number(test=test, learner=learner),
        ),
        "status": overrides.pop("status", TestAttemptStatus.STARTED),
        "check_status": overrides.pop(
            "check_status",
            AttemptCheckStatus.NOT_CHECKED,
        ),
        "started_at": overrides.pop("started_at", timezone.now()),
        "submitted_at": overrides.pop("submitted_at", None),
        "auto_checked_at": overrides.pop("auto_checked_at", None),
        "reviewed_at": overrides.pop("reviewed_at", None),
        "confirmed_at": overrides.pop("confirmed_at", None),
        "published_at": overrides.pop("published_at", None),
        "auto_score": overrides.pop("auto_score", Decimal("0")),
        "teacher_score": overrides.pop("teacher_score", None),
        "final_score": overrides.pop("final_score", None),
        "auto_grade": overrides.pop("auto_grade", None),
        "teacher_grade": overrides.pop("teacher_grade", None),
        "final_grade": overrides.pop("final_grade", None),
        "requires_manual_review": overrides.pop(
            "requires_manual_review",
            False,
        ),
        "is_confirmed_by_teacher": overrides.pop(
            "is_confirmed_by_teacher",
            False,
        ),
        "is_visible_to_learner": overrides.pop(
            "is_visible_to_learner",
            False,
        ),
        "is_visible_to_guardian": overrides.pop(
            "is_visible_to_guardian",
            False,
        ),
        "reviewer_teacher": overrides.pop("reviewer_teacher", None),
        "teacher_comment": overrides.pop("teacher_comment", ""),
    }
    data.update(overrides)

    return TestAttempt.objects.create(**data)


def create_answer(
    *,
    attempt: TestAttempt | None = None,
    question: TestQuestion | None = None,
    selected_option: TestQuestionOption | None = None,
    **overrides,
) -> TestAttemptAnswer:
    """
    Создаёт ответ на вопрос теста.
    """

    attempt = attempt or create_attempt()
    question = question or create_choice_question_with_options(
        test=attempt.test,
    )

    selected_option = selected_option or _get_default_selected_option(
        question=question,
    )

    data = {
        "attempt": attempt,
        "question": question,
        "selected_option": selected_option,
        "selected_options_data": overrides.pop(
            "selected_options_data",
            [],
        ),
        "text_answer": overrides.pop("text_answer", ""),
        "number_answer": overrides.pop("number_answer", None),
        "is_correct": overrides.pop("is_correct", None),
        "auto_score": overrides.pop("auto_score", Decimal("0")),
        "teacher_score": overrides.pop("teacher_score", None),
        "final_score": overrides.pop("final_score", None),
        "requires_manual_review": overrides.pop(
            "requires_manual_review",
            False,
        ),
        "teacher_comment": overrides.pop("teacher_comment", ""),
    }
    data.update(overrides)

    return TestAttemptAnswer.objects.create(**data)


def _next_attempt_number(*, test, learner) -> int:
    """
    Возвращает следующий номер попытки.
    """

    last_number = (
        TestAttempt.objects.filter(
            test=test,
            learner=learner,
        )
        .order_by("-attempt_number")
        .values_list("attempt_number", flat=True)
        .first()
    )

    return (last_number or 0) + 1


def _get_default_selected_option(*, question):
    """
    Возвращает первый активный вариант ответа.
    """

    return question.options.filter(is_active=True).order_by("order", "id").first()
