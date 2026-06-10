from __future__ import annotations

from types import SimpleNamespace

from apps.course.permissions import (
    CourseEnrollmentPermission,
    CourseEnrollmentStatusPermission,
    CoursePermission,
    CourseProgressPermission,
    CourseProgressRecalculatePermission,
    CourseStatusPermission,
    LessonProgressPermission,
    LessonProgressStatusPermission,
)
from apps.course.permissions.shared import (
    user_can_manage_course_enrollment_object,
    user_can_manage_course_object,
    user_can_manage_course_progress_object,
    user_can_read_course_enrollment_object,
    user_can_read_course_object,
    user_can_read_course_progress_object,
    user_can_read_lesson_progress_object,
    user_can_track_lesson_progress_object,
)
from apps.course.tests.factories import (
    create_course,
    create_course_enrollment,
    create_course_progress,
    create_learner,
    create_lesson_progress,
    create_superadmin,
    create_teacher,
)
from django.test import TestCase


class CoursePermissionsTestCase(TestCase):
    """
    Тесты ограничений доступа модуля course.
    """

    def setUp(self) -> None:
        """
        Подготавливает пользователей и базовые сущности.
        """

        self.superadmin = create_superadmin(
            email="course-permissions-superadmin@example.com",
        )
        self.teacher = create_teacher(
            email="course-permissions-teacher@example.com",
        )
        self.other_teacher = create_teacher(
            email="course-permissions-other-teacher@example.com",
        )
        self.learner = create_learner(
            email="course-permissions-learner@example.com",
        )
        self.other_learner = create_learner(
            email="course-permissions-other-learner@example.com",
        )

        self.course = create_course(
            owner_teacher=self.teacher,
        )
        self.enrollment = create_course_enrollment(
            course=self.course,
            learner=self.learner,
        )
        self.course_progress = create_course_progress(
            enrollment=self.enrollment,
        )
        self.lesson_progress = create_lesson_progress(
            enrollment=self.enrollment,
            course_progress=self.course_progress,
        )

    def test_superadmin_can_read_and_manage_course(self) -> None:
        """
        Суперадмин может читать и управлять курсом.
        """

        self.assertTrue(
            user_can_read_course_object(
                user=self.superadmin,
                course=self.course,
            )
        )
        self.assertTrue(
            user_can_manage_course_object(
                user=self.superadmin,
                course=self.course,
            )
        )

    def test_owner_teacher_can_read_and_manage_own_course(self) -> None:
        """
        Владелец-преподаватель может читать и управлять своим курсом.
        """

        self.assertTrue(
            user_can_read_course_object(
                user=self.teacher,
                course=self.course,
            )
        )
        self.assertTrue(
            user_can_manage_course_object(
                user=self.teacher,
                course=self.course,
            )
        )

    def test_foreign_teacher_cannot_manage_course(self) -> None:
        """
        Чужой преподаватель не может управлять чужим курсом.
        """

        self.assertFalse(
            user_can_manage_course_object(
                user=self.other_teacher,
                course=self.course,
            )
        )

    def test_enrolled_learner_can_read_course(self) -> None:
        """
        Записанный обучающийся может читать курс.
        """

        self.assertTrue(
            user_can_read_course_object(
                user=self.learner,
                course=self.course,
            )
        )

    def test_not_enrolled_learner_cannot_read_course(self) -> None:
        """
        Незачисленный обучающийся не может читать курс.
        """

        self.assertFalse(
            user_can_read_course_object(
                user=self.other_learner,
                course=self.course,
            )
        )

    def test_learner_can_read_own_enrollment(self) -> None:
        """
        Обучающийся может читать собственную запись на курс.
        """

        self.assertTrue(
            user_can_read_course_enrollment_object(
                user=self.learner,
                enrollment=self.enrollment,
            )
        )

    def test_learner_cannot_manage_own_enrollment(self) -> None:
        """
        Обучающийся не управляет собственной записью на курс.
        """

        self.assertFalse(
            user_can_manage_course_enrollment_object(
                user=self.learner,
                enrollment=self.enrollment,
            )
        )

    def test_teacher_can_manage_course_enrollment(self) -> None:
        """
        Преподаватель-владелец курса может управлять записью на курс.
        """

        self.assertTrue(
            user_can_manage_course_enrollment_object(
                user=self.teacher,
                enrollment=self.enrollment,
            )
        )

    def test_learner_can_read_own_course_progress(self) -> None:
        """
        Обучающийся может читать собственный прогресс курса.
        """

        self.assertTrue(
            user_can_read_course_progress_object(
                user=self.learner,
                progress=self.course_progress,
            )
        )

    def test_learner_cannot_manage_own_course_progress(self) -> None:
        """
        Обучающийся не управляет собственным прогрессом курса напрямую.
        """

        self.assertFalse(
            user_can_manage_course_progress_object(
                user=self.learner,
                progress=self.course_progress,
            )
        )

    def test_learner_can_read_own_lesson_progress(self) -> None:
        """
        Обучающийся может читать собственный прогресс урока.
        """

        self.assertTrue(
            user_can_read_lesson_progress_object(
                user=self.learner,
                progress=self.lesson_progress,
            )
        )

    def test_learner_can_track_own_lesson_progress(self) -> None:
        """
        Обучающийся может фиксировать прогресс своего урока.
        """

        self.assertTrue(
            user_can_track_lesson_progress_object(
                user=self.learner,
                progress=self.lesson_progress,
            )
        )

    def test_other_learner_cannot_track_foreign_lesson_progress(self) -> None:
        """
        Другой обучающийся не может фиксировать чужой прогресс урока.
        """

        self.assertFalse(
            user_can_track_lesson_progress_object(
                user=self.other_learner,
                progress=self.lesson_progress,
            )
        )

    def test_course_permission_allows_authenticated_read(self) -> None:
        """
        CoursePermission разрешает авторизованное чтение.
        """

        permission = CoursePermission()
        request = self._build_request(
            method="GET",
            user=self.learner,
        )

        self.assertTrue(permission.has_permission(request, view=None))

    def test_course_permission_denies_anonymous_read(self) -> None:
        """
        CoursePermission запрещает чтение анонимному пользователю.
        """

        permission = CoursePermission()
        request = self._build_request(
            method="GET",
            user=AnonymousUserStub(),
        )

        self.assertFalse(permission.has_permission(request, view=None))

    def test_course_permission_allows_teacher_write(self) -> None:
        """
        CoursePermission разрешает запись преподавателю.
        """

        permission = CoursePermission()
        request = self._build_request(
            method="POST",
            user=self.teacher,
        )

        self.assertTrue(permission.has_permission(request, view=None))

    def test_course_permission_denies_learner_write(self) -> None:
        """
        CoursePermission запрещает создание курса обучающемуся.
        """

        permission = CoursePermission()
        request = self._build_request(
            method="POST",
            user=self.learner,
        )

        self.assertFalse(permission.has_permission(request, view=None))

    def test_course_permission_allows_owner_object_write(self) -> None:
        """
        CoursePermission разрешает владельцу изменять объект курса.
        """

        permission = CoursePermission()
        request = self._build_request(
            method="PATCH",
            user=self.teacher,
        )

        self.assertTrue(
            permission.has_object_permission(
                request,
                view=None,
                obj=self.course,
            )
        )

    def test_course_permission_denies_foreign_teacher_object_write(self) -> None:
        """
        CoursePermission запрещает чужому преподавателю изменять объект курса.
        """

        permission = CoursePermission()
        request = self._build_request(
            method="PATCH",
            user=self.other_teacher,
        )

        self.assertFalse(
            permission.has_object_permission(
                request,
                view=None,
                obj=self.course,
            )
        )

    def test_course_status_permission_allows_owner(self) -> None:
        """
        CourseStatusPermission разрешает владельцу менять статус курса.
        """

        permission = CourseStatusPermission()
        request = self._build_request(
            method="POST",
            user=self.teacher,
        )

        self.assertTrue(permission.has_permission(request, view=None))
        self.assertTrue(
            permission.has_object_permission(
                request,
                view=None,
                obj=self.course,
            )
        )

    def test_enrollment_permission_allows_learner_read_own_object(self) -> None:
        """
        CourseEnrollmentPermission разрешает обучающемуся читать свою запись.
        """

        permission = CourseEnrollmentPermission()
        request = self._build_request(
            method="GET",
            user=self.learner,
        )

        self.assertTrue(
            permission.has_object_permission(
                request,
                view=None,
                obj=self.enrollment,
            )
        )

    def test_enrollment_permission_denies_learner_write(self) -> None:
        """
        CourseEnrollmentPermission запрещает обучающемуся изменять запись.
        """

        permission = CourseEnrollmentPermission()
        request = self._build_request(
            method="PATCH",
            user=self.learner,
        )

        self.assertFalse(
            permission.has_object_permission(
                request,
                view=None,
                obj=self.enrollment,
            )
        )

    def test_enrollment_status_permission_allows_teacher(self) -> None:
        """
        CourseEnrollmentStatusPermission разрешает преподавателю менять статус записи.
        """

        permission = CourseEnrollmentStatusPermission()
        request = self._build_request(
            method="POST",
            user=self.teacher,
        )

        self.assertTrue(permission.has_permission(request, view=None))
        self.assertTrue(
            permission.has_object_permission(
                request,
                view=None,
                obj=self.enrollment,
            )
        )

    def test_course_progress_permission_allows_learner_read(self) -> None:
        """
        CourseProgressPermission разрешает обучающемуся читать свой прогресс.
        """

        permission = CourseProgressPermission()
        request = self._build_request(
            method="GET",
            user=self.learner,
        )

        self.assertTrue(
            permission.has_object_permission(
                request,
                view=None,
                obj=self.course_progress,
            )
        )

    def test_course_progress_recalculate_permission_allows_teacher(self) -> None:
        """
        CourseProgressRecalculatePermission разрешает преподавателю пересчёт прогресса.
        """

        permission = CourseProgressRecalculatePermission()
        request = self._build_request(
            method="POST",
            user=self.teacher,
        )

        self.assertTrue(permission.has_permission(request, view=None))
        self.assertTrue(
            permission.has_object_permission(
                request,
                view=None,
                obj=self.course_progress,
            )
        )

    def test_lesson_progress_permission_allows_learner_read(self) -> None:
        """
        LessonProgressPermission разрешает обучающемуся читать свой прогресс урока.
        """

        permission = LessonProgressPermission()
        request = self._build_request(
            method="GET",
            user=self.learner,
        )

        self.assertTrue(
            permission.has_object_permission(
                request,
                view=None,
                obj=self.lesson_progress,
            )
        )

    def test_lesson_progress_status_permission_allows_learner_track(self) -> None:
        """
        LessonProgressStatusPermission разрешает обучающемуся фиксировать свой прогресс.
        """

        permission = LessonProgressStatusPermission()
        request = self._build_request(
            method="POST",
            user=self.learner,
        )

        self.assertTrue(permission.has_permission(request, view=None))
        self.assertTrue(
            permission.has_object_permission(
                request,
                view=None,
                obj=self.lesson_progress,
            )
        )

    def test_lesson_progress_status_permission_denies_foreign_learner(self) -> None:
        """
        LessonProgressStatusPermission запрещает менять чужой прогресс урока.
        """

        permission = LessonProgressStatusPermission()
        request = self._build_request(
            method="POST",
            user=self.other_learner,
        )

        self.assertTrue(permission.has_permission(request, view=None))
        self.assertFalse(
            permission.has_object_permission(
                request,
                view=None,
                obj=self.lesson_progress,
            )
        )

    def _build_request(
        self,
        *,
        method: str,
        user,
    ):
        """
        Создаёт минимальный request-объект для permission-классов.
        """

        return SimpleNamespace(
            method=method,
            user=user,
        )


class AnonymousUserStub:
    """
    Минимальная заглушка анонимного пользователя.
    """

    is_authenticated = False
    is_staff = False
    is_superuser = False
