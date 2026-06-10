from apps.users.tests.test_user_settings_api.base import UserSettingsApiTestBase
from rest_framework import status


class TestUserSettingsAccessApi(UserSettingsApiTestBase):
    def test_update_privacy_settings(self) -> None:
        self.authenticate()

        response = self.client.patch(
            self.privacy_url,
            data={
                "profile_visibility": "private",
                "show_email": False,
                "show_phone": False,
                "show_birth_date": False,
                "allow_students_access": False,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["profile_visibility"], "private")
        self.assertFalse(response.data["show_email"])

    def test_update_role_settings(self) -> None:
        self.authenticate()

        response = self.client.patch(
            self.roles_url,
            data={
                "active_role": "teacher",
                "roles": {
                    "teacher": {
                        "show_hero_block": False,
                        "show_ai_card": True,
                    }
                },
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["active_role"], "teacher")
        self.assertFalse(response.data["roles"]["teacher"]["show_hero_block"])
        self.assertTrue(response.data["roles"]["teacher"]["show_ai_card"])

    def test_role_settings_reject_unknown_role(self) -> None:
        self.authenticate()

        response = self.client.patch(
            self.roles_url,
            data={"roles": {"hacker": {"show_admin_panel": True}}},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
