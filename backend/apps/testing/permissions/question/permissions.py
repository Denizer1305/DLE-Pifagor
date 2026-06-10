from __future__ import annotations

from apps.testing.permissions.shared import (
    is_authenticated_user,
    is_teacher,
    is_testing_admin,
    user_can_manage_option_object,
    user_can_manage_question_object,
    user_can_read_test_object,
)
from rest_framework.permissions import SAFE_METHODS, BasePermission


class TestQuestionPermission(BasePermission):
    """
    Ограничение доступа к вопросам теста.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет доступ к списку и созданию вопросов.
        """

        user = request.user

        if not is_authenticated_user(user=user):
            return False

        if request.method in SAFE_METHODS:
            return True

        return is_testing_admin(user=user) or is_teacher(user=user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет доступ к конкретному вопросу.
        """

        user = request.user

        if request.method in SAFE_METHODS:
            return user_can_read_test_object(
                user=user,
                test=obj.test,
            )

        return user_can_manage_question_object(
            user=user,
            question=obj,
        )


class TestQuestionOptionPermission(BasePermission):
    """
    Ограничение доступа к вариантам ответа.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет доступ к списку и созданию вариантов ответа.
        """

        user = request.user

        if not is_authenticated_user(user=user):
            return False

        if request.method in SAFE_METHODS:
            return True

        return is_testing_admin(user=user) or is_teacher(user=user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет доступ к конкретному варианту ответа.
        """

        user = request.user

        if request.method in SAFE_METHODS:
            return user_can_read_test_object(
                user=user,
                test=obj.question.test,
            )

        return user_can_manage_option_object(
            user=user,
            option=obj,
        )


class QuestionOrderingPermission(BasePermission):
    """
    Ограничение для переупорядочивания вопросов и вариантов.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет доступ к action переупорядочивания.
        """

        user = request.user

        return is_testing_admin(user=user) or is_teacher(user=user)
