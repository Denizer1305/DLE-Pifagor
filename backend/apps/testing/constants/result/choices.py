from __future__ import annotations


class LearnerResultStatus:
    """
    Статусы итогового результата обучающегося по тесту.
    """

    ACTIVE = "active"
    BLOCKED = "blocked"
    ARCHIVED = "archived"


LEARNER_RESULT_STATUS_CHOICES = (
    (LearnerResultStatus.ACTIVE, "Активен"),
    (LearnerResultStatus.BLOCKED, "Повторное прохождение заблокировано"),
    (LearnerResultStatus.ARCHIVED, "Архивирован"),
)


class GradeSource:
    """
    Источник итоговой оценки.
    """

    AUTO = "auto"
    TEACHER = "teacher"
    AVERAGE = "average"


GRADE_SOURCE_CHOICES = (
    (GradeSource.AUTO, "Автоматически рассчитана"),
    (GradeSource.TEACHER, "Подтверждена преподавателем"),
    (GradeSource.AVERAGE, "Средняя по попыткам"),
)
