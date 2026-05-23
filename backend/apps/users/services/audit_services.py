from __future__ import annotations

from typing import Any

from apps.core.utils import get_client_ip, hash_value
from apps.users.constants.audit import AuditActorType, UserAuditAction
from apps.users.constants.onboarding import RegistrationAttemptStatus
from apps.users.models import RegistrationAttemptLog, UserAuditLog


def create_user_audit_log(
    *,
    action: str,
    actor=None,
    target_user=None,
    actor_type: str = AuditActorType.USER,
    message: str = "",
    metadata: dict[str, Any] | None = None,
    request=None,
) -> UserAuditLog:
    """
    Создаёт запись аудита действия пользователя.

    Args:
        action:
            Код действия аудита.
        actor:
            Пользователь, который выполнил действие.
        target_user:
            Пользователь, над которым выполнено действие.
        actor_type:
            Тип инициатора действия.
        message:
            Человекочитаемое описание действия.
        metadata:
            Дополнительные данные аудита.
        request:
            HTTP-запрос. Используется для IP и User-Agent.

    Returns:
        UserAuditLog: Созданная запись аудита.
    """

    ip_address = None
    user_agent = ""

    if request is not None:
        ip_address = get_client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT", "")

    return UserAuditLog.objects.create(
        actor=actor,
        actor_type=actor_type,
        target_user=target_user,
        action=action,
        message=message,
        metadata=metadata or {},
        ip_address=ip_address,
        user_agent=user_agent,
    )


def create_registration_attempt_log(
    *,
    email: str = "",
    phone: str = "",
    role_code: str = "",
    status: str = RegistrationAttemptStatus.FAILED,
    failure_reason: str = "",
    metadata: dict[str, Any] | None = None,
    request=None,
) -> RegistrationAttemptLog:
    """
    Создаёт запись попытки регистрации.

    Важно:
        Email и телефон не сохраняются в открытом виде.
        В БД пишутся только хеши.

    Args:
        email:
            Email из попытки регистрации.
        phone:
            Телефон из попытки регистрации.
        role_code:
            Код роли, которую пытался выбрать пользователь.
        status:
            Статус попытки регистрации.
        failure_reason:
            Причина ошибки.
        metadata:
            Дополнительные данные.
        request:
            HTTP-запрос. Используется для IP и User-Agent.

    Returns:
        RegistrationAttemptLog: Созданная запись попытки регистрации.
    """

    ip_address = None
    user_agent = ""

    if request is not None:
        ip_address = get_client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT", "")

    return RegistrationAttemptLog.objects.create(
        email_hash=hash_value(email) if email else "",
        phone_hash=hash_value(phone) if phone else "",
        role_code=role_code or "",
        status=status,
        failure_reason=failure_reason or "",
        ip_address=ip_address,
        user_agent=user_agent,
        metadata=metadata or {},
    )


def log_user_registered(*, user, actor=None, request=None) -> UserAuditLog:
    """
    Фиксирует регистрацию пользователя.

    Args:
        user:
            Зарегистрированный пользователь.
        actor:
            Инициатор действия.
        request:
            HTTP-запрос.

    Returns:
        UserAuditLog: Запись аудита.
    """

    return create_user_audit_log(
        actor=actor or user,
        target_user=user,
        action=UserAuditAction.USER_REGISTERED,
        message="Пользователь зарегистрирован.",
        request=request,
    )


def log_email_verified(*, user, request=None) -> UserAuditLog:
    """
    Фиксирует подтверждение email.

    Args:
        user:
            Пользователь.
        request:
            HTTP-запрос.

    Returns:
        UserAuditLog: Запись аудита.
    """

    return create_user_audit_log(
        actor=user,
        target_user=user,
        action=UserAuditAction.EMAIL_VERIFIED,
        message="Email пользователя подтверждён.",
        request=request,
    )


def log_join_request_created(*, user, join_request, request=None) -> UserAuditLog:
    """
    Фиксирует создание заявки пользователя.

    Args:
        user:
            Пользователь, создавший заявку.
        join_request:
            Созданная заявка.
        request:
            HTTP-запрос.

    Returns:
        UserAuditLog: Запись аудита.
    """

    return create_user_audit_log(
        actor=user,
        target_user=user,
        action=UserAuditAction.JOIN_REQUEST_CREATED,
        message="Создана заявка пользователя.",
        metadata={
            "join_request_id": join_request.id,
            "request_type": join_request.request_type,
        },
        request=request,
    )


def log_join_request_approved(
    *, actor, target_user, join_request, request=None
) -> UserAuditLog:
    """
    Фиксирует подтверждение заявки пользователя.

    Args:
        actor:
            Проверяющий пользователь.
        target_user:
            Пользователь, чью заявку подтвердили.
        join_request:
            Подтверждённая заявка.
        request:
            HTTP-запрос.

    Returns:
        UserAuditLog: Запись аудита.
    """

    return create_user_audit_log(
        actor=actor,
        target_user=target_user,
        action=UserAuditAction.JOIN_REQUEST_APPROVED,
        message="Заявка пользователя подтверждена.",
        metadata={
            "join_request_id": join_request.id,
            "request_type": join_request.request_type,
        },
        request=request,
    )


def log_join_request_rejected(
    *, actor, target_user, join_request, request=None
) -> UserAuditLog:
    """
    Фиксирует отклонение заявки пользователя.

    Args:
        actor:
            Проверяющий пользователь.
        target_user:
            Пользователь, чью заявку отклонили.
        join_request:
            Отклонённая заявка.
        request:
            HTTP-запрос.

    Returns:
        UserAuditLog: Запись аудита.
    """

    return create_user_audit_log(
        actor=actor,
        target_user=target_user,
        action=UserAuditAction.JOIN_REQUEST_REJECTED,
        message="Заявка пользователя отклонена.",
        metadata={
            "join_request_id": join_request.id,
            "request_type": join_request.request_type,
        },
        request=request,
    )


def log_failed_login(*, email: str = "", request=None) -> UserAuditLog:
    """
    Фиксирует неудачную попытку входа.

    Args:
        email:
            Email, который использовался при входе.
        request:
            HTTP-запрос.

    Returns:
        UserAuditLog: Запись аудита.
    """

    return create_user_audit_log(
        action=UserAuditAction.LOGIN_FAILED,
        actor=None,
        target_user=None,
        actor_type=AuditActorType.SYSTEM,
        message="Неудачная попытка входа.",
        metadata={
            "email_hash": hash_value(email) if email else "",
        },
        request=request,
    )
