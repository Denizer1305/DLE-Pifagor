"""
Публичный интерфейс сервисов пользовательских настроек.
"""

from __future__ import annotations

from apps.users.services.user_settings.defaults import (
    get_default_appearance_settings,
    get_default_notification_settings,
    get_default_privacy_settings,
    get_default_role_settings,
    get_default_security_settings,
    get_default_user_settings_payload,
)
from apps.users.services.user_settings.payloads import (
    build_appearance_settings_payload,
    build_notification_settings_payload,
    build_privacy_settings_payload,
    build_role_settings_payload,
    build_security_settings_payload,
    build_settings_payload,
    merge_settings,
)
from apps.users.services.user_settings.security import build_security_sessions_payload
from apps.users.services.user_settings.updates import (
    update_all_settings,
    update_appearance_settings,
    update_notification_settings,
    update_privacy_settings,
    update_role_settings,
    update_security_settings,
)

__all__ = [
    "build_appearance_settings_payload",
    "build_notification_settings_payload",
    "build_privacy_settings_payload",
    "build_role_settings_payload",
    "build_security_sessions_payload",
    "build_security_settings_payload",
    "build_settings_payload",
    "get_default_appearance_settings",
    "get_default_notification_settings",
    "get_default_privacy_settings",
    "get_default_role_settings",
    "get_default_security_settings",
    "get_default_user_settings_payload",
    "merge_settings",
    "update_all_settings",
    "update_appearance_settings",
    "update_notification_settings",
    "update_privacy_settings",
    "update_role_settings",
    "update_security_settings",
]
