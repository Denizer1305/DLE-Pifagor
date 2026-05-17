from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING

"""
Сервисы приложения users.

Файл работает как ленивый фасад.

Можно импортировать так:
    from apps.users.services import register_learner

При этом реальные модули не загружаются заранее, что снижает риск
циклических импортов между services, tasks и emails.
"""


_SERVICE_EXPORTS = {
    # audit_services.py
    "create_registration_attempt_log": "apps.users.services.audit_services",
    "create_user_audit_log": "apps.users.services.audit_services",
    "log_email_verified": "apps.users.services.audit_services",
    "log_failed_login": "apps.users.services.audit_services",
    "log_join_request_approved": "apps.users.services.audit_services",
    "log_join_request_created": "apps.users.services.audit_services",
    "log_join_request_rejected": "apps.users.services.audit_services",
    "log_user_registered": "apps.users.services.audit_services",
    # auth_services.py
    "authenticate_user": "apps.users.services.auth_services",
    "blacklist_refresh_token": "apps.users.services.auth_services",
    "clear_refresh_token_cookie": "apps.users.services.auth_services",
    "create_token_pair_for_user": "apps.users.services.auth_services",
    "get_refresh_token_from_request": "apps.users.services.auth_services",
    "login_user": "apps.users.services.auth_services",
    "refresh_access_token": "apps.users.services.auth_services",
    "set_refresh_token_cookie": "apps.users.services.auth_services",
    # email_verification_services.py
    "build_email_verification_url": "apps.users.services.email_verification_services",
    "create_email_verification_token": "apps.users.services.email_verification_services",
    "verify_email_token": "apps.users.services.email_verification_services",
    # invite_code_services.py
    "create_guardian_curator_code": "apps.users.services.invite_code_services",
    "create_guardian_learner_code": "apps.users.services.invite_code_services",
    "create_invite_code": "apps.users.services.invite_code_services",
    "create_teacher_registration_code": "apps.users.services.invite_code_services",
    "use_invite_code": "apps.users.services.invite_code_services",
    "validate_invite_code": "apps.users.services.invite_code_services",
    # password_reset_services.py
    "build_password_reset_url": "apps.users.services.password_reset_services",
    "create_password_reset_token": "apps.users.services.password_reset_services",
    "request_password_reset": "apps.users.services.password_reset_services",
    "reset_password_by_token": "apps.users.services.password_reset_services",
    # join_requests/
    "approve_join_request": "apps.users.services.join_requests",
    "create_guardian_join_request": "apps.users.services.join_requests",
    "create_join_request": "apps.users.services.join_requests",
    "create_learner_join_request": "apps.users.services.join_requests",
    "create_teacher_join_request": "apps.users.services.join_requests",
    "reject_join_request": "apps.users.services.join_requests",
    # profiles/
    "create_base_profile": "apps.users.services.profiles",
    "create_guardian_learner_link": "apps.users.services.profiles",
    "create_guardian_profile": "apps.users.services.profiles",
    "create_learner_profile": "apps.users.services.profiles",
    "create_teacher_profile": "apps.users.services.profiles",
    "moderate_avatar": "apps.users.services.profiles",
    "reject_profile": "apps.users.services.profiles",
    "submit_avatar_for_moderation": "apps.users.services.profiles",
    "verify_learner_profile": "apps.users.services.profiles",
    "verify_teacher_profile": "apps.users.services.profiles",
    # registration/
    "register_guardian": "apps.users.services.registration",
    "register_learner": "apps.users.services.registration",
    "register_minor_learner_by_guardian": "apps.users.services.registration",
    "register_teacher": "apps.users.services.registration",
    "submit_learner_group_request": "apps.users.services.registration",
    # user_lifecycle_services.py
    "activate_user": "apps.users.services.user_lifecycle_services",
    "anonymize_user": "apps.users.services.user_lifecycle_services",
    "archive_user": "apps.users.services.user_lifecycle_services",
    "block_user": "apps.users.services.user_lifecycle_services",
    "schedule_user_deletion": "apps.users.services.user_lifecycle_services",
    "schedule_user_deletion_after_rejection": "apps.users.services.user_lifecycle_services",
    # user_settings_services.py
    "create_default_user_settings": "apps.users.services.user_settings_services",
    "set_active_role": "apps.users.services.user_settings_services",
    "update_compact_mode": "apps.users.services.user_settings_services",
    "update_interface_theme": "apps.users.services.user_settings_services",
    "update_language": "apps.users.services.user_settings_services",
    "update_timezone": "apps.users.services.user_settings_services",
}


def __getattr__(name: str):
    """
    Лениво импортирует сервис при первом обращении.

    Args:
        name:
            Имя запрашиваемого сервиса.

    Returns:
        object: Функция сервиса.

    Raises:
        AttributeError: Если имя не зарегистрировано в фасаде.
    """

    if name not in _SERVICE_EXPORTS:
        raise AttributeError(f"module 'apps.users.services' has no attribute '{name}'")

    module = import_module(_SERVICE_EXPORTS[name])
    value = getattr(module, name)

    globals()[name] = value

    return value


def __dir__() -> list[str]:
    """
    Возвращает список публичных имён пакета.

    Returns:
        list[str]: Список экспортируемых сервисов.
    """

    return sorted(list(globals().keys()) + list(_SERVICE_EXPORTS.keys()))


if TYPE_CHECKING:
    from apps.users.services.audit_services import (
        create_registration_attempt_log,
        create_user_audit_log,
        log_email_verified,
        log_failed_login,
        log_join_request_approved,
        log_join_request_created,
        log_join_request_rejected,
        log_user_registered,
    )
    from apps.users.services.auth_services import (
        authenticate_user,
        blacklist_refresh_token,
        clear_refresh_token_cookie,
        create_token_pair_for_user,
        get_refresh_token_from_request,
        login_user,
        refresh_access_token,
        set_refresh_token_cookie,
    )
    from apps.users.services.email_verification_services import (
        build_email_verification_url,
        create_email_verification_token,
        verify_email_token,
    )
    from apps.users.services.invite_code_services import (
        create_guardian_curator_code,
        create_guardian_learner_code,
        create_invite_code,
        create_teacher_registration_code,
        use_invite_code,
        validate_invite_code,
    )
    from apps.users.services.join_requests import (
        approve_join_request,
        create_guardian_join_request,
        create_join_request,
        create_learner_join_request,
        create_teacher_join_request,
        reject_join_request,
    )
    from apps.users.services.profiles import (
        create_base_profile,
        create_guardian_learner_link,
        create_guardian_profile,
        create_learner_profile,
        create_teacher_profile,
        moderate_avatar,
        reject_profile,
        submit_avatar_for_moderation,
        verify_learner_profile,
        verify_teacher_profile,
    )
    from apps.users.services.registration import (
        register_guardian,
        register_learner,
        register_minor_learner_by_guardian,
        register_teacher,
        submit_learner_group_request,
    )
    from apps.users.services.user_lifecycle_services import (
        activate_user,
        anonymize_user,
        archive_user,
        block_user,
        schedule_user_deletion,
        schedule_user_deletion_after_rejection,
    )
    from apps.users.services.user_settings_services import (
        create_default_user_settings,
        set_active_role,
        update_compact_mode,
        update_interface_theme,
        update_language,
        update_timezone,
    )


__all__ = list(_SERVICE_EXPORTS.keys())
