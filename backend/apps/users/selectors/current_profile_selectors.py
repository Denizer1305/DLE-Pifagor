from __future__ import annotations

from apps.users.constants.roles import RoleCode
from apps.users.models import Profile
from apps.users.selectors.role_selectors import get_user_active_role_codes


def get_or_create_profile_for_user(user) -> Profile:
    """
    Возвращает или создаёт базовый профиль текущего пользователя.
    """

    profile, _created = Profile.objects.get_or_create(user=user)

    return profile


def get_active_role_code_for_user(user) -> str:
    """
    Возвращает активную роль пользователя.

    Если активная роль не задана в настройках, берёт первую доступную роль.
    """

    settings = getattr(user, "settings", None)

    if settings and settings.active_role:
        return settings.active_role

    role_codes = sorted(get_user_active_role_codes(user))

    if role_codes:
        return role_codes[0]

    if user.is_superuser:
        return RoleCode.SUPERADMIN

    return ""


def get_role_label(role_code: str) -> str:
    """
    Возвращает русское название роли.
    """

    labels = dict(RoleCode.choices)

    return labels.get(role_code, role_code or "Пользователь")


def get_current_role_profile(user, role_code: str):
    """
    Возвращает ролевой профиль пользователя по активной роли.
    """

    if role_code in {
        RoleCode.TEACHER,
        RoleCode.CURATOR,
        RoleCode.METHODIST,
        RoleCode.ORGANIZER,
        RoleCode.MENTOR,
    }:
        return getattr(user, "teacher_profile", None)

    if role_code == RoleCode.LEARNER:
        return getattr(user, "learner_profile", None)

    if role_code == RoleCode.GUARDIAN:
        return getattr(user, "guardian_profile", None)

    return None
