from __future__ import annotations

from apps.testing.permissions.shared.role_checks import (
    is_guardian,
    is_learner,
    is_teacher,
    is_testing_admin,
)


def user_can_manage_test_object(*, user, test) -> bool:
    """
    Проверяет право управлять тестом.
    """

    if is_testing_admin(user=user):
        return True

    return bool(is_teacher(user=user) and test.owner_teacher_id == user.id)


def user_can_read_test_object(*, user, test) -> bool:
    """
    Проверяет право читать тест.
    """

    if user_can_manage_test_object(user=user, test=test):
        return True

    if not is_learner(user=user):
        return False

    return _learner_has_course_access(
        learner=user,
        course_id=test.course_id,
    )


def user_can_manage_question_object(*, user, question) -> bool:
    """
    Проверяет право управлять вопросом.
    """

    return user_can_manage_test_object(
        user=user,
        test=question.test,
    )


def user_can_manage_option_object(*, user, option) -> bool:
    """
    Проверяет право управлять вариантом ответа.
    """

    return user_can_manage_question_object(
        user=user,
        question=option.question,
    )


def user_can_read_attempt_object(*, user, attempt) -> bool:
    """
    Проверяет право читать попытку.
    """

    if user_can_manage_test_object(
        user=user,
        test=attempt.test,
    ):
        return True

    if is_learner(user=user):
        return attempt.learner_id == user.id

    if is_guardian(user=user):
        return attempt.is_visible_to_guardian

    return False


def user_can_manage_attempt_object(*, user, attempt) -> bool:
    """
    Проверяет право управлять попыткой.
    """

    return user_can_manage_test_object(
        user=user,
        test=attempt.test,
    )


def user_can_track_attempt_object(*, user, attempt) -> bool:
    """
    Проверяет право обучающегося проходить попытку.
    """

    return bool(is_learner(user=user) and attempt.learner_id == user.id)


def user_can_read_result_object(*, user, result) -> bool:
    """
    Проверяет право читать итоговый результат.
    """

    if user_can_manage_test_object(
        user=user,
        test=result.test,
    ):
        return True

    if is_learner(user=user):
        return result.learner_id == user.id and result.is_visible_to_learner

    if is_guardian(user=user):
        return result.is_visible_to_guardian

    return False


def _learner_has_course_access(
    *,
    learner,
    course_id: int,
) -> bool:
    """
    Проверяет, что обучающийся записан на курс.
    """

    try:
        from apps.course.models import CourseEnrollment
    except ImportError:
        return False

    return CourseEnrollment.objects.filter(
        course_id=course_id,
        learner_id=learner.id,
    ).exists()
