from __future__ import annotations

from apps.organizations.selectors import (
    get_active_subject_by_code,
    get_active_subject_by_id,
    get_active_subjects_queryset,
    get_admin_active_subjects_queryset_for_actor,
    get_admin_subjects_queryset_for_actor,
    get_subject_by_id,
    get_subjects_base_queryset,
)
from apps.organizations.tests.factories import (
    assign_user_role,
    create_organization,
    create_subject,
    create_superadmin,
    create_test_user,
)
from apps.users.constants.roles import RoleCode
from django.test import TestCase


class SubjectSelectorsTestCase(TestCase):
    """
    Тесты селекторов учебных предметов.
    """

    def setUp(self) -> None:
        self.superadmin = create_superadmin(
            email="superadmin-subject-selectors@example.com",
            phone="+79998400001",
        )
        self.regular_user = create_test_user(
            email="regular-subject-selectors@example.com",
            phone="+79998400002",
        )
        self.organization = create_organization(
            name="Организация предметов",
            short_name="Предметы",
            code="subject_selector_org",
            slug="subject-selector-org",
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
        self.inactive_subject = create_subject(
            name="Неактивный предмет",
            short_name="Неактивный",
            code="inactive_subject",
            is_active=False,
        )

    def test_get_subjects_base_queryset_returns_all_subjects(self) -> None:
        """
        Базовый selector возвращает все предметы.
        """

        queryset = get_subjects_base_queryset()

        self.assertIn(self.math, queryset)
        self.assertIn(self.physics, queryset)
        self.assertIn(self.inactive_subject, queryset)

    def test_get_active_subjects_queryset_returns_only_active_subjects(
        self,
    ) -> None:
        """
        Selector активных предметов возвращает только активные предметы.
        """

        queryset = get_active_subjects_queryset()

        self.assertIn(self.math, queryset)
        self.assertIn(self.physics, queryset)
        self.assertNotIn(self.inactive_subject, queryset)

    def test_get_subject_by_id_returns_subject(self) -> None:
        """
        Selector возвращает предмет по ID.
        """

        subject = get_subject_by_id(subject_id=self.math.id)

        self.assertEqual(subject, self.math)

    def test_get_subject_by_id_returns_none_for_empty_id(self) -> None:
        """
        Selector возвращает None, если ID не передан.
        """

        subject = get_subject_by_id(subject_id=None)

        self.assertIsNone(subject)

    def test_get_active_subject_by_id_returns_only_active_subject(self) -> None:
        """
        Selector активного предмета по ID не возвращает неактивный предмет.
        """

        active_subject = get_active_subject_by_id(subject_id=self.math.id)
        inactive_subject = get_active_subject_by_id(
            subject_id=self.inactive_subject.id,
        )

        self.assertEqual(active_subject, self.math)
        self.assertIsNone(inactive_subject)

    def test_get_active_subject_by_code_returns_subject(self) -> None:
        """
        Selector возвращает активный предмет по коду.
        """

        subject = get_active_subject_by_code(code="math")

        self.assertEqual(subject, self.math)

    def test_get_active_subject_by_code_returns_none_for_inactive_subject(
        self,
    ) -> None:
        """
        Selector не возвращает неактивный предмет по коду.
        """

        subject = get_active_subject_by_code(code="inactive_subject")

        self.assertIsNone(subject)

    def test_get_active_subject_by_code_returns_none_for_empty_code(self) -> None:
        """
        Selector возвращает None, если код пустой.
        """

        subject = get_active_subject_by_code(code="")

        self.assertIsNone(subject)

    def test_superadmin_sees_all_admin_subjects(self) -> None:
        """
        Суперадмин видит весь справочник предметов.
        """

        queryset = get_admin_subjects_queryset_for_actor(
            actor=self.superadmin,
        )

        self.assertIn(self.math, queryset)
        self.assertIn(self.physics, queryset)
        self.assertIn(self.inactive_subject, queryset)

    def test_org_admin_sees_all_admin_subjects(self) -> None:
        """
        Администратор организации видит глобальный справочник предметов.
        """

        admin = create_test_user(
            email="subject-org-admin@example.com",
            phone="+79998400003",
        )
        assign_user_role(
            user=admin,
            role_code=RoleCode.ORG_ADMIN,
            organization=self.organization,
            assigned_by=self.superadmin,
        )

        queryset = get_admin_subjects_queryset_for_actor(actor=admin)

        self.assertIn(self.math, queryset)
        self.assertIn(self.physics, queryset)
        self.assertIn(self.inactive_subject, queryset)

    def test_regular_user_sees_no_admin_subjects(self) -> None:
        """
        Обычный пользователь не видит предметы в админке.
        """

        queryset = get_admin_subjects_queryset_for_actor(
            actor=self.regular_user,
        )

        self.assertEqual(queryset.count(), 0)

    def test_get_admin_active_subjects_queryset_for_actor_returns_only_active(
        self,
    ) -> None:
        """
        Admin selector активных предметов исключает неактивные предметы.
        """

        queryset = get_admin_active_subjects_queryset_for_actor(
            actor=self.superadmin,
        )

        self.assertIn(self.math, queryset)
        self.assertIn(self.physics, queryset)
        self.assertNotIn(self.inactive_subject, queryset)
