from __future__ import annotations

from apps.course.permissions.shared import (
    user_can_manage_course_progress_object,
    user_can_manage_courses_in_scope,
    user_can_manage_lesson_progress_object,
    user_can_read_course_progress_object,
    user_can_read_courses,
    user_can_read_lesson_progress_object,
    user_can_track_course_progress_object,
    user_can_track_lesson_progress_object,
)
from rest_framework.permissions import SAFE_METHODS, BasePermission


class CourseProgressPermission(BasePermission):
    """
    Ограничения доступа к общему прогрессу курса.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет доступ к списку и созданию прогресса курса.
        """

        if request.method in SAFE_METHODS:
            return user_can_read_courses(request.user)

        return user_can_manage_courses_in_scope(request.user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет доступ к конкретному прогрессу курса.
        """

        if request.method in SAFE_METHODS:
            return user_can_read_course_progress_object(
                user=request.user,
                progress=obj,
            )

        return user_can_manage_course_progress_object(
            user=request.user,
            progress=obj,
        )


class CourseProgressRecalculatePermission(BasePermission):
    """
    Ограничения для пересчёта прогресса курса.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет базовое право пересчёта прогресса.
        """

        return user_can_manage_courses_in_scope(request.user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет право пересчитать конкретный прогресс курса.
        """

        return user_can_manage_course_progress_object(
            user=request.user,
            progress=obj,
        )


class CourseProgressTrackPermission(BasePermission):
    """
    Ограничения для фиксации активности по курсу.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет наличие авторизации.
        """

        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет право фиксировать активность по прогрессу курса.
        """

        return user_can_track_course_progress_object(
            user=request.user,
            progress=obj,
        )


class LessonProgressPermission(BasePermission):
    """
    Ограничения доступа к прогрессу уроков.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет доступ к списку и созданию прогресса урока.
        """

        if request.method in SAFE_METHODS:
            return user_can_read_courses(request.user)

        return user_can_manage_courses_in_scope(request.user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет доступ к конкретному прогрессу урока.
        """

        if request.method in SAFE_METHODS:
            return user_can_read_lesson_progress_object(
                user=request.user,
                progress=obj,
            )

        return user_can_manage_lesson_progress_object(
            user=request.user,
            progress=obj,
        )


class LessonProgressStatusPermission(BasePermission):
    """
    Ограничения для старта, завершения и сброса прогресса урока.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет базовое право изменения прогресса урока.
        """

        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет право изменить конкретный прогресс урока.
        """

        return user_can_track_lesson_progress_object(
            user=request.user,
            progress=obj,
        )
