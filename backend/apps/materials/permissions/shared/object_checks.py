from __future__ import annotations

from apps.materials.selectors import (
    user_can_access_material,
    user_can_access_organization,
    user_is_global_material_admin,
    user_is_material_teacher,
    user_is_organization_material_admin,
)


def user_can_read_material_object(
    *,
    user,
    material,
) -> bool:
    """
    Проверяет право чтения конкретного материала.
    """

    return user_can_access_material(
        user=user,
        material=material,
    )


def user_can_manage_material_object(
    *,
    user,
    material,
) -> bool:
    """
    Проверяет право управления конкретным материалом.
    """

    if user_is_global_material_admin(user):
        return True

    if material.owner_id == getattr(user, "id", None):
        return True

    if material.organization_id:
        return bool(
            user_is_organization_material_admin(user)
            and user_can_access_organization(
                user=user,
                organization_id=material.organization_id,
            )
        )

    return False


def user_can_read_material_category_object(
    *,
    user,
    category,
) -> bool:
    """
    Проверяет право чтения категории материалов.
    """

    if user_is_global_material_admin(user):
        return True

    if category.organization_id is None:
        return True

    return user_can_access_organization(
        user=user,
        organization_id=category.organization_id,
    )


def user_can_manage_material_category_object(
    *,
    user,
    category,
) -> bool:
    """
    Проверяет право управления категорией материалов.
    """

    if user_is_global_material_admin(user):
        return True

    if category.organization_id is None:
        return False

    return bool(
        user_is_organization_material_admin(user)
        and user_can_access_organization(
            user=user,
            organization_id=category.organization_id,
        )
    )


def user_can_read_material_version_object(
    *,
    user,
    version,
) -> bool:
    """
    Проверяет право чтения версии материала.
    """

    return user_can_read_material_object(
        user=user,
        material=version.material,
    )


def user_can_manage_material_version_object(
    *,
    user,
    version,
) -> bool:
    """
    Проверяет право управления версией материала.
    """

    return user_can_manage_material_object(
        user=user,
        material=version.material,
    )


def user_can_read_usage_log_object(
    *,
    user,
    usage_log,
) -> bool:
    """
    Проверяет право чтения события журнала использования материала.
    """

    if user_is_global_material_admin(user):
        return True

    if usage_log.user_id == getattr(user, "id", None):
        return True

    return user_can_manage_material_object(
        user=user,
        material=usage_log.material,
    )


def user_can_manage_usage_log_object(
    *,
    user,
    usage_log,
) -> bool:
    """
    Проверяет право управления событием журнала использования материала.
    """

    return user_is_global_material_admin(user)


def user_can_create_material_in_organization(
    *,
    user,
    organization,
) -> bool:
    """
    Проверяет право создания материала в организации.
    """

    if user_is_global_material_admin(user):
        return True

    if organization is None:
        return user_is_material_teacher(user)

    return bool(
        (user_is_organization_material_admin(user) or user_is_material_teacher(user))
        and user_can_access_organization(
            user=user,
            organization_id=organization.id,
        )
    )
