from __future__ import annotations

from apps.course.permissions.shared import (
    user_can_manage_course_enrollment_object,
    user_can_manage_course_related_object,
    user_can_manage_courses_in_scope,
    user_can_read_course_enrollment_object,
    user_can_read_course_related_object,
    user_can_read_courses,
)
from rest_framework.permissions import SAFE_METHODS, BasePermission


class CourseGroupAccessPermission(BasePermission):
    """
    Ограничения доступа к групповым доступам курса.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет доступ к списку и созданию групповых доступов.
        """

        if request.method in SAFE_METHODS:
            return user_can_read_courses(request.user)

        return user_can_manage_courses_in_scope(request.user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет доступ к конкретному групповому доступу.
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


class CourseGroupAccessVisibilityPermission(BasePermission):
    """
    Ограничения для изменения видимости курса для группы.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет базовое право изменения видимости.
        """

        return user_can_manage_courses_in_scope(request.user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет право изменить видимость конкретного доступа.
        """

        return user_can_manage_course_related_object(
            user=request.user,
            obj=obj,
        )


class CourseAccessRulePermission(BasePermission):
    """
    Ограничения доступа к правилам доступа курса.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет доступ к списку и созданию правил доступа.
        """

        if request.method in SAFE_METHODS:
            return user_can_read_courses(request.user)

        return user_can_manage_courses_in_scope(request.user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет доступ к конкретному правилу доступа.
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


class CourseAccessRuleStatusPermission(BasePermission):
    """
    Ограничения для включения и выключения правила доступа.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет базовое право изменения правила доступа.
        """

        return user_can_manage_courses_in_scope(request.user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет право изменить конкретное правило доступа.
        """

        return user_can_manage_course_related_object(
            user=request.user,
            obj=obj,
        )


class CourseEnrollmentPermission(BasePermission):
    """
    Ограничения доступа к записям на курс.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет доступ к списку и созданию записей на курс.
        """

        if request.method in SAFE_METHODS:
            return user_can_read_courses(request.user)

        return user_can_manage_courses_in_scope(request.user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет доступ к конкретной записи на курс.
        """

        if request.method in SAFE_METHODS:
            return user_can_read_course_enrollment_object(
                user=request.user,
                enrollment=obj,
            )

        return user_can_manage_course_enrollment_object(
            user=request.user,
            enrollment=obj,
        )


class CourseEnrollmentStatusPermission(BasePermission):
    """
    Ограничения для старта, завершения, отмены и архивации записи.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет базовое право смены статуса записи.
        """

        return user_can_manage_courses_in_scope(request.user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет право изменить статус конкретной записи.
        """

        return user_can_manage_course_enrollment_object(
            user=request.user,
            enrollment=obj,
        )
