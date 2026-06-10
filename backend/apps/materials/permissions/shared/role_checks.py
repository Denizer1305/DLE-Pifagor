from __future__ import annotations

from apps.materials.selectors import (
    user_can_edit_materials,
    user_is_authenticated,
    user_is_global_material_admin,
    user_is_material_teacher,
    user_is_organization_material_admin,
)


def user_can_manage_materials_globally(user) -> bool:
    """
    Проверяет право глобального управления материалами.
    """

    return user_is_global_material_admin(user)


def user_can_manage_materials_in_scope(user) -> bool:
    """
    Проверяет право управления материалами в доступной области.
    """

    if not user_is_authenticated(user):
        return False

    return bool(
        user_can_edit_materials(user)
        or user_is_organization_material_admin(user)
        or user_is_material_teacher(user)
    )


def user_can_read_materials(user) -> bool:
    """
    Проверяет базовое право чтения материалов.
    """

    return user_is_authenticated(user)
