from __future__ import annotations

from apps.notifications.constants import (
    CRITICAL_NOTIFICATION_CATEGORIES,
    CRITICAL_NOTIFICATION_LEVELS,
    NotificationCategory,
    NotificationDeliveryChannel,
)
from apps.users.constants.settings import (
    NotificationFrequency as UserNotificationFrequency,
)
from apps.users.services.user_settings.defaults import get_default_notification_settings
from apps.users.services.user_settings.payloads import (
    build_notification_settings_payload,
)
from django.core.exceptions import ObjectDoesNotExist

CATEGORY_FREQUENCY_KEYS = {
    NotificationCategory.DAILY_SUMMARY: "digest",
    NotificationCategory.ASSIGNMENTS: "assignments",
    NotificationCategory.TESTS: "assignments",
    NotificationCategory.SCHEDULE: "schedule",
    NotificationCategory.CALENDAR: "schedule",
    NotificationCategory.NOTES: "schedule",
    NotificationCategory.BIRTHDAY: "education",
    NotificationCategory.EDUCATION: "education",
    NotificationCategory.FEEDBACK: "feedback",
    NotificationCategory.MODERATION: "feedback",
    NotificationCategory.SECURITY: "security",
    NotificationCategory.SYSTEM: "system",
}


def should_create_notification_for_recipient(
    *,
    recipient,
    category: str,
    level: str,
) -> bool:
    if is_required_notification(category=category, level=level):
        return True

    settings = get_recipient_notification_settings(recipient=recipient)
    frequency_key = CATEGORY_FREQUENCY_KEYS.get(category, "system")
    frequency = settings.get("frequency", {}).get(frequency_key)
    channels = settings.get("channels", {})

    return frequency != UserNotificationFrequency.DISABLED and channels.get(
        NotificationDeliveryChannel.IN_APP, True
    )


def resolve_delivery_channels_for_recipient(
    *,
    recipient,
    category: str,
    level: str,
    channels: list[str] | None,
) -> list[str]:
    settings = get_recipient_notification_settings(recipient=recipient)
    channel_settings = settings.get("channels", {})
    normalized_channels = normalize_channels(channels)
    force_in_app = is_required_notification(category=category, level=level)
    allowed_channels = []

    for channel in normalized_channels:
        if force_in_app and channel == NotificationDeliveryChannel.IN_APP:
            allowed_channels.append(channel)
            continue

        if channel_settings.get(channel, True):
            allowed_channels.append(channel)

    if force_in_app and NotificationDeliveryChannel.IN_APP not in allowed_channels:
        allowed_channels.append(NotificationDeliveryChannel.IN_APP)

    return allowed_channels


def get_recipient_notification_settings(*, recipient) -> dict:
    try:
        settings_obj = recipient.settings
    except ObjectDoesNotExist:
        return get_default_notification_settings()

    return build_notification_settings_payload(settings_obj=settings_obj)


def is_required_notification(*, category: str, level: str) -> bool:
    return (
        category in CRITICAL_NOTIFICATION_CATEGORIES
        or level in CRITICAL_NOTIFICATION_LEVELS
    )


def normalize_channels(channels: list[str] | None) -> list[str]:
    source_channels = channels or [NotificationDeliveryChannel.IN_APP]
    normalized_channels = []

    for channel in source_channels:
        if channel not in normalized_channels:
            normalized_channels.append(channel)

    if NotificationDeliveryChannel.IN_APP not in normalized_channels:
        normalized_channels.append(NotificationDeliveryChannel.IN_APP)

    return normalized_channels
