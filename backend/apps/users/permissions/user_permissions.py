from __future__ import annotations

from apps.users.permissions.helpers import (
    get_object_user,
    is_authenticated_active_user,
    is_organization_admin,
    is_safe_method,
    is_self,
    is_superadmin,
)
from rest_framework.permissions import BasePermission


class CanViewUser(BasePermission):
    """
    Разрешает просмотр пользователя.

    Доступ имеют:
        - сам пользователь;
        - суперадминистратор;
        - администратор организации при объектном контексте.
    """

    message = "У вас нет прав на просмотр этого пользователя."

    def has_permission(self, request, view) -> bool:
        """
        Проверяет доступ к списку или endpoint пользователя.

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
        Проверяет доступ к конкретному пользователю.

        Args:
            request:
                DRF request.
            view:
                DRF view.
            obj:
                Пользователь.

        Returns:
            bool: True, если доступ разрешён.
        """

        if is_self(request.user, obj):
            return True

        return is_superadmin(request.user)


class CanUpdateUser(BasePermission):
    """
    Разрешает изменение пользователя.

    Доступ имеют:
        - сам пользователь для своего аккаунта;
        - суперадминистратор.

    Важные системные изменения лучше выполнять отдельными сервисами.
    """

    message = "У вас нет прав на изменение этого пользователя."

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
        Проверяет право изменения пользователя.

        Args:
            request:
                DRF request.
            view:
                DRF view.
            obj:
                Пользователь.

        Returns:
            bool: True, если изменение разрешено.
        """

        return is_self(request.user, obj) or is_superadmin(request.user)


class CanManageUserLifecycle(BasePermission):
    """
    Разрешает управление жизненным циклом пользователя.

    Сюда относятся:
        - блокировка;
        - архивация;
        - планирование удаления;
        - анонимизация.
    """

    message = "У вас нет прав на управление жизненным циклом пользователя."

    def has_permission(self, request, view) -> bool:
        """
        Проверяет, может ли пользователь выполнять lifecycle-операции.

        Args:
            request:
                DRF request.
            view:
                DRF view.

        Returns:
            bool: True, если пользователь является суперадминистратором.
        """

        return is_superadmin(request.user)


class CanBlockUser(CanManageUserLifecycle):
    """
    Разрешает блокировку пользователя.
    """


class CanArchiveUser(CanManageUserLifecycle):
    """
    Разрешает архивацию пользователя.
    """


class CanAnonymizeUser(CanManageUserLifecycle):
    """
    Разрешает анонимизацию пользователя.
    """


class CanViewOwnOrManagedUser(BasePermission):
    """
    Разрешает видеть свой аккаунт или управляемый аккаунт ребёнка.
    """

    message = "У вас нет доступа к этому аккаунту."

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
        Проверяет доступ к своему или управляемому аккаунту.

        Args:
            request:
                DRF request.
            view:
                DRF view.
            obj:
                Пользователь.

        Returns:
            bool: True, если доступ разрешён.
        """

        if is_self(request.user, obj):
            return True

        return getattr(obj, "account_managed_by_id", None) == request.user.id


class CanReadUserObject(BasePermission):
    """
    Универсальное чтение объекта, связанного с пользователем.

    Подходит для объектов, где есть поле user.
    """

    message = "У вас нет прав на просмотр объекта пользователя."

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
        Проверяет доступ к объекту пользователя.

        Args:
            request:
                DRF request.
            view:
                DRF view.
            obj:
                Объект с полем user.

        Returns:
            bool: True, если доступ разрешён.
        """

        object_user = get_object_user(obj)

        return (
            is_self(request.user, object_user)
            or is_superadmin(request.user)
            or is_safe_method(request)
        )


class CanManageUsersInOrganization(BasePermission):
    """
    Разрешает управление пользователями в рамках организации.

    Для точной фильтрации списка пользователей нужно ограничивать queryset во view.
    """

    message = "У вас нет прав на управление пользователями организации."

    def has_permission(self, request, view) -> bool:
        """
        Проверяет общий доступ на уровне view.

        Args:
            request:
                DRF request.
            view:
                DRF view.

        Returns:
            bool: True, если пользователь суперадмин или администратор организации.
        """

        return is_superadmin(request.user) or is_organization_admin(request.user)
