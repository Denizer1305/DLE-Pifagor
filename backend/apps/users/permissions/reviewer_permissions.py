from __future__ import annotations

from apps.users.permissions.helpers import (
    can_review_guardian_link,
    can_review_learner,
    can_review_teacher,
    get_object_context,
    is_authenticated_active_user,
    is_organization_reviewer,
)
from rest_framework.permissions import BasePermission


class IsOrganizationReviewerRole(BasePermission):
    """
    Разрешает доступ пользователям, которые могут рассматривать заявки.
    """

    message = "Доступ разрешён только пользователю, который может рассматривать заявки."

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
        Проверяет право проверки объекта в организационном контексте.

        Args:
            request:
                DRF request.
            view:
                DRF view.
            obj:
                Объект проверки.

        Returns:
            bool: True, если пользователь может проверять объект.
        """

        context = get_object_context(obj)

        return is_organization_reviewer(
            request.user,
            organization=context["organization"],
            department=context["department"],
            group=context["group"],
        )


class CanReviewTeacherObject(BasePermission):
    """
    Разрешает проверку объекта, связанного с преподавателем.
    """

    message = "У вас нет прав на проверку преподавателя."

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
        Проверяет право проверки преподавателя.

        Args:
            request:
                DRF request.
            view:
                DRF view.
            obj:
                Объект с organization/department.

        Returns:
            bool: True, если проверка разрешена.
        """

        context = get_object_context(obj)

        return can_review_teacher(
            request.user,
            organization=context["organization"],
            department=context["department"],
        )


class CanReviewLearnerObject(BasePermission):
    """
    Разрешает проверку объекта, связанного с учащимся.
    """

    message = "У вас нет прав на проверку учащегося."

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
        Проверяет право проверки учащегося.

        Args:
            request:
                DRF request.
            view:
                DRF view.
            obj:
                Объект с organization/department/group.

        Returns:
            bool: True, если проверка разрешена.
        """

        context = get_object_context(obj)

        return can_review_learner(
            request.user,
            organization=context["organization"],
            department=context["department"],
            group=context["group"],
        )


class CanReviewGuardianLinkObject(BasePermission):
    """
    Разрешает проверку объекта связи родителя и учащегося.
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
        Проверяет право проверки связи.

        Args:
            request:
                DRF request.
            view:
                DRF view.
            obj:
                Объект связи или заявка.

        Returns:
            bool: True, если проверка разрешена.
        """

        context = get_object_context(obj)

        return can_review_guardian_link(
            request.user,
            organization=context["organization"],
            department=context["department"],
            group=context["group"],
        )
