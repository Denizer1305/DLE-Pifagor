from __future__ import annotations

from apps.course.permissions.shared.object_checks import (
    user_can_manage_course_related_object,
    user_can_read_course_related_object,
)
from apps.course.permissions.shared.role_checks import (
    user_can_manage_courses_globally,
    user_can_manage_courses_in_scope,
    user_can_read_courses,
)
from rest_framework.permissions import SAFE_METHODS, BasePermission


class CourseReadOnlyOrScopedWritePermission(BasePermission):
    """
    Базовое ограничение: читать могут авторизованные пользователи,
    изменять — пользователи с правом управления курсами.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет доступ на уровне запроса.
        """

        if request.method in SAFE_METHODS:
            return user_can_read_courses(request.user)

        return user_can_manage_courses_in_scope(request.user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет доступ на уровне объекта.
        """

        if request.method in SAFE_METHODS:
            return user_can_read_course_related_object(
                user=request.user,
                obj=obj,
            )

        return user_can_manage_course_related_object(
            user=request.user,
            obj=obj,
        )


class CourseGlobalAdminOnlyPermission(BasePermission):
    """
    Ограничение только для глобальных администраторов.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет глобальное административное право.
        """

        return user_can_manage_courses_globally(request.user)


class CourseAuthenticatedReadPermission(BasePermission):
    """
    Ограничение только на авторизованное чтение.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет авторизацию пользователя.
        """

        return user_can_read_courses(request.user)
