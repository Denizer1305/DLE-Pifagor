from __future__ import annotations


class QuestionType:
    """
    Типы вопросов теста.
    """

    SINGLE_CHOICE = "single_choice"
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    SHORT_TEXT = "short_text"
    NUMBER = "number"


QUESTION_TYPE_CHOICES = (
    (QuestionType.SINGLE_CHOICE, "Один вариант ответа"),
    (QuestionType.MULTIPLE_CHOICE, "Несколько вариантов ответа"),
    (QuestionType.TRUE_FALSE, "Верно / неверно"),
    (QuestionType.SHORT_TEXT, "Короткий текстовый ответ"),
    (QuestionType.NUMBER, "Числовой ответ"),
)


class QuestionCheckMode:
    """
    Режим проверки вопроса.
    """

    AUTO = "auto"
    MANUAL = "manual"
    SEMI_AUTO = "semi_auto"


QUESTION_CHECK_MODE_CHOICES = (
    (QuestionCheckMode.AUTO, "Автоматическая проверка"),
    (QuestionCheckMode.MANUAL, "Ручная проверка"),
    (QuestionCheckMode.SEMI_AUTO, "Полуавтоматическая проверка"),
)
