from __future__ import annotations

from collections.abc import Callable
from typing import Any

from rest_framework.permissions import SAFE_METHODS, BasePermission

from .object_checks import user_can_manage_payload_organizations
from .role_checks import (
    user_can_manage_global_education,
    user_can_manage_scoped_education,
    user_has_education_access,
)


class EducationBasePermission(BasePermission):
    """
    Базовый permission академического модуля.
    """

    message = "Недостаточно прав для работы с академическим модулем."

    def has_permission(self, request, view) -> bool:
        """
        Проверяет авторизацию и базовый доступ к education.
        """

        return bool(
            request.user
            and request.user.is_authenticated
            and user_has_education_access(request.user)
        )


class EducationGlobalMutationPermission(EducationBasePermission):
    """
    Permission для глобальных академических сущностей.

    Чтение доступно участникам академического процесса.
    Изменение доступно только глобальным администраторам.
    """

    message = "Изменять глобальные академические данные может только глобальный администратор."

    def has_permission(self, request, view) -> bool:
        """
        Проверяет доступ к глобальной академической сущности.
        """

        if not super().has_permission(request, view):
            return False

        if request.method in SAFE_METHODS:
            return True

        return user_can_manage_global_education(request.user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет объектный доступ.
        """

        if request.method in SAFE_METHODS:
            return user_has_education_access(request.user)

        return user_can_manage_global_education(request.user)


class EducationScopedPermission(EducationBasePermission):
    """
    Permission для академических сущностей, привязанных
    к организации или группе.
    """

    message = "Недостаточно прав для этой академической области."

    payload_organization_getter: Callable[[Any], set[int]] | None = None

    def has_permission(self, request, view) -> bool:
        """
        Проверяет общий доступ и возможность создания объекта.
        """

        if not super().has_permission(request, view):
            return False

        if request.method in SAFE_METHODS:
            return True

        if not user_can_manage_scoped_education(request.user):
            return False

        if request.method != "POST":
            return True

        if self.payload_organization_getter is None:
            return True

        organization_ids = self.payload_organization_getter(request.data)

        return user_can_manage_payload_organizations(
            user=request.user,
            organization_ids=organization_ids,
        )
