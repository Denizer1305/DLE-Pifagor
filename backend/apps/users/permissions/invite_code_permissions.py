from __future__ import annotations

from apps.users.constants.onboarding import InviteCodePurpose
from apps.users.permissions.helpers import (
    can_review_guardian_link,
    can_review_teacher,
    get_object_context,
    is_authenticated_active_user,
    is_organization_admin,
    is_superadmin,
)
from rest_framework.permissions import BasePermission


class CanViewInviteCodes(BasePermission):
    """
    Разрешает просмотр кодов приглашения.

    Доступ имеют:
        - суперадминистратор;
        - администратор организации;
        - пользователь, создавший код.
    """

    message = "У вас нет прав на просмотр кодов приглашения."

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
        Проверяет право просмотра конкретного кода.

        Args:
            request:
                DRF request.
            view:
                DRF view.
            obj:
                InviteCode.

        Returns:
            bool: True, если доступ разрешён.
        """

        if obj.created_by_id == request.user.id:
            return True

        if is_superadmin(request.user):
            return True

        context = get_object_context(obj)

        return is_organization_admin(
            request.user,
            organization=context["organization"],
            department=context["department"],
        )


class CanCreateTeacherInviteCode(BasePermission):
    """
    Разрешает создание кода регистрации преподавателя.
    """

    message = "У вас нет прав на создание кода регистрации преподавателя."

    def has_permission(self, request, view) -> bool:
        """
        Проверяет право создания кода преподавателя.

        Args:
            request:
                DRF request.
            view:
                DRF view.

        Returns:
            bool: True, если пользователь потенциально может создавать такие коды.
        """

        return is_superadmin(request.user) or can_review_teacher(request.user)


class CanCreateGuardianLinkCode(BasePermission):
    """
    Разрешает создание кода связи родителя и учащегося.
    """

    message = "У вас нет прав на создание кода связи родителя и учащегося."

    def has_permission(self, request, view) -> bool:
        """
        Проверяет право создания кода связи родителя и учащегося.

        Args:
            request:
                DRF request.
            view:
                DRF view.

        Returns:
            bool: True, если пользователь потенциально может создавать такие коды.
        """

        return is_superadmin(request.user) or can_review_guardian_link(request.user)


class CanDisableInviteCode(BasePermission):
    """
    Разрешает отключение кода приглашения.
    """

    message = "У вас нет прав на отключение кода приглашения."

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
        Проверяет право отключения конкретного кода.

        Args:
            request:
                DRF request.
            view:
                DRF view.
            obj:
                InviteCode.

        Returns:
            bool: True, если отключение разрешено.
        """

        if obj.created_by_id == request.user.id:
            return True

        if is_superadmin(request.user):
            return True

        context = get_object_context(obj)

        return is_organization_admin(
            request.user,
            organization=context["organization"],
            department=context["department"],
        )


class CanUseInviteCode(BasePermission):
    """
    Разрешает использование кода приглашения активным пользователям.

    Важно:
        Саму проверку кода выполняет invite_code_services.validate_invite_code().
    """

    message = "Вы не можете использовать этот код приглашения."

    def has_permission(self, request, view) -> bool:
        """
        Проверяет право использовать код.

        Args:
            request:
                DRF request.
            view:
                DRF view.

        Returns:
            bool: True, если пользователь активен.
        """

        return is_authenticated_active_user(request.user)


class CanManageInviteCode(BasePermission):
    """
    Универсальное разрешение на управление кодом приглашения.
    """

    message = "У вас нет прав на управление этим кодом приглашения."

    def has_permission(self, request, view) -> bool:
        """
        Проверяет общий доступ к управлению кодами.

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
        Проверяет право управления конкретным кодом.

        Args:
            request:
                DRF request.
            view:
                DRF view.
            obj:
                InviteCode.

        Returns:
            bool: True, если управление разрешено.
        """

        if obj.purpose == InviteCodePurpose.TEACHER_REGISTRATION:
            context = get_object_context(obj)

            return can_review_teacher(
                request.user,
                organization=context["organization"],
                department=context["department"],
            )

        if obj.purpose in {
            InviteCodePurpose.GUARDIAN_LINK_CURATOR,
            InviteCodePurpose.GUARDIAN_LINK_LEARNER,
        }:
            context = get_object_context(obj)

            return can_review_guardian_link(
                request.user,
                organization=context["organization"],
                department=context["department"],
                group=context["group"],
            )

        return is_superadmin(request.user)
