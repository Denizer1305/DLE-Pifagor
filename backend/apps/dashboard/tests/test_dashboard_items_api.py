from __future__ import annotations

from apps.dashboard.models import DashboardItem
from apps.notifications.models import Notification
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

User = get_user_model()


class DashboardItemsApiTestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.url = "/api/v1/dashboard/me/items/"
        self.user = User.objects.create_user(
            email="calendar@example.com",
            phone="+79990000770",
            password="StrongPassword123!",
            first_name="Ирина",
            last_name="Календарева",
        )

    def test_items_require_authentication(self) -> None:
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 401)

    def test_user_creates_and_reads_calendar_event(self) -> None:
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            self.url,
            {
                "kind": "calendar",
                "title": "Консультация",
                "text": "Встреча с преподавателем",
                "date": "2026-05-27",
                "event_type": "lesson",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(DashboardItem.objects.count(), 1)

        list_response = self.client.get(self.url)

        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(list_response.data[0]["title"], "Консультация")

    def test_user_creates_note(self) -> None:
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            self.url,
            {
                "kind": "note",
                "title": "Подготовить материалы",
                "text": "Проверить список документов",
                "date": "2026-05-28",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["kind"], "note")

    def test_enabled_today_item_creates_notification(self) -> None:
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            self.url,
            {
                "kind": "calendar",
                "title": "Встреча сегодня",
                "text": "",
                "date": timezone.localdate().isoformat(),
                "notification_enabled": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data["notification_enabled"])
        self.assertEqual(Notification.objects.filter(recipient=self.user).count(), 1)

    def test_disabled_today_note_does_not_create_notification(self) -> None:
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            self.url,
            {
                "kind": "note",
                "title": "Личная заметка",
                "text": "",
                "date": timezone.localdate().isoformat(),
                "notification_enabled": False,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertFalse(response.data["notification_enabled"])
        self.assertFalse(Notification.objects.filter(recipient=self.user).exists())

    def test_delete_item_removes_related_notification(self) -> None:
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            self.url,
            {
                "kind": "calendar",
                "title": "Удаляемая встреча",
                "text": "",
                "date": timezone.localdate().isoformat(),
                "notification_enabled": True,
            },
            format="json",
        )

        item_id = response.data["id"]
        delete_response = self.client.delete(f"{self.url}{item_id}/")

        self.assertEqual(delete_response.status_code, 204)
        self.assertFalse(DashboardItem.objects.filter(id=item_id).exists())
        self.assertFalse(Notification.objects.filter(recipient=self.user).exists())

    def test_delete_notification_removes_calendar_source(self) -> None:
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            self.url,
            {
                "kind": "calendar",
                "title": "Встреча из уведомления",
                "text": "",
                "date": timezone.localdate().isoformat(),
                "notification_enabled": True,
            },
            format="json",
        )

        item_id = response.data["id"]
        notification = Notification.objects.get(recipient=self.user)
        delete_response = self.client.delete(
            f"/api/v1/notifications/{notification.id}/"
        )

        self.assertEqual(delete_response.status_code, 200)
        self.assertFalse(DashboardItem.objects.filter(id=item_id).exists())
