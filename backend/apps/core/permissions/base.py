from __future__ import annotations

from apps.core.permissions.predicates import is_active_user, is_safe_method
from rest_framework.permissions import BasePermission


class IsAuthenticatedAndActive(BasePermission):
    """
    Разрешает доступ только авторизованному и активному пользователю.
    """

    message = "Для доступа необходимо войти в активный аккаунт."

    def has_permission(self, request, view) -> bool:
        """
        Проверяет доступ на уровне запроса.
        """

        return is_active_user(request.user)


class IsReadOnly(BasePermission):
    """
    Разрешает только безопасные методы чтения.
    """

    message = "Разрешён только просмотр данных."

    def has_permission(self, request, view) -> bool:
        """
        Проверяет, является ли HTTP-метод безопасным.
        """

        return is_safe_method(request)


class IsSuperUser(BasePermission):
    """
    Разрешает доступ только Django superuser.

    Бизнес-роль superadmin проверяется через role predicates.
    """

    message = "Доступ разрешён только системному администратору."

    def has_permission(self, request, view) -> bool:
        """
        Проверяет, является ли пользователь системным superuser.
        """

        user = request.user

        return bool(
            user and user.is_authenticated and getattr(user, "is_superuser", False)
        )
