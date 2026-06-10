from __future__ import annotations

from apps.organizations.selectors import (
    actor_can_access_teacher_subject,
    actor_can_manage_teacher_subject,
    get_active_teacher_subject_by_id,
    get_active_teacher_subjects_for_teacher,
    get_active_teacher_subjects_queryset,
    get_admin_active_teacher_subjects_queryset_for_actor,
    get_admin_teacher_subjects_queryset_for_actor,
    get_primary_teacher_subject,
    get_teacher_subject_by_id,
    get_teacher_subjects_base_queryset,
    get_teacher_subjects_for_subject,
    get_teacher_subjects_for_teacher,
)
from apps.organizations.tests.factories import (
    assign_user_role,
    create_organization,
    create_subject,
    create_superadmin,
    create_teacher,
    create_teacher_subject,
    create_test_user,
)
from apps.users.constants.roles import RoleCode
from django.test import TestCase


class TeacherSubjectSelectorsTestCase(TestCase):
    """
    Тесты селекторов предметов преподавателей.
    """

    def setUp(self) -> None:
        self.superadmin = create_superadmin(
            email="superadmin-teacher-subject-selectors@example.com",
            phone="+79998500001",
        )
        self.regular_user = create_test_user(
            email="regular-teacher-subject-selectors@example.com",
            phone="+79998500002",
        )

        self.organization = create_organization(
            name="Организация предметов преподавателей",
            short_name="Предметы преподавателей",
            code="teacher_subject_selector_org",
            slug="teacher-subject-selector-org",
        )
        self.other_organization = create_organization(
            name="Другая организация предметов преподавателей",
            short_name="Другая",
            code="other_teacher_subject_selector_org",
            slug="other-teacher-subject-selector-org",
        )

        self.teacher = create_teacher(
            organization=self.organization,
            email="teacher-subject-selector@example.com",
            phone="+79998500003",
            first_name="Иван",
            last_name="Иванов",
            position="Преподаватель",
        )
        self.other_teacher = create_teacher(
            organization=self.other_organization,
            email="other-teacher-subject-selector@example.com",
            phone="+79998500004",
            first_name="Пётр",
            last_name="Петров",
            position="Преподаватель",
        )

        self.math = create_subject(
            name="Математика",
            short_name="Математика",
            code="math",
            is_active=True,
        )
        self.physics = create_subject(
            name="Физика",
            short_name="Физика",
            code="physics",
            is_active=True,
        )
        self.history = create_subject(
            name="История",
            short_name="История",
            code="history",
            is_active=True,
        )
        self.inactive_subject = create_subject(
            name="Неактивный предмет",
            short_name="Неактивный",
            code="inactive_teacher_subject_selector",
            is_active=False,
        )

        self.teacher_subject = create_teacher_subject(
            teacher=self.teacher,
            subject=self.math,
            is_primary=True,
            is_active=True,
        )
        self.second_teacher_subject = create_teacher_subject(
            teacher=self.teacher,
            subject=self.physics,
            is_primary=False,
            is_active=True,
        )
        self.inactive_teacher_subject = create_teacher_subject(
            teacher=self.teacher,
            subject=self.history,
            is_primary=False,
            is_active=False,
        )
        self.teacher_subject_with_inactive_subject = create_teacher_subject(
            teacher=self.teacher,
            subject=self.inactive_subject,
            is_primary=False,
            is_active=True,
        )
        self.other_teacher_subject = create_teacher_subject(
            teacher=self.other_teacher,
            subject=self.history,
            is_primary=True,
            is_active=True,
        )

    def test_get_teacher_subjects_base_queryset_returns_all_links(self) -> None:
        """
        Базовый selector возвращает все связи преподавателей с предметами.
        """

        queryset = get_teacher_subjects_base_queryset()

        self.assertIn(self.teacher_subject, queryset)
        self.assertIn(self.second_teacher_subject, queryset)
        self.assertIn(self.inactive_teacher_subject, queryset)
        self.assertIn(self.teacher_subject_with_inactive_subject, queryset)
        self.assertIn(self.other_teacher_subject, queryset)

    def test_get_active_teacher_subjects_queryset_returns_only_active_links(
        self,
    ) -> None:
        """
        Selector активных связей исключает неактивные связи и неактивные предметы.
        """

        queryset = get_active_teacher_subjects_queryset()

        self.assertIn(self.teacher_subject, queryset)
        self.assertIn(self.second_teacher_subject, queryset)
        self.assertIn(self.other_teacher_subject, queryset)
        self.assertNotIn(self.inactive_teacher_subject, queryset)
        self.assertNotIn(self.teacher_subject_with_inactive_subject, queryset)

    def test_get_teacher_subject_by_id_returns_link(self) -> None:
        """
        Selector возвращает связь преподавателя с предметом по ID.
        """

        teacher_subject = get_teacher_subject_by_id(
            teacher_subject_id=self.teacher_subject.id,
        )

        self.assertEqual(teacher_subject, self.teacher_subject)

    def test_get_teacher_subject_by_id_returns_none_for_empty_id(self) -> None:
        """
        Selector возвращает None, если ID не передан.
        """

        teacher_subject = get_teacher_subject_by_id(
            teacher_subject_id=None,
        )

        self.assertIsNone(teacher_subject)

    def test_get_active_teacher_subject_by_id_returns_only_active_link(
        self,
    ) -> None:
        """
        Selector активной связи по ID не возвращает неактивную связь.
        """

        active_link = get_active_teacher_subject_by_id(
            teacher_subject_id=self.teacher_subject.id,
        )
        inactive_link = get_active_teacher_subject_by_id(
            teacher_subject_id=self.inactive_teacher_subject.id,
        )

        self.assertEqual(active_link, self.teacher_subject)
        self.assertIsNone(inactive_link)

    def test_get_teacher_subjects_for_teacher_returns_teacher_links(self) -> None:
        """
        Selector возвращает все предметы конкретного преподавателя.
        """

        queryset = get_teacher_subjects_for_teacher(
            teacher=self.teacher,
        )

        self.assertIn(self.teacher_subject, queryset)
        self.assertIn(self.second_teacher_subject, queryset)
        self.assertIn(self.inactive_teacher_subject, queryset)
        self.assertNotIn(self.other_teacher_subject, queryset)

    def test_get_active_teacher_subjects_for_teacher_returns_active_links(
        self,
    ) -> None:
        """
        Selector возвращает активные предметы конкретного преподавателя.
        """

        queryset = get_active_teacher_subjects_for_teacher(
            teacher=self.teacher,
        )

        self.assertIn(self.teacher_subject, queryset)
        self.assertIn(self.second_teacher_subject, queryset)
        self.assertNotIn(self.inactive_teacher_subject, queryset)
        self.assertNotIn(self.teacher_subject_with_inactive_subject, queryset)

    def test_get_primary_teacher_subject_returns_primary_link(self) -> None:
        """
        Selector возвращает основной предмет преподавателя.
        """

        teacher_subject = get_primary_teacher_subject(
            teacher=self.teacher,
        )

        self.assertEqual(teacher_subject, self.teacher_subject)

    def test_get_teacher_subjects_for_subject_returns_subject_links(self) -> None:
        """
        Selector возвращает связи по конкретному предмету.
        """

        queryset = get_teacher_subjects_for_subject(
            subject=self.math,
        )

        self.assertIn(self.teacher_subject, queryset)
        self.assertNotIn(self.second_teacher_subject, queryset)
        self.assertNotIn(self.other_teacher_subject, queryset)

    def test_superadmin_sees_all_teacher_subjects(self) -> None:
        """
        Суперадмин видит все связи преподавателей с предметами.
        """

        queryset = get_admin_teacher_subjects_queryset_for_actor(
            actor=self.superadmin,
        )

        self.assertIn(self.teacher_subject, queryset)
        self.assertIn(self.second_teacher_subject, queryset)
        self.assertIn(self.other_teacher_subject, queryset)

    def test_org_admin_sees_teacher_subjects_of_own_organization(self) -> None:
        """
        Администратор организации видит предметы преподавателей своей организации.
        """

        admin = create_test_user(
            email="teacher-subject-org-admin-selector@example.com",
            phone="+79998500005",
        )
        assign_user_role(
            user=admin,
            role_code=RoleCode.ORG_ADMIN,
            organization=self.organization,
            assigned_by=self.superadmin,
        )

        queryset = get_admin_teacher_subjects_queryset_for_actor(actor=admin)

        self.assertIn(self.teacher_subject, queryset)
        self.assertIn(self.second_teacher_subject, queryset)
        self.assertNotIn(self.other_teacher_subject, queryset)

    def test_regular_user_sees_no_teacher_subjects(self) -> None:
        """
        Обычный пользователь не видит предметы преподавателей в админке.
        """

        queryset = get_admin_teacher_subjects_queryset_for_actor(
            actor=self.regular_user,
        )

        self.assertEqual(queryset.count(), 0)

    def test_get_admin_active_teacher_subjects_returns_only_active_links(
        self,
    ) -> None:
        """
        Admin selector активных связей исключает неактивные связи.
        """

        queryset = get_admin_active_teacher_subjects_queryset_for_actor(
            actor=self.superadmin,
        )

        self.assertIn(self.teacher_subject, queryset)
        self.assertIn(self.second_teacher_subject, queryset)
        self.assertNotIn(self.inactive_teacher_subject, queryset)
        self.assertNotIn(self.teacher_subject_with_inactive_subject, queryset)

    def test_actor_can_access_teacher_subject(self) -> None:
        """
        Selector проверяет доступ к предмету преподавателя.
        """

        admin = create_test_user(
            email="teacher-subject-access-admin@example.com",
            phone="+79998500006",
        )
        assign_user_role(
            user=admin,
            role_code=RoleCode.ORG_ADMIN,
            organization=self.organization,
            assigned_by=self.superadmin,
        )

        self.assertTrue(
            actor_can_access_teacher_subject(
                actor=admin,
                teacher_subject=self.teacher_subject,
            )
        )
        self.assertFalse(
            actor_can_access_teacher_subject(
                actor=admin,
                teacher_subject=self.other_teacher_subject,
            )
        )

    def test_actor_can_manage_teacher_subject_matches_access_scope(self) -> None:
        """
        Управление предметом преподавателя совпадает с областью видимости.
        """

        admin = create_test_user(
            email="teacher-subject-manage-admin@example.com",
            phone="+79998500007",
        )
        assign_user_role(
            user=admin,
            role_code=RoleCode.ORG_ADMIN,
            organization=self.organization,
            assigned_by=self.superadmin,
        )

        self.assertTrue(
            actor_can_manage_teacher_subject(
                actor=admin,
                teacher_subject=self.teacher_subject,
            )
        )
        self.assertFalse(
            actor_can_manage_teacher_subject(
                actor=admin,
                teacher_subject=self.other_teacher_subject,
            )
        )
