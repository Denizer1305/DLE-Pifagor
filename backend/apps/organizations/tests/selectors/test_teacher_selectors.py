from __future__ import annotations

from apps.organizations.selectors import (
    filter_public_teachers_queryset,
    get_public_teacher_subjects_queryset,
    get_public_teachers_base_queryset,
    get_public_teachers_queryset,
)
from apps.organizations.tests.factories import (
    create_organization,
    create_subject,
    create_teacher,
    create_teacher_subject,
)
from apps.users.constants.lifecycle import ProfileStatus
from django.test import TestCase


class TeacherSelectorsTestCase(TestCase):
    """
    Тесты публичных селекторов преподавателей.
    """

    def setUp(self) -> None:
        self.organization = create_organization(
            name="Организация преподавателей",
            short_name="Преподаватели",
            code="teacher_selector_public_org",
            slug="teacher-selector-public-org",
            is_active=True,
            is_public=True,
            is_default_public=True,
        )
        self.other_organization = create_organization(
            name="Другая организация преподавателей",
            short_name="Другая",
            code="other_teacher_selector_public_org",
            slug="other-teacher-selector-public-org",
            is_active=True,
            is_public=True,
            is_default_public=False,
        )

        self.math = create_subject(
            name="Математика",
            short_name="Математика",
            code="math",
        )
        self.physics = create_subject(
            name="Физика",
            short_name="Физика",
            code="physics",
        )
        self.history = create_subject(
            name="История",
            short_name="История",
            code="history",
        )

        self.teacher = create_teacher(
            organization=self.organization,
            email="public-teacher-selector@example.com",
            phone="+79997500001",
            first_name="Иван",
            last_name="Иванов",
            middle_name="Иванович",
            position="Преподаватель математики",
            is_public=True,
            show_on_teachers_page=True,
            status=ProfileStatus.VERIFIED,
        )
        create_teacher_subject(
            teacher=self.teacher,
            subject=self.math,
            is_primary=True,
            is_active=True,
        )
        create_teacher_subject(
            teacher=self.teacher,
            subject=self.physics,
            is_primary=False,
            is_active=True,
        )

        self.hidden_teacher = create_teacher(
            organization=self.organization,
            email="hidden-teacher-selector@example.com",
            phone="+79997500002",
            first_name="Пётр",
            last_name="Петров",
            middle_name="Петрович",
            position="Скрытый преподаватель",
            is_public=False,
            show_on_teachers_page=True,
            status=ProfileStatus.VERIFIED,
        )

        self.not_shown_teacher = create_teacher(
            organization=self.organization,
            email="not-shown-teacher-selector@example.com",
            phone="+79997500003",
            first_name="Сергей",
            last_name="Сергеев",
            middle_name="Сергеевич",
            position="Не показывается на странице",
            is_public=True,
            show_on_teachers_page=False,
            status=ProfileStatus.VERIFIED,
        )

        self.unverified_teacher = create_teacher(
            organization=self.organization,
            email="unverified-teacher-selector@example.com",
            phone="+79997500004",
            first_name="Алексей",
            last_name="Алексеев",
            middle_name="Алексеевич",
            position="Преподаватель на проверке",
            is_public=True,
            show_on_teachers_page=True,
            status=ProfileStatus.PENDING_REVIEW,
        )

        self.other_teacher = create_teacher(
            organization=self.other_organization,
            email="other-public-teacher-selector@example.com",
            phone="+79997500005",
            first_name="Анна",
            last_name="Сидорова",
            middle_name="Андреевна",
            position="Преподаватель истории",
            is_public=True,
            show_on_teachers_page=True,
            status=ProfileStatus.VERIFIED,
        )
        create_teacher_subject(
            teacher=self.other_teacher,
            subject=self.history,
            is_primary=True,
            is_active=True,
        )

    def test_get_public_teachers_base_queryset_returns_only_public_verified_teachers(
        self,
    ) -> None:
        """
        Базовый selector возвращает только публичных подтверждённых преподавателей.
        """

        queryset = get_public_teachers_base_queryset(self.organization)

        self.assertIn(self.teacher.teacher_profile, queryset)
        self.assertNotIn(self.hidden_teacher.teacher_profile, queryset)
        self.assertNotIn(self.not_shown_teacher.teacher_profile, queryset)
        self.assertNotIn(self.unverified_teacher.teacher_profile, queryset)
        self.assertNotIn(self.other_teacher.teacher_profile, queryset)

    def test_get_public_teachers_base_queryset_returns_empty_for_none_organization(
        self,
    ) -> None:
        """
        Если организация не передана, selector возвращает пустой QuerySet.
        """

        queryset = get_public_teachers_base_queryset(None)

        self.assertEqual(queryset.count(), 0)

    def test_get_public_teachers_queryset_filters_by_search_in_full_name(
        self,
    ) -> None:
        """
        Поиск фильтрует преподавателей по ФИО.
        """

        queryset = get_public_teachers_queryset(
            self.organization,
            search="Иванов",
        )

        self.assertIn(self.teacher.teacher_profile, queryset)
        self.assertEqual(queryset.count(), 1)

    def test_get_public_teachers_queryset_filters_by_search_in_position(
        self,
    ) -> None:
        """
        Поиск фильтрует преподавателей по должности.
        """

        queryset = get_public_teachers_queryset(
            self.organization,
            search="математики",
        )

        self.assertIn(self.teacher.teacher_profile, queryset)
        self.assertEqual(queryset.count(), 1)

    def test_get_public_teachers_queryset_filters_by_subject_code(self) -> None:
        """
        Selector фильтрует преподавателей по коду предмета.
        """

        queryset = get_public_teachers_queryset(
            self.organization,
            subject="math",
        )

        self.assertIn(self.teacher.teacher_profile, queryset)
        self.assertEqual(queryset.count(), 1)

    def test_get_public_teachers_queryset_returns_empty_for_unknown_subject(
        self,
    ) -> None:
        """
        Неизвестный код предмета возвращает пустой QuerySet.
        """

        queryset = get_public_teachers_queryset(
            self.organization,
            subject="unknown_subject",
        )

        self.assertEqual(queryset.count(), 0)

    def test_get_public_teachers_queryset_filters_by_position(self) -> None:
        """
        Selector фильтрует преподавателей по должности.
        """

        queryset = get_public_teachers_queryset(
            self.organization,
            position="математики",
        )

        self.assertIn(self.teacher.teacher_profile, queryset)
        self.assertEqual(queryset.count(), 1)

    def test_filter_public_teachers_queryset_keeps_matching_teacher(self) -> None:
        """
        Низкоуровневый фильтр оставляет подходящего преподавателя.
        """

        base_queryset = get_public_teachers_base_queryset(self.organization)

        queryset = filter_public_teachers_queryset(
            queryset=base_queryset,
            search="Иван",
            subject="math",
            position="математики",
        )

        self.assertIn(self.teacher.teacher_profile, queryset)
        self.assertEqual(queryset.count(), 1)

    def test_get_public_teacher_subjects_queryset_returns_public_teacher_subjects(
        self,
    ) -> None:
        """
        Selector возвращает предметы публичных преподавателей организации.
        """

        queryset = get_public_teacher_subjects_queryset(self.organization)

        self.assertIn(self.math, queryset)
        self.assertIn(self.physics, queryset)
        self.assertNotIn(self.history, queryset)

    def test_get_public_teacher_subjects_queryset_ignores_hidden_teacher_subjects(
        self,
    ) -> None:
        """
        Предметы скрытых преподавателей не попадают в публичный список.
        """

        create_teacher_subject(
            teacher=self.hidden_teacher,
            subject=self.history,
            is_primary=True,
            is_active=True,
        )

        queryset = get_public_teacher_subjects_queryset(self.organization)

        self.assertNotIn(self.history, queryset)

    def test_get_public_teacher_subjects_queryset_ignores_inactive_subject_link(
        self,
    ) -> None:
        """
        Неактивная связь преподавателя с предметом не попадает в список.
        """

        literature = create_subject(
            name="Литература",
            short_name="Литература",
            code="literature",
        )
        create_teacher_subject(
            teacher=self.teacher,
            subject=literature,
            is_primary=False,
            is_active=False,
        )

        queryset = get_public_teacher_subjects_queryset(self.organization)

        self.assertNotIn(literature, queryset)

    def test_get_public_teacher_subjects_queryset_ignores_inactive_subject(
        self,
    ) -> None:
        """
        Неактивный предмет не попадает в публичный список фильтров.
        """

        inactive_subject = create_subject(
            name="Неактивный предмет",
            short_name="Неактивный",
            code="inactive_subject",
            is_active=False,
        )
        create_teacher_subject(
            teacher=self.teacher,
            subject=inactive_subject,
            is_primary=False,
            is_active=True,
        )

        queryset = get_public_teacher_subjects_queryset(self.organization)

        self.assertNotIn(inactive_subject, queryset)

    def test_get_public_teacher_subjects_queryset_returns_empty_for_none_organization(
        self,
    ) -> None:
        """
        Если организация не передана, selector возвращает пустой QuerySet предметов.
        """

        queryset = get_public_teacher_subjects_queryset(None)

        self.assertEqual(queryset.count(), 0)