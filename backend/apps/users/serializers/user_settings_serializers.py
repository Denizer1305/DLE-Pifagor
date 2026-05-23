from __future__ import annotations

from apps.users.models import UserSettings
from rest_framework import serializers


class UserSettingsSerializer(serializers.ModelSerializer):
    """
    Сериализатор настроек пользователя.
    """

    class Meta:
        model = UserSettings
        fields = [
            "id",
            "language",
            "timezone",
            "active_role",
            "interface_theme",
            "compact_mode",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "active_role",
            "created_at",
            "updated_at",
        ]


class UserSettingsUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор обновления настроек пользователя.
    """

    class Meta:
        model = UserSettings
        fields = [
            "language",
            "timezone",
            "interface_theme",
            "compact_mode",
        ]


class SetActiveRoleSerializer(serializers.Serializer):
    """
    Сериализатор установки активной роли пользователя.
    """

    role_code = serializers.CharField(max_length=64)
