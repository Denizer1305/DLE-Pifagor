"""
Сервисы поздравлений с днём рождения.
"""

from __future__ import annotations

from apps.notifications.constants import (
    NotificationCategory,
    NotificationDeliveryChannel,
    NotificationLevel,
    NotificationSourceType,
    NotificationType,
)
from apps.notifications.services.notification_services import (
    build_deduplication_key,
    create_notification,
)
from django.utils import timezone


def create_birthday_notification(
    *, user, target_date=None
) -> tuple[object | None, bool]:
    """
    Создаёт поздравление с днём рождения, если сегодня день рождения пользователя.
    """

    target_date = target_date or timezone.localdate()

    if not is_user_birthday(user=user, target_date=target_date):
        return None, False

    role_code = get_user_role_code(user)
    title = "С днём рождения!"
    message = get_birthday_message_by_role(role_code)

    deduplication_key = build_deduplication_key(
        user_id=user.id,
        notification_type=NotificationType.BIRTHDAY,
        source_type=NotificationSourceType.USER,
        source_id=user.id,
        target_date=target_date,
    )

    return create_notification(
        recipient=user,
        title=title,
        message=message,
        notification_type=NotificationType.BIRTHDAY,
        category=NotificationCategory.BIRTHDAY,
        level=NotificationLevel.SUCCESS,
        source_type=NotificationSourceType.USER,
        source_id=str(user.id),
        deduplication_key=deduplication_key,
        delivery_channels=[
            NotificationDeliveryChannel.IN_APP,
            NotificationDeliveryChannel.EMAIL,
        ],
        payload={
            "target_date": target_date.isoformat(),
            "role_code": role_code,
            "should_send_email": True,
        },
    )


def is_user_birthday(*, user, target_date) -> bool:
    """
    Проверяет, является ли выбранная дата днём рождения пользователя.
    """

    birth_date = getattr(user, "birth_date", None)

    if not birth_date:
        return False

    return birth_date.day == target_date.day and birth_date.month == target_date.month


def get_birthday_message_by_role(role_code: str) -> str:
    """
    Возвращает текст поздравления по роли пользователя.
    """

    messages = {
        "teacher": (
            "Поздравляем с днём рождения! Спасибо за ваш труд, внимание к студентам "
            "и вклад в развитие образовательной среды."
        ),
        "learner": (
            "Поздравляем с днём рождения! Желаем интересного обучения, смелых целей "
            "и уверенного движения к мечте."
        ),
        "guardian": (
            "Поздравляем с днём рождения! Желаем тепла, радости и приятных событий "
            "в этот прекрасный день."
        ),
        "admin": (
            "Поздравляем с днём рождения! Желаем спокойной работы платформы, "
            "сильных решений и вдохновения."
        ),
    }

    return messages.get(
        role_code,
        "Поздравляем с днём рождения! Желаем радости, вдохновения и прекрасного дня.",
    )


def get_user_role_code(user) -> str:
    """
    Возвращает активную роль пользователя для поздравления.
    """

    settings_obj = getattr(user, "settings", None)

    if settings_obj and settings_obj.active_role:
        return settings_obj.active_role

    if user.is_superuser:
        return "admin"

    return "learner"
