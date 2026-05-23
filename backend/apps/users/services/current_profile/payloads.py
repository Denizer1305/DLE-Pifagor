from __future__ import annotations

from apps.users.selectors.current_profile_selectors import (
    get_active_role_code_for_user,
    get_current_role_profile,
    get_or_create_profile_for_user,
    get_role_label,
)
from apps.users.services.current_profile.role_profiles import build_role_profile_payload


def build_current_profile_payload(*, user) -> dict:
    """
    Собирает данные для страницы «Мой профиль».
    """

    profile = get_or_create_profile_for_user(user)
    role_code = get_active_role_code_for_user(user)
    role_profile = get_current_role_profile(user, role_code)

    return {
        "identity": build_identity_payload(user=user, profile=profile),
        "contacts": build_contacts_payload(user=user, profile=profile),
        "display_settings": build_display_settings_payload(profile=profile),
        "active_role": {
            "code": role_code,
            "label": get_role_label(role_code),
        },
        "role_profile": build_role_profile_payload(
            role_code=role_code,
            role_profile=role_profile,
        ),
        "available_roles": [],
    }


def build_identity_payload(*, user, profile) -> dict:
    """
    Собирает блок основных данных профиля.
    """

    return {
        "id": user.id,
        "email": user.email,
        "phone": user.phone or "",
        "first_name": user.first_name,
        "last_name": user.last_name,
        "middle_name": user.middle_name or "",
        "full_name": user.get_full_name(),
        "birth_date": user.birth_date,
        "gender": profile.gender,
        "city": profile.city or "",
        "about": profile.about or "",
        "avatar_url": profile.avatar.url if profile.avatar else "",
        "timezone": profile.timezone or "",
    }


def build_contacts_payload(*, user, profile) -> dict:
    """
    Собирает блок контактов профиля.
    """

    return {
        "email": user.email,
        "backup_email": user.backup_email or "",
        "phone": user.phone or "",
        "vk_url": profile.social_link_vk or "",
        "max_url": profile.social_link_max or "",
        "preferred_contact_method": profile.preferred_contact_method,
        "is_email_verified": user.is_email_verified,
        "is_phone_verified": user.is_phone_verified,
        "show_email": profile.show_email,
        "show_phone": profile.show_phone,
    }


def build_display_settings_payload(*, profile) -> dict:
    """
    Собирает настройки отображения профиля.
    """

    return {
        "show_email": profile.show_email,
        "show_phone": profile.show_phone,
        "email_notifications": profile.email_notifications,
        "push_notifications": profile.push_notifications,
    }
