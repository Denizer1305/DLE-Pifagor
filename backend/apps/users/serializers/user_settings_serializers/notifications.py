from __future__ import annotations

from apps.users.constants.settings import NotificationFrequency
from rest_framework import serializers

NOTIFICATION_FREQUENCIES = {
    NotificationFrequency.INSTANT,
    NotificationFrequency.DAILY,
    NotificationFrequency.WEEKLY,
    NotificationFrequency.DISABLED,
}

ALLOWED_CHANNELS = {
    "in_app",
    "email",
    "vk",
    "max",
}

ALLOWED_CATEGORIES = {
    "security",
    "education",
    "assignments",
    "schedule",
    "feedback",
    "system",
    "digest",
    "marketing",
}


class NotificationSettingsUpdateSerializer(serializers.Serializer):
    channels = serializers.DictField(required=False)
    frequency = serializers.DictField(required=False)
    digest_time = serializers.RegexField(
        regex=r"^(?:[01]\d|2[0-3]):[0-5]\d$",
        required=False,
    )

    def validate_channels(self, value: dict) -> dict:
        for channel, is_enabled in value.items():
            if channel not in ALLOWED_CHANNELS:
                raise serializers.ValidationError(
                    f"Недопустимый канал уведомлений: {channel}."
                )

            if not isinstance(is_enabled, bool):
                raise serializers.ValidationError(
                    f"Значение канала {channel} должно быть boolean."
                )

        return value

    def validate_frequency(self, value: dict) -> dict:
        for category, frequency in value.items():
            if category not in ALLOWED_CATEGORIES:
                raise serializers.ValidationError(
                    f"Недопустимая категория уведомлений: {category}."
                )

            if frequency not in NOTIFICATION_FREQUENCIES:
                raise serializers.ValidationError(
                    f"Недопустимая частота уведомлений: {frequency}."
                )

        return value
