from __future__ import annotations

from apps.core.exceptions import ConflictApplicationError
from apps.users.models import UserJoinRequest
from apps.users.selectors.user_join_request_selectors import (
    user_has_pending_join_request,
)
from apps.users.services.audit_services import log_join_request_created


def create_join_request(
    *,
    request_type: str,
    user,
    target_user=None,
    organization=None,
    department=None,
    group=None,
    message: str = "",
    expires_at=None,
    request=None,
) -> UserJoinRequest:
    """
    Создаёт базовую заявку пользователя.

    Args:
        request_type:
            Тип заявки.
        user:
            Пользователь, создающий заявку.
        target_user:
            Целевой пользователь.
        organization:
            Образовательная организация.
        department:
            Отделение.
        group:
            Учебная группа.
        message:
            Сообщение пользователя.
        expires_at:
            Дата истечения заявки.
        request:
            HTTP-запрос.

    Returns:
        UserJoinRequest: Созданная заявка.
    """

    if user_has_pending_join_request(
        user=user,
        request_type=request_type,
        organization=organization,
        department=department,
        group=group,
        target_user=target_user,
    ):
        raise ConflictApplicationError(
            "У пользователя уже есть ожидающая заявка такого типа.",
            code="pending_join_request_exists",
        )

    join_request = UserJoinRequest.objects.create(
        request_type=request_type,
        user=user,
        target_user=target_user,
        organization=organization,
        department=department,
        group=group,
        message=message or "",
        expires_at=expires_at,
    )

    log_join_request_created(
        user=user,
        join_request=join_request,
        request=request,
    )

    return join_request
