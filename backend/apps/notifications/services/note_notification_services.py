"""
Сервисы уведомлений по напоминаниям заметок.
"""

from __future__ import annotations

from apps.notifications.constants import (
    NotificationCategory,
    NotificationLevel,
    NotificationSourceType,
    NotificationType,
)
from apps.notifications.selectors import get_note_reminders_for_user
from apps.notifications.services.notification_services import (
    build_deduplication_key,
    create_notification,
)
from django.utils import timezone


def create_note_reminder_notifications_for_user(
    *,
    user,
    starts_at=None,
    ends_at=None,
) -> list:
    """
    Создаёт уведомления по заметкам с включённым напоминанием.
    """

    starts_at = starts_at or timezone.now()
    ends_at = ends_at or starts_at

    reminders = get_note_reminders_for_user(
        user=user,
        starts_at=starts_at,
        ends_at=ends_at,
    )

    created_notifications = []

    for note in reminders:
        notification, created = create_note_reminder_notification(
            user=user,
            note=note,
            target_date=timezone.localdate(starts_at),
        )

        if created:
            created_notifications.append(notification)

    return created_notifications


def create_note_reminder_notification(*, user, note, target_date):
    """
    Создаёт уведомление по одной заметке.
    """

    note_id = get_source_attr(note, "id", "")
    note_title = get_source_attr(note, "title", "Заметка")
    remind_at = get_source_attr(note, "remind_at", None)

    deduplication_key = build_deduplication_key(
        user_id=user.id,
        notification_type=NotificationType.NOTE_REMINDER,
        source_type=NotificationSourceType.NOTE,
        source_id=note_id,
        target_date=target_date,
    )

    return create_notification(
        recipient=user,
        title="Напоминание по заметке",
        message=f"Пора вернуться к заметке: {note_title}.",
        notification_type=NotificationType.NOTE_REMINDER,
        category=NotificationCategory.NOTES,
        level=NotificationLevel.INFO,
        source_type=NotificationSourceType.NOTE,
        source_id=str(note_id),
        deduplication_key=deduplication_key,
        action_label="Открыть заметки",
        action_url=build_notes_action_url(user=user),
        event_at=remind_at,
        payload={
            "note_id": note_id,
            "note_title": note_title,
            "target_date": target_date.isoformat(),
        },
    )


def build_notes_action_url(*, user) -> str:
    """
    Возвращает ссылку на заметки по роли пользователя.
    """

    role_code = get_user_role_code(user)

    if role_code == "teacher":
        return "/teacher/notes"

    if role_code == "guardian":
        return "/parent/notes"

    if role_code == "admin":
        return "/admin/notes"

    return "/student/notes"


def get_user_role_code(user) -> str:
    """
    Возвращает активную роль пользователя.
    """

    settings_obj = getattr(user, "settings", None)

    if settings_obj and settings_obj.active_role:
        return settings_obj.active_role

    if user.is_superuser:
        return "admin"

    return "learner"


def get_source_attr(source, attr: str, default=""):
    """
    Безопасно получает атрибут из объекта или словаря.
    """

    if isinstance(source, dict):
        return source.get(attr, default)

    return getattr(source, attr, default)
