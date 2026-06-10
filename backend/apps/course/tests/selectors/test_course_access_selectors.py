from __future__ import annotations

from apps.course.models import CourseAccessRule, CourseEnrollment
from apps.course.selectors import (
    course_access_rule_list_queryset,
    course_enrollment_list_queryset,
    course_group_access_list_queryset,
    get_course_access_rule_by_code,
    get_course_access_rule_by_id,
    get_course_enrollment_by_course_and_learner,
    get_course_enrollment_by_id,
    get_course_group_access_by_course_and_group,
    get_course_group_access_by_id,
)
from apps.course.tests.factories import (
    create_course,
    create_course_access_rule,
    create_course_enrollment,
    create_course_group_access,
    create_learner,
    create_study_group,
    unique_code,
)
from django.test import TestCase


def get_enrollment_status_value(
    *status_names: str,
    default: str = "active",
) -> str:
    """
    Возвращает первое существующее значение статуса записи на курс.
    """

    for status_name in status_names:
        if hasattr(CourseEnrollment.StatusChoices, status_name):
            return getattr(CourseEnrollment.StatusChoices, status_name)

    choices = getattr(CourseEnrollment.StatusChoices, "choices", ())

    if choices:
        return choices[0][0]

    return default


class CourseAccessSelectorsTestCase(TestCase):
    """
    Тесты селекторов доступа к курсам.
    """

    def setUp(self) -> None:
        """
        Подготавливает доступы и записи на курс.
        """

        self.course = create_course(
            title="Access Selectors Course",
        )
        self.other_course = create_course(
            title="Other Access Course",
        )
        self.group = create_study_group(
            organization=self.course.organization,
        )
        self.learner = create_learner(
            email="course-access-selector-learner@example.com",
        )

        self.group_access = create_course_group_access(
            course=self.course,
            group=self.group,
        )
        self.access_rule = create_course_access_rule(
            course=self.course,
            learner=self.learner,
            access_code=unique_code("rule"),
            access_type=CourseAccessRule.AccessTypeChoices.LEARNER,
        )
        self.initial_enrollment_status = get_enrollment_status_value(
            "NOT_STARTED",
            "ENROLLED",
            "ACTIVE",
            "IN_PROGRESS",
            default="active",
        )

        self.enrollment = create_course_enrollment(
            course=self.course,
            learner=self.learner,
            group_access=self.group_access,
            access_rule=self.access_rule,
            status=self.initial_enrollment_status,
        )

        self.other_group_access = create_course_group_access(
            course=self.other_course,
        )

    def test_group_access_list_filters_by_course(self) -> None:
        """
        Групповые доступы фильтруются по курсу.
        """

        access_ids = set(
            course_group_access_list_queryset(
                course_id=self.course.id,
            ).values_list(
                "id",
                flat=True,
            )
        )

        self.assertIn(self.group_access.id, access_ids)
        self.assertNotIn(self.other_group_access.id, access_ids)

    def test_group_access_list_filters_by_group(self) -> None:
        """
        Групповые доступы фильтруются по группе.
        """

        access_ids = set(
            course_group_access_list_queryset(
                group_id=self.group.id,
            ).values_list(
                "id",
                flat=True,
            )
        )

        self.assertIn(self.group_access.id, access_ids)

    def test_get_group_access_by_id_returns_access(self) -> None:
        """
        Селектор возвращает групповой доступ по id.
        """

        access = get_course_group_access_by_id(self.group_access.id)

        self.assertEqual(access.id, self.group_access.id)

    def test_get_group_access_by_course_and_group_returns_access(self) -> None:
        """
        Селектор возвращает групповой доступ по курсу и группе.
        """

        access = get_course_group_access_by_course_and_group(
            course_id=self.course.id,
            group_id=self.group.id,
        )

        self.assertEqual(access.id, self.group_access.id)

    def test_access_rule_list_filters_by_course(self) -> None:
        """
        Правила доступа фильтруются по курсу.
        """

        rule_ids = set(
            course_access_rule_list_queryset(
                course_id=self.course.id,
            ).values_list(
                "id",
                flat=True,
            )
        )

        self.assertIn(self.access_rule.id, rule_ids)

    def test_access_rule_list_filters_by_access_type(self) -> None:
        """
        Правила доступа фильтруются по типу доступа.
        """

        rule_ids = set(
            course_access_rule_list_queryset(
                access_type=CourseAccessRule.AccessTypeChoices.LEARNER,
            ).values_list(
                "id",
                flat=True,
            )
        )

        self.assertIn(self.access_rule.id, rule_ids)

    def test_get_access_rule_by_id_returns_rule(self) -> None:
        """
        Селектор возвращает правило доступа по id.
        """

        rule = get_course_access_rule_by_id(self.access_rule.id)

        self.assertEqual(rule.id, self.access_rule.id)

    def test_get_access_rule_by_code_returns_rule(self) -> None:
        """
        Селектор возвращает правило доступа по коду.
        """

        rule = get_course_access_rule_by_code(self.access_rule.access_code)

        self.assertEqual(rule.id, self.access_rule.id)

    def test_enrollment_list_filters_by_course(self) -> None:
        """
        Записи на курс фильтруются по курсу.
        """

        enrollment_ids = set(
            course_enrollment_list_queryset(
                course_id=self.course.id,
            ).values_list(
                "id",
                flat=True,
            )
        )

        self.assertIn(self.enrollment.id, enrollment_ids)

    def test_enrollment_list_filters_by_learner(self) -> None:
        """
        Записи на курс фильтруются по обучающемуся.
        """

        enrollment_ids = set(
            course_enrollment_list_queryset(
                learner_id=self.learner.id,
            ).values_list(
                "id",
                flat=True,
            )
        )

        self.assertIn(self.enrollment.id, enrollment_ids)

    def test_enrollment_list_filters_by_status(self) -> None:
        """
        Записи на курс фильтруются по статусу.
        """

        enrollment_ids = set(
            course_enrollment_list_queryset(
                status=self.initial_enrollment_status,
            ).values_list(
                "id",
                flat=True,
            )
        )

        self.assertIn(self.enrollment.id, enrollment_ids)

    def test_get_enrollment_by_id_returns_enrollment(self) -> None:
        """
        Селектор возвращает запись на курс по id.
        """

        enrollment = get_course_enrollment_by_id(self.enrollment.id)

        self.assertEqual(enrollment.id, self.enrollment.id)

    def test_get_enrollment_by_course_and_learner_returns_enrollment(self) -> None:
        """
        Селектор возвращает запись по курсу и обучающемуся.
        """

        enrollment = get_course_enrollment_by_course_and_learner(
            course_id=self.course.id,
            learner_id=self.learner.id,
        )

        self.assertEqual(enrollment.id, self.enrollment.id)
