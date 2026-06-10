from __future__ import annotations

from apps.course.models import CourseAccessRule, CourseEnrollment, CourseGroupAccess
from apps.course.services import (
    archive_course_enrollment,
    archive_course_group_access,
    cancel_course_enrollment,
    complete_course_enrollment,
    create_course_access_rule,
    create_course_enrollment,
    create_course_group_access,
    deactivate_course_access_rule,
    hide_course_for_group,
    restore_course_access_rule,
    show_course_for_group,
    start_course_enrollment,
    update_course_access_rule,
    update_course_enrollment,
    update_course_group_access,
)
from apps.course.tests.factories import create_course
from apps.course.tests.factories import (
    create_course_access_rule as factory_create_course_access_rule,
)
from apps.course.tests.factories import (
    create_course_enrollment as factory_create_course_enrollment,
)
from apps.course.tests.factories import (
    create_course_group_access as factory_create_course_group_access,
)
from apps.course.tests.factories import (
    create_learner,
    create_study_group,
    get_choice_value,
    unique_code,
)
from django.test import TestCase


class CourseAccessServicesTestCase(TestCase):
    """
    Тесты сервисов доступа к курсам.
    """

    def setUp(self) -> None:
        """
        Подготавливает данные доступа.
        """

        self.course = create_course()
        self.group = create_study_group(
            organization=self.course.organization,
        )
        self.learner = create_learner(
            email="course-access-services-learner@example.com",
        )

    def test_create_course_group_access_creates_access(self) -> None:
        """
        Сервис создаёт групповой доступ.
        """

        group_access = create_course_group_access(
            data={
                "course": self.course,
                "group": self.group,
                "visibility": CourseGroupAccess.VisibilityChoices.VISIBLE,
                "auto_enroll": True,
                "is_active": True,
            }
        )

        self.assertEqual(group_access.course_id, self.course.id)
        self.assertEqual(group_access.group_id, self.group.id)

    def test_update_course_group_access_updates_notes(self) -> None:
        """
        Сервис обновляет групповой доступ.
        """

        group_access = factory_create_course_group_access(
            course=self.course,
            group=self.group,
        )

        updated_access = update_course_group_access(
            group_access=group_access,
            data={
                "notes": "Новая заметка",
            },
        )

        self.assertEqual(updated_access.notes, "Новая заметка")

    def test_hide_and_show_course_for_group_change_visibility(self) -> None:
        """
        Сервисы скрывают и показывают курс группе.
        """

        group_access = factory_create_course_group_access(
            course=self.course,
            group=self.group,
            visibility=CourseGroupAccess.VisibilityChoices.VISIBLE,
        )

        hidden_access = hide_course_for_group(group_access=group_access)

        self.assertEqual(
            hidden_access.visibility,
            CourseGroupAccess.VisibilityChoices.HIDDEN,
        )

        shown_access = show_course_for_group(group_access=hidden_access)

        self.assertEqual(
            shown_access.visibility,
            CourseGroupAccess.VisibilityChoices.VISIBLE,
        )
        self.assertTrue(shown_access.is_active)

    def test_archive_course_group_access_sets_archived_state(self) -> None:
        """
        Сервис архивирует групповой доступ.
        """

        group_access = factory_create_course_group_access(
            course=self.course,
            group=self.group,
        )

        archived_access = archive_course_group_access(
            group_access=group_access,
        )

        self.assertEqual(
            archived_access.visibility,
            CourseGroupAccess.VisibilityChoices.ARCHIVED,
        )
        self.assertFalse(archived_access.is_active)

    def test_create_course_access_rule_creates_rule(self) -> None:
        """
        Сервис создаёт правило доступа.
        """

        access_rule = create_course_access_rule(
            data={
                "course": self.course,
                "access_type": CourseAccessRule.AccessTypeChoices.LEARNER,
                "learner": self.learner,
                "access_code": unique_code("access"),
                "auto_enroll": True,
                "is_active": True,
            }
        )

        self.assertEqual(access_rule.course_id, self.course.id)
        self.assertEqual(access_rule.learner_id, self.learner.id)

    def test_update_course_access_rule_updates_notes(self) -> None:
        """
        Сервис обновляет правило доступа.
        """

        access_rule = factory_create_course_access_rule(
            course=self.course,
            learner=self.learner,
        )

        updated_rule = update_course_access_rule(
            access_rule=access_rule,
            data={
                "notes": "Новое правило",
            },
        )

        self.assertEqual(updated_rule.notes, "Новое правило")

    def test_deactivate_and_restore_course_access_rule_change_active_flag(self) -> None:
        """
        Сервисы выключают и восстанавливают правило доступа.
        """

        access_rule = factory_create_course_access_rule(
            course=self.course,
            learner=self.learner,
            is_active=True,
        )

        deactivated_rule = deactivate_course_access_rule(
            access_rule=access_rule,
        )

        self.assertFalse(deactivated_rule.is_active)

        restored_rule = restore_course_access_rule(
            access_rule=deactivated_rule,
        )

        self.assertTrue(restored_rule.is_active)

    def test_create_course_enrollment_creates_enrollment(self) -> None:
        """
        Сервис создаёт запись на курс.
        """

        initial_status = get_choice_value(
            CourseEnrollment,
            "StatusChoices",
            "NOT_STARTED",
            "ENROLLED",
            "ACTIVE",
            "IN_PROGRESS",
            default="active",
        )

        enrollment = create_course_enrollment(
            data={
                "course": self.course,
                "learner": self.learner,
                "status": initial_status,
                "progress_percent": 0,
            }
        )

        self.assertEqual(enrollment.course_id, self.course.id)
        self.assertEqual(enrollment.learner_id, self.learner.id)

    def test_update_course_enrollment_updates_progress(self) -> None:
        """
        Сервис обновляет запись на курс.
        """

        enrollment = factory_create_course_enrollment(
            course=self.course,
            learner=self.learner,
        )

        updated_enrollment = update_course_enrollment(
            enrollment=enrollment,
            data={
                "progress_percent": 40,
            },
        )

        self.assertEqual(updated_enrollment.progress_percent, 40)

    def test_start_course_enrollment_sets_in_progress(self) -> None:
        """
        Сервис запускает прохождение курса.
        """

        enrollment = factory_create_course_enrollment(
            course=self.course,
            learner=self.learner,
        )

        started_enrollment = start_course_enrollment(enrollment=enrollment)

        self.assertEqual(
            started_enrollment.status,
            CourseEnrollment.StatusChoices.IN_PROGRESS,
        )
        self.assertIsNotNone(started_enrollment.started_at)
        self.assertIsNotNone(started_enrollment.last_activity_at)

    def test_complete_course_enrollment_sets_completed(self) -> None:
        """
        Сервис завершает прохождение курса.
        """

        enrollment = factory_create_course_enrollment(
            course=self.course,
            learner=self.learner,
        )

        completed_enrollment = complete_course_enrollment(
            enrollment=enrollment,
        )

        self.assertEqual(
            completed_enrollment.status,
            CourseEnrollment.StatusChoices.COMPLETED,
        )
        self.assertEqual(completed_enrollment.progress_percent, 100)
        self.assertIsNotNone(completed_enrollment.completed_at)

    def test_cancel_course_enrollment_sets_cancelled(self) -> None:
        """
        Сервис отменяет запись на курс.
        """

        enrollment = factory_create_course_enrollment(
            course=self.course,
            learner=self.learner,
        )

        cancelled_enrollment = cancel_course_enrollment(
            enrollment=enrollment,
        )

        self.assertEqual(
            cancelled_enrollment.status,
            CourseEnrollment.StatusChoices.CANCELLED,
        )

    def test_archive_course_enrollment_sets_archived(self) -> None:
        """
        Сервис архивирует запись на курс.
        """

        enrollment = factory_create_course_enrollment(
            course=self.course,
            learner=self.learner,
        )

        archived_enrollment = archive_course_enrollment(
            enrollment=enrollment,
        )

        self.assertEqual(
            archived_enrollment.status,
            CourseEnrollment.StatusChoices.ARCHIVED,
        )
