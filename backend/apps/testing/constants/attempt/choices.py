from __future__ import annotations

from django.db import models


class TestAttemptStatus(models.TextChoices):
    """
    Статусы попытки прохождения теста.
    """

    STARTED = "started", "Начата"
    SUBMITTED = "submitted", "Отправлена"
    NEEDS_REVIEW = "needs_review", "Требует проверки"
    AUTO_CHECKED = "auto_checked", "Проверена автоматически"
    CONFIRMED = "confirmed", "Подтверждена преподавателем"
    PUBLISHED = "published", "Опубликована"
    EXPIRED = "expired", "Время истекло"
    CANCELLED = "cancelled", "Отменена"


TEST_ATTEMPT_STATUS_CHOICES = (
    (TestAttemptStatus.STARTED, "Начата"),
    (TestAttemptStatus.SUBMITTED, "Отправлена"),
    (TestAttemptStatus.AUTO_CHECKED, "Проверена автоматически"),
    (TestAttemptStatus.NEEDS_REVIEW, "Ожидает проверки преподавателем"),
    (TestAttemptStatus.CONFIRMED, "Оценка подтверждена"),
    (TestAttemptStatus.PUBLISHED, "Результат опубликован"),
    (TestAttemptStatus.CANCELLED, "Отменена"),
)


class AttemptCheckStatus(models.TextChoices):
    """
    Статусы проверки попытки.
    """

    NOT_CHECKED = "not_checked", "Не проверена"
    NEEDS_REVIEW = "needs_review", "Требует проверки"
    AUTO_CHECKED = "auto_checked", "Проверена автоматически"
    CHECKED = "checked", "Проверена"


ATTEMPT_CHECK_STATUS_CHOICES = (
    (AttemptCheckStatus.NOT_CHECKED, "Не проверено"),
    (AttemptCheckStatus.AUTO_CHECKED, "Проверено автоматически"),
    (AttemptCheckStatus.NEEDS_REVIEW, "Требует ручной проверки"),
    (AttemptCheckStatus.CHECKED, "Проверено"),
)
