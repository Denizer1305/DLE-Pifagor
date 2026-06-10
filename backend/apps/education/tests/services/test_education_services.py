from __future__ import annotations

from datetime import date

from apps.education.models import (
    CurriculumItem,
    LearnerGroupEnrollment,
    TeacherGroupSubject,
)
from apps.education.services import (
    complete_learner_group_enrollment,
    create_curriculum_item,
    create_teacher_group_subject,
    set_current_academic_year,
    set_current_education_period,
)
from apps.education.tests.factories import (
    create_academic_year,
    create_curriculum,
    create_education_period,
    create_group_subject,
    create_learner_group_enrollment,
    create_subject,
    create_teacher_organization,
    create_teacher_subject,
    create_user,
)
from django.core.exceptions import ValidationError
from django.test import TestCase


class EducationServicesTestCase(TestCase):
    """
    Тесты сервисного слоя education.
    """

    def test_set_current_academic_year_unsets_previous_current_year(self) -> None:
        """
        Назначение текущего учебного года снимает старый текущий год.
        """

        old_year = create_academic_year(
            name="2024/2025",
            start_date=date(2024, 9, 1),
            end_date=date(2025, 6, 30),
            is_current=True,
        )
        new_year = create_academic_year(
            name="2025/2026",
            start_date=date(2025, 9, 1),
            end_date=date(2026, 6, 30),
            is_current=False,
        )

        set_current_academic_year(academic_year=new_year)

        old_year.refresh_from_db()
        new_year.refresh_from_db()

        self.assertFalse(old_year.is_current)
        self.assertTrue(new_year.is_current)

    def test_set_current_period_unsets_previous_current_period(self) -> None:
        """
        Назначение текущего периода снимает текущий флаг у старого периода года.
        """

        academic_year = create_academic_year()

        old_period = create_education_period(
            academic_year=academic_year,
            code="semester_1",
            sequence=1,
            is_current=True,
        )
        new_period = create_education_period(
            academic_year=academic_year,
            name="2 семестр",
            code="semester_2",
            sequence=2,
            start_date=date(academic_year.end_date.year, 1, 10),
            end_date=academic_year.end_date,
            is_current=False,
        )

        set_current_education_period(period=new_period)

        old_period.refresh_from_db()
        new_period.refresh_from_db()

        self.assertFalse(old_period.is_current)
        self.assertTrue(new_period.is_current)

    def test_curriculum_item_rejects_period_from_another_year(self) -> None:
        """
        Элемент учебного плана не принимает период другого учебного года.
        """

        curriculum = create_curriculum()
        another_year = create_academic_year(
            name="2026/2027",
            start_date=date(2026, 9, 1),
            end_date=date(2027, 6, 30),
        )
        wrong_period = create_education_period(
            academic_year=another_year,
            code="wrong_period",
        )

        with self.assertRaises(ValidationError):
            create_curriculum_item(
                data={
                    "curriculum": curriculum,
                    "period": wrong_period,
                    "subject": create_subject(),
                    "sequence": 1,
                    "planned_hours": 72,
                    "contact_hours": 48,
                    "independent_hours": 24,
                    "assessment_type": CurriculumItem.AssessmentTypeChoices.EXAM,
                    "is_required": True,
                    "is_active": True,
                    "notes": "",
                }
            )

    def test_teacher_assignment_rejects_hours_over_group_subject_hours(self) -> None:
        """
        Назначение преподавателя не может превысить часы предмета группы.
        """

        group_subject = create_group_subject(planned_hours=40)
        teacher = create_user(role_code="teacher")

        create_teacher_organization(
            teacher=teacher,
            organization=group_subject.group.organization,
        )
        create_teacher_subject(
            teacher=teacher,
            subject=group_subject.subject,
        )

        with self.assertRaises(ValidationError):
            create_teacher_group_subject(
                data={
                    "teacher": teacher,
                    "group_subject": group_subject,
                    "role": TeacherGroupSubject.RoleChoices.PRIMARY,
                    "is_primary": True,
                    "is_active": True,
                    "planned_hours": 80,
                    "starts_at": group_subject.period.start_date,
                    "ends_at": group_subject.period.end_date,
                    "notes": "",
                }
            )

    def test_complete_enrollment_sets_finished_status_and_unsets_primary(self) -> None:
        """
        Завершение зачисления выставляет статус и снимает основной флаг.
        """

        enrollment = create_learner_group_enrollment(is_primary=True)

        complete_learner_group_enrollment(
            enrollment=enrollment,
            completion_date=enrollment.academic_year.end_date,
            status=LearnerGroupEnrollment.StatusChoices.GRADUATED,
        )

        enrollment.refresh_from_db()

        self.assertEqual(
            enrollment.status,
            LearnerGroupEnrollment.StatusChoices.GRADUATED,
        )
        self.assertFalse(enrollment.is_primary)
