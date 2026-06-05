"""
Обновление пользовательских настроек.
"""

from __future__ import annotations

from apps.users.services.user_settings.payloads import (
    build_appearance_settings_payload,
    build_notification_settings_payload,
    build_privacy_settings_payload,
    build_role_settings_payload,
    build_security_settings_payload,
    build_settings_payload,
    merge_settings,
)
from django.db import transaction


@transaction.atomic
def update_all_settings(*, settings_obj, data: dict) -> dict:
    """
    Обновляет полный набор пользовательских настроек.
    """

    if "appearance" in data:
        update_appearance_settings(settings_obj=settings_obj, data=data["appearance"])

    if "notifications" in data:
        update_notification_settings(
            settings_obj=settings_obj, data=data["notifications"]
        )

    if "privacy" in data:
        update_privacy_settings(settings_obj=settings_obj, data=data["privacy"])

    if "security" in data:
        update_security_settings(settings_obj=settings_obj, data=data["security"])

    if "roles" in data:
        update_role_settings(settings_obj=settings_obj, data=data["roles"])

    settings_obj.refresh_from_db()

    return build_settings_payload(settings_obj=settings_obj)


@transaction.atomic
def update_appearance_settings(*, settings_obj, data: dict) -> dict:
    """
    Обновляет настройки внешнего вида.
    """

    appearance_data = data.copy()
    language = appearance_data.pop("language", None)
    current = build_appearance_settings_payload(settings_obj=settings_obj)
    current.pop("language", None)
    settings_obj.appearance_settings = merge_settings(current, appearance_data)

    update_fields = ["appearance_settings", "updated_at"]

    if language is not None:
        settings_obj.language = language
        update_fields.append("language")

    settings_obj.full_clean()
    settings_obj.save(update_fields=update_fields)

    return build_appearance_settings_payload(settings_obj=settings_obj)


@transaction.atomic
def update_notification_settings(*, settings_obj, data: dict) -> dict:
    """
    Обновляет настройки уведомлений.
    """

    current = build_notification_settings_payload(settings_obj=settings_obj)
    settings_obj.notification_settings = merge_settings(current, data)
    settings_obj.full_clean()
    settings_obj.save(update_fields=["notification_settings", "updated_at"])

    return build_notification_settings_payload(settings_obj=settings_obj)


@transaction.atomic
def update_privacy_settings(*, settings_obj, data: dict) -> dict:
    """
    Обновляет настройки приватности.
    """

    current = build_privacy_settings_payload(settings_obj=settings_obj)
    settings_obj.privacy_settings = merge_settings(current, data)
    settings_obj.full_clean()
    settings_obj.save(update_fields=["privacy_settings", "updated_at"])

    return build_privacy_settings_payload(settings_obj=settings_obj)


@transaction.atomic
def update_role_settings(*, settings_obj, data: dict) -> dict:
    """
    Обновляет ролевые настройки.
    """

    current = build_role_settings_payload(settings_obj=settings_obj)
    settings_obj.role_settings = merge_settings(current, data)
    settings_obj.full_clean()
    settings_obj.save(update_fields=["role_settings", "updated_at"])

    return build_role_settings_payload(settings_obj=settings_obj)


@transaction.atomic
def update_security_settings(*, settings_obj, data: dict) -> dict:
    """
    Обновляет настройки безопасности.
    """

    current = build_security_settings_payload(settings_obj=settings_obj)
    settings_obj.security_settings = merge_settings(current, data)
    settings_obj.full_clean()
    settings_obj.save(update_fields=["security_settings", "updated_at"])

    return build_security_settings_payload(settings_obj=settings_obj)
