from __future__ import annotations

from apps.users.permissions.helpers import (
    can_review_guardian_link,
    is_authenticated_active_user,
    is_superadmin,
)
from apps.users.selectors.guardian_selectors import guardian_has_access_to_learner
from rest_framework.permissions import BasePermission


class CanReviewGuardianLink(BasePermission):
    """
    Разрешает проверку связи родителя и учащегося.
    """

    message = "У вас нет прав на проверку связи родителя и учащегося."

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
        Проверяет право проверки связи родителя и учащегося.

        Args:
            request:
                DRF request.
            view:
                DRF view.
            obj:
                GuardianLearner.

        Returns:
            bool: True, если пользователь может проверить связь.
        """

        learner_profile = getattr(obj.learner, "learner_profile", None)

        if learner_profile is None:
            return is_superadmin(request.user)

        return can_review_guardian_link(
            request.user,
            organization=learner_profile.organization,
            department=learner_profile.department,
            group=learner_profile.group,
        )


class CanGuardianAccessLearner(BasePermission):
    """
    Разрешает родителю доступ к данным связанного учащегося.
    """

    message = "У вас нет доступа к данным этого учащегося."

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
        Проверяет доступ родителя к учащемуся.

        Args:
            request:
                DRF request.
            view:
                DRF view.
            obj:
                Объект учащегося или профиль учащегося.

        Returns:
            bool: True, если родитель имеет активную связь с учащимся.
        """

        learner = getattr(obj, "user", obj)

        if is_superadmin(request.user):
            return True

        return guardian_has_access_to_learner(request.user, learner)
