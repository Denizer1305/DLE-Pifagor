from __future__ import annotations

from apps.testing.permissions.shared import (
    is_authenticated_user,
    is_teacher,
    is_testing_admin,
)
from rest_framework.permissions import BasePermission


class TestAttemptIntegrityReportPermission(BasePermission):
    """
    Ограничение доступа к отчётам добросовестности попыток.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет доступ к списку отчётов.
        """

        user = request.user

        if not is_authenticated_user(user=user):
            return False

        return is_testing_admin(user=user) or is_teacher(user=user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет доступ к конкретному отчёту.
        """

        return _user_can_read_integrity_report(
            user=request.user,
            report=obj,
        )


def _user_can_read_integrity_report(*, user, report) -> bool:
    """
    Проверяет, может ли пользователь читать отчёт добросовестности.
    """

    if is_testing_admin(user=user):
        return True

    if not is_teacher(user=user):
        return False

    return report.attempt.test.owner_teacher_id == user.id
