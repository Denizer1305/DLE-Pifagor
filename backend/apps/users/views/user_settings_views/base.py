from apps.users.selectors import get_or_create_settings_for_user
from rest_framework.permissions import IsAuthenticated


class UserSettingsBaseMixin:
    permission_classes = [IsAuthenticated]

    def get_settings_obj(self):
        return get_or_create_settings_for_user(self.request.user)
