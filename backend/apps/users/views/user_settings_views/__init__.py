from apps.users.views.user_settings_views.access import UserSettingsAccessMixin
from apps.users.views.user_settings_views.base import UserSettingsBaseMixin
from apps.users.views.user_settings_views.general import UserSettingsGeneralMixin
from apps.users.views.user_settings_views.security import UserSettingsSecurityMixin
from rest_framework import viewsets


class UserSettingsViewSet(
    UserSettingsBaseMixin,
    UserSettingsGeneralMixin,
    UserSettingsAccessMixin,
    UserSettingsSecurityMixin,
    viewsets.ViewSet,
):
    """API personal settings of the current user."""


__all__ = ["UserSettingsViewSet"]
