from __future__ import annotations

from apps.users.constants.settings import ProfileVisibility
from rest_framework import serializers

PROFILE_VISIBILITIES = {
    ProfileVisibility.PUBLIC,
    ProfileVisibility.ORGANIZATION,
    ProfileVisibility.ROLE_ONLY,
    ProfileVisibility.PRIVATE,
}


class PrivacySettingsUpdateSerializer(serializers.Serializer):
    profile_visibility = serializers.CharField(required=False)
    show_email = serializers.BooleanField(required=False)
    show_phone = serializers.BooleanField(required=False)
    show_city = serializers.BooleanField(required=False)
    show_birth_date = serializers.BooleanField(required=False)
    show_role_profile = serializers.BooleanField(required=False)
    show_achievements = serializers.BooleanField(required=False)
    allow_teachers_access = serializers.BooleanField(required=False)
    allow_students_access = serializers.BooleanField(required=False)
    allow_guardians_access = serializers.BooleanField(required=False)
    allow_admins_access = serializers.BooleanField(required=False)
    allow_data_export = serializers.BooleanField(required=False)

    def validate_profile_visibility(self, value: str) -> str:
        if value not in PROFILE_VISIBILITIES:
            raise serializers.ValidationError("Недопустимый режим видимости профиля.")

        return value
