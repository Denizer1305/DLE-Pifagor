"""
Сервисы уведомлений о дедлайнах и контрольных.

Интервалы:
- сегодня;
- завтра;
- через 3 дня;
- просрочено после полуночи следующего дня.
"""

from __future__ import annotations

from datetime import timedelta

from apps.notifications.constants import (
    NOTIFICATION_SOON_DAYS,
    NotificationCategory,
    NotificationLevel,
    NotificationSourceType,
    NotificationType,
)
from apps.notifications.selectors import get_assignment_deadlines_for_user
from apps.notifications.services.notification_services import (
    build_deduplication_key,
    create_notification,
)
from django.utils import timezone


def create_assignment_deadline_notifications_for_user(
    *,
    user,
    target_date=None,
) -> list:
    """
    Создаёт уведомления о дедлайнах заданий пользователя.
    """

    target_date = target_date or timezone.localdate()
    created_notifications = []

    for rule in get_deadline_rules(target_date):
        assignments = get_assignment_deadlines_for_user(
            user=user,
            target_date=rule["date"],
        )

        for assignment in assignments:
            notification, created = create_assignment_deadline_notification(
                user=user,
                assignment=assignment,
                target_date=target_date,
                rule=rule,
            )

            if created:
                created_notifications.append(notification)

    return created_notifications


def create_assignment_deadline_notification(
    *,
    user,
    assignment,
    target_date,
    rule: dict,
):
    """
    Создаёт одно уведомление о дедлайне задания.
    """

    assignment_id = get_source_attr(assignment, "id", "")
    assignment_title = get_source_attr(assignment, "title", "Задание")

    deduplication_key = build_deduplication_key(
        user_id=user.id,
        notification_type=rule["notification_type"],
        source_type=NotificationSourceType.ASSIGNMENT,
        source_id=assignment_id,
        target_date=target_date,
    )

    return create_notification(
        recipient=user,
        title=rule["title"],
        message=rule["message"].format(title=assignment_title),
        notification_type=rule["notification_type"],
        category=NotificationCategory.ASSIGNMENTS,
        level=rule["level"],
        source_type=NotificationSourceType.ASSIGNMENT,
        source_id=str(assignment_id),
        deduplication_key=deduplication_key,
        action_label="Открыть задание",
        action_url=build_assignment_action_url(user=user, assignment_id=assignment_id),
        payload={
            "assignment_id": assignment_id,
            "assignment_title": assignment_title,
            "target_date": target_date.isoformat(),
            "deadline_date": rule["date"].isoformat(),
            "rule": rule["key"],
        },
    )


def get_deadline_rules(target_date) -> list[dict]:
    """
    Возвращает правила уведомлений о дедлайнах.
    """

    return [
        {
            "key": "today",
            "date": target_date,
            "notification_type": NotificationType.ASSIGNMENT_DUE_TODAY,
            "level": NotificationLevel.WARNING,
            "title": "Задание нужно сдать сегодня",
            "message": "Сегодня нужно сдать: {title}.",
        },
        {
            "key": "tomorrow",
            "date": target_date + timedelta(days=1),
            "notification_type": NotificationType.ASSIGNMENT_DUE_TOMORROW,
            "level": NotificationLevel.WARNING,
            "title": "Задание нужно сдать завтра",
            "message": "Завтра дедлайн по заданию: {title}.",
        },
        {
            "key": "soon",
            "date": target_date + timedelta(days=NOTIFICATION_SOON_DAYS),
            "notification_type": NotificationType.ASSIGNMENT_DUE_SOON,
            "level": NotificationLevel.INFO,
            "title": "Скоро дедлайн задания",
            "message": "Через 3 дня нужно сдать: {title}.",
        },
    ]


def create_assignment_overdue_notifications_for_user(
    *,
    user,
    target_date=None,
) -> list:
    """
    Создаёт уведомления о просроченных заданиях.

    Вызывается после полуночи следующего дня.
    """

    target_date = target_date or timezone.localdate()
    overdue_date = target_date - timedelta(days=1)
    assignments = get_assignment_deadlines_for_user(
        user=user,
        target_date=overdue_date,
    )

    created_notifications = []

    for assignment in assignments:
        notification, created = create_assignment_overdue_notification(
            user=user,
            assignment=assignment,
            target_date=target_date,
            overdue_date=overdue_date,
        )

        if created:
            created_notifications.append(notification)

    return created_notifications


def create_assignment_overdue_notification(
    *,
    user,
    assignment,
    target_date,
    overdue_date,
):
    """
    Создаёт уведомление о просроченном задании.
    """

    assignment_id = get_source_attr(assignment, "id", "")
    assignment_title = get_source_attr(assignment, "title", "Задание")

    deduplication_key = build_deduplication_key(
        user_id=user.id,
        notification_type=NotificationType.ASSIGNMENT_OVERDUE,
        source_type=NotificationSourceType.ASSIGNMENT,
        source_id=assignment_id,
        target_date=target_date,
    )

    return create_notification(
        recipient=user,
        title="Задание просрочено",
        message=f"Срок сдачи задания «{assignment_title}» уже прошёл.",
        notification_type=NotificationType.ASSIGNMENT_OVERDUE,
        category=NotificationCategory.ASSIGNMENTS,
        level=NotificationLevel.DANGER,
        source_type=NotificationSourceType.ASSIGNMENT,
        source_id=str(assignment_id),
        deduplication_key=deduplication_key,
        action_label="Открыть задание",
        action_url=build_assignment_action_url(user=user, assignment_id=assignment_id),
        payload={
            "assignment_id": assignment_id,
            "assignment_title": assignment_title,
            "target_date": target_date.isoformat(),
            "overdue_date": overdue_date.isoformat(),
        },
    )


def build_assignment_action_url(*, user, assignment_id) -> str:
    """
    Возвращает ссылку на задание по роли пользователя.
    """

    role_code = get_user_role_code(user)

    if role_code == "teacher":
        return f"/teacher/assignments/{assignment_id}"

    if role_code == "guardian":
        return f"/parent/assignments/{assignment_id}"

    return f"/student/assignments/{assignment_id}"


def get_user_role_code(user) -> str:
    """
    Возвращает активную роль пользователя.
    """

    settings_obj = getattr(user, "settings", None)

    if settings_obj and settings_obj.active_role:
        return settings_obj.active_role

    return "learner"


def get_source_attr(source, attr: str, default=""):
    """
    Безопасно получает атрибут из объекта или словаря.
    """

    if isinstance(source, dict):
        return source.get(attr, default)

    return getattr(source, attr, default)
