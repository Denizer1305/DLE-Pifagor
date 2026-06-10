from __future__ import annotations

from apps.education.selectors import (
    academic_year_list_queryset,
    curriculum_list_queryset,
    get_active_group_subjects_for_group,
    get_primary_enrollment_for_learner,
    learner_group_enrollment_list_queryset,
)
from apps.education.tests.factories import (
    create_academic_year,
    create_curriculum,
    create_group_subject,
    create_learner_group_enrollment,
    create_organization,
    create_study_group,
    create_user,
)
from django.test import TestCase


class EducationSelectorsTestCase(TestCase):
    """
    Тесты селекторов education.
    """

    def test_academic_year_list_queryset_filters_by_search(self) -> None:
        """
        Селектор учебных годов ищет по названию.
        """

        first_year = create_academic_year(name="2025/2026")
        second_year = create_academic_year(
            name="2026/2027",
            start_date="2026-09-01",
            end_date="2027-06-30",
        )

        queryset = academic_year_list_queryset(search="2025")

        self.assertIn(first_year, queryset)
        self.assertNotIn(second_year, queryset)

    def test_curriculum_list_queryset_filters_by_organization(self) -> None:
        """
        Селектор учебных планов фильтрует по организации.
        """

        organization = create_organization(name="Основная организация")
        another_organization = create_organization(name="Другая организация")

        curriculum = create_curriculum(organization=organization)
        another_curriculum = create_curriculum(
            organization=another_organization,
            code="another_curriculum",
        )

        queryset = curriculum_list_queryset(
            organization_id=organization.id,
        )

        self.assertIn(curriculum, queryset)
        self.assertNotIn(another_curriculum, queryset)

    def test_get_active_group_subjects_for_group_returns_only_active(self) -> None:
        """
        Селектор предметов группы возвращает только активные предметы.
        """

        group = create_study_group()
        active_subject = create_group_subject(group=group, is_active=True)
        inactive_subject = create_group_subject(
            group=group,
            is_active=False,
            subject=None,
        )

        queryset = get_active_group_subjects_for_group(group.id)

        self.assertIn(active_subject, queryset)
        self.assertNotIn(inactive_subject, queryset)

    def test_primary_enrollment_selector_returns_primary_enrollment(self) -> None:
        """
        Селектор возвращает основное зачисление обучающегося.
        """

        learner = create_user(role_code="learner")
        primary = create_learner_group_enrollment(
            learner=learner,
            is_primary=True,
        )

        create_learner_group_enrollment(
            learner=learner,
            academic_year=primary.academic_year,
            group=create_study_group(),
            is_primary=False,
        )

        result = get_primary_enrollment_for_learner(
            learner.id,
            academic_year_id=primary.academic_year.id,
        )

        self.assertEqual(result, primary)

    def test_enrollment_list_queryset_filters_by_learner(self) -> None:
        """
        Селектор зачислений фильтрует по обучающемуся.
        """

        learner = create_user(role_code="learner")
        other_learner = create_user(role_code="learner")

        enrollment = create_learner_group_enrollment(learner=learner)
        other_enrollment = create_learner_group_enrollment(
            learner=other_learner,
            academic_year=enrollment.academic_year,
            group=create_study_group(),
            is_primary=False,
        )

        queryset = learner_group_enrollment_list_queryset(
            learner_id=learner.id,
        )

        self.assertIn(enrollment, queryset)
        self.assertNotIn(other_enrollment, queryset)
