from __future__ import annotations

from apps.core.permissions.predicates import has_any_role, has_role, is_active_user
from rest_framework.permissions import BasePermission


class RoleRequiredPermission(BasePermission):
    """
    Базовая permission для проверки одной роли.

    Наследник должен определить role_code.
    """

    role_code = None
    message = "Недостаточно прав для выполнения действия."

    def has_permission(self, request, view) -> bool:
        """
        Проверяет наличие роли у пользователя.
        """

        if self.role_code is None:
            return False

        return has_role(
            user=request.user,
            role_code=self.role_code,
        )


class AnyRoleRequiredPermission(BasePermission):
    """
    Базовая permission для проверки набора ролей.

    Наследник должен определить role_codes.
    """

    role_codes = ()
    message = "Недостаточно прав для выполнения действия."

    def has_permission(self, request, view) -> bool:
        """
        Проверяет наличие хотя бы одной роли у пользователя.
        """

        if not self.role_codes:
            return False

        return has_any_role(
            user=request.user,
            role_codes=self.role_codes,
        )


class ActiveUserPermission(BasePermission):
    """
    Явная permission для активного пользователя.

    Может использоваться там, где не нужен отдельный класс
    IsAuthenticatedAndActive, но нужен короткий role-style base.
    """

    message = "Пользователь должен быть активен."

    def has_permission(self, request, view) -> bool:
        """
        Проверяет активного пользователя.
        """

        return is_active_user(request.user)
