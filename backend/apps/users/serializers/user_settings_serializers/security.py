from __future__ import annotations

from apps.users.constants.settings import SessionLifetimeMode
from django.contrib.auth import password_validation
from rest_framework import serializers

SESSION_LIFETIME_MODES = {
    SessionLifetimeMode.STANDARD,
    SessionLifetimeMode.EXTENDED,
    SessionLifetimeMode.STRICT,
}


class SecuritySettingsUpdateSerializer(serializers.Serializer):
    login_notifications_enabled = serializers.BooleanField(required=False)
    suspicious_activity_notifications_enabled = serializers.BooleanField(required=False)
    trusted_devices_enabled = serializers.BooleanField(required=False)
    session_lifetime_mode = serializers.CharField(required=False)
    two_factor_enabled = serializers.BooleanField(required=False)

    def validate_session_lifetime_mode(self, value: str) -> str:
        if value not in SESSION_LIFETIME_MODES:
            raise serializers.ValidationError("Недопустимый режим длительности сессии.")

        return value


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    new_password_confirm = serializers.CharField(write_only=True)

    def validate_current_password(self, value: str) -> str:
        user = self.context["request"].user

        if not user.check_password(value):
            raise serializers.ValidationError("Текущий пароль указан неверно.")

        return value

    def validate(self, attrs: dict) -> dict:
        if attrs["new_password"] != attrs["new_password_confirm"]:
            raise serializers.ValidationError(
                {
                    "new_password_confirm": "Пароли не совпадают.",
                }
            )

        password_validation.validate_password(
            attrs["new_password"],
            self.context["request"].user,
        )

        return attrs
