from __future__ import annotations

from apps.course.tests.factories import create_course, create_teacher
from apps.testing.constants import (
    QuestionCheckMode,
    QuestionType,
    TestStatus,
    TestVisibility,
)
from apps.testing.models import Test, TestQuestion, TestQuestionOption
from apps.testing.tests.factories.common import unique_title


def create_test(**overrides) -> Test:
    """
    Создаёт учебный тест.
    """

    course = overrides.pop("course", None) or create_course()
    owner_teacher = overrides.pop(
        "owner_teacher",
        getattr(course, "owner_teacher", None) or create_teacher(),
    )

    data = {
        "title": overrides.pop("title", unique_title("Тест")),
        "description": overrides.pop("description", "Описание теста."),
        "instructions": overrides.pop(
            "instructions",
            "Ответьте на вопросы теста.",
        ),
        "course": course,
        "lesson": overrides.pop("lesson", None),
        "lesson_block": overrides.pop("lesson_block", None),
        "organization": overrides.pop("organization", course.organization),
        "subject": overrides.pop("subject", course.subject),
        "owner_teacher": owner_teacher,
        "status": overrides.pop("status", TestStatus.DRAFT),
        "visibility": overrides.pop("visibility", TestVisibility.COURSE),
        "max_attempts": overrides.pop("max_attempts", 3),
        "time_limit_minutes": overrides.pop("time_limit_minutes", None),
        "max_score": overrides.pop("max_score", 100),
        "passing_score": overrides.pop("passing_score", 50),
        "shuffle_questions": overrides.pop("shuffle_questions", False),
        "shuffle_options": overrides.pop("shuffle_options", False),
        "show_correct_answers_after_publish": overrides.pop(
            "show_correct_answers_after_publish",
            False,
        ),
        "is_active": overrides.pop("is_active", True),
    }
    data.update(overrides)

    return Test.objects.create(**data)


def create_question(
    *,
    test: Test | None = None,
    **overrides,
) -> TestQuestion:
    """
    Создаёт вопрос теста.
    """

    test = test or create_test()

    data = {
        "test": test,
        "question_type": overrides.pop(
            "question_type",
            QuestionType.SINGLE_CHOICE,
        ),
        "check_mode": overrides.pop("check_mode", QuestionCheckMode.AUTO),
        "title": overrides.pop("title", unique_title("Вопрос")),
        "text": overrides.pop("text", "Выберите правильный ответ."),
        "explanation": overrides.pop("explanation", ""),
        "expected_text_answer": overrides.pop("expected_text_answer", ""),
        "expected_number_answer": overrides.pop(
            "expected_number_answer",
            None,
        ),
        "case_sensitive": overrides.pop("case_sensitive", False),
        "order": overrides.pop("order", _next_question_order(test=test)),
        "score": overrides.pop("score", 1),
        "is_required": overrides.pop("is_required", True),
        "is_active": overrides.pop("is_active", True),
    }
    data.update(overrides)

    return TestQuestion.objects.create(**data)


def create_option(
    *,
    question: TestQuestion | None = None,
    **overrides,
) -> TestQuestionOption:
    """
    Создаёт вариант ответа.
    """

    question = question or create_question()

    data = {
        "question": question,
        "text": overrides.pop("text", unique_title("Вариант")),
        "order": overrides.pop("order", _next_option_order(question=question)),
        "is_correct": overrides.pop("is_correct", False),
        "score": overrides.pop("score", 0),
        "feedback": overrides.pop("feedback", ""),
        "is_active": overrides.pop("is_active", True),
    }
    data.update(overrides)

    return TestQuestionOption.objects.create(**data)


def create_choice_question_with_options(
    *,
    test: Test | None = None,
    **overrides,
) -> TestQuestion:
    """
    Создаёт вопрос с двумя вариантами ответа.
    """

    question = create_question(
        test=test,
        **overrides,
    )

    create_option(
        question=question,
        text="Правильный ответ",
        is_correct=True,
        score=question.score,
    )
    create_option(
        question=question,
        text="Неправильный ответ",
        is_correct=False,
        score=0,
    )

    return question


def _next_question_order(*, test: Test) -> int:
    """
    Возвращает следующий порядок вопроса в тесте.
    """

    last_order = (
        TestQuestion.objects.filter(test=test)
        .order_by("-order")
        .values_list("order", flat=True)
        .first()
    )

    return (last_order or 0) + 1


def _next_option_order(*, question: TestQuestion) -> int:
    """
    Возвращает следующий порядок варианта в вопросе.
    """

    last_order = (
        TestQuestionOption.objects.filter(question=question)
        .order_by("-order")
        .values_list("order", flat=True)
        .first()
    )

    return (last_order or 0) + 1
