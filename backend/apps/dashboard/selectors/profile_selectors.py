from __future__ import annotations

from apps.users.constants.lifecycle import UserRoleStatus


def get_user_avatar_url(user, request=None) -> str:
    """
    Возвращает абсолютный URL аватара пользователя.

    Сейчас учитывает возможное отсутствие связанного profile.
    """

    try:
        profile = getattr(user, "profile", None)
    except Exception:
        return ""

    if not profile or not getattr(profile, "avatar", None):
        return ""

    avatar_url = profile.avatar.url

    if request:
        return request.build_absolute_uri(avatar_url)

    return avatar_url


def get_admin_role_label(user) -> str:
    """
    Возвращает человекочитаемую роль администратора.
    """

    if user.is_superuser:
        return "Суперпользователь платформы"

    user_role = (
        user.user_roles.select_related("role")
        .filter(
            status=UserRoleStatus.ACTIVE,
            role__is_active=True,
        )
        .order_by("role__sort_order")
        .first()
    )

    if user_role:
        return user_role.role.label

    return "Администратор"


def get_admin_profile_payload(user, request=None) -> dict:
    """
    Формирует профиль администратора для dashboard.
    """

    return {
        "id": user.id,
        "full_name": user.get_full_name() or user.email,
        "email": user.email,
        "avatar_url": get_user_avatar_url(user, request=request),
        "role_label": get_admin_role_label(user),
    }
