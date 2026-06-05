from apps.users.serializers.user_settings_serializers.appearance import (
    AppearanceSettingsUpdateSerializer,
)
from apps.users.serializers.user_settings_serializers.notifications import (
    NotificationSettingsUpdateSerializer,
)
from apps.users.serializers.user_settings_serializers.privacy import (
    PrivacySettingsUpdateSerializer,
)
from apps.users.serializers.user_settings_serializers.roles import (
    RoleSettingsUpdateSerializer,
)
from apps.users.serializers.user_settings_serializers.security import (
    SecuritySettingsUpdateSerializer,
)
from rest_framework import serializers


class UserSettingsUpdateSerializer(serializers.Serializer):
    appearance = AppearanceSettingsUpdateSerializer(required=False)
    notifications = NotificationSettingsUpdateSerializer(required=False)
    privacy = PrivacySettingsUpdateSerializer(required=False)
    security = SecuritySettingsUpdateSerializer(required=False)
    roles = RoleSettingsUpdateSerializer(required=False)
