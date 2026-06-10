from __future__ import annotations

from apps.course.permissions.shared import (
    user_can_manage_course_related_object,
    user_can_manage_courses_in_scope,
    user_can_read_course_related_object,
    user_can_read_courses,
)
from rest_framework.permissions import SAFE_METHODS, BasePermission


class CoursePlanPermission(BasePermission):
    """
    Ограничения доступа к КТП курса.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет доступ к списку и созданию КТП.
        """

        if request.method in SAFE_METHODS:
            return user_can_read_courses(request.user)

        return user_can_manage_courses_in_scope(request.user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет доступ к конкретному КТП.
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


class CoursePlanStatusPermission(BasePermission):
    """
    Ограничения для проверки, утверждения и архивации КТП.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет базовое право изменения статуса КТП.
        """

        return user_can_manage_courses_in_scope(request.user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет право изменить статус конкретного КТП.
        """

        return user_can_manage_course_related_object(
            user=request.user,
            obj=obj,
        )


class CoursePlanImportPermission(BasePermission):
    """
    Ограничения доступа к импортам КТП.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет доступ к списку и созданию импортов.
        """

        if request.method in SAFE_METHODS:
            return user_can_read_courses(request.user)

        return user_can_manage_courses_in_scope(request.user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет доступ к конкретному импорту КТП.
        """

        if request.method in SAFE_METHODS:
            return user_can_read_course_related_object(
                user=request.user,
                obj=obj.course_plan,
            )

        return user_can_manage_course_related_object(
            user=request.user,
            obj=obj.course_plan,
        )


class CoursePlanImportStatusPermission(BasePermission):
    """
    Ограничения для изменения статуса импорта КТП.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет базовое право изменения статуса импорта.
        """

        return user_can_manage_courses_in_scope(request.user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет право изменить статус конкретного импорта.
        """

        return user_can_manage_course_related_object(
            user=request.user,
            obj=obj.course_plan,
        )
