from __future__ import annotations

from apps.course.permissions.shared import (
    user_can_manage_course_related_object,
    user_can_manage_courses_in_scope,
    user_can_read_course_related_object,
    user_can_read_courses,
)
from rest_framework.permissions import SAFE_METHODS, BasePermission


class CourseSectionPermission(BasePermission):
    """
    Ограничения доступа к разделам курса.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет доступ к списку и созданию разделов.
        """

        if request.method in SAFE_METHODS:
            return user_can_read_courses(request.user)

        return user_can_manage_courses_in_scope(request.user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет доступ к конкретному разделу.
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


class CourseSectionStatusPermission(BasePermission):
    """
    Ограничения для публикации и архивации раздела.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет базовое право изменения статуса раздела.
        """

        return user_can_manage_courses_in_scope(request.user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет право изменить статус конкретного раздела.
        """

        return user_can_manage_course_related_object(
            user=request.user,
            obj=obj,
        )


class CourseLessonPermission(BasePermission):
    """
    Ограничения доступа к урокам курса.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет доступ к списку и созданию уроков.
        """

        if request.method in SAFE_METHODS:
            return user_can_read_courses(request.user)

        return user_can_manage_courses_in_scope(request.user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет доступ к конкретному уроку.
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


class CourseLessonStatusPermission(BasePermission):
    """
    Ограничения для публикации и архивации урока.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет базовое право изменения статуса урока.
        """

        return user_can_manage_courses_in_scope(request.user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет право изменить статус конкретного урока.
        """

        return user_can_manage_course_related_object(
            user=request.user,
            obj=obj,
        )


class CourseLessonBlockPermission(BasePermission):
    """
    Ограничения доступа к блокам урока.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет доступ к списку и созданию блоков.
        """

        if request.method in SAFE_METHODS:
            return user_can_read_courses(request.user)

        return user_can_manage_courses_in_scope(request.user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет доступ к конкретному блоку урока.
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


class CourseLessonBlockVisibilityPermission(BasePermission):
    """
    Ограничения для показа и скрытия блока урока.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет базовое право изменения видимости блока.
        """

        return user_can_manage_courses_in_scope(request.user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет право изменить видимость блока.
        """

        return user_can_manage_course_related_object(
            user=request.user,
            obj=obj,
        )


class CourseMaterialLinkPermission(BasePermission):
    """
    Ограничения доступа к материалам курса.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет доступ к списку и созданию связей с материалами.
        """

        if request.method in SAFE_METHODS:
            return user_can_read_courses(request.user)

        return user_can_manage_courses_in_scope(request.user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет доступ к конкретной связи курса с материалом.
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


class CourseMaterialLinkVisibilityPermission(BasePermission):
    """
    Ограничения для показа и скрытия материала курса.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет базовое право изменения видимости материала курса.
        """

        return user_can_manage_courses_in_scope(request.user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет право изменить видимость материала курса.
        """

        return user_can_manage_course_related_object(
            user=request.user,
            obj=obj,
        )
