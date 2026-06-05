"""Serializers for personal user settings endpoints."""

from apps.users.serializers.user_settings_serializers.appearance import (
    AppearanceSettingsUpdateSerializer,
)
from apps.users.serializers.user_settings_serializers.notifications import (
    NotificationSettingsUpdateSerializer,
)
from apps.users.serializers.user_settings_serializers.payloads import (
    UserSettingsPayloadSerializer,
)
from apps.users.serializers.user_settings_serializers.privacy import (
    PrivacySettingsUpdateSerializer,
)
from apps.users.serializers.user_settings_serializers.roles import (
    RoleSettingsUpdateSerializer,
)
from apps.users.serializers.user_settings_serializers.security import (
    ChangePasswordSerializer,
    SecuritySettingsUpdateSerializer,
)
from apps.users.serializers.user_settings_serializers.updates import (
    UserSettingsUpdateSerializer,
)

__all__ = [
    "AppearanceSettingsUpdateSerializer",
    "ChangePasswordSerializer",
    "NotificationSettingsUpdateSerializer",
    "PrivacySettingsUpdateSerializer",
    "RoleSettingsUpdateSerializer",
    "SecuritySettingsUpdateSerializer",
    "UserSettingsPayloadSerializer",
    "UserSettingsUpdateSerializer",
]
