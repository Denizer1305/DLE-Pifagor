from __future__ import annotations

from apps.course.selectors import (
    user_can_edit_courses,
    user_is_authenticated,
    user_is_course_learner,
    user_is_course_teacher,
    user_is_global_course_admin,
    user_is_organization_course_admin,
)


def user_can_read_courses(user) -> bool:
    """
    Проверяет базовое право чтения курсов.
    """

    return user_is_authenticated(user)


def user_can_manage_courses_globally(user) -> bool:
    """
    Проверяет право глобального управления курсами.
    """

    return user_is_global_course_admin(user)


def user_can_manage_courses_in_scope(user) -> bool:
    """
    Проверяет право управления курсами в доступной области.
    """

    if not user_is_authenticated(user):
        return False

    return bool(
        user_can_edit_courses(user)
        or user_is_course_teacher(user)
        or user_is_organization_course_admin(user)
    )


def user_can_track_own_course_progress(user) -> bool:
    """
    Проверяет право фиксировать собственный прогресс по курсу.
    """

    return bool(user_is_authenticated(user) and user_is_course_learner(user))
