from __future__ import annotations

from apps.users.constants.settings import SettingsRoleCode
from rest_framework import serializers

SETTINGS_ROLE_CODES = {
    SettingsRoleCode.TEACHER,
    SettingsRoleCode.LEARNER,
    SettingsRoleCode.GUARDIAN,
    SettingsRoleCode.ADMIN,
}


class RoleSettingsUpdateSerializer(serializers.Serializer):
    active_role = serializers.CharField(required=False)
    roles = serializers.DictField(required=False)

    def validate_active_role(self, value: str) -> str:
        if value not in SETTINGS_ROLE_CODES:
            raise serializers.ValidationError("Недопустимая роль для настроек.")

        return value

    def validate_roles(self, value: dict) -> dict:
        for role_code, role_settings in value.items():
            if role_code not in SETTINGS_ROLE_CODES:
                raise serializers.ValidationError(
                    f"Недопустимая роль в настройках: {role_code}."
                )

            if not isinstance(role_settings, dict):
                raise serializers.ValidationError(
                    f"Настройки роли {role_code} должны быть объектом."
                )

            for setting_name, setting_value in role_settings.items():
                if not isinstance(setting_value, bool):
                    raise serializers.ValidationError(
                        f"Настройка {setting_name} роли {role_code} должна быть boolean."
                    )

        return value
