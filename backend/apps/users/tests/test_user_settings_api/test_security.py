from apps.users.tests.test_user_settings_api.base import UserSettingsApiTestBase
from rest_framework import status


class TestUserSettingsSecurityApi(UserSettingsApiTestBase):
    def test_update_security_settings(self) -> None:
        self.authenticate()

        response = self.client.patch(
            self.security_url,
            data={
                "login_notifications_enabled": True,
                "suspicious_activity_notifications_enabled": True,
                "trusted_devices_enabled": False,
                "session_lifetime_mode": "strict",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["trusted_devices_enabled"])
        self.assertEqual(response.data["session_lifetime_mode"], "strict")

    def test_change_password(self) -> None:
        self.authenticate()

        response = self.client.post(
            self.change_password_url,
            data={
                "current_password": "StrongPassword123!",
                "new_password": "NewStrongPassword123!",
                "new_password_confirm": "NewStrongPassword123!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("NewStrongPassword123!"))

    def test_change_password_rejects_wrong_current_password(self) -> None:
        self.authenticate()

        response = self.client.post(
            self.change_password_url,
            data={
                "current_password": "WrongPassword123!",
                "new_password": "NewStrongPassword123!",
                "new_password_confirm": "NewStrongPassword123!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_security_sessions_returns_current_session(self) -> None:
        self.authenticate()

        response = self.client.get(self.sessions_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("items", response.data)
        self.assertGreaterEqual(len(response.data["items"]), 1)
        self.assertEqual(response.data["items"][0]["id"], "current")
