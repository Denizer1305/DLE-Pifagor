from __future__ import annotations

from apps.testing.constants import QuestionType
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_question_options_for_publish(*, question) -> None:
    """
    Проверяет варианты ответа перед публикацией теста.

    Не вызывается при обычном создании вопроса, потому что варианты
    могут быть добавлены после сохранения вопроса.
    """

    if not question.pk:
        return

    if question.question_type == QuestionType.SINGLE_CHOICE:
        _validate_single_choice_options(question=question)

    if question.question_type == QuestionType.MULTIPLE_CHOICE:
        _validate_multiple_choice_options(question=question)

    if question.question_type == QuestionType.TRUE_FALSE:
        _validate_true_false_options(question=question)


def _validate_single_choice_options(*, question) -> None:
    """
    Проверяет варианты для вопроса с одним правильным ответом.
    """

    active_options = question.options.filter(is_active=True)
    correct_count = active_options.filter(is_correct=True).count()

    if active_options.count() < 2:
        raise ValidationError(
            {
                "options": _(
                    "Для вопроса с одним вариантом ответа нужно минимум 2 варианта."
                )
            }
        )

    if correct_count != 1:
        raise ValidationError(
            {
                "options": _(
                    "Для вопроса с одним вариантом ответа должен быть "
                    "ровно 1 правильный вариант."
                )
            }
        )


def _validate_multiple_choice_options(*, question) -> None:
    """
    Проверяет варианты для вопроса с несколькими правильными ответами.
    """

    active_options = question.options.filter(is_active=True)
    correct_count = active_options.filter(is_correct=True).count()

    if active_options.count() < 2:
        raise ValidationError(
            {
                "options": _(
                    "Для вопроса с несколькими вариантами нужно минимум 2 варианта."
                )
            }
        )

    if correct_count < 1:
        raise ValidationError(
            {
                "options": _(
                    "Для вопроса с несколькими вариантами нужен хотя бы "
                    "1 правильный вариант."
                )
            }
        )


def _validate_true_false_options(*, question) -> None:
    """
    Проверяет варианты для вопроса верно/неверно.
    """

    active_options = question.options.filter(is_active=True)
    correct_count = active_options.filter(is_correct=True).count()

    if active_options.count() != 2:
        raise ValidationError(
            {"options": _("Для вопроса верно/неверно должно быть ровно 2 варианта.")}
        )

    if correct_count != 1:
        raise ValidationError(
            {
                "options": _(
                    "Для вопроса верно/неверно должен быть ровно "
                    "1 правильный вариант."
                )
            }
        )
