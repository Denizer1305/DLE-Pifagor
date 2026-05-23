from __future__ import annotations

from apps.users.permissions.helpers import (
    get_object_context,
    is_authenticated_active_user,
    is_organization_admin,
)
from rest_framework.permissions import BasePermission


class IsOrganizationAdminRole(BasePermission):
    """
    Разрешает доступ администраторам организации.

    Для объектных проверок берёт organization/department из объекта.
    """

    message = "Доступ разрешён только администратору организации."

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
        Проверяет доступ к объекту в организационном контексте.

        Args:
            request:
                DRF request.
            view:
                DRF view.
            obj:
                Объект проверки.

        Returns:
            bool: True, если пользователь управляет контекстом объекта.
        """

        context = get_object_context(obj)

        return is_organization_admin(
            request.user,
            organization=context["organization"],
            department=context["department"],
        )
