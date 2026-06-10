from __future__ import annotations


class TestAttemptStatus:
    """
    Статусы попытки прохождения теста.
    """

    STARTED = "started"
    SUBMITTED = "submitted"
    AUTO_CHECKED = "auto_checked"
    NEEDS_REVIEW = "needs_review"
    CONFIRMED = "confirmed"
    PUBLISHED = "published"
    CANCELLED = "cancelled"


TEST_ATTEMPT_STATUS_CHOICES = (
    (TestAttemptStatus.STARTED, "Начата"),
    (TestAttemptStatus.SUBMITTED, "Отправлена"),
    (TestAttemptStatus.AUTO_CHECKED, "Проверена автоматически"),
    (TestAttemptStatus.NEEDS_REVIEW, "Ожидает проверки преподавателем"),
    (TestAttemptStatus.CONFIRMED, "Оценка подтверждена"),
    (TestAttemptStatus.PUBLISHED, "Результат опубликован"),
    (TestAttemptStatus.CANCELLED, "Отменена"),
)


class AttemptCheckStatus:
    """
    Статусы проверки ответа/попытки.
    """

    NOT_CHECKED = "not_checked"
    AUTO_CHECKED = "auto_checked"
    NEEDS_REVIEW = "needs_review"
    CHECKED = "checked"


ATTEMPT_CHECK_STATUS_CHOICES = (
    (AttemptCheckStatus.NOT_CHECKED, "Не проверено"),
    (AttemptCheckStatus.AUTO_CHECKED, "Проверено автоматически"),
    (AttemptCheckStatus.NEEDS_REVIEW, "Требует ручной проверки"),
    (AttemptCheckStatus.CHECKED, "Проверено"),
)
