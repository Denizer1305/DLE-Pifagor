from __future__ import annotations

from apps.course.models import Course, CourseEnrollment, CourseProgress, LessonProgress
from apps.course.selectors import (
    user_can_manage_course,
    user_can_read_course,
    user_is_global_course_admin,
)


def user_can_read_course_object(
    *,
    user,
    course: Course,
) -> bool:
    """
    Проверяет право чтения конкретного курса.
    """

    return user_can_read_course(
        user=user,
        course=course,
    )


def user_can_manage_course_object(
    *,
    user,
    course: Course,
) -> bool:
    """
    Проверяет право управления конкретным курсом.
    """

    return user_can_manage_course(
        user=user,
        course=course,
    )


def user_can_read_course_related_object(
    *,
    user,
    obj,
) -> bool:
    """
    Проверяет право чтения объекта, связанного с курсом.
    """

    course = get_course_from_related_object(obj)

    if course is None:
        return False

    return user_can_read_course_object(
        user=user,
        course=course,
    )


def user_can_manage_course_related_object(
    *,
    user,
    obj,
) -> bool:
    """
    Проверяет право управления объектом, связанным с курсом.
    """

    course = get_course_from_related_object(obj)

    if course is None:
        return False

    return user_can_manage_course_object(
        user=user,
        course=course,
    )


def user_can_read_course_enrollment_object(
    *,
    user,
    enrollment: CourseEnrollment,
) -> bool:
    """
    Проверяет право чтения записи на курс.
    """

    if not user or not user.is_authenticated:
        return False

    if user_is_global_course_admin(user):
        return True

    if enrollment.learner_id == getattr(user, "id", None):
        return True

    return user_can_manage_course_object(
        user=user,
        course=enrollment.course,
    )


def user_can_manage_course_enrollment_object(
    *,
    user,
    enrollment: CourseEnrollment,
) -> bool:
    """
    Проверяет право управления записью на курс.
    """

    return user_can_manage_course_object(
        user=user,
        course=enrollment.course,
    )


def user_can_track_course_enrollment_object(
    *,
    user,
    enrollment: CourseEnrollment,
) -> bool:
    """
    Проверяет право фиксировать прогресс по записи на курс.
    """

    if not user or not user.is_authenticated:
        return False

    if enrollment.learner_id == getattr(user, "id", None):
        return True

    return user_can_manage_course_enrollment_object(
        user=user,
        enrollment=enrollment,
    )


def user_can_read_course_progress_object(
    *,
    user,
    progress: CourseProgress,
) -> bool:
    """
    Проверяет право чтения общего прогресса курса.
    """

    return user_can_read_course_enrollment_object(
        user=user,
        enrollment=progress.enrollment,
    )


def user_can_manage_course_progress_object(
    *,
    user,
    progress: CourseProgress,
) -> bool:
    """
    Проверяет право управления общим прогрессом курса.
    """

    return user_can_manage_course_enrollment_object(
        user=user,
        enrollment=progress.enrollment,
    )


def user_can_track_course_progress_object(
    *,
    user,
    progress: CourseProgress,
) -> bool:
    """
    Проверяет право фиксировать активность по прогрессу курса.
    """

    return user_can_track_course_enrollment_object(
        user=user,
        enrollment=progress.enrollment,
    )


def user_can_read_lesson_progress_object(
    *,
    user,
    progress: LessonProgress,
) -> bool:
    """
    Проверяет право чтения прогресса урока.
    """

    return user_can_read_course_enrollment_object(
        user=user,
        enrollment=progress.enrollment,
    )


def user_can_manage_lesson_progress_object(
    *,
    user,
    progress: LessonProgress,
) -> bool:
    """
    Проверяет право управления прогрессом урока.
    """

    return user_can_manage_course_enrollment_object(
        user=user,
        enrollment=progress.enrollment,
    )


def user_can_track_lesson_progress_object(
    *,
    user,
    progress: LessonProgress,
) -> bool:
    """
    Проверяет право фиксировать прогресс урока.
    """

    return user_can_track_course_enrollment_object(
        user=user,
        enrollment=progress.enrollment,
    )


def get_course_from_related_object(obj) -> Course | None:
    """
    Возвращает курс из связанного объекта.
    """

    if isinstance(obj, Course):
        return obj

    course = getattr(obj, "course", None)

    if course is not None:
        return course

    section = getattr(obj, "section", None)

    if section is not None:
        return getattr(section, "course", None)

    lesson = getattr(obj, "lesson", None)

    if lesson is not None:
        return getattr(lesson, "course", None)

    enrollment = getattr(obj, "enrollment", None)

    if enrollment is not None:
        return getattr(enrollment, "course", None)

    course_progress = getattr(obj, "course_progress", None)

    if course_progress is not None:
        enrollment = getattr(course_progress, "enrollment", None)

        if enrollment is not None:
            return getattr(enrollment, "course", None)

    return None
