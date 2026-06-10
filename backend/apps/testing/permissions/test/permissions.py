from __future__ import annotations

from apps.testing.permissions.shared import (
    is_authenticated_user,
    is_teacher,
    is_testing_admin,
    user_can_manage_test_object,
    user_can_read_test_object,
)
from rest_framework.permissions import SAFE_METHODS, BasePermission


class TestPermission(BasePermission):
    """
    Ограничение доступа к тестам.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет доступ к списку и созданию тестов.
        """

        user = request.user

        if not is_authenticated_user(user=user):
            return False

        if request.method in SAFE_METHODS:
            return True

        return is_testing_admin(user=user) or is_teacher(user=user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет доступ к конкретному тесту.
        """

        user = request.user

        if request.method in SAFE_METHODS:
            return user_can_read_test_object(
                user=user,
                test=obj,
            )

        return user_can_manage_test_object(
            user=user,
            test=obj,
        )


class TestStatusPermission(BasePermission):
    """
    Ограничение для действий публикации, архивации и восстановления теста.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет общий доступ к status actions.
        """

        user = request.user

        return is_testing_admin(user=user) or is_teacher(user=user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет право менять статус конкретного теста.
        """

        return user_can_manage_test_object(
            user=request.user,
            test=obj,
        )
