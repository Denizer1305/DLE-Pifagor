from __future__ import annotations

from apps.notifications.constants import (
    NotificationCategory,
    NotificationSourceType,
    NotificationType,
)
from apps.notifications.services import build_deduplication_key, create_notification
from apps.users.constants.lifecycle import UserRoleStatus
from apps.users.constants.roles import RoleCode
from apps.users.models import LearnerProfile, UserRole
from apps.users.tests.factories import make_role, make_user
from django.test import TestCase
from rest_framework.test import APIClient


class UserDashboardNotificationsApiTestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def create_notification_for(self, user, source_id: str) -> None:
        create_notification(
            recipient=user,
            title="Новое уведомление",
            message="Событие доступно в личном кабинете.",
            notification_type=NotificationType.SYSTEM,
            category=NotificationCategory.SYSTEM,
            source_type=NotificationSourceType.SYSTEM,
            source_id=source_id,
            deduplication_key=build_deduplication_key(
                user_id=user.id,
                notification_type=NotificationType.SYSTEM,
                source_type=NotificationSourceType.SYSTEM,
                source_id=source_id,
            ),
        )

    def assign_role(self, user, role_code: str) -> None:
        UserRole.objects.create(
            user=user,
            role=make_role(code=role_code),
            status=UserRoleStatus.ACTIVE,
        )

    def test_teacher_summary_returns_notifications_and_unread_stat(self) -> None:
        teacher = make_user(email="teacher-dashboard@example.com")
        self.assign_role(teacher, RoleCode.TEACHER)
        self.create_notification_for(teacher, "teacher-dashboard")
        self.client.force_authenticate(user=teacher)

        response = self.client.get("/api/v1/dashboard/teacher/summary/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["notifications"][0]["title"], "Новое уведомление"
        )
        stats = {item["key"]: item["value"] for item in response.data["stats"]}
        self.assertEqual(stats["notifications"], 1)

    def test_student_summary_returns_notifications_and_day_count(self) -> None:
        student = make_user(email="student-dashboard@example.com")
        self.assign_role(student, RoleCode.LEARNER)
        self.create_notification_for(student, "student-dashboard")
        self.client.force_authenticate(user=student)

        response = self.client.get("/api/v1/dashboard/student/summary/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["notifications"][0]["title"], "Новое уведомление"
        )
        self.assertEqual(response.data["day_stats"]["notifications"], 1)

    def test_student_onboarding_summary_is_available_before_role_review(self) -> None:
        student = make_user(email="student-onboarding@example.com")
        UserRole.objects.create(
            user=student,
            role=make_role(code=RoleCode.LEARNER),
            status=UserRoleStatus.PENDING,
        )
        LearnerProfile.objects.create(user=student)
        self.client.force_authenticate(user=student)

        response = self.client.get("/api/v1/dashboard/student/summary/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["profile"]["email"], student.email)

    def test_parent_summary_returns_notifications_and_profile(self) -> None:
        parent = make_user(email="parent-dashboard@example.com")
        self.assign_role(parent, RoleCode.GUARDIAN)
        self.create_notification_for(parent, "parent-dashboard")
        self.client.force_authenticate(user=parent)

        response = self.client.get("/api/v1/dashboard/parent/summary/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["profile"]["email"], parent.email)
        self.assertEqual(
            response.data["notifications"][0]["title"], "Новое уведомление"
        )
        stats = {item["key"]: item["value"] for item in response.data["stats"]}
        self.assertEqual(stats["messages"], 1)
