from __future__ import annotations

from apps.testing.permissions.shared import (
    is_authenticated_user,
    is_teacher,
    is_testing_admin,
    user_can_manage_test_object,
    user_can_read_result_object,
)
from rest_framework.permissions import SAFE_METHODS, BasePermission


class TestLearnerResultPermission(BasePermission):
    """
    Ограничение доступа к итоговым результатам тестов.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет доступ к списку результатов.
        """

        return is_authenticated_user(user=request.user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет доступ к конкретному итоговому результату.
        """

        if request.method in SAFE_METHODS:
            return user_can_read_result_object(
                user=request.user,
                result=obj,
            )

        return user_can_manage_test_object(
            user=request.user,
            test=obj.test,
        )


class TestResultPublicationPermission(BasePermission):
    """
    Ограничение для публикации и скрытия результата.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет общий доступ к публикации результата.
        """

        user = request.user

        return is_testing_admin(user=user) or is_teacher(user=user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет право публиковать результат конкретной попытки/результата.
        """

        test = getattr(obj, "test", None)

        if test is None and hasattr(obj, "attempt"):
            test = obj.attempt.test

        if test is None:
            return False

        return user_can_manage_test_object(
            user=request.user,
            test=test,
        )
