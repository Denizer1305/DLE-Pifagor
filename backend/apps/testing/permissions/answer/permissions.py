from __future__ import annotations

from apps.testing.permissions.shared import (
    is_authenticated_user,
    is_learner,
    is_teacher,
    is_testing_admin,
    user_can_manage_attempt_object,
    user_can_read_attempt_object,
    user_can_track_attempt_object,
)
from rest_framework.permissions import SAFE_METHODS, BasePermission


class TestAttemptAnswerPermission(BasePermission):
    """
    Ограничение доступа к ответам на вопросы теста.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет доступ к списку и созданию ответов.
        """

        user = request.user

        if not is_authenticated_user(user=user):
            return False

        if request.method in SAFE_METHODS:
            return True

        return (
            is_testing_admin(user=user)
            or is_teacher(user=user)
            or is_learner(user=user)
        )

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет доступ к конкретному ответу.
        """

        user = request.user

        if request.method in SAFE_METHODS:
            return user_can_read_attempt_object(
                user=user,
                attempt=obj.attempt,
            )

        if is_learner(user=user):
            return user_can_track_attempt_object(
                user=user,
                attempt=obj.attempt,
            )

        return user_can_manage_attempt_object(
            user=user,
            attempt=obj.attempt,
        )


class TestAttemptAnswerReviewPermission(BasePermission):
    """
    Ограничение для ручной проверки ответа.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет общий доступ к проверке ответа.
        """

        user = request.user

        return is_testing_admin(user=user) or is_teacher(user=user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет право проверять конкретный ответ.
        """

        return user_can_manage_attempt_object(
            user=request.user,
            attempt=obj.attempt,
        )
