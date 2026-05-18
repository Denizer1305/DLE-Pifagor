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
        create_registration_attempt_log as create_registration_attempt_log,
    )
    from apps.users.services.audit_services import (
        create_user_audit_log as create_user_audit_log,
    )
    from apps.users.services.audit_services import (
        log_email_verified as log_email_verified,
    )
    from apps.users.services.audit_services import log_failed_login as log_failed_login
    from apps.users.services.audit_services import (
        log_join_request_approved as log_join_request_approved,
    )
    from apps.users.services.audit_services import (
        log_join_request_created as log_join_request_created,
    )
    from apps.users.services.audit_services import (
        log_join_request_rejected as log_join_request_rejected,
    )
    from apps.users.services.audit_services import (
        log_user_registered as log_user_registered,
    )
    from apps.users.services.auth_services import authenticate_user as authenticate_user
    from apps.users.services.auth_services import (
        blacklist_refresh_token as blacklist_refresh_token,
    )
    from apps.users.services.auth_services import (
        clear_refresh_token_cookie as clear_refresh_token_cookie,
    )
    from apps.users.services.auth_services import (
        create_token_pair_for_user as create_token_pair_for_user,
    )
    from apps.users.services.auth_services import (
        get_refresh_token_from_request as get_refresh_token_from_request,
    )
    from apps.users.services.auth_services import login_user as login_user
    from apps.users.services.auth_services import (
        refresh_access_token as refresh_access_token,
    )
    from apps.users.services.auth_services import (
        set_refresh_token_cookie as set_refresh_token_cookie,
    )
    from apps.users.services.email_verification_services import (
        build_email_verification_url as build_email_verification_url,
    )
    from apps.users.services.email_verification_services import (
        create_email_verification_token as create_email_verification_token,
    )
    from apps.users.services.email_verification_services import (
        verify_email_token as verify_email_token,
    )
    from apps.users.services.invite_code_services import (
        create_guardian_curator_code as create_guardian_curator_code,
    )
    from apps.users.services.invite_code_services import (
        create_guardian_learner_code as create_guardian_learner_code,
    )
    from apps.users.services.invite_code_services import (
        create_invite_code as create_invite_code,
    )
    from apps.users.services.invite_code_services import (
        create_teacher_registration_code as create_teacher_registration_code,
    )
    from apps.users.services.invite_code_services import (
        use_invite_code as use_invite_code,
    )
    from apps.users.services.invite_code_services import (
        validate_invite_code as validate_invite_code,
    )
    from apps.users.services.join_requests import (
        approve_join_request as approve_join_request,
    )
    from apps.users.services.join_requests import (
        create_guardian_join_request as create_guardian_join_request,
    )
    from apps.users.services.join_requests import (
        create_join_request as create_join_request,
    )
    from apps.users.services.join_requests import (
        create_learner_join_request as create_learner_join_request,
    )
    from apps.users.services.join_requests import (
        create_teacher_join_request as create_teacher_join_request,
    )
    from apps.users.services.join_requests import (
        reject_join_request as reject_join_request,
    )
    from apps.users.services.profiles import create_base_profile as create_base_profile
    from apps.users.services.profiles import (
        create_guardian_learner_link as create_guardian_learner_link,
    )
    from apps.users.services.profiles import (
        create_guardian_profile as create_guardian_profile,
    )
    from apps.users.services.profiles import (
        create_learner_profile as create_learner_profile,
    )
    from apps.users.services.profiles import (
        create_teacher_profile as create_teacher_profile,
    )
    from apps.users.services.profiles import moderate_avatar as moderate_avatar
    from apps.users.services.profiles import reject_profile as reject_profile
    from apps.users.services.profiles import (
        submit_avatar_for_moderation as submit_avatar_for_moderation,
    )
    from apps.users.services.profiles import (
        verify_learner_profile as verify_learner_profile,
    )
    from apps.users.services.profiles import (
        verify_teacher_profile as verify_teacher_profile,
    )
    from apps.users.services.registration import register_guardian as register_guardian
    from apps.users.services.registration import register_learner as register_learner
    from apps.users.services.registration import (
        register_minor_learner_by_guardian as register_minor_learner_by_guardian,
    )
    from apps.users.services.registration import register_teacher as register_teacher
    from apps.users.services.registration import (
        submit_learner_group_request as submit_learner_group_request,
    )
    from apps.users.services.user_lifecycle_services import (
        activate_user as activate_user,
    )
    from apps.users.services.user_lifecycle_services import (
        anonymize_user as anonymize_user,
    )
    from apps.users.services.user_lifecycle_services import archive_user as archive_user
    from apps.users.services.user_lifecycle_services import block_user as block_user
    from apps.users.services.user_lifecycle_services import (
        schedule_user_deletion as schedule_user_deletion,
    )
    from apps.users.services.user_lifecycle_services import (
        schedule_user_deletion_after_rejection as schedule_user_deletion_after_rejection,
    )
    from apps.users.services.user_settings_services import (
        create_default_user_settings as create_default_user_settings,
    )
    from apps.users.services.user_settings_services import (
        set_active_role as set_active_role,
    )
    from apps.users.services.user_settings_services import (
        update_compact_mode as update_compact_mode,
    )
    from apps.users.services.user_settings_services import (
        update_interface_theme as update_interface_theme,
    )
    from apps.users.services.user_settings_services import (
        update_language as update_language,
    )
    from apps.users.services.user_settings_services import (
        update_timezone as update_timezone,
    )


__all__ = list(_SERVICE_EXPORTS.keys())
