from __future__ import annotations

from apps.users.models import RegistrationAttemptLog, UserAuditLog
from django.db.models import QuerySet


def get_user_audit_logs_queryset() -> QuerySet:
    """
    Возвращает базовый QuerySet записей аудита пользователей.

    Returns:
        QuerySet: Записи аудита пользователей.
    """

    return UserAuditLog.objects.select_related(
        "actor",
        "target_user",
    )


def get_audit_logs_for_user(user) -> QuerySet:
    """
    Возвращает аудит, связанный с пользователем.

    Пользователь может быть как инициатором действия,
    так и целевым пользователем.

    Args:
        user:
            Пользователь.

    Returns:
        QuerySet: Записи аудита пользователя.
    """

    if not user:
        return UserAuditLog.objects.none()

    return get_user_audit_logs_queryset().filter(
        target_user=user,
    )


def get_audit_logs_by_actor(actor) -> QuerySet:
    """
    Возвращает действия, выполненные конкретным пользователем.

    Args:
        actor:
            Инициатор действия.

    Returns:
        QuerySet: Записи аудита.
    """

    if not actor:
        return UserAuditLog.objects.none()

    return get_user_audit_logs_queryset().filter(actor=actor)


def get_audit_logs_by_action(action: str) -> QuerySet:
    """
    Возвращает записи аудита по типу действия.

    Args:
        action:
            Код действия аудита.

    Returns:
        QuerySet: Записи аудита.
    """

    if not action:
        return UserAuditLog.objects.none()

    return get_user_audit_logs_queryset().filter(action=action)


def get_registration_attempts_queryset() -> QuerySet:
    """
    Возвращает базовый QuerySet попыток регистрации.

    Returns:
        QuerySet: Попытки регистрации.
    """

    return RegistrationAttemptLog.objects.all()


def get_registration_attempts_by_email_hash(email_hash: str) -> QuerySet:
    """
    Возвращает попытки регистрации по хешу email.

    Args:
        email_hash:
            Хеш email.

    Returns:
        QuerySet: Попытки регистрации.
    """

    if not email_hash:
        return RegistrationAttemptLog.objects.none()

    return get_registration_attempts_queryset().filter(email_hash=email_hash)


def get_registration_attempts_by_phone_hash(phone_hash: str) -> QuerySet:
    """
    Возвращает попытки регистрации по хешу телефона.

    Args:
        phone_hash:
            Хеш телефона.

    Returns:
        QuerySet: Попытки регистрации.
    """

    if not phone_hash:
        return RegistrationAttemptLog.objects.none()

    return get_registration_attempts_queryset().filter(phone_hash=phone_hash)


def get_registration_attempts_by_ip(ip_address: str) -> QuerySet:
    """
    Возвращает попытки регистрации по IP-адресу.

    Args:
        ip_address:
            IP-адрес.

    Returns:
        QuerySet: Попытки регистрации.
    """

    if not ip_address:
        return RegistrationAttemptLog.objects.none()

    return get_registration_attempts_queryset().filter(ip_address=ip_address)
