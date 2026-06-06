from __future__ import annotations

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
from apps.users.selectors import (
    actor_can_access_join_request,
    actor_can_review_join_request,
    get_join_requests_queryset_for_actor,
    get_pending_join_requests_queryset_for_actor,
    get_pending_reviewable_join_requests_queryset_for_actor,
    get_reviewable_join_requests_queryset_for_actor,
)
from django.test import TestCase


class UserJoinRequestSelectorsTestCase(TestCase):
    """
    Тесты селекторов заявок пользователей.
    """

    def setUp(self) -> None:
        self.superadmin = create_superadmin(
            email="superadmin-join-selector@example.com",
            phone="+79999000001",
        )
        self.regular_user = create_test_user(
            email="regular-join-selector@example.com",
            phone="+79999000002",
        )

        self.organization = create_organization(
            name="Организация заявок",
            short_name="Заявки",
            code="join_selector_org",
            slug="join-selector-org",
        )
        self.other_organization = create_organization(
            name="Другая организация заявок",
            short_name="Другая",
            code="other_join_selector_org",
            slug="other-join-selector-org",
        )

        self.department = create_department(
            organization=self.organization,
            name="ИТ-отделение",
            short_name="ИТ",
            code="it_join_selector",
        )
        self.other_department = create_department(
            organization=self.other_organization,
            name="Экономическое отделение",
            short_name="Экономика",
            code="economics_join_selector",
        )

        self.group = create_study_group(
            organization=self.organization,
            department=self.department,
            name="ИС-21",
            code="is_21_join_selector",
        )
        self.other_group = create_study_group(
            organization=self.other_organization,
            department=self.other_department,
            name="ЭК-21",
            code="ek_21_join_selector",
        )

        self.teacher = create_teacher(
            organization=self.organization,
            email="teacher-join-selector@example.com",
            phone="+79999000003",
        )
        self.other_teacher = create_teacher(
            organization=self.other_organization,
            email="other-teacher-join-selector@example.com",
            phone="+79999000004",
        )
        self.learner = create_test_user(
            email="learner-join-selector@example.com",
            phone="+79999000005",
        )
        self.other_learner = create_test_user(
            email="other-learner-join-selector@example.com",
            phone="+79999000006",
        )

        self.teacher_request = UserJoinRequest.objects.create(
            request_type=JoinRequestType.TEACHER_TO_ORGANIZATION,
            user=self.teacher,
            organization=self.organization,
            department=self.department,
            status=JoinRequestStatus.PENDING,
            message="Хочу преподавать в организации.",
        )
        self.other_teacher_request = UserJoinRequest.objects.create(
            request_type=JoinRequestType.TEACHER_TO_ORGANIZATION,
            user=self.other_teacher,
            organization=self.other_organization,
            department=self.other_department,
            status=JoinRequestStatus.PENDING,
            message="Заявка в чужую организацию.",
        )
        self.learner_request = UserJoinRequest.objects.create(
            request_type=JoinRequestType.LEARNER_TO_GROUP,
            user=self.learner,
            organization=self.organization,
            department=self.department,
            group=self.group,
            status=JoinRequestStatus.PENDING,
            message="Хочу вступить в группу.",
        )
        self.other_learner_request = UserJoinRequest.objects.create(
            request_type=JoinRequestType.LEARNER_TO_GROUP,
            user=self.other_learner,
            organization=self.other_organization,
            department=self.other_department,
            group=self.other_group,
            status=JoinRequestStatus.PENDING,
            message="Заявка в чужую группу.",
        )

    def test_superadmin_sees_all_join_requests(self) -> None:
        """
        Суперадминистратор видит все заявки.
        """

        queryset = get_join_requests_queryset_for_actor(actor=self.superadmin)

        self.assertIn(self.teacher_request, queryset)
        self.assertIn(self.other_teacher_request, queryset)
        self.assertIn(self.learner_request, queryset)
        self.assertIn(self.other_learner_request, queryset)

    def test_regular_user_sees_only_own_join_requests(self) -> None:
        """
        Обычный пользователь видит только свои заявки.
        """

        queryset = get_join_requests_queryset_for_actor(actor=self.learner)

        self.assertIn(self.learner_request, queryset)
        self.assertNotIn(self.teacher_request, queryset)
        self.assertNotIn(self.other_teacher_request, queryset)
        self.assertNotIn(self.other_learner_request, queryset)

    def test_org_admin_sees_requests_of_own_organization(self) -> None:
        """
        Администратор организации видит заявки своей организации.
        """

        admin = create_test_user(
            email="org-admin-join-selector@example.com",
            phone="+79999000007",
        )
        assign_user_role(
            user=admin,
            role_code=RoleCode.ORG_ADMIN,
            organization=self.organization,
            assigned_by=self.superadmin,
        )

        queryset = get_reviewable_join_requests_queryset_for_actor(actor=admin)

        self.assertIn(self.teacher_request, queryset)
        self.assertIn(self.learner_request, queryset)
        self.assertNotIn(self.other_teacher_request, queryset)
        self.assertNotIn(self.other_learner_request, queryset)

    def test_department_head_sees_requests_of_own_department(self) -> None:
        """
        Заведующий отделением видит заявки своего отделения.
        """

        head = create_test_user(
            email="head-join-selector@example.com",
            phone="+79999000008",
        )
        assign_user_role(
            user=head,
            role_code=RoleCode.DEPARTMENT_HEAD,
            organization=self.organization,
            department=self.department,
            assigned_by=self.superadmin,
        )

        queryset = get_reviewable_join_requests_queryset_for_actor(actor=head)

        self.assertIn(self.teacher_request, queryset)
        self.assertIn(self.learner_request, queryset)
        self.assertNotIn(self.other_teacher_request, queryset)
        self.assertNotIn(self.other_learner_request, queryset)

    def test_curator_sees_requests_of_own_group(self) -> None:
        """
        Куратор видит заявки своей группы.
        """

        curator = create_test_user(
            email="curator-join-selector@example.com",
            phone="+79999000009",
        )
        assign_user_role(
            user=curator,
            role_code=RoleCode.CURATOR,
            organization=self.organization,
            department=self.department,
            group=self.group,
            assigned_by=self.superadmin,
        )

        queryset = get_reviewable_join_requests_queryset_for_actor(actor=curator)

        self.assertIn(self.learner_request, queryset)
        self.assertNotIn(self.teacher_request, queryset)
        self.assertNotIn(self.other_teacher_request, queryset)
        self.assertNotIn(self.other_learner_request, queryset)

    def test_pending_queryset_for_actor_returns_only_pending_requests(self) -> None:
        """
        Selector pending-заявок исключает уже рассмотренные заявки.
        """

        self.learner_request.status = JoinRequestStatus.APPROVED
        self.learner_request.save(update_fields=["status"])

        queryset = get_pending_join_requests_queryset_for_actor(
            actor=self.superadmin,
        )

        self.assertIn(self.teacher_request, queryset)
        self.assertNotIn(self.learner_request, queryset)

    def test_pending_reviewable_queryset_returns_only_pending_reviewable_requests(
        self,
    ) -> None:
        """
        Selector pending-заявок проверяющего исключает рассмотренные заявки.
        """

        admin = create_test_user(
            email="pending-review-admin@example.com",
            phone="+79999000010",
        )
        assign_user_role(
            user=admin,
            role_code=RoleCode.ORG_ADMIN,
            organization=self.organization,
            assigned_by=self.superadmin,
        )

        self.learner_request.status = JoinRequestStatus.APPROVED
        self.learner_request.save(update_fields=["status"])

        queryset = get_pending_reviewable_join_requests_queryset_for_actor(
            actor=admin,
        )

        self.assertIn(self.teacher_request, queryset)
        self.assertNotIn(self.learner_request, queryset)

    def test_actor_can_access_own_join_request(self) -> None:
        """
        Пользователь может видеть собственную заявку.
        """

        self.assertTrue(
            actor_can_access_join_request(
                actor=self.learner,
                join_request=self.learner_request,
            )
        )

    def test_actor_can_review_join_request_in_scope(self) -> None:
        """
        Администратор может рассмотреть заявку в своей области.
        """

        admin = create_test_user(
            email="review-admin@example.com",
            phone="+79999000011",
        )
        assign_user_role(
            user=admin,
            role_code=RoleCode.ORG_ADMIN,
            organization=self.organization,
            assigned_by=self.superadmin,
        )

        self.assertTrue(
            actor_can_review_join_request(
                actor=admin,
                join_request=self.teacher_request,
            )
        )
        self.assertFalse(
            actor_can_review_join_request(
                actor=admin,
                join_request=self.other_teacher_request,
            )
        )

    def test_actor_cannot_review_own_join_request(self) -> None:
        """
        Пользователь не может рассматривать собственную заявку.
        """

        assign_user_role(
            user=self.teacher,
            role_code=RoleCode.ORG_ADMIN,
            organization=self.organization,
            assigned_by=self.superadmin,
        )

        self.assertFalse(
            actor_can_review_join_request(
                actor=self.teacher,
                join_request=self.teacher_request,
            )
        )