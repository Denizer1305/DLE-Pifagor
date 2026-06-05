from apps.users.selectors import get_or_create_settings_for_user
from apps.users.tests.test_user_settings_api.base import User, UserSettingsApiTestBase
from rest_framework import status


class TestUserSettingsGeneralApi(UserSettingsApiTestBase):
    def test_settings_requires_authentication(self) -> None:
        response = self.client.get(self.base_url)

        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN],
        )

    def test_settings_me_returns_full_payload(self) -> None:
        self.authenticate()

        response = self.client.get(self.base_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("appearance", response.data)
        self.assertIn("notifications", response.data)
        self.assertIn("privacy", response.data)
        self.assertIn("security", response.data)
        self.assertIn("roles", response.data)

    def test_settings_are_created_for_user_automatically(self) -> None:
        self.authenticate()
        self.assertFalse(hasattr(self.user, "settings"))

        response = self.client.get(self.base_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(hasattr(User.objects.get(id=self.user.id), "settings"))
        self.assertEqual(response.data["appearance"]["color_mode"], "system")

    def test_update_appearance_settings(self) -> None:
        self.authenticate()

        response = self.client.patch(
            self.appearance_url,
            data={
                "theme": "violet",
                "color_mode": "dark",
                "density": "compact",
                "animations_enabled": False,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["theme"], "violet")
        self.assertEqual(response.data["color_mode"], "dark")
        self.assertEqual(response.data["density"], "compact")
        self.assertFalse(response.data["animations_enabled"])

        settings_obj = get_or_create_settings_for_user(self.user)
        self.assertEqual(settings_obj.appearance_settings["theme"], "violet")

    def test_update_appearance_rejects_invalid_theme(self) -> None:
        self.authenticate()

        response = self.client.patch(
            self.appearance_url,
            data={"theme": "telegram-blue"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_appearance_accepts_extended_logo_theme(self) -> None:
        self.authenticate()

        response = self.client.patch(
            self.appearance_url,
            data={"theme": "light-blue"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["theme"], "light-blue")

    def test_dark_appearance_can_store_dark_display_mode(self) -> None:
        self.authenticate()

        response = self.client.patch(
            self.appearance_url,
            data={"theme": "dark", "color_mode": "dark"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["theme"], "dark")
        self.assertEqual(response.data["color_mode"], "dark")

    def test_update_appearance_stores_interface_language(self) -> None:
        self.authenticate()

        response = self.client.patch(
            self.appearance_url,
            data={"language": "fr"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["language"], "fr")
        self.assertEqual(
            get_or_create_settings_for_user(self.user).language,
            "fr",
        )

    def test_update_appearance_rejects_invalid_language(self) -> None:
        self.authenticate()

        response = self.client.patch(
            self.appearance_url,
            data={"language": "it"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_notification_settings(self) -> None:
        self.authenticate()

        response = self.client.patch(
            self.notifications_url,
            data={
                "channels": {
                    "in_app": True,
                    "email": False,
                    "vk": True,
                    "max": False,
                },
                "frequency": {
                    "security": "instant",
                    "education": "daily",
                    "marketing": "disabled",
                },
                "digest_time": "09:30",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["channels"]["email"])
        self.assertTrue(response.data["channels"]["vk"])
        self.assertEqual(response.data["frequency"]["education"], "daily")
        self.assertEqual(response.data["digest_time"], "09:30")

    def test_notification_settings_reject_telegram_channel(self) -> None:
        self.authenticate()

        response = self.client.patch(
            self.notifications_url,
            data={"channels": {"telegram": True}},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
