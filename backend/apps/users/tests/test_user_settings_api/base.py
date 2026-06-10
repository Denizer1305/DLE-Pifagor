from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

User = get_user_model()


class UserSettingsApiTestBase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="teacher@example.com",
            phone="+79007771003",
            password="StrongPassword123!",
            first_name="Елена",
            last_name="Плеханова",
        )

        self.base_url = "/api/v1/users/settings/me/"
        self.appearance_url = "/api/v1/users/settings/me/appearance/"
        self.notifications_url = "/api/v1/users/settings/me/notifications/"
        self.privacy_url = "/api/v1/users/settings/me/privacy/"
        self.roles_url = "/api/v1/users/settings/me/roles/"
        self.security_url = "/api/v1/users/settings/me/security/"
        self.change_password_url = "/api/v1/users/settings/me/security/change-password/"
        self.sessions_url = "/api/v1/users/settings/me/security/sessions/"

    def authenticate(self) -> None:
        self.client.force_authenticate(user=self.user)
