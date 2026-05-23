from __future__ import annotations

from apps.users.permissions.helpers import (
    can_review_learner,
    get_object_context,
    is_authenticated_active_user,
    is_self,
    is_superadmin,
)
from apps.users.selectors.guardian_selectors import guardian_has_access_to_learner
from rest_framework.permissions import BasePermission


class CanReviewLearnerProfile(BasePermission):
    """
    Разрешает проверку профиля учащегося.
    """

    message = "У вас нет прав на проверку профиля учащегося."

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
        Проверяет право проверки конкретного профиля учащегося.

        Args:
            request:
                DRF request.
            view:
                DRF view.
            obj:
                LearnerProfile.

        Returns:
            bool: True, если пользователь может проверить учащегося.
        """

        context = get_object_context(obj)

        return can_review_learner(
            request.user,
            organization=context["organization"],
            department=context["department"],
            group=context["group"],
        )


class CanGuardianViewLearnerProfile(BasePermission):
    """
    Разрешает родителю смотреть профиль связанного учащегося.
    """

    message = "У вас нет доступа к профилю этого учащегося."

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
        Проверяет доступ родителя к профилю учащегося.

        Args:
            request:
                DRF request.
            view:
                DRF view.
            obj:
                LearnerProfile.

        Returns:
            bool: True, если доступ разрешён.
        """

        if is_self(request.user, obj.user):
            return True

        if is_superadmin(request.user):
            return True

        return guardian_has_access_to_learner(request.user, obj.user)
