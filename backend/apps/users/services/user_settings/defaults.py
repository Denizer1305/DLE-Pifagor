"""
Дефолтные значения пользовательских настроек.

Все настройки пользователя хранятся в JSONField, поэтому этот файл является
единой точкой, где описывается полная структура настроек по умолчанию.
"""

from __future__ import annotations

from copy import deepcopy

from apps.users.constants.settings import (
    AppearanceTheme,
    ColorMode,
    InterfaceDensity,
    NotificationFrequency,
    ProfileVisibility,
    SessionLifetimeMode,
    SettingsRoleCode,
)

DEFAULT_APPEARANCE_SETTINGS: dict = {
    "theme": AppearanceTheme.LIGHT,
    "color_mode": ColorMode.SYSTEM,
    "density": InterfaceDensity.COMFORTABLE,
    "animations_enabled": True,
    "glass_panels_enabled": True,
    "rounded_cards_enabled": True,
    "sticky_sidebar_enabled": True,
    "large_cards_enabled": False,
}

DEFAULT_NOTIFICATION_SETTINGS: dict = {
    "channels": {
        "in_app": True,
        "email": True,
        "vk": False,
        "max": False,
    },
    "frequency": {
        "security": NotificationFrequency.INSTANT,
        "education": NotificationFrequency.INSTANT,
        "assignments": NotificationFrequency.DAILY,
        "schedule": NotificationFrequency.INSTANT,
        "feedback": NotificationFrequency.INSTANT,
        "system": NotificationFrequency.DAILY,
        "digest": NotificationFrequency.DAILY,
        "marketing": NotificationFrequency.DISABLED,
    },
    "digest_time": "08:00",
}

DEFAULT_PRIVACY_SETTINGS: dict = {
    "profile_visibility": ProfileVisibility.ORGANIZATION,
    "show_email": True,
    "show_phone": False,
    "show_city": True,
    "show_birth_date": False,
    "show_role_profile": True,
    "show_achievements": True,
    "allow_teachers_access": True,
    "allow_students_access": False,
    "allow_guardians_access": False,
    "allow_admins_access": True,
    "allow_data_export": True,
}

DEFAULT_SECURITY_SETTINGS: dict = {
    "login_notifications_enabled": True,
    "suspicious_activity_notifications_enabled": True,
    "trusted_devices_enabled": True,
    "session_lifetime_mode": SessionLifetimeMode.STANDARD,
    "two_factor_enabled": False,
}

DEFAULT_ROLE_SETTINGS: dict = {
    "active_role": SettingsRoleCode.TEACHER,
    "roles": {
        SettingsRoleCode.TEACHER: {
            "show_hero_block": True,
            "show_topbar": True,
            "show_sidebar": True,
            "show_quick_overview": True,
            "show_profile_contacts": True,
            "show_profile_role_section": True,
            "show_sidebar_ai": True,
            "show_ai_card": True,
            "show_lesson_hints": True,
            "show_group_analytics": True,
        },
        SettingsRoleCode.LEARNER: {
            "show_hero_block": True,
            "show_progress": True,
            "show_assignments": True,
            "show_schedule": True,
            "show_achievements": True,
            "show_ai_hints": True,
        },
        SettingsRoleCode.GUARDIAN: {
            "show_children_progress": True,
            "show_teacher_contacts": True,
            "show_notifications": True,
            "show_schedule": True,
        },
        SettingsRoleCode.ADMIN: {
            "show_system_summary": True,
            "show_moderation_panel": True,
            "show_audit_events": True,
            "show_support_requests": True,
        },
    },
}


def get_default_appearance_settings() -> dict:
    """
    Возвращает копию дефолтных настроек внешнего вида.
    """

    return deepcopy(DEFAULT_APPEARANCE_SETTINGS)


def get_default_notification_settings() -> dict:
    """
    Возвращает копию дефолтных настроек уведомлений.
    """

    return deepcopy(DEFAULT_NOTIFICATION_SETTINGS)


def get_default_privacy_settings() -> dict:
    """
    Возвращает копию дефолтных настроек приватности.
    """

    return deepcopy(DEFAULT_PRIVACY_SETTINGS)


def get_default_security_settings() -> dict:
    """
    Возвращает копию дефолтных настроек безопасности.
    """

    return deepcopy(DEFAULT_SECURITY_SETTINGS)


def get_default_role_settings() -> dict:
    """
    Возвращает копию дефолтных ролевых настроек.
    """

    return deepcopy(DEFAULT_ROLE_SETTINGS)


def get_default_user_settings_payload() -> dict:
    """
    Возвращает полный набор дефолтных пользовательских настроек.
    """

    return {
        "appearance": get_default_appearance_settings(),
        "notifications": get_default_notification_settings(),
        "privacy": get_default_privacy_settings(),
        "security": get_default_security_settings(),
        "roles": get_default_role_settings(),
    }
