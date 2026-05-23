from __future__ import annotations

from apps.users.permissions.helpers import (
    can_review_teacher,
    get_object_context,
    is_authenticated_active_user,
)
from rest_framework.permissions import BasePermission


class CanReviewTeacherProfile(BasePermission):
    """
    Разрешает проверку профиля преподавателя.
    """

    message = "У вас нет прав на проверку профиля преподавателя."

    def has_permission(self, request, view) -> bool:
        """
        Проверяет общий доступ.

        Args:
            request:
                DRF request.
            view:
                DRF view.

        Returns:
            bool: True, если пользователь активен.
        """

        return is_authenticated_active_user(request.user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет право проверки конкретного профиля преподавателя.

        Args:
            request:
                DRF request.
            view:
                DRF view.
            obj:
                TeacherProfile.

        Returns:
            bool: True, если пользователь может проверить преподавателя.
        """

        context = get_object_context(obj)

        return can_review_teacher(
            request.user,
            organization=context["organization"],
            department=context["department"],
        )
