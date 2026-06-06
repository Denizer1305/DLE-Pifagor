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
from apps.users.constants.lifecycle import ProfileStatus, UserRoleStatus
from apps.users.constants.onboarding import JoinRequestStatus, JoinRequestType
from apps.users.constants.roles import RoleCode
from apps.users.models import UserJoinRequest, UserRole
from apps.users.services import approve_join_request, reject_join_request
from django.test import TestCase


class JoinRequestReviewServicesTestCase(TestCase):
    """
    Тесты сервисов рассмотрения заявок пользователей.
    """

    def setUp(self) -> None:
        self.superadmin = create_superadmin(
            email="superadmin-join-service@example.com",
            phone="+79999200001",
        )
        self.organization = create_organization(
            name="Организация сервисов заявок",
            short_name="Сервисы заявок",
            code="join_service_org",
            slug="join-service-org",
        )
        self.department = create_department(
            organization=self.organization,
            name="ИТ-отделение",
            short_name="ИТ",
            code="it_join_service",
        )
        self.group = create_study_group(
            organization=self.organization,
            department=self.department,
            name="ИС-21",
            code="is_21_join_service",
        )
        self.reviewer = create_test_user(
            email="reviewer-join-service@example.com",
            phone="+79999200002",
        )
        assign_user_role(
            user=self.reviewer,
            role_code=RoleCode.ORG_ADMIN,
            organization=self.organization,
            assigned_by=self.superadmin,
        )

        self.teacher = create_teacher(
            organization=self.organization,
            email="teacher-join-service@example.com",
            phone="+79999200003",
        )
        TeacherOrganization.objects.filter(
            teacher=self.teacher,
            organization=self.organization,
        ).delete()

        self.teacher.teacher_profile.status = ProfileStatus.PENDING_REVIEW
        self.teacher.teacher_profile.save(update_fields=["status"])

        self.teacher_role = UserRole.objects.get(
            user=self.teacher,
            role__code=RoleCode.TEACHER,
            organization=self.organization,
        )
        self.teacher_role.status = UserRoleStatus.PENDING
        self.teacher_role.save(update_fields=["status"])

        self.teacher_request = UserJoinRequest.objects.create(
            request_type=JoinRequestType.TEACHER_TO_ORGANIZATION,
            user=self.teacher,
            organization=self.organization,
            department=self.department,
            status=JoinRequestStatus.PENDING,
            message="Хочу работать преподавателем.",
        )

        self.learner = create_test_user(
            email="learner-join-service@example.com",
            phone="+79999200004",
        )
        assign_user_role(
            user=self.learner,
            role_code=RoleCode.LEARNER,
            organization=self.organization,
            department=self.department,
            group=self.group,
            assigned_by=self.superadmin,
        )
        self.learner_role = UserRole.objects.get(
            user=self.learner,
            role__code=RoleCode.LEARNER,
            organization=self.organization,
            group=self.group,
        )
        self.learner_role.status = UserRoleStatus.PENDING
        self.learner_role.save(update_fields=["status"])

        self.learner_request = UserJoinRequest.objects.create(
            request_type=JoinRequestType.LEARNER_TO_GROUP,
            user=self.learner,
            organization=self.organization,
            department=self.department,
            group=self.group,
            status=JoinRequestStatus.PENDING,
            message="Хочу вступить в группу.",
        )

    def test_approve_teacher_request_creates_teacher_organization(self) -> None:
        """
        Подтверждение заявки преподавателя создаёт связь с организацией.
        """

        join_request = approve_join_request(
            join_request=self.teacher_request,
            reviewer=self.reviewer,
            comment="Преподаватель принят.",
        )

        self.teacher_request.refresh_from_db()
        self.teacher.teacher_profile.refresh_from_db()
        self.teacher_role.refresh_from_db()

        self.assertEqual(join_request.status, JoinRequestStatus.APPROVED)
        self.assertEqual(self.teacher_request.reviewed_by, self.reviewer)
        self.assertEqual(self.teacher.teacher_profile.status, ProfileStatus.VERIFIED)
        self.assertEqual(self.teacher_role.status, UserRoleStatus.ACTIVE)

        teacher_organization = TeacherOrganization.objects.get(
            teacher=self.teacher,
            organization=self.organization,
        )

        self.assertTrue(teacher_organization.is_active)
        self.assertTrue(teacher_organization.is_primary)

    def test_approve_teacher_request_reactivates_existing_teacher_organization(
        self,
    ) -> None:
        """
        Подтверждение заявки восстанавливает существующую неактивную связь.
        """

        TeacherOrganization.objects.create(
            teacher=self.teacher,
            organization=self.organization,
            position="Преподаватель",
            is_primary=False,
            is_active=False,
        )

        approve_join_request(
            join_request=self.teacher_request,
            reviewer=self.reviewer,
            comment="Преподаватель восстановлен.",
        )

        teacher_organization = TeacherOrganization.objects.get(
            teacher=self.teacher,
            organization=self.organization,
        )

        self.assertTrue(teacher_organization.is_active)
        self.assertTrue(teacher_organization.is_primary)

    def test_approve_learner_request_activates_learner_role(self) -> None:
        """
        Подтверждение заявки учащегося активирует роль учащегося.
        """

        approve_join_request(
            join_request=self.learner_request,
            reviewer=self.reviewer,
            comment="Учащийся принят.",
        )

        self.learner_request.refresh_from_db()
        self.learner_role.refresh_from_db()

        self.assertEqual(self.learner_request.status, JoinRequestStatus.APPROVED)
        self.assertEqual(self.learner_role.status, UserRoleStatus.ACTIVE)

    def test_reject_join_request_changes_status_and_comment(self) -> None:
        """
        Отклонение заявки сохраняет статус и комментарий.
        """

        join_request = reject_join_request(
            join_request=self.teacher_request,
            reviewer=self.reviewer,
            comment="Недостаточно данных.",
        )

        self.teacher_request.refresh_from_db()

        self.assertEqual(join_request.status, JoinRequestStatus.REJECTED)
        self.assertEqual(self.teacher_request.reviewed_by, self.reviewer)
        self.assertEqual(self.teacher_request.review_comment, "Недостаточно данных.")