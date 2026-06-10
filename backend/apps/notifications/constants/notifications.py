"""
Константы приложения notifications.

Модуль содержит типы, уровни, статусы, источники и системные значения,
которые используются при создании, доставке, фильтрации и очистке
внутренних уведомлений платформы.
"""

from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _


class NotificationLevel(models.TextChoices):
    """
    Уровень важности уведомления.

    Используется frontend частью для визуального оформления уведомления:
    обычное сообщение, успешное событие, предупреждение или критичная ошибка.
    """

    INFO = "info", _("Информация")
    SUCCESS = "success", _("Успешное событие")
    WARNING = "warning", _("Предупреждение")
    DANGER = "danger", _("Критичное уведомление")


class NotificationStatus(models.TextChoices):
    """
    Жизненный статус уведомления.

    Новое уведомление считается активным до тех пор, пока пользователь
    не прочитает, не выполнит или не удалит его.
    """

    UNREAD = "unread", _("Не прочитано")
    READ = "read", _("Прочитано")
    COMPLETED = "completed", _("Выполнено")
    ARCHIVED = "archived", _("В архиве")


class NotificationType(models.TextChoices):
    """
    Типы уведомлений платформы.

    Тип определяет смысл уведомления и используется для дедупликации,
    фильтрации, настроек пользователя и генерации текстов.
    """

    DAILY_SUMMARY = "daily_summary", _("Ежедневная сводка")
    BIRTHDAY = "birthday", _("День рождения")

    ASSIGNMENT_DUE_TODAY = "assignment_due_today", _("Задание к сдаче сегодня")
    ASSIGNMENT_DUE_TOMORROW = "assignment_due_tomorrow", _("Задание к сдаче завтра")
    ASSIGNMENT_DUE_SOON = "assignment_due_soon", _("Задание к сдаче скоро")
    ASSIGNMENT_OVERDUE = "assignment_overdue", _("Просроченное задание")

    TEST_TODAY = "test_today", _("Контрольная сегодня")
    TEST_TOMORROW = "test_tomorrow", _("Контрольная завтра")
    EXAM_TODAY = "exam_today", _("Экзамен сегодня")
    EXAM_TOMORROW = "exam_tomorrow", _("Экзамен завтра")

    CALENDAR_EVENT_TODAY = "calendar_event_today", _("Событие календаря сегодня")
    NOTE_REMINDER = "note_reminder", _("Напоминание заметки")
    SCHEDULE_CHANGED = "schedule_changed", _("Изменение расписания")

    WORK_TO_CHECK = "work_to_check", _("Работы на проверку")
    MODERATION_REQUEST = "moderation_request", _("Заявка на модерацию")
    SUPPORT_REQUEST = "support_request", _("Обращение в поддержку")

    SECURITY = "security", _("Безопасность")
    SYSTEM = "system", _("Системное уведомление")


class NotificationCategory(models.TextChoices):
    """
    Категории уведомлений для пользовательских настроек.

    Категории связаны с настройками notifications в UserSettings.
    Пользователь может отключать обычные категории, но системные и
    критичные события должны оставаться доступными.
    """

    DAILY_SUMMARY = "daily_summary", _("Ежедневная сводка")
    ASSIGNMENTS = "assignments", _("Задания")
    TESTS = "tests", _("Контрольные и экзамены")
    SCHEDULE = "schedule", _("Расписание")
    CALENDAR = "calendar", _("Календарь")
    NOTES = "notes", _("Заметки")
    BIRTHDAY = "birthday", _("День рождения")
    EDUCATION = "education", _("Образование")
    FEEDBACK = "feedback", _("Обратная связь")
    MODERATION = "moderation", _("Модерация")
    SECURITY = "security", _("Безопасность")
    SYSTEM = "system", _("Система")


class NotificationSourceType(models.TextChoices):
    """
    Источник уведомления.

    Источник помогает связать уведомление с конкретной сущностью проекта:
    заданием, событием календаря, заметкой, пользователем и т.д.
    """

    USER = "user", _("Пользователь")
    ASSIGNMENT = "assignment", _("Задание")
    TEST = "test", _("Контрольная")
    EXAM = "exam", _("Экзамен")
    LESSON = "lesson", _("Урок")
    COURSE = "course", _("Курс")
    SCHEDULE = "schedule", _("Расписание")
    CALENDAR_EVENT = "calendar_event", _("Событие календаря")
    NOTE = "note", _("Заметка")
    SUPPORT_REQUEST = "support_request", _("Обращение")
    MODERATION_REQUEST = "moderation_request", _("Заявка на модерацию")
    SECURITY_EVENT = "security_event", _("Событие безопасности")
    SYSTEM = "system", _("Система")


class NotificationRole(models.TextChoices):
    """
    Роль получателя уведомления.

    Роль нужна для генерации ролевых текстов и фильтрации сценариев.
    """

    ADMIN = "admin", _("Администратор")
    TEACHER = "teacher", _("Преподаватель")
    LEARNER = "learner", _("Студент")
    GUARDIAN = "guardian", _("Родитель")


class NotificationDeliveryChannel(models.TextChoices):
    """
    Каналы доставки уведомлений.

    Внутренние уведомления создаются всегда через приложение notifications.
    Внешние каналы используются как дополнительные способы доставки.
    """

    IN_APP = "in_app", _("Внутри платформы")
    EMAIL = "email", _("Email")
    VK = "vk", _("VK")
    MAX = "max", _("MAX")


class NotificationDeliveryStatus(models.TextChoices):
    """
    Статус доставки уведомления по конкретному каналу.
    """

    PENDING = "pending", _("Ожидает отправки")
    SENT = "sent", _("Отправлено")
    FAILED = "failed", _("Ошибка отправки")
    SKIPPED = "skipped", _("Пропущено")


class NotificationFrequency(models.TextChoices):
    """
    Частота уведомлений.

    Значения должны совпадать с настройками пользователя в UserSettings.
    """

    INSTANT = "instant", _("Сразу")
    DAILY = "daily", _("Раз в день")
    WEEKLY = "weekly", _("Раз в неделю")
    DISABLED = "disabled", _("Отключено")


class NotificationBootstrapReason(models.TextChoices):
    """
    Причина запуска bootstrap-синхронизации уведомлений.
    """

    DASHBOARD_LOGIN = "dashboard_login", _("Вход в личный кабинет")
    MANUAL_SYNC = "manual_sync", _("Ручная синхронизация")
    CELERY_FALLBACK = "celery_fallback", _("Догрузка после Celery")


class NotificationDeduplicationScope(models.TextChoices):
    """
    Область дедупликации уведомления.

    Используется сервисным слоем при формировании deduplication_key.
    """

    DAILY = "daily", _("Один раз в день")
    SOURCE = "source", _("Один раз на источник")
    GLOBAL = "global", _("Глобально")


CRITICAL_NOTIFICATION_CATEGORIES = {
    NotificationCategory.SECURITY,
    NotificationCategory.SYSTEM,
}

CRITICAL_NOTIFICATION_LEVELS = {
    NotificationLevel.DANGER,
}

SYSTEM_NOTIFICATION_TYPES = {
    NotificationType.SECURITY,
    NotificationType.SYSTEM,
}

ASSIGNMENT_NOTIFICATION_TYPES = {
    NotificationType.ASSIGNMENT_DUE_TODAY,
    NotificationType.ASSIGNMENT_DUE_TOMORROW,
    NotificationType.ASSIGNMENT_DUE_SOON,
    NotificationType.ASSIGNMENT_OVERDUE,
}

TEST_NOTIFICATION_TYPES = {
    NotificationType.TEST_TODAY,
    NotificationType.TEST_TOMORROW,
    NotificationType.EXAM_TODAY,
    NotificationType.EXAM_TOMORROW,
}

CALENDAR_NOTIFICATION_TYPES = {
    NotificationType.CALENDAR_EVENT_TODAY,
    NotificationType.SCHEDULE_CHANGED,
}

NOTE_NOTIFICATION_TYPES = {
    NotificationType.NOTE_REMINDER,
}

NOTIFICATION_RETENTION_DAYS_AFTER_COMPLETION = 7

NOTIFICATION_SOON_DAYS = 3

NOTIFICATION_OVERDUE_MINUTE = 1

DAILY_NOTIFICATION_HOUR = 7
DAILY_NOTIFICATION_MINUTE = 0

OVERDUE_NOTIFICATION_HOUR = 0
OVERDUE_NOTIFICATION_MINUTE = 1

REMINDER_SCAN_INTERVAL_MINUTES = 15

NOTIFICATION_TITLE_MAX_LENGTH = 180
NOTIFICATION_MESSAGE_MAX_LENGTH = 1200
NOTIFICATION_ACTION_LABEL_MAX_LENGTH = 120
NOTIFICATION_ACTION_URL_MAX_LENGTH = 255
NOTIFICATION_DEDUPLICATION_KEY_MAX_LENGTH = 255
NOTIFICATION_SOURCE_ID_MAX_LENGTH = 64
