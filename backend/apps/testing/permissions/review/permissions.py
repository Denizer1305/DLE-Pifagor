from __future__ import annotations

from apps.testing.permissions.shared import (
    is_authenticated_user,
    is_teacher,
    is_testing_admin,
)
from rest_framework.permissions import BasePermission


class TestReviewQueuePermission(BasePermission):
    """
    Ограничение доступа к очереди проверки тестов.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет доступ к review endpoints.
        """

        user = request.user

        if not is_authenticated_user(user=user):
            return False

        return is_testing_admin(user=user) or is_teacher(user=user)


class TestReviewActionPermission(BasePermission):
    """
    Ограничение для действий проверки и пересчёта попытки.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет общий доступ к действиям проверки.
        """

        user = request.user

        if not is_authenticated_user(user=user):
            return False

        return is_testing_admin(user=user) or is_teacher(user=user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет доступ к конкретной попытке.
        """

        if is_testing_admin(user=request.user):
            return True

        if not is_teacher(user=request.user):
            return False

        return obj.test.owner_teacher_id == request.user.id
