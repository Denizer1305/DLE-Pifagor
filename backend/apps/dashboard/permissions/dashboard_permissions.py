from __future__ import annotations

from apps.users.constants.lifecycle import UserRoleStatus
from apps.users.constants.roles import (
    GUARDIAN_ROLE_CODES,
    LEARNER_ROLE_CODES,
    PLATFORM_ADMIN_ROLE_CODES,
    STAFF_ROLE_CODES,
)
from rest_framework.permissions import BasePermission


class IsPlatformAdmin(BasePermission):
    """
    Разрешает доступ суперпользователю платформы.

    Сейчас поддерживает:
        - Django is_superuser;
        - активную бизнес-роль из PLATFORM_ADMIN_ROLE_CODES.

    Позже сюда без боли добавятся:
        - platform_admin;
        - moderator;
        - support;
        - organization_admin с ограничением по organization.
    """

    message = "Недостаточно прав для доступа к административной сводке."

    def has_permission(self, request, view) -> bool:
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        return user.user_roles.filter(
            role__code__in=PLATFORM_ADMIN_ROLE_CODES,
            status=UserRoleStatus.ACTIVE,
            role__is_active=True,
        ).exists()


class IsTeacherDashboardUser(BasePermission):
    message = "Недостаточно прав для доступа к кабинету преподавателя."

    def has_permission(self, request, view) -> bool:
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        return user.user_roles.filter(
            role__code__in=STAFF_ROLE_CODES,
            status=UserRoleStatus.ACTIVE,
            role__is_active=True,
        ).exists()


class IsStudentDashboardUser(BasePermission):
    message = "Недостаточно прав для доступа к кабинету студента."

    def has_permission(self, request, view) -> bool:
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        has_active_learner_role = user.user_roles.filter(
            role__code__in=LEARNER_ROLE_CODES,
            status=UserRoleStatus.ACTIVE,
            role__is_active=True,
        ).exists()

        if has_active_learner_role:
            return True

        return (
            user.is_email_verified
            and user.is_login_allowed
            and hasattr(user, "learner_profile")
        )


class IsParentDashboardUser(BasePermission):
    message = "Недостаточно прав для доступа к кабинету родителя."

    def has_permission(self, request, view) -> bool:
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        return user.user_roles.filter(
            role__code__in=GUARDIAN_ROLE_CODES,
            status=UserRoleStatus.ACTIVE,
            role__is_active=True,
        ).exists()
