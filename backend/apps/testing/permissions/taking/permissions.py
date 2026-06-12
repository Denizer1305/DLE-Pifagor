from __future__ import annotations

from apps.testing.permissions.shared import is_authenticated_user, is_learner
from rest_framework.permissions import BasePermission


class TestTakingPermission(BasePermission):
    """
    Ограничение доступа к прохождению теста обучающимся.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет общий доступ к taking endpoints.
        """

        user = request.user

        if not is_authenticated_user(user=user):
            return False

        return is_learner(user=user)


class TestTakingAttemptPermission(BasePermission):
    """
    Ограничение доступа к попытке в режиме прохождения.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет общий доступ к действиям с попыткой.
        """

        user = request.user

        if not is_authenticated_user(user=user):
            return False

        return is_learner(user=user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет, что попытка принадлежит текущему обучающемуся.
        """

        return obj.learner_id == request.user.id
