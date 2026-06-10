from __future__ import annotations

from apps.course.permissions.shared import (
    user_can_manage_course_object,
    user_can_manage_courses_in_scope,
    user_can_read_course_object,
    user_can_read_courses,
)
from rest_framework.permissions import SAFE_METHODS, BasePermission


class CoursePermission(BasePermission):
    """
    Ограничения доступа к курсам.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет доступ к списку и созданию курсов.
        """

        if request.method in SAFE_METHODS:
            return user_can_read_courses(request.user)

        return user_can_manage_courses_in_scope(request.user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет доступ к конкретному курсу.
        """

        if request.method in SAFE_METHODS:
            return user_can_read_course_object(
                user=request.user,
                course=obj,
            )

        return user_can_manage_course_object(
            user=request.user,
            course=obj,
        )


class CourseStatusPermission(BasePermission):
    """
    Ограничения для публикации, архивации и восстановления курса.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет базовое право изменения статуса курса.
        """

        return user_can_manage_courses_in_scope(request.user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет право изменить статус конкретного курса.
        """

        return user_can_manage_course_object(
            user=request.user,
            course=obj,
        )


class CourseDuplicatePermission(BasePermission):
    """
    Ограничения для копирования курса.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет базовое право копирования курса.
        """

        return user_can_manage_courses_in_scope(request.user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет право копировать конкретный курс.
        """

        return user_can_manage_course_object(
            user=request.user,
            course=obj,
        )


class CourseCreateWithPlanPermission(BasePermission):
    """
    Ограничение для создания курса вместе с КТП.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет право создания курса с КТП.
        """

        return user_can_manage_courses_in_scope(request.user)
