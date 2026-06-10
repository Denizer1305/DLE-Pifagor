from __future__ import annotations

from apps.organizations.models import TeacherOrganization
from apps.organizations.tests.factories import (
    assign_user_role,
    create_department,
    create_organization,
    create_study_group,
    create_superadmin,
    create_teacher,
    create_test_user,
)
from apps.users.constants.onboarding import JoinRequestStatus, JoinRequestType
from apps.users.constants.roles import RoleCode
from apps.users.models import UserJoinRequest
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


def get_response_items(response) -> list:
    """
    Возвращает список объектов из обычного, пагинированного
    или обёрнутого API-ответа.
    """

    data = response.json()

    if isinstance(data, list):
        return data

    if not isinstance(data, dict):
        return []

    if isinstance(data.get("results"), list):
        return data["results"]

    if isinstance(data.get("items"), list):
        return data["items"]

    nested_data = data.get("data")

    if isinstance(nested_data, list):
        return nested_data

    if isinstance(nested_data, dict):
        if isinstance(nested_data.get("results"), list):
            return nested_data["results"]

        if isinstance(nested_data.get("items"), list):
            return nested_data["items"]

    return []


class UserJoinRequestsApiTestCase(TestCase):
    """
    Тесты API заявок пользователей.
    """

    def setUp(self) -> None:
        self.client = APIClient()

        self.superadmin = create_superadmin(
            email="superadmin-join-api@example.com",
            phone="+79999100001",
        )
        self.organization = create_organization(
            name="Организация API заявок",
            short_name="API заявки",
            code="join_api_org",
            slug="join-api-org",
        )
        self.other_organization = create_organization(
            name="Другая организация API заявок",
            short_name="Другая",
            code="other_join_api_org",
            slug="other-join-api-org",
        )
        self.department = create_department(
            organization=self.organization,
            name="ИТ-отделение",
            short_name="ИТ",
            code="it_join_api",
        )
        self.other_department = create_department(
            organization=self.other_organization,
            name="Экономическое отделение",
            short_name="Экономика",
            code="economics_join_api",
        )
        self.group = create_study_group(
            organization=self.organization,
            department=self.department,
            name="ИС-21",
            code="is_21_join_api",
        )
        self.other_group = create_study_group(
            organization=self.other_organization,
            department=self.other_department,
            name="ЭК-21",
            code="ek_21_join_api",
        )

        self.admin = create_test_user(
            email="org-admin-join-api@example.com",
            phone="+79999100002",
        )
        assign_user_role(
            user=self.admin,
            role_code=RoleCode.ORG_ADMIN,
            organization=self.organization,
            assigned_by=self.superadmin,
        )

        self.curator = create_test_user(
            email="curator-join-api@example.com",
            phone="+79999100003",
        )
        assign_user_role(
            user=self.curator,
            role_code=RoleCode.CURATOR,
            organization=self.organization,
            department=self.department,
            group=self.group,
            assigned_by=self.superadmin,
        )

        self.teacher = create_teacher(
            organization=self.organization,
            email="teacher-join-api@example.com",
            phone="+79999100004",
        )
        self.other_teacher = create_teacher(
            organization=self.other_organization,
            email="other-teacher-join-api@example.com",
            phone="+79999100005",
        )
        self.learner = create_test_user(
            email="learner-join-api@example.com",
            phone="+79999100006",
        )
        self.other_learner = create_test_user(
            email="other-learner-join-api@example.com",
            phone="+79999100007",
        )

        self.teacher_request = UserJoinRequest.objects.create(
            request_type=JoinRequestType.TEACHER_TO_ORGANIZATION,
            user=self.teacher,
            organization=self.organization,
            department=self.department,
            status=JoinRequestStatus.PENDING,
        )
        self.other_teacher_request = UserJoinRequest.objects.create(
            request_type=JoinRequestType.TEACHER_TO_ORGANIZATION,
            user=self.other_teacher,
            organization=self.other_organization,
            department=self.other_department,
            status=JoinRequestStatus.PENDING,
        )
        self.learner_request = UserJoinRequest.objects.create(
            request_type=JoinRequestType.LEARNER_TO_GROUP,
            user=self.learner,
            organization=self.organization,
            department=self.department,
            group=self.group,
            status=JoinRequestStatus.PENDING,
        )
        self.other_learner_request = UserJoinRequest.objects.create(
            request_type=JoinRequestType.LEARNER_TO_GROUP,
            user=self.other_learner,
            organization=self.other_organization,
            department=self.other_department,
            group=self.other_group,
            status=JoinRequestStatus.PENDING,
        )

    def test_user_sees_only_own_join_requests(self) -> None:
        """
        Обычный пользователь видит только свои заявки.
        """

        self.client.force_authenticate(user=self.learner)

        url = reverse("users:join-requests-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        request_ids = {item["id"] for item in get_response_items(response)}

        self.assertIn(self.learner_request.id, request_ids)
        self.assertNotIn(self.teacher_request.id, request_ids)
        self.assertNotIn(self.other_teacher_request.id, request_ids)
        self.assertNotIn(self.other_learner_request.id, request_ids)

    def test_org_admin_sees_requests_of_own_organization(self) -> None:
        """
        Администратор организации видит входящие заявки своей организации.
        """

        self.client.force_authenticate(user=self.admin)

        url = reverse("users:join-requests-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        request_ids = {item["id"] for item in get_response_items(response)}

        self.assertIn(self.teacher_request.id, request_ids)
        self.assertIn(self.learner_request.id, request_ids)
        self.assertNotIn(self.other_teacher_request.id, request_ids)
        self.assertNotIn(self.other_learner_request.id, request_ids)

    def test_curator_sees_requests_of_own_group(self) -> None:
        """
        Куратор видит заявки учащихся в свою группу.
        """

        self.client.force_authenticate(user=self.curator)

        url = reverse("users:join-requests-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        request_ids = {item["id"] for item in get_response_items(response)}

        self.assertIn(self.learner_request.id, request_ids)
        self.assertNotIn(self.teacher_request.id, request_ids)
        self.assertNotIn(self.other_teacher_request.id, request_ids)
        self.assertNotIn(self.other_learner_request.id, request_ids)

    def test_org_admin_can_approve_teacher_request(self) -> None:
        """
        Администратор организации может подтвердить заявку преподавателя.
        """

        TeacherOrganization.objects.filter(
            teacher=self.teacher,
            organization=self.organization,
        ).delete()

        self.client.force_authenticate(user=self.admin)

        url = reverse(
            "users:join-requests-approve",
            kwargs={"pk": self.teacher_request.id},
        )
        response = self.client.post(
            url,
            {
                "comment": "Преподаватель принят.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.teacher_request.refresh_from_db()

        self.assertEqual(self.teacher_request.status, JoinRequestStatus.APPROVED)
        self.assertEqual(self.teacher_request.reviewed_by, self.admin)

        self.assertTrue(
            TeacherOrganization.objects.filter(
                teacher=self.teacher,
                organization=self.organization,
                is_active=True,
            ).exists()
        )

    def test_org_admin_cannot_approve_foreign_request(self) -> None:
        """
        Администратор организации не может подтвердить чужую заявку.
        """

        self.client.force_authenticate(user=self.admin)

        url = reverse(
            "users:join-requests-approve",
            kwargs={"pk": self.other_teacher_request.id},
        )
        response = self.client.post(
            url,
            {
                "comment": "Чужая заявка.",
            },
            format="json",
        )

        self.assertIn(
            response.status_code,
            (
                status.HTTP_403_FORBIDDEN,
                status.HTTP_404_NOT_FOUND,
            ),
        )

        self.other_teacher_request.refresh_from_db()

        self.assertEqual(
            self.other_teacher_request.status,
            JoinRequestStatus.PENDING,
        )

    def test_curator_can_approve_learner_request(self) -> None:
        """
        Куратор может подтвердить заявку учащегося в свою группу.
        """

        self.client.force_authenticate(user=self.curator)

        url = reverse(
            "users:join-requests-approve",
            kwargs={"pk": self.learner_request.id},
        )
        response = self.client.post(
            url,
            {
                "comment": "Учащийся принят.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.learner_request.refresh_from_db()

        self.assertEqual(self.learner_request.status, JoinRequestStatus.APPROVED)
        self.assertEqual(self.learner_request.reviewed_by, self.curator)

    def test_user_cannot_approve_own_join_request(self) -> None:
        """
        Пользователь не может подтвердить собственную заявку.
        """

        assign_user_role(
            user=self.teacher,
            role_code=RoleCode.ORG_ADMIN,
            organization=self.organization,
            assigned_by=self.superadmin,
        )

        self.client.force_authenticate(user=self.teacher)

        url = reverse(
            "users:join-requests-approve",
            kwargs={"pk": self.teacher_request.id},
        )
        response = self.client.post(
            url,
            {
                "comment": "Сам себя подтвердил.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.teacher_request.refresh_from_db()

        self.assertEqual(self.teacher_request.status, JoinRequestStatus.PENDING)

    def test_org_admin_can_reject_teacher_request(self) -> None:
        """
        Администратор организации может отклонить заявку преподавателя.
        """

        self.client.force_authenticate(user=self.admin)

        url = reverse(
            "users:join-requests-reject",
            kwargs={"pk": self.teacher_request.id},
        )
        response = self.client.post(
            url,
            {
                "comment": "Недостаточно данных.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.teacher_request.refresh_from_db()

        self.assertEqual(self.teacher_request.status, JoinRequestStatus.REJECTED)
        self.assertEqual(self.teacher_request.reviewed_by, self.admin)
        self.assertEqual(
            self.teacher_request.review_comment,
            "Недостаточно данных.",
        )
