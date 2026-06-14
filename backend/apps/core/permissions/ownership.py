from __future__ import annotations

from apps.core.permissions.predicates import is_authenticated_user, is_safe_method
from rest_framework.permissions import BasePermission

OWNER_FIELD_NAMES = (
    "user",
    "owner",
    "created_by",
)


def get_object_owner(obj):
    """
    Возвращает владельца объекта по стандартным полям.

    Для сложных доменных связей нужно писать permission внутри приложения.
    """

    if obj is None:
        return None

    for field_name in OWNER_FIELD_NAMES:
        owner = getattr(obj, field_name, None)

        if owner is not None:
            return owner

    return None


def is_object_owner(user, obj) -> bool:
    """
    Проверяет, является ли пользователь владельцем объекта.
    """

    if not is_authenticated_user(user):
        return False

    return get_object_owner(obj) == user


class IsOwner(BasePermission):
    """
    Разрешает доступ владельцу объекта.

    Ожидает, что у объекта есть одно из полей:
    user, owner, created_by.
    """

    message = "Вы можете работать только со своими объектами."

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет объектный доступ.
        """

        return is_object_owner(request.user, obj)


class IsOwnerOrReadOnly(BasePermission):
    """
    Разрешает чтение всем, а изменение только владельцу.
    """

    message = "Изменять объект может только владелец."

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет объектный доступ.
        """

        if is_safe_method(request):
            return True

        return is_object_owner(request.user, obj)
